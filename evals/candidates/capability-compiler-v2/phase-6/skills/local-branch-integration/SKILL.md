---
name: local-branch-integration
description: Integrate an approved local base ref into an isolated change branch while preserving a recoverable pre-integration ref and performing no remote writes. Do not use for create or update the remote pull request from a verified pushed ref or install or configure a destructive git command guard locally.
---

# Local Branch Integration

## Responsibility

Integrate an approved local base ref into an isolated change branch while preserving a recoverable pre-integration ref and performing no remote writes.

## Trigger

Use when the requested outcome is: Integrate an approved local base ref into an isolated change branch while preserving a recoverable pre-integration ref and performing no remote writes.

Do not use when:
- Create or update the remote pull request from a verified pushed ref. Route to `remote-pull-request-change`.
- Install or configure a destructive Git command guard locally. Route to `local-git-guard-setup`.

## Required Inputs

- Isolated worktree, change branch, approved base reference, clean-state evidence, and local mutation authority.

Also require exact target identity, authority, mutation boundary, evidence consumer, cleanup or rollback, and declared unknowns where applicable.

## Procedure

1. Verify repository and worktree identity, current branch, clean state, approved local base ref, expected ancestry, local-only authority, and no concurrent writer.
2. Record pre-integration HEAD and create a recoverable local reference before the approved non-destructive merge or rebase mode.
3. Perform only the declared local integration; stop on conflicts and preserve index, worktree, refs, and exact recovery commands.
4. Record post-state, changed files, conflicts or success, before/after refs, and required host checks; never fetch, push, force, delete, or merge remotely.

## Output Contract

Produce:
- integrated local branch or conflict state
- before and after ref evidence
- changed-file or conflict report
- exact recovery command

Every material action, command, result, finding, score, capture, provider receipt, or completion claim must bind to exact target identity and current evidence or be labeled assumption/unknown.

## Coverage

- `local-only`
- `clean-worktree`
- `pre-integration-ref`
- `conflict-preservation`
- `recovery-command`
- `no-remote-write`

## Hard Gates

- Local integration requires an approved local base ref, clean isolated change branch, recoverable pre-integration identity, and zero fetch, push, force, remote merge, or branch deletion.
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
- `isolated-task-implementation`
- `local-git-guard-setup`
- `change-delivery-preflight`
- `pull-request-update`

Never silently expand source, command, browser, data, credential, local-system, provider, or remote authority. Independent review, QA, audit, evidence acquisition, analysis, and triage never repair source. Setup and authentication never imply authority to perform the downstream action.
