# Build 2, Task 2 — real application API integration

## Final checkpoint update — 25 September 2026

Sanjay reports the following manual verification and understanding. These are
**user-reported checks**, not checks independently rerun or observed by Codex:

- The frontend design is approved.
- Creating a real application works, and the record remains after refreshing.
- Board/List switching on the real Applications screen works.
- He understands that real records currently appear under the display-only
  **Stage not recorded** fallback and that authoritative stage tracking belongs
  to Build 5.

The full integration diff and latest Board correction were compared with this
review package before checkpointing. Creation/list/detail use the existing API;
the real Board and List consume the same paginated query result and URL search/
offset state; preview fixtures remain isolated; CORS remains an explicit local
allowlist; and guarded database automation still targets only `applysync_test`.
No blocking issue was found. The approved design was not revised.

The final corrected executable files match the post-correction results recorded
below: typecheck/build passed, **19 frontend tests passed**, and **9 Chromium
browser tests passed**. The backend/CORS implementation, API/query foundation and
guarded real integration runner have not changed since the earlier **63 Python
tests passed** and **one real browser → FastAPI → test PostgreSQL flow passed**;
those two results are reused as historical evidence rather than claimed as fresh.

This checkpoint is authorized with message
`Connect ApplySync frontend to application APIs`. The resulting commit identifier,
normal push result and live remote verification are reported separately after Git
completes; they cannot be embedded self-referentially in this commit. The detailed
Git state later in this document describes the pre-commit review point.

Build 2 implementation is ready to hand off toward Build 3, but Build 2 is not
declared wholly complete under the repository learning agreement. The detailed
request-flow explanation, focused investigation/change exercise and earlier
transaction exercise remain pending and carry forward as nonblocking learning
gaps. This task does not begin Authentication & Ownership.

## Focused correction — real Board/List restored

Sanjay reports that creating a **real application and reloading preserves it**.
This is user-reported persistence verification, distinct from Codex's earlier
real browser/database test. His request-flow explanation and earlier transaction
exercise are still pending; this report does not mark them complete.

Per his explicit correction, the main `/applications` screen now has the approved
Board/List toggle. List remains the default; `?view=board` opens Board directly.
Both views consume the same filtered `list.data.items` from the existing query
cache. The view query parameter is independent of `q` and `offset`, so switching
does not reset search/pagination or refetch the page. Both use the same pagination
controls and current-page counts.

`StoredBoard` renders a single neutral column, **Stage not recorded**, with the
explanation: “Applications will be grouped by stage when stage tracking is
available.” This is display text only, not a stage field or enum. No API record,
POST body or database row is assigned this value or Applied. The existing
`ApplicationCard` styling is shared, with real cards linking to real detail routes.
The separately labelled `/preview/applications` retains its fictional multistage
board and isolated state.

Correction files: `StoredApplications.tsx` owns the toggle and selection;
`ApplicationsView.tsx` shares the card and adds `StoredBoard`; three CSS rules size
the column and style its neutral heading/explanation. The focused component/browser
checks, README and this handoff are updated. No backend, dependency, migration,
authentication or drag-and-drop changes were made for this correction.

Fresh correction checks, run from `frontend/`:

| Command | Result |
| --- | --- |
| `npm.cmd run typecheck` | Passed. |
| `npm.cmd run build` | Passed, 2.50s; 1954 modules; JS 329.53 kB, CSS 20.47 kB. |
| `npm.cmd run test` | **19 passed**, four files, 4.41s. Loading, error/retry and empty states are checked in both views, including switching during these states. |
| `npm.cmd run test:e2e` | **9 passed**, 12.7s. New browser check compares real-route record IDs across Board/List on two pages, preserves search/offset, verifies no refetch solely from switching, opens real details, checks fallback/counts, absence of sample data/stage controls, and zero writes. |

The first typecheck caught an unsupported Testing Library `exact` option in the
new test; it was removed and the full check sequence above passed. Browser tests
for this correction use synthetic mocked API responses, not database writes.
Backend/API/query/real-integration-runner fingerprints match the prior verified
snapshot. The earlier **63 passing backend tests** and **one passing real
browser → FastAPI → test PostgreSQL flow** below are explicitly reused historical
evidence, not rerun results. No database access or cleanup was needed for this
display correction. Chromium is the tested browser; other engines remain unrun.

Fresh rendered images were inspected: [desktop Board](screenshots/Build2_Task2/correction/stored-board.png),
[desktop List](screenshots/Build2_Task2/correction/stored-list.png),
[mobile Board](screenshots/Build2_Task2/correction/stored-mobile-board.png), and
[mobile List](screenshots/Build2_Task2/correction/stored-mobile-list.png).
The approved design is preserved. The frontend on port 5173 returned HTTP 200.
Open http://127.0.0.1:5173/applications?view=board to review the correction.
Everything remains unstaged and uncommitted on `main` at the base commit below.

Correction success path: toggle → `selection('view', ...)` updates only view in
the URL → the same cached/filtered applications reach `StoredBoard` or
`ApplicationList` → a shared card opens `/applications/{id}` with search/offset
intact. Failure path: a list query error takes the common error/retry branch
before either renderer; switching views preserves that error and never substitutes
sample data. The source appendix below has been refreshed to the corrected files.

## Outcome and identity

Implemented and verified for local review, with changes **uncommitted and unstaged**.
The approved light theme, purple accents, sidebar, cards, list and modal structure
are preserved. The normal `/applications` route now lists, creates and retrieves
PostgreSQL-backed records. The explicitly separate `/preview/applications` route
retains the synthetic Board/List and never writes to the API.

- Repository: `C:\Users\sanja\Desktop\ApplySync`, branch `main`.
- Base/current HEAD: `f4815f27fd36609d185e542338df3b4b131cc186`,
  `Build approved ApplySync frontend preview`.
- Working tree and index were clean before this task. No unrelated changes were
  reset or discarded. No commit, push, deployment or authentication was performed.
- Origin: `https://github.com/sanjaykumarmugada18/applysync.git`.
  A fresh `git ls-remote --exit-code origin refs/heads/main` returned that same
  base commit during verification. This is live evidence, not a tracking-ref inference.
- Read root AGENTS.md (no nested instructions found), the actual v2.0 PDF pages
  3, 6–7, 12 and 16, both Build 1 handoffs and the approved Build 2 Task 1 handoff.
  The existing routes, schemas, transaction/configuration code and tests were inspected.
- Sanjay's previous design approval and successful **preview** creation remain
  user-reported evidence. They are not evidence of his completing the integrated
  request-flow learning checkpoint. His real create/reload check is now reported
  successful, as recorded above; the explanatory exercises remain pending.

## Files and responsibilities

| File | Responsibility |
| --- | --- |
| `main.py` | Adds narrow local CORS permissions; preserves app factory, lazy engine, errors, health and API router. |
| `frontend/src/App.tsx` | QueryClient provider and separate stored/preview routes. |
| `frontend/src/StoredApplications.tsx` (new) | Queries, creation mutation, list invalidation, pagination, loaded-page search, detail routes and real-data states. |
| `frontend/src/PreviewApplications.tsx` (new) | Existing preview extracted from App with preview-scoped URLs and a return link; state stays in memory. |
| `frontend/src/api.ts` (new) | Shared fetch client, public origin validation, response checking, generic errors and safe backend field-error mapping. |
| `frontend/src/query.ts` (new) | QueryClient defaults: no automatic retries, no focus refetch, requests attempted even when browser reports offline. |
| `frontend/src/components/ApplicationForm.tsx` | Reuses validation/fields; adds async submission, synchronous repeat-submit guard, pending controls, retained values and field/server errors. |
| `frontend/src/components/ApplicationsView.tsx` | Reuses approved list with optional preview stage; real rows have no stage and use real detail links. Board links stay inside preview. |
| `frontend/src/components/Shell.tsx` | Real-versus-preview labels and navigation context; approved shell styling unchanged. |
| `frontend/src/components/ui.tsx` | Modal label and pending close/Escape protection; existing focus and native dialog behavior preserved. |
| `frontend/src/styles.css` | Stage-free real list, pagination, record-ID wrapping and neutral Board display rules. Existing design tokens/rules retained. |
| `frontend/index.html` | Neutral ApplySync title usable by both route families. |
| `frontend/.env.example` (new) | Placeholder-only public API-origin configuration instructions. |
| `frontend/package.json`, `frontend/package-lock.json` | Pin TanStack Query and its core dependency; add integration-test command. |
| `frontend/tsconfig.json` | Includes the new integration runner configuration in type checking. |
| `frontend/playwright.config.ts` | Keeps ordinary preview/mocked checks separate from real database integration. |
| `frontend/playwright.integration.config.ts` (new) | Dedicated real-browser suite, guarded run environment and temporary frontend on 4173. |
| `frontend/src/App.test.tsx`, `frontend/e2e/preview.spec.ts` | Existing preview regressions moved to the explicit preview route; new screenshots do not overwrite Task 1 evidence. |
| `frontend/src/api.test.ts` (new) | Safe configuration/errors, validation mapping, no POST retries and malformed-response behavior. |
| `frontend/src/StoredApplications.test.tsx` (new) | Loaded-page semantics, real labels, loading/empty/errors/retry, pending/validation, creation/cache refresh and preview separation. |
| `frontend/e2e/stored.spec.ts` (new) | Real browser with mocked network/500/422 responses, pending submission, retries and full-last-page pagination. |
| `frontend/e2e/integration.spec.ts` (new) | Real Chromium → FastAPI → test PostgreSQL creation, response, CORS, pagination, reload, missing ID and preview isolation. |
| `scripts/run_frontend_integration.py` (new) | Verifies dedicated test target, seeds only unique test fixtures, owns test server processes, runs browser checks, independently verifies persistence, and safely cleans up. |
| `tests/test_cors.py` (new) | Six ASGI checks for explicit origins, preflight, generic errors, health and rejected origins/methods. |
| `README.md` | Exact two-terminal Windows setup, API configuration, data/preview distinction, pagination and safe test commands. |
| `docs/screenshots/Build2_Task2/` (new) | Four integrated screenshots plus seven preview regression images; all synthetic. |
| `docs/Build2_Task2_Review.md` (new) | This handoff, relevant diffs, complete new source/test files and unchanged backend context. |

No migration is needed: `id`, `company`, `role`, `applied_on`, `created_at` remain
the complete API/model contract. There are no stages, users, status changes,
events, update/delete operations, Gmail, workers or other future-stage entities.
The approved PDF and Task 1 screenshots are unchanged.

## API and configuration decisions

The existing GET list envelope is `{items, limit, offset}`, with limit 1–100 and
offset 0–10,000, ordered by `created_at ASC, id ASC`. The UI chooses a fixed limit
of **20**, exposes Previous/Next, and does not infer a database-wide total. A full
last page can lead to an empty next page; the screen explains this and allows
returning. The offset cap is surfaced instead of silently continuing past the API
limit. URL offsets outside the supported numeric range receive a visible error.

Search is explicitly **“Search this loaded page”**, and counts distinguish shown
versus loaded records. Nothing fetches the whole database to simulate global
search. Real records use the approved Board/List layouts, with a neutral fallback
column in Board and no stage filter or assigned stage. The linked sample Board/List remains available separately.
Fixture stage wrappers never enter POST bodies, real query results or PostgreSQL.

`VITE_API_BASE_URL` is public browser configuration. Omission defaults to
`http://127.0.0.1:8000`; an explicitly invalid value produces a configuration error.
This local task accepts HTTP loopback origins, with no credentials, query string,
fragment or path. `frontend/.env.example` has a placeholder rather than secrets.
Users may create an ignored `frontend/.env.local` and replace the placeholder;
Vite must restart after changing it. No frontend local environment file was
created or copied by this task. Root `.env` was never printed or embedded; the
backend loaded its settings normally for connections.

CORS allows exactly localhost and 127.0.0.1 on frontend ports 5173 and 4173.
Only GET/POST are allowed; Content-Type supports JSON preflight. Credentials are
disabled both in FastAPI CORS and fetch (`credentials: 'omit'`). There is no
wildcard. This is a browser permission policy, **not** authentication. Both servers
remain loopback-only development services. No Vite proxy bypasses CORS verification.

TanStack Query **5.103.2** was selected after checking npm peer metadata
(`react: ^18 || ^19`) against installed React 19.3.0, Node 22.12.0 and npm 10.9.0.
Only this package and its matching query-core transitive dependency were added.
Installation reported **2 packages added, 171 audited, 0 vulnerabilities**;
`npm ls --depth=0` reports the pinned set with no invalid/missing dependencies.
Existing dependencies were not upgraded. The npm lockfile is updated.

Official references consulted:
[TanStack mutations](https://tanstack.com/query/latest/docs/framework/react/guides/mutations),
[query invalidation](https://tanstack.com/query/latest/docs/framework/react/guides/query-invalidation),
[FastAPI CORS](https://fastapi.tiangolo.com/tutorial/cors/), and
[Vite public environment variables](https://vite.dev/guide/env-and-mode).
The implementation uses mutations for creation and invalidation to refresh list
queries, as described by TanStack; Vite explicitly exposes `VITE_` values to the browser.

## One request, from form to persisted record

1. `ApplicationForm.submit` prevents native navigation, calls the existing
   `validateCreate` in `data.ts`, trims company/role, checks nonblank/200-character
   limits and a real YYYY-MM-DD date. Future dates remain allowed. Local failures
   keep values and focus the first invalid field without making a request.
2. A synchronous ref guard prevents a second submit before React's pending state
   renders. Fields become read-only, submission/cancel are disabled and the modal
   blocks closing while the POST is pending. `StoredApplications.add` awaits
   `mutation.mutateAsync(values)`. POST retries are explicitly disabled.
3. `api.createApplication` calls the shared `request('/applications', values)`.
   This is the actual plain-fetch implementation, not a separate demo: fetch
   combines the public API origin with the path, sends POST with
   `Content-Type: application/json` and `JSON.stringify(values)`, omits cookies,
   and waits for the response. A 15-second AbortSignal timeout bounds the wait.
   JSON is the textual object format crossing the network; awaiting a Promise
   lets the browser remain interactive while it waits.
4. FastAPI validates the body using `schemas.ApplicationCreate`; caller-supplied
   IDs/timestamps or other unexpected fields remain forbidden. The existing
   `applications.create_application` creates a `JobApplication` inside
   `database.session_scope`, flushes it and materializes the response. The ORM
   supplies the UUID and PostgreSQL supplies `created_at`. The session context
   must **commit successfully** before the route returns its 201 response.
5. The fetch client checks HTTP/JSON response handling and the five-field shape.
   The mutation receives the confirmed stored values. `StoredApplications.add`
   puts that record in its detail query cache, invalidates the list queries, and
   opens the returned detail URL. List refresh failure is a read error, not a
   failed creation. The new record is easy to retrieve directly even though
   oldest-first ordering may place it on a later list page.
6. Reload discards JavaScript memory. The detail route issues a new GET through
   `getApplication`; `applications.get_application` reads the UUID from the
   database and returns the stored fields. The real integration test and its
   independent SQLAlchemy read verify this path.

**Failure path:** a server 422 is mapped in `api.validationFields` using only
recognized field names and error types. Raw server messages, input echoes and
exception details are never rendered or logged by the client. The form retains
its values, displays associated field errors and does not show success. A network,
timeout or server error after POST instead says creation could not be confirmed
and **may have been saved**. It tells the user to check the list before submitting
again. No automatic resend can create a duplicate. Duplicate applications are
still a valid API feature, so no client uniqueness restriction was invented.

Read failures show generic messages and explicit retry controls; no sample
fallback exists. A valid missing UUID shows not-found; a malformed UUID is
identified locally and is not sent as a detail query. Unexpected successful
response shapes are treated as failures, not trusted as applications.

## Integration verification before the Board correction (historical)

All results below were independently executed by Codex in this task. They are
separate from historical Task 1 results and Sanjay's reported preview check.

| Command/check | Observed result |
| --- | --- |
| `npm.cmd install --save-exact @tanstack/react-query@5.103.2` in `frontend/` | Exit 0; 2 added, 171 audited, zero vulnerabilities. |
| `npm.cmd run typecheck` | Exit 0, no TypeScript errors. The final build repeats this check. |
| `npm.cmd run build` | Exit 0; 1954 modules, final build 2.66s; JS 328.51 kB / gzip 103.64, CSS 20.29 kB / gzip 5.43. Includes neutral browser title. |
| `npm.cmd run test` | **18 passed**, four files, 3.80s. Includes existing nine preview/data checks and nine new API/component checks. |
| `npm.cmd run test:e2e` | **8 passed**, 9.8s. Five preserved preview behaviors plus three mocked real-data browser scenarios. Real Chromium against the production preview server. |
| `.\.venv\Scripts\python.exe -m pytest --run-db -q` from root | **63 passed**, 7.06s. Existing 57 regressions plus six CORS checks; dedicated test DB only for automated writes. |
| `.\.venv\Scripts\python.exe -m scripts.run_frontend_integration` | **1 real browser test passed**, 7.0s. Separately printed PASS for independent committed-row verification and scoped test cleanup. |
| `npm.cmd ls --depth=0` | Exit 0; all direct dependencies installed at pinned versions, including Query 5.103.2. |
| `git diff --check` | No whitespace errors; only normal LF/CRLF conversion notices. |
| `git diff --exit-code -- migrations schemas.py applications.py database.py config.py models.py requirements.txt` | Exit 0, these contracts/persistence files are unchanged. |
| Development server health and read-only list GET | Both HTTP 200; health healthy; list response includes `Access-Control-Allow-Origin: http://127.0.0.1:5173`. No development record values printed, no automated development write. |
| Frontend HTTP on 5173 | HTTP 200; existing correct frontend reused. |
| Live GitHub main check | Matches base `f4815f27fd36609d185e542338df3b4b131cc186`; no task commit/push. |
| Final packaging checks | Manifest and lockfile dependency groups match. Bounded private-key/token/database-URL scan found no matches. `.env` remains ignored and untracked; generated dependencies/build/test output remain ignored. Source package contains 27 file fingerprints, 12 complete new files and four unchanged backend context files. |

The component tests use jsdom and mocked fetch, and do **not** prove database
persistence or native browser behavior. The eight ordinary Playwright checks use
a real browser but mock stored-data failures. The separate integration suite uses
actual cross-origin fetch, FastAPI, SQLAlchemy and PostgreSQL, with no API mocking.

The real test verifies 20-record paging followed by a nonempty second page,
loaded-page search, normalized creation values, generated fields, POST 201,
the browser-origin CORS response header, list-query refresh, direct detail and
reload, missing/malformed IDs, mobile containment and complete preview-write
separation. There is exactly one real browser POST in that flow. The backend
regressions additionally prove invalid input, duplicate applications, constraint
rollback, failed-commit privacy, health/unknown routes and persistence across
separate Uvicorn processes. PostgreSQL itself is never restarted.

### Data isolation and cleanup

`run_frontend_integration.verify_target` checks `current_database()`, `current_user`
and Alembic revision: **applysync_test**, **applysync_test**, **0001**. The child
API repeats verification and uses `create_app('test')`. No admin role is used.
Twenty-one fixtures receive a fresh UUID-bearing run marker and an old synthetic
creation timestamp to exercise paging without altering any existing record.

The browser-created company has that same unique run prefix. After tests, the
runner independently reads its normalized values in PostgreSQL. It terminates only
the Uvicorn child it owns; Playwright owns its temporary Vite process. Before
cleanup it repeats target verification, deletes **only that unique company-prefix
set**, and confirms zero records with that prefix remain. Cleanup also covers
lost POST responses and failed tests. No development record or unrelated database
is changed. There is no clearing, reseeding, migration or schema recreation.

### Failures encountered and resolved

- One npm command was initially issued from the repository root and returned
  ENOENT (there is no root package.json); it was rerun from `frontend/`.
- TypeScript caught an unsafe index inferred from untrusted validation JSON; the
  field is now `unknown` until narrowed to supported names.
- A test incorrectly interpreted the mobile “Applied [date]” caption as a stage.
  It now asserts absence of stage badges and checks the real-data labels.
- Initial real-browser attempts failed. The runner originally hid child output
  on Windows; safe phase/category diagnostics and captured browser output made
  the cause visible. An encoding-damaged preview separator and an unchanged
  sidebar preview label were corrected. A subsequent form selector was narrowed
  to its dialog so it could not match the page's search field. The final full
  integration flow passed, with scoped cleanup confirmed after every attempt.
- Browser output includes harmless NO_COLOR/FORCE_COLOR warnings. No final check
  is failed or blocked. No final test was skipped.

### Visual evidence and limits

Actual rendered desktop/mobile integrated screenshots were inspected, including
long synthetic company names, pagination, stage-free list and the detail panel.
The final preview regression images preserve the light/purple/pastel visual design.
Task 1's original evidence is retained unchanged.

- [Stored desktop list](screenshots/Build2_Task2/stored-list.png)
- [Stored desktop detail](screenshots/Build2_Task2/stored-detail.png)
- [Stored mobile list](screenshots/Build2_Task2/stored-mobile-list.png)
- [Stored mobile detail](screenshots/Build2_Task2/stored-mobile-detail.png)
- [Preview board](screenshots/Build2_Task2/preview/desktop-board.png)
- [Preview mobile list](screenshots/Build2_Task2/preview/mobile-list.png)

Only Chromium was tested; Firefox/WebKit, physical phone devices and screen readers
remain unrun. There is no full accessibility certification, deployment test or
authentication/ownership check. Network/server/validation failures are simulated
in frontend tests; real PostgreSQL failure behavior is also covered by existing
backend tests. No production services or real Gmail data are involved.

## Opening the interface and learning checkpoint

At handoff the existing frontend remains available at
http://127.0.0.1:5173/applications, and a development Uvicorn process was started
on http://127.0.0.1:8000 (process 3360). Test-only servers were stopped. The API
was checked read-only; no development application was created on Sanjay's behalf.
For later sessions, README contains exact Windows commands for both terminals,
safe configuration, dependencies, Chromium installation and all test suites.

Manual check for Sanjay: create one fictional development application, note its
generated detail URL, reload that URL and confirm its company, role and applied
date remain. The API has no delete endpoint; automated cleanup will not remove
this deliberately created development record.

Focused learning checkpoint: while making that request, open browser Network
tools and identify the POST's three supplied fields, the returned generated
fields, and the GET after reload. Locate `ApplicationForm.submit`, `request` in
`api.ts`, `applications.create_application`, `session_scope` and
`StoredApplications.add`. Explain why the success message waits for the response.
This exercise is suggested, **not marked completed**.

The three state concepts are distinct:

- **Form state:** temporary typed values and errors, retained after a failed
  submission but lost when the form/browser is discarded.
- **TanStack Query cache:** temporary browser memory of server results; keys
  distinguish list pages and IDs, and invalidation refreshes stale lists. It is
  not durable storage and is not shared with the sample fixture array.
- **PostgreSQL:** committed records that survive browser reload and application
  restart. A cache update alone does not establish persistence; successful commit
  and later independent retrieval do.

## Build 2 exit criteria and Planning & Progress

Implementation evidence now covers UI creation/retrieval/reload against a real
database, list refresh, clear validation/failure states, responsive interactions
and retained backend checks. The approved shell and reusable preview Board remain.
There is no authoritative stage system or backend global search; these are explicit
scope limitations, not invented frontend functionality.

Build 2 as a whole is **still in progress**: Sanjay reports his integrated
create/reload check succeeded, while explanation of one component/request path and
focused investigation/change remain pending; a reviewed working commit is also pending and not authorized in this
task. Earlier transaction/request-flow learning items carry forward. No separate
dashboard statistics or unsupported server totals were introduced; the loaded-page
summary is the current bounded display. Stage review must confirm any remaining
dashboard requirement before declaring the whole stage complete. Authentication
belongs to Build 3 and has not begun.

Git handoff: all listed changes are unstaged, new source/tests/screenshots/review
are untracked, and HEAD remains the base commit. Existing ignore rules keep `.env`,
environments, `node_modules`, `dist`, browser traces/results and caches out of Git.
The new `.env.example` is intentional public placeholder configuration. No secret
contents or database connection URLs are in this package.

## Code review appendix

Below are relevant tracked diffs (including the small lockfile delta), complete new
source/test/configuration files, and unchanged schema/route/transaction context.
Generated dependencies, binary screenshots and this document itself are not
embedded. File fingerprints identify the exact reviewed implementation.

<!-- BEGIN SOURCE SNAPSHOT -->

### Fingerprints

| File | SHA-256 |
| --- | --- |
| `README.md` | `b0f86557621013ce4204b62793b7e684f74029b1c3bfb0649ca417571856790f` |
| `frontend/.env.example` | `0a77d8e776293d9eb51835bcf69a57fc0b2407573f8de5afa34575e5f0a3e098` |
| `frontend/e2e/integration.spec.ts` | `5cb3a141f6b1f837765b111a22a99be1b64bf5633fe5fe78ae9fbbaa32c173de` |
| `frontend/e2e/preview.spec.ts` | `ebde55e04ad905fb4b80f87290765c27b6209e2d26b181cfd55e5c56e931e92c` |
| `frontend/e2e/stored.spec.ts` | `e0964601930567c1453991bc4d9521eb94e213d5c0bafda58f36f9304843db43` |
| `frontend/index.html` | `e02afae43f921630ea780a3621c69a92ba985ecad3b3dd7bddee1b09df13a13b` |
| `frontend/package-lock.json` | `cbdb2ce4ee5245602d40f4ca6772474326c247b9d6a6c6a93f3b3dcd3f7a355b` |
| `frontend/package.json` | `74001cb427abce4265b47ddcd798e3533e6cf128e55b04e660a5c02a8fa7d16c` |
| `frontend/playwright.config.ts` | `c8915e602ecc1cd6f8a300fc0ceb3cde84e0757de0aed02562f96f085131aa32` |
| `frontend/playwright.integration.config.ts` | `268e32fee5d733da6105e65d51e8b0c61ab108a0ab8d1341b7598a910d18c912` |
| `frontend/src/App.test.tsx` | `83dcabd1ae8cec4087f8788c89e30b258acb7c935c2186773d55425f21a84c72` |
| `frontend/src/App.tsx` | `b098731506466bb2308407f354397b94a7ee9e432e5ee68c242fc0cb814bb9b5` |
| `frontend/src/PreviewApplications.tsx` | `a51dec105a9b8e940abc1964c2f2bfd894ef0ccad2d844a193c9c096daed1cce` |
| `frontend/src/StoredApplications.test.tsx` | `782c4899733368257d1163930d7ef63e0a226c7b022bab6cc5e5cb30a5b3145b` |
| `frontend/src/StoredApplications.tsx` | `864ed6c4e84772d055234b92d9dc9b953c22eed380a5e62f825324adb50da63b` |
| `frontend/src/api.test.ts` | `9f3f62bfb0a7f38fc9efe1ed0126610d6012a11ff860008225c69bc82b0e17c2` |
| `frontend/src/api.ts` | `c9121c3401f8cbcfafb3764cc37a49ae3a4a256e20b26da3261297c3753b3048` |
| `frontend/src/components/ApplicationForm.tsx` | `209bc3e56ee2379e2f97d48396600952abdd2478e2051661b1f3b97c97df8c0f` |
| `frontend/src/components/ApplicationsView.tsx` | `9bb46dde3dd64ef7e5e9f503e6a3f9fcdaa24df8b4773405ee5d438e34deda9f` |
| `frontend/src/components/Shell.tsx` | `1f0ab3812cbac8e46f0db0fe45becea744c96ee92892e8573bc1705f97030c8f` |
| `frontend/src/components/ui.tsx` | `70c1ade6f55a77334b7c47e75fdf07377773b54700ff7c7af6063f50a872e2b4` |
| `frontend/src/query.ts` | `fcadcf16727ca46cbc975208583886e981c81f0374509f0de78b2d253bc27b82` |
| `frontend/src/styles.css` | `6d46d464bfd7459397f88391a346f0b33f6cbd693264df207fe9b9a79eb8af0c` |
| `frontend/tsconfig.json` | `b684f361e12b2b595b310e1d17bae273151402787defcfaf278134f21dd88d3b` |
| `main.py` | `3935e778530a6b5995399388aa17fad681ba7b96648a32c3cc5e046a222355df` |
| `scripts/run_frontend_integration.py` | `3ba82e50ebbfc01f2cb3b7a57857fae545fffc028784b5aced4856b07a128c5c` |
| `tests/test_cors.py` | `da6391d2cd5e5446f48057a10e14eb48d129cea7d3616ae778fcc74f757957b9` |

### Tracked changes

```diff
diff --git a/README.md b/README.md
index 9e7caba..b1286a0 100644
--- a/README.md
+++ b/README.md
@@ -1,10 +1,93 @@
 # applysync
 AI-powered privacy-first job application tracker that automatically syncs Gmail application emails into a Kanban dashboard.

-Current scope: Build 2, task 1 adds an interactive frontend **design preview** with
-synthetic, in-memory applications. The existing Build 1 create/list/detail APIs and
-`GET /health` remain unchanged. The preview does not call them. Gmail and automatic
-tracking above describe the project goal, not implemented features.
+Current scope: Build 2, task 2 connects the approved frontend to the PostgreSQL
+create/list/detail APIs. `/applications` displays stored data; the explicitly separate
+`/preview/applications` retains the fictional Board/List preview. Gmail and automatic
+tracking above describe the project goal, not implemented features. This is local,
+unauthenticated development functionality, not a public deployment.
+
+## Integrated interface (two PowerShell terminals)
+
+Use the existing backend `.venv`, provisioned local databases and ignored root
+`.env`. Do not reprovision or replace existing credentials. For a fresh machine,
+follow the backend setup below first. Terminal 1, from the repository root:
+
+```powershell
+Set-Location 'C:\Users\sanja\Desktop\ApplySync'
+.\.venv\Scripts\python.exe -m uvicorn main:app --host 127.0.0.1 --port 8000
+```
+
+Terminal 2, from `frontend/`:
+
+```powershell
+Set-Location 'C:\Users\sanja\Desktop\ApplySync\frontend'
+npm.cmd ci
+npm.cmd run dev
+```
+
+Open **http://127.0.0.1:5173/applications**. Backend health is
+http://127.0.0.1:8000/health and Swagger is http://127.0.0.1:8000/docs.
+Stop your own servers with Ctrl+C; reuse existing correct servers rather than
+starting duplicates. Restart an older backend process to load the new CORS policy.
+
+The public `VITE_API_BASE_URL` defaults to `http://127.0.0.1:8000`. To configure a
+different local port, copy `frontend/.env.example` to `frontend/.env.local` **only
+if that local file does not already exist**, replace its placeholder with your
+local API origin (for example `http://127.0.0.1:8000`), and restart Vite. This
+variable is browser-visible and must contain no credentials, token, query string
+or database URL. Root backend `.env` is separate and must never be copied into
+the frontend. The client accepts local HTTP origins only for this task.
+
+FastAPI allows exactly `http://localhost:5173`, `http://127.0.0.1:5173`,
+`http://localhost:4173` and `http://127.0.0.1:4173`, with GET/POST and Content-Type.
+There is no wildcard or credential support. CORS permits browser cross-origin
+reads; it is not authentication or ownership protection.
+
+Stored records share Board/List views (List is the default). The Board uses one
+neutral **Stage not recorded** column and explains that grouping will be available
+when stage tracking exists. This heading is only a display fallback; no stage is
+assigned or saved. Switching views retains loaded-page search and pagination.
+Pages contain at most
+20 records, ordered by `created_at ASC, id ASC`. Previous/Next controls use the
+existing offset contract, up to 10,000. A full last page may lead to an empty next
+page because the API has no total/has-more field. Counts describe the loaded page,
+not the database total. Search explicitly covers **only the loaded page**. No
+whole-database fetch or global search is implemented.
+
+Creation trims/validates text and dates, disables repeat submission while saving,
+and shows success only after a confirmed response. It refreshes list queries and
+opens the returned record's detail URL; reload performs a real detail GET. Since
+the list is oldest-first, the new record may be on a later page. Read failures
+have retry controls. Failed creation retains input; uncertain network/server
+outcomes instruct you to check the list before resubmitting. POST is never retried
+automatically. Duplicate company/role applications remain allowed.
+
+The client uses TanStack Query 5.103.2 with the shared `src/api.ts` fetch client.
+See [Build 2 Task 2 review](docs/Build2_Task2_Review.md) for code, checks and limitations.
+
+From the repository root, run backend regression checks and the guarded real
+browser integration check (existing migrated **test** database required):
+
+```powershell
+Set-Location 'C:\Users\sanja\Desktop\ApplySync'
+.\.venv\Scripts\python.exe -m pytest --run-db -q
+.\.venv\Scripts\python.exe -m scripts.run_frontend_integration
+```
+
+Install frontend dependencies and Chromium using the commands below first. Keep
+port 4173 free. The integration runner verifies test database/role/revision,
+inserts 21 uniquely marked synthetic fixtures, starts its own test API on a free
+loopback port and a temporary frontend on 4173, and runs real cross-origin browser
+create/read/reload checks. It independently verifies the committed row in
+PostgreSQL, stops only its own servers, rechecks the database target, and removes
+only its own marked records. It neither clears development data nor runs DDL.
+Do not invoke `npm run test:integration` directly against an arbitrary backend;
+the Python runner supplies its guarded target and run marker.
+
+Manual check: add one fictional development application, note its generated
+detail URL, reload that page and verify the record remains. This is a deliberate
+development record; automated checks do not remove it. The API has no delete endpoint.

 ## Frontend design preview (no backend required)

@@ -18,7 +101,7 @@ npm.cmd ci
 npm.cmd run dev
 ```

-Open **http://127.0.0.1:5173/applications**. Stop with Ctrl+C. Port 5173 is fixed;
+Open **http://127.0.0.1:5173/preview/applications**. Stop with Ctrl+C. Port 5173 is fixed;
 if it is occupied, stop your previous frontend server first. The backend server and
 PostgreSQL are not needed for this preview. Do not copy backend secrets into frontend
 environment files; browser-visible configuration cannot protect credentials.
@@ -35,7 +118,9 @@ a new-record detail URL after reload shows a clear missing-preview-record messag
 Search/filter/view selections live in URL query parameters, not browser storage.
 Sample stages live outside the API-shaped `Application` type. There is no backend
 stage contract, drag-and-drop, API request, local/session storage, authentication,
-remote logo request, or persistent save. Backend integration is the next task.
+remote logo request, or persistent save **on this preview route**. The normal
+Applications route uses the real API independently. Leaving the preview also
+unmounts its temporary fixture state.

 The interface follows the three supplied `docs/design.pdf` screenshots with a white
 sidebar/cards, cool-gray workspace, purple actions, pastel board headers and restrained
@@ -55,10 +140,12 @@ npm.cmd run test:e2e
 ```

 Browser tests use a temporary production preview server on port 4173 and save
-screenshots under `docs/screenshots/Build2_Task1/`. Keep that port free. Tests cover
+screenshots under `docs/screenshots/Build2_Task2/`. Keep that port free. Tests cover
 search/filter/view state, validation, preview creation/reset, route-backed details,
 keyboard handling, reduced motion and desktop/mobile layouts. Native dialog behaviour
 is tested in Chromium; the component-test DOM only supplies a minimal dialog stub.
+`test:e2e` includes mocked real-data failure checks and preview regressions; the
+separate guarded Python runner above proves the actual database integration.

 See [Build 2 Task 1 review](docs/Build2_Task1_Review.md) for evidence, reference
 comparisons, dependency choices, screenshots, limitations and a learning walkthrough.
diff --git a/frontend/e2e/preview.spec.ts b/frontend/e2e/preview.spec.ts
index 476ea1c..64b326b 100644
--- a/frontend/e2e/preview.spec.ts
+++ b/frontend/e2e/preview.spec.ts
@@ -1,11 +1,11 @@
 import { expect, test } from '@playwright/test'
 import { mkdirSync } from 'node:fs'

-const screenshots = '../docs/screenshots/Build2_Task1'
+const screenshots = '../docs/screenshots/Build2_Task2/preview'
 mkdirSync(screenshots, { recursive: true })

 test('intermediate viewport widths keep controls inside the page', async ({ page }) => {
-  await page.goto('/applications')
+  await page.goto('/preview/applications')
   for (const width of [320, 768, 860, 900, 1280]) {
     await page.setViewportSize({ width, height: 900 })
     expect(await page.evaluate(() => document.documentElement.scrollWidth <= window.innerWidth), `page overflow at ${width}px`).toBe(true)
@@ -15,7 +15,7 @@ test('intermediate viewport widths keep controls inside the page', async ({ page
 test('desktop reference layout, shared filtering, details and focus return', async ({ page }) => {
   const failures: string[] = []
   page.on('pageerror', error => failures.push(error.message))
-  await page.goto('/applications')
+  await page.goto('/preview/applications')
   await expect(page.getByRole('link', { name: 'Product Designer at Cedar & Finch' })).toBeVisible()
   await expect(page.getByRole('region', { name: 'Offer, 0 applications' })).toContainText('No applications here')
   expect(await page.evaluate(() => document.documentElement.scrollWidth <= window.innerWidth)).toBe(true)
@@ -51,7 +51,7 @@ test('preview validation, add, reload reset and no data requests', async ({ page
   page.on('request', request => {
     if (['fetch', 'xhr'].includes(request.resourceType())) dataRequests.push(request.url())
   })
-  await page.goto('/applications')
+  await page.goto('/preview/applications')
   const trigger = page.getByRole('link', { name: 'Add application', exact: true })
   await trigger.click()
   const dialog = page.getByRole('dialog')
@@ -80,7 +80,7 @@ test('preview validation, add, reload reset and no data requests', async ({ page

 test('mobile navigation, contained board, stacked list and full-screen details', async ({ page }) => {
   await page.setViewportSize({ width: 390, height: 844 })
-  await page.goto('/applications')
+  await page.goto('/preview/applications')
   expect(await page.evaluate(() => document.documentElement.scrollWidth <= window.innerWidth)).toBe(true)
   const board = page.getByRole('region', { name: /Application board/ })
   expect(await board.evaluate(element => element.scrollWidth > element.clientWidth)).toBe(true)
@@ -105,7 +105,7 @@ test('mobile navigation, contained board, stacked list and full-screen details',
 test('reduced motion and board scroll position survive opening a detail', async ({ page }) => {
   await page.emulateMedia({ reducedMotion: 'reduce' })
   await page.setViewportSize({ width: 1100, height: 850 })
-  await page.goto('/applications')
+  await page.goto('/preview/applications')
   const board = page.getByRole('region', { name: /Application board/ })
   await board.evaluate(element => { element.scrollLeft = element.scrollWidth })
   const before = await board.evaluate(element => element.scrollLeft)
diff --git a/frontend/index.html b/frontend/index.html
index dd436ac..eafb0c0 100644
--- a/frontend/index.html
+++ b/frontend/index.html
@@ -4,7 +4,7 @@
     <meta charset="UTF-8" />
     <meta name="viewport" content="width=device-width, initial-scale=1.0" />
     <meta name="theme-color" content="#5145e5" />
-    <title>Applications · ApplySync preview</title>
+    <title>Applications · ApplySync</title>
     <link rel="icon" type="image/svg+xml" href="/mark.svg" />
   </head>
   <body><div id="root"></div><script type="module" src="/src/main.tsx"></script></body>
diff --git a/frontend/package-lock.json b/frontend/package-lock.json
index fa1b8b8..a7c2501 100644
--- a/frontend/package-lock.json
+++ b/frontend/package-lock.json
@@ -8,6 +8,7 @@
       "name": "applysync-preview",
       "version": "0.1.0",
       "dependencies": {
+        "@tanstack/react-query": "5.103.2",
         "lucide-react": "1.47.0",
         "react": "19.3.0",
         "react-dom": "19.3.0",
@@ -1622,6 +1623,32 @@
         "vite": "^5.2.0 || ^6 || ^7 || ^8"
       }
     },
+    "node_modules/@tanstack/query-core": {
+      "version": "5.103.2",
+      "resolved": "https://registry.npmjs.org/@tanstack/query-core/-/query-core-5.103.2.tgz",
+      "integrity": "sha512-I8DkFXls5jXLqtm8+QpOhEmG07hIblhSZFzafg9wHsMSEvMzULy9hK17wU1T/ahfhMbtITJhbxutwwCoihkR7A==",
+      "license": "MIT",
+      "funding": {
+        "type": "github",
+        "url": "https://github.com/sponsors/tannerlinsley"
+      }
+    },
+    "node_modules/@tanstack/react-query": {
+      "version": "5.103.2",
+      "resolved": "https://registry.npmjs.org/@tanstack/react-query/-/react-query-5.103.2.tgz",
+      "integrity": "sha512-B+fWiYZBc+0uUD5zDZAeLw9dKj7XEsdnuu6zRZ+no6LNKpeE3P3bJ+N6HINjcIlWR6fW3vUoTneEaGa2V6ehqw==",
+      "license": "MIT",
+      "dependencies": {
+        "@tanstack/query-core": "5.103.2"
+      },
+      "funding": {
+        "type": "github",
+        "url": "https://github.com/sponsors/tannerlinsley"
+      },
+      "peerDependencies": {
+        "react": "^18 || ^19"
+      }
+    },
     "node_modules/@testing-library/dom": {
       "version": "10.4.2",
       "resolved": "https://registry.npmjs.org/@testing-library/dom/-/dom-10.4.2.tgz",
diff --git a/frontend/package.json b/frontend/package.json
index 28cee0d..7b32432 100644
--- a/frontend/package.json
+++ b/frontend/package.json
@@ -12,9 +12,11 @@
     "build": "npm run typecheck && vite build",
     "preview": "vite preview --host 127.0.0.1",
     "test": "vitest run",
-    "test:e2e": "playwright test"
+    "test:e2e": "playwright test",
+    "test:integration": "playwright test --config playwright.integration.config.ts"
   },
   "dependencies": {
+    "@tanstack/react-query": "5.103.2",
     "lucide-react": "1.47.0",
     "react": "19.3.0",
     "react-dom": "19.3.0",
diff --git a/frontend/playwright.config.ts b/frontend/playwright.config.ts
index 6d66471..2d9bbed 100644
--- a/frontend/playwright.config.ts
+++ b/frontend/playwright.config.ts
@@ -1,7 +1,7 @@
 import { defineConfig } from '@playwright/test'

 export default defineConfig({
-  testDir: './e2e', fullyParallel: false, workers: 1, reporter: 'list',
+  testDir: './e2e', testIgnore: '**/integration.spec.ts', fullyParallel: false, workers: 1, reporter: 'list',
   use: { baseURL: 'http://127.0.0.1:4173', browserName: 'chromium', viewport: { width: 1600, height: 1000 }, trace: 'retain-on-failure' },
   webServer: { command: 'npm run preview -- --port 4173 --strictPort', url: 'http://127.0.0.1:4173', reuseExistingServer: false },
 })
diff --git a/frontend/src/App.test.tsx b/frontend/src/App.test.tsx
index 28ea7c8..e8d6ab6 100644
--- a/frontend/src/App.test.tsx
+++ b/frontend/src/App.test.tsx
@@ -4,7 +4,7 @@ import { MemoryRouter } from 'react-router'
 import { expect, it } from 'vitest'
 import { App } from './App'

-function setup(path = '/applications', empty = false) {
+function setup(path = '/preview/applications', empty = false) {
   const user = userEvent.setup()
   render(<MemoryRouter initialEntries={[path]}><App initialRecords={empty ? [] : undefined} /></MemoryRouter>)
   return user
@@ -46,7 +46,7 @@ it('preserves input on validation errors and adds a trimmed preview record to bo
   expect(screen.getByRole('link', { name: 'Engineer at Preview Company' })).toBeInTheDocument()
 })
 it('opens route-backed detail and returns without losing search', async () => {
-  const user = setup('/applications?q=cedar&view=list')
+  const user = setup('/preview/applications?q=cedar&view=list')
   await user.click(screen.getByRole('link', { name: 'Product Designer at Cedar & Finch' }))
   expect(screen.getByRole('dialog')).toHaveTextContent('Application overview')
   expect(screen.getByRole('dialog')).toHaveTextContent('21 Sept 2026')
@@ -55,7 +55,7 @@ it('opens route-backed detail and returns without losing search', async () => {
   expect(screen.getByRole('searchbox')).toHaveValue('cedar')
 })
 it('supports an empty dataset and direct missing-record routes', () => {
-  setup('/applications/missing', true)
+  setup('/preview/applications/missing', true)
   expect(screen.getByText('Your next chapter starts here')).toBeInTheDocument()
   expect(screen.getByRole('dialog')).toHaveTextContent('Application not found')
 })
diff --git a/frontend/src/App.tsx b/frontend/src/App.tsx
index 68f5743..ad1a4d4 100644
--- a/frontend/src/App.tsx
+++ b/frontend/src/App.tsx
@@ -1,66 +1,17 @@
+import { Navigate, Route, Routes } from 'react-router'
+import { QueryClientProvider } from '@tanstack/react-query'
 import { useState } from 'react'
-import { Link, Navigate, useLocation, useNavigate, useParams, useSearchParams, Route, Routes } from 'react-router'
-import { ArrowLeft, CalendarDays, Columns3, List, Plus, Search, SearchX, SlidersHorizontal } from 'lucide-react'
 import { Shell } from './components/Shell'
-import { Board, ApplicationList, CompanyMark } from './components/ApplicationsView'
-import { Button, Modal, PreviewNotice, StageLabel } from './components/ui'
-import { ApplicationForm } from './components/ApplicationForm'
-import { filterApplications, formatDate, sampleApplications, stages, type CreateValues, type PreviewApplication } from './data'
+import { PreviewApplications } from './PreviewApplications'
+import { StoredApplications } from './StoredApplications'
+import { makeQueryClient } from './query'
+import type { PreviewApplication } from './data'

-function Applications({ initialRecords = sampleApplications }: { initialRecords?: PreviewApplication[] }) {
-  const [records, setRecords] = useState(initialRecords)
-  const [feedback, setFeedback] = useState('')
-  const [params, setParams] = useSearchParams()
-  const location = useLocation()
-  const navigate = useNavigate()
-  const { id } = useParams()
-  const search = params.get('q') ?? ''
-  const selectedStage = stages.find(stage => stage === params.get('stage')) ?? 'All stages'
-  const view = params.get('view') === 'list' ? 'list' : 'board'
-  const filtered = filterApplications(records, search, selectedStage)
-  const selected = records.find(record => record.application.id === id)
-  const isNew = id === 'new'
-  const close = () => navigate(`/applications${location.search}`, { replace: true })
-  function setSelection(key: string, value: string) {
-    setParams(current => {
-      const next = new URLSearchParams(current)
-      value ? next.set(key, value) : next.delete(key)
-      return next
-    }, { replace: true })
-  }
-  function add(values: CreateValues) {
-    setRecords(current => [{ application: { ...values, id: crypto.randomUUID(), created_at: new Date().toISOString() }, sampleStage: 'Applied' }, ...current])
-    setFeedback(`${values.company} added to the preview. Reloading removes this addition.`)
-    close()
-  }
-  return <>
-    <div className="page-heading"><div><p className="eyebrow">YOUR NEXT CHAPTER</p><h1>Applications</h1><p className="page-description">A clear view of every opportunity, from first step to next move.</p></div>
-      <Link id="add-application" className="button button-primary" to={`/applications/new${location.search}`}><Plus size={18} />Add application</Link>
-    </div>
-    <div className="applications-workspace">
-      <div className="toolbar">
-        <div className="view-switch" role="group" aria-label="Application view"><button aria-pressed={view === 'board'} onClick={() => setSelection('view', '')}><Columns3 size={17} />Board</button><button aria-pressed={view === 'list'} onClick={() => setSelection('view', 'list')}><List size={18} />List</button></div>
-        <div className="filter-controls"><div className="search-field"><Search size={18} /><label className="sr-only" htmlFor="search">Search company or role</label><input id="search" type="search" placeholder="Search company or role…" value={search} onChange={event => setSelection('q', event.target.value)} /></div>
-          <div className="stage-filter"><SlidersHorizontal size={16} /><label className="sr-only" htmlFor="stage-filter">Sample stage</label><select id="stage-filter" value={selectedStage} onChange={event => setSelection('stage', event.target.value === 'All stages' ? '' : event.target.value)}><option>All stages</option>{stages.map(stage => <option key={stage}>{stage}</option>)}</select></div>
-        </div>
-      </div>
-      <div className="results-meta"><p aria-live="polite"><strong>{filtered.length}</strong> of {records.length} applications</p><span>Stages are for this preview only</span></div>
-      {feedback && <div className="success-note" role="status"><span>{feedback}{(search || selectedStage !== 'All stages') && ' Your current filters may hide it.'}</span><Button variant="quiet" onClick={() => setFeedback('')}>Dismiss</Button></div>}
-      {!filtered.length ? <div className="empty-state"><SearchX size={28} /><h2>{records.length ? 'No matching applications' : 'Your next chapter starts here'}</h2><p>{records.length ? 'Try a different company, role, or sample stage.' : 'Add an application to explore your preview.'}</p>
-        {records.length ? <Button onClick={() => setParams(view === 'list' ? { view: 'list' } : {}, { replace: true })}>Clear search & filter</Button> : <Link className="button button-primary" to={`/applications/new${location.search}`}>Add application</Link>}
-      </div> : view === 'board' ? <Board records={filtered} search={location.search} /> : <ApplicationList records={filtered} search={location.search} />}
-      <footer className="workspace-footer"><span>Small steps. New possibilities.</span><span>Preview additions reset on reload.</span></footer>
-    </div>
-    {id && <Modal title={isNew ? 'Add application' : selected?.application.role ?? 'Application not found'} subtitle={isNew ? 'Make room for your next opportunity.' : selected?.application.company} variant={isNew ? 'form' : 'panel'} onClose={close}>
-      {isNew ? <ApplicationForm onAdd={add} onClose={close} /> : selected ? <div className="detail-body">
-        <div className="detail-identity"><CompanyMark company={selected.application.company} /><div><span className="eyebrow">COMPANY</span><strong>{selected.application.company}</strong></div></div>
-        <h3>Application overview</h3><dl className="detail-facts"><div><dt><CalendarDays size={16} />Applied date</dt><dd>{formatDate(selected.application.applied_on)}</dd></div><div><dt>Sample stage</dt><dd><StageLabel stage={selected.sampleStage} /></dd></div></dl>
-        <div className="detail-preview"><PreviewNotice /><p>This is a fictional application. Stages help you explore the layout; they are not saved application history.</p></div>
-        <Button onClick={close}><ArrowLeft size={17} />Back to applications</Button>
-      </div> : <div className="detail-body"><p>This preview record is unavailable. Preview additions disappear on reload.</p><Button onClick={close}>Back to applications</Button></div>}
-    </Modal>}
-  </>
-}
 export function App({ initialRecords }: { initialRecords?: PreviewApplication[] }) {
-  return <Shell><Routes><Route path="/applications/:id?" element={<Applications initialRecords={initialRecords} />} /><Route path="*" element={<Navigate to="/applications" replace />} /></Routes></Shell>
+  const [client] = useState(makeQueryClient)
+  return <QueryClientProvider client={client}><Shell><Routes>
+    <Route path="/applications/:id?" element={<StoredApplications />} />
+    <Route path="/preview/applications/:id?" element={<PreviewApplications initialRecords={initialRecords} />} />
+    <Route path="*" element={<Navigate to="/applications" replace />} />
+  </Routes></Shell></QueryClientProvider>
 }
diff --git a/frontend/src/components/ApplicationForm.tsx b/frontend/src/components/ApplicationForm.tsx
index 5a2399a..e1c6abf 100644
--- a/frontend/src/components/ApplicationForm.tsx
+++ b/frontend/src/components/ApplicationForm.tsx
@@ -1,13 +1,19 @@
-import { useState, type FormEvent } from 'react'
+import { useRef, useState, type FormEvent } from 'react'
+import { ApiError, errorMessage } from '../api'
 import { Info, Plus } from 'lucide-react'
 import { validateCreate, type CreateValues } from '../data'
 import { Button } from './ui'

-export function ApplicationForm({ onAdd, onClose }: { onAdd: (values: CreateValues) => void; onClose: () => void }) {
+export function ApplicationForm({ onAdd, onClose, mode = 'preview' }: { onAdd: (values: CreateValues) => void | Promise<void>; onClose: () => void; mode?: 'preview' | 'stored' }) {
   const [values, setValues] = useState<CreateValues>({ company: '', role: '', applied_on: '' })
   const [errors, setErrors] = useState<Partial<Record<keyof CreateValues, string>>>({})
-  function submit(event: FormEvent<HTMLFormElement>) {
+  const lock = useRef(false)
+  const [pending, setPending] = useState(false)
+  const [failure, setFailure] = useState('')
+  async function submit(event: FormEvent<HTMLFormElement>) {
     event.preventDefault()
+    if (lock.current) return
+    const form = event.currentTarget
     const result = validateCreate(values)
     setErrors(result.errors)
     if (Object.keys(result.errors).length) {
@@ -15,22 +21,34 @@ export function ApplicationForm({ onAdd, onClose }: { onAdd: (values: CreateValu
       event.currentTarget.querySelector<HTMLInputElement>(`[name="${first}"]`)?.focus()
       return
     }
-    onAdd(result.clean)
+    lock.current = true
+    setPending(true)
+    setFailure('')
+    try { await onAdd(result.clean) }
+    catch (error) {
+      if (error instanceof ApiError) {
+        setErrors(error.fields)
+        const first = Object.keys(error.fields)[0]
+        if (first) form.querySelector<HTMLInputElement>(`[name="${first}"]`)?.focus()
+      }
+      setFailure(errorMessage(error, true))
+    } finally { lock.current = false; setPending(false) }
   }
   return <form onSubmit={submit} noValidate className="application-form">
-    <div className="info-note"><Info size={18} /><p>Added to this preview only. Your additions reset when you reload.</p></div>
+    <div className="info-note"><Info size={18} /><p>{mode === 'preview' ? 'Added to this preview only. Your additions reset when you reload.' : 'Save to the local database. Keep this form open while saving.'}</p></div>
+    {failure && <p className="field-error" role="alert">{failure}</p>}
     <div className="form-fields">
       {(['company', 'role', 'applied_on'] as const).map((field, i) => <div className="field" key={field}>
         <label htmlFor={field}>{['Company', 'Role', 'Applied date'][i]} <span aria-hidden="true">*</span></label>
         <input id={field} name={field} data-autofocus={field === 'company' ? '' : undefined} type={field === 'applied_on' ? 'date' : 'text'}
           placeholder={field === 'company' ? 'e.g. Cedar & Finch' : field === 'role' ? 'e.g. Product Designer' : undefined}
-          required value={values[field]} aria-invalid={!!errors[field]} aria-describedby={errors[field] ? `${field}-error` : `${field}-hint`}
+          readOnly={pending} required value={values[field]} aria-invalid={!!errors[field]} aria-describedby={errors[field] ? `${field}-error` : `${field}-hint`}
           onChange={event => setValues({ ...values, [field]: event.target.value })} />
         {errors[field] ? <p id={`${field}-error`} className="field-error" role="alert">{errors[field]}</p> :
           <p id={`${field}-hint`} className="field-hint">{field === 'applied_on' ? 'The date you applied. Future dates are also accepted.' : 'Up to 200 characters.'}</p>}
       </div>)}
     </div>
-    <p className="form-stage-note">Starts in <strong>Applied</strong>, a provisional sample stage.</p>
-    <div className="form-actions"><Button onClick={onClose} type="button">Cancel</Button><Button variant="primary" type="submit"><Plus size={17} />Add to preview</Button></div>
+    {mode === 'preview' && <p className="form-stage-note">Starts in <strong>Applied</strong>, a provisional sample stage.</p>}
+    <div className="form-actions"><Button disabled={pending} onClick={onClose} type="button">Cancel</Button><Button disabled={pending} variant="primary" type="submit"><Plus size={17} />{pending ? 'Saving…' : mode === 'preview' ? 'Add to preview' : 'Save application'}</Button></div>
   </form>
 }
diff --git a/frontend/src/components/ApplicationsView.tsx b/frontend/src/components/ApplicationsView.tsx
index 7ef5bb4..3b026b3 100644
--- a/frontend/src/components/ApplicationsView.tsx
+++ b/frontend/src/components/ApplicationsView.tsx
@@ -1,15 +1,14 @@
 import { CalendarDays, ChevronRight, Inbox } from 'lucide-react'
 import { Link } from 'react-router'
-import { formatDate, initials, stages, type PreviewApplication } from '../data'
+import { formatDate, initials, stages, type Application, type Stage, type PreviewApplication } from '../data'
 import { StageLabel } from './ui'

 export function CompanyMark({ company }: { company: string }) {
   const color = company.charCodeAt(0) % 5
   return <span aria-hidden="true" className={`company-mark company-color-${color}`}>{initials(company)}</span>
 }
-function ApplicationCard({ record, search }: { record: PreviewApplication; search: string }) {
-  const { application } = record
-  return <Link to={`/applications/${application.id}${search}`} className="application-card" aria-label={`${application.role} at ${application.company}`}>
+function ApplicationCard({ application, search, preview = true }: { application: Application; search: string; preview?: boolean }) {
+  return <Link to={`${preview ? '/preview' : ''}/applications/${application.id}${search}`} className="application-card" aria-label={`${application.role} at ${application.company}`}>
     <div className="card-top"><CompanyMark company={application.company} /><ChevronRight size={17} className="card-arrow" /></div>
     <h3>{application.role}</h3><p className="card-company">{application.company}</p>
     <div className="card-footer"><CalendarDays size={15} /><span>Applied {formatDate(application.applied_on)}</span></div>
@@ -22,7 +21,7 @@ export function Board({ records, search }: { records: PreviewApplication[]; sear
         const cards = records.filter(record => record.sampleStage === stage)
         return <section key={stage} className="board-column" aria-label={`${stage}, ${cards.length} applications`}>
           <div className={`column-heading stage-${stage.toLowerCase()}`}><h2>{stage}</h2><span className="column-count">{cards.length}</span></div>
-          <div className="column-cards">{cards.map(record => <ApplicationCard key={record.application.id} record={record} search={search} />)}
+          <div className="column-cards">{cards.map(record => <ApplicationCard key={record.application.id} application={record.application} search={search} />)}
             {!cards.length && <div className="column-empty"><Inbox size={22} /><p>No applications here</p><span>Room for what’s next.</span></div>}
           </div>
         </section>
@@ -30,15 +29,22 @@ export function Board({ records, search }: { records: PreviewApplication[]; sear
     </div>
   </div>
 }
-export function ApplicationList({ records, search }: { records: PreviewApplication[]; search: string }) {
-  return <div className="application-list" role="region" aria-label="Application list">
-    <div className="list-heading" aria-hidden="true"><span>Company</span><span>Role</span><span>Applied date</span><span>Sample stage</span><span /></div>
+export function StoredBoard({ applications, search }: { applications: Application[]; search: string }) {
+  // A display fallback only: never assign a stage to an API record.
+  return <section className="stored-board board-column" aria-label="Stored application board">
+    <div className="column-heading neutral-heading"><h2>Stage not recorded</h2><span className="column-count" aria-label={`${applications.length} shown on this page`}>{applications.length}</span></div>
+    <div className="column-cards">{applications.map(application => <ApplicationCard key={application.id} application={application} search={search} preview={false} />)}</div>
+  </section>
+}
+export function ApplicationList({ records, search, preview = true }: { records: { application: Application; sampleStage?: Stage }[]; search: string; preview?: boolean }) {
+  return <div className={`application-list ${preview ? "" : "stored-list"}`} role="region" aria-label="Application list">
+    <div className="list-heading" aria-hidden="true"><span>Company</span><span>Role</span><span>Applied date</span>{preview && <span>Sample stage</span>}<span /></div>
     <ul>{records.map(({ application, sampleStage }) => <li key={application.id}>
-      <Link className="list-row" to={`/applications/${application.id}${search}`} aria-label={`${application.role} at ${application.company}`}>
+      <Link className="list-row" to={`${preview ? "/preview" : ""}/applications/${application.id}${search}`} aria-label={`${application.role} at ${application.company}`}>
         <span className="list-company"><CompanyMark company={application.company} /><span>{application.company}</span></span>
         <span className="list-role">{application.role}</span>
         <span className="list-date"><span className="mobile-only">Applied </span>{formatDate(application.applied_on)}</span>
-        <span className="list-stage"><StageLabel stage={sampleStage} /></span>
+        {preview && sampleStage && <span className="list-stage"><StageLabel stage={sampleStage} /></span>}
         <ChevronRight size={17} className="list-arrow" />
       </Link>
     </li>)}</ul>
diff --git a/frontend/src/components/Shell.tsx b/frontend/src/components/Shell.tsx
index 2a41a5b..277a99c 100644
--- a/frontend/src/components/Shell.tsx
+++ b/frontend/src/components/Shell.tsx
@@ -1,20 +1,22 @@
 import { useState, type ReactNode } from 'react'
-import { Link } from 'react-router'
+import { Link, useLocation } from 'react-router'
 import { ArrowUpRight, Layers3, Menu, ShieldCheck } from 'lucide-react'
 import { Modal, PreviewNotice } from './ui'

 function Sidebar({ onNavigate }: { onNavigate?: () => void }) {
+  const preview = useLocation().pathname.startsWith('/preview/')
   return <div className="sidebar-inner">
     <Link className="brand" to="/applications" onClick={onNavigate}><img src="/mark.svg" alt="" width="32" height="32" /><span>ApplySync<span className="brand-dot">.</span></span></Link>
     <div className="sidebar-body">
       <p className="eyebrow">YOUR WORKSPACE</p>
-      <nav aria-label="Main navigation"><Link className="nav-link" aria-current="page" to="/applications" onClick={onNavigate}><Layers3 size={19} /> Applications <ArrowUpRight size={16} className="ml-auto" /></Link></nav>
-      <div className="sidebar-note"><span className="tiny-tag">BUILD 2 · PREVIEW</span><h2>A little more clarity.</h2><p>One place to see your next opportunity taking shape.</p></div>
+      <nav aria-label="Main navigation"><Link className="nav-link" aria-current="page" to={preview ? "/preview/applications" : "/applications"} onClick={onNavigate}><Layers3 size={19} /> Applications <ArrowUpRight size={16} className="ml-auto" /></Link></nav>
+      <div className="sidebar-note"><span className="tiny-tag">{preview ? 'BUILD 2 · PREVIEW' : 'BUILD 2 · LOCAL DEVELOPMENT'}</span><h2>A little more clarity.</h2><p>One place to see your next opportunity taking shape.</p></div>
     </div>
-    <div className="sidebar-footer"><ShieldCheck size={20} /><div><strong>Private by design</strong><p>Fictional data. All local.</p></div></div>
+    <div className="sidebar-footer"><ShieldCheck size={20} /><div><strong>Private by design</strong><p>{preview ? "Fictional data. All local." : "Local, unauthenticated use."}</p></div></div>
   </div>
 }
 export function Shell({ children }: { children: ReactNode }) {
+  const preview = useLocation().pathname.startsWith('/preview/')
   const [navigationOpen, setNavigationOpen] = useState(false)
   return <div className="app-shell">
     <a className="skip-link" href="#main-content">Skip to applications</a>
@@ -23,10 +25,10 @@ export function Shell({ children }: { children: ReactNode }) {
       <header className="topbar">
         <button className="icon-button mobile-menu" aria-label="Open navigation" onClick={() => setNavigationOpen(true)}><Menu size={21} /></button>
         <div className="breadcrumb"><span>Workspace</span><span aria-hidden="true">/</span><strong>Applications</strong></div>
-        <PreviewNotice />
+        <PreviewNotice>{preview ? 'Design preview · Sample data' : 'Local development · Stored data'}</PreviewNotice>
       </header>
       <main id="main-content" tabIndex={-1}>{children}</main>
     </div>
-    {navigationOpen && <Modal title="Your workspace" variant="navigation" onClose={() => setNavigationOpen(false)}><Sidebar onNavigate={() => setNavigationOpen(false)} /></Modal>}
+    {navigationOpen && <Modal title="Your workspace" variant="navigation" preview={preview} onClose={() => setNavigationOpen(false)}><Sidebar onNavigate={() => setNavigationOpen(false)} /></Modal>}
   </div>
 }
diff --git a/frontend/src/components/ui.tsx b/frontend/src/components/ui.tsx
index ef4d9e7..a1d439e 100644
--- a/frontend/src/components/ui.tsx
+++ b/frontend/src/components/ui.tsx
@@ -12,8 +12,8 @@ export function PreviewNotice({ children = 'Design preview · Sample data' }: {
   return <span className="preview-notice"><span className="preview-dot" />{children}</span>
 }

-export function Modal({ title, subtitle, children, onClose, variant = 'panel' }: {
-  title: string; subtitle?: string; children: ReactNode; onClose: () => void; variant?: 'panel' | 'form' | 'navigation'
+export function Modal({ title, subtitle, children, onClose, variant = 'panel', busy = false, preview = true }: {
+  title: string; subtitle?: string; children: ReactNode; onClose: () => void; variant?: 'panel' | 'form' | 'navigation'; busy?: boolean; preview?: boolean
 }) {
   const dialog = useRef<HTMLDialogElement>(null)
   const titleId = useId()
@@ -41,10 +41,10 @@ export function Modal({ title, subtitle, children, onClose, variant = 'panel' }:
       if (event.shiftKey && document.activeElement === first) { event.preventDefault(); last?.focus() }
       else if (!event.shiftKey && document.activeElement === last) { event.preventDefault(); first?.focus() }
     }}
-    onCancel={event => { event.preventDefault(); onClose() }}>
+    onCancel={event => { event.preventDefault(); if (!busy) onClose() }}>
     <div className="modal-heading">
-      <div><p className="eyebrow">APPLYSYNC PREVIEW</p><h2 id={titleId}>{title}</h2>{subtitle && <p className="text-muted mt-2">{subtitle}</p>}</div>
-      <button className="icon-button shrink-0" aria-label="Close panel" onClick={onClose}><X size={20} /></button>
+      <div><p className="eyebrow">{preview ? 'APPLYSYNC PREVIEW' : 'APPLYSYNC · LOCAL DEVELOPMENT'}</p><h2 id={titleId}>{title}</h2>{subtitle && <p className="text-muted mt-2">{subtitle}</p>}</div>
+      <button disabled={busy} className="icon-button shrink-0" aria-label="Close panel" onClick={onClose}><X size={20} /></button>
     </div>
     {children}
   </dialog>
diff --git a/frontend/src/styles.css b/frontend/src/styles.css
index 9bd081b..7e4e3f7 100644
--- a/frontend/src/styles.css
+++ b/frontend/src/styles.css
@@ -208,3 +208,15 @@ input::placeholder { color: #667085; }
 @media (prefers-reduced-motion: reduce) {
   *, *::before, *::after { animation: none !important; transition: none !important; scroll-behavior: auto !important; }
 }
+
+/* Real records reuse the approved list; the API has no stage column. */
+.stored-list .list-heading, .stored-list .list-row { grid-template-columns: 1.1fr 1.3fr 130px 20px; }
+.pagination { display: flex; flex-wrap: wrap; align-items: center; justify-content: space-between; gap: 14px; padding-top: 20px; color: var(--color-muted); font-size: 13px; }
+.record-id { overflow-wrap: anywhere; font-size: 13px; }
+.stored-board { width: min(100%, 280px); }
+.neutral-heading { background: #eaedf1; color: #424b5b; }
+.board-explanation { color: var(--color-muted); font-size: 13px; line-height: 1.6; margin-bottom: 16px; }
+@media (max-width: 620px) {
+  .stored-list .list-row { grid-template-columns: minmax(0, 1fr); }
+  .pagination span { order: 3; width: 100%; text-align: center; }
+}
diff --git a/frontend/tsconfig.json b/frontend/tsconfig.json
index 3baa9bf..4f23c4b 100644
--- a/frontend/tsconfig.json
+++ b/frontend/tsconfig.json
@@ -6,5 +6,5 @@
     "resolveJsonModule": true, "isolatedModules": true, "noEmit": true,
     "types": ["vite/client", "vitest/globals", "@testing-library/jest-dom"]
   },
-  "include": ["src", "vite.config.ts", "playwright.config.ts", "e2e"]
+  "include": ["src", "vite.config.ts", "playwright.config.ts", "playwright.integration.config.ts", "e2e"]
 }
diff --git a/main.py b/main.py
index 872024f..2fb3f3f 100644
--- a/main.py
+++ b/main.py
@@ -2,6 +2,7 @@ from contextlib import asynccontextmanager
 from threading import Lock

 from fastapi import FastAPI, Request
+from fastapi.middleware.cors import CORSMiddleware
 from fastapi.responses import JSONResponse
 from sqlalchemy.exc import SQLAlchemyError

@@ -32,6 +33,14 @@ def create_app(database_target: str = "dev") -> FastAPI:
     if database_target not in {"dev", "test"}:
         raise ConfigurationError("Database target must be dev or test.")
     application = FastAPI(lifespan=lifespan)
+    application.add_middleware(
+        CORSMiddleware,
+        allow_origins=[f"http://{host}:{port}" for host in ("localhost", "127.0.0.1")
+                       for port in (5173, 4173)],
+        allow_credentials=False,
+        allow_methods=["GET", "POST"],
+        allow_headers=["Content-Type"],
+    )
     application.state.database_target = database_target
     application.state.engine = None
     application.state.engine_lock = Lock()
```

### Complete file: frontend/.env.example

```text
# Public browser configuration. Never put credentials or secrets here.
# Copy to frontend/.env.local and replace the placeholder with http://127.0.0.1:8000
VITE_API_BASE_URL=replace-with-local-api-origin
```

### Complete file: frontend/e2e/integration.spec.ts

```typescript
import { expect, test } from '@playwright/test'
import { mkdirSync } from 'node:fs'

const api = process.env.APPLYSYNC_E2E_API_ORIGIN!
const marker = process.env.APPLYSYNC_E2E_RUN_ID!
const screenshots = '../docs/screenshots/Build2_Task2'
mkdirSync(screenshots, { recursive: true })

test('real browser CORS, PostgreSQL creation, query refresh, pagination and reload', async ({ page }) => {
  let listReads = 0
  let posts = 0
  const errors: string[] = []
  page.on('pageerror', error => errors.push(error.message))
  page.on('request', request => {
    if (request.url().startsWith(api + '/applications?')) listReads++
    if (request.url() === api + '/applications' && request.method() === 'POST') posts++
  })
  await page.goto('/applications')
  await expect(page.getByRole('region', { name: 'Application list' }).getByRole('listitem')).toHaveCount(20)
  await expect(page.getByLabel('Sample stage')).toHaveCount(0)
  await expect(page.locator('.stage-label')).toHaveCount(0)
  await expect(page.getByText('Oldest first · No total count available')).toBeVisible()
  await page.getByRole('button', { name: 'Next page' }).click()
  await expect(page).toHaveURL(/offset=20/)
  await expect(page.getByRole('region', { name: 'Application list' }).getByRole('listitem').first()).toBeVisible()
  await page.getByRole('button', { name: 'Previous page' }).click()
  await expect(page).toHaveURL(/offset=0/)
  await page.getByRole('searchbox').fill('no-such-synthetic-result')
  await expect(page.getByText('No matches on this page')).toBeVisible()
  await page.getByRole('button', { name: 'Clear page search' }).click()
  await page.screenshot({ path: `${screenshots}/stored-list.png`, fullPage: true })

  const before = listReads
  await page.getByRole('link', { name: 'Add application', exact: true }).click()
  await page.getByRole('dialog').getByLabel('Company', { exact: false }).fill(`  ${marker} created  `)
  await page.getByRole('dialog').getByLabel('Role', { exact: false }).fill('  Browser Engineer  ')
  await page.getByRole('dialog').getByLabel('Applied date', { exact: false }).fill('2100-01-01')
  const confirmed = page.waitForResponse(response => response.url() === api + '/applications' && response.request().method() === 'POST')
  await page.getByRole('button', { name: 'Save application' }).click()
  const response = await confirmed
  expect(response.status()).toBe(201)
  expect(response.headers()['access-control-allow-origin']).toBe('http://127.0.0.1:4173')
  const record = await response.json()
  expect(record.company).toBe(marker + ' created')
  expect(record.role).toBe('Browser Engineer')
  expect(record.created_at).toBeTruthy()
  await expect(page).toHaveURL(new RegExp(`/applications/${record.id}`))
  await expect(page.getByText('Application saved to the database.')).toBeVisible()
  await expect.poll(() => listReads).toBeGreaterThan(before)
  const reread = page.waitForResponse(response => response.url() === `${api}/applications/${record.id}`)
  await page.reload()
  expect((await reread).status()).toBe(200)
  await expect(page.getByRole('dialog')).toContainText(marker + ' created')
  await expect(page.getByRole('dialog')).toContainText('1 Jan 2100')
  await page.screenshot({ path: `${screenshots}/stored-detail.png`, animations: 'disabled' })
  await page.setViewportSize({ width: 390, height: 844 })
  await page.screenshot({ path: `${screenshots}/stored-mobile-detail.png`, animations: 'disabled' })
  await page.keyboard.press('Escape')
  await page.screenshot({ path: `${screenshots}/stored-mobile-list.png`, fullPage: true })
  expect(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth)).toBe(true)

  await page.goto('/applications/00000000-0000-4000-8000-000000000000')
  await expect(page.getByRole('dialog')).toContainText('Application not found.')
  await page.goto('/applications/not-a-uuid')
  await expect(page.getByRole('dialog')).toContainText('Invalid application ID')
  await page.keyboard.press('Escape')
  await page.getByRole('link', { name: 'Explore sample Board/List preview' }).click()
  const readsBeforePreview = listReads
  await expect(page.getByText('Design preview · Sample data')).toBeVisible()
  await page.getByRole('link', { name: 'Add application', exact: true }).click()
  await page.getByRole('dialog').getByLabel('Company', { exact: false }).fill('Preview-only Company')
  await page.getByRole('dialog').getByLabel('Role', { exact: false }).fill('Preview-only Role')
  await page.getByRole('dialog').getByLabel('Applied date', { exact: false }).fill('2100-01-01')
  await page.getByRole('button', { name: 'Add to preview' }).click()
  await expect(page.getByRole('status')).toContainText('added to the preview')
  expect(posts).toBe(1)
  expect(listReads).toBe(readsBeforePreview)
  await page.reload()
  await expect(page.getByText('Preview-only Company')).toHaveCount(0)
  expect(errors).toEqual([])
})
```

### Complete file: frontend/e2e/stored.spec.ts

```typescript
import { expect, test } from '@playwright/test'
import { mkdirSync } from 'node:fs'

const base = 'http://127.0.0.1:8000'
const row = { id: '00000000-0000-4000-8000-000000000099', company: 'Synthetic Company', role: 'Engineer', applied_on: '2026-09-01', created_at: '2026-09-01T12:00:00Z' }
const headers = { 'access-control-allow-origin': 'http://127.0.0.1:4173' }

test('real Board/List share IDs, query state and paging with neutral stage fallback', async ({ page }) => {
  const records = Array.from({ length: 22 }, (_, i) => ({ ...row,
    id: `00000000-0000-4000-8000-${String(i + 100).padStart(12, '0')}`,
    company: `Synthetic Company ${i + 1}`,
  }))
  let reads = 0
  let writes = 0
  await page.route(`${base}/**`, async route => {
    const request = route.request()
    if (request.method() !== 'GET') { writes++; return route.abort() }
    const url = new URL(request.url())
    if (url.pathname === '/applications') {
      reads++
      const offset = Number(url.searchParams.get('offset'))
      return route.fulfill({ headers, json: { items: records.slice(offset, offset + 20), offset, limit: 20 } })
    }
    await route.fulfill({ headers, json: records.find(record => url.pathname.endsWith(record.id)) })
  })
  await page.goto('/applications?q=Synthetic&offset=0')
  const list = page.getByRole('region', { name: 'Application list' })
  await expect(list.getByRole('link')).toHaveCount(20)
  const ids = async (selector: string) => page.locator(selector).evaluateAll(links => links.map(link => new URL((link as HTMLAnchorElement).href).pathname))
  const listIds = await ids('.list-row')
  const before = reads
  await page.getByRole('button', { name: 'Board', exact: true }).click()
  const board = page.getByRole('region', { name: 'Stored application board' })
  await expect(board.getByRole('link')).toHaveCount(20)
  expect(await ids('.application-card')).toEqual(listIds)
  expect(reads).toBe(before)
  await expect(board.getByRole('heading', { name: 'Stage not recorded' })).toBeVisible()
  await expect(page.getByText('Applications will be grouped by stage when stage tracking is available.')).toBeVisible()
  await expect(page.getByText('Cedar & Finch')).toHaveCount(0)
  await expect(page.locator('.stage-label')).toHaveCount(0)
  await expect(page.getByLabel('Sample stage')).toHaveCount(0)
  await page.getByRole('button', { name: 'Next page' }).click()
  await expect(board.getByRole('link')).toHaveCount(2)
  await expect(page.getByText('2 shown · 2 loaded on this page')).toBeVisible()
  await expect(page.getByRole('searchbox')).toHaveValue('Synthetic')
  expect(new URL(page.url()).searchParams.get('offset')).toBe('20')
  const secondPageIds = await ids('.application-card')
  const shots = '../docs/screenshots/Build2_Task2/correction'
  mkdirSync(shots, { recursive: true })
  await page.screenshot({ path: `${shots}/stored-board.png`, fullPage: true })
  await page.getByRole('button', { name: 'List', exact: true }).click()
  await expect(list.getByRole('link')).toHaveCount(2)
  expect(await ids('.list-row')).toEqual(secondPageIds)
  expect(new URL(page.url()).searchParams.get('offset')).toBe('20')
  await expect(page.getByRole('searchbox')).toHaveValue('Synthetic')
  await page.screenshot({ path: `${shots}/stored-list.png`, fullPage: true })
  await page.getByRole('button', { name: 'Board', exact: true }).click()
  await board.getByRole('link').first().click()
  expect(new URL(page.url()).pathname).toBe(secondPageIds[0])
  await expect(page.getByRole('dialog')).toContainText('Synthetic Company 21')
  await page.keyboard.press('Escape')
  await expect(page.getByRole('button', { name: 'Board', exact: true })).toHaveAttribute('aria-pressed', 'true')
  expect(new URL(page.url()).searchParams.get('offset')).toBe('20')
  await page.setViewportSize({ width: 390, height: 844 })
  await page.screenshot({ path: `${shots}/stored-mobile-board.png`, fullPage: true })
  expect(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth)).toBe(true)
  await page.getByRole('button', { name: 'List', exact: true }).click()
  await page.screenshot({ path: `${shots}/stored-mobile-list.png`, fullPage: true })
  expect(await ids('.list-row')).toEqual(secondPageIds)
  expect(writes).toBe(0)
})

test('read network/server failures, retry, empty page and malformed pagination', async ({ page }) => {
  let state = 'network'
  await page.route(`${base}/**`, async route => {
    if (state === 'network') return route.abort('connectionrefused')
    await route.fulfill({ status: state === 'server' ? 500 : 200, headers, json: state === 'server' ? { detail: 'synthetic-private' } : { items: [], limit: 20, offset: 0 } })
  })
  await page.goto('/applications')
  await expect(page.getByRole('alert')).toContainText('Cannot reach the backend')
  state = 'server'
  await page.getByRole('button', { name: 'Retry list' }).click()
  await expect(page.getByRole('alert')).toContainText('server could not load')
  await expect(page.getByText('synthetic-private')).toHaveCount(0)
  state = 'empty'
  await page.getByRole('button', { name: 'Retry list' }).click()
  await expect(page.getByText('No stored applications yet')).toBeVisible()
  await page.goto('/applications?offset=-1')
  await expect(page.getByRole('alert')).toContainText('Invalid page offset')
})

test('pending POST, backend validation, server/network uncertainty and success', async ({ page }) => {
  let mode = 'validation'
  let finish!: () => void
  let postCount = 0
  await page.route(`${base}/**`, async route => {
    if (route.request().method() === 'POST') {
      postCount++
      await new Promise<void>(resolve => { finish = resolve })
      if (mode === 'network') return route.abort('connectionreset')
      return route.fulfill({ headers, status: mode === 'validation' ? 422 : mode === 'server' ? 500 : 201,
        json: mode === 'validation' ? { detail: [{ loc: ['body', 'company'], type: 'string_too_long', msg: 'synthetic-private' }] } : mode === 'server' ? { detail: 'synthetic-private' } : row })
    }
    await route.fulfill({ headers, json: route.request().url().includes('?') ? { items: [], limit: 20, offset: 0 } : row })
  })
  await page.goto('/applications/new')
  const dialog = page.getByRole('dialog')
  await dialog.getByLabel('Company', { exact: false }).fill('Synthetic Company')
  await dialog.getByLabel('Role', { exact: false }).fill('Engineer')
  await dialog.getByLabel('Applied date', { exact: false }).fill('2026-09-01')
  await dialog.getByRole('button', { name: 'Save application' }).click()
  await expect(dialog.getByRole('button', { name: 'Saving…' })).toBeDisabled()
  await page.keyboard.press('Enter')
  await page.keyboard.press('Escape')
  await expect(dialog).toBeVisible()
  await expect.poll(() => postCount).toBe(1)
  finish()
  await expect(dialog.getByText('Use 200 characters or fewer.')).toBeVisible()
  await expect(dialog.getByLabel('Company', { exact: false })).toHaveValue('Synthetic Company')
  for (const next of ['server', 'network']) {
    mode = next
    const before = postCount
    await dialog.getByRole('button', { name: 'Save application' }).click()
    await expect.poll(() => postCount).toBe(before + 1)
    finish()
    await expect(dialog.getByRole('alert')).toContainText('may have been saved')
    await expect(dialog.getByLabel('Role', { exact: false })).toHaveValue('Engineer')
  }
  expect(postCount).toBe(3)
  mode = 'success'
  await dialog.getByRole('button', { name: 'Save application' }).click()
  await expect.poll(() => postCount).toBe(4)
  finish()
  await expect(page.getByText('Application saved to the database.')).toBeVisible()
  await expect(page).toHaveURL(new RegExp(row.id))
})

test('direct detail read failure retries and full last page leads to honest empty next page', async ({ page }) => {
  let detailFails = true
  await page.route(`${base}/**`, async route => {
    const url = new URL(route.request().url())
    if (url.search) {
      const offset = Number(url.searchParams.get('offset'))
      return route.fulfill({ headers, json: { items: offset ? [] : Array.from({ length: 20 }, (_, i) => ({ ...row, id: `00000000-0000-4000-8000-${String(i).padStart(12, '0')}` })), limit: 20, offset } })
    }
    await route.fulfill({ headers, status: detailFails ? 500 : 200, json: detailFails ? {} : row })
  })
  await page.goto(`/applications/${row.id}`)
  await expect(page.getByRole('dialog').getByRole('alert')).toContainText('server could not load')
  detailFails = false
  await page.getByRole('button', { name: 'Retry details' }).click()
  await expect(page.getByRole('dialog')).toContainText('Synthetic Company')
  await page.keyboard.press('Escape')
  await page.getByRole('button', { name: 'Next page' }).click()
  await expect(page.getByText('No applications on this page')).toBeVisible()
  await expect(page.getByRole('button', { name: 'Next page' })).toBeDisabled()
  await expect(page.getByRole('button', { name: 'Previous page' })).toBeEnabled()
})
```

### Complete file: frontend/playwright.integration.config.ts

```typescript
import { defineConfig } from '@playwright/test'

if (!process.env.APPLYSYNC_E2E_RUN_ID || !process.env.APPLYSYNC_E2E_API_ORIGIN) {
  throw new Error('Run the guarded Python integration runner from the repository root.')
}
export default defineConfig({
  testDir: './e2e', testMatch: '**/integration.spec.ts', workers: 1, reporter: 'list',
  use: { baseURL: 'http://127.0.0.1:4173', browserName: 'chromium', viewport: { width: 1440, height: 1000 }, trace: 'retain-on-failure' },
  webServer: { command: 'npm run dev -- --port 4173 --strictPort', url: 'http://127.0.0.1:4173', reuseExistingServer: false,
    env: { VITE_API_BASE_URL: process.env.APPLYSYNC_E2E_API_ORIGIN } },
})
```

### Complete file: frontend/src/PreviewApplications.tsx

```tsx
import { useState } from 'react'
import { Link, useLocation, useNavigate, useParams, useSearchParams } from 'react-router'
import { ArrowLeft, CalendarDays, Columns3, List, Plus, Search, SearchX, SlidersHorizontal } from 'lucide-react'
import { Board, ApplicationList, CompanyMark } from './components/ApplicationsView'
import { Button, Modal, PreviewNotice, StageLabel } from './components/ui'
import { ApplicationForm } from './components/ApplicationForm'
import { filterApplications, formatDate, sampleApplications, stages, type CreateValues, type PreviewApplication } from './data'

export function PreviewApplications({ initialRecords = sampleApplications }: { initialRecords?: PreviewApplication[] }) {
  const [records, setRecords] = useState(initialRecords)
  const [feedback, setFeedback] = useState('')
  const [params, setParams] = useSearchParams()
  const location = useLocation()
  const navigate = useNavigate()
  const { id } = useParams()
  const search = params.get('q') ?? ''
  const selectedStage = stages.find(stage => stage === params.get('stage')) ?? 'All stages'
  const view = params.get('view') === 'list' ? 'list' : 'board'
  const filtered = filterApplications(records, search, selectedStage)
  const selected = records.find(record => record.application.id === id)
  const isNew = id === 'new'
  const close = () => navigate(`/preview/applications${location.search}`, { replace: true })
  function setSelection(key: string, value: string) {
    setParams(current => {
      const next = new URLSearchParams(current)
      value ? next.set(key, value) : next.delete(key)
      return next
    }, { replace: true })
  }
  function add(values: CreateValues) {
    setRecords(current => [{ application: { ...values, id: crypto.randomUUID(), created_at: new Date().toISOString() }, sampleStage: 'Applied' }, ...current])
    setFeedback(`${values.company} added to the preview. Reloading removes this addition.`)
    close()
  }
  return <>
    <div className="page-heading"><div><p className="eyebrow">YOUR NEXT CHAPTER</p><h1>Applications</h1><p className="page-description">A clear view of every opportunity, from first step to next move.</p></div>
      <Link id="add-application" className="button button-primary" to={`/preview/applications/new${location.search}`}><Plus size={18} />Add application</Link>
    </div>
    <div className="applications-workspace">
      <div className="toolbar">
        <div className="view-switch" role="group" aria-label="Application view"><button aria-pressed={view === 'board'} onClick={() => setSelection('view', '')}><Columns3 size={17} />Board</button><button aria-pressed={view === 'list'} onClick={() => setSelection('view', 'list')}><List size={18} />List</button></div>
        <div className="filter-controls"><div className="search-field"><Search size={18} /><label className="sr-only" htmlFor="search">Search company or role</label><input id="search" type="search" placeholder="Search company or role…" value={search} onChange={event => setSelection('q', event.target.value)} /></div>
          <div className="stage-filter"><SlidersHorizontal size={16} /><label className="sr-only" htmlFor="stage-filter">Sample stage</label><select id="stage-filter" value={selectedStage} onChange={event => setSelection('stage', event.target.value === 'All stages' ? '' : event.target.value)}><option>All stages</option>{stages.map(stage => <option key={stage}>{stage}</option>)}</select></div>
        </div>
      </div>
      <div className="results-meta"><p aria-live="polite"><strong>{filtered.length}</strong> of {records.length} applications</p><span>Stages are for this preview only</span></div>
      {feedback && <div className="success-note" role="status"><span>{feedback}{(search || selectedStage !== 'All stages') && ' Your current filters may hide it.'}</span><Button variant="quiet" onClick={() => setFeedback('')}>Dismiss</Button></div>}
      {!filtered.length ? <div className="empty-state"><SearchX size={28} /><h2>{records.length ? 'No matching applications' : 'Your next chapter starts here'}</h2><p>{records.length ? 'Try a different company, role, or sample stage.' : 'Add an application to explore your preview.'}</p>
        {records.length ? <Button onClick={() => setParams(view === 'list' ? { view: 'list' } : {}, { replace: true })}>Clear search & filter</Button> : <Link className="button button-primary" to={`/preview/applications/new${location.search}`}>Add application</Link>}
      </div> : view === 'board' ? <Board records={filtered} search={location.search} /> : <ApplicationList records={filtered} search={location.search} />}
      <footer className="workspace-footer"><Link to="/applications">Return to stored applications</Link><span>Preview additions reset on reload.</span></footer>
    </div>
    {id && <Modal title={isNew ? 'Add application' : selected?.application.role ?? 'Application not found'} subtitle={isNew ? 'Make room for your next opportunity.' : selected?.application.company} variant={isNew ? 'form' : 'panel'} onClose={close}>
      {isNew ? <ApplicationForm onAdd={add} onClose={close} /> : selected ? <div className="detail-body">
        <div className="detail-identity"><CompanyMark company={selected.application.company} /><div><span className="eyebrow">COMPANY</span><strong>{selected.application.company}</strong></div></div>
        <h3>Application overview</h3><dl className="detail-facts"><div><dt><CalendarDays size={16} />Applied date</dt><dd>{formatDate(selected.application.applied_on)}</dd></div><div><dt>Sample stage</dt><dd><StageLabel stage={selected.sampleStage} /></dd></div></dl>
        <div className="detail-preview"><PreviewNotice /><p>This is a fictional application. Stages help you explore the layout; they are not saved application history.</p></div>
        <Button onClick={close}><ArrowLeft size={17} />Back to applications</Button>
      </div> : <div className="detail-body"><p>This preview record is unavailable. Preview additions disappear on reload.</p><Button onClick={close}>Back to applications</Button></div>}
    </Modal>}
  </>
}
```

### Complete file: frontend/src/StoredApplications.test.tsx

```tsx
import { act, render, screen, waitFor, within } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { MemoryRouter } from 'react-router'
import { afterEach, expect, it, vi } from 'vitest'
import { App } from './App'

const row = { id: '00000000-0000-4000-8000-000000000099', company: 'Stored Company', role: 'Engineer', applied_on: '2100-01-01', created_at: '2026-01-01T12:00:00Z' }
const json = (body: unknown, status = 200) => new Response(JSON.stringify(body), { status })
function mount(path = '/applications') { render(<MemoryRouter initialEntries={[path]}><App /></MemoryRouter>); return userEvent.setup() }
afterEach(() => vi.unstubAllGlobals())

it('lists real records without stage controls and clearly scopes search/counts', async () => {
  vi.stubGlobal('fetch', vi.fn().mockResolvedValue(json({ items: [row], limit: 20, offset: 0 })))
  const user = mount()
  expect(await screen.findByRole('link', { name: 'Engineer at Stored Company' })).toBeInTheDocument()
  expect(screen.queryByLabelText('Sample stage')).not.toBeInTheDocument()
  expect(document.querySelector('.stage-label')).not.toBeInTheDocument()
  expect(screen.getByText('Local development · Stored data')).toBeInTheDocument()
  expect(screen.getByText('BUILD 2 · LOCAL DEVELOPMENT')).toBeInTheDocument()
  await user.type(screen.getByRole('searchbox'), 'no-match')
  expect(screen.getByText('No matches on this page')).toBeInTheDocument()
  expect(screen.getByText('Oldest first · No total count available')).toBeInTheDocument()
})
it.each(['board', 'list'])('has loading, empty, failure and retry states in %s without sample fallback', async view => {
  let resolve!: (response: Response) => void
  const fetchMock = vi.fn().mockImplementationOnce(() => new Promise<Response>(r => { resolve = r }))
    .mockResolvedValueOnce(json({ items: [], limit: 20, offset: 0 }))
  vi.stubGlobal('fetch', fetchMock)
  const user = mount(`/applications?view=${view}`)
  expect(screen.getByRole('status')).toHaveTextContent('Loading applications')
  await user.click(screen.getByRole('button', { name: view === 'board' ? 'List' : 'Board' }))
  expect(screen.getByRole('status')).toHaveTextContent('Loading applications')
  expect(fetchMock).toHaveBeenCalledTimes(1)
  await act(async () => resolve(json({}, 500)))
  expect(await screen.findByRole('alert')).toHaveTextContent('server could not load')
  expect(screen.queryByText('Cedar & Finch')).not.toBeInTheDocument()
  await user.click(screen.getByRole('button', { name: view === 'board' ? 'Board' : 'List' }))
  expect(screen.getByRole('alert')).toHaveTextContent('server could not load')
  await user.click(screen.getByRole('button', { name: 'Retry list' }))
  expect(await screen.findByText('No stored applications yet')).toBeInTheDocument()
  await user.click(screen.getByRole('button', { name: view === 'board' ? 'List' : 'Board' }))
  expect(screen.getByText('No stored applications yet')).toBeInTheDocument()
  expect(screen.queryByText('Cedar & Finch')).not.toBeInTheDocument()
})
it('keeps input on backend validation and blocks duplicate pending submissions', async () => {
  let finish!: (response: Response) => void
  const posts = vi.fn(() => new Promise<Response>(resolve => { finish = resolve }))
  vi.stubGlobal('fetch', vi.fn((_url, options) => options?.method === 'POST' ? posts() : Promise.resolve(json({ items: [], limit: 20, offset: 0 }))))
  const user = mount('/applications/new')
  const form = screen.getByRole('dialog')
  await user.type(within(form).getByLabelText('Company', { exact: false }), 'Retain Me')
  await user.type(within(form).getByLabelText('Role', { exact: false }), 'Engineer')
  await user.type(within(form).getByLabelText('Applied date', { exact: false }), '2100-01-01')
  await user.click(screen.getByRole('button', { name: 'Save application' }))
  expect(screen.getByRole('button', { name: 'Saving…' })).toBeDisabled()
  await user.keyboard('{Enter}{Escape}')
  expect(posts).toHaveBeenCalledTimes(1)
  expect(screen.getByRole('dialog')).toBeInTheDocument()
  await act(async () => finish(json({ detail: [{ loc: ['body', 'company'], type: 'string_too_long' }] }, 422)))
  expect(await screen.findByText('Use 200 characters or fewer.')).toBeInTheDocument()
  expect(within(form).getByLabelText('Company', { exact: false })).toHaveValue('Retain Me')
})
it('opens confirmed detail and refreshes the list after creation', async () => {
  let created = false
  let lists = 0
  vi.stubGlobal('fetch', vi.fn((url, options) => {
    if (options?.method === 'POST') { created = true; return Promise.resolve(json(row, 201)) }
    if (String(url).includes('?')) { lists++; return Promise.resolve(json({ items: created ? [row] : [], limit: 20, offset: 0 })) }
    return Promise.resolve(json(row))
  }))
  const user = mount('/applications/new')
  await user.type(screen.getByLabelText('Company', { exact: false }), 'Stored Company')
  await user.type(screen.getByLabelText('Role', { exact: false }), 'Engineer')
  await user.type(screen.getByLabelText('Applied date', { exact: false }), '2100-01-01')
  await user.click(screen.getByRole('button', { name: 'Save application' }))
  expect(await screen.findByText('Application saved to the database.')).toBeInTheDocument()
  await user.click(screen.getByRole('button', { name: 'Back to applications' }))
  expect(await screen.findByRole('link', { name: 'Engineer at Stored Company' })).toBeInTheDocument()
  expect(lists).toBeGreaterThanOrEqual(2)
})
it('loads direct details, distinguishes missing/malformed IDs, and never fetches preview data', async () => {
  const fetchMock = vi.fn().mockResolvedValue(json({ items: [], limit: 20, offset: 0 }))
  vi.stubGlobal('fetch', fetchMock)
  const user = mount('/applications/bad-id')
  expect(screen.getByRole('alert')).toHaveTextContent('Invalid application ID')
  await user.click(screen.getByRole('button', { name: 'Back to applications' }))
  await waitFor(() => expect(fetchMock).toHaveBeenCalledTimes(1))
  await user.click(screen.getByRole('link', { name: 'Explore sample Board/List preview' }))
  expect(screen.getByText('Cedar & Finch')).toBeInTheDocument()
  expect(screen.getByText('Design preview · Sample data')).toBeInTheDocument()
  expect(fetchMock).toHaveBeenCalledTimes(1)
})
```

### Complete file: frontend/src/StoredApplications.tsx

```tsx
import { useState } from 'react'
import { Link, useLocation, useNavigate, useParams, useSearchParams } from 'react-router'
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import { CalendarDays, Columns3, List, Plus, Search } from 'lucide-react'
import { ApiError, createApplication, errorMessage, getApplication, isUuid, listApplications } from './api'
import { type CreateValues, formatDate } from './data'
import { ApplicationList, CompanyMark, StoredBoard } from './components/ApplicationsView'
import { ApplicationForm } from './components/ApplicationForm'
import { Button, Modal } from './components/ui'

const pageSize = 20
export function StoredApplications() {
  const [params, setParams] = useSearchParams()
  const { id } = useParams()
  const navigate = useNavigate()
  const location = useLocation()
  const client = useQueryClient()
  const [saved, setSaved] = useState(false)
  const rawOffset = params.get('offset') ?? '0'
  const offset = Number(rawOffset)
  const validOffset = /^\d+$/.test(rawOffset) && Number.isSafeInteger(offset) && offset <= 10_000
  const search = params.get('q') ?? ''
  const view = params.get('view') === 'board' ? 'board' : 'list'
  const isNew = id === 'new'
  const validId = !!id && !isNew && isUuid(id)
  const list = useQuery({ queryKey: ['applications', 'list', pageSize, offset],
    queryFn: ({ signal }) => listApplications(pageSize, offset, signal), enabled: validOffset })
  const detail = useQuery({ queryKey: ['applications', 'detail', id],
    queryFn: ({ signal }) => getApplication(id!, signal), enabled: validId })
  const mutation = useMutation({ mutationFn: createApplication, retry: false })
  const close = () => { if (!mutation.isPending) navigate(`/applications${location.search}`, { replace: true }) }
  const rows = list.data?.items ?? []
  const query = search.trim().toLocaleLowerCase()
  const visible = rows.filter(row => `${row.company}\n${row.role}`.toLocaleLowerCase().includes(query))
  function selection(key: string, value: string) {
    setParams(current => { const next = new URLSearchParams(current); next.set(key, value); return next }, { replace: true })
  }
  async function add(values: CreateValues) {
    const record = await mutation.mutateAsync(values)
    client.setQueryData(['applications', 'detail', record.id], record)
    // Creation is already committed. A failed refresh is a read error, not a failed POST.
    await client.invalidateQueries({ queryKey: ['applications', 'list'] })
    setSaved(true)
    navigate(`/applications/${record.id}${location.search}`, { replace: true })
  }
  return <>
    <div className="page-heading"><div><p className="eyebrow">YOUR NEXT CHAPTER</p><h1>Applications</h1><p className="page-description">Your stored applications, one opportunity at a time.</p></div>
      <Link id="add-application" className="button button-primary" to={`/applications/new${location.search}`} onClick={() => setSaved(false)}><Plus size={18} />Add application</Link>
    </div>
    <div className="applications-workspace">
      <div className="toolbar"><div className="view-switch" role="group" aria-label="Application view"><button aria-pressed={view === 'board'} onClick={() => selection('view', 'board')}><Columns3 size={17} />Board</button><button aria-pressed={view === 'list'} onClick={() => selection('view', 'list')}><List size={18} />List</button></div><div className="filter-controls"><div className="search-field"><Search size={18} /><label className="sr-only" htmlFor="search">Search this loaded page</label><input id="search" type="search" placeholder="Search this loaded page…" value={search} onChange={event => selection('q', event.target.value)} /></div></div></div>
      <div className="results-meta"><p>{visible.length} shown · {rows.length} loaded on this page</p><span>Oldest first · No total count available</span></div>
      {view === 'board' && <p className="board-explanation">Applications will be grouped by stage when stage tracking is available.</p>}
      {!validOffset ? <div className="empty-state" role="alert"><h2>Invalid page offset</h2><p>Use a whole number from 0 to 10,000.</p><Button onClick={() => selection('offset', '0')}>First page</Button></div>
        : list.isPending ? <p role="status">Loading applications…</p>
        : list.isError ? <div className="empty-state" role="alert"><h2>Applications unavailable</h2><p>{errorMessage(list.error)}</p><Button onClick={() => void list.refetch()}>Retry list</Button></div>
        : visible.length ? view === 'board' ? <StoredBoard applications={visible} search={location.search} /> : <ApplicationList records={visible.map(application => ({ application }))} search={location.search} preview={false} />
        : <div className="empty-state"><h2>{rows.length ? 'No matches on this page' : offset ? 'No applications on this page' : 'No stored applications yet'}</h2><p>{search ? 'Search only covers this loaded page. Clear it or try another page.' : 'Add an application or use the page controls.'}</p>{search && <Button onClick={() => selection('q', '')}>Clear page search</Button>}</div>}
      {validOffset && <nav className="pagination" aria-label="Application pages">
        <Button disabled={offset === 0 || list.isFetching} onClick={() => selection('offset', String(Math.max(0, offset - pageSize)))}>Previous page</Button>
        <span>Offset {offset} · Up to {pageSize} records per page</span>
        <Button disabled={!list.data || list.isError || list.isFetching || rows.length < pageSize || offset + pageSize > 10_000} onClick={() => selection('offset', String(offset + pageSize))}>Next page</Button>
      </nav>}
      {offset + pageSize > 10_000 && <p className="page-description">The API's maximum offset is 10,000. Further pages are unavailable in this version.</p>}
      <footer className="workspace-footer"><span>Search covers this page only. A full page may be followed by an empty page.</span><Link to="/preview/applications">Explore sample Board/List preview</Link></footer>
    </div>
    {id && <Modal key={isNew ? 'new' : id} title={isNew ? 'Add application' : detail.data?.role ?? 'Application details'} subtitle={detail.data?.company} onClose={close} variant={isNew ? 'form' : 'panel'} busy={mutation.isPending} preview={false}>
      {isNew ? <ApplicationForm onAdd={add} onClose={close} mode="stored" /> : <div className="detail-body">
        {saved && <p className="success-note" role="status">Application saved to the database.</p>}
        {!validId ? <p role="alert">Invalid application ID. Use a complete UUID.</p>
          : detail.isPending ? <p role="status">Loading application…</p>
          : detail.isError ? <div role="alert"><p>{errorMessage(detail.error)}</p>{!(detail.error instanceof ApiError && detail.error.kind === 'missing') && <Button onClick={() => void detail.refetch()}>Retry details</Button>}</div>
          : detail.data && <>
            <div className="detail-identity"><CompanyMark company={detail.data.company} /><div><span className="eyebrow">COMPANY</span><strong>{detail.data.company}</strong></div></div>
            <h3>Application overview</h3><dl className="detail-facts"><div><dt><CalendarDays size={16} />Applied date</dt><dd>{formatDate(detail.data.applied_on)}</dd></div><div><dt>Record ID</dt><dd className="record-id">{detail.data.id}</dd></div></dl>
            <p className="detail-preview page-description">Stored in PostgreSQL. This record remains available after reload.</p>
          </>}
        <Button onClick={close}>Back to applications</Button>
      </div>}
    </Modal>}
  </>
}
```

### Complete file: frontend/src/api.test.ts

```typescript
import { afterEach, expect, it, vi } from 'vitest'
import { ApiError, apiBase, createApplication, errorMessage, listApplications } from './api'

afterEach(() => vi.unstubAllGlobals())
it('validates public configuration without echoing it', () => {
  expect(apiBase('http://127.0.0.1:8000')).toBe('http://127.0.0.1:8000')
  for (const value of ['', 'replace-with-local-api-origin', 'https://remote.example', 'http://user:synthetic@localhost:8000', 'http://localhost:8000/?token=synthetic']) {
    expect(() => apiBase(value)).toThrow('configuration')
  }
})
it('maps validation using safe field names without exposing raw input or messages', async () => {
  vi.stubGlobal('fetch', vi.fn().mockResolvedValue(new Response(JSON.stringify({ detail: [
    { loc: ['body', 'company'], type: 'string_too_long', msg: 'synthetic-private', input: 'synthetic-private' },
  ] }), { status: 422 })))
  await expect(createApplication({ company: 'A', role: 'B', applied_on: '2026-01-01' })).rejects.toMatchObject({
    kind: 'validation', fields: { company: 'Use 200 characters or fewer.' },
  })
})
it('does not retry a failed POST and describes its uncertain outcome', async () => {
  const fetchMock = vi.fn().mockRejectedValue(new Error('synthetic-private'))
  vi.stubGlobal('fetch', fetchMock)
  await expect(createApplication({ company: 'A', role: 'B', applied_on: '2026-01-01' })).rejects.toMatchObject({ kind: 'network' })
  expect(fetchMock).toHaveBeenCalledTimes(1)
  expect(errorMessage(new ApiError('network'), true)).toContain('may have been saved')
  expect(errorMessage(new Error('synthetic-private'))).not.toContain('synthetic-private')
})
it('rejects malformed successful responses rather than falling back to fixtures', async () => {
  vi.stubGlobal('fetch', vi.fn().mockResolvedValue(new Response('{}')))
  await expect(listApplications(20, 0)).rejects.toMatchObject({ kind: 'response' })
})
```

### Complete file: frontend/src/api.ts

```typescript
import type { Application, CreateValues } from './data'

export interface ApplicationPage { items: Application[]; limit: number; offset: number }
export type FieldErrors = Partial<Record<keyof CreateValues, string>>
export class ApiError extends Error {
  constructor(public kind: 'configuration' | 'network' | 'server' | 'validation' | 'missing' | 'response', public fields: FieldErrors = {}) {
    super(kind)
  }
}

export function apiBase(value = import.meta.env.VITE_API_BASE_URL ?? 'http://127.0.0.1:8000') {
  try {
    const url = new URL(value)
    if (url.protocol !== 'http:' || !['localhost', '127.0.0.1', '[::1]'].includes(url.hostname) ||
        url.username || url.password || url.search || url.hash || url.pathname !== '/') throw new Error()
    return url.origin
  } catch { throw new ApiError('configuration') }
}

export function errorMessage(error: unknown, writing = false) {
  const kind = error instanceof ApiError ? error.kind : 'network'
  if (kind === 'configuration') return 'Set VITE_API_BASE_URL to the local backend origin, then restart Vite.'
  if (kind === 'validation') return 'Check the highlighted fields and try again.'
  if (kind === 'missing') return 'Application not found.'
  if (writing) return 'Creation could not be confirmed. It may have been saved. Check the application list before submitting again.'
  if (kind === 'server') return 'The server could not load applications. Try again.'
  if (kind === 'response') return 'The server returned an unexpected response. Try again.'
  return 'Cannot reach the backend. Check that it is running, then retry.'
}

function validationFields(body: unknown): FieldErrors {
  const fields: FieldErrors = {}
  const details = (body as { detail?: unknown })?.detail
  if (Array.isArray(details)) for (const item of details) {
    const field: unknown = item?.loc?.at(-1)
    // Never surface raw server messages or echoed input values.
    if (field === 'company' || field === 'role') fields[field] = item.type === 'string_too_long'
      ? 'Use 200 characters or fewer.' : `Enter a valid ${field}.`
    if (field === 'applied_on') fields.applied_on = 'Enter a valid date.'
  }
  return fields
}

async function request(path: string, body?: CreateValues, signal?: AbortSignal): Promise<unknown> {
  const base = apiBase()
  const timeout = AbortSignal.timeout(15_000)
  let response: Response
  try {
    response = await fetch(`${base}${path}`, {
      method: body ? 'POST' : 'GET', credentials: 'omit',
      headers: body ? { 'Content-Type': 'application/json' } : undefined,
      body: body ? JSON.stringify(body) : undefined,
      signal: signal ? AbortSignal.any([signal, timeout]) : timeout,
    })
  } catch { throw new ApiError('network') }
  if (response.status === 404) throw new ApiError('missing')
  if (response.status === 422) {
    let details: unknown
    try { details = await response.json() } catch { details = undefined }
    throw new ApiError('validation', validationFields(details))
  }
  if (!response.ok) throw new ApiError('server')
  try { return await response.json() } catch { throw new ApiError('response') }
}

function application(value: unknown): Application {
  const row = value as Application
  if (!row || !['id', 'company', 'role', 'applied_on', 'created_at'].every(key => typeof row[key as keyof Application] === 'string')) throw new ApiError('response')
  if (!isUuid(row.id) || !/^\d{4}-\d{2}-\d{2}$/.test(row.applied_on) || Number.isNaN(Date.parse(row.applied_on))) throw new ApiError('response')
  return { id: row.id, company: row.company, role: row.role, applied_on: row.applied_on, created_at: row.created_at }
}
export function isUuid(value: string) { return /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i.test(value) }
export async function listApplications(limit: number, offset: number, signal?: AbortSignal): Promise<ApplicationPage> {
  const page = await request(`/applications?limit=${limit}&offset=${offset}`, undefined, signal) as ApplicationPage
  if (!page || !Array.isArray(page.items) || page.limit !== limit || page.offset !== offset) throw new ApiError('response')
  return { items: page.items.map(application), limit, offset }
}
export async function getApplication(id: string, signal?: AbortSignal) { return application(await request(`/applications/${encodeURIComponent(id)}`, undefined, signal)) }
export async function createApplication(values: CreateValues) { return application(await request('/applications', values)) }
```

### Complete file: frontend/src/query.ts

```typescript
import { QueryClient } from '@tanstack/react-query'

export function makeQueryClient() {
  return new QueryClient({ defaultOptions: {
    queries: { retry: false, staleTime: 0, refetchOnWindowFocus: false, networkMode: 'always' },
    mutations: { retry: false, networkMode: 'always' },
  } })
}
```

### Complete file: scripts/run_frontend_integration.py

```python
"""Guarded browser -> FastAPI -> test PostgreSQL checks; no dev writes or DDL."""

from datetime import datetime, timezone
import os
from pathlib import Path
import socket
import subprocess
import sys
import time
from uuid import uuid4

import httpx
from sqlalchemy import delete, func, select, text

from config import load_settings
from database import build_engine, session_scope
from models import JobApplication

ROOT = Path(__file__).resolve().parents[1]
PHASE = "configuration"


def verify_target(engine):
    with engine.connect() as connection:
        if (connection.scalar(text("SELECT current_database()")) != "applysync_test"
                or connection.scalar(text("SELECT current_user")) != "applysync_test"
                or connection.scalar(text("SELECT version_num FROM alembic_version")) != "0001"):
            raise RuntimeError("Refusing an unverified integration database target.")


def serve(port):
    import uvicorn
    from main import create_app
    engine = build_engine(load_settings("test"))
    verify_target(engine)
    app = create_app("test")
    app.state.engine = engine
    uvicorn.run(app, host="127.0.0.1", port=port, access_log=False)


def run():
    global PHASE
    engine = build_engine(load_settings("test"))
    process = None
    marker = f"Synthetic Browser {uuid4()}"
    verified = False
    try:
        verify_target(engine)
        verified = True
        PHASE = "test fixture creation"
        # Enough owned fixtures to exercise real pagination, even in a nonempty DB.
        with session_scope(engine) as session:
            for i in range(21):
                session.add(JobApplication(company=f"{marker} seed {i:02}", role="Engineer",
                    applied_on=datetime(2026, 9, 1).date(),
                    created_at=datetime(1900, 1, 1, tzinfo=timezone.utc)))
        with socket.socket() as probe:
            probe.bind(("127.0.0.1", 0))
            port = probe.getsockname()[1]
        origin = f"http://127.0.0.1:{port}"
        PHASE = "isolated API startup"
        print("Verified test target; starting isolated API.", flush=True)
        process = subprocess.Popen([sys.executable, "-c",
            f"from scripts.run_frontend_integration import serve; serve({port})"],
            cwd=ROOT, stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL, creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))
        with httpx.Client(trust_env=False, timeout=2) as client:
            deadline = time.monotonic() + 20
            while True:
                if process.poll() is not None:
                    raise RuntimeError("Isolated test API did not start.")
                try:
                    response = client.get(origin + "/health")
                    if response.status_code == 200:
                        break
                except httpx.TransportError:
                    pass
                if time.monotonic() > deadline:
                    raise RuntimeError("Isolated test API startup timed out.")
                time.sleep(.1)
        env = {**os.environ, "APPLYSYNC_E2E_RUN_ID": marker,
               "APPLYSYNC_E2E_API_ORIGIN": origin, "VITE_API_BASE_URL": origin}
        command = ["cmd.exe", "/d", "/c", "npm.cmd", "run", "test:integration"] if os.name == "nt" else ["npm", "run", "test:integration"]
        PHASE = "browser checks"
        print("Isolated API healthy; running browser checks.", flush=True)
        result = subprocess.run(command, cwd=ROOT / "frontend", env=env,
                                stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True,
                                creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))
        print(result.stdout, flush=True)
        if result.returncode:
            raise RuntimeError("Browser integration checks failed; see test output.")
        PHASE = "committed record verification"
        with session_scope(engine) as session:
            row = session.scalar(select(JobApplication).where(JobApplication.company == marker + " created"))
            if row is None or row.role != "Browser Engineer" or row.applied_on.isoformat() != "2100-01-01":
                raise RuntimeError("Committed browser record was not verified in PostgreSQL.")
        print("PASS: committed browser-created values independently verified in test PostgreSQL.")
    finally:
        if process is not None:
            if process.poll() is None:
                process.terminate()
            try:
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait(timeout=5)
        try:
            if verified:
                verify_target(engine)  # Recheck before any cleanup.
                with session_scope(engine) as session:
                    session.execute(delete(JobApplication).where(JobApplication.company.startswith(marker)))
                with session_scope(engine) as session:
                    remaining = session.scalar(select(func.count()).select_from(JobApplication).where(JobApplication.company.startswith(marker)))
                    if remaining != 0:
                        raise RuntimeError("Owned fixture cleanup was incomplete.")
                print("PASS: only this run's uniquely marked test records cleaned up; target reverified.")
        finally:
            engine.dispose()


if __name__ == "__main__":
    try:
        run()
    except Exception as error:
        # Never expose raw configuration, connection URLs or database exceptions.
        print(f"Integration verification failed during {PHASE} ({type(error).__name__}, OS code {getattr(error, 'winerror', None)}). Check dedicated test setup and test results; private details suppressed.")
        sys.exit(1)
```

### Complete file: tests/test_cors.py

```python
import asyncio

import httpx
import pytest

import database
from config import ConfigurationError
from main import create_app


@pytest.mark.parametrize("host", ["localhost", "127.0.0.1"])
@pytest.mark.parametrize("port", [5173, 4173])
def test_local_origin_preflight_and_errors(host, port, monkeypatch):
    origin = f"http://{host}:{port}"

    def unavailable(*args):
        raise ConfigurationError("synthetic-private-details")

    monkeypatch.setattr(database, "load_settings", unavailable)

    async def check():
        async with httpx.AsyncClient(transport=httpx.ASGITransport(app=create_app()),
                                     base_url="http://test") as client:
            response = await client.options("/applications", headers={
                "Origin": origin, "Access-Control-Request-Method": "POST",
                "Access-Control-Request-Headers": "content-type"})
            assert response.status_code == 200
            assert response.headers["access-control-allow-origin"] == origin
            assert "access-control-allow-credentials" not in response.headers
            health = await client.get("/health", headers={"Origin": origin})
            assert health.json() == {"status": "healthy"}
            failed = await client.get("/applications", headers={"Origin": origin})
            assert failed.status_code == 500
            assert failed.headers["access-control-allow-origin"] == origin
            assert failed.json() == {"detail": "Internal server error"}
    asyncio.run(check())


@pytest.mark.parametrize("origin,method", [("https://unapproved.example", "POST"),
                                             ("http://localhost:5173", "DELETE")])
def test_disallowed_cors_preflight(origin, method):
    async def check():
        async with httpx.AsyncClient(transport=httpx.ASGITransport(app=create_app()),
                                     base_url="http://test") as client:
            response = await client.options("/applications", headers={
                "Origin": origin, "Access-Control-Request-Method": method})
            assert response.status_code == 400
            if origin == "https://unapproved.example":
                assert "access-control-allow-origin" not in response.headers
    asyncio.run(check())
```

### Complete file: schemas.py

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

### Complete file: applications.py

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

### Complete file: database.py

```python
"""Engine creation and explicit commit/rollback boundaries."""

from contextlib import contextmanager

from fastapi import Request
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session

from config import DatabaseSettings, load_settings


def build_engine(settings: DatabaseSettings) -> Engine:
    return create_engine(settings.url(), pool_pre_ping=True, echo=False,
                         hide_parameters=True, connect_args={"connect_timeout": 5})


def get_engine(request: Request) -> Engine:
    """One lazily initialized engine per app; health needs no configuration."""
    state = request.app.state
    with state.engine_lock:
        if state.engine is None:
            state.engine = build_engine(load_settings(state.database_target))
        return state.engine


@contextmanager
def session_scope(engine: Engine):
    # begin() commits on success and rolls back on exceptions; close always runs.
    with Session(engine) as session:
        with session.begin():
            yield session
```

### Complete file: models.py

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
