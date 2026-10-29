"""Real cryptography/signature checks against in-memory HTTP endpoints only."""
import ast
from base64 import urlsafe_b64encode
import hashlib
import json
import logging
from pathlib import Path
import time
from urllib.parse import parse_qs, urlparse

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.asymmetric import rsa
import httpx
import jwt
import pytest

from gmail_connector.client import GmailConnector, ConnectorError, GmailUnavailable, SCOPES, get_connector
from main import OAuthAccessFilter


@pytest.mark.parametrize('failure', [None, 'nonce', 'audience', 'issuer', 'expired', 'unverified', 'scope', 'signature', 'provider', 'malformed'])
def test_exchange_encryption_pkce_and_identity(failure, caplog):
    key = Fernet.generate_key()
    private = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    jwk = {**jwt.algorithms.RSAAlgorithm.to_jwk(private.public_key(), as_dict=True), 'kid': 'synthetic-key'}
    parameters = {}
    def endpoint(request):
        if request.method == 'GET': return httpx.Response(200, json={'keys': [jwk]})
        body = parse_qs(request.content.decode())
        verifier = body['code_verifier'][0]
        assert urlsafe_b64encode(hashlib.sha256(verifier.encode()).digest()).rstrip(b'=').decode() == parameters['code_challenge'][0]
        assert body['redirect_uri'] == ['http://127.0.0.1:8000/gmail/callback']
        assert body['code'] == ['synthetic-code']
        if failure == 'provider': return httpx.Response(400, json={'error': 'synthetic-sensitive-provider-message'})
        if failure == 'malformed': return httpx.Response(200, json=[])
        claims = {'iss': 'https://accounts.google.com', 'aud': 'synthetic.apps.googleusercontent.com', 'sub': 'synthetic-subject', 'email': 'synthetic@example.com', 'email_verified': True, 'nonce': parameters['nonce'][0], 'iat': int(time.time()), 'exp': int(time.time()) + 600}
        for name, field, value in [('nonce','nonce','wrong'),('audience','aud','wrong'),('issuer','iss','https://untrusted.example'),('expired','exp',1),('unverified','email_verified',False)]:
            if failure == name: claims[field] = value
        signer = rsa.generate_private_key(public_exponent=65537, key_size=2048) if failure == 'signature' else private
        return httpx.Response(200, json={'scope': ' '.join(SCOPES) + (' extra' if failure == 'scope' else ''), 'token_type': 'Bearer', 'access_token': 'synthetic-access', 'refresh_token': 'synthetic-refresh', 'id_token': jwt.encode(claims, signer, algorithm='RS256', headers={'kid': 'synthetic-key'})})
    connector = GmailConnector('synthetic.apps.googleusercontent.com', 'synthetic-secret', key.decode(), transport=httpx.MockTransport(endpoint))
    url, flow = connector.begin('synthetic-state', consent=True)
    parameters.update(parse_qs(urlparse(url).query))
    assert set(parameters['scope'][0].split()) == SCOPES
    assert parameters['code_challenge_method'] == ['S256']
    assert parameters['access_type'] == ['offline'] and parameters['prompt'] == ['consent']
    assert parameters['nonce'][0] not in flow
    with caplog.at_level(logging.INFO):
        if failure:
            with pytest.raises(ConnectorError, match='^Gmail authorization could not be completed.$'):
                connector.exchange('synthetic-code', flow)
        else:
            grant = connector.exchange('synthetic-code', flow)
            assert grant.subject == 'synthetic-subject'
            assert grant.encrypted_refresh_token != 'synthetic-refresh'
            assert Fernet(key).decrypt(grant.encrypted_refresh_token.encode()) == b'synthetic-refresh'
            assert 'synthetic-refresh' not in repr(grant)
    assert all(secret not in caplog.text for secret in ['synthetic-secret', 'synthetic-code', 'synthetic-refresh', 'synthetic-access', 'synthetic-sensitive-provider-message'])


def test_refresh_revocation_and_wrong_key():
    key = Fernet.generate_key()
    cipher = Fernet(key).encrypt(b'synthetic-refresh').decode()
    responses = [httpx.Response(200, json={'access_token': 'synthetic-access'}), httpx.Response(400, json={'error': 'invalid_grant'}), httpx.Response(503, json={}), httpx.Response(200), httpx.Response(503)]
    def endpoint(request):
        assert request.method == 'POST' and 'synthetic-refresh' not in str(request.url)
        return responses.pop(0)
    connector = GmailConnector('synthetic-id', 'synthetic-secret', key.decode(), transport=httpx.MockTransport(endpoint))
    assert connector.validate_refresh(cipher)
    assert not connector.validate_refresh(cipher)
    with pytest.raises(ConnectorError): connector.validate_refresh(cipher)
    assert connector.revoke(cipher)
    assert not connector.revoke(cipher)
    other = GmailConnector('synthetic-id','synthetic-secret',Fernet.generate_key().decode())
    assert not other.revoke(cipher)  # fails decryption before any network call


def test_configuration_and_access_logging(monkeypatch):
    monkeypatch.setattr('gmail_connector.client.dotenv_values', lambda *a, **kw: {})
    for name in ['APPLYSYNC_GOOGLE_CLIENT_ID', 'APPLYSYNC_GOOGLE_CLIENT_SECRET', 'APPLYSYNC_GMAIL_ENCRYPTION_KEY', 'APPLYSYNC_GOOGLE_REDIRECT_URI', 'APPLYSYNC_GMAIL_FRONTEND_ORIGIN']:
        monkeypatch.delenv(name, raising=False)
    with pytest.raises(GmailUnavailable): get_connector()
    record = logging.LogRecord('uvicorn.access', logging.INFO, '', 0, '%s - "%s %s HTTP/%s" %d', ('client','GET','/gmail/callback?code=synthetic-code','1.1',303), None)
    assert OAuthAccessFilter().filter(record) is False
    record.args = ('client','GET','/health','1.1',200)
    assert OAuthAccessFilter().filter(record) is True


def test_connector_architecture_boundary():
    root = Path(__file__).resolve().parents[1]
    excluded = {'.venv', '.git', 'frontend', 'tests', 'migrations', 'docs', 'tmp', 'test-results', '__pycache__', 'gmail_connector'}
    paths = [p for p in root.rglob('*.py') if not excluded.intersection(p.relative_to(root).parts)]
    for path in paths:
        tree = ast.parse(path.read_text(encoding='utf-8'))
        imports = [n.module or '' for n in ast.walk(tree) if isinstance(n, ast.ImportFrom)]
        imports += [alias.name for n in ast.walk(tree) if isinstance(n, ast.Import) for alias in n.names]
        assert not any(n.startswith(('google', 'googleapiclient', 'oauthlib', 'cryptography')) for n in imports), path.name
        text = path.read_text(encoding='utf-8')
        assert 'oauth2.googleapis.com' not in text and 'gmail.googleapis.com' not in text, path.name
    connector = (root/'gmail_connector/client.py').read_text()
    assert 'messages.' not in connector and 'gmail.googleapis.com' not in connector
