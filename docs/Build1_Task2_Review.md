# Build 1, task 2: manual application APIs

## Finalization update — 22 September 2026

Build 1 implementation is delivered for the local development scope. The user
reports that the stage chat inspected this source package and found no blocking
issue. Codex compared the current executable files and tracked diff with the
reviewed snapshot: no differences were found. The authorized checkpoint message is
`Add manual application create list and detail APIs`. The resulting commit hash and
live push verification are reported separately after these operations finish.

User-reported manual verification (not independently repeated by Codex here):

- Sanjay ran the application and used Swagger UI.
- Valid creation returned 201; he reports that the screenshot showed trimmed
  company text and generated fields. This update does not claim Codex inspected it.
- Retrieval succeeded according to his report.
- Whitespace-only company returned 422 with `string_too_short` and `min_length=1`.
- Sanjay has basic understanding of file responsibilities. The detailed request-flow
  explanation and earlier transaction exercise remain pending and carry forward.

The historical **57 passing tests** below were executed by Codex during task 2;
the stage chat did not independently rerun them. They are reused for this checkpoint
because executable code is unchanged, not presented as a fresh test run. Current
finalization checks cover snapshot identity, Git state, ignored/untracked `.env`,
the staged file list/diff, credential screening and whitespace. No database is
accessed or modified during finalization; Sanjay's synthetic development record is
preserved. Earlier zero-row counts describe the historical test run, not current data.

Planning & Progress: Build 1 implementation is delivered, with the reported manual
checks and remaining learning items recorded. Ready to scope Build 2 — Frontend &
Integration using the approved Vite/React/TypeScript stack. This does not claim all
learning completion criteria are satisfied. No frontend work is started here.

The remaining sections retain the original pre-commit review evidence and source
snapshot. Their uncommitted status and suggested exercise describe that earlier
point in time; this dated update supersedes their progress status.

## Baseline, instructions and Git state

- Repository: `C:\Users\sanja\Desktop\ApplySync`, branch `main`.
- Verified base/current commit: `8af37c857c5a7b541ab313e24d9f38dc9e5b9f5f`,
  `Build PostgreSQL persistence foundation`. Working tree was clean before editing.
- Read repository-root AGENTS.md and directly extracted reference pages 3, 6, 7,
  12, 15 and 22. Existing model, settings, transaction helper, tests and README were
  inspected. Prior task context also includes pages 5 and 21.
- A fresh `git ls-remote origin refs/heads/main` returned the same commit. This is
  live remote evidence; task 2 changes exist only in the local working tree.
- Modified tracked files: `main.py`, `database.py`, `README.md`.
- New untracked files: `applications.py`, `schemas.py`,
  `tests/test_applications.py`, `tests/test_app_lifecycle.py`,
  `tests/test_api_restart.py`, and this handoff.
- Nothing staged. Existing user files preserved. `.env` remains ignored and absent
  from the index; no secret contents or complete database URLs are in this handoff.

## Responsibilities and contract

| File | Responsibility |
| --- | --- |
| `schemas.py` | Strict creation field set, trimmed text constraints, date-only input, detached response objects and list envelope. |
| `applications.py` | Create/list/detail HTTP routes, ORM operations, ordering/pagination, 404 and transaction boundaries. |
| `database.py` | Existing engine/session helpers plus app-scoped lazy engine dependency with a first-use lock. |
| `main.py` | App factory, router registration, unchanged health response, generic database/configuration error handler, engine disposal on shutdown. |
| `tests/test_applications.py` | Real-PostgreSQL API success/validation/pagination/rollback/privacy tests using in-memory HTTP. |
| `tests/test_app_lifecycle.py` | Mocked concurrent engine initialization/reuse/disposal and unavailable-configuration behaviour. |
| `tests/test_api_restart.py` | Real Uvicorn child processes and HTTP create, stop, restart, retrieve; dedicated test database only. |
| `README.md` | Setup remains reproducible; adds request/response contract, choices, examples, limitations and practice request. |
| `docs/Build1_Task2_Review.md` | This evidence, execution paths, relevant diff, complete new files and necessary unchanged context. |

`POST /applications` requires exactly `company`, `role`, and `applied_on`. Text is
trimmed before enforcing 1-200 characters. Dates must be valid `YYYY-MM-DD` strings;
there is no past/future restriction. Unknown fields, including caller-supplied IDs
or creation timestamps, fail validation. Success returns **201** with all five
stored fields after commit. Duplicate company/role applications remain valid.

`GET /applications` returns **200** with `{"items": [...], "limit": 20, "offset": 0}`.
Defaults are limit 20 and offset 0; allowed ranges are 1-100 and 0-10,000. Records
sort by `created_at ASC, id ASC`. Empty pages contain `items: []`. Each item has the
same five fields as create/detail; no total count or next-page token is added.

`GET /applications/{application_id}` returns **200** for an existing UUID, **404**
with `{"detail":"Application not found"}` for an absent valid UUID, and **422**
for a malformed UUID. Invalid creation or pagination inputs also return 422 with
standard FastAPI validation details. SQLAlchemy/configuration failures return
**500** with `{"detail":"Internal server error"}`. The handler neither logs nor
serializes the exception or its SQL/parameters/configuration.

`GET /health` still returns **200** with `{"status":"healthy"}`. Unknown routes
still return 404. Neither needs a database connection or valid configuration.

## Success and failure paths

**Successful creation:** FastAPI validates the JSON with
`schemas.ApplicationCreate`. `ApplicationText` strips whitespace and enforces
length; `require_date_string()` prevents timestamp coercion and Pydantic validates
the calendar date. The `database.get_engine()` dependency initializes or reuses
the app's engine. `applications.create_application()` enters
`database.session_scope()`, builds `models.JobApplication`, adds it and flushes.
The ORM assigns UUID4 and PostgreSQL supplies `created_at` through RETURNING.
`ApplicationRead.model_validate()` copies the stored fields while the row is still
attached. Exiting `session_scope()` commits and closes the session; only then does
the route return the response object for 201 serialization. No lazy database reads
are required after session closure.

**Commit failure:** the real-database test injects an `OperationalError` in
SQLAlchemy's `before_commit` event. It first proves the flushed synthetic row is
visible inside the transaction. Exiting `session_scope()` then fails, triggers
rollback and closes the session. The route never reaches its return statement.
`main.database_error()` returns generic 500; no sensitive synthetic diagnostic
marker appears in response or captured logs. A fresh session proves no record
survived, and a subsequent POST succeeds after the injected fault is removed.

**Other failures:** an invalid body/UUID/query is rejected by FastAPI/Pydantic with
422. A valid UUID with no row produces a deliberate `HTTPException(404)` inside
`get_application()`. Query failures in all three routes reach the same generic
database handler. Request validation may construct an engine dependency but does
not open a database session or issue SQL in the route when validation fails.

No additional service/repository abstraction is introduced: the bounded route
functions contain the current business operations and ORM queries. SQLAlchemy and
Psycopg remain the sole persistence call chain. There are no other external calls.

## Verification evidence

All commands ran from the repository root using the existing Windows Python 3.14.2
`.venv`. Checks were independently executed here, not inferred from source review.

| Exact check | Observed result |
| --- | --- |
| `git branch --show-current`, `git rev-parse HEAD`, `git status --short` before editing | main, expected checkpoint, clean tree. |
| `.venv/Scripts/python.exe -m pip check` | `No broken requirements found.` No packages installed or upgraded in task 2. |
| `.venv/Scripts/python.exe -m pytest -q --run-db` | **57 passed in 9.14s**, zero skipped or failed. |
| `.venv/Scripts/python.exe -m alembic check` | `No new upgrade operations detected.` |
| `.venv/Scripts/python.exe -m alembic -x target=test check` | `No new upgrade operations detected.` |
| Dedicated role probes with `load_settings(target)` and `build_engine()` | `current_database()` and `current_user` match applysync_dev/applysync_test respectively. Both remain at revision 0001; both contain zero application rows after the tests. |
| `git diff --exit-code -- models.py migrations requirements.txt config.py` | Passed: model, migrations, dependencies and configuration unchanged. |
| `git diff --check` | Passed; only informational Windows LF/CRLF notices. |
| `git ls-remote origin refs/heads/main` | Live remote remains at 8af37c857c5a7b541ab313e24d9f38dc9e5b9f5f. |

The 57 cases comprise the previous 17 tests plus 37 new API cases, two lifecycle
cases and one actual-process restart case. New coverage includes:

- Create -> retrieve -> list; stored trimmed values, valid UUID4, aware timestamp,
  date, exact response field set, duplicate applications and database persistence.
- Deterministic list order, tied timestamps and UUID ordering, defaults, offsets,
  bounded page lengths and empty results beyond the existing dataset.
- Blank/whitespace-only/201-character text; wrong types; missing required fields;
  impossible dates, malformed dates, numeric timestamps and datetime strings;
  unexpected fields including ID/timestamp. Valid 200-character text and dates
  in 1900 and 2100 succeed.
- Malformed/missing UUIDs; negative/zero/excessive limits, excessive/negative
  offsets and nonnumeric/fractional pagination.
- Flushed INSERT followed by simulated commit failure, rollback, generic 500,
  private diagnostics and successful subsequent recovery. Simulated SELECT/INSERT
  failures cover all three API routes; health still works under a query fault.
- Eight concurrent engine requests share one mocked engine; shutdown disposes it.
  Missing configuration yields generic 500 for applications while health/404 work.

Most API requests use HTTPX ASGI transport in memory, backed by **real PostgreSQL**.
They do not start a web server. `test_committed_application_survives_uvicorn_restart`
starts a real Uvicorn process configured with `create_app('test')`, POSTs over local
HTTP, stops that process, starts a distinct process and GETs the same record. It
asserts identical stored JSON and also checks health and unknown-route HTTP responses
in both processes. The PostgreSQL service is never restarted. The separate existing
`scripts.check_server` command was not rerun; the restart test provides actual server
coverage for this task, not just in-memory evidence.

## Isolation, decisions and limitations

- `test_engine` verifies the database, role and revision before use. API tests assign
  this verified engine to an app explicitly targeting test. The restart child also
  explicitly selects test, with fixed database/role restrictions from configuration.
- API-test cleanup captures only IDs inserted through that test's engine/session
  events. Restart cleanup targets only its unique synthetic company marker, including
  the case of a lost response after commit. No table is cleared, no schema is dropped,
  no development record is written or deleted. Pre-existing test records participate
  in expected pagination results and are preserved. The pagination test precondition
  requires the test dataset to fit within the offset window; it never deletes data
  to satisfy that condition.
- No migration change is needed: the five existing columns support this contract.
  Revision 0001 is preserved; no upgrade/downgrade/provisioning was run for this task.
  The model/database table remains authoritative for column invariants; the Pydantic
  schemas add HTTP validation and serialization without changing the table.
- No new dependency, secret variable, deployment or infrastructure was introduced.
  Official FastAPI lifespan and Pydantic constraint documentation was consulted;
  source links are in README. Existing pinned dependency versions remain in use.
- Engine creation is lazy and app-scoped; successful engines persist until normal
  lifespan shutdown. SQLAlchemy sessions and transactions remain scoped per route.
  Health is liveness only. A forced process termination relies on OS cleanup; the
  lifecycle disposal assertion separately exercises normal shutdown with a mock.
- Offset pagination is capped and deterministic for a fixed dataset, not a snapshot
  across concurrent requests. UUID ordering is the tie breaker, not an implied
  real-world order between simultaneously created applications. No total count is
  requested or returned.
- The commit-failure test simulates failure **before commit completes**. A real lost
  connection after a server-side commit can yield an ambiguous outcome; this task
  does not add idempotency keys or retry POST automatically. Duplicate requests can
  create distinct records, consistent with supporting repeated applications.
- Failure and lifecycle injections are mocked; ordinary API persistence and process
  restart are real. No PostgreSQL service restart, load test, clean-environment
  reinstall, or deployment check was performed. There are no failed/blocked checks
  outstanding for the requested task. Secrets were never printed or embedded here.

## Learning and planning handoff

Three concepts to inspect: Pydantic validation before route execution; detached
response data versus live ORM objects; flush versus commit and rollback.

Suggested brief API checkpoint for Sanjay: run the whitespace-only-company POST
shown in README, inspect the 422 response, and locate the schema constraint that
prevents a save. This is a proposed exercise, not claimed participation. The earlier
detailed transaction checkpoint remains pending.

For `00 - Planning & Progress`: task 2 implements manual create/list/detail APIs;
57 checks pass, including real PostgreSQL rollback and actual Uvicorn process-restart
persistence. Schema stays at 0001. Changes are uncommitted on main at 8af37c8 and are
not pushed. Review/learning remain pending; do not mark all of Build 1 complete.
The next bounded action is reviewing this package and doing the focused API exercise,
then deciding whether to authorize a checkpoint commit.

## Source review appendix

Below are the relevant tracked diff and complete new source/test files, plus
unchanged model/configuration/test-fixture context. This document is not recursively
embedded. Blank context lines in the displayed diff have been whitespace-normalized
for Markdown. No `.env`, cache, environment directory or database record is included.

### Tracked changes

````diff
diff --git a/README.md b/README.md
index 37d84e2..92cc77e 100644
--- a/README.md
+++ b/README.md
@@ -1,9 +1,10 @@
 # applysync
 AI-powered privacy-first job application tracker that automatically syncs Gmail application emails into a Kanban dashboard.

-Current scope: Build 1, task 1 (local PostgreSQL persistence foundation). The only
-HTTP endpoint is `GET /health`, returning `{"status":"healthy"}`. Gmail and the
-dashboard above describe the project goal, not implemented features.
+Current scope: Build 1, task 2 (manual create/list/detail APIs backed by PostgreSQL).
+`GET /health` still returns `{"status":"healthy"}`. These unauthenticated APIs are
+local development functionality. Gmail and the dashboard above describe the project
+goal, not implemented features.

 ## Reproducible local setup (Windows PowerShell)

@@ -102,15 +103,14 @@ they do not normalize or trim stored text. The 200-character limits and required
 application date are local implementation choices, not mandated by reference v2.0.
 Company + role is **not unique**: repeated applications and concurrent processes are
 allowed. No status enum, user ownership, events, or other future entities are added.
-Status behaviour and API validation will be specified when needed.
+Status behaviour remains deferred. Current API validation is documented below.

 Synchronous SQLAlchemy sessions keep the first persistence task simple. A session
 groups queries; `database.session_scope()` commits successful work and rolls back
 on failure, then closes the session. `models.JobApplication` maps Python fields to
 columns; revision `0001` creates those columns; PostgreSQL's real table enforces
 the constraints even when a caller bypasses Python. Engines disable SQL echo and
-hide parameter values. CLI boundaries suppress raw database exceptions; future API
-handlers must also translate database errors safely, never log raw exceptions.
+hide parameter values. CLI and API error boundaries suppress raw database exceptions.

 ## Checks and running the existing application

@@ -130,8 +130,11 @@ configuration fails; no SQLite fallback is used. Tests verify real columns and
 constraints, commit/read through fresh connections, permit duplicate company/role,
 and provoke check-constraint failures to prove the whole transaction rolls back.
 Tests connect only as the dedicated test role. They delete only synthetic UUIDs
-created by that test; they never truncate tables, drop schemas, or touch development
-data. A process killed before cleanup may leave synthetic test records.
+created by that test (or the restart test's unique synthetic company marker); they
+never truncate tables, drop schemas, or touch development data. A process killed
+before cleanup may leave synthetic test records. API list tests include existing
+test records when determining expected ordering; they fail with a clear precondition
+if the test dataset exceeds the 10,000-offset window, rather than deleting records.

 The HTTP test uses HTTPX's in-memory ASGI transport, which does **not** start
 Uvicorn. To verify actual server behaviour in a second PowerShell terminal:
@@ -145,3 +148,96 @@ Expect 200 with `{"status":"healthy"}` and 404 with `{"detail":"Not Found"}`.
 If Windows sandbox permissions block pytest's temporary directory, run the same
 command in your normal local terminal; do not interpret a setup error as a passed
 test. Secrets, `.venv`, and cache files must remain outside review packages.
+
+## Manual application API
+
+Run the existing setup/migration commands only as needed on a fresh checkout.
+Task 2 adds no dependency or migration: the schema remains revision **0001**.
+Start locally with the Uvicorn command above; interactive API docs are at `/docs`.
+`main.app` selects development configuration. Automated API checks explicitly use
+`create_app("test")` and verify the test database/role/revision before any writes.
+There is no request parameter that switches databases.
+
+| Request | Result |
+| --- | --- |
+| `POST /applications` | 201 with one stored application, after a successful commit. |
+| `GET /applications?limit=20&offset=0` | 200 with `{ "items": [...], "limit": 20, "offset": 0 }`. |
+| `GET /applications/{id}` | 200 with one application, or 404 `{ "detail": "Application not found" }` for an absent valid UUID. |
+| Invalid body, UUID or pagination | 422 with FastAPI's structured validation errors. |
+| Database/configuration failure | 500 `{ "detail": "Internal server error" }`; no raw database diagnostics in response/logs. |
+
+Creation accepts exactly these three required fields:
+
+```json
+{"company":"Example Company","role":"Engineer","applied_on":"2026-09-17"}
+```
+
+Company and role must be strings. Surrounding whitespace is trimmed **before**
+checking the 1-200 character length; whitespace-only values are invalid. Dates must
+be valid `YYYY-MM-DD` JSON strings, not timestamps, datetime strings, or numbers.
+Past and future dates are both accepted. Additional fields, including `id` and
+`created_at`, are rejected. Repeated company/role applications remain allowed.
+
+Create/detail responses contain exactly `id`, `company`, `role`, `applied_on`, and
+`created_at`; the list uses the same objects inside `items`. Example shape
+(illustrative generated values):
+
+```json
+{
+  "id": "ae708452-d074-4fef-a6bd-6cbdbbbd15bf",
+  "company": "Example Company",
+  "role": "Engineer",
+  "applied_on": "2026-09-17",
+  "created_at": "2026-09-21T10:00:00Z"
+}
+```
+
+List ordering is **created_at ascending, then UUID ascending**, so records sharing
+a timestamp have deterministic ordering. `limit` defaults to 20 and allows 1-100;
+`offset` defaults to 0 and allows 0-10,000. There is no total count or next-page token.
+An offset beyond the available records returns an empty `items` array. Ordering is
+deterministic for a fixed dataset; separate pages are not a snapshot across concurrent
+writes. The offset cap deliberately limits the local API's pagination window.
+
+`database.get_engine()` creates one lazy engine per app, protected against concurrent
+first requests. FastAPI's lifespan disposes it on normal shutdown. `/health` and
+unknown routes require neither database configuration nor connectivity. Each route
+uses `session_scope()`, converting ORM records to Pydantic response objects before
+the session closes. Creation exits the transaction (committing) **before** returning
+201. A simulated pre-commit failure is tested to return 500 and roll back the flushed
+record. As with ordinary transactional APIs, a connection loss after the server has
+committed can leave the client uncertain; there is no idempotency-key mechanism in
+this task, and retrying a create can create another application.
+
+API behaviour and lifecycle decisions use the current official
+[FastAPI lifespan documentation](https://fastapi.tiangolo.com/advanced/events/) and
+[Pydantic string constraints](https://pydantic.dev/docs/validation/latest/api/pydantic/types/).
+
+### API verification and practice
+
+```powershell
+# Full suite, including real DB writes/rollback and two real Uvicorn processes:
+.\.venv\Scripts\python.exe -m pytest -q --run-db
+# Only the actual application-process restart check (test database only):
+.\.venv\Scripts\python.exe -m pytest -q --run-db tests/test_api_restart.py
+```
+
+Most API tests use in-memory HTTP transport against **real PostgreSQL**, not a
+mock database. Commit/query failures and engine lifecycle are explicitly simulated
+where needed. The restart test uses real loopback HTTP, stops its first Uvicorn
+process, starts a new one and retrieves the committed record. It does not restart
+PostgreSQL or write development records. Server subprocess output is suppressed;
+in-process failure tests assert that synthetic diagnostic markers never enter logs.
+
+Suggested learning checkpoint (not yet completed): with the local app running,
+send this invalid request from PowerShell and explain why it returns 422 instead
+of saving a record. Then locate the string constraint in `schemas.py`:
+
+```powershell
+$body = @{ company = '   '; role = 'Engineer'; applied_on = '2026-09-17' } | ConvertTo-Json
+Invoke-RestMethod -Method Post -Uri http://127.0.0.1:8000/applications -ContentType 'application/json' -Body $body
+```
+
+PowerShell reports the non-success status as an error; the API response is the
+expected validation failure. The earlier detailed transaction learning checkpoint
+remains pending too. These instructions do not claim either checkpoint is complete.
diff --git a/database.py b/database.py
index b81f54b..c3f1759 100644
--- a/database.py
+++ b/database.py
@@ -2,11 +2,12 @@

 from contextlib import contextmanager

+from fastapi import Request
 from sqlalchemy import create_engine
 from sqlalchemy.engine import Engine
 from sqlalchemy.orm import Session

-from config import DatabaseSettings
+from config import DatabaseSettings, load_settings


 def build_engine(settings: DatabaseSettings) -> Engine:
@@ -14,6 +15,15 @@ def build_engine(settings: DatabaseSettings) -> Engine:
                          hide_parameters=True, connect_args={"connect_timeout": 5})


+def get_engine(request: Request) -> Engine:
+    """One lazily initialized engine per app; health needs no configuration."""
+    state = request.app.state
+    with state.engine_lock:
+        if state.engine is None:
+            state.engine = build_engine(load_settings(state.database_target))
+        return state.engine
+
+
 @contextmanager
 def session_scope(engine: Engine):
     # begin() commits on success and rolls back on exceptions; close always runs.
diff --git a/main.py b/main.py
index 50cb24f..872024f 100644
--- a/main.py
+++ b/main.py
@@ -1,7 +1,45 @@
-from fastapi import FastAPI
+from contextlib import asynccontextmanager
+from threading import Lock
+
+from fastapi import FastAPI, Request
+from fastapi.responses import JSONResponse
+from sqlalchemy.exc import SQLAlchemyError
+
+from applications import router
+from config import ConfigurationError
+
+
+@asynccontextmanager
+async def lifespan(app: FastAPI):
+    try:
+        yield
+    finally:
+        if app.state.engine is not None:
+            app.state.engine.dispose()
+            app.state.engine = None
+
+
+async def database_error(request: Request, error: Exception):
+    # Do not log or serialize the exception, SQL, parameters, or configuration.
+    return JSONResponse(status_code=500, content={"detail": "Internal server error"})

-app = FastAPI()

-@app.get("/health")
 def health():
-    return {"status": "healthy"}
\ No newline at end of file
+    return {"status": "healthy"}
+
+
+def create_app(database_target: str = "dev") -> FastAPI:
+    if database_target not in {"dev", "test"}:
+        raise ConfigurationError("Database target must be dev or test.")
+    application = FastAPI(lifespan=lifespan)
+    application.state.database_target = database_target
+    application.state.engine = None
+    application.state.engine_lock = Lock()
+    application.add_exception_handler(SQLAlchemyError, database_error)
+    application.add_exception_handler(ConfigurationError, database_error)
+    application.add_api_route("/health", health, methods=["GET"])
+    application.include_router(router)
+    return application
+
+
+app = create_app()

````

### applications.py

```python
"""Local manual create/list/detail endpoints and their database operations."""

from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.engine import Engine

from database import get_engine, session_scope
from models import JobApplication
from schemas import ApplicationCreate, ApplicationPage, ApplicationRead

router = APIRouter(prefix="/applications", tags=["applications"])
DatabaseEngine = Annotated[Engine, Depends(get_engine)]


@router.post("", response_model=ApplicationRead, status_code=201)
def create_application(payload: ApplicationCreate, engine: DatabaseEngine):
    with session_scope(engine) as session:
        application = JobApplication(**payload.model_dump())
        session.add(application)
        session.flush()
        # Materialize while attached; no lazy loads after commit/close.
        response = ApplicationRead.model_validate(application)
    # session_scope must commit successfully before the response can be returned.
    return response


@router.get("", response_model=ApplicationPage)
def list_applications(
    engine: DatabaseEngine,
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
    offset: Annotated[int, Query(ge=0, le=10_000)] = 0,
):
    with session_scope(engine) as session:
        rows = session.scalars(select(JobApplication).order_by(
            JobApplication.created_at.asc(), JobApplication.id.asc()
        ).limit(limit).offset(offset))
        response = ApplicationPage(items=[ApplicationRead.model_validate(row) for row in rows],
                                   limit=limit, offset=offset)
    return response


@router.get("/{application_id}", response_model=ApplicationRead)
def get_application(application_id: UUID, engine: DatabaseEngine):
    with session_scope(engine) as session:
        application = session.get(JobApplication, application_id)
        if application is None:
            raise HTTPException(status_code=404, detail="Application not found")
        response = ApplicationRead.model_validate(application)
    return response

```

### schemas.py

```python
"""Manual application HTTP contracts, independent of open database sessions."""

from datetime import date, datetime
import re
from typing import Annotated
from uuid import UUID

from pydantic import BaseModel, ConfigDict, StringConstraints, field_validator

ApplicationText = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=200)]


class ApplicationCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    company: ApplicationText
    role: ApplicationText
    applied_on: date

    @field_validator("applied_on", mode="before")
    @classmethod
    def require_date_string(cls, value):
        # JSON dates are YYYY-MM-DD, not numeric timestamps or datetime strings.
        if not isinstance(value, str) or not re.fullmatch(r"[0-9]{4}-[0-9]{2}-[0-9]{2}", value):
            raise ValueError("Use a date in YYYY-MM-DD format.")
        return value


class ApplicationRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    company: str
    role: str
    applied_on: date
    created_at: datetime


class ApplicationPage(BaseModel):
    items: list[ApplicationRead]
    limit: int
    offset: int

```

### tests/test_applications.py

```python
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

```

### tests/test_app_lifecycle.py

```python
import asyncio
from concurrent.futures import ThreadPoolExecutor
from unittest.mock import Mock

import httpx
from starlette.requests import Request

import database
from config import ConfigurationError
from main import create_app


def test_lazy_engine_reuse_and_shutdown(monkeypatch):
    app = create_app("test")
    engine = Mock()
    build = Mock(return_value=engine)
    settings = Mock()
    monkeypatch.setattr(database, "load_settings", settings)
    monkeypatch.setattr(database, "build_engine", build)

    async def check():
        async with app.router.lifespan_context(app):
            build.assert_not_called()
            request = Request({"type": "http", "app": app})
            with ThreadPoolExecutor(max_workers=4) as executor:
                engines = list(executor.map(lambda _: database.get_engine(request), range(8)))
            assert all(value is engine for value in engines)
            settings.assert_called_once_with("test")
            build.assert_called_once()
        engine.dispose.assert_called_once()
        assert app.state.engine is None
    asyncio.run(check())


def test_missing_configuration_keeps_health_available(monkeypatch, caplog):
    def fail_settings(*args):
        raise ConfigurationError("synthetic-private-configuration")
    monkeypatch.setattr(database, "load_settings", fail_settings)
    app = create_app()

    async def check():
        async with app.router.lifespan_context(app):
            async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as client:
                assert (await client.get("/health")).json() == {"status": "healthy"}
                assert (await client.get("/unknown")).status_code == 404
                response = await client.get("/applications")
                assert response.status_code == 500
                assert response.json() == {"detail": "Internal server error"}
                assert "synthetic-private-configuration" not in caplog.text
    asyncio.run(check())

```

### tests/test_api_restart.py

```python
"""Real HTTP and process restart, never PostgreSQL service restart."""

from contextlib import contextmanager
from pathlib import Path
import socket
import subprocess
import sys
import time
from uuid import uuid4

import httpx
import pytest
from sqlalchemy import delete

from database import session_scope
from models import JobApplication

pytestmark = pytest.mark.database


@contextmanager
def test_server():
    with socket.socket() as probe:
        probe.bind(("127.0.0.1", 0))
        port = probe.getsockname()[1]
    code = ("import uvicorn; from main import create_app; "
            "app=create_app('test'); assert app.state.database_target == 'test'; "
            f"uvicorn.run(app, host='127.0.0.1', port={port}, access_log=False)")
    process = subprocess.Popen(
        [sys.executable, "-c", code], cwd=Path(__file__).resolve().parents[1],
        stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
    )
    try:
        with httpx.Client(base_url=f"http://127.0.0.1:{port}", trust_env=False, timeout=5) as client:
            deadline = time.monotonic() + 15
            while True:
                assert process.poll() is None, "Test Uvicorn process exited during startup"
                try:
                    health = client.get("/health")
                    break
                except httpx.TransportError:
                    if time.monotonic() >= deadline:
                        pytest.fail("Test Uvicorn startup timed out")
                    time.sleep(0.1)
            assert health.status_code == 200 and health.json() == {"status": "healthy"}
            missing = client.get("/unknown")
            assert missing.status_code == 404 and missing.json() == {"detail": "Not Found"}
            yield client, process
    finally:
        if process.poll() is None:
            process.terminate()
        try:
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            process.kill()
            process.wait(timeout=5)


# This context manager is a helper, not a collected test.
test_server.__test__ = False


def test_committed_application_survives_uvicorn_restart(test_engine):
    # test_engine verifies current database, current role and revision before spawning.
    company = f"Synthetic restart {uuid4()}"
    try:
        with test_server() as (client, first_process):
            response = client.post("/applications", json={
                "company": company, "role": "Engineer", "applied_on": "2026-09-17"})
            assert response.status_code == 201
            stored = response.json()
        assert first_process.poll() is not None
        with test_server() as (client, second_process):
            assert first_process.pid != second_process.pid
            response = client.get(f'/applications/{stored["id"]}')
            assert response.status_code == 200
            assert response.json() == stored
    finally:
        # A unique synthetic company also covers a response lost after commit.
        with session_scope(test_engine) as session:
            session.execute(delete(JobApplication).where(JobApplication.company == company))

```

### models.py

```python
"""The initial manual application record; no future-stage entities."""

from datetime import date, datetime
from uuid import UUID, uuid4

from sqlalchemy import CheckConstraint, Date, DateTime, String, Uuid, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class JobApplication(Base):
    __tablename__ = "job_applications"
    __table_args__ = (
        CheckConstraint("company ~ '[^[:space:]]'", name="ck_job_applications_company_nonblank"),
        CheckConstraint("role ~ '[^[:space:]]'", name="ck_job_applications_role_nonblank"),
    )

    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True, default=uuid4)
    company: Mapped[str] = mapped_column(String(200), nullable=False)
    role: Mapped[str] = mapped_column(String(200), nullable=False)
    applied_on: Mapped[date] = mapped_column(Date, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False,
                                               server_default=func.now())

```

### config.py

```python
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

```

### tests/conftest.py

```python
import pytest
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from config import ConfigurationError, load_settings
from database import build_engine


def pytest_addoption(parser):
    parser.addoption("--run-db", action="store_true", help="Require the dedicated migrated test database")


@pytest.fixture
def test_engine(request):
    if not request.config.getoption("--run-db"):
        pytest.skip("Pass --run-db after provisioning and migrating the dedicated test database")
    engine = None
    try:
        engine = build_engine(load_settings("test"))
        with engine.connect() as connection:
            assert connection.scalar(text("SELECT current_database()")) == "applysync_test"
            assert connection.scalar(text("SELECT current_user")) == "applysync_test"
            assert connection.scalar(text("SELECT version_num FROM alembic_version")) == "0001"
        yield engine
    except (ConfigurationError, SQLAlchemyError):
        pytest.fail("Dedicated test database is not configured, reachable, or migrated.", pytrace=False)
    finally:
        if engine is not None:
            engine.dispose()

```

### Working-tree snapshot

```text
 M README.md
 M database.py
 M main.py
?? applications.py
?? docs/Build1_Task2_Review.md
?? schemas.py
?? tests/test_api_restart.py
?? tests/test_app_lifecycle.py
?? tests/test_applications.py
```
