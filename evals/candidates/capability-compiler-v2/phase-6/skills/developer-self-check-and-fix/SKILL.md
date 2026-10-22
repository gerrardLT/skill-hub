---
name: developer-self-check-and-fix
description: Self-review one completed authorized change, fix only deterministic defects within its frozen scope, and leave independent review ownership intact. Do not use for perform the independent code review and issue findings without changing source or investigate a newly observed behavior whose root cause is not established.
---

# Developer Self Check And Fix

## Responsibility

Self-review one completed authorized change, fix only deterministic defects within its frozen scope, and leave independent review ownership intact.

## Trigger

Use when the requested outcome is: Self-review one completed authorized change, fix only deterministic defects within its frozen scope, and leave independent review ownership intact.

Do not use when:
- Perform the independent code review and issue findings without changing source. Route to `independent-code-review`.
- Investigate a newly observed behavior whose root cause is not established. Route to `root-cause-investigation`.

## Required Inputs

- Implemented code, its task specification, test output, and change list.

Also require exact target identity, authority, mutation boundary, evidence consumer, cleanup or rollback, and declared unknowns where applicable.

## Procedure

1. Freeze the patch, scope, acceptance criteria, changed files, existing test evidence, and independent-review handoff boundary.
2. Inspect the diff and affected callers for correctness, error handling, security, compatibility, dead code, formatting, and test gaps.
3. Fix only reproducible in-scope defects; route scope expansion or unknown cause to the owning capability instead of opportunistic refactoring.
4. Run approved focused checks, record every correction and remaining concern, and hand off without declaring independent approval.

## Output Contract

Produce:
- self-review checklist
- bounded correction patch
- updated focused evidence
- independent-review handoff

Every material action, command, result, finding, score, capture, provider receipt, or completion claim must bind to exact target identity and current evidence or be labeled assumption/unknown.

## Coverage

- `self-review`
- `changed-files`
- `bounded-correction`
- `no-scope-expansion`
- `no-independent-approval`
- `handoff`

## Hard Gates

- A developer correction pass may fix deterministic in-scope defects but must never impersonate independent review, erase failed evidence, or expand the frozen change.
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
- `defect-remediation`
- `root-cause-investigation`
- `independent-code-review`
- `implementation-spec-compliance-review`

Never silently expand source, command, browser, data, credential, local-system, provider, or remote authority. Independent review, QA, audit, evidence acquisition, analysis, and triage never repair source. Setup and authentication never imply authority to perform the downstream action.
