---
name: local-branch-integration
description: "Integrate an approved local base ref into an isolated change branch while preserving a recoverable pre-integration ref and performing no remote writes. Use when An approved base ref must be merged or rebased into a change branch locally with a recovery ref kept; A worktree is clean and the user wants the latest base integrated without any remote writes. Do not use for: Create or update the remote pull request from a verified pushed ref (-> remote-pull-request-change); Install or configure a destructive Git command guard locally (-> local-git-guard-setup)."
---

# Local Branch Integration

## Responsibility

Integrate an approved local base ref into an isolated change branch while preserving a recoverable pre-integration ref and performing no remote writes.

## Trigger

Use when the request matches any of:
- An approved base ref must be merged or rebased into a change branch locally with a recovery ref kept
- A worktree is clean and the user wants the latest base integrated without any remote writes

Do not use when:
- Create or update the remote pull request from a verified pushed ref. Route to `remote-pull-request-change`.
- Install or configure a destructive Git command guard locally. Route to `local-git-guard-setup`.

## Required Inputs

- Isolated worktree, change branch, approved base reference, clean-state evidence, and local mutation authority.

## Procedure

1. Verify repository and worktree identity, current branch, clean state, approved local base ref, expected ancestry, local-only authority, and no concurrent writer.
2. Record pre-integration HEAD and create a recoverable local reference before the approved non-destructive merge or rebase mode.
3. Perform only the declared local integration; stop on conflicts and preserve index, worktree, refs, and exact recovery commands.
4. Record post-state, changed files, conflicts or success, before/after refs, and required host checks; never fetch, push, force, delete, or merge remotely.

## Domain Guidance

- On conflict, stop and preserve the state. Report each conflict as mechanical (version file, lockfile, changelog ordering) or semantic (code logic), with the recovery command, so the owner knows what the stop costs.

## Output Contract

Produce:
- integrated local branch or conflict state
- before and after ref evidence
- changed-file or conflict report
- exact recovery command

Every material action, command, result, finding, score, capture, provider receipt, or completion claim must bind to exact target identity and current evidence or be labeled assumption/unknown.

Deliver each output as the artifact itself (tables, commands, patches, plans, records), not as a description of how it would be produced.

## Coverage

- `local-only`
- `clean-worktree`
- `pre-integration-ref`
- `conflict-preservation`
- `recovery-command`
- `no-remote-write`

## Hard Gates

- Local integration requires an approved local base ref, clean isolated change branch, recoverable pre-integration identity, and zero fetch, push, force, remote merge, or branch deletion.
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
- `isolated-task-implementation`
- `local-git-guard-setup`
- `change-delivery-preflight`
- `remote-pull-request-change`

Never silently expand source, command, browser, data, credential, local-system, provider, or remote authority. Independent review, QA, audit, evidence acquisition, analysis, and triage never repair source. Setup and authentication never imply authority to perform the downstream action.
