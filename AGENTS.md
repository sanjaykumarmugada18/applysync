# ApplySync repository instructions

## Authority and reference

ApplySync is Sanjay's privacy-first Gmail job application tracker. The active
specification is **ApplySync Master Reference v2.0** (17 September 2026), stored
in this repository at `docs/ApplySync_Master_Reference_v2.0.pdf`.

Read the relevant specification pages before implementation: pages 3 and 6-7
for working agreements, the active stage on pages 15-20, and the relevant
architecture requirements on pages 8-14. This file is a working guide, not a
replacement for the full specification. If the PDF is missing or unreadable,
report that explicitly; do not invent its requirements. Read-only repository
inspection can continue while the reference is made available.

The original Master Reference and Errata v1.1 are historical. v2.0 incorporates
their architecture corrections and replaces the 25-phase teaching sequence.
Follow later explicitly agreed corrections and document their rationale,
affected behaviour and verification. Discuss concrete correctness, privacy or
security conflicts before departing from the approved architecture.

## Working and learning agreement

Codex may write most code, configuration, migrations and tests. Sanjay need not
type every line, recreate generated files or memorize syntax.

Use this cycle: understand the outcome -> specify a bounded task -> implement
-> inspect actual code -> verify behaviour -> explain -> commit a working checkpoint.

- Before substantial changes, briefly state the approach, scope, file
  responsibilities, acceptance criteria and important unfamiliar concepts.
- Continue routine work within the agreed task without repeated confirmation.
  Do not generate an entire stage or repository in one unchecked pass.
- Explain each changed file's responsibility and trace one success and one
  failure path using actual file/function names. Locate validation, business
  logic, persistence, external calls and responses where applicable.
- Inspect critical conditions and test assertions closely. Avoid narrating
  familiar imports or requiring a manual first attempt for every feature.
- At meaningful checkpoints, involve Sanjay in a focused behaviour change or
  concrete diagnosis, with documentation and hints allowed. Do not claim he
  completed a learning checkpoint without his participation.
- Stop when the bounded result is reviewable. Avoid unrelated refactors,
  speculative abstractions, empty future modules and unnecessary dependencies.

## Stage boundaries and approved stack

1. **Build 1 - Backend & Persistence:** PostgreSQL, SQLAlchemy, Alembic,
   Pydantic, manual create/list/detail APIs, Pytest and reproducible setup.
2. **Build 2 - Frontend & Integration:** Vite + React + TypeScript, React
   Router, Tailwind, TanStack Query, React Hook Form/Zod where needed.
   Explain a plain-fetch request; no duplicate full implementation is needed.
3. **Build 3 - Authentication & Ownership:** registration/login/logout/me,
   application JWT cookie, ownership enforcement and security checks.
4. **Build 4 - Gmail & Reliable Synchronization:** GmailConnector, OAuth,
   setup verification, bounded backfill, incremental sync and recovery.
   Manually triggered sync; no body classification or live LLM calls yet.
5. **Build 5 - Classification & Human Review:** privacy processing, rules,
   Groq structured proposals, events/reducer, matching, corrections, merges
   and event-backed stage movement using @dnd-kit.
6. **Build 6 - Automation & Release:** Redis, worker selection, scheduled
   polling, Docker/Compose, GitHub Actions, HTTPS deployment and operations.

Use FastAPI/Python and PostgreSQL; do not substitute Next.js or another stack.
Frontend checks use Vitest/React Testing Library and Playwright as relevant.
Introduce infrastructure and entities only when the active stage needs them.
Worker library, deployment provider and other open choices are not preselected.
Six stages are not a six-day estimate.

## Current starting point: verify before changing

Reported baseline, not a fresh repository audit:

- Repository: https://github.com/sanjaykumarmugada18/applysync.git
- Sanjay uses Windows, VS Code, PowerShell and a local `.venv`.
- Previously used folder: `C:\Users\sanja\Desktop\ApplySync`.
- `main.py` and `.gitignore`; FastAPI and Uvicorn installed.
- `GET /health` returns `{"status":"healthy"}`; unknown routes return 404.
- Restart was verified; reported local commit is `37019df`,
  `Build first FastAPI health endpoint`. Push state is unverified.

Continue with Build 1; do not restart Phase 1 or reuse the old Phase 2 prompt.
Later verified handoffs supersede this baseline. Inspect the actual root,
branch, working tree (including staged/untracked files), commits, remote state,
dependencies and PostgreSQL availability before implementation. Never treat a
stale remote-tracking ref as proof of current push state; report access limits.
Preserve existing changes and unrelated databases. Distinguish the agent's
execution environment from Sanjay's Windows environment.

Build 1 delivers `POST /applications`, `GET /applications` and
`GET /applications/{id}` while preserving health behaviour. Choose and document
initial fields and response/error semantics from the current requirement;
v2.0 does not fix every field or enum. Inspect Alembic migrations before applying
them; do not bypass migrations with `create_all()`. Verify the real schema,
repeat `upgrade head`, valid/invalid requests, missing IDs and restart persistence.
Do not introduce frontend, authentication, Gmail, events, LLMs or workers here.

## Engineering invariants when their stages are implemented

- Keep secrets out of Git, responses and logs. Use placeholder configuration
  examples. Never request or include `.env` contents, unredacted connection
  URLs, credentials, tokens or real email bodies in review packages.
- Use established password hashing. Keep the application JWT in an HttpOnly
  cookie; use Secure in HTTPS production and deliberate SameSite/CSRF/CORS
  settings for the actual topology. Gmail authorization is separate from login.
- Derive ownership from the authenticated user and enforce it on all relevant
  queries, mutations, connection operations and jobs. Test two-user isolation.
- Gmail uses `gmail.readonly`. JobTracker label checks are application-level
  minimization, not an OAuth restriction. Verify required filter-group coverage
  and block sync when setup is invalid. Verify current official API/scope
  compatibility; do not silently broaden scopes to fix an integration conflict.
- Centralize token decryption, Gmail clients, API calls and label verification
  inside GmailConnector with narrow operations and architecture-boundary tests.
  This package is not a runtime sandbox. Keep access tokens memory-only,
  encrypt refresh tokens, preserve valid tokens when reauthorization omits one,
  and validate single-use, expiring OAuth state bound to user/session.
- Retrieve eligible individual messages metadata-first; never fetch full
  threads, attachments or remote tracking content. Raw bodies/HTML must not
  persist in databases, job payloads or logs. Logs must also exclude subjects,
  prompts, raw model responses and tokens.
- Screen sensitive categories before classification. Use deterministic rules
  first, then minimal redacted excerpts for safe ambiguity. Treat email as
  untrusted data. Validate model output; confidence is not proof of identity.
  The internal classifier has no Gmail, database, browser or sending tools.
- Serialize sync per connection; enforce database uniqueness on
  `(gmail_connection_id, message_fingerprint)` using HMAC fingerprints.
  Advance checkpoints only after durable ingestion. Separate classification
  retry state from ingestion; retries must not duplicate records/events/links.
  Expired history triggers bounded label-scoped reconciliation.
- In Build 5, derive stage through one central event reducer. Manual changes
  produce events; corrections supersede history and merges are transactional.
  Preserve one active thread binding per connection/thread with a partial
  unique index while retaining inactive history and binding sources.
- Apply the complete matching policy on pages 13-14, including scoped exact
  identifiers, all multi-signal conditions, contradictions and review fallback.
  Company/role/domain alone is insufficient; classification and identity
  confidence differ. Do not silently create applications from unmatched
  later-stage messages. Preserve reapplications and concurrent roles.

## Verification, handoff and completion

Add relevant tests with behaviour. Isolate tests from development data and use
synthetic fixtures and mocked external services where appropriate. Record
compatible dependency versions and reproducible setup commands. Resolve open
choices when needed and document assumptions, limitations and decisions.

After a meaningful change, provide a review package containing:

- Stage/task, branch, base/current commit, uncommitted state and push state.
- Changed files and responsibilities; relevant diff, complete new files and
  necessary context. Include staged and untracked work, not just `git diff`.
- One success and one failure execution path through actual code.
- Exact checks and observed results; failed, blocked, mocked or unrun checks.
- Dependencies, configuration/schema decisions, assumptions and limitations.
- Two or three important concepts and the next focused learning checkpoint.

Do not assume ChatGPT can see VS Code or Codex can see ChatGPT Project files.
A summary tracks progress; correctness review requires code and evidence.
Distinguish reported results, inspected code and independently executed checks.

A stage is complete only when intended behaviour and relevant checks pass,
critical logic/tests are reviewed, limitations and setup are documented, Sanjay
can explain an important path and has participated in a focused change or
diagnosis, and a coherent commit preserves the working result. Never include
unrelated user changes in a checkpoint. Report local commit and push separately;
do not infer permission to push from permission to commit. Return a concise
handoff for `00 - Planning & Progress` with remaining gaps and the next task.
