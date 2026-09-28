# Full Dev Loop Runtime Requirements

Status: approved-by-execution-request
Baseline: `curation/full-dev-loop-baseline.json`

## Scope

Extend the released requirements-to-acceptance-criteria pilot into a fail-closed six-stage runtime with natural-language routing, durable workflow state, executable failure routes, permission-aware execution, and released stage recipes.

## Exclusions

- No provider-specific deployment adapter is released in this scope.
- No remote push, merge, network call, production mutation, or deployment occurs without explicit authorization.
- Draft Slots outside the selected minimum dependency closure remain unreleased.
- Existing `requirements-to-acceptance-criteria@0.2.0` behavior and evidence remain valid.

## REQ-001 — Natural-language routing

**User story:** As a user, I want a natural-language request routed to one released Recipe so I do not need to know internal IDs.

- **AC-001:** WHEN an explicit released Recipe ID is supplied THEN the router SHALL select it before considering stored state or natural-language classification.
- **AC-002:** WHEN resumable workflow state identifies a released Recipe THEN the router SHALL resume it before classifying free text.
- **AC-003:** WHEN exactly one released Recipe matches the request THEN the router SHALL return its exact ID and version.
- **AC-004:** WHEN zero or multiple Recipes remain plausible THEN the router SHALL return `needs-input` with bounded choices and SHALL NOT guess.
- **AC-005:** WHEN request text contains instructions to bypass the catalog or select an unreleased Recipe THEN the router SHALL ignore those instructions and fail closed.

## REQ-002 — Durable workflow state

**User story:** As a user, I want interrupted workflows to resume from verified evidence rather than restart or trust prose claims.

- **AC-006:** WHEN a run changes state THEN the runtime SHALL atomically replace `.workflow/state.json`.
- **AC-007:** WHEN state is saved THEN `.workflow/state.md` SHALL be rendered from JSON and SHALL NOT be an independent source of truth.
- **AC-008:** WHEN state is loaded THEN schema, version, Recipe reference, step records, hashes, attempts, artifacts, evidence, and invalidations SHALL be validated.
- **AC-009:** WHEN state is missing THEN a new state SHALL be initialized without inventing completed steps.
- **AC-010:** WHEN state is corrupt or unsupported THEN execution SHALL return `blocked` without overwriting recoverable evidence.

## REQ-003 — Executable failure routes

**User story:** As a user, I want failures routed to the responsible upstream step without infinite loops or silent evidence loss.

- **AC-011:** WHEN a step returns `needs-input`, `failed`, or `blocked` THEN a matching declared failure route SHALL be applied or execution SHALL stop fail-closed.
- **AC-012:** WHEN action is `stop` THEN no downstream step SHALL execute.
- **AC-013:** WHEN action is `record-and-return` THEN failure evidence SHALL be persisted and returned without rerun.
- **AC-014:** WHEN action is `invalidate-and-rerun` THEN target and transitive downstream evidence SHALL be invalidated and the target SHALL receive explicit feedback.
- **AC-015:** WHEN retry budget is exhausted or an identical failure fingerprint repeats THEN execution SHALL stop `blocked`.

## REQ-004 — Permission-aware execution

**User story:** As a repository owner, I want mutation and external side effects guarded by explicit authority.

- **AC-016:** WHEN a step only generates documents THEN it SHALL run with the no-tool artifact adapter.
- **AC-017:** WHEN a step requires workspace reads, tests, or writes THEN the requested tool set SHALL be a subset of both Slot and Recipe permissions.
- **AC-018:** WHEN code mutation is authorized THEN it SHALL occur in an isolated Git worktree and record the worktree, commands, outputs, exit codes, and diff evidence.
- **AC-019:** WHEN explicit authorization is absent THEN workspace writes, remote Git, network access, merge, and deployment SHALL be denied.
- **AC-020:** WHEN a release request lacks deployment authorization THEN `ship-release` SHALL produce only a release-ready package.

## REQ-005 — Released six-stage composition

**User story:** As a user, I want requirements, design, implementation, QA, delivery, and retrospective to compose through versioned contracts.

- **AC-021:** WHEN each stage is invoked independently THEN it SHALL use only exact-version released Slot or sub-Recipe references.
- **AC-022:** WHEN `full-dev-loop` runs THEN it SHALL compose the same released stage Recipes without inlining Slot methods.
- **AC-023:** WHEN QA finds a defect THEN QA SHALL report and route it but SHALL NOT modify product source.
- **AC-024:** WHEN retrospective completes THEN a structured `next-requirements` artifact SHALL become a valid input to the next requirements stage.
- **AC-025:** WHEN an upstream input or artifact changes THEN all dependent cached evidence SHALL be invalidated.

## REQ-006 — Schema and verifier evolution

**User story:** As a maintainer, I want malformed or unsafe contracts rejected before execution.

- **AC-026:** WHEN legacy `requirements-to-acceptance-criteria@0.2.0` is loaded THEN it SHALL remain valid without migration.
- **AC-027:** WHEN Recipe recursion contains a cycle, unknown reference, version mismatch, route conflict, incomplete status coverage, or permission escalation THEN verification SHALL fail.
- **AC-028:** WHEN Slot execution metadata is malformed THEN verification SHALL fail before model or tool invocation.
- **AC-029:** WHEN a released Recipe is cataloged THEN its release evidence hashes and review verdict SHALL be valid.

## REQ-007 — Release evidence

**User story:** As a maintainer, I want every newly released Slot and Recipe backed by executable and reviewable evidence.

- **AC-030:** WHEN a Slot is promoted THEN rubric, baseline, candidate, holdout, mutation, permission, and review evidence SHALL exist and pass.
- **AC-031:** WHEN a Recipe is promoted THEN single-stage and composition runs, failure injection, state recovery, substitution, and review evidence SHALL pass.
- **AC-032:** WHEN human review is required but absent THEN the asset SHALL remain unreleased.

## REQ-008 — Regression and completion truth

**User story:** As a maintainer, I want completion claims derived from reproducible Gates.

- **AC-033:** WHEN the implementation is complete THEN the original 175-test baseline and all new tests SHALL pass.
- **AC-034:** WHEN status documents are rendered THEN test and released-asset counts SHALL come from machine reports rather than literals.
- **AC-035:** WHEN final audit is generated THEN all runtime paths SHALL be fail-closed and `skills/` SHALL match its immutable baseline.
