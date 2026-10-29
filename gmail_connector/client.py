"""Narrow Google OAuth operations. No mailbox/message operations in Task 1."""
from base64 import urlsafe_b64encode
from dataclasses import dataclass
import hashlib
import json
import os
import re
import secrets
from urllib.parse import urlencode

from cryptography.fernet import Fernet, InvalidToken
from dotenv import dotenv_values
import httpx
import jwt

from config import ROOT

AUTHORIZATION = "https://accounts.google.com/o/oauth2/v2/auth"
TOKEN = "https://oauth2.googleapis.com/token"
REVOKE = "https://oauth2.googleapis.com/revoke"
CERTS = "https://www.googleapis.com/oauth2/v3/certs"
SCOPES = frozenset({"openid", "email", "https://www.googleapis.com/auth/gmail.readonly"})
REDIRECT = "http://127.0.0.1:8000/gmail/callback"
FRONTEND = "http://127.0.0.1:5173"


class ConnectorError(Exception):
    def __init__(self):
        super().__init__("Gmail authorization could not be completed.")


class GmailUnavailable(ConnectorError):
    pass


@dataclass(frozen=True, repr=False)
class Grant:
    subject: str
    email: str
    encrypted_refresh_token: str | None
    scopes: str


class GmailConnector:
    def __init__(self, client_id, client_secret, encryption_key, *, transport=None):
        self._client_id = client_id
        self._client_secret = client_secret
        try:
            self._cipher = Fernet(encryption_key.encode())
        except (ValueError, TypeError):
            raise GmailUnavailable() from None
        self._transport = transport

    def _request(self, method, url, **kwargs):
        # No debug logging, request URLs containing tokens, redirects or ambient proxies.
        try:
            with httpx.Client(timeout=10, trust_env=False, follow_redirects=False,
                              transport=self._transport) as client:
                return client.request(method, url, **kwargs)
        except httpx.HTTPError:
            raise ConnectorError() from None

    def _seal(self, value):
        return self._cipher.encrypt(value.encode()).decode()

    def _open(self, value):
        try:
            return self._cipher.decrypt(value.encode()).decode()
        except (InvalidToken, ValueError, UnicodeError, AttributeError):
            raise ConnectorError() from None

    def begin(self, state, *, consent):
        verifier, nonce = secrets.token_urlsafe(64), secrets.token_urlsafe(32)
        challenge = urlsafe_b64encode(hashlib.sha256(verifier.encode()).digest()).rstrip(b"=").decode()
        parameters = {"client_id": self._client_id, "redirect_uri": REDIRECT,
            "response_type": "code", "scope": " ".join(sorted(SCOPES)),
            "access_type": "offline", "state": state, "nonce": nonce,
            "code_challenge": challenge, "code_challenge_method": "S256",
            "include_granted_scopes": "false", "prompt": "consent" if consent else "select_account"}
        return AUTHORIZATION + "?" + urlencode(parameters), self._seal(json.dumps({"verifier": verifier, "nonce": nonce}))

    def exchange(self, code, encrypted_flow):
        try:
            flow = json.loads(self._open(encrypted_flow))
            response = self._request("POST", TOKEN, data={"grant_type": "authorization_code",
                "client_id": self._client_id, "client_secret": self._client_secret,
                "redirect_uri": REDIRECT, "code": code, "code_verifier": flow["verifier"]})
            if response.status_code != 200:
                raise ConnectorError()
            tokens = response.json()
            granted = set(tokens["scope"].split())
            if "https://www.googleapis.com/auth/userinfo.email" in granted:
                granted.remove("https://www.googleapis.com/auth/userinfo.email")
                granted.add("email")
            if granted != SCOPES or tokens.get("token_type", "").lower() != "bearer":
                raise ConnectorError()
            # Only JWKS from the fixed Google endpoint; never trust token jku/x5u.
            header = jwt.get_unverified_header(tokens["id_token"])
            response = self._request("GET", CERTS)
            if response.status_code != 200 or header.get("alg") != "RS256":
                raise ConnectorError()
            key = next(k for k in response.json()["keys"] if k.get("kid") == header.get("kid") and k.get("kty") == "RSA")
            claims = jwt.decode(tokens["id_token"], jwt.PyJWK.from_dict(key).key,
                algorithms=["RS256"], audience=self._client_id,
                issuer=["https://accounts.google.com", "accounts.google.com"],
                options={"require": ["iss", "aud", "exp", "iat", "sub", "nonce", "email", "email_verified"]})
            if (claims["nonce"] != flow["nonce"] or claims["email_verified"] is not True
                    or not isinstance(claims["sub"], str) or not 1 <= len(claims["sub"]) <= 255
                    or not isinstance(claims["email"], str) or len(claims["email"]) > 254
                    or "@" not in claims["email"]
                    or claims.get("azp", self._client_id) != self._client_id):
                raise ConnectorError()
            refresh = tokens.get("refresh_token")
            if refresh is not None and (not isinstance(refresh, str) or not refresh or len(refresh) > 8192):
                raise ConnectorError()
            return Grant(claims["sub"], claims["email"], self._seal(refresh) if refresh else None,
                         " ".join(sorted(granted)))
        except (KeyError, ValueError, TypeError, AttributeError, StopIteration, jwt.PyJWTError):
            raise ConnectorError() from None

    def validate_refresh(self, encrypted_token):
        """Prove an old refresh grant is still usable before preserving it; no mail read."""
        response = self._request("POST", TOKEN, data={"grant_type": "refresh_token",
            "client_id": self._client_id, "client_secret": self._client_secret,
            "refresh_token": self._open(encrypted_token)})
        try:
            payload = response.json()
            if response.status_code == 400 and payload.get("error") == "invalid_grant":
                return False
            if response.status_code != 200 or not isinstance(payload.get("access_token"), str) or not payload["access_token"]:
                raise ConnectorError()
            return True
        except (ValueError, AttributeError):
            raise ConnectorError() from None

    def revoke(self, encrypted_token):
        try:
            response = self._request("POST", REVOKE, data={"token": self._open(encrypted_token)})
            return response.status_code == 200
        except ConnectorError:
            return False


def get_connector():
    values = {**dotenv_values(ROOT / ".env", interpolate=False), **os.environ}
    keys = ["APPLYSYNC_GOOGLE_CLIENT_ID", "APPLYSYNC_GOOGLE_CLIENT_SECRET", "APPLYSYNC_GMAIL_ENCRYPTION_KEY"]
    if any(not values.get(key) or values[key].startswith("replace-") for key in keys):
        raise GmailUnavailable()
    if (not re.fullmatch(r"[A-Za-z0-9._-]+\.apps\.googleusercontent\.com", values[keys[0]])
            or values.get("APPLYSYNC_GOOGLE_REDIRECT_URI") != REDIRECT
            or values.get("APPLYSYNC_GMAIL_FRONTEND_ORIGIN") != FRONTEND
            or values[keys[2]] == values.get("APPLYSYNC_AUTH_SECRET")):
        raise GmailUnavailable()
    return GmailConnector(*(values[key] for key in keys))


def generate_key():
    """Called only by the local setup utility; never display the return value."""
    return Fernet.generate_key().decode()
