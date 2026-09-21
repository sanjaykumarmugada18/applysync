"""Print schema metadata only, never configuration values or application rows."""

import argparse
import json

from sqlalchemy import inspect, text
from sqlalchemy.exc import SQLAlchemyError

from config import ConfigurationError, load_settings
from database import build_engine


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("target", choices=["dev", "test"])
    args = parser.parse_args()
    engine = None
    try:
        engine = build_engine(load_settings(args.target))
        with engine.connect() as connection:
            actual = connection.scalar(text("SELECT current_database()"))
            if actual != f"applysync_{args.target}":
                raise ConfigurationError("Unexpected database; inspection stopped.")
            schema = inspect(connection)
            result = {
                "target": args.target,
                "revision": connection.scalar(text("SELECT version_num FROM alembic_version")),
                "columns": [{"name": c["name"], "type": str(c["type"]),
                             "timezone": getattr(c["type"], "timezone", None),
                             "nullable": c["nullable"], "default": c["default"]}
                            for c in schema.get_columns("job_applications")],
                "primary_key": schema.get_pk_constraint("job_applications"),
                "checks": schema.get_check_constraints("job_applications"),
                "unique_constraints": schema.get_unique_constraints("job_applications"),
            }
            print(json.dumps(result, indent=2))
        return 0
    except (ConfigurationError, SQLAlchemyError):
        print("Schema inspection failed; check local configuration and migration status. Details suppressed.")
        return 1
    finally:
        if engine is not None:
            engine.dispose()


if __name__ == "__main__":
    raise SystemExit(main())
