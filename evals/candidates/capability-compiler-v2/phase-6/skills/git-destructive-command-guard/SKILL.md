---
name: git-destructive-command-guard
description: Author and validate a repository-scoped guard policy that intercepts declared destructive Git command patterns before execution without installing it silently. Do not use for install the already-approved guard into the repository's local git configuration or integrate the approved base branch into the isolated local change branch.
---

# Git Destructive Command Guard

## Responsibility

Author and validate a repository-scoped guard policy that intercepts declared destructive Git command patterns before execution without installing it silently.

## Trigger

Use when the requested outcome is: Author and validate a repository-scoped guard policy that intercepts declared destructive Git command patterns before execution without installing it silently.

Do not use when:
- Install the already-approved guard into the repository's local Git configuration. Route to `local-git-guard-setup`.
- Integrate the approved base branch into the isolated local change branch. Route to `local-branch-integration`.

## Required Inputs

- A command hook environment, dangerous-command policy, and local configuration.

Also require exact target identity, authority, mutation boundary, evidence consumer, cleanup or rollback, and declared unknowns where applicable.

## Procedure

1. Freeze the dangerous-command policy, shell or hook environment, repository artifact boundary, bypass rules, user-confirmation behavior, and installation owner.
2. Represent exact and equivalent destructive forms without intercepting ordinary status, diff, add, commit, fetch, or safe restore use.
3. Write only the authorized guard source, configuration template, and deterministic allow/block fixtures in the workspace.
4. Run approved fixture checks and return the candidate guard; require a separate local-system setup capability for installation or enablement.

## Output Contract

Produce:
- guard policy source
- allow and block fixture corpus
- local validation evidence
- separate installation handoff

Every material action, command, result, finding, score, capture, provider receipt, or completion claim must bind to exact target identity and current evidence or be labeled assumption/unknown.

## Coverage

- `destructive-patterns`
- `safe-command-pass`
- `repository-artifact`
- `no-silent-install`
- `separate-local-setup`

## Hard Gates

- Guard authoring may create tested repository artifacts but cannot modify Git config, hook paths, aliases, shell startup, or enable interception without separate local-system authorization.
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
- `local-git-guard-setup`
- `local-branch-integration`
- `change-scope-freeze`
- `tool-runtime-readiness`

Never silently expand source, command, browser, data, credential, local-system, provider, or remote authority. Independent review, QA, audit, evidence acquisition, analysis, and triage never repair source. Setup and authentication never imply authority to perform the downstream action.
