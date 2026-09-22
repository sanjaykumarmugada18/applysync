import asyncio
from datetime import datetime, timezone
from uuid import UUID, uuid4

import httpx
import pytest
from sqlalchemy import delete, event, func, select, update
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import Session

from database import session_scope
from main import create_app
from models import JobApplication

pytestmark = pytest.mark.database


def request(app, method, path, **kwargs):
    async def send():
        async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app),
                                     base_url="http://test") as client:
            return await client.request(method, path, **kwargs)
    return asyncio.run(send())


@pytest.fixture
def api(test_engine):
    app = create_app("test")
    app.state.engine = test_engine  # Fixture already verified database, role and revision.
    owned_ids = set()

    def remember_inserts(session, context):
        if session.get_bind() is test_engine:
            owned_ids.update(row.id for row in session.new if isinstance(row, JobApplication))

    event.listen(Session, "after_flush", remember_inserts)
    try:
        yield app, test_engine
    finally:
        event.remove(Session, "after_flush", remember_inserts)
        with session_scope(test_engine) as session:
            session.execute(delete(JobApplication).where(JobApplication.id.in_(owned_ids)))


@pytest.fixture
def payload():
    return {"company": f"Synthetic {uuid4()}", "role": "Engineer", "applied_on": "2026-09-17"}


def test_create_retrieve_list_and_duplicate(api, payload):
    app, engine = api
    supplied = {**payload, "company": " \t" + payload["company"] + "\n", "role": " Engineer "}
    responses = [request(app, "POST", "/applications", json=supplied) for _ in range(2)]
    assert all(response.status_code == 201 for response in responses)
    records = [response.json() for response in responses]
    assert len({record["id"] for record in records}) == 2
    for record in records:
        assert set(record) == {"id", "company", "role", "applied_on", "created_at"}
        assert UUID(record["id"]).version == 4
        assert record["company"] == payload["company"]
        assert record["role"] == "Engineer"
        assert record["applied_on"] == payload["applied_on"]
        assert datetime.fromisoformat(record["created_at"]).tzinfo is not None
        response = request(app, "GET", f'/applications/{record["id"]}')
        assert response.status_code == 200 and response.json() == record
        with session_scope(engine) as session:
            stored = session.get(JobApplication, UUID(record["id"]))
            assert stored.company == record["company"] and stored.role == record["role"]
            assert stored.applied_on.isoformat() == record["applied_on"]
            position = session.scalar(select(func.count()).select_from(JobApplication).where(
                (JobApplication.created_at < stored.created_at) |
                ((JobApplication.created_at == stored.created_at) & (JobApplication.id < stored.id))))
        assert position <= 10_000, "Test database exceeds the documented pagination window"
        page = request(app, "GET", f"/applications?limit=1&offset={position}")
        assert page.status_code == 200
        assert page.json() == {"items": [record], "limit": 1, "offset": position}


def test_ordering_pagination_and_empty_page(api, payload):
    app, engine = api
    records = []
    for _ in range(3):
        response = request(app, "POST", "/applications", json=payload)
        assert response.status_code == 201
        records.append(response.json())
    ids = [UUID(record["id"]) for record in records]
    # Deliberate tie proves the UUID secondary ordering. Only our records change.
    with session_scope(engine) as session:
        session.execute(update(JobApplication).where(JobApplication.id.in_(ids)).values(
            created_at=datetime(1900, 1, 1, tzinfo=timezone.utc)))
        expected = session.scalars(select(JobApplication.id).order_by(
            JobApplication.created_at, JobApplication.id)).all()
    assert len(expected) <= 10_000, "Test database exceeds the documented pagination window"
    for offset in range(0, min(len(expected), 6), 2):
        response = request(app, "GET", f"/applications?limit=2&offset={offset}")
        assert response.status_code == 200
        page = response.json()
        assert page["limit"] == 2 and page["offset"] == offset
        assert [row["id"] for row in page["items"]] == [str(id_) for id_ in expected[offset:offset+2]]
    assert [id_ for id_ in expected if id_ in ids] == sorted(ids)
    default = request(app, "GET", "/applications").json()
    assert default["limit"] == 20 and default["offset"] == 0
    assert [row["id"] for row in default["items"]] == [str(id_) for id_ in expected[:20]]
    empty = request(app, "GET", f"/applications?offset={len(expected)}")
    assert empty.status_code == 200
    assert empty.json() == {"items": [], "limit": 20, "offset": len(expected)}


@pytest.mark.parametrize("field,value", [
    ("company", ""), ("company", " \t\n"), ("company", "x" * 201),
    ("role", ""), ("role", " \t\n"), ("role", "x" * 201),
    ("company", None), ("role", 123),
    ("applied_on", "2026-02-30"), ("applied_on", "not-a-date"),
    ("applied_on", "2026-09-17T00:00:00"), ("applied_on", 0), ("applied_on", None),
    ("id", str(uuid4())), ("created_at", "2026-09-17T00:00:00Z"), ("unexpected", "value"),
])
def test_invalid_create(api, payload, field, value):
    app, engine = api
    response = request(app, "POST", "/applications", json={**payload, field: value})
    assert response.status_code == 422
    assert any(error["loc"][-1] == field for error in response.json()["detail"])
    with session_scope(engine) as session:
        assert session.scalar(select(func.count()).select_from(JobApplication).where(
            JobApplication.company == payload["company"])) == 0


@pytest.mark.parametrize("field", ["company", "role", "applied_on"])
def test_missing_required_field(api, payload, field):
    del payload[field]
    assert request(api[0], "POST", "/applications", json=payload).status_code == 422


@pytest.mark.parametrize("date_value", ["1900-01-01", "2100-01-01"])
def test_boundaries_and_no_date_range_policy(api, date_value):
    response = request(api[0], "POST", "/applications", json={
        "company": " " + "x" * 200 + " ", "role": "y" * 200, "applied_on": date_value})
    assert response.status_code == 201
    assert response.json()["company"] == "x" * 200
    assert response.json()["role"] == "y" * 200
    assert response.json()["applied_on"] == date_value


@pytest.mark.parametrize("query", ["limit=0", "limit=-1", "limit=101", "limit=abc",
                                       "limit=1.5", "offset=-1", "offset=10001", "offset=x", "offset=1.5"])
def test_invalid_pagination(api, query):
    assert request(api[0], "GET", "/applications?" + query).status_code == 422


def test_missing_and_malformed_id(api):
    assert request(api[0], "GET", "/applications/not-a-uuid").status_code == 422
    response = request(api[0], "GET", f"/applications/{uuid4()}")
    assert response.status_code == 404
    assert response.json() == {"detail": "Application not found"}


def test_commit_failure_rolls_back_and_is_private(api, payload, caplog):
    app, engine = api
    sentinel = "synthetic-sensitive-commit-details"
    flushed = []

    def fail_commit(session):
        if session.get_bind() is engine:
            # create_application already flushed a real INSERT before commit.
            flushed.append(session.scalar(select(func.count()).select_from(JobApplication).where(
                JobApplication.company == payload["company"])))
            raise OperationalError("synthetic SQL", {"password": sentinel}, Exception(sentinel))

    event.listen(Session, "before_commit", fail_commit)
    try:
        response = request(app, "POST", "/applications", json=payload)
    finally:
        event.remove(Session, "before_commit", fail_commit)
    assert flushed == [1]
    assert response.status_code == 500
    assert response.json() == {"detail": "Internal server error"}
    assert sentinel not in response.text and sentinel not in caplog.text
    with session_scope(engine) as session:
        assert session.scalar(select(func.count()).select_from(JobApplication).where(
            JobApplication.company == payload["company"])) == 0
    # Session/connection recovery: the next request can commit normally.
    assert request(app, "POST", "/applications", json=payload).status_code == 201


@pytest.mark.parametrize("method,path", [("POST", "/applications"), ("GET", "/applications"),
                                          ("GET", f"/applications/{uuid4()}")])
def test_database_errors_are_generic(api, payload, caplog, method, path):
    app, engine = api
    sentinel = "synthetic-sensitive-query-details"

    def fail_query(*args):
        raise OperationalError("synthetic SQL", {"password": sentinel}, Exception(sentinel))

    event.listen(engine, "before_cursor_execute", fail_query)
    try:
        response = request(app, method, path, **({"json": payload} if method == "POST" else {}))
        assert request(app, "GET", "/health").json() == {"status": "healthy"}
    finally:
        event.remove(engine, "before_cursor_execute", fail_query)
    assert response.status_code == 500
    assert response.json() == {"detail": "Internal server error"}
    assert sentinel not in response.text and sentinel not in caplog.text
