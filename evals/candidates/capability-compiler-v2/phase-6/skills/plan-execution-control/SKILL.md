---
name: plan-execution-control
description: Advance an approved implementation plan through explicit step states, dependencies, checkpoints, evidence, invalidation, pause, and resume without absorbing specialist work. Do not use for write the implementation plan and dependency-ordered work slices or implement one already-selected isolated task slice.
---

# Plan Execution Control

## Responsibility

Advance an approved implementation plan through explicit step states, dependencies, checkpoints, evidence, invalidation, pause, and resume without absorbing specialist work.

## Trigger

Use when the requested outcome is: Advance an approved implementation plan through explicit step states, dependencies, checkpoints, evidence, invalidation, pause, and resume without absorbing specialist work.

Do not use when:
- Write the implementation plan and dependency-ordered work slices. Route to `implementation-planning-and-handoff`.
- Implement one already-selected isolated task slice. Route to `isolated-task-implementation`.

## Required Inputs

- An executable implementation plan and an isolated work environment.

Also require exact target identity, authority, mutation boundary, evidence consumer, cleanup or rollback, and declared unknowns where applicable.

## Procedure

1. Freeze the approved plan version, step DAG, owners, permission identities, artifacts, gates, checkpoints, failure routes, and current source identity.
2. Validate prerequisites and assign one atomic owner per ready step; the controller changes state but does not perform specialist work itself.
3. Record pending, ready, running, passed, needs-input, blocked, failed, and invalidated transitions with input and output hashes.
4. On failure or upstream change, stop dependents, preserve evidence, invalidate affected outputs, and emit a bounded pause, retry, rollback, or resume instruction.

## Output Contract

Produce:
- plan execution state ledger
- step and dependency status
- checkpoint and evidence map
- invalidation, pause, and resume instructions

Every material action, command, result, finding, score, capture, provider receipt, or completion claim must bind to exact target identity and current evidence or be labeled assumption/unknown.

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
- Preserve source, build, dataset, model, workflow, provider, browser, session, or local-system identity; command, version, exit, duration, artifacts, hashes, limitations, and cleanup must remain explicit when applicable.
- Return `needs-input` when a named owner can provide missing scope, authority, evidence, governance, target, or decision.
- Return `blocked` when proceeding would exceed mutation authority, expose credentials, violate governance, erase failed evidence, perform an undeclared remote or destructive action, or mix independent review with repair.

## Status Mapping

- `passed`: the atomic output and every gate have current target-bound evidence.
- `needs-input`: a requestable scope, authority, target, fixture, governance term, or decision is absent.
- `blocked`: safe work requires prohibited access, unavailable authority, secret values, destructive or remote action, or an incompatible identity.
- `failed`: the authorized action ran but a deterministic check or required output failed.

## Non-Responsibilities

Does not approve upstream product decisions, expand authority, or perform remote writes beyond its explicit permission identity.

Adjacent capabilities:
- `implementation-planning-and-handoff`
- `isolated-task-implementation`
- `workflow-orchestration-and-lifecycle`
- `completion-evidence-gate`

Never silently expand source, command, browser, data, credential, local-system, provider, or remote authority. Independent review, QA, audit, evidence acquisition, analysis, and triage never repair source. Setup and authentication never imply authority to perform the downstream action.
