# Capability Compiler V2 — Phase 11 Plan

## Objective

Validate Revision 4 through one real, from-scratch full-stack Web application, beginning with a vague product idea and ending with a runnable local package, independent browser/QA/performance evidence, delivery preflight, deployment/observability/rollback plans, retrospective, complete patch, and recomputable manifest. No remote deployment or release occurs.

## Candidate Concept — Human Checkpoint Required

Recommended concept: **BenchShare**, a small community-workshop application where members reserve shared equipment and coordinators approve requests. It naturally exercises user roles, authorization, concurrent bookings, API/data integrity, audit evidence, responsive task UI, accessibility, browser behavior, security, tests, performance, preflight, operational plans, and rollback.

The exact product concept is not fixed until the user approves it. Product scope is a real decision and cannot be inferred from the requirement to build “some full-stack app.”

## Frozen Inputs

- Phase 9 tree: `7540c53426a5dff605c3f751fdaf105f52059ffbafce213d77c9c3db94214152`
- Phase 10 tree: `7fd6640a563789257da77e1015be3f37033a3baf40ecaf9a4b9fa1fde7828d56`
- Accepted candidate revision: `0.1.4-v2-candidate`, status `evaluating`, released=false.
- Revision 4 targeted plan: 60 runs, hash `b96a2b6172b9ee2760e3b9a40582a48e2516c70a5c9c42a0e4099ff6282ecd53`.
- Phase 10 review: 157 Skills and 314 outputs reviewed; open findings=0; final user release approval=false.
- Browser probe: Playwright 1.63 with Chromium 140 launches locally and produces current screenshot evidence.

## Isolation

- Case root: `evals/runs/capability-compiler-v2/phase-11/<case-id>/`
- Source workspace: `<case-root>/workspace/`
- Baseline snapshot: `<case-root>/baseline/`
- Evidence root: `<case-root>/evidence/`
- Package root: `<case-root>/package/`
- The dirty `skills-hub` source tree is never used as the application workspace.
- No user external repository or dirty workspace is modified.
- No remote Git, push, PR, merge, deployment, provider mutation, browser login, or local-system persistence.

The application workspace is a standalone snapshot, not a released V2 path. No local commit is required; the final patch is generated against the baseline snapshot with file hashes.

## Minimal Stack

Default stack, unless the selected concept makes it impossible:

- Python 3.12 standard library;
- `ThreadingHTTPServer` for local HTTP;
- SQLite for persistence and transactional constraints;
- native HTML/CSS/JavaScript;
- pytest for host-owned tests;
- Playwright Python for browser, responsive, keyboard, accessibility-structure, and performance evidence.

No new dependency is added merely for scaffolding. Existing pytest, jsonschema, and Playwright installations may be used by the host. The app must remain runnable with Python stdlib alone; verification tooling is external to the package.

## Lifecycle Execution

### Stage 1 — Governance and Intake

- Record exact workspace, product owner checkpoint, data classification, roles, action boundaries, and local-only execution.
- Reject real personal/customer data; use labeled synthetic records only.
- Record no-remote/no-production authority.

### Stage 2 — Discovery and Research

- Produce supplied-assumption research, jobs, risks, alternatives, unknowns, and falsification conditions.
- No participant contact, scraping, or external data collection.

### Stage 3 — Strategy and Prioritization

- Compare at least three bounded product scopes.
- Record exact scoring framework/formula/variables/unknowns.
- Human selects the scope.

### Stage 4 — Requirements and Planning

- Produce EARS-style requirements, acceptance criteria, non-goals, traceability, implementation plan, test plan, and review disposition.
- Preserve requirements-to-tests IDs.

### Stage 5 — Experience Design

- Produce information architecture, user flows, responsive states, design tokens, interaction/accessibility/motion contracts, and complete UI route.
- New visual world follows the Impeccable new-work workflow; product UI uses Operate mode.
- Product truth and visual direction remain human checkpoints.
- Implement all required states: default, loading, empty, validation error, conflict, unauthorized, success, disabled, focus, mobile, desktop, reduced motion.

### Stage 6 — Architecture, Data, API, Authorization, and Security

- Define trust boundaries, modules, SQLite schema, transactions, API contract, validation, idempotency, authorization matrix, CSRF/origin policy, session boundary, secret policy, abuse cases, migration/backup/rollback assumptions, and threat model.
- Authentication is demonstrative local role selection; it is never mislabeled production authentication.
- Authorization remains server-enforced and default-deny.

### Stage 7 — Implementation

- Model writer receives only `read/edit/write` in the isolated workspace.
- Model receives approved requirements/design/architecture and cannot run shell, network, Git, or tests.
- Host owns commands and verification.
- Source changes remain within the snapshot workspace.

### Stage 8 — Independent Verification

- Host runs unit/API/integration tests, syntax checks, build/package checks, and security assertions.
- Independent read-only model review and black-box QA cannot edit source.
- Findings require evidence and route through a separately authorized writer; repaired results invalidate affected browser/test evidence.

### Stage 9 — Performance and Reliability

- Measure matched local runs with warmup, repeats, median, spread, p95, concurrency, and failed-case retention.
- Verify SQLite conflict prevention, restart persistence, deterministic fixtures, and graceful error paths.
- No invented production capacity claim.

### Stage 10 — Release Readiness

- Produce local package, checksums, SBOM-like file/dependency inventory, configuration/secrets matrix, runbook, migration/backup notes, release notes, and delivery preflight.
- Named human release decision remains pending; readiness does not authorize remote action.

### Stage 11 — Deployment Change

- **Not executed.** Produce deployment plan only.
- Every remote action remains disabled pending fresh exact authorization.

### Stage 12 — Observation and Canary

- Produce local health endpoint checks, metrics/log schema, SLO candidates, canary baseline, observation window, missing-data policy, alert ownership, retention/deletion, and rollback recommendation boundary.
- No provider configuration.

### Stage 13 — Incident and Recovery

- Produce incident scenario, severity/roles, evidence timeline template, backup/restore proof, rollback rehearsal, and closure criteria.
- No provider incident mutation.

### Stage 14 — Learning and Feedback

- Produce retrospective, outcome versus hypothesis, unresolved risks, next-cycle requirements, and evidence-linked improvement actions.
- No persistent external learning write.

### Stage 15 — Tool Runtime Support

- Run only when the selected owner is blocked by local tooling.
- Existing Playwright readiness is proven; no install/upgrade is currently expected.
- Support never grants lifecycle approval and returns to the blocked owner.

## Model and Host Evidence

Every model step stores:

- prompt and material hashes;
- command receipt and no-network/tool policy;
- raw Pi JSON events;
- output or workspace patch;
- provider/model/token/duration/exit/stop data;
- tool event ledger;
- stage status and failure route.

Every host command stores:

- exact argv and cwd;
- start/end and duration;
- stdout/stderr;
- exit code;
- artifact hashes;
- environment/tool versions where relevant.

No retry overwrites a failed attempt. Repairs create a new iteration and preserve the prior failure.

## Browser and Design Evidence

At minimum:

- desktop 1440×1000;
- mobile 390×844;
- current route/state/viewport/input mode/source revision/timestamp/tool/hash manifest;
- keyboard-only primary journey;
- visible focus;
- responsive structure;
- reduced-motion path;
- empty, validation, conflict, unauthorized, success, and coordinator states;
- screenshots opened and validated as nonblank/current;
- DOM/accessibility assertions supplement but do not replace rendered evidence;
- one bounded visual review, one batch of fixes if required, one confirmation round.

## Acceptance Thresholds

All are frozen before implementation:

- requirements: every requirement has acceptance criteria and at least one verification route;
- architecture: no unresolved critical trust-boundary, authorization, data-integrity, secret, or rollback gap;
- tests: 100% pass, no deleted/disabled failures;
- API authorization matrix: 100% server-enforced expected outcomes;
- booking conflict and transaction tests: 100% pass under concurrent attempts;
- browser journeys: 100% required desktop/mobile/keyboard/state cases pass;
- accessibility structure: zero missing label/name/landmark/focus-order blockers in declared scope;
- rendering: zero blank/black/wrong-state captures; all evidence hashes current;
- performance: local p95 health/read/list/write thresholds declared before measurement and all met, or fail with retained evidence;
- security: zero critical/high unresolved findings in declared local-demo threat model;
- package: fresh unpack-and-run smoke passes using only documented runtime dependency;
- patch/manifest: all bytes and SHA-256 recompute exactly;
- remote/provider/production actions executed: zero.

No threshold may be lowered after results.

## Required Outputs

- approved product brief and decision record;
- discovery, strategy, requirements, UX/UI, architecture, threat model, API/data/authorization contracts;
- runnable application source;
- tests and browser scripts;
- current screenshots and rendered-review report;
- performance/reliability report;
- local package and checksums;
- full patch and file manifest;
- deployment, observability, canary, incident, rollback, and retrospective documents;
- human-review packet for Phase 12;
- Phase 11 Gate, manifest, phase report, and final V2 documentation update.

## Gates

Phase 11 fails closed on:

- missing product decision;
- Phase 9/10 tree drift;
- application source outside the isolated snapshot;
- model shell/network/remote/provider/production access;
- implementation without approved requirements/design/architecture;
- review or QA mutating source;
- stale tests/screenshots/performance evidence after repair;
- incomplete role/authorization or conflict handling;
- static source standing in for real browser review;
- missing package smoke, patch, hashes, rollback, observation, or residual-risk evidence;
- any failed predeclared threshold;
- remote action or claim of deployment/release;
- claim of final user approval.

## Stop Conditions

Stop and ask on product concept rejection, visual direction ambiguity, risk acceptance, a required capability absent from the accepted taxonomy, repeated implementation failure, inaccessible browser evidence, threshold miss after the bounded repair round, or any request to execute remote/production change.
