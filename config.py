"""Explicit local database settings; never include values in errors or repr."""

import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Mapping

from dotenv import dotenv_values
from sqlalchemy import URL

ROOT = Path(__file__).resolve().parent


class ConfigurationError(ValueError):
    pass


@dataclass(frozen=True, repr=False)
class DatabaseSettings:
    host: str
    port: int
    database: str
    username: str
    password: str = field(repr=False)

    def url(self) -> URL:
        # URL.create handles special password characters without string interpolation.
        return URL.create("postgresql+psycopg", username=self.username,
                          password=self.password, host=self.host,
                          port=self.port, database=self.database)


def load_settings(target: str = "dev", *, environ: Mapping[str, str] | None = None,
                  env_file: Path | None = ROOT / ".env") -> DatabaseSettings:
    if target not in {"dev", "test"}:
        raise ConfigurationError("Database target must be dev or test.")
    values = {}
    if env_file is not None and env_file.is_file():
        values.update(dotenv_values(env_file, interpolate=False))
    values.update(os.environ if environ is None else environ)
    prefix = f"APPLYSYNC_{target.upper()}_DB_"
    keys = ["APPLYSYNC_DB_HOST", "APPLYSYNC_DB_PORT",
            prefix + "NAME", prefix + "USER", prefix + "PASSWORD"]
    if any(not values.get(key) or not values[key].strip() for key in keys):
        raise ConfigurationError("Required ApplySync database settings are missing.")
    try:
        port = int(values["APPLYSYNC_DB_PORT"])
    except (ValueError, TypeError):
        raise ConfigurationError("Database port must be an integer from 1 to 65535.") from None
    if not 1 <= port <= 65535:
        raise ConfigurationError("Database port must be an integer from 1 to 65535.")
    # This task deliberately supports only dedicated local development/test databases.
    if values["APPLYSYNC_DB_HOST"] not in {"127.0.0.1", "localhost", "::1"}:
        raise ConfigurationError("This local setup requires a loopback database host.")
    expected = f"applysync_{target}"
    if values[prefix + "NAME"] != expected or values[prefix + "USER"] != expected:
        raise ConfigurationError("Use the dedicated database and role for the selected target.")
    password = values[prefix + "PASSWORD"]
    if password.startswith("replace-with-"):
        raise ConfigurationError("Replace the example password in local configuration.")
    return DatabaseSettings(values["APPLYSYNC_DB_HOST"], port, expected, expected, password)
