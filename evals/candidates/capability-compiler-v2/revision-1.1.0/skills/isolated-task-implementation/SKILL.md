---
name: isolated-task-implementation
description: "Implement one frozen task in one isolated authorized workspace with a single writer, bounded checks, and a reviewable handoff. Use when One fully specified task must be implemented in an isolated workspace with a single writer and a reviewable handoff; A work slice is ready to code and tests must run through the host before review. Do not use for: Execute and track a multi-step implementation plan with checkpoints and invalidation (-> plan-execution-control); Repair an independently confirmed defect after root-cause evidence exists (-> defect-remediation)."
---

# Isolated Task Implementation

## Responsibility

Implement one frozen task in one isolated authorized workspace with a single writer, bounded checks, and a reviewable handoff.

## Trigger

Use when the request matches any of:
- One fully specified task must be implemented in an isolated workspace with a single writer and a reviewable handoff
- A work slice is ready to code and tests must run through the host before review

Do not use when:
- Execute and track a multi-step implementation plan with checkpoints and invalidation. Route to `plan-execution-control`.
- Repair an independently confirmed defect after root-cause evidence exists. Route to `defect-remediation`.

## Required Inputs

- One approved task, complete task-local context, isolated workspace, edit scope, test command, and escalation boundary.

## Procedure

1. Verify frozen scope, clean isolated workspace, base identity, single-writer ownership, required inputs, acceptance criteria, tests, and prohibited paths.
2. Read the full affected flow and existing patterns before writing; reuse current helpers and keep the smallest coherent diff.
3. Implement only the assigned slice and its required tests or fixtures; stop on ambiguity, scope expansion, dependency conflict, or concurrent mutation.
4. Run approved focused checks through the host and return patch, changed files, evidence, assumptions, and handoff state without integration or remote actions.

## Domain Guidance

- Escalate instead of guessing when: the task needs an architectural decision with several valid approaches, understanding code beyond what was provided, uncertainty about whether the approach is correct, or restructuring code the plan did not anticipate. Stopping with a clear question is correct; bad work is worse than no work.

## Output Contract

Produce:
- isolated implementation patch
- changed-file and scope evidence
- focused verification records
- review and integration handoff

Every material action, command, result, finding, score, capture, provider receipt, or completion claim must bind to exact target identity and current evidence or be labeled assumption/unknown.

Deliver each output as the artifact itself (tables, commands, patches, plans, records), not as a description of how it would be produced.

## Coverage

- `isolated-workspace`
- `single-writer`
- `frozen-task`
- `minimal-diff`
- `host-checks`
- `no-integration`

## Hard Gates

- One task has one writer and one isolated workspace; missing isolation, dirty-state ambiguity, concurrent ownership, or scope expansion blocks implementation.
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
- `change-scope-freeze`
- `plan-execution-control`
- `defect-remediation`
- `local-branch-integration`

Never silently expand source, command, browser, data, credential, local-system, provider, or remote authority. Independent review, QA, audit, evidence acquisition, analysis, and triage never repair source. Setup and authentication never imply authority to perform the downstream action.
