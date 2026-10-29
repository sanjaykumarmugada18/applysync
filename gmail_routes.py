"""Authenticated connection orchestration; provider/crypto code stays in connector."""
from datetime import datetime, timedelta, timezone
import hashlib
import re
import secrets
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from sqlalchemy import delete, select
from sqlalchemy.engine import Engine

from auth import CurrentUser
from database import get_engine, session_scope
from gmail_connector import ConnectorError, GmailUnavailable, get_connector
from models import AuthSession, GmailConnection, GmailOAuthState, User

router = APIRouter(prefix="/gmail", tags=["gmail connection"])
DatabaseEngine = Annotated[Engine, Depends(get_engine)]
FRONTEND_DESTINATION = "http://127.0.0.1:5173/settings/gmail"


class ConnectionStatus(BaseModel):
    available: bool
    status: str
    email: str | None = None
    revocation_warning: bool = False


class StartResult(BaseModel):
    authorization_url: str


def now():
    return datetime.now(timezone.utc)


def lock_owner(session, user, request):
    session.scalar(select(User.id).where(User.id == user.id).with_for_update())
    if not session.scalar(select(AuthSession.id).where(AuthSession.id == request.state.session_id,
            AuthSession.user_id == user.id, AuthSession.expires_at > now()).with_for_update()):
        raise HTTPException(401, "Authentication required")


@router.get("", response_model=ConnectionStatus)
def status(user: CurrentUser, engine: DatabaseEngine):
    try:
        get_connector()
        available = True
    except GmailUnavailable:
        available = False
    with session_scope(engine) as session:
        row = session.get(GmailConnection, user.id)
        return ConnectionStatus(available=available, status=row.status if row else "not_connected",
            email=row.email if row else None, revocation_warning=row.revocation_warning if row else False)


@router.post("/start", response_model=StartResult)
def start(user: CurrentUser, engine: DatabaseEngine, request: Request):
    try:
        connector = get_connector()
    except GmailUnavailable:
        raise HTTPException(503, "Gmail connection is unavailable. Check local setup.") from None
    state = secrets.token_urlsafe(32)
    with session_scope(engine) as session:
        lock_owner(session, user, request)
        connection = session.get(GmailConnection, user.id)
        consent = connection is None or connection.status != "connected"
        url, encrypted_flow = connector.begin(state, consent=consent)
        session.execute(delete(GmailOAuthState).where(GmailOAuthState.owner_id == user.id))
        session.add(GmailOAuthState(state_hash=hashlib.sha256(state.encode()).hexdigest(),
            owner_id=user.id, session_id=request.state.session_id, encrypted_flow=encrypted_flow,
            expires_at=now() + timedelta(minutes=10)))
    return StartResult(authorization_url=url)


def result_redirect(result):
    return RedirectResponse(FRONTEND_DESTINATION + "?result=" + result, status_code=303,
                            headers={"Cache-Control": "no-store", "Referrer-Policy": "no-referrer"})


@router.get("/callback")
def callback(user: CurrentUser, engine: DatabaseEngine, request: Request):
    # Read manually so validation never echoes provider codes or query contents.
    params = request.query_params
    state = params.get("state", "")
    if len(params.getlist("state")) != 1 or not re.fullmatch(r"[A-Za-z0-9_-]{43}", state):
        return result_redirect("failed")
    digest = hashlib.sha256(state.encode()).hexdigest()
    with session_scope(engine) as session:
        lock_owner(session, user, request)
        pending = session.get(GmailOAuthState, digest)
        if (pending is None or pending.owner_id != user.id or pending.session_id != request.state.session_id
                or pending.used_at is not None or pending.expires_at <= now()):
            return result_redirect("failed")
        flow = pending.encrypted_flow
        pending.used_at = now()
        pending.encrypted_flow = None
    # Consumption commits before code exchange, even on denial/provider failure.
    if params.get("error") or len(params.getlist("code")) != 1 or not 1 <= len(params.get("code", "")) <= 4096:
        return result_redirect("failed")
    try:
        connector = get_connector()
        with session_scope(engine) as session:
            lock_owner(session, user, request)
            # Disconnect/new start/logout invalidates pending callbacks, including races.
            pending = session.get(GmailOAuthState, digest)
            if pending is None or pending.expires_at <= now():
                return result_redirect("failed")
            grant = connector.exchange(params["code"], flow)
            row = session.get(GmailConnection, user.id)
            if row and row.status != "disconnected" and row.google_subject != grant.subject:
                return result_redirect("different_account")
            refresh = grant.encrypted_refresh_token
            if not refresh and row and row.google_subject == grant.subject and row.status == "connected" and row.encrypted_refresh_token:
                if connector.validate_refresh(row.encrypted_refresh_token):
                    refresh = row.encrypted_refresh_token
                else:
                    row.status = "reauthorization_needed"
                    row.updated_at = now()
            if not refresh:
                return result_redirect("reauthorization_needed")
            if row is None:
                row = GmailConnection(owner_id=user.id)
                session.add(row)
            row.google_subject, row.email = grant.subject, grant.email
            row.encrypted_refresh_token, row.granted_scopes = refresh, grant.scopes
            row.status, row.revocation_warning = "connected", False
            row.connected_at, row.updated_at = now(), now()
        return result_redirect("connected")
    except ConnectorError:
        return result_redirect("failed")


@router.post("/disconnect", response_model=ConnectionStatus)
def disconnect(user: CurrentUser, engine: DatabaseEngine, request: Request):
    with session_scope(engine) as session:
        lock_owner(session, user, request)
        session.execute(delete(GmailOAuthState).where(GmailOAuthState.owner_id == user.id))
        row = session.get(GmailConnection, user.id)
        if row is None:
            row = GmailConnection(owner_id=user.id, status="disconnected", updated_at=now(), revocation_warning=False)
            session.add(row)
        token = row.encrypted_refresh_token
        row.encrypted_refresh_token = None
        row.google_subject = row.email = row.granted_scopes = None
        row.status, row.updated_at = "disconnected", now()
        if token:
            try:
                revoked = get_connector().revoke(token)
            except ConnectorError:
                revoked = False
            row.revocation_warning = not revoked
        # Serialize provider revocation and new grants under the same owner lock.
        # Provider timeout/failure is a warning, not a rollback of local disconnection.
        response = ConnectionStatus(available=True, status="disconnected", revocation_warning=row.revocation_warning)
    return response
