---
name: change-scope-freeze
description: "Freeze one authorized change boundary, affected artifacts, non-goals, invariants, owners, and invalidation conditions before implementation begins. Use when A change is about to start and someone must fix exactly which files, behaviors and non-goals it may touch; Scope keeps drifting and the team needs a frozen boundary with conditions that reopen it. Do not use for: Implement the already-frozen task in an isolated workspace (-> isolated-task-implementation); Investigate the unresolved cause and determine what the scope should include (-> root-cause-investigation); Block edits outside a directory with a guard hook (-> git-destructive-command-guard)."
---

# Change Scope Freeze

## Responsibility

Freeze one authorized change boundary, affected artifacts, non-goals, invariants, owners, and invalidation conditions before implementation begins.

## Trigger

Use when the request matches any of:
- A change is about to start and someone must fix exactly which files, behaviors and non-goals it may touch
- Scope keeps drifting and the team needs a frozen boundary with conditions that reopen it

Do not use when:
- Implement the already-frozen task in an isolated workspace. Route to `isolated-task-implementation`.
- Investigate the unresolved cause and determine what the scope should include. Route to `root-cause-investigation`.
- Block edits outside a directory with a guard hook. Route to `git-destructive-command-guard`.

## Required Inputs

- Authorized scope, protected paths, change identity, and expiry condition.

## Procedure

1. Record approved requirement or finding IDs, target source identity, allowed files or modules, observable behavior, tests, invariants, and explicit exclusions.
2. Separate required change, permitted incidental cleanup, prohibited expansion, and unresolved prerequisite.
3. Name the writer, workspace, evidence owner, review boundary, and conditions that invalidate or reopen scope.
4. Emit the frozen scope and stop; do not implement, test, review, or approve the change.

## Domain Guidance

- Record every allowed path as a normalized absolute prefix ending in a path separator, so a sibling such as src/app-old never matches src/app.
- List invalidation conditions as concrete triggers: requirement id changed, base ref moved, a protected path needed, a new dependency required.

## Output Contract

Produce:
- frozen change-scope contract
- allowed and prohibited artifact map
- invariant and non-goal register
- scope invalidation conditions

Every material action, command, result, finding, score, capture, provider receipt, or completion claim must bind to exact target identity and current evidence or be labeled assumption/unknown.

Deliver each output as the artifact itself (tables, commands, patches, plans, records), not as a description of how it would be produced.

## Coverage

- `scope-freeze`
- `single-writer`
- `authorized-workspace`
- `invariants`
- `non-goals`
- `invalidation`

## Hard Gates

- No implementation begins until the required behavior, authorized workspace, single writer, allowed mutation boundary, tests, invariants, and non-goals are explicit.
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

## Human Decision Authority

The Skill may return evidence, findings, options, and a recommendation. Scope approval, repair authorization, risk acceptance, publication, experiment submission, local-system change, remote action, and release disposition remain explicit human decisions under the declared identity.

## Status Mapping

- `passed`: the atomic output and every gate have current target-bound evidence.
- `needs-input`: a requestable scope, authority, target, fixture, governance term, or decision is absent. Deliver every supported part first and name the owner for the missing part.
- `blocked`: safe work requires prohibited access, unavailable authority, secret values, destructive or remote action, or an incompatible identity.
- `failed`: the authorized action ran but a deterministic check or required output failed.

## Non-Responsibilities

Adjacent capabilities:
- `root-cause-investigation`
- `isolated-task-implementation`
- `plan-execution-control`
- `implementation-spec-compliance-review`
- `git-destructive-command-guard`

Never silently expand source, command, browser, data, credential, local-system, provider, or remote authority. Independent review, QA, audit, evidence acquisition, analysis, and triage never repair source. Setup and authentication never imply authority to perform the downstream action.
