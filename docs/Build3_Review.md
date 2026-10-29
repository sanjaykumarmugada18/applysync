# Build 3 — Authentication & Ownership review

## Approved checkpoint update ? 29 October 2026

Sanjay confirms the following as **user-reported verification**, not independently
rerun by the agent on this date:

- Registration and application creation passed.
- Session and record persistence across reload passed.
- Logout blocks private access; login restores access.
- Account B cannot list or directly open account A's application.

No repeat of these manual checks was requested. The older sections below preserve
September's review/evidence history; references there to pending manual checks and
uncommitted state describe that earlier point, not this approved save operation.
The detailed transaction, request-flow and focused learning exercises remain
pending. Legacy assignment is not confirmed and was not performed.

Fresh inspection found main at base/current pre-commit HEAD
`699a1c91c06976dbc884851f629c7075988a073c`, no staged files, and the intended Build 3
work still uncommitted. All **34 normalized-text SHA-256 fingerprints matched**
the prior review, and the frontend package manifest/lockfile were unchanged.
Authentication, fixed JWT validation, durable logout revocation, cookie/CSRF/CORS,
owner filtering before pagination and direct-ID access, and account-switch cache
cancellation/isolation were inspected again; no concrete blocking issue found.
Only this handoff and the README's manual-verification status changed today.

Reused historical agent execution: **88 backend tests, 26 frontend component tests,
9 Chromium checks, one real two-account browser/database flow, typecheck/build,
and migration consistency checks passed**. These were not rerun merely because
of elapsed time; no executable or dependency configuration changed.

Fresh read-only dedicated-role checks: development and test are at revision 0002;
development has exactly two NULL-owner legacy records. No records were changed,
assigned or deleted. NULL ownership remains intentional quarantine, inaccessible
through ordinary APIs. Explicit local assignment remains optional follow-up for
making those records available to Sanjay's intended account; no new migration is
needed for that assignment. The actual utility syntax and safeguards remain below.

The authorized checkpoint message is `Add authentication and application ownership`.
Commit ID and live push verification are reported after Git completes. A fresh
origin fetch is used to check ancestry before a normal push; no merge, rebase,
reset, amend or force-push is authorized or performed. Private configuration,
dependencies, build/cache/transient outputs are excluded; only intentional synthetic
review screenshots are included. Final staged checks passed: exact 41-file scope,
34 snapshot fingerprints, `git diff --cached --check`, private-value comparison
and secret-pattern scans. No unrelated unstaged/untracked files remained. The
fresh origin fetch matched the base commit (zero divergence before committing).

Build 3's implementation and user-reported behaviour are ready to hand off to
**Build 4, Task 1 ? Gmail connection and disconnection**. Outstanding learning and
legacy-data items remain explicitly carried forward. Gmail work has not started;
this checkpoint does not claim production readiness or completed learning exercises.

## Resume audit and finalization

On resumption, actual source, complete integration diff, security assertions,
Git status and available execution results were inspected before edits. No
executable source had changed since the final successful checks below. Source
contents and modification times were consistent with the final implementation
and test-fix steps recorded in this conversation; the persisted Playwright
last-run result was also `passed`. The previous handoff stopped before its code
appendix/final audit, not before implementation.

This resumption changes documentation only: it completes the code/diff appendix,
records the final Git state, corrects screenshot-output documentation and clarifies
assignment of exactly the two legacy UUIDs. The **88 backend, 26 component, 9
Chromium, 1 real integration, typecheck/build and migration consistency results
below are reused historical agent-executed evidence**, not newly rerun results.
No implementation fix or redesign was necessary.

Fresh read-only checks confirmed development and test revision 0002, exactly two
development applications and exactly two NULL owners, valid local authentication
configuration (values suppressed), and the utility's actual `--help` syntax.
No migration or record assignment was repeated. Both servers had stopped during
the interruption; only the project backend/frontend were started, after verifying
ports 8000/5173 were free. Final HTTP/security probes are recorded below.

The final appendix includes text diffs, complete new source/test files and SHA-256
fingerprints for future comparison. It excludes all private configuration,
dependency/build output, temporary test output and binary reference contents.

## Result and checkpoint identity

Implemented in bounded steps: backend identity/ownership, frontend session state,
then security and real browser/database verification. Ready for source and manual
review; **not committed or pushed**, and not declaring the whole stage complete.

- Repository: `C:\Users\sanja\Desktop\ApplySync`, branch `main`.
- Base and current HEAD: `699a1c91c06976dbc884851f629c7075988a073c`,
  `Connect ApplySync frontend to application APIs`.
- Initial working tree was clean, with no staged files or nested AGENTS.md.
- Root instructions and reference v2.0 pages **3, 6, 7, 8 and 17** were read from
  the actual PDF. PDF extraction tooling was installed only in ignored temporary
  reference storage, not added to application dependencies.
- The latest Build 2 review and current implementation were inspected. Prior
  user-reported design, persistence and Board/List approval remain historical
  user evidence. No Build 3 manual check or learning exercise is claimed completed.
- All current changes are unstaged; the source snapshot below includes new files.
  Origin remains the existing GitHub repository; no commit/push was attempted.

## Behaviour and security decisions

Registration validates/normalizes email and creates a user and eight-hour session
in one transaction, returning 201 `{id,email}` and an HttpOnly JWT cookie. Login
verifies Argon2id and returns 200 with the same safe identity shape. `/auth/me`
restores identity; logout returns 204 only after deleting the database session.
JWT replay after logout fails, even across server restart. No token is returned
to JavaScript or stored in web storage. All sensitive routes use `no-store`.

Email-validator normalizes syntax without deliverability/DNS checks; this version
uses an ASCII local part and lowercases the entire normalized email as a deliberate
case-insensitive identity policy. A database uniqueness constraint handles races;
a lowercase check prevents accidental mixed-case direct inserts. Concurrent
registration yields one success and one 409. The 409 discloses that registration
cannot be completed for that email; login always uses generic invalid credentials.
Email verification and recovery are not implemented.

Passwords have 12–128-character bounds, with no trimming, truncation or composition
rules. Argon2id uses maintained library defaults and checks for rehash on login.
Unknown emails still incur a dummy verification. Validation errors strip raw
input/exception context so a rejected password cannot be echoed. Database and
configuration exceptions have generic responses and no raw exception logging.

JWT validation fixes HS256 rather than trusting the supplied algorithm, requires
issuer/audience/sub/jti/iat/exp, parses UUID identifiers, checks lifetime and verifies
the live session's user and expiry. Claims contain identifiers and timestamps,
no email, password or Gmail credentials. The signing secret is generated locally;
there is no fallback. Cookie attributes are HttpOnly, SameSite=Lax, Path=/,
host-only and Max-Age=28800. Explicit local mode permits HTTP; production mode
requires HTTPS origins and sets Secure. Deletion uses matching attributes.

CSRF uses a custom-header JSON API pattern: every unsafe request independently
requires an exact allowlisted Origin and `X-ApplySync-CSRF: 1`. This includes
registration, login and logout. Missing, null, foreign or invalid values return
403. HTML forms cannot add the header; browser fetch must preflight, and narrow
credentialed CORS grants only the configured frontend origins. The header is not
a secret token; security depends on the browser origin/header restrictions and
trusted frontend origins. CORS alone is not used as the authorization mechanism.

Login/registration share a locked, bounded per-process limiter: 10 attempts per
hashed email, 50 per client IP in 15 minutes, at most 10,000 retained entries.
All attempts count; 429 includes Retry-After. Restart resets it and workers do not
share limits. This is a local single-process defence; distributed rate limiting,
proxy topology and deployment hardening remain outside this task. Local startup
disables forwarded-header trust. Expired session rows remain inert until future
maintenance; there is no background cleanup infrastructure.

Every real application create derives owner from `current_user`. List applies
`owner_id == user.id` **before** ordering/limit/offset. Detail requires both UUID
and owner. Other-owner and nonexistent records return the same 404; no owner ID
is accepted in creation input. Responses keep the existing five fields. Real
Board/List, pagination and page-only search still share API records/cache. Stage
not recorded remains display-only. Synthetic preview remains public and separate.

Frontend restoration hides private content while checking `/auth/me`; 401 signs
out, while network/server failure shows a retry state. Login return destinations
are restricted to internal application routes. Identity-keyed `PrivateCache`
instances cancel/clear on unmount; each new account gets a distinct query client.
Writes have abort signals and post-await guards, so old-account completions cannot
navigate or repopulate another account's cache. POSTs never automatically replay.
Session checks repeat on focus and every minute and do not interrupt pending auth
submissions. Idle timer throttling can delay the UI reaction; the backend always
enforces expiry. Cookie identity is shared between tabs, so simultaneous manual
accounts should use separate profiles/incognito. Requests authorized before a
logout may finish; logout does not undo already committed work.

## Migration and remaining local action

Inspected `0002_identity_ownership.py` and Alembic-generated SQL before application.
It creates `users`, `auth_sessions`, an owner FK and owner/order index. It neither
assigns nor deletes legacy applications. Downgrade intentionally refuses identity
loss; `create_all()` is never used.

Before development migration: revision 0001, two legacy records, original schema.
After migration and repeated upgrade: revision **0002**, both records unchanged
in every original column and both owners NULL. The comparison stayed in memory;
no record contents were printed. Test is also at 0002. `alembic check` reported
no new upgrade operations for each target. Migration rehearsals cover empty and
representative legacy schemas in random transactionally rolled-back schemas
inside verified `applysync_test`; no development test writes occurred.

`owner_id` remains nullable deliberately: NULL quarantines preserved legacy data,
and ordinary users cannot see it. This is not a default account or first-user claim.
Ownership migration is **not fully finalized** while the two assignments remain
pending. No NOT NULL conversion is claimed or silently scheduled.

After Sanjay registers the intended account, one precise local action is:

```powershell
.\.venv\Scripts\python.exe -m scripts.assign_legacy --interactive
```

The utility lists only unassigned UUIDs locally and asks for an existing account
email and explicitly selected UUIDs. It locks and validates the entire selection,
then assigns transactionally. An unknown account, missing UUID or already-owned
record aborts all changes. Synthetic tests prove partial assignment cannot occur.
No credential needs to be shared in chat. The utility has not been run on dev.

## Files and responsibilities

| Files | Responsibility |
| --- | --- |
| `auth.py` | Identity schemas, normalized credentials, Argon2, JWT, revocable sessions, current-user dependency, bounded limiter and four auth endpoints. |
| `auth_config.py` | Secret validation, explicit local/production cookie mode and exact origin policy. |
| `models.py`, `migrations/versions/0002_identity_ownership.py` | User/session schema, preserved legacy ownership, FK and pagination index. |
| `migrations/env.py` | Supports an explicitly supplied connection for isolated migration rehearsal; ordinary target safeguards remain. |
| `applications.py` | Authenticated creation and owner-scoped list/detail queries. |
| `main.py` | Independent CSRF request checks, credentialed CORS, input-safe validation errors, auth routes, health preserved. |
| `scripts/setup_auth.py` | Append generated local signing configuration only if missing; never overwrite or print secrets. |
| `scripts/assign_legacy.py` | Local explicit account/UUID assignment with transactional validation and dev target checks. |
| `frontend/src/Auth.tsx` | Session restoration, login/register UI, route gate, safe return path, cache lifecycle and logout. |
| `frontend/src/App.tsx`, `components/Shell.tsx` | Authenticated routes, visible identity/logout; public sample preview stays separate. |
| `frontend/src/api.ts`, `StoredApplications.tsx` | Credentialed requests, CSRF header, 401 handling, cancellation and guarded mutation completion. |
| `frontend/src/styles.css` | Small auth surface/responsive identity styling using existing visual design. |
| `tests/test_auth.py`, `test_ownership_migration.py` | Security, concurrency, ownership, legacy assignment and migration assertions. |
| `tests/conftest.py`, existing API/CORS/persistence/restart tests | Revision 0002 target guard and authenticated regression expectations. Existing application unit tests explicitly override identity; dedicated security tests use real sessions. |
| `frontend/src/Auth.test.tsx`, `StoredApplications.test.tsx` | Auth/cache race/expiry/logout tests and existing feature regression under a mocked session. |
| `frontend/e2e/*.spec.ts`, Playwright configs | Authenticated feature mocks and real two-account browser flow; traces disabled to protect credentials. |
| `scripts/run_frontend_integration.py` | Verified test role/revision, generated synthetic accounts, isolated server, independent committed ownership check and scoped cleanup. |
| `requirements.txt`, `.env.example`, `.gitignore`, `README.md` | Pinned compatible auth dependencies, placeholder config, generated-file exclusion and reproducible Windows setup. |
| `docs/screenshots/Build3/*` | Intentional synthetic visual evidence; no passwords, cookies or real records. Historical Build 2 screenshots preserved. |

## Execution paths and concepts

Success: `AuthForm.submit` calls `AuthProvider.signIn`, then `api.request` sends a
credentialed POST with custom header. `main.request_security` checks Origin/header.
`auth.login` validates normalized credentials, performs `hasher.verify`, and
`issue_session` prepares a JWT and database session in `session_scope`. Only after
commit does `set_cookie` issue the HttpOnly cookie. Subsequent GET enters
`auth.current_user`, validates JWT plus live session, and `applications.list_applications`
filters by the returned identity. Logout deletes that session before clearing the
cookie; React unmounts/cancels/clears its private query client immediately.

Failure: B requests A's detail UUID. `current_user` correctly identifies B, then
`get_application` requires both A's UUID and B's owner ID. No row matches; it returns
the same 404 as a missing UUID. Separately, a stale cookie after logout fails the
database-session lookup with 401; `api.request` signals expiry, `SessionGate` removes
private content/cache, and login asks the user to explicitly resubmit unfinished work.

- **Authentication** establishes identity (`current_user`); **authorization** checks
  access to a specific record (`owner_id == user.id`). Frontend hiding is not enough.
- **Hashing** stores a one-way password verifier; **encryption** is reversible and
  is not used for passwords. JWT signing protects integrity, not confidentiality.
- **HttpOnly** prevents JavaScript reading the session cookie; **Secure** restricts
  browser cookie transmission to HTTPS. Neither replaces CSRF checks.
- **401** means missing/invalid/expired identity (or invalid login); **403** means
  request protection rejected a write; **404** conceals whether another user's UUID
  exists. **422** covers sanitized validation and **429** attempt limits.

## Verification evidence

All results here are agent-executed for Build 3, not reused unauthenticated evidence.

| Exact command / check | Observed result |
| --- | --- |
| `.venv\Scripts\python --version` | Python 3.14.2, unchanged. |
| `.venv\Scripts\python -m pip install argon2-cffi PyJWT email-validator` | Windows-compatible wheels installed; versions pinned with transitive dependencies. |
| `.venv\Scripts\python -m pip check` | No broken requirements. |
| `.venv\Scripts\python -m alembic -x target=test upgrade head --sql` | SQL inspected: additive schema, no legacy UPDATE/DELETE. |
| `.venv\Scripts\python -m alembic -x target=test upgrade head` (repeated) | Success; revision 0002. |
| Development `command.upgrade(Config('alembic.ini'), 'head')` twice, wrapped with before/after reads | Success; all original values preserved, two NULL owners. |
| `.venv\Scripts\python -m alembic check` and `... -x target=test check` | Both: No new upgrade operations detected. |
| `.venv\Scripts\python -m pytest --run-db -q -p no:cacheprovider --tb=short` | **88 passed**, 13.94s; two dependency deprecation warnings, no skips. Includes real Uvicorn restart with cookie restoration. |
| `npm.cmd run build` from frontend | Typecheck passed; Vite 1955 modules, 4.96s; JS 335.67 kB / gzip 105.47 kB; CSS 20.99 kB / gzip 5.61 kB. |
| `npm.cmd run test` | **26 passed**, five files, 4.81s. |
| `npm.cmd run test:e2e` | **9 Chromium tests passed**, 13.0s; preview and authenticated-mock feature regression. |
| `.venv\Scripts\python -m scripts.run_frontend_integration` | **1 real two-account Chromium/FastAPI/PostgreSQL flow passed**, 13.5s; committed values AND owner independently checked, run-owned fixtures cleaned. |
| Development HTTP probes after startup | Frontend /login 200; health 200 healthy; unauthenticated /applications 401. No development write. |
| `git diff --check` | Passed; only Git's informational LF/CRLF notices. |

Important assertions inspected: concurrent registration statuses `[201,409]` and
one row; hash prefix/verification without plaintext; logout cookie replay 401;
tampered/expired/malformed/missing-claim/wrong-algorithm/revoked tokens 401;
CSRF missing/invalid/untrusted checks for all four write routes; owner filtering
before pagination; both users denied a NULL owner; forged owner input 422;
assignment rollback; old account's deferred response cannot appear in B's cache;
401 creation produces exactly one POST; logout network failure does not falsely
claim signed-out success. Tests preserve unrelated records and never truncate.

Earlier attempts, not hidden: dependency download and frontend subprocesses needed
sandbox escalation; full pytest initially had four temporary-directory permission
errors (81 other tests passed) and then passed with permission. One password-echo
assertion used a sentinel matching `string_too_short`; corrected the sentinel.
TypeScript caught unsupported RTL role-query `exact` options; removed them.
One later component run had 25 passes and a timing-sensitive dialog-role failure;
the assertion now waits for modal opening and the full 26-test rerun passed.
No failing final check remains. Deprecations concern Starlette's current HTTPX
TestClient compatibility and an AnyIO alias; dependency checks pass.

## Review limits and learning handoff

This is local development, not a production-readiness claim. No Gmail, events,
stage tracking, recovery/email verification, distributed throttling, deployment,
refresh tokens or background services were introduced. Production Secure policy
is unit-tested; actual HTTPS deployment, Firefox/WebKit, physical devices and
screen readers were not tested. Idle eight-hour wall-clock waiting was not run;
expiry is exercised with expired JWTs/server session rows and frontend 401 checks.

Sanjay's manual two-account check is documented in README and remains pending.
Focused exercise: locate the owner predicate in `applications.get_application`
and explain why copying another user's UUID returns 404. The prior detailed
transaction and request-flow exercises remain pending. No learning completion is
inferred from automated tests. Assignment and source/manual review remain before
calling this stage fully finalized. Commit/push awaits a later explicit request.

Local interface: http://127.0.0.1:5173/register (login at /login); backend
http://127.0.0.1:8000. Both servers were started in hidden local processes after
checking the ports and respond. Browser rendering was independently exercised via
the isolated test stack, not by creating an account in the development database.

## Dependency references

- [Argon2 high-level hash/verify/rehash behaviour](https://argon2-cffi.readthedocs.io/en/stable/howto.html)
- [PyJWT fixed algorithm and required claim validation](https://pyjwt.readthedocs.io/en/stable/api.html)
- [Email normalization and validation](https://github.com/JoshData/python-email-validator)
- [OWASP custom-header JSON API CSRF defence](https://cheatsheetseries.owasp.org/cheatsheets/Cross-Site_Request_Forgery_Prevention_Cheat_Sheet.html)

Installed: argon2-cffi 25.1.0, bindings 26.1.0, cffi 2.1.1, pycparser 3.0,
PyJWT 2.15.0, email-validator 2.3.0, dnspython 2.8.0. Existing stack retained;
frontend manifest and lockfile unchanged. Reproducible commands are in README.

## Fresh resume checks and final Git state

- HTTP GET frontend `/login` and `/register`: 200 each.
- Real development `/health`: 200 `{"status":"healthy"}`.
- Unauthenticated `/auth/me` and `/applications`: 401 each.
- Twelve write probes across register/login/logout/create with absent, invalid or
  foreign Origin/header combinations: all 403, no database write performed.
- Credentialed trusted preflight: 200 and exact allow-origin; untrusted preflight:
  400 with no allow-origin. These were real HTTP, not in-memory probes.
- Local auth configuration validation: passed, all values suppressed.
- Dedicated development/test role and database checks: passed, both revision 0002.
- Development: two applications, both unassigned; no assignment or data mutation
  during this resume. Their unchanged original fields were verified before/after
  migration in the prior execution; this resume checked counts/state only.
- `python -m scripts.assign_legacy --help`: confirms `--interactive` or
  `--email EMAIL --ids UUID [UUID ...]`. After account registration, the interactive
  command should receive exactly the two displayed legacy UUIDs separated by a
  comma. No additional schema change is needed for assignment; nullable ownership
  remains intentional, and assignment/manual verification is still outstanding.
- Private-value scan of all intended changed/new text files against loaded local
  database credentials and signing secret: no matches; values were not printed.
- `.env` is ignored and not tracked. Generated dependency/build/test directories
  remain excluded. No binary reference changes. No secrets in the code appendix.
- Branch `main`; base/current HEAD remain
  `699a1c91c06976dbc884851f629c7075988a073c`. No staged files, no commit or push.
  Last live origin/main check before interruption matched this hash; this resume
  does not claim a new live GitHub check.
- Existing backend/frontend were absent; only project servers started. Backend
  process 1000 and frontend launcher 6132 responded. No unrelated process stopped.
  Rendered visual evidence is reused from the successful unchanged-code Chromium
  run, rather than claiming a new manual browser inspection.

### Git working-tree snapshot

```text
 M .env.example
 M .gitignore
 M README.md
 M applications.py
 M frontend/e2e/integration.spec.ts
 M frontend/e2e/preview.spec.ts
 M frontend/e2e/stored.spec.ts
 M frontend/playwright.config.ts
 M frontend/playwright.integration.config.ts
 M frontend/src/App.tsx
 M frontend/src/StoredApplications.test.tsx
 M frontend/src/StoredApplications.tsx
 M frontend/src/api.ts
 M frontend/src/components/Shell.tsx
 M frontend/src/styles.css
 M main.py
 M migrations/env.py
 M models.py
 M requirements.txt
 M scripts/run_frontend_integration.py
 M tests/conftest.py
 M tests/test_api_restart.py
 M tests/test_applications.py
 M tests/test_cors.py
 M tests/test_persistence.py
?? auth.py
?? auth_config.py
?? docs/Build3_Review.md
?? docs/screenshots/Build3/login.png
?? docs/screenshots/Build3/stored-detail.png
?? docs/screenshots/Build3/stored-list.png
?? docs/screenshots/Build3/stored-mobile-board.png
?? docs/screenshots/Build3/stored-mobile-detail.png
?? docs/screenshots/Build3/stored-mobile-list.png
?? frontend/src/Auth.test.tsx
?? frontend/src/Auth.tsx
?? migrations/versions/0002_identity_ownership.py
?? scripts/assign_legacy.py
?? scripts/setup_auth.py
?? tests/test_auth.py
?? tests/test_ownership_migration.py
```

## Source fingerprints (UTF-8 text with normalized newlines)

| File | SHA-256 |
| --- | --- |
| `.env.example` | `550a305c210e99b36d13337fbcc45df7437453be5773da5122ec1a1763052e83` |
| `.gitignore` | `2dc3146c731281a7ae5ff79381ff202dc94474081e8669107ed498c53b3e55f3` |
| `README.md` | `165f44c452ad22c7c5bc5817d6059b11395854086ae5fa050120c3bbd920e4b8` |
| `applications.py` | `6698f494ed48948e56cf0ac88f1e0415cc5cf56a73cfe5152358a2338161cb2e` |
| `auth.py` | `d74a480a70af460ab43a6310f9b0c41686f9ccaf7b7a4ad389dfea907a6a5d52` |
| `auth_config.py` | `e511d3aed0f65cd6c3751b372cdc72dccd2e3b9d511e609649627b2e29d987ae` |
| `frontend/e2e/integration.spec.ts` | `efc8d255d9444b1e1e34381410f09fb6227d8c2fdc355225ea14c1a2f26fda9f` |
| `frontend/e2e/preview.spec.ts` | `6da074abcfd101aeaf005ecd6de5864033d05dfd1cc3fb5420fd51edafd0567b` |
| `frontend/e2e/stored.spec.ts` | `1a7bd8300c579ab2e23c69f9a0c58c94534ff6c7988582ce9dfcfe4cf82dc9e0` |
| `frontend/playwright.config.ts` | `fa1466f25f39909cdebd974f184d6c25ac886536fcc73bbf9cf9c21efca0a706` |
| `frontend/playwright.integration.config.ts` | `69ffc6207c96b17caf874fe72146242216f7435402dff3c6a81416aa37607bd2` |
| `frontend/src/App.tsx` | `9a83cc40fa02c6f7fc75f0b2cbeab830916d70d2526357b90e8e957c00f66c20` |
| `frontend/src/Auth.test.tsx` | `0ebbe51f6eac3eff88ddd2a1e3b82f2e78fbd51439edaceb3ac160708686cbe1` |
| `frontend/src/Auth.tsx` | `50d28b02fe9308794723402166361d07d43f0d246f4af6fbaa6b5e6d5b4e50d2` |
| `frontend/src/StoredApplications.test.tsx` | `dc00d0c9e7fa91c0a10aa3cda3a7bf835b6bfba1db64480c1ed6a546dd9b6d86` |
| `frontend/src/StoredApplications.tsx` | `48103684061924abfb4de333acf4363b8c3dd570ece325950db8b70a7a3ca126` |
| `frontend/src/api.ts` | `ff86594a60e97ccabf3bc8f83ad03bf96e741273ce78e11db3da2defe44ed489` |
| `frontend/src/components/Shell.tsx` | `2aeca68fa17444c2dfa53855e2ec891653a9c27cf846d502a03807ac9a3a7846` |
| `frontend/src/styles.css` | `f3ad5754f2d538436b802fc87e38a16c51db8b0fda7d5c664ac95f7862b8f1a4` |
| `main.py` | `2b38dcecef9c283a38632e5ec6d716748f3d8be5f2805b2a0452fe87f64a208c` |
| `migrations/env.py` | `d9bdd52a45eeb36a97064cc1db7eba0e49581551cb155ae834b8aaf509366813` |
| `migrations/versions/0002_identity_ownership.py` | `e55f41aa81b893b65670481ad95276d3a97bc904a6f55eb414dc3c1f05d640da` |
| `models.py` | `688b77892147ecffbe8d58200391a7c3c161f313305f3d6fa9606eaf5d38cb99` |
| `requirements.txt` | `9bdf8551acb5206a94b32222fe24e81e9a1b39018538b0be6616111814831ae1` |
| `scripts/assign_legacy.py` | `8c8b5e4a790cbc0c0eb13bfdf781a2a854a5e33c973ff78068d0a9f2a4b19b56` |
| `scripts/run_frontend_integration.py` | `361603bc103c758fd6d1e291e83382c637d04ac47a7542f80d3e032d80e6a647` |
| `scripts/setup_auth.py` | `0ea96f7b57dc72099a43973afe91b071583ed65aa04c9e5fa1281dff48b10e25` |
| `tests/conftest.py` | `06fc2245c9f3026f92ec265850ff437dfa99462d6f71396eacf31d86be3d4c05` |
| `tests/test_api_restart.py` | `03d72f7432e154faebf9c2b87b9c244c44ce91b865bbdeed091fdd135a0e5409` |
| `tests/test_applications.py` | `364188a451e48126b0efd5241b02fd3f5ff84abbb4e741ec7deaa57561e6ecc6` |
| `tests/test_auth.py` | `28728619eb72091811219d78bc0ecb3ecca33ab682257cdf7e9eafc85a835ae5` |
| `tests/test_cors.py` | `9e9800e14d9cd6419fc04e37688bc412673d7aeb6e782d0c4ea3dd2c6134ea0c` |
| `tests/test_ownership_migration.py` | `c7ff7553e441cfc822f79fd4549e913e29676808596eafe80b981074dedea165` |
| `tests/test_persistence.py` | `48b58c879beb4a13284339c939c0f7e1c5da623981ff5ef97b292485e4299ec5` |

## Relevant tracked-file diff

````diff
diff --git a/.env.example b/.env.example
index 3cc1b9d..d152890 100644
--- a/.env.example
+++ b/.env.example
@@ -6,4 +6,8 @@ APPLYSYNC_DEV_DB_USER=applysync_dev
 APPLYSYNC_DEV_DB_PASSWORD=replace-with-local-development-password
 APPLYSYNC_TEST_DB_NAME=applysync_test
 APPLYSYNC_TEST_DB_USER=applysync_test
-APPLYSYNC_TEST_DB_PASSWORD=replace-with-local-test-password
\ No newline at end of file
+APPLYSYNC_TEST_DB_PASSWORD=replace-with-local-test-password
+# Generate with python -m scripts.setup_auth; never use this placeholder.
+APPLYSYNC_AUTH_SECRET=replace-with-generated-64-hex-characters
+APPLYSYNC_AUTH_MODE=local
+APPLYSYNC_AUTH_ORIGINS=http://127.0.0.1:5173,http://127.0.0.1:4173,http://localhost:5173,http://localhost:4173
diff --git a/.gitignore b/.gitignore
index 140a15c..d6bae8d 100644
--- a/.gitignore
+++ b/.gitignore
@@ -8,6 +8,7 @@ pytest-cache-files-*/
 frontend/node_modules/
 frontend/dist/
 frontend/test-results/
+test-results/
 frontend/playwright-report/
 tmp/design-reference/
 tmp/frontend-resolution/
diff --git a/README.md b/README.md
index b1286a0..0ebe5eb 100644
--- a/README.md
+++ b/README.md
@@ -1,11 +1,133 @@
 # applysync
 AI-powered privacy-first job application tracker that automatically syncs Gmail application emails into a Kanban dashboard.

-Current scope: Build 2, task 2 connects the approved frontend to the PostgreSQL
-create/list/detail APIs. `/applications` displays stored data; the explicitly separate
+Current scope: Build 3 adds registration, login, revocable JWT-cookie sessions and
+server-side ownership to the integrated PostgreSQL create/list/detail APIs. `/applications` displays stored data; the explicitly separate
 `/preview/applications` retains the fictional Board/List preview. Gmail and automatic
-tracking above describe the project goal, not implemented features. This is local,
-unauthenticated development functionality, not a public deployment.
+tracking above describe the project goal, not implemented features. This remains local development functionality, not a public deployment.
+Read the Build 3 setup and security policy below before starting the backend.
+
+## Build 3 setup and session policy
+
+On an existing checkout, from the root in PowerShell (never reprovision databases):
+
+```powershell
+.\.venv\Scripts\python.exe -m pip install -r requirements.txt
+.\.venv\Scripts\python.exe -m scripts.setup_auth
+.\.venv\Scripts\python.exe -m alembic upgrade head --sql
+.\.venv\Scripts\python.exe -m alembic upgrade head
+.\.venv\Scripts\python.exe -m alembic -x target=test upgrade head
+```
+
+`setup_auth` appends a cryptographically generated 32-byte signing secret as hex
+and explicit `local` mode to the ignored root `.env` only if those keys are absent.
+It never prints or replaces existing values. Keep that file private. Invalid
+existing values require a local edit; do not paste them into chat. The checked-in
+`.env.example` contains placeholders only. Health remains available without a
+signing secret; authentication fails safely with a generic 500.
+
+The migration in this checkout has already been applied to development and test.
+Development's **two original records remain unchanged and unassigned**. Register
+an account first. Then run this one local action if you want to assign them:
+
+```powershell
+.\.venv\Scripts\python.exe -m scripts.assign_legacy --interactive
+```
+
+It lists only unassigned UUIDs, asks for an existing account email and the explicit
+UUIDs to assign, and commits all selected assignments together. A missing account,
+missing UUID or already-owned row aborts everything. No public claim endpoint or
+default account exists. Ownership migration is not fully finalized while these
+assignments remain pending; `owner_id` intentionally stays nullable to quarantine
+legacy records. New API writes cannot create ownerless applications.
+
+For the current two-record legacy set, enter your intended registered account's
+email, then the **two displayed UUIDs separated by a comma**. Do not select other
+records if the local list has changed. Non-interactive equivalent (placeholders):
+`python -m scripts.assign_legacy --email <existing-account-email> --ids <first-uuid> <second-uuid>`.
+After assignment, sign in as that account and reload; verify both records appear.
+The nullable column remains the intentional quarantine mechanism; no further
+schema migration is required to perform the assignment.
+
+| Endpoint | Contract |
+| --- | --- |
+| POST /auth/register | `{email,password}`; 201 `{id,email}` and session cookie; duplicate normalized email: 409. |
+| POST /auth/login | Same body; 200 `{id,email}` and new session; generic invalid credentials: 401. |
+| GET /auth/me | 200 `{id,email}`; missing/invalid/expired/revoked session: 401. |
+| POST /auth/logout | 204 after deleting the server session, then matching cookie deletion; invalid session: 401. |
+
+Email uses maintained email-validator, trims surrounding whitespace, validates
+syntax without DNS lookups, requires an ASCII local part, normalizes then
+lowercases the full address. The unique database column and lowercase check
+make duplicate creation safe under concurrency. Case-insensitive mailbox identity
+is a deliberate application policy. No verification email is sent in this stage.
+Passwords accept 12?128 Unicode characters, including spaces, without trimming,
+truncation or composition rules. Argon2id hashes use the library defaults; login
+rehashes if its parameters change. Passwords/hashes never appear in responses.
+Validation responses omit the usual raw input echo.
+
+Sessions last **8 hours from issuance**, with no refresh tokens or sliding expiry.
+PyJWT signs HS256; validation fixes that algorithm and requires issuer, audience,
+subject UUID, session UUID, issued-at and expiry. The matching database session
+must still exist and be unexpired. JWT claims contain identifiers/timestamps only.
+Cookie: `applysync_session`, HttpOnly, SameSite=Lax, Path=/, host-only, Max-Age=28800.
+Local HTTP explicitly uses Secure=false. `APPLYSYNC_AUTH_MODE=production` requires
+HTTPS-only `APPLYSYNC_AUTH_ORIGINS` and sets Secure=true. Production deployment is
+not implemented: frontend API configuration still permits loopback HTTP only.
+The intended topology is same-site frontend/API (same hostname locally), with
+exact origins allowlisted; cross-site deployment needs a separate review.
+
+Every unsafe request, including login/registration/logout, must provide an exact
+trusted `Origin` and `X-ApplySync-CSRF: 1`. The custom header forces browser
+preflight; HTML forms cannot supply it. The independent server check rejects
+missing/invalid headers and absent/null/untrusted origins with 403 even if CORS
+is bypassed by a direct client. This is the custom-header CSRF pattern for a
+JSON-only API, not a secret CSRF token. Only trusted frontend origins may execute
+scripts with this privilege. HttpOnly does not protect against actions by XSS.
+
+Logout deletes the durable session before returning; replay of that cookie fails
+immediately, including after restart. Requests already authorized before logout
+may finish. Other devices retain their own sessions. Expired session rows are
+inert; scheduled cleanup and account recovery are not implemented.
+
+Login and registration share per-process 15-minute limits: 10 attempts per hashed
+normalized email and 50 per client IP, with a bounded 10,000-entry map. All attempts
+count, including successes; response is 429 with Retry-After. Restart resets limits,
+and multiple workers do not share them. This is a single-process development
+control, not distributed abuse protection. Do not trust forwarded client IPs from
+untrusted proxies (`--no-proxy-headers` for the local Uvicorn command).
+
+React restores `/auth/me` before rendering private content, rechecks on focus and
+every minute, and treats expected 401 as signed out. Network failure shows a retry
+state rather than claiming logout. Private query clients are cancelled, cleared
+and unmounted on logout, identity change or session-check failure. Pending writes
+are aborted on unmount; POST never auto-replays after sign-in. The server may have
+committed a request whose response was lost; inspect your list before resubmitting.
+Browser timer throttling may delay idle expiry UI, but the server rejects expired
+credentials on every request. Use separate browser profiles/incognito for two
+simultaneous accounts because cookies are shared by tabs on the same hostname.
+
+### Manual two-account check (Sanjay reports passing, 29 October 2026)
+
+1. Open http://127.0.0.1:5173/register and register account A. Create a fictional
+   application; reload and try both Board/List views. Copy its detail URL.
+2. In an incognito window register B. A's record must not be in B's list, and
+   opening A's detail URL must say Application not found.
+3. Log A out and refresh. Sign in as B in that window: A's cards must not flash.
+   Close any incognito window when finished. These are your intentional dev records.
+
+Focused learning checkpoint: inspect `applications.get_application` and identify
+which condition would be missing if B could read A's copied UUID. Explain why the
+frontend route guard alone cannot provide this protection. Prior learning gaps
+remain pending, not implementation blockers.
+
+Official references used: [Argon2 password hashing](https://argon2-cffi.readthedocs.io/en/stable/howto.html),
+[PyJWT validation](https://pyjwt.readthedocs.io/en/stable/api.html),
+[email normalization](https://github.com/JoshData/python-email-validator), and
+[OWASP custom-header CSRF defence](https://cheatsheetseries.owasp.org/cheatsheets/Cross-Site_Request_Forgery_Prevention_Cheat_Sheet.html).
+Python 3.14.2 installation and `pip check` passed. Requirements pin PyJWT 2.15.0,
+argon2-cffi 25.1.0, bindings 26.1.0 and email-validator 2.3.0 plus their dependencies.
+No frontend dependency changed.

 ## Integrated interface (two PowerShell terminals)

@@ -15,7 +137,7 @@ follow the backend setup below first. Terminal 1, from the repository root:

 ```powershell
 Set-Location 'C:\Users\sanja\Desktop\ApplySync'
-.\.venv\Scripts\python.exe -m uvicorn main:app --host 127.0.0.1 --port 8000
+.\.venv\Scripts\python.exe -m uvicorn main:app --host 127.0.0.1 --port 8000 --no-proxy-headers --no-access-log
 ```

 Terminal 2, from `frontend/`:
@@ -29,7 +151,9 @@ npm.cmd run dev
 Open **http://127.0.0.1:5173/applications**. Backend health is
 http://127.0.0.1:8000/health and Swagger is http://127.0.0.1:8000/docs.
 Stop your own servers with Ctrl+C; reuse existing correct servers rather than
-starting duplicates. Restart an older backend process to load the new CORS policy.
+starting duplicates. Restart an older backend process to load authentication.
+Use **127.0.0.1 for both servers**; do not mix localhost with 127.0.0.1.
+Real application routes redirect to login; the sample preview remains public.

 The public `VITE_API_BASE_URL` defaults to `http://127.0.0.1:8000`. To configure a
 different local port, copy `frontend/.env.example` to `frontend/.env.local` **only
@@ -40,9 +164,9 @@ or database URL. Root backend `.env` is separate and must never be copied into
 the frontend. The client accepts local HTTP origins only for this task.

 FastAPI allows exactly `http://localhost:5173`, `http://127.0.0.1:5173`,
-`http://localhost:4173` and `http://127.0.0.1:4173`, with GET/POST and Content-Type.
-There is no wildcard or credential support. CORS permits browser cross-origin
-reads; it is not authentication or ownership protection.
+`http://localhost:4173` and `http://127.0.0.1:4173`, with credentialed GET/POST, Content-Type and X-ApplySync-CSRF.
+There is no wildcard. Every write also checks the exact Origin and custom header
+on the server. CORS itself is not authentication or ownership protection.

 Stored records share Board/List views (List is the default). The Board uses one
 neutral **Stage not recorded** column and explains that grouping will be available
@@ -140,7 +264,9 @@ npm.cmd run test:e2e
 ```

 Browser tests use a temporary production preview server on port 4173 and save
-screenshots under `docs/screenshots/Build2_Task2/`. Keep that port free. Tests cover
+transient screenshots under ignored `test-results/` directories. The real guarded
+integration run saves intentional evidence under `docs/screenshots/Build3/`.
+Historical Build 2 images are not overwritten. Keep port 4173 free. Tests cover
 search/filter/view state, validation, preview creation/reset, route-backed details,
 keyboard handling, reduced motion and desktop/mobile layouts. Native dialog behaviour
 is tested in Chromium; the component-test DOM only supplies a minimal dialog stub.
@@ -211,8 +337,9 @@ liveness endpoint and does not assert database readiness.

 ### Inspect and apply migrations

-Read `migrations/versions/0001_job_applications.py` before these commands. This is
-an explicitly authored Alembic revision, not a claimed autogenerate result.
+Read both explicitly authored revisions in `migrations/versions/` before these
+commands. Revision `0002` preserves existing applications with NULL ownership;
+those records remain quarantined until explicitly assigned locally.

 ```powershell
 .\.venv\Scripts\python.exe -m alembic upgrade head --sql
@@ -229,8 +356,8 @@ an explicitly authored Alembic revision, not a claimed autogenerate result.
 The second upgrade should make no changes. Inspection prints only schema metadata,
 never application rows or connection settings. `alembic check` compares the real
 schema to model metadata. Do not use `Base.metadata.create_all()` to create tables.
-The reverse migration drops the application table and its records; it is provided
-for migration completeness, not part of normal setup or test cleanup.
+Revision 0002 intentionally refuses downgrade to prevent accidental loss of
+identity/ownership data. Do not reset development or downgrade to assign records.

 ## Initial schema decisions

@@ -244,17 +371,18 @@ for migration completeness, not part of normal setup or test cleanup.
 | `applied_on` | Required date explicitly supplied by the caller; distinguishes the actual application date from record creation. |
 | `created_at` | Required timezone-aware timestamp with PostgreSQL `now()` default. |

-All fields are non-null. PostgreSQL checks use its POSIX whitespace character class;
+These original fields are non-null. Build 3 adds nullable `owner_id` for legacy
+quarantine; every API-created row has an authenticated owner. PostgreSQL checks use its POSIX whitespace character class;
 they do not normalize or trim stored text. The 200-character limits and required
 application date are local implementation choices, not mandated by reference v2.0.
 Company + role is **not unique**: repeated applications and concurrent processes are
-allowed. No status enum, user ownership, events, or other future entities are added.
+allowed. Ownership is now implemented; status enums and events remain deferred.
 Status behaviour remains deferred. Current API validation is documented below.

 Synchronous SQLAlchemy sessions keep the first persistence task simple. A session
 groups queries; `database.session_scope()` commits successful work and rolls back
 on failure, then closes the session. `models.JobApplication` maps Python fields to
-columns; revision `0001` creates those columns; PostgreSQL's real table enforces
+columns; revisions `0001` and `0002` create the schema; PostgreSQL's real table enforces
 the constraints even when a caller bypasses Python. Engines disable SQL echo and
 hide parameter values. CLI and API error boundaries suppress raw database exceptions.

@@ -268,7 +396,7 @@ hide parameter values. CLI and API error boundaries suppress raw database except
 # Real Uvicorn child process and HTTP checks, with automatic shutdown:
 .\.venv\Scripts\python.exe -m scripts.check_server
 # Actual server startup (stop with Ctrl+C):
-.\.venv\Scripts\python.exe -m uvicorn main:app --host 127.0.0.1 --port 8000
+.\.venv\Scripts\python.exe -m uvicorn main:app --host 127.0.0.1 --port 8000 --no-proxy-headers --no-access-log
 ```

 Without `--run-db`, database checks explicitly skip. With it, missing/broken
@@ -277,10 +405,10 @@ constraints, commit/read through fresh connections, permit duplicate company/rol
 and provoke check-constraint failures to prove the whole transaction rolls back.
 Tests connect only as the dedicated test role. They delete only synthetic UUIDs
 created by that test (or the restart test's unique synthetic company marker); they
-never truncate tables, drop schemas, or touch development data. A process killed
-before cleanup may leave synthetic test records. API list tests include existing
-test records when determining expected ordering; they fail with a clear precondition
-if the test dataset exceeds the 10,000-offset window, rather than deleting records.
+never truncate tables or touch development data. Migration tests create random
+temporary schemas inside applysync_test and roll their entire transaction back.
+A killed process may leave synthetic test records. API ordering checks scope to
+the synthetic owner; unrelated records are excluded before pagination.

 The HTTP test uses HTTPX's in-memory ASGI transport, which does **not** start
 Uvicorn. To verify actual server behaviour in a second PowerShell terminal:
@@ -298,7 +426,9 @@ test. Secrets, `.venv`, and cache files must remain outside review packages.
 ## Manual application API

 Run the existing setup/migration commands only as needed on a fresh checkout.
-Task 2 adds no dependency or migration: the schema remains revision **0001**.
+Current schema revision is **0002**. All real application endpoints require a
+valid cookie session. POST additionally requires trusted Origin and
+`X-ApplySync-CSRF: 1`; the integrated frontend supplies these automatically.
 Start locally with the Uvicorn command above; interactive API docs are at `/docs`.
 `main.app` selects development configuration. Automated API checks explicitly use
 `create_app("test")` and verify the test database/role/revision before any writes.
@@ -308,8 +438,8 @@ There is no request parameter that switches databases.
 | --- | --- |
 | `POST /applications` | 201 with one stored application, after a successful commit. |
 | `GET /applications?limit=20&offset=0` | 200 with `{ "items": [...], "limit": 20, "offset": 0 }`. |
-| `GET /applications/{id}` | 200 with one application, or 404 `{ "detail": "Application not found" }` for an absent valid UUID. |
-| Invalid body, UUID or pagination | 422 with FastAPI's structured validation errors. |
+| `GET /applications/{id}` | 200 with one application, or 404 `{ "detail": "Application not found" }` for an absent or other-owner valid UUID. |
+| Invalid body, UUID or pagination | 422 with structured errors that omit submitted input and exception context. |
 | Database/configuration failure | 500 `{ "detail": "Internal server error" }`; no raw database diagnostics in response/logs. |

 Creation accepts exactly these three required fields:
@@ -375,15 +505,8 @@ process, starts a new one and retrieves the committed record. It does not restar
 PostgreSQL or write development records. Server subprocess output is suppressed;
 in-process failure tests assert that synthetic diagnostic markers never enter logs.

-Suggested learning checkpoint (not yet completed): with the local app running,
-send this invalid request from PowerShell and explain why it returns 422 instead
-of saving a record. Then locate the string constraint in `schemas.py`:
-
-```powershell
-$body = @{ company = '   '; role = 'Engineer'; applied_on = '2026-09-17' } | ConvertTo-Json
-Invoke-RestMethod -Method Post -Uri http://127.0.0.1:8000/applications -ContentType 'application/json' -Body $body
-```
-
-PowerShell reports the non-success status as an error; the API response is the
-expected validation failure. The earlier detailed transaction learning checkpoint
-remains pending too. These instructions do not claim either checkpoint is complete.
+Suggested learning checkpoint (not yet completed): after signing in through the
+frontend, submit a whitespace-only company and locate the string constraint in
+`schemas.py`. Direct unauthenticated PowerShell POSTs now fail request protection
+or authentication first. The detailed request-flow and earlier transaction
+exercises remain pending; this task does not claim they were completed.
diff --git a/applications.py b/applications.py
index 296f0aa..0b1fe00 100644
--- a/applications.py
+++ b/applications.py
@@ -10,15 +10,16 @@ from sqlalchemy.engine import Engine
 from database import get_engine, session_scope
 from models import JobApplication
 from schemas import ApplicationCreate, ApplicationPage, ApplicationRead
+from auth import CurrentUser

 router = APIRouter(prefix="/applications", tags=["applications"])
 DatabaseEngine = Annotated[Engine, Depends(get_engine)]


 @router.post("", response_model=ApplicationRead, status_code=201)
-def create_application(payload: ApplicationCreate, engine: DatabaseEngine):
+def create_application(payload: ApplicationCreate, engine: DatabaseEngine, user: CurrentUser):
     with session_scope(engine) as session:
-        application = JobApplication(**payload.model_dump())
+        application = JobApplication(**payload.model_dump(), owner_id=user.id)
         session.add(application)
         session.flush()
         # Materialize while attached; no lazy loads after commit/close.
@@ -30,11 +31,12 @@ def create_application(payload: ApplicationCreate, engine: DatabaseEngine):
 @router.get("", response_model=ApplicationPage)
 def list_applications(
     engine: DatabaseEngine,
+    user: CurrentUser,
     limit: Annotated[int, Query(ge=1, le=100)] = 20,
     offset: Annotated[int, Query(ge=0, le=10_000)] = 0,
 ):
     with session_scope(engine) as session:
-        rows = session.scalars(select(JobApplication).order_by(
+        rows = session.scalars(select(JobApplication).where(JobApplication.owner_id == user.id).order_by(
             JobApplication.created_at.asc(), JobApplication.id.asc()
         ).limit(limit).offset(offset))
         response = ApplicationPage(items=[ApplicationRead.model_validate(row) for row in rows],
@@ -43,9 +45,10 @@ def list_applications(


 @router.get("/{application_id}", response_model=ApplicationRead)
-def get_application(application_id: UUID, engine: DatabaseEngine):
+def get_application(application_id: UUID, engine: DatabaseEngine, user: CurrentUser):
     with session_scope(engine) as session:
-        application = session.get(JobApplication, application_id)
+        application = session.scalar(select(JobApplication).where(
+            JobApplication.id == application_id, JobApplication.owner_id == user.id))
         if application is None:
             raise HTTPException(status_code=404, detail="Application not found")
         response = ApplicationRead.model_validate(application)
diff --git a/frontend/e2e/integration.spec.ts b/frontend/e2e/integration.spec.ts
index 507be3a..c38d048 100644
--- a/frontend/e2e/integration.spec.ts
+++ b/frontend/e2e/integration.spec.ts
@@ -3,10 +3,10 @@ import { mkdirSync } from 'node:fs'

 const api = process.env.APPLYSYNC_E2E_API_ORIGIN!
 const marker = process.env.APPLYSYNC_E2E_RUN_ID!
-const screenshots = '../docs/screenshots/Build2_Task2'
+const screenshots = '../docs/screenshots/Build3'
 mkdirSync(screenshots, { recursive: true })

-test('real browser CORS, PostgreSQL creation, query refresh, pagination and reload', async ({ page }) => {
+test('real two-account sessions, ownership, creation, reload and logout', async ({ page, browser }) => {
   let listReads = 0
   let posts = 0
   const errors: string[] = []
@@ -16,6 +16,11 @@ test('real browser CORS, PostgreSQL creation, query refresh, pagination and relo
     if (request.url() === api + '/applications' && request.method() === 'POST') posts++
   })
   await page.goto('/applications')
+  await expect(page.getByRole('heading', { name: 'Welcome back' })).toBeVisible()
+  await page.screenshot({ path: `${screenshots}/login.png`, fullPage: true })
+  await page.getByLabel('Email', { exact: true }).fill(process.env.APPLYSYNC_E2E_EMAIL_A!)
+  await page.getByLabel('Password', { exact: true }).fill(process.env.APPLYSYNC_E2E_PASSWORD!)
+  await page.getByRole('button', { name: 'Sign in', exact: true }).click()
   await expect(page.getByRole('region', { name: 'Application list' }).getByRole('listitem')).toHaveCount(20)
   await expect(page.getByLabel('Sample stage')).toHaveCount(0)
   await expect(page.locator('.stage-label')).toHaveCount(0)
@@ -52,12 +57,40 @@ test('real browser CORS, PostgreSQL creation, query refresh, pagination and relo
   expect((await reread).status()).toBe(200)
   await expect(page.getByRole('dialog')).toContainText(marker + ' created')
   await expect(page.getByRole('dialog')).toContainText('1 Jan 2100')
+  // A separate browser session registers B against the actual API.
+  const contextB = await browser.newContext()
+  const pageB = await contextB.newPage()
+  await pageB.goto('http://127.0.0.1:4173/register')
+  await pageB.getByLabel('Email', { exact: true }).fill(process.env.APPLYSYNC_E2E_EMAIL_B!)
+  await pageB.getByLabel('Password', { exact: true }).fill(process.env.APPLYSYNC_E2E_PASSWORD!)
+  await pageB.getByRole('button', { name: 'Create account' }).click()
+  await expect(pageB.getByText('No stored applications yet')).toBeVisible()
+  await pageB.goto(`http://127.0.0.1:4173/applications/${record.id}`)
+  await expect(pageB.getByRole('dialog')).toContainText('Application not found.')
+  await pageB.reload()
+  await expect(pageB.getByRole('dialog')).toContainText('Application not found.')
+  await contextB.close()
   await page.screenshot({ path: `${screenshots}/stored-detail.png`, animations: 'disabled' })
   await page.setViewportSize({ width: 390, height: 844 })
   await page.screenshot({ path: `${screenshots}/stored-mobile-detail.png`, animations: 'disabled' })
   await page.keyboard.press('Escape')
   await page.screenshot({ path: `${screenshots}/stored-mobile-list.png`, fullPage: true })
   expect(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth)).toBe(true)
+  await page.getByRole('button', { name: 'Board', exact: true }).click()
+  await expect(page.getByRole('heading', { name: 'Stage not recorded' })).toBeVisible()
+  await page.screenshot({ path: `${screenshots}/stored-mobile-board.png`, fullPage: true })
+  await page.getByRole('button', { name: 'Log out', exact: true }).click()
+  await expect(page.getByRole('heading', { name: 'Welcome back' })).toBeVisible()
+  await page.reload()
+  await expect(page.getByRole('heading', { name: 'Welcome back' })).toBeVisible()
+  // Same browser changes to B: the old account's cache must not reappear.
+  await page.getByLabel('Email', { exact: true }).fill(process.env.APPLYSYNC_E2E_EMAIL_B!)
+  await page.getByLabel('Password', { exact: true }).fill(process.env.APPLYSYNC_E2E_PASSWORD!)
+  await page.getByRole('button', { name: 'Sign in', exact: true }).click()
+  await expect(page.getByText('No stored applications yet')).toBeVisible()
+  await expect(page.getByText(marker + ' created', { exact: true })).toHaveCount(0)
+  await page.goto(`/applications/${record.id}`)
+  await expect(page.getByRole('dialog')).toContainText('Application not found.')

   await page.goto('/applications/00000000-0000-4000-8000-000000000000')
   await expect(page.getByRole('dialog')).toContainText('Application not found.')
diff --git a/frontend/e2e/preview.spec.ts b/frontend/e2e/preview.spec.ts
index 64b326b..cd39036 100644
--- a/frontend/e2e/preview.spec.ts
+++ b/frontend/e2e/preview.spec.ts
@@ -1,7 +1,7 @@
 import { expect, test } from '@playwright/test'
 import { mkdirSync } from 'node:fs'

-const screenshots = '../docs/screenshots/Build2_Task2/preview'
+const screenshots = 'test-results/preview'
 mkdirSync(screenshots, { recursive: true })

 test('intermediate viewport widths keep controls inside the page', async ({ page }) => {
diff --git a/frontend/e2e/stored.spec.ts b/frontend/e2e/stored.spec.ts
index cae3eb2..29b986f 100644
--- a/frontend/e2e/stored.spec.ts
+++ b/frontend/e2e/stored.spec.ts
@@ -3,7 +3,7 @@ import { mkdirSync } from 'node:fs'

 const base = 'http://127.0.0.1:8000'
 const row = { id: '00000000-0000-4000-8000-000000000099', company: 'Synthetic Company', role: 'Engineer', applied_on: '2026-09-01', created_at: '2026-09-01T12:00:00Z' }
-const headers = { 'access-control-allow-origin': 'http://127.0.0.1:4173' }
+const headers = { 'access-control-allow-origin': 'http://127.0.0.1:4173', 'access-control-allow-credentials': 'true' }

 test('real Board/List share IDs, query state and paging with neutral stage fallback', async ({ page }) => {
   const records = Array.from({ length: 22 }, (_, i) => ({ ...row,
@@ -13,6 +13,7 @@ test('real Board/List share IDs, query state and paging with neutral stage fallb
   let reads = 0
   let writes = 0
   await page.route(`${base}/**`, async route => {
+    if (route.request().url().endsWith('/auth/me')) return route.fulfill({ headers, json: { id: 'synthetic-user', email: 'synthetic@example.com' } })
     const request = route.request()
     if (request.method() !== 'GET') { writes++; return route.abort() }
     const url = new URL(request.url())
@@ -45,7 +46,7 @@ test('real Board/List share IDs, query state and paging with neutral stage fallb
   await expect(page.getByRole('searchbox')).toHaveValue('Synthetic')
   expect(new URL(page.url()).searchParams.get('offset')).toBe('20')
   const secondPageIds = await ids('.application-card')
-  const shots = '../docs/screenshots/Build2_Task2/correction'
+  const shots = '../test-results/build3-layouts'
   mkdirSync(shots, { recursive: true })
   await page.screenshot({ path: `${shots}/stored-board.png`, fullPage: true })
   await page.getByRole('button', { name: 'List', exact: true }).click()
@@ -73,6 +74,7 @@ test('real Board/List share IDs, query state and paging with neutral stage fallb
 test('read network/server failures, retry, empty page and malformed pagination', async ({ page }) => {
   let state = 'network'
   await page.route(`${base}/**`, async route => {
+    if (route.request().url().endsWith('/auth/me')) return route.fulfill({ headers, json: { id: 'synthetic-user', email: 'synthetic@example.com' } })
     if (state === 'network') return route.abort('connectionrefused')
     await route.fulfill({ status: state === 'server' ? 500 : 200, headers, json: state === 'server' ? { detail: 'synthetic-private' } : { items: [], limit: 20, offset: 0 } })
   })
@@ -94,6 +96,7 @@ test('pending POST, backend validation, server/network uncertainty and success',
   let finish!: () => void
   let postCount = 0
   await page.route(`${base}/**`, async route => {
+    if (route.request().url().endsWith('/auth/me')) return route.fulfill({ headers, json: { id: 'synthetic-user', email: 'synthetic@example.com' } })
     if (route.request().method() === 'POST') {
       postCount++
       await new Promise<void>(resolve => { finish = resolve })
@@ -138,6 +141,7 @@ test('pending POST, backend validation, server/network uncertainty and success',
 test('direct detail read failure retries and full last page leads to honest empty next page', async ({ page }) => {
   let detailFails = true
   await page.route(`${base}/**`, async route => {
+    if (route.request().url().endsWith('/auth/me')) return route.fulfill({ headers, json: { id: 'synthetic-user', email: 'synthetic@example.com' } })
     const url = new URL(route.request().url())
     if (url.search) {
       const offset = Number(url.searchParams.get('offset'))
diff --git a/frontend/playwright.config.ts b/frontend/playwright.config.ts
index 2d9bbed..f52139e 100644
--- a/frontend/playwright.config.ts
+++ b/frontend/playwright.config.ts
@@ -2,6 +2,6 @@ import { defineConfig } from '@playwright/test'

 export default defineConfig({
   testDir: './e2e', testIgnore: '**/integration.spec.ts', fullyParallel: false, workers: 1, reporter: 'list',
-  use: { baseURL: 'http://127.0.0.1:4173', browserName: 'chromium', viewport: { width: 1600, height: 1000 }, trace: 'retain-on-failure' },
+  use: { baseURL: 'http://127.0.0.1:4173', browserName: 'chromium', viewport: { width: 1600, height: 1000 }, trace: 'off' },
   webServer: { command: 'npm run preview -- --port 4173 --strictPort', url: 'http://127.0.0.1:4173', reuseExistingServer: false },
 })
diff --git a/frontend/playwright.integration.config.ts b/frontend/playwright.integration.config.ts
index 73c1bbc..283cc85 100644
--- a/frontend/playwright.integration.config.ts
+++ b/frontend/playwright.integration.config.ts
@@ -5,7 +5,7 @@ if (!process.env.APPLYSYNC_E2E_RUN_ID || !process.env.APPLYSYNC_E2E_API_ORIGIN)
 }
 export default defineConfig({
   testDir: './e2e', testMatch: '**/integration.spec.ts', workers: 1, reporter: 'list',
-  use: { baseURL: 'http://127.0.0.1:4173', browserName: 'chromium', viewport: { width: 1440, height: 1000 }, trace: 'retain-on-failure' },
+  use: { baseURL: 'http://127.0.0.1:4173', browserName: 'chromium', viewport: { width: 1440, height: 1000 }, trace: 'off', screenshot: 'off', video: 'off' },
   webServer: { command: 'npm run dev -- --port 4173 --strictPort', url: 'http://127.0.0.1:4173', reuseExistingServer: false,
     env: { VITE_API_BASE_URL: process.env.APPLYSYNC_E2E_API_ORIGIN } },
 })
diff --git a/frontend/src/App.tsx b/frontend/src/App.tsx
index ad1a4d4..fe35429 100644
--- a/frontend/src/App.tsx
+++ b/frontend/src/App.tsx
@@ -6,12 +6,17 @@ import { PreviewApplications } from './PreviewApplications'
 import { StoredApplications } from './StoredApplications'
 import { makeQueryClient } from './query'
 import type { PreviewApplication } from './data'
+import { AuthForm, AuthProvider, ProtectedApplications } from './Auth'

 export function App({ initialRecords }: { initialRecords?: PreviewApplication[] }) {
   const [client] = useState(makeQueryClient)
-  return <QueryClientProvider client={client}><Shell><Routes>
-    <Route path="/applications/:id?" element={<StoredApplications />} />
-    <Route path="/preview/applications/:id?" element={<PreviewApplications initialRecords={initialRecords} />} />
-    <Route path="*" element={<Navigate to="/applications" replace />} />
-  </Routes></Shell></QueryClientProvider>
+  return <Routes>
+    <Route path="/preview/applications/:id?" element={<QueryClientProvider client={client}><Shell><PreviewApplications initialRecords={initialRecords} /></Shell></QueryClientProvider>} />
+    <Route path="*" element={<AuthProvider><Shell><Routes>
+      <Route path="/login" element={<AuthForm />} />
+      <Route path="/register" element={<AuthForm register />} />
+      <Route path="/applications/:id?" element={<ProtectedApplications><StoredApplications /></ProtectedApplications>} />
+      <Route path="*" element={<Navigate to="/applications" replace />} />
+    </Routes></Shell></AuthProvider>} />
+  </Routes>
 }
diff --git a/frontend/src/StoredApplications.test.tsx b/frontend/src/StoredApplications.test.tsx
index 4d2b2ce..d6fefd3 100644
--- a/frontend/src/StoredApplications.test.tsx
+++ b/frontend/src/StoredApplications.test.tsx
@@ -6,12 +6,19 @@ import { App } from './App'

 const row = { id: '00000000-0000-4000-8000-000000000099', company: 'Stored Company', role: 'Engineer', applied_on: '2100-01-01', created_at: '2026-01-01T12:00:00Z' }
 const json = (body: unknown, status = 200) => new Response(JSON.stringify(body), { status })
-function mount(path = '/applications') { render(<MemoryRouter initialEntries={[path]}><App /></MemoryRouter>); return userEvent.setup() }
+async function mount(path = '/applications') {
+  const original = globalThis.fetch
+  vi.stubGlobal('fetch', (url: string, options?: RequestInit) => String(url).endsWith('/auth/me')
+    ? Promise.resolve(json({ id: 'synthetic-user', email: 'synthetic@example.com' })) : original(url, options))
+  render(<MemoryRouter initialEntries={[path]}><App /></MemoryRouter>)
+  await screen.findByRole('searchbox')
+  return userEvent.setup()
+}
 afterEach(() => vi.unstubAllGlobals())

 it('lists real records without stage controls and clearly scopes search/counts', async () => {
   vi.stubGlobal('fetch', vi.fn().mockResolvedValue(json({ items: [row], limit: 20, offset: 0 })))
-  const user = mount()
+  const user = await mount()
   expect(await screen.findByRole('link', { name: 'Engineer at Stored Company' })).toBeInTheDocument()
   expect(screen.queryByLabelText('Sample stage')).not.toBeInTheDocument()
   expect(document.querySelector('.stage-label')).not.toBeInTheDocument()
@@ -26,7 +33,7 @@ it.each(['board', 'list'])('has loading, empty, failure and retry states in %s w
   const fetchMock = vi.fn().mockImplementationOnce(() => new Promise<Response>(r => { resolve = r }))
     .mockResolvedValueOnce(json({ items: [], limit: 20, offset: 0 }))
   vi.stubGlobal('fetch', fetchMock)
-  const user = mount(`/applications?view=${view}`)
+  const user = await mount(`/applications?view=${view}`)
   expect(screen.getByRole('status')).toHaveTextContent('Loading applications')
   await user.click(screen.getByRole('button', { name: view === 'board' ? 'List' : 'Board' }))
   expect(screen.getByRole('status')).toHaveTextContent('Loading applications')
@@ -46,7 +53,7 @@ it('keeps input on backend validation and blocks duplicate pending submissions',
   let finish!: (response: Response) => void
   const posts = vi.fn(() => new Promise<Response>(resolve => { finish = resolve }))
   vi.stubGlobal('fetch', vi.fn((_url, options) => options?.method === 'POST' ? posts() : Promise.resolve(json({ items: [], limit: 20, offset: 0 }))))
-  const user = mount('/applications/new')
+  const user = await mount('/applications/new')
   const form = screen.getByRole('dialog')
   await user.type(within(form).getByLabelText('Company', { exact: false }), 'Retain Me')
   await user.type(within(form).getByLabelText('Role', { exact: false }), 'Engineer')
@@ -68,22 +75,22 @@ it('opens confirmed detail and refreshes the list after creation', async () => {
     if (String(url).includes('?')) { lists++; return Promise.resolve(json({ items: created ? [row] : [], limit: 20, offset: 0 })) }
     return Promise.resolve(json(row))
   }))
-  const user = mount('/applications/new')
+  const user = await mount('/applications/new')
   await user.type(screen.getByLabelText('Company', { exact: false }), 'Stored Company')
   await user.type(screen.getByLabelText('Role', { exact: false }), 'Engineer')
   await user.type(screen.getByLabelText('Applied date', { exact: false }), '2100-01-01')
   await user.click(screen.getByRole('button', { name: 'Save application' }))
   expect(await screen.findByText('Application saved to the database.')).toBeInTheDocument()
-  await user.click(screen.getByRole('button', { name: 'Back to applications' }))
+  await user.click(await screen.findByRole('button', { name: 'Back to applications' }))
   expect(await screen.findByRole('link', { name: 'Engineer at Stored Company' })).toBeInTheDocument()
   expect(lists).toBeGreaterThanOrEqual(2)
 })
 it('loads direct details, distinguishes missing/malformed IDs, and never fetches preview data', async () => {
   const fetchMock = vi.fn().mockResolvedValue(json({ items: [], limit: 20, offset: 0 }))
   vi.stubGlobal('fetch', fetchMock)
-  const user = mount('/applications/bad-id')
+  const user = await mount('/applications/bad-id')
   expect(screen.getByRole('alert')).toHaveTextContent('Invalid application ID')
-  await user.click(screen.getByRole('button', { name: 'Back to applications' }))
+  await user.click(await screen.findByRole('button', { name: 'Back to applications' }))
   await waitFor(() => expect(fetchMock).toHaveBeenCalledTimes(1))
   await user.click(screen.getByRole('link', { name: 'Explore sample Board/List preview' }))
   expect(screen.getByText('Cedar & Finch')).toBeInTheDocument()
diff --git a/frontend/src/StoredApplications.tsx b/frontend/src/StoredApplications.tsx
index 121ca58..56d45cf 100644
--- a/frontend/src/StoredApplications.tsx
+++ b/frontend/src/StoredApplications.tsx
@@ -1,4 +1,4 @@
-import { useState } from 'react'
+import { useEffect, useRef, useState } from 'react'
 import { Link, useLocation, useNavigate, useParams, useSearchParams } from 'react-router'
 import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
 import { CalendarDays, Columns3, List, Plus, Search } from 'lucide-react'
@@ -16,6 +16,8 @@ export function StoredApplications() {
   const location = useLocation()
   const client = useQueryClient()
   const [saved, setSaved] = useState(false)
+  const writes = useRef<AbortController | null>(null)
+  useEffect(() => () => writes.current?.abort(), [])
   const rawOffset = params.get('offset') ?? '0'
   const offset = Number(rawOffset)
   const validOffset = /^\d+$/.test(rawOffset) && Number.isSafeInteger(offset) && offset <= 10_000
@@ -27,7 +29,10 @@ export function StoredApplications() {
     queryFn: ({ signal }) => listApplications(pageSize, offset, signal), enabled: validOffset })
   const detail = useQuery({ queryKey: ['applications', 'detail', id],
     queryFn: ({ signal }) => getApplication(id!, signal), enabled: validId })
-  const mutation = useMutation({ mutationFn: createApplication, retry: false })
+  const mutation = useMutation({ mutationFn: (values: CreateValues) => {
+    writes.current = new AbortController()
+    return createApplication(values, writes.current.signal)
+  }, retry: false })
   const close = () => { if (!mutation.isPending) navigate(`/applications${location.search}`, { replace: true }) }
   const rows = list.data?.items ?? []
   const query = search.trim().toLocaleLowerCase()
@@ -37,9 +42,11 @@ export function StoredApplications() {
   }
   async function add(values: CreateValues) {
     const record = await mutation.mutateAsync(values)
+    if (writes.current?.signal.aborted) return
     client.setQueryData(['applications', 'detail', record.id], record)
     // Creation is already committed. A failed refresh is a read error, not a failed POST.
     await client.invalidateQueries({ queryKey: ['applications', 'list'] })
+    if (writes.current?.signal.aborted) return
     setSaved(true)
     navigate(`/applications/${record.id}${location.search}`, { replace: true })
   }
diff --git a/frontend/src/api.ts b/frontend/src/api.ts
index cbaeea2..21e611b 100644
--- a/frontend/src/api.ts
+++ b/frontend/src/api.ts
@@ -3,7 +3,7 @@ import type { Application, CreateValues } from './data'
 export interface ApplicationPage { items: Application[]; limit: number; offset: number }
 export type FieldErrors = Partial<Record<keyof CreateValues, string>>
 export class ApiError extends Error {
-  constructor(public kind: 'configuration' | 'network' | 'server' | 'validation' | 'missing' | 'response', public fields: FieldErrors = {}) {
+  constructor(public kind: 'configuration' | 'network' | 'server' | 'validation' | 'missing' | 'response' | 'unauthorized' | 'forbidden' | 'conflict' | 'limited', public fields: FieldErrors = {}) {
     super(kind)
   }
 }
@@ -22,6 +22,10 @@ export function errorMessage(error: unknown, writing = false) {
   if (kind === 'configuration') return 'Set VITE_API_BASE_URL to the local backend origin, then restart Vite.'
   if (kind === 'validation') return 'Check the highlighted fields and try again.'
   if (kind === 'missing') return 'Application not found.'
+  if (kind === 'unauthorized') return 'Your session ended. Sign in and explicitly submit again.'
+  if (kind === 'forbidden') return 'Request protection failed. Open the frontend and API using the same hostname.'
+  if (kind === 'conflict') return 'Registration could not be completed for this email. Try signing in.'
+  if (kind === 'limited') return 'Too many attempts. Wait 15 minutes before trying again.'
   if (writing) return 'Creation could not be confirmed. It may have been saved. Check the application list before submitting again.'
   if (kind === 'server') return 'The server could not load applications. Try again.'
   if (kind === 'response') return 'The server returned an unexpected response. Try again.'
@@ -41,18 +45,25 @@ function validationFields(body: unknown): FieldErrors {
   return fields
 }

-async function request(path: string, body?: CreateValues, signal?: AbortSignal): Promise<unknown> {
+export async function request(path: string, body?: unknown, signal?: AbortSignal): Promise<unknown> {
   const base = apiBase()
   const timeout = AbortSignal.timeout(15_000)
   let response: Response
   try {
     response = await fetch(`${base}${path}`, {
-      method: body ? 'POST' : 'GET', credentials: 'omit',
-      headers: body ? { 'Content-Type': 'application/json' } : undefined,
+      method: body ? 'POST' : 'GET', credentials: 'include',
+      headers: body ? { 'Content-Type': 'application/json', 'X-ApplySync-CSRF': '1' } : undefined,
       body: body ? JSON.stringify(body) : undefined,
       signal: signal ? AbortSignal.any([signal, timeout]) : timeout,
     })
   } catch { throw new ApiError('network') }
+  if (response.status === 401) {
+    if (path.startsWith('/applications') && !signal?.aborted) window.dispatchEvent(new Event('applysync:expired'))
+    throw new ApiError('unauthorized')
+  }
+  if (response.status === 403) throw new ApiError('forbidden')
+  if (response.status === 409) throw new ApiError('conflict')
+  if (response.status === 429) throw new ApiError('limited')
   if (response.status === 404) throw new ApiError('missing')
   if (response.status === 422) {
     let details: unknown
@@ -60,6 +71,7 @@ async function request(path: string, body?: CreateValues, signal?: AbortSignal):
     throw new ApiError('validation', validationFields(details))
   }
   if (!response.ok) throw new ApiError('server')
+  if (response.status === 204) return undefined
   try { return await response.json() } catch { throw new ApiError('response') }
 }

@@ -76,4 +88,4 @@ export async function listApplications(limit: number, offset: number, signal?: A
   return { items: page.items.map(application), limit, offset }
 }
 export async function getApplication(id: string, signal?: AbortSignal) { return application(await request(`/applications/${encodeURIComponent(id)}`, undefined, signal)) }
-export async function createApplication(values: CreateValues) { return application(await request('/applications', values)) }
+export async function createApplication(values: CreateValues, signal?: AbortSignal) { return application(await request('/applications', values, signal)) }
diff --git a/frontend/src/components/Shell.tsx b/frontend/src/components/Shell.tsx
index 277a99c..f761815 100644
--- a/frontend/src/components/Shell.tsx
+++ b/frontend/src/components/Shell.tsx
@@ -2,6 +2,7 @@ import { useState, type ReactNode } from 'react'
 import { Link, useLocation } from 'react-router'
 import { ArrowUpRight, Layers3, Menu, ShieldCheck } from 'lucide-react'
 import { Modal, PreviewNotice } from './ui'
+import { useAuth } from '../Auth'

 function Sidebar({ onNavigate }: { onNavigate?: () => void }) {
   const preview = useLocation().pathname.startsWith('/preview/')
@@ -12,10 +13,11 @@ function Sidebar({ onNavigate }: { onNavigate?: () => void }) {
       <nav aria-label="Main navigation"><Link className="nav-link" aria-current="page" to={preview ? "/preview/applications" : "/applications"} onClick={onNavigate}><Layers3 size={19} /> Applications <ArrowUpRight size={16} className="ml-auto" /></Link></nav>
       <div className="sidebar-note"><span className="tiny-tag">{preview ? 'BUILD 2 · PREVIEW' : 'BUILD 2 · LOCAL DEVELOPMENT'}</span><h2>A little more clarity.</h2><p>One place to see your next opportunity taking shape.</p></div>
     </div>
-    <div className="sidebar-footer"><ShieldCheck size={20} /><div><strong>Private by design</strong><p>{preview ? "Fictional data. All local." : "Local, unauthenticated use."}</p></div></div>
+    <div className="sidebar-footer"><ShieldCheck size={20} /><div><strong>Private by design</strong><p>{preview ? "Fictional data. All local." : "Your account. Your applications."}</p></div></div>
   </div>
 }
 export function Shell({ children }: { children: ReactNode }) {
+  const auth = useAuth()
   const preview = useLocation().pathname.startsWith('/preview/')
   const [navigationOpen, setNavigationOpen] = useState(false)
   return <div className="app-shell">
@@ -26,6 +28,7 @@ export function Shell({ children }: { children: ReactNode }) {
         <button className="icon-button mobile-menu" aria-label="Open navigation" onClick={() => setNavigationOpen(true)}><Menu size={21} /></button>
         <div className="breadcrumb"><span>Workspace</span><span aria-hidden="true">/</span><strong>Applications</strong></div>
         <PreviewNotice>{preview ? 'Design preview · Sample data' : 'Local development · Stored data'}</PreviewNotice>
+        {auth?.user && !auth.checking && !auth.failure && <div className="signed-in"><span>{auth.user.email}</span><button className="button" onClick={() => void auth.logout()}>Log out</button></div>}
       </header>
       <main id="main-content" tabIndex={-1}>{children}</main>
     </div>
diff --git a/frontend/src/styles.css b/frontend/src/styles.css
index 7e4e3f7..16fe95f 100644
--- a/frontend/src/styles.css
+++ b/frontend/src/styles.css
@@ -220,3 +220,11 @@ input::placeholder { color: #667085; }
   .stored-list .list-row { grid-template-columns: minmax(0, 1fr); }
   .pagination span { order: 3; width: 100%; text-align: center; }
 }
+/* Build 3 identity uses the existing surfaces, fields and purple buttons. */
+.auth-card { max-width: 480px; margin: 40px auto; padding: 32px; }
+.auth-card h1 { font-size: 28px; margin: 12px 0; }
+.auth-card > p { margin-bottom: 20px; }
+.auth-card a { color: var(--purple, #7254c7); }
+.signed-in { display: flex; gap: 12px; align-items: center; min-width: 0; }
+.signed-in span { max-width: 220px; overflow: hidden; text-overflow: ellipsis; font-size: 12px; }
+@media (max-width: 700px) { .topbar { flex-wrap: wrap; height: auto; min-height: 72px; gap: 10px; padding-block: 12px; } .signed-in { margin-left: auto; } .signed-in span { max-width: 160px; } .auth-card { margin: 20px auto; padding: 22px; } }
diff --git a/main.py b/main.py
index 2fb3f3f..e558820 100644
--- a/main.py
+++ b/main.py
@@ -8,6 +8,9 @@ from sqlalchemy.exc import SQLAlchemyError

 from applications import router
 from config import ConfigurationError
+from auth import router as auth_router, AttemptLimiter
+from auth_config import allowed_origins
+from fastapi.exceptions import RequestValidationError


 @asynccontextmanager
@@ -33,21 +36,43 @@ def create_app(database_target: str = "dev") -> FastAPI:
     if database_target not in {"dev", "test"}:
         raise ConfigurationError("Database target must be dev or test.")
     application = FastAPI(lifespan=lifespan)
+    origins = allowed_origins()
+
+    @application.middleware("http")
+    async def request_security(request: Request, call_next):
+        # Independent server checks: simple forms, absent/foreign origins, and
+        # missing custom headers are rejected even without a CORS preflight.
+        if request.method not in {"GET", "HEAD", "OPTIONS"}:
+            if (request.headers.get("origin") not in origins
+                    or request.headers.get("x-applysync-csrf") != "1"):
+                return JSONResponse(status_code=403, content={"detail": "Request protection failed"})
+        response = await call_next(request)
+        if request.url.path.startswith(("/auth", "/applications")):
+            response.headers["Cache-Control"] = "no-store"
+        return response
+
+    @application.exception_handler(RequestValidationError)
+    async def safe_validation(request, error):
+        # FastAPI's default input echo can include submitted passwords.
+        return JSONResponse(status_code=422, content={"detail": [
+            {"loc": list(item["loc"]), "type": item["type"], "msg": "Invalid input"}
+            for item in error.errors()]})
     application.add_middleware(
         CORSMiddleware,
-        allow_origins=[f"http://{host}:{port}" for host in ("localhost", "127.0.0.1")
-                       for port in (5173, 4173)],
-        allow_credentials=False,
+        allow_origins=list(origins),
+        allow_credentials=True,
         allow_methods=["GET", "POST"],
-        allow_headers=["Content-Type"],
+        allow_headers=["Content-Type", "X-ApplySync-CSRF"],
     )
     application.state.database_target = database_target
     application.state.engine = None
     application.state.engine_lock = Lock()
+    application.state.attempt_limiter = AttemptLimiter()
     application.add_exception_handler(SQLAlchemyError, database_error)
     application.add_exception_handler(ConfigurationError, database_error)
     application.add_api_route("/health", health, methods=["GET"])
     application.include_router(router)
+    application.include_router(auth_router)
     return application


diff --git a/migrations/env.py b/migrations/env.py
index c8b63b2..b4e3c53 100644
--- a/migrations/env.py
+++ b/migrations/env.py
@@ -12,6 +12,12 @@ target_metadata = Base.metadata


 def run_migrations():
+    supplied = context.config.attributes.get("connection")
+    if supplied is not None:
+        context.configure(connection=supplied, target_metadata=target_metadata, compare_type=True)
+        with context.begin_transaction():
+            context.run_migrations()
+        return
     target = context.get_x_argument(as_dictionary=True).get("target", "dev")
     try:
         settings = load_settings(target)
diff --git a/models.py b/models.py
index b524759..ad3c82d 100644
--- a/models.py
+++ b/models.py
@@ -3,7 +3,7 @@
 from datetime import date, datetime
 from uuid import UUID, uuid4

-from sqlalchemy import CheckConstraint, Date, DateTime, String, Uuid, func
+from sqlalchemy import CheckConstraint, Date, DateTime, ForeignKey, Index, String, Uuid, func
 from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


@@ -11,14 +11,33 @@ class Base(DeclarativeBase):
     pass


+class User(Base):
+    __tablename__ = "users"
+    __table_args__ = (CheckConstraint("email = lower(email)", name="ck_users_email_lower"),)
+    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True, default=uuid4)
+    email: Mapped[str] = mapped_column(String(254), nullable=False, unique=True)
+    password_hash: Mapped[str] = mapped_column(String(512), nullable=False)
+    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
+
+
+class AuthSession(Base):
+    __tablename__ = "auth_sessions"
+    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True, default=uuid4)
+    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
+    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
+
+
 class JobApplication(Base):
     __tablename__ = "job_applications"
     __table_args__ = (
         CheckConstraint("company ~ '[^[:space:]]'", name="ck_job_applications_company_nonblank"),
         CheckConstraint("role ~ '[^[:space:]]'", name="ck_job_applications_role_nonblank"),
+        Index("ix_job_applications_owner_order", "owner_id", "created_at", "id"),
     )

     id: Mapped[UUID] = mapped_column(Uuid, primary_key=True, default=uuid4)
+    # NULL is a quarantined legacy record, never returned by ordinary APIs.
+    owner_id: Mapped[UUID | None] = mapped_column(ForeignKey("users.id"), nullable=True)
     company: Mapped[str] = mapped_column(String(200), nullable=False)
     role: Mapped[str] = mapped_column(String(200), nullable=False)
     applied_on: Mapped[date] = mapped_column(Date, nullable=False)
diff --git a/requirements.txt b/requirements.txt
index c5544dd..f1028d9 100644
--- a/requirements.txt
+++ b/requirements.txt
@@ -30,3 +30,12 @@ typing-inspection==0.4.4
 typing_extensions==4.16.0
 tzdata==2026.4
 uvicorn==0.53.0
+
+# Build 3 authentication (CPython 3.14.2 Windows installation verified).
+argon2-cffi==25.1.0
+argon2-cffi-bindings==26.1.0
+cffi==2.1.1
+pycparser==3.0
+PyJWT==2.15.0
+email-validator==2.3.0
+dnspython==2.8.0
diff --git a/scripts/run_frontend_integration.py b/scripts/run_frontend_integration.py
index ef7917a..e685b54 100644
--- a/scripts/run_frontend_integration.py
+++ b/scripts/run_frontend_integration.py
@@ -2,6 +2,7 @@

 from datetime import datetime, timezone
 import os
+import secrets
 from pathlib import Path
 import socket
 import subprocess
@@ -14,7 +15,8 @@ from sqlalchemy import delete, func, select, text

 from config import load_settings
 from database import build_engine, session_scope
-from models import JobApplication
+from models import JobApplication, User, AuthSession
+from auth import hasher

 ROOT = Path(__file__).resolve().parents[1]
 PHASE = "configuration"
@@ -24,7 +26,7 @@ def verify_target(engine):
     with engine.connect() as connection:
         if (connection.scalar(text("SELECT current_database()")) != "applysync_test"
                 or connection.scalar(text("SELECT current_user")) != "applysync_test"
-                or connection.scalar(text("SELECT version_num FROM alembic_version")) != "0001"):
+                or connection.scalar(text("SELECT version_num FROM alembic_version")) != "0002"):
             raise RuntimeError("Refusing an unverified integration database target.")


@@ -43,6 +45,10 @@ def run():
     engine = build_engine(load_settings("test"))
     process = None
     marker = f"Synthetic Browser {uuid4()}"
+    account_prefix = uuid4().hex
+    email_a, email_b = f"{account_prefix}-a@example.com", f"{account_prefix}-b@example.com"
+    password = secrets.token_urlsafe(24)
+    auth_env = {**os.environ, "APPLYSYNC_AUTH_SECRET": secrets.token_hex(32), "APPLYSYNC_AUTH_MODE": "local"}
     verified = False
     try:
         verify_target(engine)
@@ -50,8 +56,12 @@ def run():
         PHASE = "test fixture creation"
         # Enough owned fixtures to exercise real pagination, even in a nonempty DB.
         with session_scope(engine) as session:
+            user = User(email=email_a, password_hash=hasher.hash(password))
+            session.add(user)
+            session.flush()
+            owner_id = user.id
             for i in range(21):
-                session.add(JobApplication(company=f"{marker} seed {i:02}", role="Engineer",
+                session.add(JobApplication(company=f"{marker} seed {i:02}", role="Engineer", owner_id=owner_id,
                     applied_on=datetime(2026, 9, 1).date(),
                     created_at=datetime(1900, 1, 1, tzinfo=timezone.utc)))
         with socket.socket() as probe:
@@ -62,7 +72,7 @@ def run():
         print("Verified test target; starting isolated API.", flush=True)
         process = subprocess.Popen([sys.executable, "-c",
             f"from scripts.run_frontend_integration import serve; serve({port})"],
-            cwd=ROOT, stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL,
+            cwd=ROOT, env=auth_env, stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL,
             stderr=subprocess.DEVNULL, creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))
         with httpx.Client(trust_env=False, timeout=2) as client:
             deadline = time.monotonic() + 20
@@ -79,6 +89,8 @@ def run():
                     raise RuntimeError("Isolated test API startup timed out.")
                 time.sleep(.1)
         env = {**os.environ, "APPLYSYNC_E2E_RUN_ID": marker,
+               "APPLYSYNC_E2E_EMAIL_A": email_a, "APPLYSYNC_E2E_EMAIL_B": email_b,
+               "APPLYSYNC_E2E_PASSWORD": password,
                "APPLYSYNC_E2E_API_ORIGIN": origin, "VITE_API_BASE_URL": origin}
         command = ["cmd.exe", "/d", "/c", "npm.cmd", "run", "test:integration"] if os.name == "nt" else ["npm", "run", "test:integration"]
         PHASE = "browser checks"
@@ -92,7 +104,7 @@ def run():
         PHASE = "committed record verification"
         with session_scope(engine) as session:
             row = session.scalar(select(JobApplication).where(JobApplication.company == marker + " created"))
-            if row is None or row.role != "Browser Engineer" or row.applied_on.isoformat() != "2100-01-01":
+            if row is None or row.owner_id != owner_id or row.role != "Browser Engineer" or row.applied_on.isoformat() != "2100-01-01":
                 raise RuntimeError("Committed browser record was not verified in PostgreSQL.")
         print("PASS: committed browser-created values independently verified in test PostgreSQL.")
     finally:
@@ -109,6 +121,10 @@ def run():
                 verify_target(engine)  # Recheck before any cleanup.
                 with session_scope(engine) as session:
                     session.execute(delete(JobApplication).where(JobApplication.company.startswith(marker)))
+                    ids = select(User.id).where(User.email.in_([email_a, email_b]))
+                    session.execute(delete(JobApplication).where(JobApplication.owner_id.in_(ids)))
+                    session.execute(delete(AuthSession).where(AuthSession.user_id.in_(ids)))
+                    session.execute(delete(User).where(User.email.in_([email_a, email_b])))
                 with session_scope(engine) as session:
                     remaining = session.scalar(select(func.count()).select_from(JobApplication).where(JobApplication.company.startswith(marker)))
                     if remaining != 0:
diff --git a/tests/conftest.py b/tests/conftest.py
index 4fff6a0..0551751 100644
--- a/tests/conftest.py
+++ b/tests/conftest.py
@@ -20,7 +20,7 @@ def test_engine(request):
         with engine.connect() as connection:
             assert connection.scalar(text("SELECT current_database()")) == "applysync_test"
             assert connection.scalar(text("SELECT current_user")) == "applysync_test"
-            assert connection.scalar(text("SELECT version_num FROM alembic_version")) == "0001"
+            assert connection.scalar(text("SELECT version_num FROM alembic_version")) == "0002"
         yield engine
     except (ConfigurationError, SQLAlchemyError):
         pytest.fail("Dedicated test database is not configured, reachable, or migrated.", pytrace=False)
diff --git a/tests/test_api_restart.py b/tests/test_api_restart.py
index ee6a7a4..55668df 100644
--- a/tests/test_api_restart.py
+++ b/tests/test_api_restart.py
@@ -3,6 +3,8 @@
 from contextlib import contextmanager
 from pathlib import Path
 import socket
+import os
+import secrets
 import subprocess
 import sys
 import time
@@ -13,7 +15,8 @@ import pytest
 from sqlalchemy import delete

 from database import session_scope
-from models import JobApplication
+from models import JobApplication, User, AuthSession
+from sqlalchemy import select

 pytestmark = pytest.mark.database

@@ -61,11 +64,18 @@ def test_server():
 test_server.__test__ = False


-def test_committed_application_survives_uvicorn_restart(test_engine):
+def test_committed_application_survives_uvicorn_restart(test_engine, monkeypatch):
+    monkeypatch.setenv("APPLYSYNC_AUTH_SECRET", secrets.token_hex(32))
+    monkeypatch.setenv("APPLYSYNC_AUTH_MODE", "local")
+    email = f"{uuid4()}@example.com"
+    password = secrets.token_urlsafe(24)
     # test_engine verifies current database, current role and revision before spawning.
     company = f"Synthetic restart {uuid4()}"
     try:
         with test_server() as (client, first_process):
+            client.headers.update({"Origin": "http://127.0.0.1:5173", "X-ApplySync-CSRF": "1"})
+            assert client.post("/auth/register", json={"email": email, "password": password}).status_code == 201
+            cookies = client.cookies
             response = client.post("/applications", json={
                 "company": company, "role": "Engineer", "applied_on": "2026-09-17"})
             assert response.status_code == 201
@@ -73,6 +83,8 @@ def test_committed_application_survives_uvicorn_restart(test_engine):
         assert first_process.poll() is not None
         with test_server() as (client, second_process):
             assert first_process.pid != second_process.pid
+            client.cookies.update(cookies)
+            assert client.get("/auth/me").status_code == 200
             response = client.get(f'/applications/{stored["id"]}')
             assert response.status_code == 200
             assert response.json() == stored
@@ -80,3 +92,6 @@ def test_committed_application_survives_uvicorn_restart(test_engine):
         # A unique synthetic company also covers a response lost after commit.
         with session_scope(test_engine) as session:
             session.execute(delete(JobApplication).where(JobApplication.company == company))
+            ids = select(User.id).where(User.email == email)
+            session.execute(delete(AuthSession).where(AuthSession.user_id.in_(ids)))
+            session.execute(delete(User).where(User.email == email))
diff --git a/tests/test_applications.py b/tests/test_applications.py
index 078c8ff..2f4a031 100644
--- a/tests/test_applications.py
+++ b/tests/test_applications.py
@@ -11,6 +11,8 @@ from sqlalchemy.orm import Session
 from database import session_scope
 from main import create_app
 from models import JobApplication
+from models import User
+from auth import current_user, Identity

 pytestmark = pytest.mark.database

@@ -19,7 +21,7 @@ def request(app, method, path, **kwargs):
     async def send():
         async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app),
                                      base_url="http://test") as client:
-            return await client.request(method, path, **kwargs)
+            return await client.request(method, path, headers={"Origin": "http://127.0.0.1:5173", "X-ApplySync-CSRF": "1"}, **kwargs)
     return asyncio.run(send())


@@ -27,6 +29,13 @@ def request(app, method, path, **kwargs):
 def api(test_engine):
     app = create_app("test")
     app.state.engine = test_engine  # Fixture already verified database, role and revision.
+    with session_scope(test_engine) as session:
+        user = User(email=f"{uuid4()}@example.com", password_hash="not-a-login-account")
+        session.add(user)
+        session.flush()
+        identity = Identity.model_validate(user)
+    app.dependency_overrides[current_user] = lambda: identity
+    app.state.test_owner_id = identity.id
     owned_ids = set()

     def remember_inserts(session, context):
@@ -40,6 +49,7 @@ def api(test_engine):
         event.remove(Session, "after_flush", remember_inserts)
         with session_scope(test_engine) as session:
             session.execute(delete(JobApplication).where(JobApplication.id.in_(owned_ids)))
+            session.execute(delete(User).where(User.id == identity.id))


 @pytest.fixture
@@ -68,6 +78,7 @@ def test_create_retrieve_list_and_duplicate(api, payload):
             assert stored.company == record["company"] and stored.role == record["role"]
             assert stored.applied_on.isoformat() == record["applied_on"]
             position = session.scalar(select(func.count()).select_from(JobApplication).where(
+                JobApplication.owner_id == app.state.test_owner_id,
                 (JobApplication.created_at < stored.created_at) |
                 ((JobApplication.created_at == stored.created_at) & (JobApplication.id < stored.id))))
         assert position <= 10_000, "Test database exceeds the documented pagination window"
@@ -88,7 +99,7 @@ def test_ordering_pagination_and_empty_page(api, payload):
     with session_scope(engine) as session:
         session.execute(update(JobApplication).where(JobApplication.id.in_(ids)).values(
             created_at=datetime(1900, 1, 1, tzinfo=timezone.utc)))
-        expected = session.scalars(select(JobApplication.id).order_by(
+        expected = session.scalars(select(JobApplication.id).where(JobApplication.owner_id == app.state.test_owner_id).order_by(
             JobApplication.created_at, JobApplication.id)).all()
     assert len(expected) <= 10_000, "Test database exceeds the documented pagination window"
     for offset in range(0, min(len(expected), 6), 2):
diff --git a/tests/test_cors.py b/tests/test_cors.py
index da2c989..616d427 100644
--- a/tests/test_cors.py
+++ b/tests/test_cors.py
@@ -23,10 +23,11 @@ def test_local_origin_preflight_and_errors(host, port, monkeypatch):
                                      base_url="http://test") as client:
             response = await client.options("/applications", headers={
                 "Origin": origin, "Access-Control-Request-Method": "POST",
-                "Access-Control-Request-Headers": "content-type"})
+                "Access-Control-Request-Headers": "content-type,x-applysync-csrf"})
             assert response.status_code == 200
             assert response.headers["access-control-allow-origin"] == origin
-            assert "access-control-allow-credentials" not in response.headers
+            assert response.headers["access-control-allow-credentials"] == "true"
+            assert "x-applysync-csrf" in response.headers["access-control-allow-headers"].lower()
             health = await client.get("/health", headers={"Origin": origin})
             assert health.json() == {"status": "healthy"}
             failed = await client.get("/applications", headers={"Origin": origin})
diff --git a/tests/test_persistence.py b/tests/test_persistence.py
index 4dcd2ca..a1d67cf 100644
--- a/tests/test_persistence.py
+++ b/tests/test_persistence.py
@@ -14,8 +14,10 @@ pytestmark = pytest.mark.database
 def test_actual_schema(test_engine):
     schema = inspect(test_engine)
     columns = {column["name"]: column for column in schema.get_columns("job_applications")}
-    assert set(columns) == {"id", "company", "role", "applied_on", "created_at"}
-    assert all(not column["nullable"] for column in columns.values())
+    assert set(columns) == {"id", "company", "role", "applied_on", "created_at", "owner_id"}
+    assert all(not column["nullable"] for name, column in columns.items() if name != "owner_id")
+    assert columns["owner_id"]["nullable"]
+    assert schema.get_foreign_keys("job_applications")[0]["referred_table"] == "users"
     assert columns["company"]["type"].length == 200
     assert columns["role"]["type"].length == 200
     assert columns["created_at"]["type"].timezone
````

## Complete new source and test files

### auth.py

```python
"""Identity, revocable JWT cookie sessions, and server-side authorization."""

from collections import OrderedDict
from datetime import datetime, timedelta, timezone
from hashlib import sha256
from threading import Lock
from time import monotonic
from typing import Annotated
from uuid import UUID, uuid4
import secrets

from argon2 import PasswordHasher
from argon2.exceptions import VerificationError, InvalidHashError
from email_validator import validate_email, EmailNotValidError
from fastapi import APIRouter, Depends, HTTPException, Request, Response
import jwt
from pydantic import BaseModel, ConfigDict, Field, field_validator
from sqlalchemy import delete, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.engine import Engine

from auth_config import load_auth_settings
from database import get_engine, session_scope
from models import AuthSession, User

COOKIE = "applysync_session"
ISSUER = "applysync"
AUDIENCE = "applysync-api"
hasher = PasswordHasher()
# A missing account still incurs the same password verification work.
dummy_hash = hasher.hash(secrets.token_urlsafe(32))
router = APIRouter(prefix="/auth", tags=["authentication"])
DatabaseEngine = Annotated[Engine, Depends(get_engine)]


class Credentials(BaseModel):
    model_config = ConfigDict(extra="forbid")
    email: str = Field(max_length=254)
    password: str = Field(min_length=12, max_length=128)

    @field_validator("email")
    @classmethod
    def normalize_email(cls, value):
        try:
            return validate_email(value.strip(), check_deliverability=False,
                                  allow_smtputf8=False).normalized.lower()
        except EmailNotValidError:
            raise ValueError("Enter a valid email address.") from None


class Identity(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    email: str


class AttemptLimiter:
    """Bounded per-process throttling; never stores passwords or raw emails."""
    def __init__(self):
        self.lock = Lock()
        self.entries = OrderedDict()

    def check(self, address, email):
        now = monotonic()
        keys = [("ip", address, 50), ("email", sha256(email.encode()).hexdigest(), 10)]
        with self.lock:
            self.entries = OrderedDict((k, v) for k, v in self.entries.items() if v[0] > now - 900)
            if len(self.entries) >= 10000:
                raise HTTPException(429, "Too many attempts. Try again later.", headers={"Retry-After": "900"})
            if any(self.entries.get((kind, key), (now, 0))[1] >= limit for kind, key, limit in keys):
                raise HTTPException(429, "Too many attempts. Try again later.", headers={"Retry-After": "900"})
            for kind, key, _ in keys:
                start, count = self.entries.get((kind, key), (now, 0))
                self.entries[(kind, key)] = (start, count + 1)


def invalid_session():
    return HTTPException(401, "Authentication required")


def current_user(request: Request, engine: DatabaseEngine) -> Identity:
    token = request.cookies.get(COOKIE)
    if not token:
        raise invalid_session()
    settings = load_auth_settings()
    try:
        claims = jwt.decode(token, settings.secret, algorithms=["HS256"], issuer=ISSUER,
                            audience=AUDIENCE, options={"require": ["sub", "jti", "exp", "iat", "iss", "aud"]})
        user_id, session_id = UUID(claims["sub"]), UUID(claims["jti"])
        if (type(claims["iat"]) is not int or type(claims["exp"]) is not int
                or not 0 < claims["exp"] - claims["iat"] <= settings.lifetime):
            raise ValueError()
    except (jwt.PyJWTError, ValueError, TypeError, AttributeError):
        raise invalid_session() from None
    with session_scope(engine) as session:
        identity = session.scalar(select(User).join(AuthSession, AuthSession.user_id == User.id).where(
            User.id == user_id, AuthSession.id == session_id,
            AuthSession.expires_at > datetime.now(timezone.utc)))
        if identity is None:
            raise invalid_session()
        result = Identity.model_validate(identity)
    request.state.session_id = session_id
    return result


CurrentUser = Annotated[Identity, Depends(current_user)]


def issue_session(session, user, settings, request):
    now = datetime.now(timezone.utc).replace(microsecond=0)
    sid = uuid4()
    # Replacing a browser session revokes the previous cookie too, if valid.
    old = request.cookies.get(COOKIE)
    if old:
        try:
            claims = jwt.decode(old, settings.secret, algorithms=["HS256"], issuer=ISSUER, audience=AUDIENCE)
            session.execute(delete(AuthSession).where(AuthSession.id == UUID(claims["jti"])))
        except (jwt.PyJWTError, ValueError, KeyError, TypeError):
            pass
    session.add(AuthSession(id=sid, user_id=user.id, expires_at=now + timedelta(seconds=settings.lifetime)))
    return jwt.encode({"sub": str(user.id), "jti": str(sid), "iat": int(now.timestamp()),
                       "exp": int(now.timestamp()) + settings.lifetime, "iss": ISSUER, "aud": AUDIENCE},
                      settings.secret, algorithm="HS256")


def set_cookie(response, token, settings):
    response.set_cookie(COOKIE, token, max_age=settings.lifetime, httponly=True,
                        secure=settings.secure, samesite="lax", path="/")
    response.headers["Cache-Control"] = "no-store"


def throttle(request, payload):
    request.app.state.attempt_limiter.check(request.client.host if request.client else "unknown", payload.email)


@router.post("/register", response_model=Identity, status_code=201)
def register(payload: Credentials, request: Request, response: Response, engine: DatabaseEngine):
    settings = load_auth_settings()
    throttle(request, payload)
    password_hash = hasher.hash(payload.password)
    try:
        with session_scope(engine) as session:
            user = User(email=payload.email, password_hash=password_hash)
            session.add(user)
            session.flush()  # Database uniqueness is authoritative under concurrency.
            result = Identity.model_validate(user)
            token = issue_session(session, user, settings, request)
    except IntegrityError:
        raise HTTPException(409, "Registration could not be completed for this email.") from None
    set_cookie(response, token, settings)
    return result


@router.post("/login", response_model=Identity)
def login(payload: Credentials, request: Request, response: Response, engine: DatabaseEngine):
    settings = load_auth_settings()
    throttle(request, payload)
    with session_scope(engine) as session:
        user = session.scalar(select(User).where(User.email == payload.email))
        try:
            hasher.verify(user.password_hash if user else dummy_hash, payload.password)
        except (VerificationError, InvalidHashError):
            raise HTTPException(401, "Invalid email or password") from None
        if user is None:
            raise HTTPException(401, "Invalid email or password")
        if hasher.check_needs_rehash(user.password_hash):
            user.password_hash = hasher.hash(payload.password)
        result = Identity.model_validate(user)
        token = issue_session(session, user, settings, request)
    set_cookie(response, token, settings)
    return result


@router.get("/me", response_model=Identity)
def me(user: CurrentUser, response: Response):
    response.headers["Cache-Control"] = "no-store"
    return user


@router.post("/logout", status_code=204)
def logout(request: Request, user: CurrentUser, engine: DatabaseEngine):
    settings = load_auth_settings()
    with session_scope(engine) as session:
        session.execute(delete(AuthSession).where(AuthSession.id == request.state.session_id,
                                                 AuthSession.user_id == user.id))
    response = Response(status_code=204, headers={"Cache-Control": "no-store"})
    response.delete_cookie(COOKIE, path="/", secure=settings.secure, httponly=True, samesite="lax")
    return response

```

### auth_config.py

```python
"""Explicit cookie topology and signing configuration; never reveal values."""

from dataclasses import dataclass
import os
import re
from urllib.parse import urlsplit

from dotenv import dotenv_values

from config import ConfigurationError, ROOT

LOCAL_ORIGINS = tuple(f"http://{host}:{port}" for host in ("localhost", "127.0.0.1")
                      for port in (5173, 4173))


def values():
    return {**dotenv_values(ROOT / ".env", interpolate=False), **os.environ}


def allowed_origins():
    configured = values().get("APPLYSYNC_AUTH_ORIGINS")
    origins = tuple(configured.split(",")) if configured else LOCAL_ORIGINS
    for origin in origins:
        url = urlsplit(origin)
        if (url.scheme not in {"http", "https"} or not url.hostname or url.username
                or url.password or url.query or url.fragment or url.path
                or (url.scheme == "http" and origin not in LOCAL_ORIGINS)):
            raise ConfigurationError("Authentication origins must be explicit trusted origins.")
    return origins


@dataclass(frozen=True, repr=False)
class AuthSettings:
    secret: str
    secure: bool
    lifetime: int = 8 * 60 * 60


def load_auth_settings():
    settings = values()
    secret = settings.get("APPLYSYNC_AUTH_SECRET", "")
    mode = settings.get("APPLYSYNC_AUTH_MODE", "")
    if not re.fullmatch(r"[0-9a-fA-F]{64,}", secret) or len(set(secret)) < 12:
        raise ConfigurationError("Generate a strong authentication signing secret locally.")
    if mode not in {"local", "production"}:
        raise ConfigurationError("Set authentication mode explicitly to local or production.")
    if mode == "production" and any(not o.startswith("https://") for o in allowed_origins()):
        raise ConfigurationError("Production authentication requires HTTPS origins.")
    return AuthSettings(secret, mode == "production")

```

### frontend/src/Auth.test.tsx

```tsx
import { act, render, screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { MemoryRouter } from 'react-router'
import { afterEach, expect, it, vi } from 'vitest'
import { App } from './App'
import { internalDestination } from './Auth'

const json = (body: unknown, status = 200) => new Response(JSON.stringify(body), { status })
const a = { id: 'user-a', email: 'synthetic-a@example.com' }
const b = { id: 'user-b', email: 'synthetic-b@example.com' }
const row = { id: '00000000-0000-4000-8000-000000000099', company: 'Private A', role: 'Engineer', applied_on: '2026-09-01', created_at: '2026-09-01T00:00:00Z' }
const mount = (path = '/applications') => { render(<MemoryRouter initialEntries={[path]}><App /></MemoryRouter>); return userEvent.setup() }
afterEach(() => vi.unstubAllGlobals())

it('waits for session restoration and separates network failure from signed out', async () => {
  let resolve!: (response: Response) => void
  const fetchMock = vi.fn().mockImplementationOnce(() => new Promise<Response>(r => { resolve = r }))
  vi.stubGlobal('fetch', fetchMock)
  const user = mount()
  expect(screen.getByRole('status')).toHaveTextContent('Checking your session')
  expect(screen.queryByRole('searchbox')).not.toBeInTheDocument()
  expect(screen.queryByLabelText('Password')).not.toBeInTheDocument()
  await act(async () => resolve(json({}, 500)))
  expect(await screen.findByRole('alert')).toHaveTextContent('Session unavailable')
  expect(screen.queryByLabelText('Password')).not.toBeInTheDocument()
  fetchMock.mockResolvedValue(json({}, 401))
  await user.click(screen.getByRole('button', { name: 'Retry session' }))
  expect(await screen.findByRole('heading', { name: 'Welcome back' })).toBeInTheDocument()
})

it('uses credentialed writes with CSRF protection and prevents duplicate auth submission', async () => {
  let complete!: (response: Response) => void
  const posts = vi.fn(() => new Promise<Response>(resolve => { complete = resolve }))
  const fetchMock = vi.fn((url, options) => String(url).endsWith('/auth/me') ? Promise.resolve(json({}, 401))
    : options?.method === 'POST' ? posts() : Promise.resolve(json({ items: [], limit: 20, offset: 0 })))
  vi.stubGlobal('fetch', fetchMock)
  const user = mount('/register')
  await user.type(await screen.findByLabelText('Email'), 'synthetic@example.com')
  await user.type(screen.getByLabelText('Password'), 'synthetic-password-only')
  await user.click(screen.getByRole('button', { name: 'Create account' }))
  expect(screen.getByRole('button', { name: 'Please wait…' })).toBeDisabled()
  await user.keyboard('{Enter}')
  expect(posts).toHaveBeenCalledTimes(1)
  const options = fetchMock.mock.calls.find(([url]) => String(url).endsWith('/auth/register'))![1]
  expect(options.credentials).toBe('include')
  expect(options.headers['X-ApplySync-CSRF']).toBe('1')
  await act(async () => complete(json(a, 201)))
  expect(await screen.findByText('No stored applications yet')).toBeInTheDocument()
})

it('discards private cache and cancels an old in-flight list before switching accounts', async () => {
  let finishOld!: (response: Response) => void
  let oldSignal!: AbortSignal
  let active = a
  let lists = 0
  vi.stubGlobal('fetch', vi.fn((url, options) => {
    if (String(url).endsWith('/auth/me')) return Promise.resolve(json(active))
    if (String(url).endsWith('/auth/logout')) return Promise.resolve(new Response(null, { status: 204 }))
    if (String(url).endsWith('/auth/login')) { active = b; return Promise.resolve(json(b)) }
    lists++
    if (lists === 1) { oldSignal = options.signal; return new Promise<Response>(resolve => { finishOld = resolve }) }
    return Promise.resolve(json({ items: [], limit: 20, offset: 0 }))
  }))
  const user = mount()
  await user.click(await screen.findByRole('button', { name: 'Log out' }))
  await user.type(await screen.findByLabelText('Email'), b.email)
  await user.type(screen.getByLabelText('Password'), 'synthetic-password-only')
  await user.click(screen.getByRole('button', { name: 'Sign in' }))
  expect(await screen.findByText('No stored applications yet')).toBeInTheDocument()
  expect(oldSignal.aborted).toBe(true)
  await act(async () => finishOld(json({ items: [row], limit: 20, offset: 0 })))
  expect(screen.queryByText('Private A')).not.toBeInTheDocument()
  expect(screen.getByText(b.email)).toBeInTheDocument()
})

it('a 401 creation ends the session and never automatically replays the write', async () => {
  let writes = 0
  vi.stubGlobal('fetch', vi.fn((url, options) => {
    if (String(url).endsWith('/auth/me')) return Promise.resolve(json(a))
    if (options?.method === 'POST') { writes++; return Promise.resolve(json({}, 401)) }
    return Promise.resolve(json({ items: [], limit: 20, offset: 0 }))
  }))
  const user = mount('/applications/new')
  await user.type(await screen.findByLabelText('Company', { exact: false }), 'Unsaved')
  await user.type(screen.getByLabelText('Role', { exact: false }), 'Engineer')
  await user.type(screen.getByLabelText('Applied date', { exact: false }), '2026-09-01')
  await user.click(screen.getByRole('button', { name: 'Save application' }))
  expect(await screen.findByRole('heading', { name: 'Welcome back' })).toBeInTheDocument()
  expect(screen.queryByRole('dialog')).not.toBeInTheDocument()
  await waitFor(() => expect(writes).toBe(1))
})

it('rejects external and ambiguous return destinations', () => {
  for (const value of ['https://evil.example', '//evil.example', '/\\evil.example', '/login', '/applications/../login']) {
    expect(internalDestination(value)).toBe('/applications')
  }
  expect(internalDestination('/applications?offset=20&view=board')).toBe('/applications?offset=20&view=board')
})

it('does not claim logout succeeded when the network fails, and hides private data', async () => {
  vi.stubGlobal('fetch', vi.fn((url) => {
    if (String(url).endsWith('/auth/me')) return Promise.resolve(json(a))
    if (String(url).endsWith('/auth/logout')) return Promise.reject(new Error('network unavailable'))
    return Promise.resolve(json({ items: [row], limit: 20, offset: 0 }))
  }))
  const user = mount()
  await screen.findByText('Private A')
  await user.click(screen.getByRole('button', { name: 'Log out' }))
  expect(await screen.findByRole('alert')).toHaveTextContent('Logout could not be confirmed')
  expect(screen.queryByText('Private A')).not.toBeInTheDocument()
  expect(screen.queryByRole('heading', { name: 'Welcome back' })).not.toBeInTheDocument()
})

it('refreshing session on focus catches expiry and removes already loaded private records', async () => {
  let expired = false
  vi.stubGlobal('fetch', vi.fn((url) => String(url).endsWith('/auth/me')
    ? Promise.resolve(json(expired ? {} : a, expired ? 401 : 200))
    : Promise.resolve(json({ items: [row], limit: 20, offset: 0 }))))
  mount()
  await screen.findByText('Private A')
  expired = true
  await act(async () => { window.dispatchEvent(new Event('focus')) })
  expect(await screen.findByRole('heading', { name: 'Welcome back' })).toBeInTheDocument()
  expect(screen.queryByText('Private A')).not.toBeInTheDocument()
})

```

### frontend/src/Auth.tsx

```tsx
import { createContext, useContext, useEffect, useRef, useState, type FormEvent, type ReactNode } from 'react'
import { Link, Navigate, useLocation, useNavigate, useSearchParams } from 'react-router'
import { QueryClientProvider } from '@tanstack/react-query'
import { ApiError, errorMessage, request } from './api'
import { makeQueryClient } from './query'
import { Button } from './components/ui'

type Identity = { id: string; email: string }
type AuthState = { user: Identity | null; checking: boolean; failure: string }
type AuthContextValue = AuthState & { signIn: (email: string, password: string, register: boolean) => Promise<void>; logout: () => Promise<void>; restore: () => void }
const AuthContext = createContext<AuthContextValue | null>(null)
export const useAuth = () => useContext(AuthContext)

function identity(value: unknown): Identity {
  const user = value as Identity
  if (!user || typeof user.id !== 'string' || typeof user.email !== 'string') throw new ApiError('response')
  return { id: user.id, email: user.email }
}

// A newly mounted cache for each identity. Old requests can only reference their
// old cache, which is cancelled/cleared on unmount, never another account's cache.
export function PrivateCache({ children }: { children: ReactNode }) {
  const [client] = useState(makeQueryClient)
  useEffect(() => () => { void client.cancelQueries(); client.clear() }, [client])
  return <QueryClientProvider client={client}>{children}</QueryClientProvider>
}

export function AuthProvider({ children }: { children: ReactNode }) {
  const [state, setState] = useState<AuthState>({ user: null, checking: true, failure: '' })
  const active = useRef<AbortController | null>(null)
  const changingSession = useRef(false)
  function begin() { active.current?.abort(); const controller = new AbortController(); active.current = controller; return controller }
  async function restore(background = false) {
    if (background && changingSession.current) return
    const controller = begin()
    if (!background) setState(previous => ({ ...previous, checking: true, failure: '' }))
    try {
      const user = identity(await request('/auth/me', undefined, controller.signal))
      if (!controller.signal.aborted) setState({ user, checking: false, failure: '' })
    } catch (error) {
      if (!controller.signal.aborted) setState(previous => ({ user: error instanceof ApiError && error.kind === 'unauthorized' ? null : previous.user,
        checking: false, failure: error instanceof ApiError && error.kind === 'unauthorized' ? '' : errorMessage(error) }))
    }
  }
  useEffect(() => {
    void restore()
    const expired = () => { active.current?.abort(); setState({ user: null, checking: false, failure: '' }) }
    const focus = () => { void restore(true) }
    const timer = window.setInterval(() => { void restore(true) }, 60_000)
    window.addEventListener('applysync:expired', expired)
    window.addEventListener('focus', focus)
    return () => { window.clearInterval(timer); active.current?.abort(); window.removeEventListener('applysync:expired', expired); window.removeEventListener('focus', focus) }
  }, [])
  async function signIn(email: string, password: string, register: boolean) {
    const controller = begin()
    changingSession.current = true
    try {
      const user = identity(await request(register ? '/auth/register' : '/auth/login', { email, password }, controller.signal))
      if (!controller.signal.aborted) setState({ user, checking: false, failure: '' })
    } finally { changingSession.current = false }
  }
  async function logout() {
    const controller = begin()
    changingSession.current = true
    // Hide/unmount all private content immediately, including pending mutations.
    setState(previous => ({ ...previous, checking: true, failure: '' }))
    try {
      await request('/auth/logout', {}, controller.signal)
      if (!controller.signal.aborted) setState({ user: null, checking: false, failure: '' })
    } catch (error) {
      if (!controller.signal.aborted) setState(previous => ({ ...previous, checking: false,
        user: error instanceof ApiError && error.kind === 'unauthorized' ? null : previous.user,
        failure: error instanceof ApiError && error.kind === 'unauthorized' ? '' : 'Logout could not be confirmed. Retry the session check, then log out again.' }))
    } finally { changingSession.current = false }
  }
  return <AuthContext.Provider value={{ ...state, signIn, logout, restore: () => void restore() }}>{children}</AuthContext.Provider>
}

export function SessionGate({ children }: { children: ReactNode }) {
  const auth = useAuth()!
  if (auth.checking) return <p role="status">Checking your session…</p>
  if (auth.failure) return <div className="empty-state" role="alert"><h2>Session unavailable</h2><p>{auth.failure}</p><Button onClick={auth.restore}>Retry session</Button></div>
  return children
}

export function ProtectedApplications({ children }: { children: ReactNode }) {
  const auth = useAuth()!
  const location = useLocation()
  return <SessionGate>{auth.user ? <PrivateCache key={auth.user.id}>{children}</PrivateCache>
    : <Navigate to={`/login?returnTo=${encodeURIComponent(location.pathname + location.search)}`} replace />}</SessionGate>
}

export function internalDestination(value: string | null) {
  if (!value || !/^\/applications(?:\/(?:new|[0-9a-fA-F-]{36}))?(?:\?[^#]*)?$/.test(value) || value.includes('\\')) return '/applications'
  return value
}

export function AuthForm({ register = false }: { register?: boolean }) {
  const auth = useAuth()!
  const [params] = useSearchParams()
  const navigate = useNavigate()
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [pending, setPending] = useState(false)
  const lock = useRef(false)
  const [failure, setFailure] = useState('')
  const destination = internalDestination(params.get('returnTo'))
  async function submit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault()
    if (lock.current) return
    lock.current = true; setPending(true); setFailure('')
    try { await auth.signIn(email, password, register); setPassword(''); navigate(destination, { replace: true }) }
    catch (error) { setFailure(error instanceof ApiError && error.kind === 'unauthorized' ? 'Invalid email or password.'
      : error instanceof ApiError && error.kind === 'validation' ? 'Use a valid email and a password of 12–128 characters.' : errorMessage(error)) }
    finally { lock.current = false; setPending(false) }
  }
  return <SessionGate>{auth.user ? <Navigate to={destination} replace /> : <div className="auth-card applications-workspace">
    <p className="eyebrow">YOUR PRIVATE WORKSPACE</p><h1>{register ? 'Create your account' : 'Welcome back'}</h1>
    <p className="page-description">{register ? 'Keep your applications together, and private to you.' : 'Sign in to your stored applications. If your session ended, submit any unfinished creation again after signing in.'}</p>
    <form onSubmit={submit} className="application-form">
      {failure && <p role="alert" className="field-error">{failure}</p>}
      <div className="field"><label htmlFor="email">Email</label><input id="email" type="email" autoComplete="username" required maxLength={254} value={email} readOnly={pending} onChange={e => setEmail(e.target.value)} /></div>
      <div className="field"><label htmlFor="password">Password</label><input id="password" type="password" autoComplete={register ? 'new-password' : 'current-password'} required minLength={12} maxLength={128} aria-describedby="password-hint" value={password} readOnly={pending} onChange={e => setPassword(e.target.value)} /><p id="password-hint" className="field-hint">12–128 characters. Spaces are preserved.</p></div>
      <Button type="submit" variant="primary" disabled={pending}>{pending ? 'Please wait…' : register ? 'Create account' : 'Sign in'}</Button>
    </form>
    <p><Link to={`${register ? '/login' : '/register'}?returnTo=${encodeURIComponent(destination)}`}>{register ? 'Already registered? Sign in' : 'New here? Create an account'}</Link></p>
    <Link to="/preview/applications">Explore the labelled sample preview</Link>
  </div>}</SessionGate>
}

```

### migrations/versions/0002_identity_ownership.py

```python
"""Revocable identities and quarantined legacy ownership.

No legacy records are changed or assigned. NULL owners are inaccessible via API.
"""
from alembic import op
import sqlalchemy as sa

revision = "0002"
down_revision = "0001"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table("users",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("email", sa.String(254), nullable=False),
        sa.Column("password_hash", sa.String(512), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.PrimaryKeyConstraint("id", name="pk_users"),
        sa.UniqueConstraint("email", name="uq_users_email"),
        sa.CheckConstraint("email = lower(email)", name="ck_users_email_lower"))
    op.create_table("auth_sessions",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("user_id", sa.Uuid(), nullable=False),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id", name="pk_auth_sessions"),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], name="fk_auth_sessions_user"))
    op.create_index("ix_auth_sessions_user_id", "auth_sessions", ["user_id"])
    op.add_column("job_applications", sa.Column("owner_id", sa.Uuid(), nullable=True))
    op.create_foreign_key("fk_job_applications_owner", "job_applications", "users", ["owner_id"], ["id"])
    op.create_index("ix_job_applications_owner_order", "job_applications", ["owner_id", "created_at", "id"])


def downgrade():
    # Downgrading would remove identity/ownership. Require an explicit manual plan.
    raise RuntimeError("Identity downgrade is intentionally disabled; preserve user data.")

```

### scripts/assign_legacy.py

```python
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

```

### scripts/setup_auth.py

```python
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

```

### tests/test_auth.py

```python
"""Security tests use only verified applysync_test and synthetic identities."""
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta, timezone
import secrets
from uuid import UUID, uuid4

from fastapi.testclient import TestClient
import jwt
import pytest
from sqlalchemy import delete, func, select

from auth import COOKIE, hasher, AttemptLimiter
from auth_config import load_auth_settings
from database import session_scope
from main import create_app
from models import AuthSession, JobApplication, User

HEADERS = {"Origin": "http://127.0.0.1:5173", "X-ApplySync-CSRF": "1"}
DATA = {"company": "Synthetic private company", "role": "Engineer", "applied_on": "2026-09-01"}


@pytest.fixture
def identities(test_engine, monkeypatch):
    monkeypatch.setenv("APPLYSYNC_AUTH_SECRET", secrets.token_hex(32))
    monkeypatch.setenv("APPLYSYNC_AUTH_MODE", "local")
    app = create_app("test")
    app.state.engine = test_engine
    prefix = str(uuid4())
    password = secrets.token_urlsafe(24)
    clients = []
    def account(suffix="a", register=True):
        client = TestClient(app, headers=HEADERS)
        clients.append(client)
        credentials = {"email": f"{prefix}-{suffix}@example.com", "password": password}
        if register:
            response = client.post("/auth/register", json=credentials)
            assert response.status_code == 201
        return client, credentials
    try:
        yield app, account, test_engine
    finally:
        for client in clients:
            client.close()
        with session_scope(test_engine) as session:
            ids = select(User.id).where(User.email.startswith(prefix))
            session.execute(delete(JobApplication).where(JobApplication.owner_id.in_(ids)))
            session.execute(delete(AuthSession).where(AuthSession.user_id.in_(ids)))
            session.execute(delete(User).where(User.email.startswith(prefix)))


def test_identity_hash_normalization_duplicate_logout_and_replay(identities):
    app, account, engine = identities
    client, credentials = account()
    identity = client.get("/auth/me").json()
    assert set(identity) == {"id", "email"}
    with session_scope(engine) as session:
        user = session.get(User, UUID(identity["id"]))
        assert user.password_hash.startswith("$argon2id$")
        assert user.password_hash != credentials["password"]
        assert hasher.verify(user.password_hash, credentials["password"])
    duplicate = client.post("/auth/register", json={**credentials, "email": " " + credentials["email"].upper() + " "})
    assert duplicate.status_code == 409
    old_cookie = client.cookies.get(COOKIE)
    logout = client.post("/auth/logout")
    assert logout.status_code == 204 and "Max-Age=0" in logout.headers["set-cookie"]
    assert client.get("/auth/me").status_code == 401
    client.cookies.set(COOKIE, old_cookie)
    assert client.get("/auth/me").status_code == 401
    client.cookies.clear()
    login = client.post("/auth/login", json=credentials)
    assert login.status_code == 200
    assert "HttpOnly" in login.headers["set-cookie"] and "SameSite=lax" in login.headers["set-cookie"]
    assert "Secure" not in login.headers["set-cookie"]
    assert client.get("/auth/me").json() == identity
    for email in [credentials["email"], "absent@example.com"]:
        failure = client.post("/auth/login", json={"email": email, "password": "incorrect password"})
        assert failure.status_code == 401 and failure.json() == {"detail": "Invalid email or password"}


def test_ownership_before_pagination_and_forgery(identities):
    _, account, engine = identities
    a, _ = account("a")
    b, _ = account("b")
    own = []
    foreign = b.post("/applications", json=DATA).json()
    for _ in range(3):
        response = a.post("/applications", json=DATA)
        assert response.status_code == 201
        own.append(response.json())
    assert a.get("/applications?limit=1&offset=1").json()["items"] == [own[1]]
    assert b.get("/applications").json()["items"] == [foreign]
    for id_ in [foreign["id"], str(uuid4())]:
        response = a.get("/applications/" + id_)
        assert response.status_code == 404 and response.json() == {"detail": "Application not found"}
    assert a.post("/applications", json={**DATA, "owner_id": b.get("/auth/me").json()["id"]}).status_code == 422
    legacy_id = uuid4()
    try:
        with session_scope(engine) as session:
            session.add(JobApplication(id=legacy_id, company="Synthetic legacy", role="Engineer", applied_on=datetime.now().date()))
        assert a.get(f"/applications/{legacy_id}").status_code == 404
        assert b.get(f"/applications/{legacy_id}").status_code == 404
        assert len(a.get("/applications").json()["items"]) == 3
    finally:
        with session_scope(engine) as session:
            session.execute(delete(JobApplication).where(JobApplication.id == legacy_id))


@pytest.mark.parametrize("kind", ["missing", "malformed", "tampered", "expired", "subject", "algorithm", "claims", "revoked"])
def test_invalid_sessions(identities, kind):
    _, account, engine = identities
    client, _ = account()
    token = client.cookies.get(COOKIE)
    settings = load_auth_settings()
    claims = jwt.decode(token, settings.secret, algorithms=["HS256"], audience="applysync-api")
    client.cookies.clear()
    if kind == "malformed": token = "invalid"
    if kind == "tampered": token = jwt.encode(claims, secrets.token_hex(32), algorithm="HS256")
    if kind == "expired":
        claims["exp"] = claims["iat"] - 1
        token = jwt.encode(claims, settings.secret, algorithm="HS256")
    if kind == "subject":
        claims["sub"] = "not-a-uuid"
        token = jwt.encode(claims, settings.secret, algorithm="HS256")
    if kind == "algorithm": token = jwt.encode(claims, settings.secret, algorithm="HS384")
    if kind == "claims":
        del claims["jti"]
        token = jwt.encode(claims, settings.secret, algorithm="HS256")
    if kind == "revoked":
        with session_scope(engine) as session:
            session.execute(delete(AuthSession).where(AuthSession.id == UUID(claims["jti"])))
    if kind != "missing": client.cookies.set(COOKIE, token)
    for path in ["/auth/me", "/applications", "/applications/" + str(uuid4())]:
        response = client.get(path)
        assert response.status_code == 401 and response.json() == {"detail": "Authentication required"}
    assert client.get("/health").json() == {"status": "healthy"}


@pytest.mark.parametrize("headers", [{}, {"Origin": "http://127.0.0.1:5173"}, {"X-ApplySync-CSRF": "1"},
    {"Origin": "https://evil.example", "X-ApplySync-CSRF": "1"},
    {"Origin": "http://127.0.0.1:5173", "X-ApplySync-CSRF": "wrong"},
    {"Origin": "null", "X-ApplySync-CSRF": "1"}])
def test_csrf_all_mutations(identities, headers):
    app, account, _ = identities
    client, creds = account()
    client.headers.clear()
    for path in ["/auth/register", "/auth/login", "/auth/logout", "/applications"]:
        assert client.post(path, json=creds, headers=headers).status_code == 403
    assert client.get("/auth/me").status_code == 200


def test_concurrent_duplicate(identities):
    app, account, engine = identities
    _, creds = account(register=False)
    def register(_):
        with TestClient(app, headers=HEADERS) as client:
            return client.post("/auth/register", json=creds).status_code
    with ThreadPoolExecutor(max_workers=2) as pool:
        assert sorted(pool.map(register, range(2))) == [201, 409]
    with session_scope(engine) as session:
        assert session.scalar(select(func.count()).select_from(User).where(User.email == creds["email"])) == 1


def test_validation_does_not_echo_password(identities):
    _, account, _ = identities
    client, creds = account(register=False)
    for password in ["sentinel!", "x" * 129]:
        response = client.post("/auth/register", json={**creds, "password": password})
        assert response.status_code == 422 and password not in response.text
        assert all("input" not in item and "ctx" not in item for item in response.json()["detail"])
    assert client.post("/auth/register", json={**creds, "email": "invalid"}).status_code == 422


def test_throttle():
    from fastapi import HTTPException
    limiter = AttemptLimiter()
    for _ in range(10): limiter.check("synthetic-client", "synthetic@example.com")
    with pytest.raises(HTTPException) as caught:
        limiter.check("synthetic-client", "synthetic@example.com")
    assert caught.value.status_code == 429


def test_production_cookie_and_missing_config(monkeypatch):
    from auth import set_cookie
    from fastapi import Response
    from config import ConfigurationError
    monkeypatch.setenv("APPLYSYNC_AUTH_SECRET", secrets.token_hex(32))
    monkeypatch.setenv("APPLYSYNC_AUTH_MODE", "production")
    monkeypatch.setenv("APPLYSYNC_AUTH_ORIGINS", "https://app.example.com")
    response = Response()
    set_cookie(response, "synthetic-not-a-token", load_auth_settings())
    assert "Secure" in response.headers["set-cookie"] and "HttpOnly" in response.headers["set-cookie"]
    monkeypatch.setenv("APPLYSYNC_AUTH_SECRET", "")
    with pytest.raises(ConfigurationError): load_auth_settings()


def test_password_spaces_and_server_session_expiry(identities):
    _, account, engine = identities
    client, creds = account(register=False)
    spaced = {**creds, "password": " " + creds["password"] + " "}
    assert client.post("/auth/register", json=spaced).status_code == 201
    assert client.post("/auth/login", json=creds).status_code == 401
    assert client.post("/auth/login", json=spaced).status_code == 200
    id_ = UUID(client.get("/auth/me").json()["id"])
    with session_scope(engine) as session:
        for row in session.scalars(select(AuthSession).where(AuthSession.user_id == id_)):
            row.expires_at = datetime.now(timezone.utc) - timedelta(seconds=1)
    assert client.get("/auth/me").status_code == 401


def test_local_assignment_is_explicit_atomic_and_scoped(identities):
    from scripts.assign_legacy import assign
    _, account, engine = identities
    client, creds = account()
    ids = [uuid4(), uuid4()]
    try:
        with session_scope(engine) as session:
            for id_ in ids:
                session.add(JobApplication(id=id_, company="Synthetic legacy", role="Engineer", applied_on=datetime.now().date()))
        with pytest.raises(ValueError): assign(engine, "absent@example.com", ids)
        with pytest.raises(ValueError): assign(engine, creds["email"], [ids[0], uuid4()])
        assert client.get("/applications").json()["items"] == []
        assert assign(engine, creds["email"], [ids[0]]) == 1
        assert client.get(f"/applications/{ids[0]}").status_code == 200
        assert client.get(f"/applications/{ids[1]}").status_code == 404
        with pytest.raises(ValueError): assign(engine, creds["email"], ids)
        assert client.get(f"/applications/{ids[1]}").status_code == 404
    finally:
        with session_scope(engine) as session:
            session.execute(delete(JobApplication).where(JobApplication.id.in_(ids)))


def test_auth_configuration_failure_is_generic_and_health_still_works(identities, monkeypatch, caplog):
    _, account, _ = identities
    client, creds = account(register=False)
    monkeypatch.setenv("APPLYSYNC_AUTH_SECRET", "invalid-private-sentinel")
    response = client.post("/auth/register", json=creds)
    assert response.status_code == 500 and response.json() == {"detail": "Internal server error"}
    assert "invalid-private-sentinel" not in response.text + caplog.text
    assert creds["password"] not in response.text + caplog.text
    assert client.get("/health").json() == {"status": "healthy"}

```

### tests/test_ownership_migration.py

```python
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
            command.upgrade(config, "head")
            command.upgrade(config, "head")
            assert connection.scalar(text("select version_num from alembic_version")) == "0002"
            assert set(inspect(connection).get_table_names(schema=schema)) == {"alembic_version", "users", "auth_sessions", "job_applications"}
            assert connection.scalar(text("select count(*) from job_applications")) == int(legacy)
            if legacy:
                row = connection.execute(text("select id,company,owner_id from job_applications")).one()
                assert row == (id_, "Synthetic legacy", None)
        finally:
            transaction.rollback()

```
