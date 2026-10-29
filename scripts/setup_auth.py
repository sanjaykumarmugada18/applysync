"""Append local auth configuration once without reading out or replacing secrets."""
import secrets
from dotenv import dotenv_values
from config import ROOT


def main():
    path = ROOT / ".env"
    existing = dotenv_values(path, interpolate=False) if path.exists() else {}
    additions = []
    if "APPLYSYNC_AUTH_SECRET" not in existing:
        additions.append("APPLYSYNC_AUTH_SECRET=" + secrets.token_hex(32))
    if "APPLYSYNC_AUTH_MODE" not in existing:
        additions.append("APPLYSYNC_AUTH_MODE=local")
    if additions:
        with path.open("a", encoding="utf-8") as stream:
            stream.write("\n" + "\n".join(additions) + "\n")
    print("Local authentication settings checked; existing values preserved. No secrets displayed.")


if __name__ == "__main__":
    main()
