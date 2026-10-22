---
name: change-scope-freeze
description: Freeze one authorized change boundary, affected artifacts, non-goals, invariants, owners, and invalidation conditions before implementation begins. Do not use for implement the already-frozen task in an isolated workspace or investigate the unresolved cause and determine what the scope should include.
---

# Change Scope Freeze

## Responsibility

Freeze one authorized change boundary, affected artifacts, non-goals, invariants, owners, and invalidation conditions before implementation begins.

## Trigger

Use when the requested outcome is: Freeze one authorized change boundary, affected artifacts, non-goals, invariants, owners, and invalidation conditions before implementation begins.

Do not use when:
- Implement the already-frozen task in an isolated workspace. Route to `isolated-task-implementation`.
- Investigate the unresolved cause and determine what the scope should include. Route to `root-cause-investigation`.

## Required Inputs

- Authorized scope, protected paths, change identity, and expiry condition.

Also require exact target identity, authority, mutation boundary, evidence consumer, cleanup or rollback, and declared unknowns where applicable.

## Procedure

1. Record approved requirement or finding IDs, target source identity, allowed files or modules, observable behavior, tests, invariants, and explicit exclusions.
2. Separate required change, permitted incidental cleanup, prohibited expansion, and unresolved prerequisite.
3. Name the writer, workspace, evidence owner, review boundary, and conditions that invalidate or reopen scope.
4. Emit the frozen scope and stop; do not implement, test, review, or approve the change.

## Output Contract

Produce:
- frozen change-scope contract
- allowed and prohibited artifact map
- invariant and non-goal register
- scope invalidation conditions

Every material action, command, result, finding, score, capture, provider receipt, or completion claim must bind to exact target identity and current evidence or be labeled assumption/unknown.

## Coverage

- `scope-freeze`
- `single-writer`
- `authorized-workspace`
- `invariants`
- `non-goals`
- `invalidation`

## Hard Gates

- No implementation begins until the required behavior, authorized workspace, single writer, allowed mutation boundary, tests, invariants, and non-goals are explicit.
- Preserve source, build, dataset, model, workflow, provider, browser, session, or local-system identity; command, version, exit, duration, artifacts, hashes, limitations, and cleanup must remain explicit when applicable.
- Return `needs-input` when a named owner can provide missing scope, authority, evidence, governance, target, or decision.
- Return `blocked` when proceeding would exceed mutation authority, expose credentials, violate governance, erase failed evidence, perform an undeclared remote or destructive action, or mix independent review with repair.

## Human Decision Authority

The Skill may return evidence, findings, options, and a recommendation. Scope approval, repair authorization, risk acceptance, publication, experiment submission, local-system change, remote action, and release disposition remain explicit human decisions under the declared identity.

## Status Mapping

- `passed`: the atomic output and every gate have current target-bound evidence.
- `needs-input`: a requestable scope, authority, target, fixture, governance term, or decision is absent.
- `blocked`: safe work requires prohibited access, unavailable authority, secret values, destructive or remote action, or an incompatible identity.
- `failed`: the authorized action ran but a deterministic check or required output failed.

## Non-Responsibilities

Does not absorb unrelated lifecycle responsibilities or expand provider, workspace, or remote-write authority implicitly.

Adjacent capabilities:
- `root-cause-investigation`
- `isolated-task-implementation`
- `plan-execution-control`
- `implementation-spec-compliance-review`

Never silently expand source, command, browser, data, credential, local-system, provider, or remote authority. Independent review, QA, audit, evidence acquisition, analysis, and triage never repair source. Setup and authentication never imply authority to perform the downstream action.
