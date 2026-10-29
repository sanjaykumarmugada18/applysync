"""Synthetic accounts on the checked test database; Google is always faked."""
from concurrent.futures import ThreadPoolExecutor
from datetime import timedelta
import hashlib
from urllib.parse import parse_qs, urlparse
from uuid import UUID
from threading import Event

import pytest
from sqlalchemy import select

from database import session_scope
from gmail_connector import ConnectorError
from gmail_connector.client import Grant
from gmail_routes import now
from models import GmailConnection, GmailOAuthState
from test_auth import identities, HEADERS


class FakeConnector:
    def __init__(self):
        self.grant = Grant('synthetic-subject', 'synthetic@example.com', 'synthetic-ciphertext', 'openid email gmail.readonly')
        self.exchanges = 0
        self.revocations = 0
        self.revoked = True
        self.valid = True
        self.fail = False

    def begin(self, state, *, consent):
        return 'https://accounts.google.com/o/oauth2/v2/auth?state=' + state, 'synthetic-encrypted-flow'

    def exchange(self, code, flow):
        self.exchanges += 1
        assert flow == 'synthetic-encrypted-flow'
        if self.fail:
            raise ConnectorError()
        return self.grant

    def validate_refresh(self, token):
        assert token == 'synthetic-ciphertext'
        return self.valid

    def revoke(self, token):
        assert token == 'synthetic-ciphertext'
        self.revocations += 1
        return self.revoked


@pytest.fixture
def google(monkeypatch):
    fake = FakeConnector()
    monkeypatch.setattr('gmail_routes.get_connector', lambda: fake)
    return fake


def begin(client):
    response = client.post('/gmail/start')
    assert response.status_code == 200
    assert set(response.json()) == {'authorization_url'}
    return parse_qs(urlparse(response.json()['authorization_url']).query)['state'][0]


def callback(client, state, **parameters):
    return client.get('/gmail/callback', params={'state': state, 'code': 'synthetic-code', **parameters}, follow_redirects=False)


def test_success_reauth_preserve_and_account_replacement(identities, google):
    _, account, engine = identities
    client, _ = account()
    owner = UUID(client.get('/auth/me').json()['id'])
    state = begin(client)
    with session_scope(engine) as session:
        pending = session.get(GmailOAuthState, hashlib.sha256(state.encode()).hexdigest())
        assert pending.owner_id == owner and pending.session_id and pending.expires_at > now()
        assert pending.encrypted_flow != state
    response = callback(client, state)
    assert response.status_code == 303 and response.headers['location'].endswith('result=connected')
    assert response.headers['referrer-policy'] == 'no-referrer'
    assert callback(client, state).headers['location'].endswith('result=failed')
    assert google.exchanges == 1
    status = client.get('/gmail').json()
    assert status == {'available': True, 'status': 'connected', 'email': 'synthetic@example.com', 'revocation_warning': False}
    assert 'synthetic-ciphertext' not in str(status)
    google.grant = Grant('synthetic-subject', 'renamed@example.com', None, 'openid email gmail.readonly')
    assert callback(client, begin(client)).headers['location'].endswith('result=connected')
    with session_scope(engine) as session:
        assert session.get(GmailConnection, owner).encrypted_refresh_token == 'synthetic-ciphertext'
    google.grant = Grant('different-subject', 'different@example.com', 'other-ciphertext', 'openid email gmail.readonly')
    assert callback(client, begin(client)).headers['location'].endswith('result=different_account')
    assert client.get('/gmail').json()['email'] == 'renamed@example.com'


@pytest.mark.parametrize('failure', ['expired', 'wrong_user', 'wrong_session', 'malformed', 'missing', 'denial', 'missing_code', 'provider', 'logout', 'superseded', 'disconnected'])
def test_callback_failures_consume_valid_state(identities, google, failure):
    _, account, engine = identities
    client, credentials = account()
    state = begin(client)
    original = client
    if failure == 'expired':
        with session_scope(engine) as session:
            session.get(GmailOAuthState, hashlib.sha256(state.encode()).hexdigest()).expires_at = now() - timedelta(seconds=1)
    if failure == 'wrong_user': client, _ = account('b')
    if failure == 'wrong_session':
        client, _ = account(register=False)
        assert client.post('/auth/login', json=credentials).status_code == 200
    if failure == 'malformed': state = 'bad'
    if failure == 'missing': state = ''
    if failure == 'provider': google.fail = True
    if failure == 'logout': client.post('/auth/logout')
    if failure == 'superseded': begin(client)
    if failure == 'disconnected': client.post('/gmail/disconnect')
    extra = {'error': 'access_denied'} if failure == 'denial' else {'code': ''} if failure == 'missing_code' else {}
    response = callback(client, state, **extra)
    assert response.status_code == (401 if failure == 'logout' else 303)
    if response.status_code == 303: assert response.headers['location'].endswith('result=failed')
    assert google.exchanges == int(failure == 'provider')
    if failure in {'denial', 'missing_code', 'provider'}:
        google.fail = False
        assert callback(original, state).headers['location'].endswith('result=failed')
        assert google.exchanges == int(failure == 'provider')


def test_missing_refresh_and_expired_old_grant(identities, google):
    _, account, engine = identities
    client, _ = account()
    google.grant = Grant('synthetic-subject', 'synthetic@example.com', None, 'openid email gmail.readonly')
    assert callback(client, begin(client)).headers['location'].endswith('result=reauthorization_needed')
    assert client.get('/gmail').json()['status'] == 'not_connected'
    google.grant = Grant('synthetic-subject', 'synthetic@example.com', 'synthetic-ciphertext', 'openid email gmail.readonly')
    callback(client, begin(client))
    google.grant = Grant('synthetic-subject', 'synthetic@example.com', None, 'openid email gmail.readonly')
    google.valid = False
    assert callback(client, begin(client)).headers['location'].endswith('result=reauthorization_needed')
    assert client.get('/gmail').json()['status'] == 'reauthorization_needed'


@pytest.mark.parametrize('revoked', [True, False])
def test_disconnect_repeat_concurrency_and_isolation(identities, google, revoked):
    _, account, engine = identities
    a, _ = account('a'); b, _ = account('b')
    callback(a, begin(a)); callback(b, begin(b))
    google.revoked = revoked
    with ThreadPoolExecutor(max_workers=2) as pool:
        responses = list(pool.map(lambda _: a.post('/gmail/disconnect'), range(2)))
    assert all(r.status_code == 200 and r.json()['status'] == 'disconnected' for r in responses)
    assert all(r.json()['revocation_warning'] == (not revoked) for r in responses)
    assert google.revocations == 1
    assert b.get('/gmail').json()['status'] == 'connected'
    owner = UUID(a.get('/auth/me').json()['id'])
    with session_scope(engine) as session:
        row = session.get(GmailConnection, owner)
        assert row.encrypted_refresh_token is None and row.google_subject is None and row.email is None
    assert a.post('/gmail/disconnect').status_code == 200
    assert google.revocations == 1


def test_start_disconnect_protection_and_cors(identities, google):
    app, account, _ = identities
    client, _ = account()
    for path in ['/gmail/start', '/gmail/disconnect']:
        for headers in [{'Origin': 'https://untrusted.example'}, {'X-ApplySync-CSRF': ''}]:
            assert client.post(path, headers=headers).status_code == 403
        response = client.options(path, headers={'Origin': 'https://untrusted.example', 'Access-Control-Request-Method': 'POST', 'Access-Control-Request-Headers': 'X-ApplySync-CSRF'})
        assert response.status_code == 400 and 'access-control-allow-origin' not in response.headers
        response = client.options(path, headers={**HEADERS, 'Access-Control-Request-Method': 'POST', 'Access-Control-Request-Headers': 'X-ApplySync-CSRF'})
        assert response.headers['access-control-allow-credentials'] == 'true'
    client.post('/auth/logout')
    assert client.get('/gmail').status_code == 401
    assert client.post('/gmail/start').status_code == 401
    assert client.post('/gmail/disconnect').status_code == 401


def test_callback_race_single_exchange(identities, google):
    _, account, _ = identities
    client, _ = account()
    state = begin(client)
    with ThreadPoolExecutor(max_workers=2) as pool:
        results = list(pool.map(lambda _: callback(client, state).headers['location'], range(2)))
    assert sorted(r.split('=')[-1] for r in results) == ['connected', 'failed']
    assert google.exchanges == 1


def test_unavailable_is_safe(identities, monkeypatch):
    from gmail_connector import GmailUnavailable
    def unavailable(): raise GmailUnavailable()
    monkeypatch.setattr('gmail_routes.get_connector', unavailable)
    _, account, _ = identities
    client, _ = account()
    assert client.get('/gmail').json()['available'] is False
    assert client.post('/gmail/start').status_code == 503
    assert client.get('/health').json() == {'status': 'healthy'}
    assert client.get('/applications').status_code == 200


def test_disconnect_waits_for_callback_then_removes_grant(identities, google):
    _, account, _ = identities
    client, _ = account()
    state = begin(client)
    entered, release = Event(), Event()
    exchange = google.exchange
    def delayed(code, flow):
        entered.set()
        assert release.wait(5)
        return exchange(code, flow)
    google.exchange = delayed
    with ThreadPoolExecutor(max_workers=2) as pool:
        finish = pool.submit(callback, client, state)
        assert entered.wait(5)
        disconnect = pool.submit(client.post, '/gmail/disconnect')
        release.set()
        assert finish.result().headers['location'].endswith('result=connected')
        assert disconnect.result().json()['status'] == 'disconnected'
    assert client.get('/gmail').json()['status'] == 'disconnected'
    assert google.revocations == 1


def test_logout_serializes_with_exchange_and_revokes_session(identities, google):
    _, account, _ = identities
    client, _ = account()
    state = begin(client)
    entered, release = Event(), Event()
    exchange = google.exchange
    def delayed(code, flow):
        entered.set()
        assert release.wait(5)
        return exchange(code, flow)
    google.exchange = delayed
    with ThreadPoolExecutor(max_workers=2) as pool:
        finish = pool.submit(callback, client, state)
        assert entered.wait(5)
        logout = pool.submit(client.post, '/auth/logout')
        release.set()
        assert finish.result().status_code == 303
        assert logout.result().status_code == 204
    assert client.get('/gmail').status_code == 401
    assert callback(client, state).status_code == 401
