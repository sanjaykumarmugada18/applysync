from datetime import date
from uuid import UUID, uuid4

import pytest
from sqlalchemy import delete, inspect, select
from sqlalchemy.exc import IntegrityError

from database import session_scope
from models import JobApplication

pytestmark = pytest.mark.database


def test_actual_schema(test_engine):
    schema = inspect(test_engine)
    columns = {column["name"]: column for column in schema.get_columns("job_applications")}
    assert set(columns) == {"id", "company", "role", "applied_on", "created_at"}
    assert all(not column["nullable"] for column in columns.values())
    assert columns["company"]["type"].length == 200
    assert columns["role"]["type"].length == 200
    assert columns["created_at"]["type"].timezone
    assert columns["created_at"]["default"] == "now()"
    assert schema.get_pk_constraint("job_applications")["constrained_columns"] == ["id"]
    assert not schema.get_unique_constraints("job_applications")
    assert {c["name"] for c in schema.get_check_constraints("job_applications")} == {
        "ck_job_applications_company_nonblank", "ck_job_applications_role_nonblank"}


def test_committed_write_read_and_repeat_applications(test_engine):
    ids = []
    try:
        with session_scope(test_engine) as session:
            applications = [JobApplication(company="Synthetic Example", role="Engineer",
                                            applied_on=date(2026, 9, 17)) for _ in range(2)]
            session.add_all(applications)
            session.flush()
            ids.extend(application.id for application in applications)
            assert len(set(ids)) == 2
            assert all(isinstance(id_, UUID) and id_.version == 4 for id_ in ids)
        # A fresh connection pool and session must still see committed records.
        test_engine.dispose()
        with session_scope(test_engine) as session:
            rows = session.scalars(select(JobApplication).where(JobApplication.id.in_(ids))).all()
            assert len(rows) == 2
            assert all(row.company == "Synthetic Example" for row in rows)
            assert all(row.created_at.tzinfo is not None for row in rows)
            assert all(row.applied_on == date(2026, 9, 17) for row in rows)
    finally:
        # Delete only UUIDs owned by this check, never truncate or clear the database.
        with session_scope(test_engine) as session:
            session.execute(delete(JobApplication).where(JobApplication.id.in_(ids)))


@pytest.mark.parametrize("field", ["company", "role"])
def test_constraint_failure_rolls_back_whole_transaction(test_engine, field):
    ids = [uuid4(), uuid4()]
    try:
        with pytest.raises(IntegrityError) as caught:
            with session_scope(test_engine) as session:
                session.add(JobApplication(id=ids[0], company="Synthetic Example", role="Engineer",
                                           applied_on=date(2026, 9, 17)))
                session.flush()  # Good write occurred inside the same transaction.
                values = {"company": "Synthetic Example", "role": "Engineer"}
                values[field] = " \t\n"
                session.add(JobApplication(id=ids[1], applied_on=date(2026, 9, 17), **values))
                session.flush()
        assert caught.value.orig.sqlstate == "23514"
        assert caught.value.orig.diag.constraint_name == f"ck_job_applications_{field}_nonblank"
        with session_scope(test_engine) as session:
            assert session.scalars(select(JobApplication.id).where(JobApplication.id.in_(ids))).all() == []
    finally:
        with session_scope(test_engine) as session:
            session.execute(delete(JobApplication).where(JobApplication.id.in_(ids)))
