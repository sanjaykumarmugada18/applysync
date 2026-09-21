"""Run locally once: prompt for admin access, never print/store its password."""

import getpass
import os
from pathlib import Path
import secrets
import sys

import psycopg
from psycopg import sql

ROOT = Path(__file__).resolve().parents[1]
NAMES = ("applysync_dev", "applysync_test")


def provision(connection, passwords):
    # Check both names before any changes. Never adopt, drop, or reset existing data.
    for name in NAMES:
        if connection.execute("SELECT 1 FROM pg_database WHERE datname = %s", (name,)).fetchone():
            raise RuntimeError("A requested database already exists; stopped without adopting it.")
        if connection.execute("SELECT 1 FROM pg_roles WHERE rolname = %s", (name,)).fetchone():
            raise RuntimeError("A requested role already exists; stopped without adopting it.")
    config = ROOT / ".env"
    lines = ["APPLYSYNC_DB_HOST=127.0.0.1", "APPLYSYNC_DB_PORT=5432"]
    for target, name in zip(("DEV", "TEST"), NAMES):
        lines.extend([f"APPLYSYNC_{target}_DB_NAME={name}",
                      f"APPLYSYNC_{target}_DB_USER={name}",
                      f"APPLYSYNC_{target}_DB_PASSWORD={passwords[name]}"])
    # Exclusive creation prevents overwriting local configuration. Store generated
    # credentials before DDL so a partial setup can be diagnosed without losing them.
    with config.open("x", encoding="utf-8") as stream:
        stream.write("\n".join(lines) + "\n")
    for name in NAMES:
        # Send a SCRAM verifier, not a plaintext password, in the role DDL.
        verifier = connection.pgconn.encrypt_password(
            passwords[name].encode(), name.encode(), b"scram-sha-256").decode()
        connection.execute(sql.SQL(
            "CREATE ROLE {} LOGIN NOSUPERUSER NOCREATEDB NOCREATEROLE NOREPLICATION PASSWORD {}"
        ).format(sql.Identifier(name), sql.Literal(verifier)))
        connection.execute(sql.SQL("CREATE DATABASE {} OWNER {} TEMPLATE template0").format(
            sql.Identifier(name), sql.Identifier(name)))
        connection.execute(sql.SQL("REVOKE ALL ON DATABASE {} FROM PUBLIC").format(sql.Identifier(name)))


def main():
    if (ROOT / ".env").exists():
        print("Local .env already exists; nothing changed. Request a setup-state review.")
        return 1
    print("Creates applysync_dev and applysync_test only; existing names cause refusal.")
    print("Uses the local PostgreSQL maintenance database postgres for administrative DDL.")
    username = input("Local PostgreSQL administrator username [postgres]: ").strip() or "postgres"
    password = getpass.getpass("Local PostgreSQL administrator password (hidden): ")
    try:
        with psycopg.connect(host="127.0.0.1", port=5432, dbname="postgres",
                             user=username, password=password, passfile=os.devnull,
                             connect_timeout=5, autocommit=True) as connection:
            provision(connection, {name: secrets.token_urlsafe(32) for name in NAMES})
        print("Dedicated databases and roles created; generated credentials saved only to ignored .env.")
        print("No application migrations have been applied. Return to Codex for verification.")
        return 0
    except (psycopg.Error, OSError, RuntimeError):
        print("Setup stopped; diagnostic details suppressed to protect credentials.")
        print("If .env now exists, setup may be partial: do not delete it or rerun blindly.")
        print("Request a setup-state review. Existing databases were not adopted or deleted.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
