"""Explicit cookie topology and signing configuration; never reveal values."""

from dataclasses import dataclass
import os
import re
from urllib.parse import urlsplit

from dotenv import dotenv_values

from config import ConfigurationError, ROOT

LOCAL_ORIGINS = tuple(f"http://{host}:{port}" for host in ("localhost", "127.0.0.1")
                      for port in (5173, 4173))


def values():
    return {**dotenv_values(ROOT / ".env", interpolate=False), **os.environ}


def allowed_origins():
    configured = values().get("APPLYSYNC_AUTH_ORIGINS")
    origins = tuple(configured.split(",")) if configured else LOCAL_ORIGINS
    for origin in origins:
        url = urlsplit(origin)
        if (url.scheme not in {"http", "https"} or not url.hostname or url.username
                or url.password or url.query or url.fragment or url.path
                or (url.scheme == "http" and origin not in LOCAL_ORIGINS)):
            raise ConfigurationError("Authentication origins must be explicit trusted origins.")
    return origins


@dataclass(frozen=True, repr=False)
class AuthSettings:
    secret: str
    secure: bool
    lifetime: int = 8 * 60 * 60


def load_auth_settings():
    settings = values()
    secret = settings.get("APPLYSYNC_AUTH_SECRET", "")
    mode = settings.get("APPLYSYNC_AUTH_MODE", "")
    if not re.fullmatch(r"[0-9a-fA-F]{64,}", secret) or len(set(secret)) < 12:
        raise ConfigurationError("Generate a strong authentication signing secret locally.")
    if mode not in {"local", "production"}:
        raise ConfigurationError("Set authentication mode explicitly to local or production.")
    if mode == "production" and any(not o.startswith("https://") for o in allowed_origins()):
        raise ConfigurationError("Production authentication requires HTTPS origins.")
    return AuthSettings(secret, mode == "production")
