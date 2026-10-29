# applysync
AI-powered privacy-first job application tracker that automatically syncs Gmail application emails into a Kanban dashboard.

Current scope: Build 4 Task 1 adds optional Gmail connection/disconnection settings,
with no message reading or synchronization. Build 3 supplies registration, login, revocable JWT-cookie sessions and
server-side ownership to the integrated PostgreSQL create/list/detail APIs. `/applications` displays stored data; the explicitly separate
`/preview/applications` retains the fictional Board/List preview. Automatic
tracking above describes the project goal, not an implemented feature. This remains local development functionality, not a public deployment.
Read the Build 3 setup and security policy below before starting the backend.

## Build 3 setup and session policy

On an existing checkout, from the root in PowerShell (never reprovision databases):

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m scripts.setup_auth
.\.venv\Scripts\python.exe -m alembic upgrade head --sql
.\.venv\Scripts\python.exe -m alembic upgrade head
.\.venv\Scripts\python.exe -m alembic -x target=test upgrade head
```

`setup_auth` appends a cryptographically generated 32-byte signing secret as hex
and explicit `local` mode to the ignored root `.env` only if those keys are absent.
It never prints or replaces existing values. Keep that file private. Invalid
existing values require a local edit; do not paste them into chat. The checked-in
`.env.example` contains placeholders only. Health remains available without a
signing secret; authentication fails safely with a generic 500.

The migration in this checkout has already been applied to development and test.
Development's **two original records remain unchanged and unassigned**. Register
an account first. Then run this one local action if you want to assign them:

```powershell
.\.venv\Scripts\python.exe -m scripts.assign_legacy --interactive
```

It lists only unassigned UUIDs, asks for an existing account email and the explicit
UUIDs to assign, and commits all selected assignments together. A missing account,
missing UUID or already-owned row aborts everything. No public claim endpoint or
default account exists. Ownership migration is not fully finalized while these
assignments remain pending; `owner_id` intentionally stays nullable to quarantine
legacy records. New API writes cannot create ownerless applications.

For the current two-record legacy set, enter your intended registered account's
email, then the **two displayed UUIDs separated by a comma**. Do not select other
records if the local list has changed. Non-interactive equivalent (placeholders):
`python -m scripts.assign_legacy --email <existing-account-email> --ids <first-uuid> <second-uuid>`.
After assignment, sign in as that account and reload; verify both records appear.
The nullable column remains the intentional quarantine mechanism; no further
schema migration is required to perform the assignment.

| Endpoint | Contract |
| --- | --- |
| POST /auth/register | `{email,password}`; 201 `{id,email}` and session cookie; duplicate normalized email: 409. |
| POST /auth/login | Same body; 200 `{id,email}` and new session; generic invalid credentials: 401. |
| GET /auth/me | 200 `{id,email}`; missing/invalid/expired/revoked session: 401. |
| POST /auth/logout | 204 after deleting the server session, then matching cookie deletion; invalid session: 401. |

Email uses maintained email-validator, trims surrounding whitespace, validates
syntax without DNS lookups, requires an ASCII local part, normalizes then
lowercases the full address. The unique database column and lowercase check
make duplicate creation safe under concurrency. Case-insensitive mailbox identity
is a deliberate application policy. No verification email is sent in this stage.
Passwords accept 12?128 Unicode characters, including spaces, without trimming,
truncation or composition rules. Argon2id hashes use the library defaults; login
rehashes if its parameters change. Passwords/hashes never appear in responses.
Validation responses omit the usual raw input echo.

Sessions last **8 hours from issuance**, with no refresh tokens or sliding expiry.
PyJWT signs HS256; validation fixes that algorithm and requires issuer, audience,
subject UUID, session UUID, issued-at and expiry. The matching database session
must still exist and be unexpired. JWT claims contain identifiers/timestamps only.
Cookie: `applysync_session`, HttpOnly, SameSite=Lax, Path=/, host-only, Max-Age=28800.
Local HTTP explicitly uses Secure=false. `APPLYSYNC_AUTH_MODE=production` requires
HTTPS-only `APPLYSYNC_AUTH_ORIGINS` and sets Secure=true. Production deployment is
not implemented: frontend API configuration still permits loopback HTTP only.
The intended topology is same-site frontend/API (same hostname locally), with
exact origins allowlisted; cross-site deployment needs a separate review.

Every unsafe request, including login/registration/logout, must provide an exact
trusted `Origin` and `X-ApplySync-CSRF: 1`. The custom header forces browser
preflight; HTML forms cannot supply it. The independent server check rejects
missing/invalid headers and absent/null/untrusted origins with 403 even if CORS
is bypassed by a direct client. This is the custom-header CSRF pattern for a
JSON-only API, not a secret CSRF token. Only trusted frontend origins may execute
scripts with this privilege. HttpOnly does not protect against actions by XSS.

Logout deletes the durable session before returning; replay of that cookie fails
immediately, including after restart. Requests already authorized before logout
may finish. Other devices retain their own sessions. Expired session rows are
inert; scheduled cleanup and account recovery are not implemented.

Login and registration share per-process 15-minute limits: 10 attempts per hashed
normalized email and 50 per client IP, with a bounded 10,000-entry map. All attempts
count, including successes; response is 429 with Retry-After. Restart resets limits,
and multiple workers do not share them. This is a single-process development
control, not distributed abuse protection. Do not trust forwarded client IPs from
untrusted proxies (`--no-proxy-headers` for the local Uvicorn command).

React restores `/auth/me` before rendering private content, rechecks on focus and
every minute, and treats expected 401 as signed out. Network failure shows a retry
state rather than claiming logout. Private query clients are cancelled, cleared
and unmounted on logout, identity change or session-check failure. Pending writes
are aborted on unmount; POST never auto-replays after sign-in. The server may have
committed a request whose response was lost; inspect your list before resubmitting.
Browser timer throttling may delay idle expiry UI, but the server rejects expired
credentials on every request. Use separate browser profiles/incognito for two
simultaneous accounts because cookies are shared by tabs on the same hostname.

### Manual two-account check (Sanjay reports passing, 29 October 2026)

1. Open http://127.0.0.1:5173/register and register account A. Create a fictional
   application; reload and try both Board/List views. Copy its detail URL.
2. In an incognito window register B. A's record must not be in B's list, and
   opening A's detail URL must say Application not found.
3. Log A out and refresh. Sign in as B in that window: A's cards must not flash.
   Close any incognito window when finished. These are your intentional dev records.

Focused learning checkpoint: inspect `applications.get_application` and identify
which condition would be missing if B could read A's copied UUID. Explain why the
frontend route guard alone cannot provide this protection. Prior learning gaps
remain pending, not implementation blockers.

Official references used: [Argon2 password hashing](https://argon2-cffi.readthedocs.io/en/stable/howto.html),
[PyJWT validation](https://pyjwt.readthedocs.io/en/stable/api.html),
[email normalization](https://github.com/JoshData/python-email-validator), and
[OWASP custom-header CSRF defence](https://cheatsheetseries.owasp.org/cheatsheets/Cross-Site_Request_Forgery_Prevention_Cheat_Sheet.html).
Python 3.14.2 installation and `pip check` passed. Requirements pin PyJWT 2.15.0,
argon2-cffi 25.1.0, bindings 26.1.0 and email-validator 2.3.0 plus their dependencies.
No frontend dependency changed.

## Integrated interface (two PowerShell terminals)

Use the existing backend `.venv`, provisioned local databases and ignored root
`.env`. Do not reprovision or replace existing credentials. For a fresh machine,
follow the backend setup below first. Terminal 1, from the repository root:

```powershell
Set-Location 'C:\Users\sanja\Desktop\ApplySync'
.\.venv\Scripts\python.exe -m uvicorn main:app --host 127.0.0.1 --port 8000 --no-proxy-headers --no-access-log
```

Terminal 2, from `frontend/`:

```powershell
Set-Location 'C:\Users\sanja\Desktop\ApplySync\frontend'
npm.cmd ci
npm.cmd run dev
```

Open **http://127.0.0.1:5173/applications**. Backend health is
http://127.0.0.1:8000/health and Swagger is http://127.0.0.1:8000/docs.
Stop your own servers with Ctrl+C; reuse existing correct servers rather than
starting duplicates. Restart an older backend process to load authentication.
Use **127.0.0.1 for both servers**; do not mix localhost with 127.0.0.1.
Real application routes redirect to login; the sample preview remains public.

The public `VITE_API_BASE_URL` defaults to `http://127.0.0.1:8000`. To configure a
different local port, copy `frontend/.env.example` to `frontend/.env.local` **only
if that local file does not already exist**, replace its placeholder with your
local API origin (for example `http://127.0.0.1:8000`), and restart Vite. This
variable is browser-visible and must contain no credentials, token, query string
or database URL. Root backend `.env` is separate and must never be copied into
the frontend. The client accepts local HTTP origins only for this task.

FastAPI allows exactly `http://localhost:5173`, `http://127.0.0.1:5173`,
`http://localhost:4173` and `http://127.0.0.1:4173`, with credentialed GET/POST, Content-Type and X-ApplySync-CSRF.
There is no wildcard. Every write also checks the exact Origin and custom header
on the server. CORS itself is not authentication or ownership protection.

Stored records share Board/List views (List is the default). The Board uses one
neutral **Stage not recorded** column and explains that grouping will be available
when stage tracking exists. This heading is only a display fallback; no stage is
assigned or saved. Switching views retains loaded-page search and pagination.
Pages contain at most
20 records, ordered by `created_at ASC, id ASC`. Previous/Next controls use the
existing offset contract, up to 10,000. A full last page may lead to an empty next
page because the API has no total/has-more field. Counts describe the loaded page,
not the database total. Search explicitly covers **only the loaded page**. No
whole-database fetch or global search is implemented.

Creation trims/validates text and dates, disables repeat submission while saving,
and shows success only after a confirmed response. It refreshes list queries and
opens the returned record's detail URL; reload performs a real detail GET. Since
the list is oldest-first, the new record may be on a later page. Read failures
have retry controls. Failed creation retains input; uncertain network/server
outcomes instruct you to check the list before resubmitting. POST is never retried
automatically. Duplicate company/role applications remain allowed.

The client uses TanStack Query 5.103.2 with the shared `src/api.ts` fetch client.
See [Build 2 Task 2 review](docs/Build2_Task2_Review.md) for code, checks and limitations.

From the repository root, run backend regression checks and the guarded real
browser integration check (existing migrated **test** database required):

```powershell
Set-Location 'C:\Users\sanja\Desktop\ApplySync'
.\.venv\Scripts\python.exe -m pytest --run-db -q
.\.venv\Scripts\python.exe -m scripts.run_frontend_integration
```

Install frontend dependencies and Chromium using the commands below first. Keep
port 4173 free. The integration runner verifies test database/role/revision,
inserts 21 uniquely marked synthetic fixtures, starts its own test API on a free
loopback port and a temporary frontend on 4173, and runs real cross-origin browser
create/read/reload checks. It independently verifies the committed row in
PostgreSQL, stops only its own servers, rechecks the database target, and removes
only its own marked records. It neither clears development data nor runs DDL.
Do not invoke `npm run test:integration` directly against an arbitrary backend;
the Python runner supplies its guarded target and run marker.

Manual check: add one fictional development application, note its generated
detail URL, reload that page and verify the record remains. This is a deliberate
development record; automated checks do not remove it. The API has no delete endpoint.

## Frontend design preview (no backend required)

Tested with **Node 22.12.0 and npm 10.9.0** on Windows. Use npm for this frontend;
exact dependency versions are recorded in `frontend/package.json` and its lockfile.
From PowerShell:

```powershell
Set-Location 'C:\Users\sanja\Desktop\ApplySync\frontend'
npm.cmd ci
npm.cmd run dev
```

Open **http://127.0.0.1:5173/preview/applications**. Stop with Ctrl+C. Port 5173 is fixed;
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
remote logo request, or persistent save **on this preview route**. The normal
Applications route uses the real API independently. Leaving the preview also
unmounts its temporary fixture state.

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
transient screenshots under ignored `test-results/` directories. The real guarded
integration run saves intentional evidence under `docs/screenshots/Build3/`.
Historical Build 2 images are not overwritten. Keep port 4173 free. Tests cover
search/filter/view state, validation, preview creation/reset, route-backed details,
keyboard handling, reduced motion and desktop/mobile layouts. Native dialog behaviour
is tested in Chromium; the component-test DOM only supplies a minimal dialog stub.
`test:e2e` includes mocked real-data failure checks and preview regressions; the
separate guarded Python runner above proves the actual database integration.

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

Read both explicitly authored revisions in `migrations/versions/` before these
commands. Revision `0002` preserves existing applications with NULL ownership;
those records remain quarantined until explicitly assigned locally.

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
Revision 0002 intentionally refuses downgrade to prevent accidental loss of
identity/ownership data. Do not reset development or downgrade to assign records.

## Initial schema decisions

`job_applications` represents one manual hiring-process application:

| Column | Choice and reason |
| --- | --- |
| `id` | UUID primary key; Python generates UUID4 when the ORM inserts a record. Direct SQL must supply it. |
| `company` | Required `varchar(200)`; database rejects whitespace-only values. |
| `role` | Required `varchar(200)`; same constraint. |
| `applied_on` | Required date explicitly supplied by the caller; distinguishes the actual application date from record creation. |
| `created_at` | Required timezone-aware timestamp with PostgreSQL `now()` default. |

These original fields are non-null. Build 3 adds nullable `owner_id` for legacy
quarantine; every API-created row has an authenticated owner. PostgreSQL checks use its POSIX whitespace character class;
they do not normalize or trim stored text. The 200-character limits and required
application date are local implementation choices, not mandated by reference v2.0.
Company + role is **not unique**: repeated applications and concurrent processes are
allowed. Ownership is now implemented; status enums and events remain deferred.
Status behaviour remains deferred. Current API validation is documented below.

Synchronous SQLAlchemy sessions keep the first persistence task simple. A session
groups queries; `database.session_scope()` commits successful work and rolls back
on failure, then closes the session. `models.JobApplication` maps Python fields to
columns; revisions `0001` and `0002` create the schema; PostgreSQL's real table enforces
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
.\.venv\Scripts\python.exe -m uvicorn main:app --host 127.0.0.1 --port 8000 --no-proxy-headers --no-access-log
```

Without `--run-db`, database checks explicitly skip. With it, missing/broken
configuration fails; no SQLite fallback is used. Tests verify real columns and
constraints, commit/read through fresh connections, permit duplicate company/role,
and provoke check-constraint failures to prove the whole transaction rolls back.
Tests connect only as the dedicated test role. They delete only synthetic UUIDs
created by that test (or the restart test's unique synthetic company marker); they
never truncate tables or touch development data. Migration tests create random
temporary schemas inside applysync_test and roll their entire transaction back.
A killed process may leave synthetic test records. API ordering checks scope to
the synthetic owner; unrelated records are excluded before pagination.

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
Current schema revision is **0002**. All real application endpoints require a
valid cookie session. POST additionally requires trusted Origin and
`X-ApplySync-CSRF: 1`; the integrated frontend supplies these automatically.
Start locally with the Uvicorn command above; interactive API docs are at `/docs`.
`main.app` selects development configuration. Automated API checks explicitly use
`create_app("test")` and verify the test database/role/revision before any writes.
There is no request parameter that switches databases.

| Request | Result |
| --- | --- |
| `POST /applications` | 201 with one stored application, after a successful commit. |
| `GET /applications?limit=20&offset=0` | 200 with `{ "items": [...], "limit": 20, "offset": 0 }`. |
| `GET /applications/{id}` | 200 with one application, or 404 `{ "detail": "Application not found" }` for an absent or other-owner valid UUID. |
| Invalid body, UUID or pagination | 422 with structured errors that omit submitted input and exception context. |
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

Suggested learning checkpoint (not yet completed): after signing in through the
frontend, submit a whitespace-only company and locate the string constraint in
`schemas.py`. Direct unauthenticated PowerShell POSTs now fail request protection
or authentication first. The detailed request-flow and earlier transaction
exercises remain pending; this task does not claim they were completed.


## Build 4 Task 1: Gmail connection setup (local only)

The settings page is **http://127.0.0.1:5173/settings/gmail**. Sign in to
ApplySync first at **http://127.0.0.1:5173/login**. Google authorization is a
separate connection, not an alternative ApplySync login. Missing Gmail settings
leave health, authentication and manual tracking available.

Existing databases have been upgraded to `0003` in this workspace. For another
checkout, inspect `python -m alembic upgrade 0002:0003 --sql`, then run the ordinary
`upgrade head` for dev and `-x target=test upgrade head` for test. Do not provision
or reset an existing database. The new migration only adds two Gmail tables.

### One-time Google Cloud setup

1. Open [Google Cloud Console](https://console.cloud.google.com/) and create/select
   a dedicated ApplySync development project. In **APIs & Services > Library**,
   find **Gmail API**, then **Enable**. No API key or service account is required.
2. Open **Google Auth platform > Branding**. Choose **Get Started** if needed;
   set the app name to ApplySync development, select your support email, provide
   your contact email and complete the consent setup. Choose **External** for a
   personal Gmail account.
3. In **Audience**, retain **Testing** status. Under **Test users > Add users**, add
   only the Google accounts you intend to test with. Save; do not publish the app.
4. In **Data Access > Add or Remove Scopes**, select only `openid`, `email`
   (the Console may display `https://www.googleapis.com/auth/userinfo.email`), and
   `https://www.googleapis.com/auth/gmail.readonly`. Save. Readonly is a restricted
   mailbox-wide scope; a label is not an OAuth restriction. This task makes no
   mailbox requests. Public release/verification is outside this task.
5. In **Clients > Create Client**, choose **Web application**, name it ApplySync
   local, and add exactly this **Authorized redirect URI**:
   `http://127.0.0.1:8000/gmail/callback`. This is a server-side code flow, so
   **Authorized JavaScript origins can remain empty**. The frontend origin used
   by ApplySync is exactly `http://127.0.0.1:5173`; it is not the callback URI.
6. From the repository root run:

   ```powershell
   .\.venv\Scripts\python.exe -m pip install -r requirements.txt
   .\.venv\Scripts\python.exe -m scripts.setup_gmail
   ```

   Open the ignored root `.env` in VS Code locally. Enter the new client's ID in
   `APPLYSYNC_GOOGLE_CLIENT_ID` and its secret in `APPLYSYNC_GOOGLE_CLIENT_SECRET`.
   The helper appends missing settings only and generates
   `APPLYSYNC_GMAIL_ENCRYPTION_KEY` without displaying it. Keep its generated value;
   it is separate from `APPLYSYNC_AUTH_SECRET`. Existing placeholders/invalid
   settings are deliberately not overwritten; correct those locally.

   Keep `APPLYSYNC_GOOGLE_REDIRECT_URI=http://127.0.0.1:8000/gmail/callback` and
   `APPLYSYNC_GMAIL_FRONTEND_ORIGIN=http://127.0.0.1:5173`. Do not use `localhost`
   for this flow, put secrets into frontend variables, or share `.env`, OAuth
   URLs containing codes/state, cookies, or screenshots of credentials.
7. Start the backend and frontend in separate PowerShell terminals if not already
   running. Gmail settings are loaded on each operation, so entering them does not
   require a server restart in the current implementation.

   ```powershell
   # Repository root:
   .\.venv\Scripts\python.exe -m uvicorn main:app --host 127.0.0.1 --port 8000 --no-access-log
   # Another terminal:
   cd frontend
   npm.cmd ci
   npm.cmd run dev -- --port 5173 --strictPort
   ```

   Sign in on 127.0.0.1, open Gmail settings, choose Connect Google account, and
   authorize only the intended test account/scopes. Confirm the connected address,
   refresh the settings page, then disconnect. Google may require reauthorization
   while the app remains in Testing. Live provider compatibility, consent and
   revocation must be verified here; mocked tests are not a live OAuth result.

Keep the encryption key private and backed up securely. Changing/losing it makes
existing encrypted grants unusable; disconnect and authorize again, rather than
silently overwriting the key. No automatic key rotation is implemented.

### Connection contract and safeguards

- `GET /gmail`: current user's `{available,status,email,revocation_warning}`.
  Status is `not_connected`, `connected`, `disconnected`, or `reauthorization_needed`.
  No token, database state hash, verifier, or provider diagnostic is returned.
- `POST /gmail/start`: authenticated, exact allowed Origin and
  `X-ApplySync-CSRF: 1`; returns one Google `authorization_url`. That protocol URL
  necessarily contains random OAuth state and public client metadata, never a
  client secret or PKCE verifier. Only the latest pending flow per user is valid.
- `GET /gmail/callback`: Google browser redirect; requires the same ApplySync
  session, valid one-use state within ten minutes, and the matching PKCE verifier.
  Missing authentication returns 401. Other handled failures redirect to the fixed
  settings URL with a safe result code. No caller-provided return URL is accepted.
- `POST /gmail/disconnect`: same write protections; affects only the current
  user. Clears stored authorization and pending state and attempts Google revocation.
  Provider timeout/failure still commits local disconnection and a warning.
  Revocation and the local update are serialized in one transaction: local fields
  are cleared before the provider call, but durable commit follows that bounded
  call. A process/database failure can leave the result uncertain; refresh status.
  After a confirmed warning, remove access in
  [Google account connections](https://myaccount.google.com/connections).
  The token is erased, so there is no automatic server-side revocation retry.

Disconnect explicitly before choosing a different Google account. Same-account
reauthorization preserves the old encrypted refresh token only when Google omits
a new one and a refresh confirms the old grant is usable. Access/ID tokens remain
in memory. Logout revokes the ApplySync session and pending OAuth state, but does
not disconnect a previously committed Gmail grant. No connection grants access
to another ApplySync user's data.

### Reproducible checks

```powershell
# Root, dedicated test database already migrated:
.\.venv\Scripts\python.exe -m pytest --run-db -q -p no:cacheprovider --tb=short
.\.venv\Scripts\python.exe -m pip check
.\.venv\Scripts\python.exe -m scripts.run_frontend_integration
# Frontend directory:
npm.cmd run typecheck
npm.cmd run build
npm.cmd test
npm.cmd run test:e2e
```

Google endpoints are faked in automated checks; no real mailbox is used. The real
browser/database runner verifies two-account authentication/application regression
against `applysync_test` only and cleans its own synthetic records. Its screenshots
now default to ignored `frontend/test-results/integration-screenshots`, preserving
historical review images. The Gmail browser screenshots are intentional synthetic
review evidence in `docs/screenshots/Build4_Task1`.

See [Build 4 Task 1 review](docs/Build4_Task1_Review.md) for source, security decisions,
exact execution evidence and official documentation. Gmail label/filter verification
and any message ingestion remain future work. Earlier learning exercises remain pending.
