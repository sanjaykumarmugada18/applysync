"""Migration rehearsal in transient schemas inside the verified test database."""
from datetime import date
from uuid import uuid4

from alembic import command
from alembic.config import Config
from sqlalchemy import inspect, text
import pytest


@pytest.mark.parametrize("legacy", [False, True])
def test_upgrade_preserves_legacy_and_repeats(test_engine, legacy):
    schema = "migration_test_" + uuid4().hex
    # All DDL and fixtures rolled back; no public tables or dev data touched.
    with test_engine.connect() as connection:
        transaction = connection.begin()
        try:
            assert connection.scalar(text("select current_database()")) == "applysync_test"
            assert connection.scalar(text("select current_user")) == "applysync_test"
            connection.execute(text(f'CREATE SCHEMA "{schema}"'))
            connection.execute(text(f'SET LOCAL search_path TO "{schema}"'))
            config = Config("alembic.ini")
            config.attributes["connection"] = connection
            command.upgrade(config, "0001")
            id_ = uuid4()
            if legacy:
                connection.execute(text("INSERT INTO job_applications (id,company,role,applied_on) VALUES (:id,'Synthetic legacy','Engineer',:day)"), {"id": id_, "day": date(2026, 9, 1)})
            command.upgrade(config, "0002")
            command.upgrade(config, "0002")
            assert connection.scalar(text("select version_num from alembic_version")) == "0002"
            assert set(inspect(connection).get_table_names(schema=schema)) == {"alembic_version", "users", "auth_sessions", "job_applications"}
            assert connection.scalar(text("select count(*) from job_applications")) == int(legacy)
            if legacy:
                row = connection.execute(text("select id,company,owner_id from job_applications")).one()
                assert row == (id_, "Synthetic legacy", None)
        finally:
            transaction.rollback()
