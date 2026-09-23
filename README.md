# applysync
AI-powered privacy-first job application tracker that automatically syncs Gmail application emails into a Kanban dashboard.

Current scope: Build 2, task 1 adds an interactive frontend **design preview** with
synthetic, in-memory applications. The existing Build 1 create/list/detail APIs and
`GET /health` remain unchanged. The preview does not call them. Gmail and automatic
tracking above describe the project goal, not implemented features.

## Frontend design preview (no backend required)

Tested with **Node 22.12.0 and npm 10.9.0** on Windows. Use npm for this frontend;
exact dependency versions are recorded in `frontend/package.json` and its lockfile.
From PowerShell:

```powershell
Set-Location 'C:\Users\sanja\Desktop\ApplySync\frontend'
npm.cmd ci
npm.cmd run dev
```

Open **http://127.0.0.1:5173/applications**. Stop with Ctrl+C. Port 5173 is fixed;
if it is occupied, stop your previous frontend server first. The backend server and
PostgreSQL are not needed for this preview. Do not copy backend secrets into frontend
environment files; browser-visible configuration cannot protect credentials.

Use Board/List over the same nine fictional records, search by company/role, and
combine search with a sample-stage filter. Cards/list rows open routed details.
The Add application form trims text, rejects blank or over-200-character values,
and accepts valid calendar dates including future dates. New records start in the
provisional **Applied** stage and appear in both views. Existing filters remain
selected, so they may hide a new record; the success message explains this.

All records are held in React memory. Additions **reset on reload**, and reopening
a new-record detail URL after reload shows a clear missing-preview-record message.
Search/filter/view selections live in URL query parameters, not browser storage.
Sample stages live outside the API-shaped `Application` type. There is no backend
stage contract, drag-and-drop, API request, local/session storage, authentication,
remote logo request, or persistent save. Backend integration is the next task.

The interface follows the three supplied `docs/design.pdf` screenshots with a white
sidebar/cards, cool-gray workspace, purple actions, pastel board headers and restrained
detail hierarchy. On phones the sidebar becomes a menu, list records stack, and
details/forms fill the screen. The board scrolls inside its own region. Escape closes
panels; keyboard focus returns to the trigger. Reduced-motion preferences are honored.

Frontend checks (run from `frontend/`):

```powershell
npm.cmd run typecheck
npm.cmd run build
npm.cmd run test
# One-time download for browser checks:
npx.cmd playwright install chromium
npm.cmd run test:e2e
```

Browser tests use a temporary production preview server on port 4173 and save
screenshots under `docs/screenshots/Build2_Task1/`. Keep that port free. Tests cover
search/filter/view state, validation, preview creation/reset, route-backed details,
keyboard handling, reduced motion and desktop/mobile layouts. Native dialog behaviour
is tested in Chromium; the component-test DOM only supplies a minimal dialog stub.

See [Build 2 Task 1 review](docs/Build2_Task1_Review.md) for evidence, reference
comparisons, dependency choices, screenshots, limitations and a learning walkthrough.

## Reproducible local setup (Windows PowerShell)

The following commands concern the **backend** and are not required for the frontend preview.

Use CPython **3.14.2**, the existing `.venv`, and local PostgreSQL (inspected server
installation: 14.7). From the repository root:

```powershell
# Only if creating an environment on a fresh checkout:
py -3.14 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m pip check
```

`requirements.txt` pins the complete runtime/test dependency set tested on Windows
x64. SQLAlchemy 2.0.54 supplies the ORM, Psycopg 3.3.5 its PostgreSQL driver,
Alembic 1.20.0 schema migrations, and python-dotenv 1.2.3 local configuration.
Pytest 9.1.1 and HTTPX 0.28.1 supply tests. Existing FastAPI/Uvicorn/Pydantic
versions are preserved. No PostgreSQL driver compilation is needed: the installed
Psycopg binary wheel bundles its client library. This does not install a server.

Compatibility references, checked 17 September 2026:
- [SQLAlchemy 2.0 documentation](https://docs.sqlalchemy.org/en/20/intro.html)
  and [Python 3.14 support history](https://www.sqlalchemy.org/blog/2025/05/14/sqlalchemy-2.0.41-released/).
- [Psycopg supported Python/PostgreSQL/Windows versions and binary installation](https://www.psycopg.org/psycopg3/docs/basic/install.html).
- [Alembic installation](https://alembic.sqlalchemy.org/en/latest/front.html).

### Dedicated database setup

With the existing PostgreSQL service running, perform this **once locally**:

```powershell
.\.venv\Scripts\python.exe -m scripts.setup_databases
```

Enter your local PostgreSQL administrator username and password at its prompts.
The password is hidden, never saved, and must not be pasted into chat. The script
connects to `127.0.0.1:5432` and the `postgres` maintenance database, checks catalog
names, and creates only **applysync_dev** and **applysync_test**, each owned by its
own restricted login role of the same name. It does not access unrelated tables.
Each database denies PUBLIC database access; the two roles do not share ownership.
Administrator privileges are used only for setup, never for application access.

The script refuses existing database/role names or an existing `.env`; it never
assumes an existing database is empty, resets passwords, drops databases, or
overwrites configuration. It writes generated application passwords only to the
ignored `.env`, before creation starts. PostgreSQL database creation cannot be
wrapped in one transaction: if setup fails partway, preserve `.env` and request a
setup-state review. Do not delete databases/configuration to force a retry.

`.env.example` contains placeholders only. Configuration consists of shared
`APPLYSYNC_DB_HOST`/`APPLYSYNC_DB_PORT` plus `APPLYSYNC_DEV_DB_NAME`,
`APPLYSYNC_DEV_DB_USER`, `APPLYSYNC_DEV_DB_PASSWORD` and the equivalent `TEST`
variables. Process environment values override `.env`; variable interpolation is
disabled. Only loopback hosts and the exact dedicated database/role names are
accepted for this local task. No complete connection URL is stored or printed.
Configuration loads only when persistence is requested; `/health` stays a simple
liveness endpoint and does not assert database readiness.

### Inspect and apply migrations

Read `migrations/versions/0001_job_applications.py` before these commands. This is
an explicitly authored Alembic revision, not a claimed autogenerate result.

```powershell
.\.venv\Scripts\python.exe -m alembic upgrade head --sql
.\.venv\Scripts\python.exe -m alembic upgrade head
.\.venv\Scripts\python.exe -m alembic upgrade head
.\.venv\Scripts\python.exe -m scripts.inspect_database dev
.\.venv\Scripts\python.exe -m alembic check
.\.venv\Scripts\python.exe -m alembic -x target=test upgrade head
.\.venv\Scripts\python.exe -m alembic -x target=test upgrade head
.\.venv\Scripts\python.exe -m scripts.inspect_database test
.\.venv\Scripts\python.exe -m alembic -x target=test check
```

The second upgrade should make no changes. Inspection prints only schema metadata,
never application rows or connection settings. `alembic check` compares the real
schema to model metadata. Do not use `Base.metadata.create_all()` to create tables.
The reverse migration drops the application table and its records; it is provided
for migration completeness, not part of normal setup or test cleanup.

## Initial schema decisions

`job_applications` represents one manual hiring-process application:

| Column | Choice and reason |
| --- | --- |
| `id` | UUID primary key; Python generates UUID4 when the ORM inserts a record. Direct SQL must supply it. |
| `company` | Required `varchar(200)`; database rejects whitespace-only values. |
| `role` | Required `varchar(200)`; same constraint. |
| `applied_on` | Required date explicitly supplied by the caller; distinguishes the actual application date from record creation. |
| `created_at` | Required timezone-aware timestamp with PostgreSQL `now()` default. |

All fields are non-null. PostgreSQL checks use its POSIX whitespace character class;
they do not normalize or trim stored text. The 200-character limits and required
application date are local implementation choices, not mandated by reference v2.0.
Company + role is **not unique**: repeated applications and concurrent processes are
allowed. No status enum, user ownership, events, or other future entities are added.
Status behaviour remains deferred. Current API validation is documented below.

Synchronous SQLAlchemy sessions keep the first persistence task simple. A session
groups queries; `database.session_scope()` commits successful work and rolls back
on failure, then closes the session. `models.JobApplication` maps Python fields to
columns; revision `0001` creates those columns; PostgreSQL's real table enforces
the constraints even when a caller bypasses Python. Engines disable SQL echo and
hide parameter values. CLI and API error boundaries suppress raw database exceptions.

## Checks and running the existing application

```powershell
# Configuration, setup safety (mocked), and in-memory HTTP checks:
.\.venv\Scripts\python.exe -m pytest -q
# Also require real migrated PostgreSQL test database access:
.\.venv\Scripts\python.exe -m pytest -q --run-db
# Real Uvicorn child process and HTTP checks, with automatic shutdown:
.\.venv\Scripts\python.exe -m scripts.check_server
# Actual server startup (stop with Ctrl+C):
.\.venv\Scripts\python.exe -m uvicorn main:app --host 127.0.0.1 --port 8000
```

Without `--run-db`, database checks explicitly skip. With it, missing/broken
configuration fails; no SQLite fallback is used. Tests verify real columns and
constraints, commit/read through fresh connections, permit duplicate company/role,
and provoke check-constraint failures to prove the whole transaction rolls back.
Tests connect only as the dedicated test role. They delete only synthetic UUIDs
created by that test (or the restart test's unique synthetic company marker); they
never truncate tables, drop schemas, or touch development data. A process killed
before cleanup may leave synthetic test records. API list tests include existing
test records when determining expected ordering; they fail with a clear precondition
if the test dataset exceeds the 10,000-offset window, rather than deleting records.

The HTTP test uses HTTPX's in-memory ASGI transport, which does **not** start
Uvicorn. To verify actual server behaviour in a second PowerShell terminal:

```powershell
curl.exe -i http://127.0.0.1:8000/health
curl.exe -i http://127.0.0.1:8000/does-not-exist
```

Expect 200 with `{"status":"healthy"}` and 404 with `{"detail":"Not Found"}`.
If Windows sandbox permissions block pytest's temporary directory, run the same
command in your normal local terminal; do not interpret a setup error as a passed
test. Secrets, `.venv`, and cache files must remain outside review packages.

## Manual application API

Run the existing setup/migration commands only as needed on a fresh checkout.
Task 2 adds no dependency or migration: the schema remains revision **0001**.
Start locally with the Uvicorn command above; interactive API docs are at `/docs`.
`main.app` selects development configuration. Automated API checks explicitly use
`create_app("test")` and verify the test database/role/revision before any writes.
There is no request parameter that switches databases.

| Request | Result |
| --- | --- |
| `POST /applications` | 201 with one stored application, after a successful commit. |
| `GET /applications?limit=20&offset=0` | 200 with `{ "items": [...], "limit": 20, "offset": 0 }`. |
| `GET /applications/{id}` | 200 with one application, or 404 `{ "detail": "Application not found" }` for an absent valid UUID. |
| Invalid body, UUID or pagination | 422 with FastAPI's structured validation errors. |
| Database/configuration failure | 500 `{ "detail": "Internal server error" }`; no raw database diagnostics in response/logs. |

Creation accepts exactly these three required fields:

```json
{"company":"Example Company","role":"Engineer","applied_on":"2026-09-17"}
```

Company and role must be strings. Surrounding whitespace is trimmed **before**
checking the 1-200 character length; whitespace-only values are invalid. Dates must
be valid `YYYY-MM-DD` JSON strings, not timestamps, datetime strings, or numbers.
Past and future dates are both accepted. Additional fields, including `id` and
`created_at`, are rejected. Repeated company/role applications remain allowed.

Create/detail responses contain exactly `id`, `company`, `role`, `applied_on`, and
`created_at`; the list uses the same objects inside `items`. Example shape
(illustrative generated values):

```json
{
  "id": "ae708452-d074-4fef-a6bd-6cbdbbbd15bf",
  "company": "Example Company",
  "role": "Engineer",
  "applied_on": "2026-09-17",
  "created_at": "2026-09-21T10:00:00Z"
}
```

List ordering is **created_at ascending, then UUID ascending**, so records sharing
a timestamp have deterministic ordering. `limit` defaults to 20 and allows 1-100;
`offset` defaults to 0 and allows 0-10,000. There is no total count or next-page token.
An offset beyond the available records returns an empty `items` array. Ordering is
deterministic for a fixed dataset; separate pages are not a snapshot across concurrent
writes. The offset cap deliberately limits the local API's pagination window.

`database.get_engine()` creates one lazy engine per app, protected against concurrent
first requests. FastAPI's lifespan disposes it on normal shutdown. `/health` and
unknown routes require neither database configuration nor connectivity. Each route
uses `session_scope()`, converting ORM records to Pydantic response objects before
the session closes. Creation exits the transaction (committing) **before** returning
201. A simulated pre-commit failure is tested to return 500 and roll back the flushed
record. As with ordinary transactional APIs, a connection loss after the server has
committed can leave the client uncertain; there is no idempotency-key mechanism in
this task, and retrying a create can create another application.

API behaviour and lifecycle decisions use the current official
[FastAPI lifespan documentation](https://fastapi.tiangolo.com/advanced/events/) and
[Pydantic string constraints](https://pydantic.dev/docs/validation/latest/api/pydantic/types/).

### API verification and practice

```powershell
# Full suite, including real DB writes/rollback and two real Uvicorn processes:
.\.venv\Scripts\python.exe -m pytest -q --run-db
# Only the actual application-process restart check (test database only):
.\.venv\Scripts\python.exe -m pytest -q --run-db tests/test_api_restart.py
```

Most API tests use in-memory HTTP transport against **real PostgreSQL**, not a
mock database. Commit/query failures and engine lifecycle are explicitly simulated
where needed. The restart test uses real loopback HTTP, stops its first Uvicorn
process, starts a new one and retrieves the committed record. It does not restart
PostgreSQL or write development records. Server subprocess output is suppressed;
in-process failure tests assert that synthetic diagnostic markers never enter logs.

Suggested learning checkpoint (not yet completed): with the local app running,
send this invalid request from PowerShell and explain why it returns 422 instead
of saving a record. Then locate the string constraint in `schemas.py`:

```powershell
$body = @{ company = '   '; role = 'Engineer'; applied_on = '2026-09-17' } | ConvertTo-Json
Invoke-RestMethod -Method Post -Uri http://127.0.0.1:8000/applications -ContentType 'application/json' -Body $body
```

PowerShell reports the non-success status as an error; the API response is the
expected validation failure. The earlier detailed transaction learning checkpoint
remains pending too. These instructions do not claim either checkpoint is complete.
