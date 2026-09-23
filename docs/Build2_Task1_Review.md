# Build 2, Task 1 — frontend foundation and interactive design preview

## Review status and resumption audit

Sanjay has approved the light theme, purple accents, Board/List layouts and overall
design after opening the frontend. He reports successfully adding a preview
application. These are user-reported manual checks, separate from Codex's executed
checks below. No further visual refinement was requested.

The approved checkpoint is being saved with the authorized commit message
`Build approved ApplySync frontend preview` on `main`. Before saving, HEAD was
`203481dcc4bb13d3d51456ae63e4f55f95a739a9` and the index was empty. All 19
frontend source/config/test/manifest/lockfile fingerprints matched this verified
snapshot, and the README/ignore diff matched too. No implementation changes were
needed. The previous successful typecheck, build, 9 component/data tests, 5
Chromium tests and nine-card/zero-error rendered check are reused as historical
agent-executed evidence; they were not rerun for this documentation-only update.

The checkpoint includes the supplied `docs/design.pdf` and all seven intentional
review screenshots. Dependencies, build output, caches, transient browser output,
temporary reference files and secrets are excluded. The final commit identifier
and live push result are reported separately after Git completes; they cannot be
embedded self-referentially in this commit. The remainder of this document records
the earlier verification and its pre-commit working-tree state.

Build 2, Task 1 is approved as a sample-data preview. Backend integration has not
started. Build 2 as a whole remains in progress. The reload/state learning
checkpoint, earlier transaction exercise and detailed API request-flow explanation
remain pending; successful preview creation does not mark those exercises complete.

The original attached Task 1 request, root `AGENTS.md`, and actual source were
checked. During the original implementation, Master Reference v2.0 pages 6–7,
12 and 16 were read, and all three pages of `design.pdf` were rendered and
visually inspected. Master Reference page 3 was also read on resumption. Root
instructions were reread on resumption. No nested
repository instructions were found during the initial inspection.

Before the interruption, the frontend, npm lockfile, ignore rules, README setup
instructions, nine component/data tests, five browser tests and seven screenshots
already existed. Saved Playwright state reported `passed`; previous command
results also recorded passing checks. Those results alone were not treated as
proof of current completion. This review document was missing, and the preview
server still needed to be started.

On resumption, Codex inspected the implementation against the original request,
reran all four requested check commands, regenerated and visually inspected all
seven screenshots, wrote this handoff and started/checked the development server.
No executable source, dependency, style or test change was necessary in this
resumed pass. Existing work and the approved design were preserved.

## Outcome against the request

| Requirement | Inspected implementation and evidence |
| --- | --- |
| Reference-based appearance | Light gray workspace, white 232px sidebar and cards, 64px top bar, purple actions, lavender active navigation, thin borders and pastel stage strips; fresh screenshots inspected. |
| Board/List and shared data | Both receive the same filtered React state; nine fictional records, five provisional stages, empty Offer column, varied dates and long text. |
| Search and filtering | Case-insensitive company/role search AND sample-stage filtering; URL query parameters preserve selections between views and detail routes. |
| Details and creation | `/applications/:id` opens a side panel; `/applications/new` opens a validated preview form. Mobile surfaces fill the viewport. Missing preview IDs have a clear explanation. |
| Validation | Trimmed nonblank company/role, at most 200 Unicode code points, real calendar date including future dates. Errors retain values and focus the first invalid field. |
| Empty states | Empty dataset, empty board column and combined-filter no-results states. Clearing filters retains the selected view. |
| Keyboard and responsive behavior | Semantic links/buttons, labels, visible focus, native modal background inertness, Tab wrapping, Escape and trigger focus restoration. Mobile menu/list and contained horizontal board scrolling. |
| Motion | 160ms control transitions and 180ms panel entry; reduced-motion preference disables both. |
| Data boundary | Visible “Design preview · Sample data” notice. React memory only; additions disappear on reload. No API calls or browser persistence. |
| Reproducibility | Exact dependency pins, npm lockfile, install/run/check commands, and generated-output ignore rules. |

## Changed files and responsibilities

All paths below are relative to the repository root. Complete new source/config/test
files and the tracked-file diff are included in the snapshot appendix below.

| Files | Responsibility |
| --- | --- |
| `.gitignore` | Excludes frontend dependencies, build output, Playwright output and temporary reference/resolution files; existing secret rules retained. |
| `README.md` | Windows install/run/check instructions, preview semantics and link to this handoff; backend setup retained. |
| `frontend/package.json`, `frontend/package-lock.json` | Scripts, compatible exact dependency versions and reproducible npm dependency graph. |
| `frontend/index.html`, `frontend/public/mark.svg` | Browser entry/title and original ApplySync mark; no remote assets. |
| `frontend/tsconfig.json`, `frontend/vite.config.ts` | Strict TypeScript, React/Tailwind build, fixed loopback development port and Vitest configuration. |
| `frontend/playwright.config.ts` | Chromium checks against a temporary production preview server on port 4173. |
| `frontend/src/main.tsx` | React entry point, BrowserRouter and shared styles. |
| `frontend/src/data.ts` | API-shaped fields, separate sample-stage wrapper, synthetic fixtures, filtering, date formatting, initials and validation. |
| `frontend/src/App.tsx` | Shared in-memory state, route/query state, toolbar, empty states, preview creation and detail content. |
| `frontend/src/components/Shell.tsx` | Reusable sidebar, top bar, main region, skip link and mobile navigation. |
| `frontend/src/components/ui.tsx` | Shared buttons, stage labels, preview notice and accessible modal lifecycle. |
| `frontend/src/components/ApplicationsView.tsx` | Shared company mark, routed board cards and responsive list. |
| `frontend/src/components/ApplicationForm.tsx` | Controlled form values, field validation/errors and submit/cancel actions. |
| `frontend/src/styles.css` | Tailwind import/tokens, reference-based component styling, responsive rules, focus and reduced motion. |
| `frontend/src/test-setup.ts` | Testing Library cleanup and minimal jsdom dialog stubs. |
| `frontend/src/data.test.ts`, `frontend/src/App.test.tsx` | Four data/validation tests and five rendered-component behavior tests. |
| `frontend/e2e/preview.spec.ts` | Five real-browser checks, responsive/keyboard assertions and screenshot capture. |
| `docs/screenshots/Build2_Task1/*.png` | Seven actual rendered screenshots for visual review. |
| `docs/Build2_Task1_Review.md` | This review, results, limitations and source snapshot. |

`docs/design.pdf` was already an untracked user-supplied reference when this task
began. It was preserved. It is not a generated frontend file or an implementation
change. Backend source, dependencies, migrations and configuration are unchanged.
No database was accessed; the user's existing development record is untouched.

## Reference fidelity and intentional differences

- Page 1 supplies the main board composition: compact bordered white cards,
  slim pastel column headings, written stage labels/counts, white sidebar and
  purple selection/actions. Columns have a 250px minimum (260px on phones),
  14px gaps and internal horizontal scrolling rather than compressed cards.
- Page 2 supplies the card treatment, spacing, initials and restrained hierarchy.
  The requested alternative is a readable List view, not an additional job-grid
  screen. Ordinary card titles/company text are 15px/14px; supporting labels are
  smaller without copying illegibly small screenshot text.
- Page 3 supplies the role/company heading and boxed factual overview. ApplySync
  uses a route-backed desktop panel and full-screen mobile detail. It deliberately
  has no invented description, email body, notes or timeline.
- Employer navigation, account controls, candidate portraits, document/comment
  counts, sharing controls and fake notification buttons were omitted. Branding
  is original; fictional company initials avoid remote logo requests.
- The selected color tokens are adaptations, not colors measured from the PDF.
  Historical contrast calculations on the final tokens found white/purple 6.30:1,
  muted text/workspace 4.63:1 and stage text/backgrounds at least 5.20:1. This is
  not a full accessibility certification.

Fresh rendered images inspected after the resumed browser run:

- [Desktop board](screenshots/Build2_Task1/desktop-board.png)
- [Desktop list](screenshots/Build2_Task1/desktop-list.png)
- [Desktop detail and focus](screenshots/Build2_Task1/desktop-detail.png)
- [Form validation](screenshots/Build2_Task1/form-validation.png)
- [Mobile board](screenshots/Build2_Task1/mobile-board.png)
- [Mobile stacked list](screenshots/Build2_Task1/mobile-list.png)
- [Mobile detail with long text](screenshots/Build2_Task1/mobile-detail.png)

## Dependencies and local setup

Observed environment: Windows, Node **22.12.0**, npm **10.9.0**. One package
manager is used: npm. No global installation or Node replacement was performed.

Runtime pins: React/React DOM **19.3.0**, React Router **7.18.4**, Lucide React
**1.47.0**. Build/check pins include Vite **7.3.6**, TypeScript **5.9.3**,
Tailwind and its Vite plugin **4.3.3**, React Vite plugin **5.2.0**, Vitest
**5.0.1**, Testing Library React **16.3.3**, user-event **14.6.7**, jest-dom
**7.0.1**, jsdom **26.1.0** and Playwright **1.63.0**. Type packages are also
exactly pinned in the complete manifest below.

Package engine/peer metadata was checked during implementation. Router 8 required
a newer Node patch than installed, so compatible Router 7 was selected. Vite 7 and
Vitest 5 support the existing Node 22.12 environment; installation and current
build/test results verify this actual combination. React Hook Form/Zod and
TanStack Query are not needed for a three-field in-memory preview; data-fetching
integration belongs to the next task.

Official references consulted during implementation:
[Vite setup](https://vite.dev/guide/),
[Tailwind Vite setup](https://tailwindcss.com/docs/installation/using-vite), and
[React Router declarative setup](https://reactrouter.com/start/declarative/installation).
Exact package metadata and the lockfile govern the installed versions; those
documentation pages can change.

From PowerShell on a fresh checkout:

```powershell
Set-Location 'C:\Users\sanja\Desktop\ApplySync\frontend'
npm.cmd ci
npm.cmd run dev
```

Open [the preview](http://127.0.0.1:5173/applications). It needs neither the backend
nor PostgreSQL. No frontend environment file is needed. Never copy backend secrets
to browser-visible variables. Stop your own terminal's server with Ctrl+C.

The resumed session already started this command and left it running on
`127.0.0.1:5173` (observed Vite process ID 3832). HTTP returned **200**. A fresh
headless Chromium visit to that development URL observed the ApplySync preview
title, **9 cards**, and **0 page errors**. This was a real server/render check,
separate from jsdom tests and the production preview used by Playwright.

The in-app browser connector returned no available browsers, so Codex could not
open a user-visible browser tab. Use the clickable URL above. Rendered-page
inspection was performed using the actual Chromium tests/screenshots, not inferred
from the HTML response alone.

## Agent-executed checks from prior verification (reused)

These results were executed by Codex **after resumption**, not copied from the
pre-interruption test totals. Commands run in `frontend/` unless stated otherwise.

| Exact check | Current observed result |
| --- | --- |
| `node --version`; `npm.cmd --version` | `v22.12.0`; `10.9.0`. |
| `npm.cmd run typecheck` | Exit 0; no TypeScript errors. |
| `npm.cmd run build` | Exit 0; repeats typecheck; Vite 7.3.6 transforms 1905 modules, builds in 2.49s. CSS 19.82 kB (gzip 5.35), JS 283.85 kB (gzip 90.63). |
| `npm.cmd run test` | Exit 0; **2 files, 9 tests passed**, 15.16s. jsdom component/data checks. |
| `npm.cmd run test:e2e` | Exit 0; **5 Chromium tests passed**, 7.2s, one worker. Real production-preview server on 4173; stopped by Playwright afterward. |
| `npm.cmd ls --depth=0` | Exit 0; all 18 direct runtime/dev packages present at manifest versions, no invalid/missing dependencies reported. |
| Manifest/lockfile comparison | Both dependency groups in the manifest exactly match the lockfile root. |
| Credential-pattern scan of 19 allowlisted frontend files and README | Zero findings for credential-bearing URLs, private keys, known token prefixes or assigned secret values. No `.env` contents were read; this is a bounded pattern check, not a guarantee against every possible secret. |
| `npm.cmd run dev` | Vite ready in 620ms; left running on loopback port 5173. |
| `Invoke-WebRequest -UseBasicParsing 'http://127.0.0.1:5173/applications'` | HTTP 200; expected ApplySync title and Vite client present. |
| Chromium development-server smoke check | `page.goto` status 200; title `Applications · ApplySync preview`; `.application-card` count 9; page-error array empty. |
| `Get-NetTCPConnection -LocalPort 5173 -State Listen` | Authorized retry confirmed `127.0.0.1`, port 5173, process 3832. |
| Root `git diff --check` | No whitespace errors; Git reports only its normal future LF-to-CRLF conversion notices. |
| Root `git diff --exit-code -- '*.py' migrations requirements.txt .env.example` | Exit 0, no backend diff. |
| Root `git check-ignore frontend/node_modules frontend/dist frontend/test-results .env` | All four paths ignored. `git ls-files .env` returned no paths; contents never read. |
| Root `git diff --cached --name-only` | Empty: nothing staged. |
| Review snapshot validation | All 19 source/lockfile SHA-256 fingerprints match; all 18 non-lock new files are embedded in full. New text files pass the whitespace scan. Initial scan caught three whitespace-only lines copied from Git diff context; these were normalized and the check passed on rerun. |

Browser assertions cover combined search/filter empty state, view/query retention,
keyboard card activation, detail URL, focus inside the modal and back to its
trigger, preserved invalid input, trimmed creation, future dates, shared list/board
updates, missing-record behavior after reload, and zero fetch/XHR data requests in
the creation flow. Responsive checks include 320, 768, 860, 900 and 1280px page
widths, 1600px desktop screenshots, 390×844 mobile screenshots and 1100px
reduced-motion/board-scroll checks. Long card text stays inside its card. Reduced
motion produces `animation-name: none` and `transition-duration: 0s`.

Component/data assertions were inspected as well as executed: empty dataset and
Offer column, filter clearing while retaining List, no-results, missing detail,
successful state update, blank/overlong fields, impossible and leap dates,
200-character boundary and UTC calendar formatting. The dialog stubs in
`test-setup.ts` only toggle the `open` attribute; they do not prove browser focus
or native inertness. Real browser checks provide that separate evidence.

## Historical results, resolved failures and limits

- Before interruption, `npm.cmd ci` successfully installed the final lockfile:
  168 packages added, 169 audited, zero vulnerabilities. A final live registry
  audit also reported zero. These install/audit results were **not rerun on
  resumption**; the current `npm ls`, typecheck, build and tests passed.
- Earlier Vitest 3 had two moderate development-server audit advisories. It was
  replaced by compatible Vitest 5.0.1. An attempted intermediate Vitest 4 update
  hit npm's internal `edgesOut` resolver error; the final version installed and
  passed checks. jsdom's dependency emitted a `whatwg-encoding` deprecation warning
  during installation; no final audit vulnerability was reported.
- Earlier build attempts inside the process sandbox failed with `spawn EPERM`;
  authorized process execution resolved that. A resumed listener inspection also
  encountered sandbox access denial; the authorized retry succeeded. These are
  tool-environment failures, not unresolved application failures.
- Earlier verification caught unsupported test selector options, dialog Tab focus
  leaving the intended cycle, intermediate-width toolbar overflow, and overly
  exact mobile fractional-pixel assertions. Those were fixed before interruption.
  Screenshots now disable active animations to avoid recording a transient fade.
  Current checks pass with those fixes in place.
- Current browser output includes harmless `NO_COLOR`/`FORCE_COLOR` warnings. No
  current type/build/component/browser check is failed or blocked.
- Only Chromium was tested. Firefox, WebKit, real phone hardware, screen readers
  and a comprehensive automated accessibility audit were not run. Touch/keyboard
  behavior and visual approval still need Sanjay's review. The UI has a 320px
  minimum width; smaller viewports are not a target of this preview.
- The previous **57 backend tests** remain historical Build 1 evidence. They were
  not rerun; backend/database tests are unnecessary for this isolated frontend
  task. No service/database restart, migration or database write was performed.
- No backend integration, authentication, Gmail, persistence, drag-and-drop or
  authoritative stage changes exist in this preview. There is no API pagination
  or server-error path yet. Production hosting/deep-link server configuration is
  deferred; this task checks Vite local servers.
- A fresh remote fetch or live GitHub comparison was not performed. Nothing was
  committed or pushed, and remote-tracking refs are not offered as live proof.

## Actual success and failure paths

**Success:** `ApplicationForm.submit` calls `validateCreate` in `data.ts`. It trims
the two text fields and returns clean valid values. `Applications.add` in
`App.tsx` generates a UUID and timestamp, wraps the API-shaped fields with the
provisional `sampleStage: 'Applied'`, and prepends the record using `setRecords`.
It sets preview-only feedback and closes the route-backed form. `Modal` cleanup
restores the prior body overflow/focus. `filterApplications` derives visible data;
`Board` and `ApplicationList` render from that same state. An active filter may
hide the new record and the feedback explains this. There is **no persistence or
external call** in this path.

**Failure:** a whitespace company and otherwise valid fields reach
`ApplicationForm.submit`. `validateCreate` trims company to an empty string and
returns `Enter a company.`. The form stores field errors, focuses that input and
returns before calling `onAdd`. The user's other values remain; no record or
success message is created. The dialog stays open with an associated, written
error rather than relying on color alone.

**Learning walkthrough:** `sampleApplications` lives in `data.ts`; `useState`
in `Applications` initializes the mounted component's state from those fixtures.
Filtering derives a subset and never deletes those records. Board/List are two
representations of that subset. URL query state survives switching views and
opening details, while newly added records live only in React memory. Reload
starts the application again from the original fixtures, so a new record's old
detail URL can no longer find it.

Three concepts to distinguish: React state versus persistent storage; route/query
state versus selected data; and jsdom component tests versus real browser tests.
The next focused learning checkpoint is for Sanjay to add a fictional application,
find it in List, reload, and explain why it disappears using `setRecords` and
`sampleApplications`. This checkpoint has **not** been completed on his behalf.
The earlier Build 1 transaction exercise and detailed API request-flow learning
remain pending; basic file familiarity and reported Swagger checks do not mark
those exercises complete.

## Git and Planning & Progress handoff at verification time

- Repository: `C:\Users\sanja\Desktop\ApplySync`.
- Branch: `main`.
- Base and current commit: `203481dcc4bb13d3d51456ae63e4f55f95a739a9`
  (`Add manual application create list and detail APIs`).
- Staged changes: none.
- Tracked unstaged changes: `.gitignore`, `README.md`.
- Untracked task work: `frontend/` source/config/tests/manifest/lockfile,
  seven `docs/screenshots/Build2_Task1/` images, and this review.
- Pre-existing untracked user asset: `docs/design.pdf`, preserved.
- `.env` remains ignored and untracked; generated files/environments are excluded.
- Task 1 is implemented and verified for local visual review, not committed.
  Sanjay's visual acceptance and focused learning checkpoint remain open.
  Build 2 is **not complete**. After review, the next bounded task is real manual
  API integration while preserving the approved interface and explicitly handling
  the backend's lack of authoritative stages.

## Source snapshot appendix

The following tracked diff and complete new source/config/test files capture the
reviewed working tree. The complete generated dependency graph is supplied as
[`frontend/package-lock.json`](../frontend/package-lock.json), rather than
duplicating thousands of generated lines here. The appendix includes its SHA-256
along with hashes for source files, so later comparisons can detect drift.
Screenshots and the pre-existing reference PDF are linked above; binary files,
dependencies, caches, secrets and this document's own contents are not embedded.

<!-- BEGIN GENERATED SNAPSHOT -->

### Relevant tracked diff

```diff
diff --git a/.gitignore b/.gitignore
index 8354ab0..140a15c 100644
--- a/.gitignore
+++ b/.gitignore
@@ -5,3 +5,9 @@
 __pycache__/
 .pytest_cache/
 pytest-cache-files-*/
+frontend/node_modules/
+frontend/dist/
+frontend/test-results/
+frontend/playwright-report/
+tmp/design-reference/
+tmp/frontend-resolution/
diff --git a/README.md b/README.md
index 92cc77e..9e7caba 100644
--- a/README.md
+++ b/README.md
@@ -1,13 +1,72 @@
 # applysync
 AI-powered privacy-first job application tracker that automatically syncs Gmail application emails into a Kanban dashboard.

-Current scope: Build 1, task 2 (manual create/list/detail APIs backed by PostgreSQL).
-`GET /health` still returns `{"status":"healthy"}`. These unauthenticated APIs are
-local development functionality. Gmail and the dashboard above describe the project
-goal, not implemented features.
+Current scope: Build 2, task 1 adds an interactive frontend **design preview** with
+synthetic, in-memory applications. The existing Build 1 create/list/detail APIs and
+`GET /health` remain unchanged. The preview does not call them. Gmail and automatic
+tracking above describe the project goal, not implemented features.
+
+## Frontend design preview (no backend required)
+
+Tested with **Node 22.12.0 and npm 10.9.0** on Windows. Use npm for this frontend;
+exact dependency versions are recorded in `frontend/package.json` and its lockfile.
+From PowerShell:
+
+```powershell
+Set-Location 'C:\Users\sanja\Desktop\ApplySync\frontend'
+npm.cmd ci
+npm.cmd run dev
+```
+
+Open **http://127.0.0.1:5173/applications**. Stop with Ctrl+C. Port 5173 is fixed;
+if it is occupied, stop your previous frontend server first. The backend server and
+PostgreSQL are not needed for this preview. Do not copy backend secrets into frontend
+environment files; browser-visible configuration cannot protect credentials.
+
+Use Board/List over the same nine fictional records, search by company/role, and
+combine search with a sample-stage filter. Cards/list rows open routed details.
+The Add application form trims text, rejects blank or over-200-character values,
+and accepts valid calendar dates including future dates. New records start in the
+provisional **Applied** stage and appear in both views. Existing filters remain
+selected, so they may hide a new record; the success message explains this.
+
+All records are held in React memory. Additions **reset on reload**, and reopening
+a new-record detail URL after reload shows a clear missing-preview-record message.
+Search/filter/view selections live in URL query parameters, not browser storage.
+Sample stages live outside the API-shaped `Application` type. There is no backend
+stage contract, drag-and-drop, API request, local/session storage, authentication,
+remote logo request, or persistent save. Backend integration is the next task.
+
+The interface follows the three supplied `docs/design.pdf` screenshots with a white
+sidebar/cards, cool-gray workspace, purple actions, pastel board headers and restrained
+detail hierarchy. On phones the sidebar becomes a menu, list records stack, and
+details/forms fill the screen. The board scrolls inside its own region. Escape closes
+panels; keyboard focus returns to the trigger. Reduced-motion preferences are honored.
+
+Frontend checks (run from `frontend/`):
+
+```powershell
+npm.cmd run typecheck
+npm.cmd run build
+npm.cmd run test
+# One-time download for browser checks:
+npx.cmd playwright install chromium
+npm.cmd run test:e2e
+```
+
+Browser tests use a temporary production preview server on port 4173 and save
+screenshots under `docs/screenshots/Build2_Task1/`. Keep that port free. Tests cover
+search/filter/view state, validation, preview creation/reset, route-backed details,
+keyboard handling, reduced motion and desktop/mobile layouts. Native dialog behaviour
+is tested in Chromium; the component-test DOM only supplies a minimal dialog stub.
+
+See [Build 2 Task 1 review](docs/Build2_Task1_Review.md) for evidence, reference
+comparisons, dependency choices, screenshots, limitations and a learning walkthrough.

 ## Reproducible local setup (Windows PowerShell)

+The following commands concern the **backend** and are not required for the frontend preview.
+
 Use CPython **3.14.2**, the existing `.venv`, and local PostgreSQL (inspected server
 installation: 14.7). From the repository root:
```

### File fingerprints

| File | SHA-256 |
| --- | --- |
| `frontend/e2e/preview.spec.ts` | `a2b163072897f8d5c0984918d870e94abf1c57e3d7a306d6b25a49144347ae80` |
| `frontend/index.html` | `6102c6f6f47334db86443c218a6d8bbc2dffe32ffb36873ec1ae3ef4297a5a79` |
| `frontend/package-lock.json` | `7df0ba642f379d02b9e659ea6e473c7417d789064af7d8bcdfb7d45049ffe1bf` |
| `frontend/package.json` | `728602f5e9c807ac75d30b752b36c8f03e6a847f94479fd27a827cfc63d4211b` |
| `frontend/playwright.config.ts` | `a10959085c2eda5bd8224a2f54291d0fb613bfdbb7240f261c1e3fdb9a8a3028` |
| `frontend/public/mark.svg` | `7f523c083fa607648fbe71520543bf907da284aa7ebd6eb87d0bbff1b5aa23c3` |
| `frontend/src/App.test.tsx` | `f751cd4cdc12c6f1b2f2b361d9fd9cded182bde9ba4b0034897d79425d331e4a` |
| `frontend/src/App.tsx` | `6fa5257b0f6a8c089d8a840fa16f68083d35b0f1d2574dc046125dd8071e4a64` |
| `frontend/src/components/ApplicationForm.tsx` | `b0c1172f150f651947914ad0c8ad8e9c188da9c04db7c797f3a200d9a6c01f50` |
| `frontend/src/components/ApplicationsView.tsx` | `829d9765bc6c95d013ccbf9d43391575e7b0da650fd3093ab5c647a680a19b89` |
| `frontend/src/components/Shell.tsx` | `9929067eb4aaf469bc7bc062cd4ecba2b7cf786e19b1936cc126c72795c864bb` |
| `frontend/src/components/ui.tsx` | `9925654fad10c7702593afec8e2a4cb585114b38a47cb8452a140fcaf20f7948` |
| `frontend/src/data.test.ts` | `6ee86f600141444fb6c5ad3226be9c707b3fb8ce389cad7b3d080432a284951d` |
| `frontend/src/data.ts` | `edc53720a6c27b1f023bd16e5d75a5966c55fef52eb9b1f27d87be9ac8fdec77` |
| `frontend/src/main.tsx` | `77f2f66409767a1ca3f55e409f24f92ab955d7436ecb04d5fee8efe897177db0` |
| `frontend/src/styles.css` | `2407334a7fbe9cafe57bfef80e44f112277189ee35c6699a682a433d8903df5f` |
| `frontend/src/test-setup.ts` | `8c9cc7521c2e43c7f8b6cf67dcf9263ce84042487208d62f4bce628d645cb9c5` |
| `frontend/tsconfig.json` | `3ae2a8e1eb24c9fc6724ab30919974a00b9ea86e0fb0516c870851fe654792df` |
| `frontend/vite.config.ts` | `73b9993c3d51666f035b93cd4801d6b91efbd98095be5bf64c9fc515f46514b9` |

### Complete file: frontend/e2e/preview.spec.ts

```typescript
import { expect, test } from '@playwright/test'
import { mkdirSync } from 'node:fs'

const screenshots = '../docs/screenshots/Build2_Task1'
mkdirSync(screenshots, { recursive: true })

test('intermediate viewport widths keep controls inside the page', async ({ page }) => {
  await page.goto('/applications')
  for (const width of [320, 768, 860, 900, 1280]) {
    await page.setViewportSize({ width, height: 900 })
    expect(await page.evaluate(() => document.documentElement.scrollWidth <= window.innerWidth), `page overflow at ${width}px`).toBe(true)
  }
})

test('desktop reference layout, shared filtering, details and focus return', async ({ page }) => {
  const failures: string[] = []
  page.on('pageerror', error => failures.push(error.message))
  await page.goto('/applications')
  await expect(page.getByRole('link', { name: 'Product Designer at Cedar & Finch' })).toBeVisible()
  await expect(page.getByRole('region', { name: 'Offer, 0 applications' })).toContainText('No applications here')
  expect(await page.evaluate(() => document.documentElement.scrollWidth <= window.innerWidth)).toBe(true)
  const longCard = page.getByRole('link', { name: /Senior User Experience Researcher/ })
  expect(await longCard.evaluate(element => element.scrollWidth <= element.clientWidth)).toBe(true)
  await page.screenshot({ path: `${screenshots}/desktop-board.png`, fullPage: true })
  await page.getByRole('searchbox').fill('cedar')
  await page.getByLabel('Sample stage').selectOption('Interview')
  await expect(page.getByText('No matching applications')).toBeVisible()
  await page.getByRole('button', { name: 'List', exact: true }).click()
  await expect(page.getByRole('searchbox')).toHaveValue('cedar')
  await page.getByLabel('Sample stage').selectOption('All stages')
  const card = page.getByRole('link', { name: 'Product Designer at Cedar & Finch' })
  await card.focus()
  await page.keyboard.press('Enter')
  await expect(page.getByRole('dialog')).toBeVisible()
  await expect(page).toHaveURL(/00000000-0000-4000-8000-000000000001/)
  await page.screenshot({ path: `${screenshots}/desktop-detail.png`, animations: 'disabled' })
  // Native modal must prevent focus escaping to the background.
  for (let i = 0; i < 8; i++) await page.keyboard.press('Tab')
  expect(await page.evaluate(() => !!document.querySelector('dialog')?.contains(document.activeElement))).toBe(true)
  await page.keyboard.press('Escape')
  await expect(page.getByRole('dialog')).toHaveCount(0)
  await expect(card).toBeFocused()
  await expect(page.getByRole('searchbox')).toHaveValue('cedar')
  await page.getByRole('searchbox').fill('')
  await page.screenshot({ path: `${screenshots}/desktop-list.png`, fullPage: true })
  expect(failures).toEqual([])
})

test('preview validation, add, reload reset and no data requests', async ({ page }) => {
  const dataRequests: string[] = []
  page.on('request', request => {
    if (['fetch', 'xhr'].includes(request.resourceType())) dataRequests.push(request.url())
  })
  await page.goto('/applications')
  const trigger = page.getByRole('link', { name: 'Add application', exact: true })
  await trigger.click()
  const dialog = page.getByRole('dialog')
  await expect(dialog.getByLabel('Company', { exact: false })).toBeFocused()
  await dialog.getByLabel('Company', { exact: false }).fill('   ')
  await dialog.getByLabel('Role', { exact: false }).fill('Interface Engineer')
  await dialog.getByLabel('Applied date', { exact: false }).fill('2100-01-01')
  await dialog.getByRole('button', { name: 'Add to preview' }).click()
  await expect(dialog.getByRole('alert')).toContainText('Enter a company.')
  await expect(dialog.getByLabel('Role', { exact: false })).toHaveValue('Interface Engineer')
  await page.screenshot({ path: `${screenshots}/form-validation.png`, animations: 'disabled' })
  await dialog.getByLabel('Company', { exact: false }).fill(' Preview Works ')
  await dialog.getByRole('button', { name: 'Add to preview' }).click()
  await expect(page.getByRole('status')).toContainText('Preview Works added to the preview')
  await expect(trigger).toBeFocused()
  await expect(page.getByRole('region', { name: 'Applied, 5 applications' })).toBeVisible()
  await page.getByRole('button', { name: 'List', exact: true }).click()
  await page.getByRole('link', { name: 'Interface Engineer at Preview Works' }).click()
  await expect(page.getByRole('dialog')).toContainText('1 Jan 2100')
  await page.reload()
  await expect(page.getByRole('dialog')).toContainText('Application not found')
  await page.keyboard.press('Escape')
  await expect(page.getByRole('link', { name: 'Interface Engineer at Preview Works' })).toHaveCount(0)
  expect(dataRequests).toEqual([])
})

test('mobile navigation, contained board, stacked list and full-screen details', async ({ page }) => {
  await page.setViewportSize({ width: 390, height: 844 })
  await page.goto('/applications')
  expect(await page.evaluate(() => document.documentElement.scrollWidth <= window.innerWidth)).toBe(true)
  const board = page.getByRole('region', { name: /Application board/ })
  expect(await board.evaluate(element => element.scrollWidth > element.clientWidth)).toBe(true)
  await page.screenshot({ path: `${screenshots}/mobile-board.png`, fullPage: true })
  const menu = page.getByRole('button', { name: 'Open navigation' })
  await menu.click()
  await expect(page.getByRole('dialog')).toBeVisible()
  await page.keyboard.press('Escape')
  await expect(menu).toBeFocused()
  await page.getByRole('button', { name: 'List', exact: true }).click()
  expect(await page.evaluate(() => document.documentElement.scrollWidth <= window.innerWidth)).toBe(true)
  await page.screenshot({ path: `${screenshots}/mobile-list.png`, fullPage: true })
  await page.getByRole('link', { name: /Senior User Experience Researcher/ }).click()
  await expect(page.getByRole('dialog')).toHaveCSS('opacity', '1')
  const bounds = await page.getByRole('dialog').boundingBox()
  expect(bounds?.width).toBeCloseTo(390, 1)
  expect(bounds?.height).toBeCloseTo(844, 1)
  await page.screenshot({ path: `${screenshots}/mobile-detail.png`, animations: 'disabled' })
  await page.keyboard.press('Escape')
})

test('reduced motion and board scroll position survive opening a detail', async ({ page }) => {
  await page.emulateMedia({ reducedMotion: 'reduce' })
  await page.setViewportSize({ width: 1100, height: 850 })
  await page.goto('/applications')
  const board = page.getByRole('region', { name: /Application board/ })
  await board.evaluate(element => { element.scrollLeft = element.scrollWidth })
  const before = await board.evaluate(element => element.scrollLeft)
  await page.getByRole('link', { name: 'Frontend Developer at Pebblewave' }).click()
  expect(await page.getByRole('dialog').evaluate(element => getComputedStyle(element).animationName)).toBe('none')
  await page.keyboard.press('Escape')
  expect(await board.evaluate(element => element.scrollLeft)).toBe(before)
  expect(await page.getByRole('button', { name: 'Board', exact: true }).evaluate(element => getComputedStyle(element).transitionDuration)).toBe('0s')
})
```

### Complete file: frontend/index.html

```html
<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <meta name="theme-color" content="#5145e5" />
    <title>Applications · ApplySync preview</title>
    <link rel="icon" type="image/svg+xml" href="/mark.svg" />
  </head>
  <body><div id="root"></div><script type="module" src="/src/main.tsx"></script></body>
</html>
```

### Complete file: frontend/package.json

```json
{
  "name": "applysync-preview",
  "private": true,
  "version": "0.1.0",
  "type": "module",
  "engines": {
    "node": "^22.12.0 || ^24.0.0 || >=26.0.0"
  },
  "scripts": {
    "dev": "vite --host 127.0.0.1",
    "typecheck": "tsc --noEmit",
    "build": "npm run typecheck && vite build",
    "preview": "vite preview --host 127.0.0.1",
    "test": "vitest run",
    "test:e2e": "playwright test"
  },
  "dependencies": {
    "lucide-react": "1.47.0",
    "react": "19.3.0",
    "react-dom": "19.3.0",
    "react-router": "7.18.4"
  },
  "devDependencies": {
    "@playwright/test": "1.63.0",
    "@tailwindcss/vite": "4.3.3",
    "@testing-library/jest-dom": "7.0.1",
    "@testing-library/react": "16.3.3",
    "@testing-library/user-event": "14.6.7",
    "@types/node": "22.20.4",
    "@types/react": "19.3.0",
    "@types/react-dom": "19.3.0",
    "@vitejs/plugin-react": "5.2.0",
    "jsdom": "26.1.0",
    "tailwindcss": "4.3.3",
    "typescript": "5.9.3",
    "vite": "7.3.6",
    "vitest": "5.0.1"
  }
}
```

### Complete file: frontend/playwright.config.ts

```typescript
import { defineConfig } from '@playwright/test'

export default defineConfig({
  testDir: './e2e', fullyParallel: false, workers: 1, reporter: 'list',
  use: { baseURL: 'http://127.0.0.1:4173', browserName: 'chromium', viewport: { width: 1600, height: 1000 }, trace: 'retain-on-failure' },
  webServer: { command: 'npm run preview -- --port 4173 --strictPort', url: 'http://127.0.0.1:4173', reuseExistingServer: false },
})
```

### Complete file: frontend/public/mark.svg

```xml
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32"><rect width="32" height="32" rx="8" fill="#5145e5"/><path d="M9 23 16 8l7 15M12 18h8" fill="none" stroke="white" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/></svg>
```

### Complete file: frontend/src/App.test.tsx

```tsx
import { fireEvent, render, screen, within } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { MemoryRouter } from 'react-router'
import { expect, it } from 'vitest'
import { App } from './App'

function setup(path = '/applications', empty = false) {
  const user = userEvent.setup()
  render(<MemoryRouter initialEntries={[path]}><App initialRecords={empty ? [] : undefined} /></MemoryRouter>)
  return user
}
it('shows stage counts and an empty Offer column', () => {
  setup()
  expect(screen.getByRole('region', { name: 'Applied, 4 applications' })).toBeInTheDocument()
  expect(screen.getByRole('region', { name: 'Offer, 0 applications' })).toHaveTextContent('No applications here')
})
it('retains combined filters across views and clears no-results', async () => {
  const user = setup()
  await user.type(screen.getByRole('searchbox'), 'cedar')
  await user.selectOptions(screen.getByLabelText('Sample stage'), 'Interview')
  expect(screen.getByText('No matching applications')).toBeInTheDocument()
  await user.click(screen.getByRole('button', { name: 'List' }))
  expect(screen.getByRole('searchbox')).toHaveValue('cedar')
  expect(screen.getByLabelText('Sample stage')).toHaveValue('Interview')
  await user.click(screen.getByRole('button', { name: 'Clear search & filter' }))
  expect(screen.getByRole('region', { name: 'Application list' })).toBeInTheDocument()
  expect(screen.getByRole('button', { name: 'List' })).toHaveAttribute('aria-pressed', 'true')
})
it('preserves input on validation errors and adds a trimmed preview record to both views', async () => {
  const user = setup()
  await user.click(screen.getByRole('link', { name: 'Add application' }))
  const dialog = screen.getByRole('dialog')
  await user.type(within(dialog).getByLabelText('Company', { exact: false }), '   ')
  await user.type(within(dialog).getByLabelText('Role', { exact: false }), ' Engineer ')
  fireEvent.change(within(dialog).getByLabelText('Applied date', { exact: false }), { target: { value: '2100-01-01' } })
  await user.click(screen.getByRole('button', { name: 'Add to preview' }))
  expect(screen.getByRole('alert')).toHaveTextContent('Enter a company.')
  expect(within(dialog).getByLabelText('Role', { exact: false })).toHaveValue(' Engineer ')
  await user.clear(within(dialog).getByLabelText('Company', { exact: false }))
  await user.type(within(dialog).getByLabelText('Company', { exact: false }), ' Preview Company ')
  await user.click(screen.getByRole('button', { name: 'Add to preview' }))
  expect(screen.queryByRole('dialog')).not.toBeInTheDocument()
  expect(screen.getByRole('status')).toHaveTextContent('Preview Company added to the preview')
  expect(screen.getByRole('link', { name: 'Engineer at Preview Company' })).toBeInTheDocument()
  await user.click(screen.getByRole('button', { name: 'List' }))
  expect(screen.getByRole('link', { name: 'Engineer at Preview Company' })).toBeInTheDocument()
})
it('opens route-backed detail and returns without losing search', async () => {
  const user = setup('/applications?q=cedar&view=list')
  await user.click(screen.getByRole('link', { name: 'Product Designer at Cedar & Finch' }))
  expect(screen.getByRole('dialog')).toHaveTextContent('Application overview')
  expect(screen.getByRole('dialog')).toHaveTextContent('21 Sept 2026')
  await user.click(screen.getByRole('button', { name: 'Back to applications' }))
  expect(screen.queryByRole('dialog')).not.toBeInTheDocument()
  expect(screen.getByRole('searchbox')).toHaveValue('cedar')
})
it('supports an empty dataset and direct missing-record routes', () => {
  setup('/applications/missing', true)
  expect(screen.getByText('Your next chapter starts here')).toBeInTheDocument()
  expect(screen.getByRole('dialog')).toHaveTextContent('Application not found')
})
```

### Complete file: frontend/src/App.tsx

```tsx
import { useState } from 'react'
import { Link, Navigate, useLocation, useNavigate, useParams, useSearchParams, Route, Routes } from 'react-router'
import { ArrowLeft, CalendarDays, Columns3, List, Plus, Search, SearchX, SlidersHorizontal } from 'lucide-react'
import { Shell } from './components/Shell'
import { Board, ApplicationList, CompanyMark } from './components/ApplicationsView'
import { Button, Modal, PreviewNotice, StageLabel } from './components/ui'
import { ApplicationForm } from './components/ApplicationForm'
import { filterApplications, formatDate, sampleApplications, stages, type CreateValues, type PreviewApplication } from './data'

function Applications({ initialRecords = sampleApplications }: { initialRecords?: PreviewApplication[] }) {
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
  const close = () => navigate(`/applications${location.search}`, { replace: true })
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
      <Link id="add-application" className="button button-primary" to={`/applications/new${location.search}`}><Plus size={18} />Add application</Link>
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
        {records.length ? <Button onClick={() => setParams(view === 'list' ? { view: 'list' } : {}, { replace: true })}>Clear search & filter</Button> : <Link className="button button-primary" to={`/applications/new${location.search}`}>Add application</Link>}
      </div> : view === 'board' ? <Board records={filtered} search={location.search} /> : <ApplicationList records={filtered} search={location.search} />}
      <footer className="workspace-footer"><span>Small steps. New possibilities.</span><span>Preview additions reset on reload.</span></footer>
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
export function App({ initialRecords }: { initialRecords?: PreviewApplication[] }) {
  return <Shell><Routes><Route path="/applications/:id?" element={<Applications initialRecords={initialRecords} />} /><Route path="*" element={<Navigate to="/applications" replace />} /></Routes></Shell>
}
```

### Complete file: frontend/src/components/ApplicationForm.tsx

```tsx
import { useState, type FormEvent } from 'react'
import { Info, Plus } from 'lucide-react'
import { validateCreate, type CreateValues } from '../data'
import { Button } from './ui'

export function ApplicationForm({ onAdd, onClose }: { onAdd: (values: CreateValues) => void; onClose: () => void }) {
  const [values, setValues] = useState<CreateValues>({ company: '', role: '', applied_on: '' })
  const [errors, setErrors] = useState<Partial<Record<keyof CreateValues, string>>>({})
  function submit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault()
    const result = validateCreate(values)
    setErrors(result.errors)
    if (Object.keys(result.errors).length) {
      const first = Object.keys(result.errors)[0]
      event.currentTarget.querySelector<HTMLInputElement>(`[name="${first}"]`)?.focus()
      return
    }
    onAdd(result.clean)
  }
  return <form onSubmit={submit} noValidate className="application-form">
    <div className="info-note"><Info size={18} /><p>Added to this preview only. Your additions reset when you reload.</p></div>
    <div className="form-fields">
      {(['company', 'role', 'applied_on'] as const).map((field, i) => <div className="field" key={field}>
        <label htmlFor={field}>{['Company', 'Role', 'Applied date'][i]} <span aria-hidden="true">*</span></label>
        <input id={field} name={field} data-autofocus={field === 'company' ? '' : undefined} type={field === 'applied_on' ? 'date' : 'text'}
          placeholder={field === 'company' ? 'e.g. Cedar & Finch' : field === 'role' ? 'e.g. Product Designer' : undefined}
          required value={values[field]} aria-invalid={!!errors[field]} aria-describedby={errors[field] ? `${field}-error` : `${field}-hint`}
          onChange={event => setValues({ ...values, [field]: event.target.value })} />
        {errors[field] ? <p id={`${field}-error`} className="field-error" role="alert">{errors[field]}</p> :
          <p id={`${field}-hint`} className="field-hint">{field === 'applied_on' ? 'The date you applied. Future dates are also accepted.' : 'Up to 200 characters.'}</p>}
      </div>)}
    </div>
    <p className="form-stage-note">Starts in <strong>Applied</strong>, a provisional sample stage.</p>
    <div className="form-actions"><Button onClick={onClose} type="button">Cancel</Button><Button variant="primary" type="submit"><Plus size={17} />Add to preview</Button></div>
  </form>
}
```

### Complete file: frontend/src/components/ApplicationsView.tsx

```tsx
import { CalendarDays, ChevronRight, Inbox } from 'lucide-react'
import { Link } from 'react-router'
import { formatDate, initials, stages, type PreviewApplication } from '../data'
import { StageLabel } from './ui'

export function CompanyMark({ company }: { company: string }) {
  const color = company.charCodeAt(0) % 5
  return <span aria-hidden="true" className={`company-mark company-color-${color}`}>{initials(company)}</span>
}
function ApplicationCard({ record, search }: { record: PreviewApplication; search: string }) {
  const { application } = record
  return <Link to={`/applications/${application.id}${search}`} className="application-card" aria-label={`${application.role} at ${application.company}`}>
    <div className="card-top"><CompanyMark company={application.company} /><ChevronRight size={17} className="card-arrow" /></div>
    <h3>{application.role}</h3><p className="card-company">{application.company}</p>
    <div className="card-footer"><CalendarDays size={15} /><span>Applied {formatDate(application.applied_on)}</span></div>
  </Link>
}
export function Board({ records, search }: { records: PreviewApplication[]; search: string }) {
  return <div className="board-scroll" role="region" aria-label="Application board, scroll horizontally for more stages" tabIndex={0}>
    <div className="board">
      {stages.map(stage => {
        const cards = records.filter(record => record.sampleStage === stage)
        return <section key={stage} className="board-column" aria-label={`${stage}, ${cards.length} applications`}>
          <div className={`column-heading stage-${stage.toLowerCase()}`}><h2>{stage}</h2><span className="column-count">{cards.length}</span></div>
          <div className="column-cards">{cards.map(record => <ApplicationCard key={record.application.id} record={record} search={search} />)}
            {!cards.length && <div className="column-empty"><Inbox size={22} /><p>No applications here</p><span>Room for what’s next.</span></div>}
          </div>
        </section>
      })}
    </div>
  </div>
}
export function ApplicationList({ records, search }: { records: PreviewApplication[]; search: string }) {
  return <div className="application-list" role="region" aria-label="Application list">
    <div className="list-heading" aria-hidden="true"><span>Company</span><span>Role</span><span>Applied date</span><span>Sample stage</span><span /></div>
    <ul>{records.map(({ application, sampleStage }) => <li key={application.id}>
      <Link className="list-row" to={`/applications/${application.id}${search}`} aria-label={`${application.role} at ${application.company}`}>
        <span className="list-company"><CompanyMark company={application.company} /><span>{application.company}</span></span>
        <span className="list-role">{application.role}</span>
        <span className="list-date"><span className="mobile-only">Applied </span>{formatDate(application.applied_on)}</span>
        <span className="list-stage"><StageLabel stage={sampleStage} /></span>
        <ChevronRight size={17} className="list-arrow" />
      </Link>
    </li>)}</ul>
  </div>
}
```

### Complete file: frontend/src/components/Shell.tsx

```tsx
import { useState, type ReactNode } from 'react'
import { Link } from 'react-router'
import { ArrowUpRight, Layers3, Menu, ShieldCheck } from 'lucide-react'
import { Modal, PreviewNotice } from './ui'

function Sidebar({ onNavigate }: { onNavigate?: () => void }) {
  return <div className="sidebar-inner">
    <Link className="brand" to="/applications" onClick={onNavigate}><img src="/mark.svg" alt="" width="32" height="32" /><span>ApplySync<span className="brand-dot">.</span></span></Link>
    <div className="sidebar-body">
      <p className="eyebrow">YOUR WORKSPACE</p>
      <nav aria-label="Main navigation"><Link className="nav-link" aria-current="page" to="/applications" onClick={onNavigate}><Layers3 size={19} /> Applications <ArrowUpRight size={16} className="ml-auto" /></Link></nav>
      <div className="sidebar-note"><span className="tiny-tag">BUILD 2 · PREVIEW</span><h2>A little more clarity.</h2><p>One place to see your next opportunity taking shape.</p></div>
    </div>
    <div className="sidebar-footer"><ShieldCheck size={20} /><div><strong>Private by design</strong><p>Fictional data. All local.</p></div></div>
  </div>
}
export function Shell({ children }: { children: ReactNode }) {
  const [navigationOpen, setNavigationOpen] = useState(false)
  return <div className="app-shell">
    <a className="skip-link" href="#main-content">Skip to applications</a>
    <aside className="desktop-sidebar"><Sidebar /></aside>
    <div className="workspace">
      <header className="topbar">
        <button className="icon-button mobile-menu" aria-label="Open navigation" onClick={() => setNavigationOpen(true)}><Menu size={21} /></button>
        <div className="breadcrumb"><span>Workspace</span><span aria-hidden="true">/</span><strong>Applications</strong></div>
        <PreviewNotice />
      </header>
      <main id="main-content" tabIndex={-1}>{children}</main>
    </div>
    {navigationOpen && <Modal title="Your workspace" variant="navigation" onClose={() => setNavigationOpen(false)}><Sidebar onNavigate={() => setNavigationOpen(false)} /></Modal>}
  </div>
}
```

### Complete file: frontend/src/components/ui.tsx

```tsx
import { useEffect, useId, useRef, type ButtonHTMLAttributes, type ReactNode } from 'react'
import { X } from 'lucide-react'
import type { Stage } from '../data'

export function Button({ variant = 'secondary', className = '', ...props }: ButtonHTMLAttributes<HTMLButtonElement> & { variant?: 'primary' | 'secondary' | 'quiet' }) {
  return <button {...props} className={`button button-${variant} ${className}`} />
}
export function StageLabel({ stage }: { stage: Stage }) {
  return <span className={`stage-label stage-${stage.toLowerCase()}`}><span className="stage-dot" />{stage}</span>
}
export function PreviewNotice({ children = 'Design preview · Sample data' }: { children?: ReactNode }) {
  return <span className="preview-notice"><span className="preview-dot" />{children}</span>
}

export function Modal({ title, subtitle, children, onClose, variant = 'panel' }: {
  title: string; subtitle?: string; children: ReactNode; onClose: () => void; variant?: 'panel' | 'form' | 'navigation'
}) {
  const dialog = useRef<HTMLDialogElement>(null)
  const titleId = useId()
  useEffect(() => {
    const previous = document.activeElement as HTMLElement | null
    const element = dialog.current!
    element.showModal()
    element.querySelector<HTMLElement>('[data-autofocus]')?.focus()
    const overflow = document.body.style.overflow
    document.body.style.overflow = 'hidden'
    return () => {
      element.close()
      document.body.style.overflow = overflow
      const target = previous?.isConnected && previous !== document.body ? previous : document.getElementById('add-application')
      target?.focus({ preventScroll: true })
    }
  }, [])
  return <dialog ref={dialog} className={`modal modal-${variant}`} aria-labelledby={titleId}
    onKeyDown={event => {
      if (event.key !== 'Tab') return
      const targets = Array.from(event.currentTarget.querySelectorAll<HTMLElement>('button:not([disabled]), a[href], input:not([disabled]), select:not([disabled]), [tabindex="0"]'))
        .filter(element => element.getClientRects().length > 0)
      const first = targets[0]
      const last = targets.at(-1)
      if (event.shiftKey && document.activeElement === first) { event.preventDefault(); last?.focus() }
      else if (!event.shiftKey && document.activeElement === last) { event.preventDefault(); first?.focus() }
    }}
    onCancel={event => { event.preventDefault(); onClose() }}>
    <div className="modal-heading">
      <div><p className="eyebrow">APPLYSYNC PREVIEW</p><h2 id={titleId}>{title}</h2>{subtitle && <p className="text-muted mt-2">{subtitle}</p>}</div>
      <button className="icon-button shrink-0" aria-label="Close panel" onClick={onClose}><X size={20} /></button>
    </div>
    {children}
  </dialog>
}
```

### Complete file: frontend/src/data.test.ts

```typescript
import { describe, expect, it } from 'vitest'
import { filterApplications, formatDate, sampleApplications, validateCreate } from './data'

describe('preview data boundaries', () => {
  it('combines company/role search and stage filtering', () => {
    expect(filterApplications(sampleApplications, '  PRODUCT ', 'Interview')).toHaveLength(1)
    expect(filterApplications(sampleApplications, 'cedar', 'Interview')).toHaveLength(0)
    expect(filterApplications(sampleApplications, 'cedar', 'All stages')).toHaveLength(1)
  })
  it('formats calendar dates without timezone shifts', () => {
    expect(formatDate('2026-09-01')).toBe('1 Sept 2026')
  })
  it('trims and allows future dates and duplicate values', () => {
    const values = { company: ' Cedar & Finch ', role: ' Engineer ', applied_on: '2100-01-01' }
    const result = validateCreate(values)
    expect(result.errors).toEqual({})
    expect(result.clean.company).toBe('Cedar & Finch')
    expect(result.clean.role).toBe('Engineer')
    expect(validateCreate(values)).toEqual(result)
  })
  it('rejects blank, oversized and impossible date values', () => {
    expect(validateCreate({ company: '   ', role: 'r'.repeat(201), applied_on: '2026-02-30' }).errors)
      .toEqual({ company: 'Enter a company.', role: 'Use 200 characters or fewer.', applied_on: 'Enter a valid date.' })
    for (const applied_on of ['', '2026-2-1', '0000-01-01', '2025-02-29']) {
      expect(validateCreate({ company: 'A', role: 'B', applied_on }).errors.applied_on).toBeTruthy()
    }
    expect(validateCreate({ company: 'x'.repeat(200), role: 'r'.repeat(200), applied_on: '2024-02-29' }).errors).toEqual({})
  })
})
```

### Complete file: frontend/src/data.ts

```typescript
// The eventual API shape has no stage. Preview-only values stay in a separate wrapper.
export interface Application {
  id: string
  company: string
  role: string
  applied_on: string
  created_at: string
}
export const stages = ['Applied', 'Assessment', 'Interview', 'Offer', 'Rejected'] as const
export type Stage = typeof stages[number]
export interface PreviewApplication { application: Application; sampleStage: Stage }
export type CreateValues = Pick<Application, 'company' | 'role' | 'applied_on'>

const samples: [string, string, string, Stage][] = [
  ['Cedar & Finch', 'Product Designer', '2026-09-21', 'Applied'],
  ['Orbitwell', 'Frontend Engineer', '2026-09-20', 'Applied'],
  ['Northstar Sustainable Infrastructure Collective', 'Senior User Experience Researcher, Digital Products', '2026-09-18', 'Applied'],
  ['Morrow Studio', 'Design Systems Designer', '2026-09-17', 'Applied'],
  ['Fernpath', 'UX Researcher', '2026-09-16', 'Assessment'],
  ['Lumenfield', 'Software Engineer', '2026-09-14', 'Assessment'],
  ['Kindred Works', 'Product Designer', '2026-09-12', 'Interview'],
  ['Aster & Co.', 'Interaction Designer', '2026-09-10', 'Interview'],
  ['Pebblewave', 'Frontend Developer', '2026-09-04', 'Rejected'],
]
export const sampleApplications: PreviewApplication[] = samples.map(([company, role, applied_on, sampleStage], i) => ({
  application: { id: `00000000-0000-4000-8000-${String(i + 1).padStart(12, '0')}`, company, role, applied_on, created_at: `${applied_on}T12:00:00Z` },
  sampleStage,
}))

export function filterApplications(records: PreviewApplication[], search: string, stage: string) {
  const query = search.trim().toLocaleLowerCase()
  return records.filter(({ application, sampleStage }) =>
    (stage === 'All stages' || sampleStage === stage) &&
    `${application.company}\n${application.role}`.toLocaleLowerCase().includes(query))
}

export function formatDate(value: string) {
  // Date-only values must retain the calendar day in every timezone.
  return new Intl.DateTimeFormat('en-GB', { day: 'numeric', month: 'short', year: 'numeric', timeZone: 'UTC' })
    .format(new Date(`${value}T12:00:00Z`))
}
export function initials(company: string) {
  return company.split(/\s+/).filter(word => /^[a-z]/i.test(word)).slice(0, 2).map(word => word[0]).join('').toUpperCase()
}
export function validateCreate(values: CreateValues) {
  const clean = { ...values, company: values.company.trim(), role: values.role.trim() }
  const errors: Partial<Record<keyof CreateValues, string>> = {}
  for (const key of ['company', 'role'] as const) {
    if (!clean[key]) errors[key] = `Enter a ${key}.`
    else if ([...clean[key]].length > 200) errors[key] = 'Use 200 characters or fewer.'
  }
  const date = new Date(`${values.applied_on}T12:00:00Z`)
  if (!/^\d{4}-\d{2}-\d{2}$/.test(values.applied_on) || values.applied_on.startsWith('0000') ||
      Number.isNaN(date.getTime()) || date.toISOString().slice(0, 10) !== values.applied_on) {
    errors.applied_on = 'Enter a valid date.'
  }
  return { clean, errors }
}
```

### Complete file: frontend/src/main.tsx

```tsx
import React from 'react'
import ReactDOM from 'react-dom/client'
import { BrowserRouter } from 'react-router'
import { App } from './App'
import './styles.css'

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode><BrowserRouter><App /></BrowserRouter></React.StrictMode>,
)
```

### Complete file: frontend/src/styles.css

```css
@import "tailwindcss";

@theme {
  --color-primary: #5145e5;
  --color-muted: #667085;
  --color-ink: #20242c;
  --color-line: #e2e5ea;
  --color-workspace: #f5f7f9;
  --font-sans: "Segoe UI", "Helvetica Neue", Arial, sans-serif;
}
:root { font-family: var(--font-sans); color: var(--color-ink); background: var(--color-workspace); font-synthesis: none; text-rendering: optimizeLegibility; -webkit-font-smoothing: antialiased; }
* { box-sizing: border-box; }
body { margin: 0; min-width: 320px; font-size: 14px; }
button, input, select { font: inherit; }
button, a, input, select { -webkit-tap-highlight-color: transparent; }
button, select { cursor: pointer; }
a { text-decoration: none; color: inherit; }
button, a { touch-action: manipulation; }
button, a, input, select { transition: background-color 160ms, border-color 160ms, box-shadow 160ms; }
:focus-visible { outline: 3px solid #5145e5; outline-offset: 3px; }
button:disabled { opacity: .6; cursor: default; }
h1, h2, h3, p { margin: 0; }
.app-shell { display: flex; min-height: 100dvh; }
.desktop-sidebar { width: 232px; flex: 0 0 232px; background: white; border-right: 1px solid var(--color-line); }
.sidebar-inner { display: flex; flex-direction: column; min-height: 100dvh; position: sticky; top: 0; height: 100dvh; }
.brand { height: 64px; display: flex; align-items: center; gap: 10px; padding: 0 24px; font-size: 22px; font-weight: 750; letter-spacing: -.8px; border-bottom: 1px solid var(--color-line); }
.brand-dot { color: var(--color-primary); }
.sidebar-body { padding: 30px 16px; }
.eyebrow { color: var(--color-muted); font-size: 11px; letter-spacing: 1.1px; font-weight: 650; }
.sidebar-body > .eyebrow { padding: 0 12px; margin-bottom: 12px; }
.nav-link { display: flex; align-items: center; gap: 11px; min-height: 46px; background: #eeecfc; color: #4438c6; border: 1px solid #e1dcfa; border-radius: 7px; padding: 0 12px; font-weight: 600; }
.nav-link:hover { background: #e5e1fc; }
.sidebar-note { margin: 34px 12px 0; padding-top: 28px; border-top: 1px solid var(--color-line); }
.tiny-tag { font-size: 10px; font-weight: 650; letter-spacing: .5px; color: #625b94; }
.sidebar-note h2 { font-size: 14px; font-weight: 650; margin: 14px 0 7px; }
.sidebar-note p { color: var(--color-muted); line-height: 1.7; font-size: 13px; }
.sidebar-footer { margin-top: auto; display: flex; gap: 10px; padding: 22px 24px; border-top: 1px solid var(--color-line); color: #687080; }
.sidebar-footer strong { font-size: 12px; font-weight: 600; color: #444c5b; }
.sidebar-footer p { font-size: 11px; margin-top: 4px; }
.workspace { min-width: 0; flex: 1; }
.topbar { min-height: 64px; background: white; border-bottom: 1px solid var(--color-line); display: flex; align-items: center; justify-content: space-between; gap: 14px; padding: 0 28px; }
.breadcrumb { display: flex; gap: 14px; align-items: center; font-size: 13px; color: var(--color-muted); }
.breadcrumb strong { font-weight: 500; color: #424a58; }
.preview-notice { display: inline-flex; align-items: center; gap: 7px; color: #625a88; font-size: 12px; font-weight: 500; }
.preview-dot { width: 6px; height: 6px; border-radius: 50%; background: #8174c9; flex-shrink: 0; }
main { padding: 30px 28px 24px; min-width: 0; }
.page-heading { display: flex; justify-content: space-between; align-items: center; gap: 24px; margin-bottom: 28px; }
.page-heading h1 { font-size: 29px; line-height: 1.25; font-weight: 700; letter-spacing: -.8px; margin-top: 7px; }
.page-description { margin-top: 9px; font-size: 14px; color: var(--color-muted); line-height: 1.6; }
.button { display: inline-flex; align-items: center; justify-content: center; gap: 8px; min-height: 42px; border-radius: 7px; border: 1px solid transparent; padding: 9px 15px; font-weight: 550; font-size: 14px; line-height: 1.5; flex-shrink: 0; }
.button-primary { color: white; background: var(--color-primary); border-color: var(--color-primary); box-shadow: 0 2px 3px #28204a0b; }
.button-primary:hover { background: #4338ca; border-color: #4338ca; }
.button-secondary { background: white; border-color: #d9dde4; color: #3a4353; }
.button-secondary:hover { background: #f8f9fc; border-color: #aaa7d8; }
.button-quiet { color: #493eb8; padding: 5px 9px; min-height: 36px; }
.button-quiet:hover { background: #ece9fc; }
.toolbar { display: flex; justify-content: space-between; align-items: center; gap: 18px; padding-bottom: 18px; border-bottom: 1px solid var(--color-line); }
.view-switch { display: flex; background: #eaedf1; padding: 4px; border: 1px solid #e3e6eb; border-radius: 8px; gap: 3px; flex-shrink: 0; }
.view-switch button { display: flex; align-items: center; gap: 7px; border-radius: 5px; padding: 7px 13px; min-height: 36px; color: #667085; font-weight: 550; border: 1px solid transparent; }
.view-switch button[aria-pressed="true"] { background: white; color: #4b3fcc; box-shadow: 0 1px 3px #20242c0b; border-color: #e1e3e9; }
.view-switch button:hover { color: #4438c6; }
.filter-controls { display: flex; gap: 10px; align-items: center; min-width: 0; }
.search-field, .stage-filter { display: flex; align-items: center; position: relative; color: #778091; }
.search-field > svg { position: absolute; left: 12px; pointer-events: none; }
.search-field input { background: white; border: 1px solid #dce0e7; border-radius: 7px; width: 288px; min-height: 42px; padding: 9px 12px 9px 38px; color: var(--color-ink); }
input::placeholder { color: #667085; }
.stage-filter > svg { position: absolute; left: 12px; pointer-events: none; }
.stage-filter select { min-height: 42px; border: 1px solid #dce0e7; border-radius: 7px; background: white; color: #424b5b; padding: 9px 28px 9px 36px; width: 166px; }
.results-meta { display: flex; justify-content: space-between; gap: 16px; align-items: center; padding: 17px 0 15px; font-size: 12px; color: var(--color-muted); }
.results-meta strong { color: #364052; font-weight: 600; }
.results-meta > span { color: #667085; font-size: 11px; }
.board-scroll { overflow-x: auto; padding: 1px 1px 18px; scrollbar-color: #c9c6da transparent; scrollbar-width: thin; }
.board { display: grid; grid-template-columns: repeat(5, minmax(250px, 1fr)); gap: 14px; }
.board-column { min-width: 0; }
.column-heading { display: flex; align-items: center; justify-content: space-between; gap: 8px; padding: 7px 11px; border-radius: 5px; min-height: 35px; margin-bottom: 13px; }
.column-heading h2 { font-size: 12px; text-transform: uppercase; letter-spacing: .5px; font-weight: 650; }
.column-count { min-width: 22px; height: 20px; line-height: 20px; border-radius: 4px; text-align: center; font-size: 11px; font-weight: 700; background: #ffffff90; }
.stage-applied { background: #f8eed4; color: #776023; }
.stage-assessment { background: #e1eafb; color: #395c92; }
.stage-interview { background: #eee2fa; color: #7444a4; }
.stage-offer { background: #dcefe5; color: #34664a; }
.stage-rejected { background: #f4e1e3; color: #924650; }
.column-cards { display: flex; flex-direction: column; gap: 12px; }
.application-card { display: block; background: white; border: 1px solid #dfe3e9; border-radius: 9px; padding: 15px 15px 0; box-shadow: 0 1px 2px #20242c03; overflow-wrap: anywhere; }
.application-card:hover { border-color: #a9a0ef; box-shadow: 0 3px 9px #5145e50b; }
.card-top { display: flex; align-items: center; justify-content: space-between; margin-bottom: 13px; }
.company-mark { display: inline-flex; align-items: center; justify-content: center; width: 36px; height: 36px; border-radius: 8px; font-size: 12px; font-weight: 700; letter-spacing: .3px; flex-shrink: 0; }
.company-color-0 { background: #ede8f9; color: #69509c; }
.company-color-1 { background: #e8edf6; color: #496482; }
.company-color-2 { background: #e4efe9; color: #466854; }
.company-color-3 { background: #f4e9df; color: #916b48; }
.company-color-4 { background: #f4e5eb; color: #945a73; }
.card-arrow { color: #9299a5; }
.application-card h3 { font-size: 15px; font-weight: 650; line-height: 1.45; }
.card-company { font-size: 14px; line-height: 1.6; color: var(--color-muted); margin-top: 4px; }
.card-footer { margin-top: 15px; padding: 12px 0; border-top: 1px solid #eef0f3; display: flex; align-items: center; gap: 7px; font-size: 12px; color: #626d7d; }
.column-empty { border: 1px dashed #d9dee6; border-radius: 8px; display: flex; align-items: center; flex-direction: column; padding: 30px 10px; color: #7d8794; background: #f8f9fb; }
.column-empty p { margin-top: 13px; color: #656f80; font-size: 13px; }
.column-empty span { font-size: 11px; margin-top: 5px; color: #667085; }
.workspace-footer { display: flex; justify-content: space-between; gap: 18px; font-size: 11px; color: #667085; border-top: 1px solid var(--color-line); margin-top: 20px; padding-top: 17px; }
.application-list { border: 1px solid var(--color-line); border-radius: 9px; background: white; overflow: hidden; }
.list-heading, .list-row { display: grid; grid-template-columns: 1.1fr 1.3fr 130px 120px 20px; gap: 22px; align-items: center; padding: 17px 20px; }
.list-heading { color: #677184; font-size: 12px; font-weight: 600; background: #fafbfc; }
.list-row { min-height: 82px; border-top: 1px solid #e9ecf1; }
.list-row:hover { background: #fcfbff; }
.list-company { display: flex; align-items: center; gap: 12px; min-width: 0; font-weight: 550; overflow-wrap: anywhere; }
.list-role { font-weight: 600; line-height: 1.5; overflow-wrap: anywhere; min-width: 0; }
.list-date { font-size: 13px; color: var(--color-muted); }
.list-arrow { color: #8d96a5; }
.stage-label { display: inline-flex; align-items: center; gap: 6px; font-size: 11px; padding: 4px 8px; border-radius: 5px; white-space: nowrap; font-weight: 550; }
.stage-dot { height: 5px; width: 5px; border-radius: 50%; background: currentColor; }
.empty-state { border: 1px dashed #d6dbe4; border-radius: 10px; background: #ffffff88; min-height: 320px; display: flex; align-items: center; justify-content: center; flex-direction: column; text-align: center; padding: 24px; color: #7a759a; }
.empty-state h2 { font-size: 18px; color: #343848; font-weight: 600; margin: 16px 0 8px; }
.empty-state p { color: var(--color-muted); margin-bottom: 20px; line-height: 1.6; }
.success-note { margin: 0 0 16px; display: flex; justify-content: space-between; align-items: center; gap: 12px; color: #3e614f; background: #edf6ef; border: 1px solid #d9e8dc; padding: 10px 14px; border-radius: 7px; font-size: 13px; }
.icon-button { display: inline-flex; justify-content: center; align-items: center; width: 40px; height: 40px; border: 1px solid #e4e7ed; border-radius: 7px; color: #606a7a; background: white; }
.icon-button:hover { color: #4c40cf; background: #f5f3ff; }
.modal { color: var(--color-ink); border: 1px solid #e1e4eb; background: white; padding: 0; box-shadow: 0 12px 50px #21233120; animation: panel-in 180ms ease-out; }
.modal::backdrop { background: #22293842; }
.modal-panel { position: fixed; inset: 0 0 0 auto; margin: 0; height: 100dvh; max-height: 100dvh; width: 470px; max-width: 100%; border-radius: 0; }
.modal-form { margin: auto; width: 520px; max-width: calc(100% - 32px); max-height: calc(100dvh - 40px); border-radius: 12px; }
.modal-heading { display: flex; justify-content: space-between; align-items: flex-start; gap: 16px; padding: 28px; background: #f9fafc; border-bottom: 1px solid var(--color-line); }
.modal-heading h2 { font-weight: 700; font-size: 23px; line-height: 1.35; letter-spacing: -.4px; margin-top: 10px; overflow-wrap: anywhere; }
.detail-body { padding: 28px; }
.detail-identity { display: flex; align-items: center; gap: 13px; padding-bottom: 28px; margin-bottom: 25px; border-bottom: 1px solid var(--color-line); }
.detail-identity .company-mark { width: 46px; height: 46px; }
.detail-identity strong { display: block; font-size: 15px; line-height: 1.5; margin-top: 5px; overflow-wrap: anywhere; }
.detail-body h3 { font-size: 16px; font-weight: 650; margin-bottom: 18px; }
.detail-facts { border: 1px solid var(--color-line); border-radius: 8px; background: #f9fafc; padding: 0 18px; }
.detail-facts > div { padding: 17px 0; }
.detail-facts > div + div { border-top: 1px solid var(--color-line); }
.detail-facts dt { display: flex; gap: 7px; align-items: center; color: var(--color-muted); font-size: 12px; }
.detail-facts dd { margin-top: 8px; font-weight: 600; }
.detail-preview { margin: 28px 0; }
.detail-preview p { margin-top: 11px; color: var(--color-muted); font-size: 13px; line-height: 1.8; }
.application-form { padding: 24px 28px; }
.info-note { display: flex; align-items: flex-start; gap: 9px; color: #675b89; background: #f5f2fc; border-radius: 7px; padding: 12px; font-size: 12px; line-height: 1.7; }
.info-note svg { flex-shrink: 0; margin-top: 1px; }
.form-fields { display: flex; flex-direction: column; gap: 20px; margin: 24px 0 18px; }
.field label { display: block; margin-bottom: 8px; font-weight: 600; }
.field label > span { color: #776c9a; }
.field input { width: 100%; min-height: 44px; border: 1px solid #d5dae3; border-radius: 6px; padding: 9px 12px; background: white; }
.field input[aria-invalid="true"] { border-color: #c24959; }
.field-error { color: #ad283e; margin-top: 7px; font-size: 12px; }
.field-hint { color: var(--color-muted); margin-top: 7px; font-size: 11px; }
.form-stage-note { color: var(--color-muted); font-size: 12px; line-height: 1.7; }
.form-stage-note strong { color: #635b7c; }
.form-actions { display: flex; justify-content: flex-end; gap: 10px; padding-top: 24px; margin-top: 22px; border-top: 1px solid var(--color-line); }
.mobile-menu, .mobile-only { display: none; }
.skip-link { position: fixed; left: 12px; top: -100px; z-index: 10; background: white; padding: 12px; }
.skip-link:focus { top: 12px; }
.modal-navigation { position: fixed; inset: 0 auto 0 0; margin: 0; width: 300px; max-width: 90%; height: 100dvh; max-height: 100dvh; }
.modal-navigation .modal-heading { padding: 20px; }
.modal-navigation .sidebar-inner { min-height: auto; height: calc(100dvh - 114px); }
@keyframes panel-in { from { opacity: 0; transform: translateX(8px); } to { opacity: 1; transform: translateX(0); } }
@media (max-width: 1100px) {
  .search-field input { width: 230px; }
  .list-heading, .list-row { gap: 12px; grid-template-columns: 1fr 1.2fr 100px 105px 16px; padding: 16px; }
  .page-heading { align-items: flex-start; }
  .page-heading > .button { margin-top: 20px; }
}
@media (max-width: 850px) {
  .desktop-sidebar { display: none; }
  .mobile-menu { display: inline-flex; }
  .topbar { padding: 10px 20px; }
  .breadcrumb { margin-right: auto; }
  main { padding: 24px 20px; }
}
@media (min-width: 621px) and (max-width: 1000px) {
  .toolbar { flex-wrap: wrap; }
  .filter-controls { width: 100%; }
  .search-field { flex: 1; min-width: 0; }
  .search-field input { width: 100%; }
  .stage-filter { flex-shrink: 0; }
}
@media (max-width: 620px) {
  .breadcrumb { display: none; }
  .topbar { padding: 10px 16px; }
  main { padding: 24px 16px; }
  .page-heading { flex-direction: column; gap: 17px; margin-bottom: 23px; }
  .page-heading h1 { font-size: 27px; }
  .page-heading > .button { margin-top: 0; }
  .toolbar { flex-wrap: wrap; gap: 14px; }
  .filter-controls { width: 100%; flex-wrap: wrap; }
  .search-field { width: 100%; }
  .search-field input { width: 100%; font-size: 16px; }
  .stage-filter { width: 100%; }
  .stage-filter select { width: 100%; }
  .results-meta { align-items: flex-start; }
  .results-meta > span { max-width: 135px; text-align: right; }
  .board { grid-template-columns: repeat(5, 260px); }
  .workspace-footer { flex-direction: column; gap: 8px; }
  .list-heading { display: none; }
  .list-row { grid-template-columns: minmax(0,1fr) auto; gap: 10px 8px; padding: 18px; }
  .list-company { grid-column: 1 / -1; font-size: 13px; font-weight: 400; color: var(--color-muted); padding-right: 20px; }
  .list-role { grid-column: 1 / -1; font-size: 15px; }
  .list-date { grid-column: 1; font-size: 11px; }
  .list-stage { grid-column: 2; }
  .list-arrow { display: none; }
  .mobile-only { display: inline; }
  .modal-panel, .modal-form { inset: 0; margin: 0; width: 100%; max-width: 100%; height: 100dvh; max-height: 100dvh; border-radius: 0; }
  .modal-heading { padding: 24px 20px; }
  .detail-body, .application-form { padding: 24px 20px; }
  .field input { font-size: 16px; }
  .form-actions .button { flex: 1; }
  .success-note { align-items: flex-start; }
}
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after { animation: none !important; transition: none !important; scroll-behavior: auto !important; }
}
```

### Complete file: frontend/src/test-setup.ts

```typescript
import '@testing-library/jest-dom/vitest'
import { afterEach } from 'vitest'
import { cleanup } from '@testing-library/react'

afterEach(cleanup)
// jsdom has no native dialog implementation; actual focus trapping/inertness is
// verified separately in Playwright with Chromium's real dialog implementation.
HTMLDialogElement.prototype.showModal = function () { this.setAttribute('open', '') }
HTMLDialogElement.prototype.close = function () { this.removeAttribute('open') }
```

### Complete file: frontend/tsconfig.json

```json
{
  "compilerOptions": {
    "target": "ES2022", "lib": ["ES2022", "DOM", "DOM.Iterable"],
    "module": "ESNext", "moduleResolution": "Bundler", "jsx": "react-jsx",
    "strict": true, "skipLibCheck": true, "esModuleInterop": true,
    "resolveJsonModule": true, "isolatedModules": true, "noEmit": true,
    "types": ["vite/client", "vitest/globals", "@testing-library/jest-dom"]
  },
  "include": ["src", "vite.config.ts", "playwright.config.ts", "e2e"]
}
```

### Complete file: frontend/vite.config.ts

```typescript
import { defineConfig } from 'vitest/config'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'

export default defineConfig({
  plugins: [react(), tailwindcss()],
  server: { port: 5173, strictPort: true },
  test: { environment: 'jsdom', setupFiles: './src/test-setup.ts', include: ['src/**/*.test.{ts,tsx}'] },
})
```
