# Full Dev Loop Runtime Design

Status: approved-by-execution-request
Requirements: `.specs/full-dev-loop-runtime/requirements.md`

## DES-001 — Versioned contract extensions

**Implements:** REQ-003, REQ-004, REQ-006

Extend Slot contracts with optional `execution` metadata: adapter, allowed tools, mutation class, authorization requirements, and correction inputs. Extend Recipes with optional routing metadata, sub-Recipe steps, feedback mappings, and retry policy. All additions remain optional so the existing 0.2.0 Recipe stays valid.

**Verification:** AC-011–AC-020, AC-026–AC-029.

## DES-002 — Recursive Recipe verifier and catalog

**Implements:** REQ-001, REQ-005, REQ-006, REQ-007

Load all Recipe files by ID and exact version, validate release evidence, recursively expand sub-Recipe references for dependency and permission checks, detect cycles, reject ambiguous route phrases, and require fail-closed coverage for each executable step status.

**Verification:** AC-003–AC-005, AC-021–AC-022, AC-026–AC-032.

## DES-003 — Workflow state store

**Implements:** REQ-002, REQ-003, REQ-005

Create `tools/curation/workflow_state.py`. `state.json` is validated machine truth. Writes use same-directory temporary file, flush, fsync, then `os.replace`. `state.md` is deterministically rendered after JSON commit. Unsupported or corrupt state is copied to a diagnostic path and execution blocks.

**Verification:** AC-006–AC-015, AC-025.

## DES-004 — Released-only router

**Implements:** REQ-001, REQ-006

Create `tools/curation/recipe_route.py` and `recipes/catalog.json`. Priority: explicit Recipe ref, resumable state, deterministic phrase scoring, optional structured model tie-break restricted to catalog enum. Ambiguity returns `needs-input`; text cannot add candidates.

**Verification:** AC-001–AC-005, AC-029.

## DES-005 — Stateful orchestration engine

**Implements:** REQ-002, REQ-003, REQ-005

Refactor `recipe_execute.py` around an execution queue and state store. Preserve current worker callable compatibility. Apply failure routes, feedback mappings, invalidation, retry budget, failure fingerprint detection, and existing hash reuse. Persist before and after each external execution boundary.

**Verification:** AC-006–AC-015, AC-021–AC-025.

## DES-006 — Execution adapters and authorization policy

**Implements:** REQ-004

Keep the current no-tools Pi adapter for artifact-only steps. Add a workspace adapter that requires explicit authorization flags, creates a temporary Git worktree, applies a fixed tool allowlist, captures structured command/tool evidence, and returns a patch/result artifact. Deny remote/network/deploy capabilities by default.

**Verification:** AC-016–AC-020.

## DES-007 — Minimal stage Slot closure

**Implements:** REQ-005, REQ-007

Promote only the smallest capability closure needed by six stages:

- Requirements: existing 4 released pilot Slots.
- Design: `design-context-and-direction-contract`, `interaction-states-forms-and-navigation`, `accessibility-contracts-and-assistive-validation`, `cross-domain-ui-preflight-checklists`.
- Implementation: `implementation-planning-and-handoff`, `tdd-change-loop`, `developer-self-check-and-fix`, `completion-evidence-gate`.
- QA: `independent-blackbox-qa`, `independent-code-review`, `baseline-regression-control`.
- Delivery: `change-delivery-preflight`, `change-packaging-and-versioning`, `merge-and-deploy-readiness`.
- Retrospective: `engineering-retrospective-and-improvement`, `root-cause-investigation`, `results-analysis-and-decision-readout`, `feedback-and-continuous-learning-loop`.

All other draft Slots remain unreleased.

**Verification:** AC-021–AC-025, AC-030.

## DES-008 — Stage Recipes and full composition

**Implements:** REQ-001, REQ-003, REQ-005, REQ-007

Create `write-prd`, `design-web-flow`, `build-feature-tdd`, `qa-only`, `ship-release`, `retro-to-requirements`, and `full-dev-loop`. `write-prd` wraps the existing Recipe as a sub-Recipe. `full-dev-loop` composes stage Recipes. Feedback routes use stable artifact keys.

**Verification:** AC-021–AC-032.

## DES-009 — Evaluation and release evidence generator

**Implements:** REQ-007

Use a shared stage-release manifest and verifier rather than cloning the pilot's one-off code. Each promoted Slot records source provenance plus rubric, baseline/candidate, holdout, mutation, permission, automated review, and explicit human review evidence. Recipe evidence includes successful composition and failure injections.

**Verification:** AC-030–AC-032.

## DES-010 — Unified Gates and dynamic status

**Implements:** REQ-008

Add runtime routing/state/authorization/composition Gates to `run_all_gates.py`. Change `render_status.py` to parse test summary and release counts from `gate-report.json` and release manifests. CI runs the same entry point.

**Verification:** AC-033–AC-035.

## Trust boundaries

- `skills/`: immutable source evidence.
- `slots/` and `recipes/`: versioned released runtime assets.
- `.workflow/`: project-local machine state, never release evidence.
- isolated worktree: only location for authorized implementation mutation.
- host repository and remote/network/deployment: denied unless explicitly authorized.

## Failure handling

- Validation failure: `blocked`, no worker call.
- Missing required input: `needs-input`, no downstream call.
- Runtime or Gate failure: persist evidence, apply declared route.
- Repeated fingerprint or budget exhaustion: `blocked`.
- State corruption: preserve file, produce diagnostic, do not overwrite.
