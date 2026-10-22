---
name: plan-execution-control
description: "Consolidated capability with 2 selectable modes: plan-execution-control; plan-review-decision-synthesis. Choose exactly one mode per invocation."
version: 1.1.0-consolidated
modes: [plan-execution-control, plan-review-decision-synthesis]
---

# Plan Execution Control

## Responsibility

Consolidated capability covering 2 related modes: Advance an approved implementation plan through explicit step states, dependencies, checkpoints, evidence, invalidation, pause, and resume without absorbing specialist work.; Synthesize independent plan-review findings, preserve dissent, classify decision types, and surface human approval points without rerunning reviews.

## Mode selection

This capability has several distinct modes. Read this table first, pick exactly one
mode for the current request, then follow only that mode's section. Do not blend
modes: each carries its own permission identity, gates, and stop conditions. The
permission column is binding - a run uses the permission of the mode it selected,
never the widest permission in this document.

| Mode | Permission | Use when | Routes elsewhere |
| --- | --- | --- | --- |
| `plan-execution-control` | `workspace-write-local-exec` | An approved plan is being executed step by step and someone must track state, dependencies and checkpoints; A step failed or an upstream artifact changed and dependents must be stopped and invalidated | Write the implementation plan and dependency-ordered work slices (-> implementation-planning-and-handoff); Implement one |
| `plan-review-decision-synthesis` | `workspace-write` | Several independent plan reviews exist and someone must merge them into one decision view without hiding disagreement; A plan needs its open issues sorted into mechanical fixes, taste choices and one- | Perform the independent design review that is missing (-> design-plan-review); Approve and edit the plan using the synth |

## Mode: `plan-execution-control`

### plan-execution-control

#### Responsibility

Advance an approved implementation plan through explicit step states, dependencies, checkpoints, evidence, invalidation, pause, and resume without absorbing specialist work.

#### Trigger

Use when the request matches any of:
- An approved plan is being executed step by step and someone must track state, dependencies and checkpoints
- A step failed or an upstream artifact changed and dependents must be stopped and invalidated

Do not use when:
- Write the implementation plan and dependency-ordered work slices. Route to `implementation-planning-and-handoff`.
- Implement one already-selected isolated task slice. Route to `isolated-task-implementation`.

#### Required Inputs

- An executable implementation plan and an isolated work environment.

#### Procedure

1. Freeze the approved plan version, step DAG, owners, permission identities, artifacts, gates, checkpoints, failure routes, and current source identity.
2. Validate prerequisites and assign one atomic owner per ready step; the controller changes state but does not perform specialist work itself.
3. Record pending, ready, running, passed, needs-input, blocked, failed, and invalidated transitions with input and output hashes.
4. On failure or upstream change, stop dependents, preserve evidence, invalidate affected outputs, and emit a bounded pause, retry, rollback, or resume instruction.

#### Domain Guidance

- Map implementer report states to transitions: DONE moves to review; DONE_WITH_CONCERNS requires reading the concerns and resolving correctness or scope concerns before review; NEEDS_CONTEXT returns to the owner for the missing information; BLOCKED stops dependents.
- Invariant: never run two writers against the same workspace or overlapping files at the same time.
- Unspecified null-versus-false semantics are an owner decision, not an implementation guess. Resume only dependent work whose meaning and evidence are established; keep unrelated supported work deliverable.

#### Output Contract

Produce:
- plan execution state ledger
- step and dependency status
- checkpoint and evidence map
- invalidation, pause, and resume instructions

Every material action, command, result, finding, score, capture, provider receipt, or completion claim must bind to exact target identity and current evidence or be labeled assumption/unknown.

Deliver each output as the artifact itself (tables, commands, patches, plans, records), not as a description of how it would be produced.

#### Coverage

- `step-state`
- `dependency-DAG`
- `checkpoint`
- `evidence-hash`
- `invalidation`
- `pause-resume`
- `no-specialist-work`

#### Hard Gates

- A controller may transition only steps whose dependencies, identity, authority, and gates are current; it cannot mark specialist work passed or reuse evidence after upstream invalidation.
- Independent review, QA, audit, acquisition, analysis, and triage never imply remediation; setup or authentication never implies downstream action authority.
- Preserve source, build, dataset, model, workflow, provider, browser, session, or local-system identity; command, version, exit, duration, artifacts, hashes, limitations, and cleanup must remain explicit when applicable.
- Return `needs-input` when a named owner can provide missing scope, authority, evidence, governance, target, or decision.
- Return `blocked` when proceeding would exceed mutation authority, expose credentials, violate governance, erase failed evidence, perform an undeclared remote or destructive action, or mix independent review with repair.
- Deliver every part the supplied evidence and authority support, label assumptions, and list each missing item with the owner who can supply it; `needs-input` or `blocked` applies to the unsupported part, not to the whole deliverable.

#### Forbidden Actions

- request, reveal, print, persist, hash, or transmit credential or secret values
- perform source, local-system, browser, provider, publication, or remote mutations outside the exact atomic scope and fresh authorization
- invent commands, exits, duration, artifacts, captures, provider receipts, benchmark results, approval, or completion evidence
- combine independent evidence or findings with remediation, risk acceptance, publication, deployment, or release
- claim evaluation, approval, release, or completion evidence that has not been produced

#### Status Mapping

- `passed`: the atomic output and every gate have current target-bound evidence.
- `needs-input`: a requestable scope, authority, target, fixture, governance term, or decision is absent. Deliver every supported part first and name the owner for the missing part.
- `blocked`: safe work requires prohibited access, unavailable authority, secret values, destructive or remote action, or an incompatible identity.
- `failed`: the authorized action ran but a deterministic check or required output failed.

#### Non-Responsibilities

Adjacent capabilities:
- `implementation-planning-and-handoff`
- `isolated-task-implementation`
- `workflow-orchestration-and-lifecycle`
- `completion-evidence-gate`

Never silently expand source, command, browser, data, credential, local-system, provider, or remote authority. Independent review, QA, audit, evidence acquisition, analysis, and triage never repair source. Setup and authentication never imply authority to perform the downstream action.

## Mode: `plan-review-decision-synthesis`

### plan-review-decision-synthesis

#### Responsibility

Synthesize independent plan-review findings, preserve dissent, classify decision types, and surface human approval points without rerunning reviews.

#### Trigger

Use when the request matches any of:
- Several independent plan reviews exist and someone must merge them into one decision view without hiding disagreement
- A plan needs its open issues sorted into mechanical fixes, taste choices and one-way doors for a human to decide

Do not use when:
- Perform the independent design review that is missing. Route to `design-plan-review`.
- Approve and edit the plan using the synthesized recommendations. Route to `implementation-planning-and-handoff`.

#### Required Inputs

- Independent review findings, plan version, decision policy, authority, and unresolved questions.

#### Procedure

1. Verify review identities, frozen plan version, citations, applicability, and independence.
2. Deduplicate findings by underlying decision without erasing distinct rationale.
3. Classify evidence defect, reversible choice, taste decision, one-way door, conflict, and non-applicable item.
4. Preserve agreement, dissent, dependencies, and proposed amendments.
5. Return an audit trail and explicit human decisions; do not approve or write the plan.

#### Domain Guidance

- Mechanical items (one clearly right answer) carry a recommended resolution with the principle cited and stay out of the human queue. Taste choices and one-way doors go to the human approval queue with the owner named.
- Decision principles for mechanical items: choose completeness, fix what is inside the blast radius, prefer the simpler option when two fix the same thing, and never resolve a conflict between reviewers silently.

#### Output Contract

Produce:
- review decision matrix
- dissent register
- proposed amendments
- human approval queue

Every material claim, score, recommendation, or finding must link to a supplied or authorized source, or be labeled assumption/unknown.

Deliver each output as the artifact itself (tables, commands, patches, plans, records), not as a description of how it would be produced.

#### Hard Gates

- Synthesis cannot manufacture reviewer consensus, downgrade a blocking dissent, or convert recommendations into approved scope.
- Preserve conflicts, counterevidence, unknowns, source identity, and authority boundaries.
- Return `needs-input` when an identifiable owner can supply a missing requirement or decision.
- Return `blocked` when required authority, evidence, governance, or a safe execution boundary is unavailable.
- Deliver every part the supplied evidence and authority support, label assumptions, and list each missing item with the owner who can supply it; `needs-input` or `blocked` applies to the unsupported part, not to the whole deliverable.

#### Forbidden Actions

- remote Git, pull-request mutation, merge, deploy, cloud mutation, or external-system write
- invent facts, evidence, authority, approval, or customer data
- perform adjacent or downstream capability responsibilities
- claim evaluation, approval, release, or completion evidence that has not been produced

#### Human Decision Authority

Output evidence, options, tradeoffs, unknowns, and a recommendation. GO/PIVOT/KILL, scope approval, strategic selection, taste choices, and build approval remain human decisions; record the owner and decision separately.

#### Status Mapping

- `passed`: output contract and every hard gate are satisfied.
- `needs-input`: a requestable source, decision, or governance term is missing. Deliver every supported part first and name the owner for the missing part.
- `blocked`: proceeding would exceed authority, violate governance, or rely on unavailable critical evidence.
- `failed`: supplied inputs were processed but a deterministic gate or required output failed.

#### Non-Responsibilities

Adjacent capabilities:
- `independent-plan-review`
- `executive-plan-review`
- `design-plan-review`
- `developer-experience-plan-review`
- `implementation-planning-and-handoff`

Never perform remote Git, external-system writes, merge, deploy, cloud mutation, participant recruitment/contact, or downstream implementation unless a different explicitly authorized capability owns that action.
