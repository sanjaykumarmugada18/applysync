"""Security tests use only verified applysync_test and synthetic identities."""
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta, timezone
import secrets
from uuid import UUID, uuid4

from fastapi.testclient import TestClient
import jwt
import pytest
from sqlalchemy import delete, func, select

from auth import COOKIE, hasher, AttemptLimiter
from auth_config import load_auth_settings
from database import session_scope
from main import create_app
from models import AuthSession, JobApplication, User

HEADERS = {"Origin": "http://127.0.0.1:5173", "X-ApplySync-CSRF": "1"}
DATA = {"company": "Synthetic private company", "role": "Engineer", "applied_on": "2026-09-01"}


@pytest.fixture
def identities(test_engine, monkeypatch):
    monkeypatch.setenv("APPLYSYNC_AUTH_SECRET", secrets.token_hex(32))
    monkeypatch.setenv("APPLYSYNC_AUTH_MODE", "local")
    app = create_app("test")
    app.state.engine = test_engine
    prefix = str(uuid4())
    password = secrets.token_urlsafe(24)
    clients = []
    def account(suffix="a", register=True):
        client = TestClient(app, headers=HEADERS)
        clients.append(client)
        credentials = {"email": f"{prefix}-{suffix}@example.com", "password": password}
        if register:
            response = client.post("/auth/register", json=credentials)
            assert response.status_code == 201
        return client, credentials
    try:
        yield app, account, test_engine
    finally:
        for client in clients:
            client.close()
        with session_scope(test_engine) as session:
            ids = select(User.id).where(User.email.startswith(prefix))
            session.execute(delete(JobApplication).where(JobApplication.owner_id.in_(ids)))
            session.execute(delete(AuthSession).where(AuthSession.user_id.in_(ids)))
            session.execute(delete(User).where(User.email.startswith(prefix)))


def test_identity_hash_normalization_duplicate_logout_and_replay(identities):
    app, account, engine = identities
    client, credentials = account()
    identity = client.get("/auth/me").json()
    assert set(identity) == {"id", "email"}
    with session_scope(engine) as session:
        user = session.get(User, UUID(identity["id"]))
        assert user.password_hash.startswith("$argon2id$")
        assert user.password_hash != credentials["password"]
        assert hasher.verify(user.password_hash, credentials["password"])
    duplicate = client.post("/auth/register", json={**credentials, "email": " " + credentials["email"].upper() + " "})
    assert duplicate.status_code == 409
    old_cookie = client.cookies.get(COOKIE)
    logout = client.post("/auth/logout")
    assert logout.status_code == 204 and "Max-Age=0" in logout.headers["set-cookie"]
    assert client.get("/auth/me").status_code == 401
    client.cookies.set(COOKIE, old_cookie)
    assert client.get("/auth/me").status_code == 401
    client.cookies.clear()
    login = client.post("/auth/login", json=credentials)
    assert login.status_code == 200
    assert "HttpOnly" in login.headers["set-cookie"] and "SameSite=lax" in login.headers["set-cookie"]
    assert "Secure" not in login.headers["set-cookie"]
    assert client.get("/auth/me").json() == identity
    for email in [credentials["email"], "absent@example.com"]:
        failure = client.post("/auth/login", json={"email": email, "password": "incorrect password"})
        assert failure.status_code == 401 and failure.json() == {"detail": "Invalid email or password"}


def test_ownership_before_pagination_and_forgery(identities):
    _, account, engine = identities
    a, _ = account("a")
    b, _ = account("b")
    own = []
    foreign = b.post("/applications", json=DATA).json()
    for _ in range(3):
        response = a.post("/applications", json=DATA)
        assert response.status_code == 201
        own.append(response.json())
    assert a.get("/applications?limit=1&offset=1").json()["items"] == [own[1]]
    assert b.get("/applications").json()["items"] == [foreign]
    for id_ in [foreign["id"], str(uuid4())]:
        response = a.get("/applications/" + id_)
        assert response.status_code == 404 and response.json() == {"detail": "Application not found"}
    assert a.post("/applications", json={**DATA, "owner_id": b.get("/auth/me").json()["id"]}).status_code == 422
    legacy_id = uuid4()
    try:
        with session_scope(engine) as session:
            session.add(JobApplication(id=legacy_id, company="Synthetic legacy", role="Engineer", applied_on=datetime.now().date()))
        assert a.get(f"/applications/{legacy_id}").status_code == 404
        assert b.get(f"/applications/{legacy_id}").status_code == 404
        assert len(a.get("/applications").json()["items"]) == 3
    finally:
        with session_scope(engine) as session:
            session.execute(delete(JobApplication).where(JobApplication.id == legacy_id))


@pytest.mark.parametrize("kind", ["missing", "malformed", "tampered", "expired", "subject", "algorithm", "claims", "revoked"])
def test_invalid_sessions(identities, kind):
    _, account, engine = identities
    client, _ = account()
    token = client.cookies.get(COOKIE)
    settings = load_auth_settings()
    claims = jwt.decode(token, settings.secret, algorithms=["HS256"], audience="applysync-api")
    client.cookies.clear()
    if kind == "malformed": token = "invalid"
    if kind == "tampered": token = jwt.encode(claims, secrets.token_hex(32), algorithm="HS256")
    if kind == "expired":
        claims["exp"] = claims["iat"] - 1
        token = jwt.encode(claims, settings.secret, algorithm="HS256")
    if kind == "subject":
        claims["sub"] = "not-a-uuid"
        token = jwt.encode(claims, settings.secret, algorithm="HS256")
    if kind == "algorithm": token = jwt.encode(claims, settings.secret, algorithm="HS384")
    if kind == "claims":
        del claims["jti"]
        token = jwt.encode(claims, settings.secret, algorithm="HS256")
    if kind == "revoked":
        with session_scope(engine) as session:
            session.execute(delete(AuthSession).where(AuthSession.id == UUID(claims["jti"])))
    if kind != "missing": client.cookies.set(COOKIE, token)
    for path in ["/auth/me", "/applications", "/applications/" + str(uuid4())]:
        response = client.get(path)
        assert response.status_code == 401 and response.json() == {"detail": "Authentication required"}
    assert client.get("/health").json() == {"status": "healthy"}


@pytest.mark.parametrize("headers", [{}, {"Origin": "http://127.0.0.1:5173"}, {"X-ApplySync-CSRF": "1"},
    {"Origin": "https://evil.example", "X-ApplySync-CSRF": "1"},
    {"Origin": "http://127.0.0.1:5173", "X-ApplySync-CSRF": "wrong"},
    {"Origin": "null", "X-ApplySync-CSRF": "1"}])
def test_csrf_all_mutations(identities, headers):
    app, account, _ = identities
    client, creds = account()
    client.headers.clear()
    for path in ["/auth/register", "/auth/login", "/auth/logout", "/applications"]:
        assert client.post(path, json=creds, headers=headers).status_code == 403
    assert client.get("/auth/me").status_code == 200


def test_concurrent_duplicate(identities):
    app, account, engine = identities
    _, creds = account(register=False)
    def register(_):
        with TestClient(app, headers=HEADERS) as client:
            return client.post("/auth/register", json=creds).status_code
    with ThreadPoolExecutor(max_workers=2) as pool:
        assert sorted(pool.map(register, range(2))) == [201, 409]
    with session_scope(engine) as session:
        assert session.scalar(select(func.count()).select_from(User).where(User.email == creds["email"])) == 1


def test_validation_does_not_echo_password(identities):
    _, account, _ = identities
    client, creds = account(register=False)
    for password in ["sentinel!", "x" * 129]:
        response = client.post("/auth/register", json={**creds, "password": password})
        assert response.status_code == 422 and password not in response.text
        assert all("input" not in item and "ctx" not in item for item in response.json()["detail"])
    assert client.post("/auth/register", json={**creds, "email": "invalid"}).status_code == 422


def test_throttle():
    from fastapi import HTTPException
    limiter = AttemptLimiter()
    for _ in range(10): limiter.check("synthetic-client", "synthetic@example.com")
    with pytest.raises(HTTPException) as caught:
        limiter.check("synthetic-client", "synthetic@example.com")
    assert caught.value.status_code == 429


def test_production_cookie_and_missing_config(monkeypatch):
    from auth import set_cookie
    from fastapi import Response
    from config import ConfigurationError
    monkeypatch.setenv("APPLYSYNC_AUTH_SECRET", secrets.token_hex(32))
    monkeypatch.setenv("APPLYSYNC_AUTH_MODE", "production")
    monkeypatch.setenv("APPLYSYNC_AUTH_ORIGINS", "https://app.example.com")
    response = Response()
    set_cookie(response, "synthetic-not-a-token", load_auth_settings())
    assert "Secure" in response.headers["set-cookie"] and "HttpOnly" in response.headers["set-cookie"]
    monkeypatch.setenv("APPLYSYNC_AUTH_SECRET", "")
    with pytest.raises(ConfigurationError): load_auth_settings()


def test_password_spaces_and_server_session_expiry(identities):
    _, account, engine = identities
    client, creds = account(register=False)
    spaced = {**creds, "password": " " + creds["password"] + " "}
    assert client.post("/auth/register", json=spaced).status_code == 201
    assert client.post("/auth/login", json=creds).status_code == 401
    assert client.post("/auth/login", json=spaced).status_code == 200
    id_ = UUID(client.get("/auth/me").json()["id"])
    with session_scope(engine) as session:
        for row in session.scalars(select(AuthSession).where(AuthSession.user_id == id_)):
            row.expires_at = datetime.now(timezone.utc) - timedelta(seconds=1)
    assert client.get("/auth/me").status_code == 401


def test_local_assignment_is_explicit_atomic_and_scoped(identities):
    from scripts.assign_legacy import assign
    _, account, engine = identities
    client, creds = account()
    ids = [uuid4(), uuid4()]
    try:
        with session_scope(engine) as session:
            for id_ in ids:
                session.add(JobApplication(id=id_, company="Synthetic legacy", role="Engineer", applied_on=datetime.now().date()))
        with pytest.raises(ValueError): assign(engine, "absent@example.com", ids)
        with pytest.raises(ValueError): assign(engine, creds["email"], [ids[0], uuid4()])
        assert client.get("/applications").json()["items"] == []
        assert assign(engine, creds["email"], [ids[0]]) == 1
        assert client.get(f"/applications/{ids[0]}").status_code == 200
        assert client.get(f"/applications/{ids[1]}").status_code == 404
        with pytest.raises(ValueError): assign(engine, creds["email"], ids)
        assert client.get(f"/applications/{ids[1]}").status_code == 404
    finally:
        with session_scope(engine) as session:
            session.execute(delete(JobApplication).where(JobApplication.id.in_(ids)))


def test_auth_configuration_failure_is_generic_and_health_still_works(identities, monkeypatch, caplog):
    _, account, _ = identities
    client, creds = account(register=False)
    monkeypatch.setenv("APPLYSYNC_AUTH_SECRET", "invalid-private-sentinel")
    response = client.post("/auth/register", json=creds)
    assert response.status_code == 500 and response.json() == {"detail": "Internal server error"}
    assert "invalid-private-sentinel" not in response.text + caplog.text
    assert creds["password"] not in response.text + caplog.text
    assert client.get("/health").json() == {"status": "healthy"}
