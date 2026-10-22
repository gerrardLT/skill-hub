---
name: plan-execution-control
description: "Advance an approved implementation plan through explicit step states, dependencies, checkpoints, evidence, invalidation, pause, and resume without absorbing specialist work. Use when An approved plan is being executed step by step and someone must track state, dependencies and checkpoints; A step failed or an upstream artifact changed and dependents must be stopped and invalidated. Do not use for: Write the implementation plan and dependency-ordered work slices (-> implementation-planning-and-handoff); Implement one already-selected isolated task slice (-> isolated-task-implementation)."
---

# Plan Execution Control

## Responsibility

Advance an approved implementation plan through explicit step states, dependencies, checkpoints, evidence, invalidation, pause, and resume without absorbing specialist work.

## Trigger

Use when the request matches any of:
- An approved plan is being executed step by step and someone must track state, dependencies and checkpoints
- A step failed or an upstream artifact changed and dependents must be stopped and invalidated

Do not use when:
- Write the implementation plan and dependency-ordered work slices. Route to `implementation-planning-and-handoff`.
- Implement one already-selected isolated task slice. Route to `isolated-task-implementation`.

## Required Inputs

- An executable implementation plan and an isolated work environment.

## Procedure

1. Freeze the approved plan version, step DAG, owners, permission identities, artifacts, gates, checkpoints, failure routes, and current source identity.
2. Validate prerequisites and assign one atomic owner per ready step; the controller changes state but does not perform specialist work itself.
3. Record pending, ready, running, passed, needs-input, blocked, failed, and invalidated transitions with input and output hashes.
4. On failure or upstream change, stop dependents, preserve evidence, invalidate affected outputs, and emit a bounded pause, retry, rollback, or resume instruction.

## Domain Guidance

- Map implementer report states to transitions: DONE moves to review; DONE_WITH_CONCERNS requires reading the concerns and resolving correctness or scope concerns before review; NEEDS_CONTEXT returns to the owner for the missing information; BLOCKED stops dependents.
- Invariant: never run two writers against the same workspace or overlapping files at the same time.

## Output Contract

Produce:
- plan execution state ledger
- step and dependency status
- checkpoint and evidence map
- invalidation, pause, and resume instructions

Every material action, command, result, finding, score, capture, provider receipt, or completion claim must bind to exact target identity and current evidence or be labeled assumption/unknown.

Deliver each output as the artifact itself (tables, commands, patches, plans, records), not as a description of how it would be produced.

## Coverage

- `step-state`
- `dependency-DAG`
- `checkpoint`
- `evidence-hash`
- `invalidation`
- `pause-resume`
- `no-specialist-work`

## Hard Gates

- A controller may transition only steps whose dependencies, identity, authority, and gates are current; it cannot mark specialist work passed or reuse evidence after upstream invalidation.
- Independent review, QA, audit, acquisition, analysis, and triage never imply remediation; setup or authentication never implies downstream action authority.
- Preserve source, build, dataset, model, workflow, provider, browser, session, or local-system identity; command, version, exit, duration, artifacts, hashes, limitations, and cleanup must remain explicit when applicable.
- Return `needs-input` when a named owner can provide missing scope, authority, evidence, governance, target, or decision.
- Return `blocked` when proceeding would exceed mutation authority, expose credentials, violate governance, erase failed evidence, perform an undeclared remote or destructive action, or mix independent review with repair.
- Deliver every part the supplied evidence and authority support, label assumptions, and list each missing item with the owner who can supply it; `needs-input` or `blocked` applies to the unsupported part, not to the whole deliverable.

## Forbidden Actions

- request, reveal, print, persist, hash, or transmit credential or secret values
- perform source, local-system, browser, provider, publication, or remote mutations outside the exact atomic scope and fresh authorization
- invent commands, exits, duration, artifacts, captures, provider receipts, benchmark results, approval, or completion evidence
- combine independent evidence or findings with remediation, risk acceptance, publication, deployment, or release
- claim evaluation, approval, release, or completion evidence that has not been produced

## Status Mapping

- `passed`: the atomic output and every gate have current target-bound evidence.
- `needs-input`: a requestable scope, authority, target, fixture, governance term, or decision is absent. Deliver every supported part first and name the owner for the missing part.
- `blocked`: safe work requires prohibited access, unavailable authority, secret values, destructive or remote action, or an incompatible identity.
- `failed`: the authorized action ran but a deterministic check or required output failed.

## Non-Responsibilities

Adjacent capabilities:
- `implementation-planning-and-handoff`
- `isolated-task-implementation`
- `workflow-orchestration-and-lifecycle`
- `completion-evidence-gate`

Never silently expand source, command, browser, data, credential, local-system, provider, or remote authority. Independent review, QA, audit, evidence acquisition, analysis, and triage never repair source. Setup and authentication never imply authority to perform the downstream action.
