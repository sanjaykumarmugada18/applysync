"""Local, explicit, transactional assignment of selected legacy record UUIDs."""
import argparse
from uuid import UUID
from sqlalchemy import select, text
from auth import Credentials
from config import load_settings
from database import build_engine, session_scope
from models import JobApplication, User


def assign(engine, email, ids):
    with session_scope(engine) as session:
        user = session.scalar(select(User).where(User.email == email))
        if user is None:
            raise ValueError("Target account must already exist.")
        rows = session.scalars(select(JobApplication).where(JobApplication.id.in_(ids)).with_for_update()).all()
        if len(rows) != len(set(ids)) or any(row.owner_id is not None for row in rows):
            raise ValueError("Every requested record must exist and be unassigned; nothing changed.")
        for row in rows:
            row.owner_id = user.id
    return len(rows)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--email")
    parser.add_argument("--ids", type=UUID, nargs="+")
    parser.add_argument("--interactive", action="store_true", help="List only unassigned UUIDs and choose locally")
    args = parser.parse_args()
    engine = build_engine(load_settings("dev"))
    try:
        with engine.connect() as connection:
            if (connection.scalar(text("select current_database()")) != "applysync_dev"
                    or connection.scalar(text("select current_user")) != "applysync_dev"):
                raise ValueError("Refusing an unexpected database target.")
        if args.interactive:
            with session_scope(engine) as session:
                ids = session.scalars(select(JobApplication.id).where(JobApplication.owner_id.is_(None))).all()
            print("Unassigned legacy record UUIDs (no record contents):")
            for id_ in ids:
                print(id_)
            args.email = input("Existing account email to receive selected records: ")
            args.ids = [UUID(value.strip()) for value in input("Explicit UUIDs to assign, separated by commas: ").split(",")]
        if not args.email or not args.ids:
            raise ValueError("An existing account and explicit UUIDs are required.")
        email = Credentials.normalize_email(args.email)
        count = assign(engine, email, args.ids)
        print(f"Assigned {count} explicitly selected legacy records transactionally.")
    except Exception:
        print("Assignment failed; no partial assignment. Verify target account and unassigned UUIDs locally.")
        raise SystemExit(1) from None
    finally:
        engine.dispose()


if __name__ == "__main__":
    main()
