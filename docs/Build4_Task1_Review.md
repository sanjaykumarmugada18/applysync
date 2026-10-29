# Build 4 Task 1 review: Gmail connection and disconnection

## Checkpoint approval and live verification update

Sanjay reports that **all live connect, disconnect and reconnect checks passed**.
These are user-reported results, not independent agent execution. This supersedes
the original handoff's pending live-connect/disconnect setup item. It does not
claim independent inspection of Google-side revocation, additional failure cases,
or completion of any learning exercise.

Before saving this checkpoint, all 27 file hashes below matched the current
source, tests, configuration, README and intentional screenshots. No executable
code or dependency configuration changed since verification. Reused historical
agent evidence: 122 backend tests, 31 component tests, 10 Chromium checks,
typecheck/production build, and one real two-account browser/database regression.
No database access, ownership assignment or provider calls are needed for this
checkpoint. The two unassigned legacy records and pending learning items remain
as previously documented.

The user explicitly authorized a local commit and normal push. The pre-commit
branch is `main`, base HEAD is `58d86b6555822c51c69bd3a9b700da17826cb5fb`,
and the intended commit message is `Add Gmail connection and disconnection`.
Only this review update differs from the verified snapshot. Final Git/secret and
staged whitespace checks accompany the commit; its identifier and live remote
verification are reported separately after execution rather than predicting them
inside the commit itself.

Planning & Progress: Build 4 Task 1 has passed reported live checks and is approved
for saving. Build 4 remains in progress. Label/filter setup verification is the
next bounded task; it has not started. Learning exercises remain pending.

## Historical implementation handoff

The following records the original pre-approval state and its verification.
Statements about uncommitted work, missing local setup and unperformed live checks
below describe that earlier point in time; the checkpoint update above supersedes
them where specified. Source snapshots remain unchanged.

Recorded 29 October 2026. Implementation and mocked verification are ready for
review and Google Cloud local configuration. **Live Google OAuth has not been
verified. Build 4 Task 2 has not started.** No messages, labels, filters, bodies,
threads or attachments were retrieved. No classification, sync, workers, stages,
auth redesign or deployment was added.

## Repository and evidence provenance

- Branch `main`; base and current HEAD `58d86b6555822c51c69bd3a9b700da17826cb5fb`,
  `Add authentication and application ownership`.
- Origin `https://github.com/sanjaykumarmugada18/applysync.git`. Live main was
  checked at task start and matched that commit. No commit or push in this task;
  remote state at final handoff has not been re-fetched and is not newly asserted.
- Task started with a clean tree. All changes listed below belong to Task 1;
  index remains empty, implementation is unstaged, new files are untracked.
- `.env` remains ignored and absent from Git. No existing secret values were
  displayed; normal configuration loading was used for database connections and
  a safe Gmail-availability check. This task did not run `setup_gmail` or replace
  local credentials. Dependencies/build outputs/test artifacts remain ignored.
- Read root `AGENTS.md`, Build 3 review and current source, original Task 1 and
  resume attachments, and actual v2.0 PDF pages 8-10 and 18 for Gmail architecture
  and active stage. Working-agreement pages 3, 6-7 were previously read. The PDF
  was successfully extracted, not inferred from the working guide.
- Before the resume message, the connector/routes/models/migration and initial
  UI existed; migration preservation and 120 backend tests had passed. The
  frontend test-only `exact` option mismatch was fixed without dropping the
  assertion. After that, final UI behavior, extra concurrency tests, documentation,
  fresh verification, screenshots and startup were completed.
- Earlier Build 3 manual authentication checks remain **user-reported**; no live
  Google checks by Sanjay are claimed. Pending transaction/request-flow and other
  learning exercises have not been marked complete.

## Changed files and responsibilities

| Files | Responsibility |
| --- | --- |
| `gmail_connector/__init__.py`, `gmail_connector/client.py` | Narrow provider boundary: fixed endpoints, configuration, authorization URL, S256 PKCE, code/refresh exchange, RS256 identity verification, Fernet encryption, revoke. |
| `gmail_routes.py` | Current-user status/start/callback/disconnect; transaction boundaries, session/state checks, locking, safe response/redirect contract. |
| `models.py` | One connection per owner and latest pending OAuth state per owner. No modifications to old entity fields. |
| `migrations/versions/0003_gmail_connection.py` | Add only the two new tables, ownership/session foreign keys, status constraint and unique/primary keys. |
| `main.py` | Register routes; no-store/referrer protections and suppress callback access-log lines. Existing Origin/CSRF/CORS and generic DB error handlers reused. |
| `requirements.txt` | Pin `cryptography==50.0.2`; retain all existing versions. |
| `.env.example`, `scripts/setup_gmail.py` | Placeholder contract and append-only local setup helper; generate a separate encryption key without displaying it. |
| `frontend/src/GmailSettings.tsx` | Status/query UI, guarded start/disconnect, safe result notices, query invalidation, abort-on-unmount and fixed Google destination validation. |
| `frontend/src/App.tsx`, `Auth.tsx`, `api.ts` | Protected settings route, safe return path after login, session-expiry handling for Gmail calls. |
| `frontend/src/components/Shell.tsx`, `styles.css` | Settings navigation and card using the existing light/purple design; active links, responsive actions, generic skip link. Application views remain intact. |
| `tests/test_gmail.py` | Test-DB orchestration/state/isolation/CSRF/CORS/refresh/disconnect/concurrency checks with a fake connector. |
| `tests/test_gmail_connector.py` | Real cryptography/signatures with in-memory HTTP transport; PKCE, identity rejection, encryption, provider failure, config, access-log filtering and import-boundary assertions. |
| `tests/test_gmail_migration.py` | Isolated rollback-only schema rehearsal preserving users, sessions, owned and unassigned applications across 0002 -> 0003. |
| `tests/conftest.py`, `scripts/run_frontend_integration.py` | Require dedicated test database/user at 0003 before test writes. |
| `tests/test_ownership_migration.py` | Keep original Build 3 migration assertions scoped explicitly to 0002 instead of the moving head. No assertion removed. |
| `frontend/src/GmailSettings.test.tsx`, `frontend/e2e/gmail.spec.ts` | Component and Chromium state/CSRF/failure/unmount/mobile checks; fake Google only. |
| `frontend/e2e/integration.spec.ts` | Real application regression screenshots default to ignored test output instead of overwriting historical Build 3 evidence. |
| `README.md`, this review | Reproducible configuration, contract, limitations and exact review snapshot. |
| `docs/screenshots/Build4_Task1/gmail-connected.png`, `gmail-mobile.png` | Intentional synthetic desktop/mobile screenshots, freshly rendered and visually inspected. No real accounts or credentials. |

## Contract and execution paths

`GET /gmail` returns only `available`, safe `status`, own connected `email` and
`revocation_warning`. Status is not a live provider-health probe. Missing Gmail
configuration reports `available:false`; start returns generic 503. Existing
health/authentication/application functionality does not require Google config.

`POST /gmail/start` requires the existing authenticated cookie, an exactly trusted
Origin, and `X-ApplySync-CSRF: 1`. It returns `authorization_url` for a fixed Google
host/path; the frontend allowlists that destination. OAuth's random state and
public client metadata necessarily travel in that URL, but no state database row,
PKCE verifier, nonce secret store, client secret or refresh token is serialized.

**Success path:** `GmailSettings.act('start')` -> `api.request` credentialed POST ->
`auth.current_user` -> `gmail_routes.start`/`lock_owner` -> `GmailConnector.begin`.
State hash, encrypted verifier/nonce and user/session/expiry are committed before
returning the authorization URL. Google redirects to `/gmail/callback`.
`gmail_routes.callback` validates state and marks it used in a committed transaction
**before** exchange. A second transaction rechecks and locks user/session and
confirms the pending flow still exists. `GmailConnector.exchange` validates the
Google signature/identity/scopes and encrypts any refresh token. The route commits
only the current owner's grant, then redirects to fixed settings `?result=connected`.
The settings query displays safe fields. No message request occurs.

**Failure path:** a denied or missing-code callback still consumes valid state;
replay is rejected before exchange. Invalid provider identity/scopes produce a
fixed `ConnectorError`; no grant is stored and the frontend receives only
`?result=failed`. For disconnect, `gmail_routes.disconnect` clears the local grant
and pending state, invokes `GmailConnector.revoke`, and commits `disconnected`
even when the provider request times out/fails. UI invalidates its query and shows
an auditable stored warning with a Google account-connections link. No raw provider
error or token is returned. Session/SQL failures retain existing generic errors.

## Security and open-choice decisions

- **Bound state:** 32 random bytes (43 URL-safe characters), SHA-256 hash in DB,
  ten-minute lifetime, owner+session foreign keys, single-use `used_at`, encrypted
  flow removed on consumption. A new start replaces the old pending flow. Owner
  row locking serializes starts/callbacks/disconnects. Session row locking makes
  logout serialize with exchange; logout deletes the pending state by cascade.
  An already committed Gmail connection persists across ApplySync logout.
- **PKCE:** S256 with a fresh 64-byte random verifier. Google discovery explicitly
  advertises S256. The native authorization-code documentation defines the
  verifier/challenge exchange; the web-server guide supplies the confidential
  client/offline flow. The connector sends the original decrypted verifier to the
  fixed token endpoint. Google performs verifier validation; our fake endpoint
  independently recomputes the hash in tests. Live provider acceptance remains
  unverified, not inferred from those tests.
- **Identity/scopes:** request only `gmail.readonly`, `openid`, `email`; normalize
  Google's `userinfo.email` alias. Reject missing or additional grants. Verify
  RS256 against the fixed Google JWKS endpoint, issuer, audience, expiration,
  issued-at, nonce, verified email, immutable `sub`, and `azp` if present. Do not
  follow token-provided key URLs. Email is display metadata; stable `sub` controls
  same-account identity. The minimal OIDC scopes avoid inferring identity from
  email spelling or a mailbox fetch.
- **Cookies and browser security:** existing eight-hour HttpOnly, SameSite=Lax
  app JWT plus revocable server session. Local HTTP deliberately has Secure off;
  existing production mode requires HTTPS/Secure, but this Gmail flow is local
  only. SameSite=Lax permits Google's top-level GET callback. That callback is
  exempt from the write-only custom header requirement and instead requires
  state/session/PKCE. All other writes use exact Origin/custom-header checks.
  Existing credentialed CORS stays limited to configured explicit origins (default
  loopback localhost/127.0.0.1 ports 5173/4173); no wildcard or untrusted preflight.
  Gmail redirects/config use **127.0.0.1 only**, frontend5173/backend8000.
- **Storage:** Fernet authenticated encryption with a separate generated key for
  refresh token and ephemeral verifier/nonce; access and ID tokens are memory-only.
  State is not the login cookie. One connection row per owner (owner primary key),
  one pending flow per owner (unique constraint). Existing refresh ciphertext is
  preserved on omitted refresh only for the same connected subject and a successful
  refresh validation. Invalid-grant marks reauthorization needed; transient provider
  errors preserve existing data. No background refresh or mailbox clients yet.
- **Different account:** reject silent replacement, preserve existing connection,
  require explicit disconnect first. A denied replacement may leave Google-side
  consent for the other account; remove that consent in Google account connections
  if unwanted. The app does not store/use the rejected grant or revoke the original.
- **Disconnect timing:** owner/session locks cover the bounded provider call. Local
  fields are cleared before revocation in the transaction, but **durability occurs
  on commit after the call**, not in an earlier independent commit. Provider failure
  is caught and commits a warning. Concurrent disconnects perform one revocation;
  subsequent requests preserve the warning without recreating credentials. The
  erased token cannot be retried server-side; manual removal in Google completes
  provider-side cleanup. Crash/database commit failure leaves uncertain results;
  refresh status before acting. Google revocation may affect grants under the same
  Google project; use a dedicated development OAuth project.
- **Errors/logs:** fixed exception text and safe callback result codes; hide SQL
  parameters, no token-bearing request URLs to Google, no raw provider body logging.
  Callback responses have no-store/no-referrer; Uvicorn access filter drops callback
  lines even if access logging is enabled. Documented startup disables access logs.
  No trace/video capture of live OAuth; don't export browser callback URLs. These
  controls cover project logging, not arbitrary external proxy/browser tooling.
- **Account changes:** settings runs inside existing identity-keyed `PrivateCache`;
  logout unmounts/clears it. Query cancellation and mutation AbortController prevent
  delayed old responses from redirecting or displaying data after account change.
  Mutation/query errors are generic. Notices are cleared when starting a new action.
- **Boundary:** only `gmail_connector` imports token cryptography or implements
  Google requests. Routes orchestrate safe connector operations. Architecture tests
  scan application Python recursively excluding tests/migrations/tooling and fail
  on Google SDK/crypto imports or provider endpoint leakage outside the connector.
  This is code organization, not a runtime sandbox. No classifier exists here.

## Migration and preserved data

Inspected `migrations/versions/0003_gmail_connection.py` and generated SQL from:

```powershell
.\.venv\Scripts\python.exe -m alembic -x target=test upgrade 0002:0003 --sql
```

SQL contained only CREATE TABLE/constraints for `gmail_connections` and
`gmail_oauth_states` plus Alembic version update. Applied via Alembic on supplied
transactions for the verified application roles/database pairs `applysync_dev`
and `applysync_test`, not an administrator. Before/after comparisons held full
pre-existing users, sessions and application rows in memory without output.
Every value compared equal. Both databases became `0003`; repeated `upgrade head`
was a no-op and `alembic.command.check` reported no new upgrade operations.
Development had **two unassigned legacy applications before and after**; no
assignment/deletion/update was performed. Test DB had zero unassigned records.

After the resume message these checks were repeated at 0003: exact database/user,
revision, before/after row equality across no-op upgrade, model consistency,
connection primary key and presence of encrypted refresh/no access-token column.
Both passed; development still has two unassigned legacy rows. The fresh automated
migration rehearsal additionally seeds users/sessions/owned+unassigned applications
in a unique transient schema at 0002, upgrades twice, compares complete rows and
rolls the schema back. Downgrade is intentionally blocked pending an explicit
preservation plan. Existing migration files are unchanged.

## Verification ledger

All following final results were executed by the agent on this Windows workspace,
not independently rerun or manually verified by Sanjay. No skipped tests in the
full backend/frontend runs.

| Command/check | Observed result and boundary |
| --- | --- |
| `.venv\Scripts\python -m pip install cryptography` | Installed 50.0.2 Windows abi3 wheel in existing Python3.14.2 environment; retained existing dependencies. Pinned in manifest. |
| `.venv\Scripts\python -m pip check` | No broken requirements found; repeated after implementation. |
| `.venv\Scripts\python -m pytest --run-db -q -p no:cacheprovider --tb=short` | **122 passed, 2 warnings, 18.01s**, final backend/test source. All Google calls faked; real test PostgreSQL. Includes real Uvicorn restart test from earlier builds. |
| `npm.cmd run build` in frontend | **Passed**; includes `npm run typecheck` (`tsc --noEmit`), then Vite7.3.6 production build, 1956 modules, 2.77s final build. |
| `npm.cmd test` | **31 passed, 6 files, 4.97s**, final UI source. |
| `npm.cmd run test:e2e` | **10 Chromium checks passed, 10.2s**; 9 existing checks + new Gmail state/mobile test. HTTP/Google mocked; no live provider request. Zero page errors asserted for Gmail. |
| `.venv\Scripts\python -m scripts.run_frontend_integration` | **1 passed, 16.6s**; real Uvicorn, browser and test PostgreSQL, two-account create/reload/isolation/logout. Committed values independently verified; only uniquely marked fixtures cleaned. No Gmail calls. This ran before a final Gmail-only notice/heading change; affected UI checks were rerun afterward. |
| Migration SQL, application, repeat upgrade, model check | Both dev/test0003; no model drift, existing rows equal, two legacy development records unchanged/unassigned. Repeated after resume. |
| Live local HTTP | Backend8000 `/health`200 with healthy JSON; unauthenticated `/auth/me` and `/gmail`401. Frontend5173 `/login`, `/register`, `/settings/gmail`200. Servers remain running. HTML response is separate from browser rendering evidence. |
| Gmail local configuration probe | `GmailUnavailable`, reported generically. No secret values output; normal app starts. Unit/API tests verify unavailable state/503 start and unaffected applications/health. |
| Visual inspection | Opened final desktop connected and mobile disconnected synthetic PNGs. Readable approved light/purple layout, contained mobile card/actions, restored navigation focus. |
| Standalone local helper/config checks | Temporary fixture confirmed append-only helper idempotence and preservation; synthetic valid config accepted, wrong redirect hostname/frontend origin, malformed key and placeholder rejected. No real .env changed or Google requests. |
| Git/secret/whitespace | Empty index; `.env` ignored/untracked. `git diff --check` passed (only LF/CRLF normalization notices). Changed/new text scanned for credential/token/private-key/authenticated-DB-URL patterns without printing values; no matches. New-file trailing whitespace check also passed. |

The earlier **120 passed** backend result is historical, superseded by122 after
adding explicit concurrent callback/disconnect and callback/logout tests. Earlier
Build3 88/26/9 results are historical regression context, not current proof.
Initial frontend typecheck failed because Testing Library's role query does not
accept `exact`; removing that unsupported option preserved exact string-name
matching and the useful assertion. Final typecheck passed. One inspection command
used a nonexistent test filename and one helper invocation used the wrong working
directory; both were corrected without data/source loss. A standalone helper check initially hit sandbox temporary-directory permissions; rerunning with normal local permissions passed. No pending failed checks.
Warnings: existing Starlette/httpx TestClient and AnyIO alias deprecations; Playwright
NO_COLOR/FORCE_COLOR environment notices. No unrelated dependency update was made.

Important assertions inspected: committed one-use state before exchange; replay
and wrong-user/session cause no exchange; signed wrong issuer/audience/nonce,
expired/unverified identity and extra scopes rejected; test PKCE recomputation;
actual Fernet decrypt/encrypted inequality; omitted refresh preserves exact old
ciphertext; different subject retains old email; concurrent disconnect invokes
provider once; callback/logout serialization ends unauthenticated; foreign account
stays connected; no raw provider markers in captured logs; fixture target checks
before writes and cleanup; aborted late start cannot navigate after logout.

## Official documentation and local setup

Official primary sources read for this implementation:

- [Google web-server OAuth](https://developers.google.com/identity/protocols/oauth2/web-server): confidential client code exchange, offline consent/refresh, state and revoke.
- [Google authorization-code PKCE](https://developers.google.com/identity/protocols/oauth2/native-app): verifier/S256 exchange mechanics.
- [Google discovery metadata](https://accounts.google.com/.well-known/openid-configuration): actual S256 support, issuer, JWKS and token/revoke endpoints.
- [Google OpenID Connect](https://developers.google.com/identity/openid-connect/openid-connect): signed identity validation, nonce and stable sub.
- [Gmail scopes](https://developers.google.com/workspace/gmail/api/auth/scopes): readonly restricted scope; no modify/send/full-mail scope.
- [Consent setup](https://developers.google.com/workspace/guides/configure-oauth-consent): Branding, Audience, Data Access and test users.
- [OAuth client creation](https://developers.google.com/workspace/guides/create-credentials): Clients, Web application and exact redirect URI. Protocol/client-secret handling follows the more specific web-server OAuth flow.
- [Fernet](https://cryptography.io/en/latest/fernet/): authenticated encryption, secret key generation/handling. Token timestamp is visible metadata; raw credentials are not.

[README: One-time Google Cloud setup](../README.md#one-time-google-cloud-setup)
contains the complete ordered console/local instructions. Immediate next action:
open Google Cloud Console and create/select a dedicated ApplySync development
project, then enable Gmail API in APIs & Services > Library. Configure Branding,
External/Testing Audience + intended test users, the exact three Data Access
scopes, and a Web application client. Redirect is exactly
`http://127.0.0.1:8000/gmail/callback`. JavaScript origins are unnecessary for this
server-side flow (leave empty); the app frontend is `http://127.0.0.1:5173`.

Run `.venv\Scripts\python -m scripts.setup_gmail`; enter ID/secret **only in local
root .env**. Required names (examples are placeholders only):

```dotenv
APPLYSYNC_GOOGLE_CLIENT_ID=replace-with-web-client-id.apps.googleusercontent.com
APPLYSYNC_GOOGLE_CLIENT_SECRET=replace-with-web-client-secret
APPLYSYNC_GOOGLE_REDIRECT_URI=http://127.0.0.1:8000/gmail/callback
APPLYSYNC_GMAIL_ENCRYPTION_KEY=replace-with-generated-fernet-key
APPLYSYNC_GMAIL_FRONTEND_ORIGIN=http://127.0.0.1:5173
```

Use the helper-generated key, never the placeholder or authentication secret.
Existing values are not replaced. Keep `.env` private; never send credentials,
cookies, tokens or callback URLs to chat. No Google Cloud project/client/test-user
setup or live consent/revocation has been performed by the agent.

## Limitations, remaining checks and learning

- **Blocked/user-required:** complete local Google configuration, live consent,
  account address and reload confirmation, live disconnect/provider revocation,
  and denial/retry behavior. No successful live OAuth claim. Readonly permission is
  mailbox-wide, but Task1 reads no mail. Label/filter verification is still Task2.
- Provider revoked/expired grants are discovered on later validation, not by
  background polling; connected status means a stored grant, not a continuous
  assurance. No Gmail API client operations or automatic refresh scheduler exist.
- State storage is bounded to one row per owner; expired entries are rejected and
  replaced by next start or removed on session deletion/disconnect. No cleanup job.
- Encryption-key rotation/recovery, production HTTPS redirects, provider app
  verification and deployment remain outside this local task. Do not deploy these
  fixed loopback settings unchanged. No automatic provider-revocation retry after
  local token erasure.
- Existing nullable ownership deliberately preserves the two legacy applications;
  no ownership finalization performed. Earlier learning exercises remain pending.
- Focused learning checkpoint (not performed): after local setup, start a connection
  and cancel Google consent. Observe the safe retry message and identify where
  `gmail_routes.callback` commits `used_at` before examining denial. Explain why a
  fresh start is required instead of retrying the old callback. Do not copy its URL.
- Planning & Progress: Task1 code/mocked checks are delivered for review; live Google
  verification and learning remain. Only after acceptance should Task2 begin Gmail
  setup verification. Nothing has been committed/pushed in this task.

## Reviewable source snapshot

The appendices below include every changed tracked-text diff and complete new
source/test/migration file. Snapshot SHA-256 values let a later review detect
changes without assuming that a progress message proves source identity. Review
markdown itself is excluded from its own hash to avoid recursion; binary evidence
is linked/listed rather than encoded. No `.env` or private logs are included.

### Snapshot hashes

| File | SHA-256 |
| --- | --- |
| `.env.example` | `b9f60d2358ddb22aeaf8e031ae6f7c8832e06d5865a023870ffb522a0a36ce23` |
| `README.md` | `377f2e0d1eaa2c333e3f2d0eb8ecb41ee052ad7aeb2dfacdf29313bb3dbea31a` |
| `docs/screenshots/Build4_Task1/gmail-connected.png` | `a62cc5b4185ef5e7eaf59e2dca5e06d32efadc722fc97c698117a0e4f0494e83` |
| `docs/screenshots/Build4_Task1/gmail-mobile.png` | `1ace5c88a186228d01b333d2733b1fb4ca14e1490c7ad1d464709e9997c98f47` |
| `frontend/e2e/gmail.spec.ts` | `3ae955bc6b2fdcb40fb3208c3e3bc7295b803d0e8ba500d8fa90a404c59f0f1b` |
| `frontend/e2e/integration.spec.ts` | `adca5c7540d66583dc5aa645071a20a9540a953a2f57f394172825ed6252769c` |
| `frontend/src/App.tsx` | `1677cff7c3f439f7f065bffdc1472ef8ff672b3d176d2e84b88938955fbb4dc1` |
| `frontend/src/Auth.tsx` | `642238e3916055e334bb6797eed0b1b15166c7718ff940ccf2d590a5db084fd9` |
| `frontend/src/GmailSettings.test.tsx` | `25d20795f757e6736eaaa49114b3d0d3f859a541953780c328821e3a47d6d9a0` |
| `frontend/src/GmailSettings.tsx` | `690e915e9b55d5fc5a11c4aa48220030cd8eb3d6d722514c0d38b6c18b3adf25` |
| `frontend/src/api.ts` | `87f7e68e09539c0eacb69d820f3fb41157c2d423ff75fdb6fe5edb68ee93ba03` |
| `frontend/src/components/Shell.tsx` | `a111426dbf7b2e90cf6f3a0aa4575a3b0b2261c18fd1226a77f0925c91ce256f` |
| `frontend/src/styles.css` | `7cf42934f96b36f570447fca72fef6bc443841bd6d3fabac0b9bedb59322da55` |
| `gmail_connector/__init__.py` | `1cd89af0aeff2b396a746cd2b3dee9175889363ffdc23d9f1024b83f27149d81` |
| `gmail_connector/client.py` | `f97f35259ea201224b9f95577d76db6979941ad32eed7f2eea285a2bc1d4ac30` |
| `gmail_routes.py` | `9894a285ff83e750aa0401137ead967bfbe0e577b408729c338a81cba4829940` |
| `main.py` | `b0924fcd1975a17da28f44317c6b023138b7fba6a1e696bea45d395b5d92f9cd` |
| `migrations/versions/0003_gmail_connection.py` | `3ef21cf896335623e5102458846c0a86046ea3e655b36b815e2e40d7feb3b7b3` |
| `models.py` | `4d25593564a2fd2bc5742b2452d183de4cf2c6aed7e759cbbe7ff77e0fbc8301` |
| `requirements.txt` | `8cf1b2a6e159d8e3d8644579928006e8a57543355d178504b976b262b8cd6023` |
| `scripts/run_frontend_integration.py` | `c881fa0d524d9661b20d2f5b0d29d93830aab050a7d8e7743817e020da70f133` |
| `scripts/setup_gmail.py` | `56efd77fb9825733da08c7e939b2071303a87fc524583b6e03e0d0bc8e902c85` |
| `tests/conftest.py` | `677c52f155fd7c96235b25f3a90e04168deec5e5b72b5d1dda68edce8cd68e35` |
| `tests/test_gmail.py` | `d17803b1330c9f5d89b74b3c883827f108d694b4448ef495f41a14eef20457e0` |
| `tests/test_gmail_connector.py` | `00f167d39efe6cefbe63a301182378311d6493a5e71a383ad3a07332d72705e7` |
| `tests/test_gmail_migration.py` | `d18aaed5f01d14b64bb5cb53b717aca5b6bb9813d79f564884a9cd00f4e72e1a` |
| `tests/test_ownership_migration.py` | `de33ead965a569f6c38a1291eb4ee8c215a319d0da74e0762238f5be76b702c8` |

### Tracked text diffs

```diff
diff --git a/.env.example b/.env.example
index d152890..06b588a 100644
--- a/.env.example
+++ b/.env.example
@@ -11,3 +11,9 @@ APPLYSYNC_TEST_DB_PASSWORD=replace-with-local-test-password
 APPLYSYNC_AUTH_SECRET=replace-with-generated-64-hex-characters
 APPLYSYNC_AUTH_MODE=local
 APPLYSYNC_AUTH_ORIGINS=http://127.0.0.1:5173,http://127.0.0.1:4173,http://localhost:5173,http://localhost:4173
+# Gmail is optional; generate a separate key with python -m scripts.setup_gmail.
+APPLYSYNC_GOOGLE_CLIENT_ID=replace-with-web-client-id.apps.googleusercontent.com
+APPLYSYNC_GOOGLE_CLIENT_SECRET=replace-with-web-client-secret
+APPLYSYNC_GOOGLE_REDIRECT_URI=http://127.0.0.1:8000/gmail/callback
+APPLYSYNC_GMAIL_ENCRYPTION_KEY=replace-with-generated-fernet-key
+APPLYSYNC_GMAIL_FRONTEND_ORIGIN=http://127.0.0.1:5173
diff --git a/README.md b/README.md
index 0ebe5eb..7712c40 100644
--- a/README.md
+++ b/README.md
@@ -1,10 +1,11 @@
 # applysync
 AI-powered privacy-first job application tracker that automatically syncs Gmail application emails into a Kanban dashboard.

-Current scope: Build 3 adds registration, login, revocable JWT-cookie sessions and
+Current scope: Build 4 Task 1 adds optional Gmail connection/disconnection settings,
+with no message reading or synchronization. Build 3 supplies registration, login, revocable JWT-cookie sessions and
 server-side ownership to the integrated PostgreSQL create/list/detail APIs. `/applications` displays stored data; the explicitly separate
-`/preview/applications` retains the fictional Board/List preview. Gmail and automatic
-tracking above describe the project goal, not implemented features. This remains local development functionality, not a public deployment.
+`/preview/applications` retains the fictional Board/List preview. Automatic
+tracking above describes the project goal, not an implemented feature. This remains local development functionality, not a public deployment.
 Read the Build 3 setup and security policy below before starting the backend.

 ## Build 3 setup and session policy
@@ -510,3 +511,133 @@ frontend, submit a whitespace-only company and locate the string constraint in
 `schemas.py`. Direct unauthenticated PowerShell POSTs now fail request protection
 or authentication first. The detailed request-flow and earlier transaction
 exercises remain pending; this task does not claim they were completed.
+
+
+## Build 4 Task 1: Gmail connection setup (local only)
+
+The settings page is **http://127.0.0.1:5173/settings/gmail**. Sign in to
+ApplySync first at **http://127.0.0.1:5173/login**. Google authorization is a
+separate connection, not an alternative ApplySync login. Missing Gmail settings
+leave health, authentication and manual tracking available.
+
+Existing databases have been upgraded to `0003` in this workspace. For another
+checkout, inspect `python -m alembic upgrade 0002:0003 --sql`, then run the ordinary
+`upgrade head` for dev and `-x target=test upgrade head` for test. Do not provision
+or reset an existing database. The new migration only adds two Gmail tables.
+
+### One-time Google Cloud setup
+
+1. Open [Google Cloud Console](https://console.cloud.google.com/) and create/select
+   a dedicated ApplySync development project. In **APIs & Services > Library**,
+   find **Gmail API**, then **Enable**. No API key or service account is required.
+2. Open **Google Auth platform > Branding**. Choose **Get Started** if needed;
+   set the app name to ApplySync development, select your support email, provide
+   your contact email and complete the consent setup. Choose **External** for a
+   personal Gmail account.
+3. In **Audience**, retain **Testing** status. Under **Test users > Add users**, add
+   only the Google accounts you intend to test with. Save; do not publish the app.
+4. In **Data Access > Add or Remove Scopes**, select only `openid`, `email`
+   (the Console may display `https://www.googleapis.com/auth/userinfo.email`), and
+   `https://www.googleapis.com/auth/gmail.readonly`. Save. Readonly is a restricted
+   mailbox-wide scope; a label is not an OAuth restriction. This task makes no
+   mailbox requests. Public release/verification is outside this task.
+5. In **Clients > Create Client**, choose **Web application**, name it ApplySync
+   local, and add exactly this **Authorized redirect URI**:
+   `http://127.0.0.1:8000/gmail/callback`. This is a server-side code flow, so
+   **Authorized JavaScript origins can remain empty**. The frontend origin used
+   by ApplySync is exactly `http://127.0.0.1:5173`; it is not the callback URI.
+6. From the repository root run:
+
+   ```powershell
+   .\.venv\Scripts\python.exe -m pip install -r requirements.txt
+   .\.venv\Scripts\python.exe -m scripts.setup_gmail
+   ```
+
+   Open the ignored root `.env` in VS Code locally. Enter the new client's ID in
+   `APPLYSYNC_GOOGLE_CLIENT_ID` and its secret in `APPLYSYNC_GOOGLE_CLIENT_SECRET`.
+   The helper appends missing settings only and generates
+   `APPLYSYNC_GMAIL_ENCRYPTION_KEY` without displaying it. Keep its generated value;
+   it is separate from `APPLYSYNC_AUTH_SECRET`. Existing placeholders/invalid
+   settings are deliberately not overwritten; correct those locally.
+
+   Keep `APPLYSYNC_GOOGLE_REDIRECT_URI=http://127.0.0.1:8000/gmail/callback` and
+   `APPLYSYNC_GMAIL_FRONTEND_ORIGIN=http://127.0.0.1:5173`. Do not use `localhost`
+   for this flow, put secrets into frontend variables, or share `.env`, OAuth
+   URLs containing codes/state, cookies, or screenshots of credentials.
+7. Start the backend and frontend in separate PowerShell terminals if not already
+   running. Gmail settings are loaded on each operation, so entering them does not
+   require a server restart in the current implementation.
+
+   ```powershell
+   # Repository root:
+   .\.venv\Scripts\python.exe -m uvicorn main:app --host 127.0.0.1 --port 8000 --no-access-log
+   # Another terminal:
+   cd frontend
+   npm.cmd ci
+   npm.cmd run dev -- --port 5173 --strictPort
+   ```
+
+   Sign in on 127.0.0.1, open Gmail settings, choose Connect Google account, and
+   authorize only the intended test account/scopes. Confirm the connected address,
+   refresh the settings page, then disconnect. Google may require reauthorization
+   while the app remains in Testing. Live provider compatibility, consent and
+   revocation must be verified here; mocked tests are not a live OAuth result.
+
+Keep the encryption key private and backed up securely. Changing/losing it makes
+existing encrypted grants unusable; disconnect and authorize again, rather than
+silently overwriting the key. No automatic key rotation is implemented.
+
+### Connection contract and safeguards
+
+- `GET /gmail`: current user's `{available,status,email,revocation_warning}`.
+  Status is `not_connected`, `connected`, `disconnected`, or `reauthorization_needed`.
+  No token, database state hash, verifier, or provider diagnostic is returned.
+- `POST /gmail/start`: authenticated, exact allowed Origin and
+  `X-ApplySync-CSRF: 1`; returns one Google `authorization_url`. That protocol URL
+  necessarily contains random OAuth state and public client metadata, never a
+  client secret or PKCE verifier. Only the latest pending flow per user is valid.
+- `GET /gmail/callback`: Google browser redirect; requires the same ApplySync
+  session, valid one-use state within ten minutes, and the matching PKCE verifier.
+  Missing authentication returns 401. Other handled failures redirect to the fixed
+  settings URL with a safe result code. No caller-provided return URL is accepted.
+- `POST /gmail/disconnect`: same write protections; affects only the current
+  user. Clears stored authorization and pending state and attempts Google revocation.
+  Provider timeout/failure still commits local disconnection and a warning.
+  Revocation and the local update are serialized in one transaction: local fields
+  are cleared before the provider call, but durable commit follows that bounded
+  call. A process/database failure can leave the result uncertain; refresh status.
+  After a confirmed warning, remove access in
+  [Google account connections](https://myaccount.google.com/connections).
+  The token is erased, so there is no automatic server-side revocation retry.
+
+Disconnect explicitly before choosing a different Google account. Same-account
+reauthorization preserves the old encrypted refresh token only when Google omits
+a new one and a refresh confirms the old grant is usable. Access/ID tokens remain
+in memory. Logout revokes the ApplySync session and pending OAuth state, but does
+not disconnect a previously committed Gmail grant. No connection grants access
+to another ApplySync user's data.
+
+### Reproducible checks
+
+```powershell
+# Root, dedicated test database already migrated:
+.\.venv\Scripts\python.exe -m pytest --run-db -q -p no:cacheprovider --tb=short
+.\.venv\Scripts\python.exe -m pip check
+.\.venv\Scripts\python.exe -m scripts.run_frontend_integration
+# Frontend directory:
+npm.cmd run typecheck
+npm.cmd run build
+npm.cmd test
+npm.cmd run test:e2e
+```
+
+Google endpoints are faked in automated checks; no real mailbox is used. The real
+browser/database runner verifies two-account authentication/application regression
+against `applysync_test` only and cleans its own synthetic records. Its screenshots
+now default to ignored `frontend/test-results/integration-screenshots`, preserving
+historical review images. The Gmail browser screenshots are intentional synthetic
+review evidence in `docs/screenshots/Build4_Task1`.
+
+See [Build 4 Task 1 review](docs/Build4_Task1_Review.md) for source, security decisions,
+exact execution evidence and official documentation. Gmail label/filter verification
+and any message ingestion remain future work. Earlier learning exercises remain pending.
diff --git a/frontend/e2e/integration.spec.ts b/frontend/e2e/integration.spec.ts
index c38d048..5805c65 100644
--- a/frontend/e2e/integration.spec.ts
+++ b/frontend/e2e/integration.spec.ts
@@ -3,7 +3,7 @@ import { mkdirSync } from 'node:fs'

 const api = process.env.APPLYSYNC_E2E_API_ORIGIN!
 const marker = process.env.APPLYSYNC_E2E_RUN_ID!
-const screenshots = '../docs/screenshots/Build3'
+const screenshots = process.env.APPLYSYNC_E2E_SCREENSHOTS ?? 'test-results/integration-screenshots'
 mkdirSync(screenshots, { recursive: true })

 test('real two-account sessions, ownership, creation, reload and logout', async ({ page, browser }) => {
diff --git a/frontend/src/App.tsx b/frontend/src/App.tsx
index fe35429..2786710 100644
--- a/frontend/src/App.tsx
+++ b/frontend/src/App.tsx
@@ -1,6 +1,7 @@
 import { Navigate, Route, Routes } from 'react-router'
 import { QueryClientProvider } from '@tanstack/react-query'
 import { useState } from 'react'
+import { GmailSettings } from './GmailSettings'
 import { Shell } from './components/Shell'
 import { PreviewApplications } from './PreviewApplications'
 import { StoredApplications } from './StoredApplications'
@@ -15,6 +16,7 @@ export function App({ initialRecords }: { initialRecords?: PreviewApplication[]
     <Route path="*" element={<AuthProvider><Shell><Routes>
       <Route path="/login" element={<AuthForm />} />
       <Route path="/register" element={<AuthForm register />} />
+      <Route path="/settings/gmail" element={<ProtectedApplications><GmailSettings /></ProtectedApplications>} />
       <Route path="/applications/:id?" element={<ProtectedApplications><StoredApplications /></ProtectedApplications>} />
       <Route path="*" element={<Navigate to="/applications" replace />} />
     </Routes></Shell></AuthProvider>} />
diff --git a/frontend/src/Auth.tsx b/frontend/src/Auth.tsx
index df6070f..dd55d8d 100644
--- a/frontend/src/Auth.tsx
+++ b/frontend/src/Auth.tsx
@@ -91,6 +91,7 @@ export function ProtectedApplications({ children }: { children: ReactNode }) {
 }

 export function internalDestination(value: string | null) {
+  if (value === '/settings/gmail') return value
   if (!value || !/^\/applications(?:\/(?:new|[0-9a-fA-F-]{36}))?(?:\?[^#]*)?$/.test(value) || value.includes('\\')) return '/applications'
   return value
 }
diff --git a/frontend/src/api.ts b/frontend/src/api.ts
index 21e611b..106eeef 100644
--- a/frontend/src/api.ts
+++ b/frontend/src/api.ts
@@ -58,7 +58,7 @@ export async function request(path: string, body?: unknown, signal?: AbortSignal
     })
   } catch { throw new ApiError('network') }
   if (response.status === 401) {
-    if (path.startsWith('/applications') && !signal?.aborted) window.dispatchEvent(new Event('applysync:expired'))
+    if ((path.startsWith('/applications') || path.startsWith('/gmail')) && !signal?.aborted) window.dispatchEvent(new Event('applysync:expired'))
     throw new ApiError('unauthorized')
   }
   if (response.status === 403) throw new ApiError('forbidden')
diff --git a/frontend/src/components/Shell.tsx b/frontend/src/components/Shell.tsx
index f761815..f2836c0 100644
--- a/frontend/src/components/Shell.tsx
+++ b/frontend/src/components/Shell.tsx
@@ -1,16 +1,17 @@
 import { useState, type ReactNode } from 'react'
 import { Link, useLocation } from 'react-router'
-import { ArrowUpRight, Layers3, Menu, ShieldCheck } from 'lucide-react'
+import { ArrowUpRight, Layers3, Mail, Menu, ShieldCheck } from 'lucide-react'
 import { Modal, PreviewNotice } from './ui'
 import { useAuth } from '../Auth'

 function Sidebar({ onNavigate }: { onNavigate?: () => void }) {
-  const preview = useLocation().pathname.startsWith('/preview/')
+  const path = useLocation().pathname
+  const preview = path.startsWith('/preview/')
   return <div className="sidebar-inner">
     <Link className="brand" to="/applications" onClick={onNavigate}><img src="/mark.svg" alt="" width="32" height="32" /><span>ApplySync<span className="brand-dot">.</span></span></Link>
     <div className="sidebar-body">
       <p className="eyebrow">YOUR WORKSPACE</p>
-      <nav aria-label="Main navigation"><Link className="nav-link" aria-current="page" to={preview ? "/preview/applications" : "/applications"} onClick={onNavigate}><Layers3 size={19} /> Applications <ArrowUpRight size={16} className="ml-auto" /></Link></nav>
+      <nav aria-label="Main navigation"><Link className="nav-link" aria-current={path.includes("applications") ? "page" : undefined} to={preview ? "/preview/applications" : "/applications"} onClick={onNavigate}><Layers3 size={19} /> Applications <ArrowUpRight size={16} className="ml-auto" /></Link>{!preview && <Link className="nav-link" aria-current={path === "/settings/gmail" ? "page" : undefined} to="/settings/gmail" onClick={onNavigate}><Mail size={19} /> Gmail settings</Link>}</nav>
       <div className="sidebar-note"><span className="tiny-tag">{preview ? 'BUILD 2 · PREVIEW' : 'BUILD 2 · LOCAL DEVELOPMENT'}</span><h2>A little more clarity.</h2><p>One place to see your next opportunity taking shape.</p></div>
     </div>
     <div className="sidebar-footer"><ShieldCheck size={20} /><div><strong>Private by design</strong><p>{preview ? "Fictional data. All local." : "Your account. Your applications."}</p></div></div>
@@ -18,15 +19,16 @@ function Sidebar({ onNavigate }: { onNavigate?: () => void }) {
 }
 export function Shell({ children }: { children: ReactNode }) {
   const auth = useAuth()
-  const preview = useLocation().pathname.startsWith('/preview/')
+  const path = useLocation().pathname
+  const preview = path.startsWith('/preview/')
   const [navigationOpen, setNavigationOpen] = useState(false)
   return <div className="app-shell">
-    <a className="skip-link" href="#main-content">Skip to applications</a>
+    <a className="skip-link" href="#main-content">Skip to main content</a>
     <aside className="desktop-sidebar"><Sidebar /></aside>
     <div className="workspace">
       <header className="topbar">
         <button className="icon-button mobile-menu" aria-label="Open navigation" onClick={() => setNavigationOpen(true)}><Menu size={21} /></button>
-        <div className="breadcrumb"><span>Workspace</span><span aria-hidden="true">/</span><strong>Applications</strong></div>
+        <div className="breadcrumb"><span>Workspace</span><span aria-hidden="true">/</span><strong>{path === "/settings/gmail" ? "Gmail settings" : "Applications"}</strong></div>
         <PreviewNotice>{preview ? 'Design preview · Sample data' : 'Local development · Stored data'}</PreviewNotice>
         {auth?.user && !auth.checking && !auth.failure && <div className="signed-in"><span>{auth.user.email}</span><button className="button" onClick={() => void auth.logout()}>Log out</button></div>}
       </header>
diff --git a/frontend/src/styles.css b/frontend/src/styles.css
index 16fe95f..74146b7 100644
--- a/frontend/src/styles.css
+++ b/frontend/src/styles.css
@@ -228,3 +228,10 @@ input::placeholder { color: #667085; }
 .signed-in { display: flex; gap: 12px; align-items: center; min-width: 0; }
 .signed-in span { max-width: 220px; overflow: hidden; text-overflow: ellipsis; font-size: 12px; }
 @media (max-width: 700px) { .topbar { flex-wrap: wrap; height: auto; min-height: 72px; gap: 10px; padding-block: 12px; } .signed-in { margin-left: auto; } .signed-in span { max-width: 160px; } .auth-card { margin: 20px auto; padding: 22px; } }
+
+/* Gmail settings reuse the approved palette, controls and responsive shell. */
+.nav-link + .nav-link { margin-top: 8px; }
+.nav-link:not([aria-current]) { background: transparent; border-color: transparent; color: var(--color-muted); }
+.gmail-card { max-width: 640px; background: white; border: 1px solid var(--color-line); border-radius: 10px; line-height: 1.7; overflow-wrap: anywhere; }
+.gmail-card h2, .gmail-card h3 { font-weight: 650; margin-bottom: 12px; }
+.gmail-actions { display: flex; flex-wrap: wrap; gap: 10px; margin: 18px 0; }
diff --git a/main.py b/main.py
index e558820..736486e 100644
--- a/main.py
+++ b/main.py
@@ -1,5 +1,6 @@
 from contextlib import asynccontextmanager
 from threading import Lock
+import logging

 from fastapi import FastAPI, Request
 from fastapi.middleware.cors import CORSMiddleware
@@ -11,6 +12,16 @@ from config import ConfigurationError
 from auth import router as auth_router, AttemptLimiter
 from auth_config import allowed_origins
 from fastapi.exceptions import RequestValidationError
+from gmail_routes import router as gmail_router
+
+
+class OAuthAccessFilter(logging.Filter):
+    def filter(self, record):
+        # Uvicorn's default access line contains query strings, including codes.
+        return "/gmail/callback" not in record.getMessage()
+
+
+logging.getLogger("uvicorn.access").addFilter(OAuthAccessFilter())


 @asynccontextmanager
@@ -47,8 +58,10 @@ def create_app(database_target: str = "dev") -> FastAPI:
                     or request.headers.get("x-applysync-csrf") != "1"):
                 return JSONResponse(status_code=403, content={"detail": "Request protection failed"})
         response = await call_next(request)
-        if request.url.path.startswith(("/auth", "/applications")):
+        if request.url.path.startswith(("/auth", "/applications", "/gmail")):
             response.headers["Cache-Control"] = "no-store"
+        if request.url.path == "/gmail/callback":
+            response.headers["Referrer-Policy"] = "no-referrer"
         return response

     @application.exception_handler(RequestValidationError)
@@ -73,6 +86,7 @@ def create_app(database_target: str = "dev") -> FastAPI:
     application.add_api_route("/health", health, methods=["GET"])
     application.include_router(router)
     application.include_router(auth_router)
+    application.include_router(gmail_router)
     return application


diff --git a/models.py b/models.py
index ad3c82d..a7a7c1c 100644
--- a/models.py
+++ b/models.py
@@ -3,7 +3,7 @@
 from datetime import date, datetime
 from uuid import UUID, uuid4

-from sqlalchemy import CheckConstraint, Date, DateTime, ForeignKey, Index, String, Uuid, func
+from sqlalchemy import Boolean, CheckConstraint, Date, DateTime, ForeignKey, Index, String, Text, Uuid, func
 from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


@@ -43,3 +43,27 @@ class JobApplication(Base):
     applied_on: Mapped[date] = mapped_column(Date, nullable=False)
     created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False,
                                                server_default=func.now())
+
+
+class GmailConnection(Base):
+    __tablename__ = "gmail_connections"
+    owner_id: Mapped[UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
+    google_subject: Mapped[str | None] = mapped_column(String(255))
+    email: Mapped[str | None] = mapped_column(String(254))
+    encrypted_refresh_token: Mapped[str | None] = mapped_column(Text)
+    granted_scopes: Mapped[str | None] = mapped_column(Text)
+    status: Mapped[str] = mapped_column(String(32), nullable=False)
+    revocation_warning: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
+    connected_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
+    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
+    __table_args__ = (CheckConstraint("status IN ('connected','disconnected','reauthorization_needed')", name="ck_gmail_status"),)
+
+
+class GmailOAuthState(Base):
+    __tablename__ = "gmail_oauth_states"
+    state_hash: Mapped[str] = mapped_column(String(64), primary_key=True)
+    owner_id: Mapped[UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False, unique=True)
+    session_id: Mapped[UUID] = mapped_column(ForeignKey("auth_sessions.id", ondelete="CASCADE"), nullable=False)
+    encrypted_flow: Mapped[str | None] = mapped_column(Text)
+    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
+    used_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
diff --git a/requirements.txt b/requirements.txt
index f1028d9..b13bf25 100644
--- a/requirements.txt
+++ b/requirements.txt
@@ -39,3 +39,5 @@ pycparser==3.0
 PyJWT==2.15.0
 email-validator==2.3.0
 dnspython==2.8.0
+
+cryptography==50.0.2
diff --git a/scripts/run_frontend_integration.py b/scripts/run_frontend_integration.py
index e685b54..75f8b9d 100644
--- a/scripts/run_frontend_integration.py
+++ b/scripts/run_frontend_integration.py
@@ -26,7 +26,7 @@ def verify_target(engine):
     with engine.connect() as connection:
         if (connection.scalar(text("SELECT current_database()")) != "applysync_test"
                 or connection.scalar(text("SELECT current_user")) != "applysync_test"
-                or connection.scalar(text("SELECT version_num FROM alembic_version")) != "0002"):
+                or connection.scalar(text("SELECT version_num FROM alembic_version")) != "0003"):
             raise RuntimeError("Refusing an unverified integration database target.")


diff --git a/tests/conftest.py b/tests/conftest.py
index 0551751..1cb4728 100644
--- a/tests/conftest.py
+++ b/tests/conftest.py
@@ -20,7 +20,7 @@ def test_engine(request):
         with engine.connect() as connection:
             assert connection.scalar(text("SELECT current_database()")) == "applysync_test"
             assert connection.scalar(text("SELECT current_user")) == "applysync_test"
-            assert connection.scalar(text("SELECT version_num FROM alembic_version")) == "0002"
+            assert connection.scalar(text("SELECT version_num FROM alembic_version")) == "0003"
         yield engine
     except (ConfigurationError, SQLAlchemyError):
         pytest.fail("Dedicated test database is not configured, reachable, or migrated.", pytrace=False)
diff --git a/tests/test_ownership_migration.py b/tests/test_ownership_migration.py
index 9d7892c..40e759a 100644
--- a/tests/test_ownership_migration.py
+++ b/tests/test_ownership_migration.py
@@ -25,8 +25,8 @@ def test_upgrade_preserves_legacy_and_repeats(test_engine, legacy):
             id_ = uuid4()
             if legacy:
                 connection.execute(text("INSERT INTO job_applications (id,company,role,applied_on) VALUES (:id,'Synthetic legacy','Engineer',:day)"), {"id": id_, "day": date(2026, 9, 1)})
-            command.upgrade(config, "head")
-            command.upgrade(config, "head")
+            command.upgrade(config, "0002")
+            command.upgrade(config, "0002")
             assert connection.scalar(text("select version_num from alembic_version")) == "0002"
             assert set(inspect(connection).get_table_names(schema=schema)) == {"alembic_version", "users", "auth_sessions", "job_applications"}
             assert connection.scalar(text("select count(*) from job_applications")) == int(legacy)
```

### Complete new file: `frontend/e2e/gmail.spec.ts`

```typescript
import { expect, test } from '@playwright/test'

test('Gmail status, protected start, callback result, disconnect and mobile settings (mocked Google/API)', async ({ page }) => {
  const headers = { 'access-control-allow-origin': 'http://127.0.0.1:4173', 'access-control-allow-credentials': 'true' }
  let connection = { available: true, status: 'not_connected', email: null as string | null, revocation_warning: false }
  const errors: string[] = []
  page.on('pageerror', error => errors.push(error.message))
  await page.route('http://127.0.0.1:8000/**', async route => {
    const path = new URL(route.request().url()).pathname
    if (path === '/auth/me') return route.fulfill({ headers, json: { id: 'synthetic-user', email: 'synthetic@example.com' } })
    if (path === '/gmail/start') {
      expect(route.request().headers()['x-applysync-csrf']).toBe('1')
      return route.fulfill({ headers, json: { authorization_url: 'https://accounts.google.com/o/oauth2/v2/auth?state=synthetic' } })
    }
    if (path === '/gmail/disconnect') {
      expect(route.request().headers()['x-applysync-csrf']).toBe('1')
      connection = { ...connection, status: 'disconnected', email: null, revocation_warning: true }
    }
    return route.fulfill({ headers, json: connection })
  })
  await page.route('https://accounts.google.com/**', route => route.fulfill({ contentType: 'text/html', body: '<p>Mock Google authorization; no provider access.</p>' }))
  await page.goto('/settings/gmail')
  await expect(page.getByText('Not connected', { exact: true })).toBeVisible()
  await page.getByRole('button', { name: 'Connect Google account', exact: true }).click()
  await expect(page).toHaveURL(/https:\/\/accounts.google.com\/o\/oauth2\/v2\/auth/)
  connection = { ...connection, status: 'connected', email: 'synthetic-google@example.com' }
  await page.goto('/settings/gmail?result=connected')
  await expect(page.getByText('synthetic-google@example.com', { exact: true })).toBeVisible()
  await page.screenshot({ path: '../docs/screenshots/Build4_Task1/gmail-connected.png', fullPage: true })
  await page.getByRole('button', { name: 'Disconnect', exact: true }).click()
  await expect(page.getByText('Disconnected', { exact: true })).toBeVisible()
  await expect(page.getByRole('alert')).toContainText('revocation could not be confirmed')
  await page.setViewportSize({ width: 390, height: 844 })
  await page.emulateMedia({ reducedMotion: 'reduce' })
  await page.getByRole('button', { name: 'Open navigation' }).click()
  await page.keyboard.press('Escape')
  await expect(page.getByRole('dialog')).toHaveCount(0)
  expect(await page.evaluate(() => document.documentElement.scrollWidth <= window.innerWidth)).toBe(true)
  await page.screenshot({ path: '../docs/screenshots/Build4_Task1/gmail-mobile.png', fullPage: true })
  await page.goto('/settings/gmail?result=different_account')
  await expect(page.getByText(/existing connection was preserved/)).toBeVisible()
  await page.goto('/settings/gmail?result=reauthorization_needed')
  await expect(page.getByText(/Offline authorization is missing/)).toBeVisible()
  await page.goto('/settings/gmail?result=failed')
  await expect(page.getByText(/Connection could not be completed/)).toBeVisible()
  expect(errors).toEqual([])
})
```

### Complete new file: `frontend/src/GmailSettings.test.tsx`

```tsx
import { act, render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { MemoryRouter } from 'react-router'
import { afterEach, expect, it, vi } from 'vitest'
import { App } from './App'
import { googleDestination } from './GmailSettings'

const json = (body: unknown, status = 200) => new Response(JSON.stringify(body), { status })
const identity = { id: 'synthetic-user', email: 'synthetic@example.com' }
const disconnected = { available: true, status: 'not_connected', email: null, revocation_warning: false }
const mount = (path = '/settings/gmail') => { render(<MemoryRouter initialEntries={[path]}><App /></MemoryRouter>); return userEvent.setup() }
afterEach(() => vi.unstubAllGlobals())

it('shows unavailable configuration without offering a broken connection', async () => {
  vi.stubGlobal('fetch', vi.fn(url => Promise.resolve(json(String(url).endsWith('/auth/me') ? identity : { ...disconnected, available: false }))))
  mount()
  expect(await screen.findByText('Not connected')).toBeInTheDocument()
  expect(screen.getByRole('button', { name: 'Connect Google account' })).toBeDisabled()
  expect(screen.getByText(/this task reads no messages/)).toBeInTheDocument()
})

it('disables duplicate starts, uses CSRF and displays safe failure', async () => {
  let finish!: (value: Response) => void
  const fetchMock = vi.fn((url, options) => String(url).endsWith('/auth/me') ? Promise.resolve(json(identity))
    : options.method === 'POST' ? new Promise<Response>(r => { finish = r }) : Promise.resolve(json(disconnected)))
  vi.stubGlobal('fetch', fetchMock)
  const user = mount()
  await user.click(await screen.findByRole('button', { name: 'Connect Google account' }))
  expect(screen.getByRole('button', { name: 'Starting connection…' })).toBeDisabled()
  const options = fetchMock.mock.calls.find(([url]) => String(url).endsWith('/gmail/start'))![1]
  expect(options.credentials).toBe('include'); expect(options.headers['X-ApplySync-CSRF']).toBe('1')
  await act(async () => finish(json({ detail: 'do not display raw provider error' }, 500)))
  expect(await screen.findByRole('alert')).toHaveTextContent('could not be confirmed')
  expect(screen.queryByText('do not display raw provider error')).not.toBeInTheDocument()
})

it('disconnects and refreshes safe status including revocation warning', async () => {
  let connection = { ...disconnected, status: 'connected', email: 'synthetic-google@example.com' as string | null }
  vi.stubGlobal('fetch', vi.fn((url, options) => {
    if (String(url).endsWith('/auth/me')) return Promise.resolve(json(identity))
    if (options.method === 'POST') connection = { ...disconnected, status: 'disconnected', revocation_warning: true }
    return Promise.resolve(json(connection))
  }))
  const user = mount('/settings/gmail?result=connected')
  await user.click(await screen.findByRole('button', { name: 'Disconnect' }))
  expect(await screen.findByText('Disconnected')).toBeInTheDocument()
  expect(screen.queryByText('synthetic-google@example.com')).not.toBeInTheDocument()
  expect(screen.getByRole('alert')).toHaveTextContent('revocation could not be confirmed')
})

it('allows only the fixed Google authorization destination', () => {
  expect(googleDestination('https://accounts.google.com/o/oauth2/v2/auth?state=synthetic')).toContain('accounts.google.com')
  for (const value of ['https://evil.example/', 'javascript:alert(1)', 'https://accounts.google.com/other', 'https://user@accounts.google.com/o/oauth2/v2/auth']) expect(() => googleDestination(value)).toThrow()
})

it('aborts a delayed start on logout so it cannot navigate a new account', async () => {
  let finish!: (value: Response) => void
  let signal!: AbortSignal
  vi.stubGlobal('fetch', vi.fn((url, options) => {
    if (String(url).endsWith('/auth/me')) return Promise.resolve(json(identity))
    if (String(url).endsWith('/auth/logout')) return Promise.resolve(new Response(null, { status: 204 }))
    if (String(url).endsWith('/gmail/start')) { signal = options.signal; return new Promise<Response>(r => { finish = r }) }
    return Promise.resolve(json(disconnected))
  }))
  const user = mount()
  await user.click(await screen.findByRole('button', { name: 'Connect Google account' }))
  await user.click(screen.getByRole('button', { name: 'Log out' }))
  expect(signal.aborted).toBe(true)
  await act(async () => finish(json({ authorization_url: 'https://accounts.google.com/o/oauth2/v2/auth?state=synthetic' })))
  expect(await screen.findByRole('heading', { name: 'Welcome back' })).toBeInTheDocument()
  expect(screen.queryByRole('heading', { name: 'Gmail connection' })).not.toBeInTheDocument()
})
```

### Complete new file: `frontend/src/GmailSettings.tsx`

```tsx
import { useEffect, useRef, useState } from 'react'
import { useSearchParams } from 'react-router'
import { useQuery, useQueryClient } from '@tanstack/react-query'
import { request } from './api'
import { Button } from './components/ui'

type Connection = { available: boolean; status: 'not_connected' | 'connected' | 'disconnected' | 'reauthorization_needed'; email: string | null; revocation_warning: boolean }
const labels = { not_connected: 'Not connected', connected: 'Connected', disconnected: 'Disconnected', reauthorization_needed: 'Reauthorization needed' }
const outcomes: Record<string, string> = {
  connected: 'Google authorization completed.',
  failed: 'Connection could not be completed. Try connecting again.',
  different_account: 'Your existing connection was preserved. Disconnect it before connecting a different Google account.',
  reauthorization_needed: 'Offline authorization is missing or expired. Connect again to grant consent.',
}
export function googleDestination(value: unknown) {
  if (typeof value !== 'string') throw new Error('Invalid destination')
  const url = new URL(value)
  if (url.origin !== 'https://accounts.google.com' || url.pathname !== '/o/oauth2/v2/auth' || url.username || url.password || url.hash) throw new Error('Invalid destination')
  return url.href
}
export function GmailSettings() {
  const [params, setParams] = useSearchParams()
  const client = useQueryClient()
  const active = useRef<AbortController | null>(null)
  const [pending, setPending] = useState('')
  const [failure, setFailure] = useState('')
  useEffect(() => () => { active.current?.abort() }, [])
  const query = useQuery({ queryKey: ['gmail'], queryFn: async ({ signal }) => {
    const value = await request('/gmail', undefined, signal) as Connection
    if (!value || !Object.hasOwn(labels, value.status) || typeof value.available !== 'boolean' || typeof value.revocation_warning !== 'boolean' || (value.email !== null && typeof value.email !== 'string')) throw new Error('Invalid status')
    return value
  } })
  async function act(action: 'start' | 'disconnect') {
    if (active.current) return
    const controller = new AbortController(); active.current = controller
    setParams({}, { replace: true })
    setPending(action); setFailure('')
    try {
      const value = await request(`/gmail/${action}`, {}, controller.signal)
      if (controller.signal.aborted) return
      if (action === 'start') window.location.assign(googleDestination((value as { authorization_url?: unknown })?.authorization_url))
      else await client.invalidateQueries({ queryKey: ['gmail'] })
    } catch {
      if (!controller.signal.aborted) setFailure('The connection change could not be confirmed. Refresh status before retrying.')
    } finally {
      if (!controller.signal.aborted) { active.current = null; setPending('') }
    }
  }
  const data = query.data
  return <section className="applications-workspace">
    <div className="page-heading"><div><p className="eyebrow">YOUR PRIVATE WORKSPACE</p><h1>Gmail connection</h1>
    <p className="page-description">Connect your Google account separately from your ApplySync sign-in.</p></div></div>
    <div className="auth-card gmail-card">
      <h2>Read-only access, deliberate setup</h2>
      <p>Google grants read-only access across your mailbox. ApplySync will limit future reading through its approved Gmail connector and verified label setup. Label and filter verification comes next; this task reads no messages.</p>
      <p>Only your Google account identity and encrypted offline authorization are stored. You can disconnect at any time.</p>
      {outcomes[params.get('result') ?? ''] && <p role="status">{outcomes[params.get('result') ?? '']}</p>}
      {query.isPending && <p role="status">Loading connection…</p>}
      {query.isError && <p role="alert">Connection status is unavailable. Retry status.</p>}
      {data && <>
        <h3>{labels[data.status]}</h3>
        {data.email && <p>{data.email}</p>}
        {!data.available && <p role="status">Gmail is unavailable until local Google Cloud configuration is complete. Application tracking still works.</p>}
        {data.revocation_warning && <p role="alert">Disconnected locally, but Google revocation could not be confirmed. Remove ApplySync access in <a href="https://myaccount.google.com/connections" target="_blank" rel="noreferrer">Google account connections</a>.</p>}
        <div className="gmail-actions">
          <Button variant="primary" disabled={!!pending || !data.available || query.isError} onClick={() => void act('start')}>{pending === 'start' ? 'Starting connection…' : data.status === 'connected' ? 'Reconnect Google account' : 'Connect Google account'}</Button>
          {['connected', 'reauthorization_needed'].includes(data.status) && <Button disabled={!!pending} onClick={() => void act('disconnect')}>{pending === 'disconnect' ? 'Disconnecting…' : 'Disconnect'}</Button>}
        </div>
      </>}
      {failure && <p role="alert">{failure}</p>}
      <Button disabled={!!pending || query.isFetching} onClick={() => void query.refetch()}>Refresh status</Button>
    </div>
  </section>
}
```

### Complete new file: `gmail_connector/__init__.py`

```python
"""Only this package handles Google endpoints, identity and token cryptography."""
from .client import GmailConnector, ConnectorError, GmailUnavailable, get_connector

__all__ = ["GmailConnector", "ConnectorError", "GmailUnavailable", "get_connector"]
```

### Complete new file: `gmail_connector/client.py`

```python
"""Narrow Google OAuth operations. No mailbox/message operations in Task 1."""
from base64 import urlsafe_b64encode
from dataclasses import dataclass
import hashlib
import json
import os
import re
import secrets
from urllib.parse import urlencode

from cryptography.fernet import Fernet, InvalidToken
from dotenv import dotenv_values
import httpx
import jwt

from config import ROOT

AUTHORIZATION = "https://accounts.google.com/o/oauth2/v2/auth"
TOKEN = "https://oauth2.googleapis.com/token"
REVOKE = "https://oauth2.googleapis.com/revoke"
CERTS = "https://www.googleapis.com/oauth2/v3/certs"
SCOPES = frozenset({"openid", "email", "https://www.googleapis.com/auth/gmail.readonly"})
REDIRECT = "http://127.0.0.1:8000/gmail/callback"
FRONTEND = "http://127.0.0.1:5173"


class ConnectorError(Exception):
    def __init__(self):
        super().__init__("Gmail authorization could not be completed.")


class GmailUnavailable(ConnectorError):
    pass


@dataclass(frozen=True, repr=False)
class Grant:
    subject: str
    email: str
    encrypted_refresh_token: str | None
    scopes: str


class GmailConnector:
    def __init__(self, client_id, client_secret, encryption_key, *, transport=None):
        self._client_id = client_id
        self._client_secret = client_secret
        try:
            self._cipher = Fernet(encryption_key.encode())
        except (ValueError, TypeError):
            raise GmailUnavailable() from None
        self._transport = transport

    def _request(self, method, url, **kwargs):
        # No debug logging, request URLs containing tokens, redirects or ambient proxies.
        try:
            with httpx.Client(timeout=10, trust_env=False, follow_redirects=False,
                              transport=self._transport) as client:
                return client.request(method, url, **kwargs)
        except httpx.HTTPError:
            raise ConnectorError() from None

    def _seal(self, value):
        return self._cipher.encrypt(value.encode()).decode()

    def _open(self, value):
        try:
            return self._cipher.decrypt(value.encode()).decode()
        except (InvalidToken, ValueError, UnicodeError, AttributeError):
            raise ConnectorError() from None

    def begin(self, state, *, consent):
        verifier, nonce = secrets.token_urlsafe(64), secrets.token_urlsafe(32)
        challenge = urlsafe_b64encode(hashlib.sha256(verifier.encode()).digest()).rstrip(b"=").decode()
        parameters = {"client_id": self._client_id, "redirect_uri": REDIRECT,
            "response_type": "code", "scope": " ".join(sorted(SCOPES)),
            "access_type": "offline", "state": state, "nonce": nonce,
            "code_challenge": challenge, "code_challenge_method": "S256",
            "include_granted_scopes": "false", "prompt": "consent" if consent else "select_account"}
        return AUTHORIZATION + "?" + urlencode(parameters), self._seal(json.dumps({"verifier": verifier, "nonce": nonce}))

    def exchange(self, code, encrypted_flow):
        try:
            flow = json.loads(self._open(encrypted_flow))
            response = self._request("POST", TOKEN, data={"grant_type": "authorization_code",
                "client_id": self._client_id, "client_secret": self._client_secret,
                "redirect_uri": REDIRECT, "code": code, "code_verifier": flow["verifier"]})
            if response.status_code != 200:
                raise ConnectorError()
            tokens = response.json()
            granted = set(tokens["scope"].split())
            if "https://www.googleapis.com/auth/userinfo.email" in granted:
                granted.remove("https://www.googleapis.com/auth/userinfo.email")
                granted.add("email")
            if granted != SCOPES or tokens.get("token_type", "").lower() != "bearer":
                raise ConnectorError()
            # Only JWKS from the fixed Google endpoint; never trust token jku/x5u.
            header = jwt.get_unverified_header(tokens["id_token"])
            response = self._request("GET", CERTS)
            if response.status_code != 200 or header.get("alg") != "RS256":
                raise ConnectorError()
            key = next(k for k in response.json()["keys"] if k.get("kid") == header.get("kid") and k.get("kty") == "RSA")
            claims = jwt.decode(tokens["id_token"], jwt.PyJWK.from_dict(key).key,
                algorithms=["RS256"], audience=self._client_id,
                issuer=["https://accounts.google.com", "accounts.google.com"],
                options={"require": ["iss", "aud", "exp", "iat", "sub", "nonce", "email", "email_verified"]})
            if (claims["nonce"] != flow["nonce"] or claims["email_verified"] is not True
                    or not isinstance(claims["sub"], str) or not 1 <= len(claims["sub"]) <= 255
                    or not isinstance(claims["email"], str) or len(claims["email"]) > 254
                    or "@" not in claims["email"]
                    or claims.get("azp", self._client_id) != self._client_id):
                raise ConnectorError()
            refresh = tokens.get("refresh_token")
            if refresh is not None and (not isinstance(refresh, str) or not refresh or len(refresh) > 8192):
                raise ConnectorError()
            return Grant(claims["sub"], claims["email"], self._seal(refresh) if refresh else None,
                         " ".join(sorted(granted)))
        except (KeyError, ValueError, TypeError, AttributeError, StopIteration, jwt.PyJWTError):
            raise ConnectorError() from None

    def validate_refresh(self, encrypted_token):
        """Prove an old refresh grant is still usable before preserving it; no mail read."""
        response = self._request("POST", TOKEN, data={"grant_type": "refresh_token",
            "client_id": self._client_id, "client_secret": self._client_secret,
            "refresh_token": self._open(encrypted_token)})
        try:
            payload = response.json()
            if response.status_code == 400 and payload.get("error") == "invalid_grant":
                return False
            if response.status_code != 200 or not isinstance(payload.get("access_token"), str) or not payload["access_token"]:
                raise ConnectorError()
            return True
        except (ValueError, AttributeError):
            raise ConnectorError() from None

    def revoke(self, encrypted_token):
        try:
            response = self._request("POST", REVOKE, data={"token": self._open(encrypted_token)})
            return response.status_code == 200
        except ConnectorError:
            return False


def get_connector():
    values = {**dotenv_values(ROOT / ".env", interpolate=False), **os.environ}
    keys = ["APPLYSYNC_GOOGLE_CLIENT_ID", "APPLYSYNC_GOOGLE_CLIENT_SECRET", "APPLYSYNC_GMAIL_ENCRYPTION_KEY"]
    if any(not values.get(key) or values[key].startswith("replace-") for key in keys):
        raise GmailUnavailable()
    if (not re.fullmatch(r"[A-Za-z0-9._-]+\.apps\.googleusercontent\.com", values[keys[0]])
            or values.get("APPLYSYNC_GOOGLE_REDIRECT_URI") != REDIRECT
            or values.get("APPLYSYNC_GMAIL_FRONTEND_ORIGIN") != FRONTEND
            or values[keys[2]] == values.get("APPLYSYNC_AUTH_SECRET")):
        raise GmailUnavailable()
    return GmailConnector(*(values[key] for key in keys))


def generate_key():
    """Called only by the local setup utility; never display the return value."""
    return Fernet.generate_key().decode()
```

### Complete new file: `gmail_routes.py`

```python
"""Authenticated connection orchestration; provider/crypto code stays in connector."""
from datetime import datetime, timedelta, timezone
import hashlib
import re
import secrets
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from sqlalchemy import delete, select
from sqlalchemy.engine import Engine

from auth import CurrentUser
from database import get_engine, session_scope
from gmail_connector import ConnectorError, GmailUnavailable, get_connector
from models import AuthSession, GmailConnection, GmailOAuthState, User

router = APIRouter(prefix="/gmail", tags=["gmail connection"])
DatabaseEngine = Annotated[Engine, Depends(get_engine)]
FRONTEND_DESTINATION = "http://127.0.0.1:5173/settings/gmail"


class ConnectionStatus(BaseModel):
    available: bool
    status: str
    email: str | None = None
    revocation_warning: bool = False


class StartResult(BaseModel):
    authorization_url: str


def now():
    return datetime.now(timezone.utc)


def lock_owner(session, user, request):
    session.scalar(select(User.id).where(User.id == user.id).with_for_update())
    if not session.scalar(select(AuthSession.id).where(AuthSession.id == request.state.session_id,
            AuthSession.user_id == user.id, AuthSession.expires_at > now()).with_for_update()):
        raise HTTPException(401, "Authentication required")


@router.get("", response_model=ConnectionStatus)
def status(user: CurrentUser, engine: DatabaseEngine):
    try:
        get_connector()
        available = True
    except GmailUnavailable:
        available = False
    with session_scope(engine) as session:
        row = session.get(GmailConnection, user.id)
        return ConnectionStatus(available=available, status=row.status if row else "not_connected",
            email=row.email if row else None, revocation_warning=row.revocation_warning if row else False)


@router.post("/start", response_model=StartResult)
def start(user: CurrentUser, engine: DatabaseEngine, request: Request):
    try:
        connector = get_connector()
    except GmailUnavailable:
        raise HTTPException(503, "Gmail connection is unavailable. Check local setup.") from None
    state = secrets.token_urlsafe(32)
    with session_scope(engine) as session:
        lock_owner(session, user, request)
        connection = session.get(GmailConnection, user.id)
        consent = connection is None or connection.status != "connected"
        url, encrypted_flow = connector.begin(state, consent=consent)
        session.execute(delete(GmailOAuthState).where(GmailOAuthState.owner_id == user.id))
        session.add(GmailOAuthState(state_hash=hashlib.sha256(state.encode()).hexdigest(),
            owner_id=user.id, session_id=request.state.session_id, encrypted_flow=encrypted_flow,
            expires_at=now() + timedelta(minutes=10)))
    return StartResult(authorization_url=url)


def result_redirect(result):
    return RedirectResponse(FRONTEND_DESTINATION + "?result=" + result, status_code=303,
                            headers={"Cache-Control": "no-store", "Referrer-Policy": "no-referrer"})


@router.get("/callback")
def callback(user: CurrentUser, engine: DatabaseEngine, request: Request):
    # Read manually so validation never echoes provider codes or query contents.
    params = request.query_params
    state = params.get("state", "")
    if len(params.getlist("state")) != 1 or not re.fullmatch(r"[A-Za-z0-9_-]{43}", state):
        return result_redirect("failed")
    digest = hashlib.sha256(state.encode()).hexdigest()
    with session_scope(engine) as session:
        lock_owner(session, user, request)
        pending = session.get(GmailOAuthState, digest)
        if (pending is None or pending.owner_id != user.id or pending.session_id != request.state.session_id
                or pending.used_at is not None or pending.expires_at <= now()):
            return result_redirect("failed")
        flow = pending.encrypted_flow
        pending.used_at = now()
        pending.encrypted_flow = None
    # Consumption commits before code exchange, even on denial/provider failure.
    if params.get("error") or len(params.getlist("code")) != 1 or not 1 <= len(params.get("code", "")) <= 4096:
        return result_redirect("failed")
    try:
        connector = get_connector()
        with session_scope(engine) as session:
            lock_owner(session, user, request)
            # Disconnect/new start/logout invalidates pending callbacks, including races.
            pending = session.get(GmailOAuthState, digest)
            if pending is None or pending.expires_at <= now():
                return result_redirect("failed")
            grant = connector.exchange(params["code"], flow)
            row = session.get(GmailConnection, user.id)
            if row and row.status != "disconnected" and row.google_subject != grant.subject:
                return result_redirect("different_account")
            refresh = grant.encrypted_refresh_token
            if not refresh and row and row.google_subject == grant.subject and row.status == "connected" and row.encrypted_refresh_token:
                if connector.validate_refresh(row.encrypted_refresh_token):
                    refresh = row.encrypted_refresh_token
                else:
                    row.status = "reauthorization_needed"
                    row.updated_at = now()
            if not refresh:
                return result_redirect("reauthorization_needed")
            if row is None:
                row = GmailConnection(owner_id=user.id)
                session.add(row)
            row.google_subject, row.email = grant.subject, grant.email
            row.encrypted_refresh_token, row.granted_scopes = refresh, grant.scopes
            row.status, row.revocation_warning = "connected", False
            row.connected_at, row.updated_at = now(), now()
        return result_redirect("connected")
    except ConnectorError:
        return result_redirect("failed")


@router.post("/disconnect", response_model=ConnectionStatus)
def disconnect(user: CurrentUser, engine: DatabaseEngine, request: Request):
    with session_scope(engine) as session:
        lock_owner(session, user, request)
        session.execute(delete(GmailOAuthState).where(GmailOAuthState.owner_id == user.id))
        row = session.get(GmailConnection, user.id)
        if row is None:
            row = GmailConnection(owner_id=user.id, status="disconnected", updated_at=now(), revocation_warning=False)
            session.add(row)
        token = row.encrypted_refresh_token
        row.encrypted_refresh_token = None
        row.google_subject = row.email = row.granted_scopes = None
        row.status, row.updated_at = "disconnected", now()
        if token:
            try:
                revoked = get_connector().revoke(token)
            except ConnectorError:
                revoked = False
            row.revocation_warning = not revoked
        # Serialize provider revocation and new grants under the same owner lock.
        # Provider timeout/failure is a warning, not a rollback of local disconnection.
        response = ConnectionStatus(available=True, status="disconnected", revocation_warning=row.revocation_warning)
    return response
```

### Complete new file: `migrations/versions/0003_gmail_connection.py`

```python
"""Gmail connection and session-bound OAuth state; no existing row updates."""
from alembic import op
import sqlalchemy as sa

revision = "0003"
down_revision = "0002"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table("gmail_connections",
        sa.Column("owner_id", sa.Uuid(), sa.ForeignKey("users.id", ondelete="CASCADE"), primary_key=True),
        sa.Column("google_subject", sa.String(255)), sa.Column("email", sa.String(254)),
        sa.Column("encrypted_refresh_token", sa.Text()), sa.Column("granted_scopes", sa.Text()),
        sa.Column("status", sa.String(32), nullable=False),
        sa.Column("revocation_warning", sa.Boolean(), nullable=False),
        sa.Column("connected_at", sa.DateTime(timezone=True)),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.CheckConstraint("status IN ('connected','disconnected','reauthorization_needed')", name="ck_gmail_status"))
    op.create_table("gmail_oauth_states",
        sa.Column("state_hash", sa.String(64), primary_key=True),
        sa.Column("owner_id", sa.Uuid(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False, unique=True),
        sa.Column("session_id", sa.Uuid(), sa.ForeignKey("auth_sessions.id", ondelete="CASCADE"), nullable=False),
        sa.Column("encrypted_flow", sa.Text()),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("used_at", sa.DateTime(timezone=True)))


def downgrade():
    raise RuntimeError("Gmail downgrade requires an explicit authorization-data preservation plan.")
```

### Complete new file: `scripts/setup_gmail.py`

```python
"""Append missing Gmail placeholders/key locally; never display or replace values."""
from config import ROOT
from gmail_connector.client import generate_key


def main():
    path = ROOT / '.env'
    names = set()
    if path.exists():
        with path.open(encoding='utf-8') as stream:
            for line in stream:
                names.add(line.partition('=')[0].strip())
    defaults = {
        'APPLYSYNC_GOOGLE_CLIENT_ID': 'replace-with-web-client-id.apps.googleusercontent.com',
        'APPLYSYNC_GOOGLE_CLIENT_SECRET': 'replace-with-web-client-secret',
        'APPLYSYNC_GOOGLE_REDIRECT_URI': 'http://127.0.0.1:8000/gmail/callback',
        'APPLYSYNC_GMAIL_FRONTEND_ORIGIN': 'http://127.0.0.1:5173',
    }
    additions = [name+'='+value for name, value in defaults.items() if name not in names]
    if 'APPLYSYNC_GMAIL_ENCRYPTION_KEY' not in names:
        additions.append('APPLYSYNC_GMAIL_ENCRYPTION_KEY='+generate_key())
    if additions:
        with path.open('a', encoding='utf-8') as stream:
            stream.write('\n'+'\n'.join(additions)+'\n')
    print('Missing Gmail settings added locally. Existing values preserved; no secrets displayed.')
    print('Enter the web OAuth client ID and secret in .env locally. Never share the file or key.')


if __name__ == '__main__':
    main()
```

### Complete new file: `tests/test_gmail.py`

```python
"""Synthetic accounts on the checked test database; Google is always faked."""
from concurrent.futures import ThreadPoolExecutor
from datetime import timedelta
import hashlib
from urllib.parse import parse_qs, urlparse
from uuid import UUID
from threading import Event

import pytest
from sqlalchemy import select

from database import session_scope
from gmail_connector import ConnectorError
from gmail_connector.client import Grant
from gmail_routes import now
from models import GmailConnection, GmailOAuthState
from test_auth import identities, HEADERS


class FakeConnector:
    def __init__(self):
        self.grant = Grant('synthetic-subject', 'synthetic@example.com', 'synthetic-ciphertext', 'openid email gmail.readonly')
        self.exchanges = 0
        self.revocations = 0
        self.revoked = True
        self.valid = True
        self.fail = False

    def begin(self, state, *, consent):
        return 'https://accounts.google.com/o/oauth2/v2/auth?state=' + state, 'synthetic-encrypted-flow'

    def exchange(self, code, flow):
        self.exchanges += 1
        assert flow == 'synthetic-encrypted-flow'
        if self.fail:
            raise ConnectorError()
        return self.grant

    def validate_refresh(self, token):
        assert token == 'synthetic-ciphertext'
        return self.valid

    def revoke(self, token):
        assert token == 'synthetic-ciphertext'
        self.revocations += 1
        return self.revoked


@pytest.fixture
def google(monkeypatch):
    fake = FakeConnector()
    monkeypatch.setattr('gmail_routes.get_connector', lambda: fake)
    return fake


def begin(client):
    response = client.post('/gmail/start')
    assert response.status_code == 200
    assert set(response.json()) == {'authorization_url'}
    return parse_qs(urlparse(response.json()['authorization_url']).query)['state'][0]


def callback(client, state, **parameters):
    return client.get('/gmail/callback', params={'state': state, 'code': 'synthetic-code', **parameters}, follow_redirects=False)


def test_success_reauth_preserve_and_account_replacement(identities, google):
    _, account, engine = identities
    client, _ = account()
    owner = UUID(client.get('/auth/me').json()['id'])
    state = begin(client)
    with session_scope(engine) as session:
        pending = session.get(GmailOAuthState, hashlib.sha256(state.encode()).hexdigest())
        assert pending.owner_id == owner and pending.session_id and pending.expires_at > now()
        assert pending.encrypted_flow != state
    response = callback(client, state)
    assert response.status_code == 303 and response.headers['location'].endswith('result=connected')
    assert response.headers['referrer-policy'] == 'no-referrer'
    assert callback(client, state).headers['location'].endswith('result=failed')
    assert google.exchanges == 1
    status = client.get('/gmail').json()
    assert status == {'available': True, 'status': 'connected', 'email': 'synthetic@example.com', 'revocation_warning': False}
    assert 'synthetic-ciphertext' not in str(status)
    google.grant = Grant('synthetic-subject', 'renamed@example.com', None, 'openid email gmail.readonly')
    assert callback(client, begin(client)).headers['location'].endswith('result=connected')
    with session_scope(engine) as session:
        assert session.get(GmailConnection, owner).encrypted_refresh_token == 'synthetic-ciphertext'
    google.grant = Grant('different-subject', 'different@example.com', 'other-ciphertext', 'openid email gmail.readonly')
    assert callback(client, begin(client)).headers['location'].endswith('result=different_account')
    assert client.get('/gmail').json()['email'] == 'renamed@example.com'


@pytest.mark.parametrize('failure', ['expired', 'wrong_user', 'wrong_session', 'malformed', 'missing', 'denial', 'missing_code', 'provider', 'logout', 'superseded', 'disconnected'])
def test_callback_failures_consume_valid_state(identities, google, failure):
    _, account, engine = identities
    client, credentials = account()
    state = begin(client)
    original = client
    if failure == 'expired':
        with session_scope(engine) as session:
            session.get(GmailOAuthState, hashlib.sha256(state.encode()).hexdigest()).expires_at = now() - timedelta(seconds=1)
    if failure == 'wrong_user': client, _ = account('b')
    if failure == 'wrong_session':
        client, _ = account(register=False)
        assert client.post('/auth/login', json=credentials).status_code == 200
    if failure == 'malformed': state = 'bad'
    if failure == 'missing': state = ''
    if failure == 'provider': google.fail = True
    if failure == 'logout': client.post('/auth/logout')
    if failure == 'superseded': begin(client)
    if failure == 'disconnected': client.post('/gmail/disconnect')
    extra = {'error': 'access_denied'} if failure == 'denial' else {'code': ''} if failure == 'missing_code' else {}
    response = callback(client, state, **extra)
    assert response.status_code == (401 if failure == 'logout' else 303)
    if response.status_code == 303: assert response.headers['location'].endswith('result=failed')
    assert google.exchanges == int(failure == 'provider')
    if failure in {'denial', 'missing_code', 'provider'}:
        google.fail = False
        assert callback(original, state).headers['location'].endswith('result=failed')
        assert google.exchanges == int(failure == 'provider')


def test_missing_refresh_and_expired_old_grant(identities, google):
    _, account, engine = identities
    client, _ = account()
    google.grant = Grant('synthetic-subject', 'synthetic@example.com', None, 'openid email gmail.readonly')
    assert callback(client, begin(client)).headers['location'].endswith('result=reauthorization_needed')
    assert client.get('/gmail').json()['status'] == 'not_connected'
    google.grant = Grant('synthetic-subject', 'synthetic@example.com', 'synthetic-ciphertext', 'openid email gmail.readonly')
    callback(client, begin(client))
    google.grant = Grant('synthetic-subject', 'synthetic@example.com', None, 'openid email gmail.readonly')
    google.valid = False
    assert callback(client, begin(client)).headers['location'].endswith('result=reauthorization_needed')
    assert client.get('/gmail').json()['status'] == 'reauthorization_needed'


@pytest.mark.parametrize('revoked', [True, False])
def test_disconnect_repeat_concurrency_and_isolation(identities, google, revoked):
    _, account, engine = identities
    a, _ = account('a'); b, _ = account('b')
    callback(a, begin(a)); callback(b, begin(b))
    google.revoked = revoked
    with ThreadPoolExecutor(max_workers=2) as pool:
        responses = list(pool.map(lambda _: a.post('/gmail/disconnect'), range(2)))
    assert all(r.status_code == 200 and r.json()['status'] == 'disconnected' for r in responses)
    assert all(r.json()['revocation_warning'] == (not revoked) for r in responses)
    assert google.revocations == 1
    assert b.get('/gmail').json()['status'] == 'connected'
    owner = UUID(a.get('/auth/me').json()['id'])
    with session_scope(engine) as session:
        row = session.get(GmailConnection, owner)
        assert row.encrypted_refresh_token is None and row.google_subject is None and row.email is None
    assert a.post('/gmail/disconnect').status_code == 200
    assert google.revocations == 1


def test_start_disconnect_protection_and_cors(identities, google):
    app, account, _ = identities
    client, _ = account()
    for path in ['/gmail/start', '/gmail/disconnect']:
        for headers in [{'Origin': 'https://untrusted.example'}, {'X-ApplySync-CSRF': ''}]:
            assert client.post(path, headers=headers).status_code == 403
        response = client.options(path, headers={'Origin': 'https://untrusted.example', 'Access-Control-Request-Method': 'POST', 'Access-Control-Request-Headers': 'X-ApplySync-CSRF'})
        assert response.status_code == 400 and 'access-control-allow-origin' not in response.headers
        response = client.options(path, headers={**HEADERS, 'Access-Control-Request-Method': 'POST', 'Access-Control-Request-Headers': 'X-ApplySync-CSRF'})
        assert response.headers['access-control-allow-credentials'] == 'true'
    client.post('/auth/logout')
    assert client.get('/gmail').status_code == 401
    assert client.post('/gmail/start').status_code == 401
    assert client.post('/gmail/disconnect').status_code == 401


def test_callback_race_single_exchange(identities, google):
    _, account, _ = identities
    client, _ = account()
    state = begin(client)
    with ThreadPoolExecutor(max_workers=2) as pool:
        results = list(pool.map(lambda _: callback(client, state).headers['location'], range(2)))
    assert sorted(r.split('=')[-1] for r in results) == ['connected', 'failed']
    assert google.exchanges == 1


def test_unavailable_is_safe(identities, monkeypatch):
    from gmail_connector import GmailUnavailable
    def unavailable(): raise GmailUnavailable()
    monkeypatch.setattr('gmail_routes.get_connector', unavailable)
    _, account, _ = identities
    client, _ = account()
    assert client.get('/gmail').json()['available'] is False
    assert client.post('/gmail/start').status_code == 503
    assert client.get('/health').json() == {'status': 'healthy'}
    assert client.get('/applications').status_code == 200


def test_disconnect_waits_for_callback_then_removes_grant(identities, google):
    _, account, _ = identities
    client, _ = account()
    state = begin(client)
    entered, release = Event(), Event()
    exchange = google.exchange
    def delayed(code, flow):
        entered.set()
        assert release.wait(5)
        return exchange(code, flow)
    google.exchange = delayed
    with ThreadPoolExecutor(max_workers=2) as pool:
        finish = pool.submit(callback, client, state)
        assert entered.wait(5)
        disconnect = pool.submit(client.post, '/gmail/disconnect')
        release.set()
        assert finish.result().headers['location'].endswith('result=connected')
        assert disconnect.result().json()['status'] == 'disconnected'
    assert client.get('/gmail').json()['status'] == 'disconnected'
    assert google.revocations == 1


def test_logout_serializes_with_exchange_and_revokes_session(identities, google):
    _, account, _ = identities
    client, _ = account()
    state = begin(client)
    entered, release = Event(), Event()
    exchange = google.exchange
    def delayed(code, flow):
        entered.set()
        assert release.wait(5)
        return exchange(code, flow)
    google.exchange = delayed
    with ThreadPoolExecutor(max_workers=2) as pool:
        finish = pool.submit(callback, client, state)
        assert entered.wait(5)
        logout = pool.submit(client.post, '/auth/logout')
        release.set()
        assert finish.result().status_code == 303
        assert logout.result().status_code == 204
    assert client.get('/gmail').status_code == 401
    assert callback(client, state).status_code == 401
```

### Complete new file: `tests/test_gmail_connector.py`

```python
"""Real cryptography/signature checks against in-memory HTTP endpoints only."""
import ast
from base64 import urlsafe_b64encode
import hashlib
import json
import logging
from pathlib import Path
import time
from urllib.parse import parse_qs, urlparse

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.asymmetric import rsa
import httpx
import jwt
import pytest

from gmail_connector.client import GmailConnector, ConnectorError, GmailUnavailable, SCOPES, get_connector
from main import OAuthAccessFilter


@pytest.mark.parametrize('failure', [None, 'nonce', 'audience', 'issuer', 'expired', 'unverified', 'scope', 'signature', 'provider', 'malformed'])
def test_exchange_encryption_pkce_and_identity(failure, caplog):
    key = Fernet.generate_key()
    private = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    jwk = {**jwt.algorithms.RSAAlgorithm.to_jwk(private.public_key(), as_dict=True), 'kid': 'synthetic-key'}
    parameters = {}
    def endpoint(request):
        if request.method == 'GET': return httpx.Response(200, json={'keys': [jwk]})
        body = parse_qs(request.content.decode())
        verifier = body['code_verifier'][0]
        assert urlsafe_b64encode(hashlib.sha256(verifier.encode()).digest()).rstrip(b'=').decode() == parameters['code_challenge'][0]
        assert body['redirect_uri'] == ['http://127.0.0.1:8000/gmail/callback']
        assert body['code'] == ['synthetic-code']
        if failure == 'provider': return httpx.Response(400, json={'error': 'synthetic-sensitive-provider-message'})
        if failure == 'malformed': return httpx.Response(200, json=[])
        claims = {'iss': 'https://accounts.google.com', 'aud': 'synthetic.apps.googleusercontent.com', 'sub': 'synthetic-subject', 'email': 'synthetic@example.com', 'email_verified': True, 'nonce': parameters['nonce'][0], 'iat': int(time.time()), 'exp': int(time.time()) + 600}
        for name, field, value in [('nonce','nonce','wrong'),('audience','aud','wrong'),('issuer','iss','https://untrusted.example'),('expired','exp',1),('unverified','email_verified',False)]:
            if failure == name: claims[field] = value
        signer = rsa.generate_private_key(public_exponent=65537, key_size=2048) if failure == 'signature' else private
        return httpx.Response(200, json={'scope': ' '.join(SCOPES) + (' extra' if failure == 'scope' else ''), 'token_type': 'Bearer', 'access_token': 'synthetic-access', 'refresh_token': 'synthetic-refresh', 'id_token': jwt.encode(claims, signer, algorithm='RS256', headers={'kid': 'synthetic-key'})})
    connector = GmailConnector('synthetic.apps.googleusercontent.com', 'synthetic-secret', key.decode(), transport=httpx.MockTransport(endpoint))
    url, flow = connector.begin('synthetic-state', consent=True)
    parameters.update(parse_qs(urlparse(url).query))
    assert set(parameters['scope'][0].split()) == SCOPES
    assert parameters['code_challenge_method'] == ['S256']
    assert parameters['access_type'] == ['offline'] and parameters['prompt'] == ['consent']
    assert parameters['nonce'][0] not in flow
    with caplog.at_level(logging.INFO):
        if failure:
            with pytest.raises(ConnectorError, match='^Gmail authorization could not be completed.$'):
                connector.exchange('synthetic-code', flow)
        else:
            grant = connector.exchange('synthetic-code', flow)
            assert grant.subject == 'synthetic-subject'
            assert grant.encrypted_refresh_token != 'synthetic-refresh'
            assert Fernet(key).decrypt(grant.encrypted_refresh_token.encode()) == b'synthetic-refresh'
            assert 'synthetic-refresh' not in repr(grant)
    assert all(secret not in caplog.text for secret in ['synthetic-secret', 'synthetic-code', 'synthetic-refresh', 'synthetic-access', 'synthetic-sensitive-provider-message'])


def test_refresh_revocation_and_wrong_key():
    key = Fernet.generate_key()
    cipher = Fernet(key).encrypt(b'synthetic-refresh').decode()
    responses = [httpx.Response(200, json={'access_token': 'synthetic-access'}), httpx.Response(400, json={'error': 'invalid_grant'}), httpx.Response(503, json={}), httpx.Response(200), httpx.Response(503)]
    def endpoint(request):
        assert request.method == 'POST' and 'synthetic-refresh' not in str(request.url)
        return responses.pop(0)
    connector = GmailConnector('synthetic-id', 'synthetic-secret', key.decode(), transport=httpx.MockTransport(endpoint))
    assert connector.validate_refresh(cipher)
    assert not connector.validate_refresh(cipher)
    with pytest.raises(ConnectorError): connector.validate_refresh(cipher)
    assert connector.revoke(cipher)
    assert not connector.revoke(cipher)
    other = GmailConnector('synthetic-id','synthetic-secret',Fernet.generate_key().decode())
    assert not other.revoke(cipher)  # fails decryption before any network call


def test_configuration_and_access_logging(monkeypatch):
    monkeypatch.setattr('gmail_connector.client.dotenv_values', lambda *a, **kw: {})
    for name in ['APPLYSYNC_GOOGLE_CLIENT_ID', 'APPLYSYNC_GOOGLE_CLIENT_SECRET', 'APPLYSYNC_GMAIL_ENCRYPTION_KEY', 'APPLYSYNC_GOOGLE_REDIRECT_URI', 'APPLYSYNC_GMAIL_FRONTEND_ORIGIN']:
        monkeypatch.delenv(name, raising=False)
    with pytest.raises(GmailUnavailable): get_connector()
    record = logging.LogRecord('uvicorn.access', logging.INFO, '', 0, '%s - "%s %s HTTP/%s" %d', ('client','GET','/gmail/callback?code=synthetic-code','1.1',303), None)
    assert OAuthAccessFilter().filter(record) is False
    record.args = ('client','GET','/health','1.1',200)
    assert OAuthAccessFilter().filter(record) is True


def test_connector_architecture_boundary():
    root = Path(__file__).resolve().parents[1]
    excluded = {'.venv', '.git', 'frontend', 'tests', 'migrations', 'docs', 'tmp', 'test-results', '__pycache__', 'gmail_connector'}
    paths = [p for p in root.rglob('*.py') if not excluded.intersection(p.relative_to(root).parts)]
    for path in paths:
        tree = ast.parse(path.read_text(encoding='utf-8'))
        imports = [n.module or '' for n in ast.walk(tree) if isinstance(n, ast.ImportFrom)]
        imports += [alias.name for n in ast.walk(tree) if isinstance(n, ast.Import) for alias in n.names]
        assert not any(n.startswith(('google', 'googleapiclient', 'oauthlib', 'cryptography')) for n in imports), path.name
        text = path.read_text(encoding='utf-8')
        assert 'oauth2.googleapis.com' not in text and 'gmail.googleapis.com' not in text, path.name
    connector = (root/'gmail_connector/client.py').read_text()
    assert 'messages.' not in connector and 'gmail.googleapis.com' not in connector
```

### Complete new file: `tests/test_gmail_migration.py`

```python
"""Preservation rehearsal in a rolled-back schema, never development data."""
from uuid import uuid4
from alembic import command
from alembic.config import Config
from sqlalchemy import inspect, text


def test_gmail_upgrade_preserves_existing_rows(test_engine):
    schema = 'migration_test_' + uuid4().hex
    with test_engine.connect() as connection:
        transaction = connection.begin()
        try:
            assert connection.scalar(text('select current_database()')) == 'applysync_test'
            connection.execute(text(f'CREATE SCHEMA "{schema}"'))
            connection.execute(text(f'SET LOCAL search_path TO "{schema}"'))
            config = Config('alembic.ini'); config.attributes['connection'] = connection
            command.upgrade(config, '0002')
            user, session_id, owned, legacy = [uuid4() for _ in range(4)]
            connection.execute(text("insert into users(id,email,password_hash) values (:id,'synthetic@example.com','synthetic-placeholder')"), {'id':user})
            connection.execute(text("insert into auth_sessions(id,user_id,expires_at) values (:id,:owner,now()+interval '1 hour')"), {'id':session_id,'owner':user})
            for id_, owner in [(owned,user),(legacy,None)]:
                connection.execute(text("insert into job_applications(id,company,role,applied_on,owner_id) values (:id,'Synthetic','Engineer',current_date,:owner)"), {'id':id_,'owner':owner})
            tables = ['users','auth_sessions','job_applications']
            before = {t: connection.execute(text(f'SELECT * FROM {t} ORDER BY id')).all() for t in tables}
            command.upgrade(config,'0003'); command.upgrade(config,'head')
            assert before == {t: connection.execute(text(f'SELECT * FROM {t} ORDER BY id')).all() for t in tables}
            assert connection.scalar(text('select version_num from alembic_version')) == '0003'
            assert set(inspect(connection).get_table_names(schema=schema)) == set(tables+['alembic_version','gmail_connections','gmail_oauth_states'])
            assert inspect(connection).get_pk_constraint('gmail_connections')['constrained_columns'] == ['owner_id']
            assert len(inspect(connection).get_foreign_keys('gmail_oauth_states')) == 2
        finally:
            transaction.rollback()
```
