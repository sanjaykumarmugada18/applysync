"""Identity, revocable JWT cookie sessions, and server-side authorization."""

from collections import OrderedDict
from datetime import datetime, timedelta, timezone
from hashlib import sha256
from threading import Lock
from time import monotonic
from typing import Annotated
from uuid import UUID, uuid4
import secrets

from argon2 import PasswordHasher
from argon2.exceptions import VerificationError, InvalidHashError
from email_validator import validate_email, EmailNotValidError
from fastapi import APIRouter, Depends, HTTPException, Request, Response
import jwt
from pydantic import BaseModel, ConfigDict, Field, field_validator
from sqlalchemy import delete, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.engine import Engine

from auth_config import load_auth_settings
from database import get_engine, session_scope
from models import AuthSession, User

COOKIE = "applysync_session"
ISSUER = "applysync"
AUDIENCE = "applysync-api"
hasher = PasswordHasher()
# A missing account still incurs the same password verification work.
dummy_hash = hasher.hash(secrets.token_urlsafe(32))
router = APIRouter(prefix="/auth", tags=["authentication"])
DatabaseEngine = Annotated[Engine, Depends(get_engine)]


class Credentials(BaseModel):
    model_config = ConfigDict(extra="forbid")
    email: str = Field(max_length=254)
    password: str = Field(min_length=12, max_length=128)

    @field_validator("email")
    @classmethod
    def normalize_email(cls, value):
        try:
            return validate_email(value.strip(), check_deliverability=False,
                                  allow_smtputf8=False).normalized.lower()
        except EmailNotValidError:
            raise ValueError("Enter a valid email address.") from None


class Identity(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    email: str


class AttemptLimiter:
    """Bounded per-process throttling; never stores passwords or raw emails."""
    def __init__(self):
        self.lock = Lock()
        self.entries = OrderedDict()

    def check(self, address, email):
        now = monotonic()
        keys = [("ip", address, 50), ("email", sha256(email.encode()).hexdigest(), 10)]
        with self.lock:
            self.entries = OrderedDict((k, v) for k, v in self.entries.items() if v[0] > now - 900)
            if len(self.entries) >= 10000:
                raise HTTPException(429, "Too many attempts. Try again later.", headers={"Retry-After": "900"})
            if any(self.entries.get((kind, key), (now, 0))[1] >= limit for kind, key, limit in keys):
                raise HTTPException(429, "Too many attempts. Try again later.", headers={"Retry-After": "900"})
            for kind, key, _ in keys:
                start, count = self.entries.get((kind, key), (now, 0))
                self.entries[(kind, key)] = (start, count + 1)


def invalid_session():
    return HTTPException(401, "Authentication required")


def current_user(request: Request, engine: DatabaseEngine) -> Identity:
    token = request.cookies.get(COOKIE)
    if not token:
        raise invalid_session()
    settings = load_auth_settings()
    try:
        claims = jwt.decode(token, settings.secret, algorithms=["HS256"], issuer=ISSUER,
                            audience=AUDIENCE, options={"require": ["sub", "jti", "exp", "iat", "iss", "aud"]})
        user_id, session_id = UUID(claims["sub"]), UUID(claims["jti"])
        if (type(claims["iat"]) is not int or type(claims["exp"]) is not int
                or not 0 < claims["exp"] - claims["iat"] <= settings.lifetime):
            raise ValueError()
    except (jwt.PyJWTError, ValueError, TypeError, AttributeError):
        raise invalid_session() from None
    with session_scope(engine) as session:
        identity = session.scalar(select(User).join(AuthSession, AuthSession.user_id == User.id).where(
            User.id == user_id, AuthSession.id == session_id,
            AuthSession.expires_at > datetime.now(timezone.utc)))
        if identity is None:
            raise invalid_session()
        result = Identity.model_validate(identity)
    request.state.session_id = session_id
    return result


CurrentUser = Annotated[Identity, Depends(current_user)]


def issue_session(session, user, settings, request):
    now = datetime.now(timezone.utc).replace(microsecond=0)
    sid = uuid4()
    # Replacing a browser session revokes the previous cookie too, if valid.
    old = request.cookies.get(COOKIE)
    if old:
        try:
            claims = jwt.decode(old, settings.secret, algorithms=["HS256"], issuer=ISSUER, audience=AUDIENCE)
            session.execute(delete(AuthSession).where(AuthSession.id == UUID(claims["jti"])))
        except (jwt.PyJWTError, ValueError, KeyError, TypeError):
            pass
    session.add(AuthSession(id=sid, user_id=user.id, expires_at=now + timedelta(seconds=settings.lifetime)))
    return jwt.encode({"sub": str(user.id), "jti": str(sid), "iat": int(now.timestamp()),
                       "exp": int(now.timestamp()) + settings.lifetime, "iss": ISSUER, "aud": AUDIENCE},
                      settings.secret, algorithm="HS256")


def set_cookie(response, token, settings):
    response.set_cookie(COOKIE, token, max_age=settings.lifetime, httponly=True,
                        secure=settings.secure, samesite="lax", path="/")
    response.headers["Cache-Control"] = "no-store"


def throttle(request, payload):
    request.app.state.attempt_limiter.check(request.client.host if request.client else "unknown", payload.email)


@router.post("/register", response_model=Identity, status_code=201)
def register(payload: Credentials, request: Request, response: Response, engine: DatabaseEngine):
    settings = load_auth_settings()
    throttle(request, payload)
    password_hash = hasher.hash(payload.password)
    try:
        with session_scope(engine) as session:
            user = User(email=payload.email, password_hash=password_hash)
            session.add(user)
            session.flush()  # Database uniqueness is authoritative under concurrency.
            result = Identity.model_validate(user)
            token = issue_session(session, user, settings, request)
    except IntegrityError:
        raise HTTPException(409, "Registration could not be completed for this email.") from None
    set_cookie(response, token, settings)
    return result


@router.post("/login", response_model=Identity)
def login(payload: Credentials, request: Request, response: Response, engine: DatabaseEngine):
    settings = load_auth_settings()
    throttle(request, payload)
    with session_scope(engine) as session:
        user = session.scalar(select(User).where(User.email == payload.email))
        try:
            hasher.verify(user.password_hash if user else dummy_hash, payload.password)
        except (VerificationError, InvalidHashError):
            raise HTTPException(401, "Invalid email or password") from None
        if user is None:
            raise HTTPException(401, "Invalid email or password")
        if hasher.check_needs_rehash(user.password_hash):
            user.password_hash = hasher.hash(payload.password)
        result = Identity.model_validate(user)
        token = issue_session(session, user, settings, request)
    set_cookie(response, token, settings)
    return result


@router.get("/me", response_model=Identity)
def me(user: CurrentUser, response: Response):
    response.headers["Cache-Control"] = "no-store"
    return user


@router.post("/logout", status_code=204)
def logout(request: Request, user: CurrentUser, engine: DatabaseEngine):
    settings = load_auth_settings()
    with session_scope(engine) as session:
        session.execute(delete(AuthSession).where(AuthSession.id == request.state.session_id,
                                                 AuthSession.user_id == user.id))
    response = Response(status_code=204, headers={"Cache-Control": "no-store"})
    response.delete_cookie(COOKIE, path="/", secure=settings.secure, httponly=True, samesite="lax")
    return response
