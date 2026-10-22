---
name: local-git-guard-setup
description: Install or configure one approved repository-local Git guard after classifying the hooks path, with consent, verification, backup, and uninstall instructions. Do not use for author or change the guard policy and fixtures in project source or integrate a base branch into a local change branch.
---

# Local Git Guard Setup

## Responsibility

Install or configure one approved repository-local Git guard after classifying the hooks path, with consent, verification, backup, and uninstall instructions.

## Trigger

Use when the requested outcome is: Install or configure one approved repository-local Git guard after classifying the hooks path, with consent, verification, backup, and uninstall instructions.

Do not use when:
- Author or change the guard policy and fixtures in project source. Route to `git-destructive-command-guard`.
- Integrate a base branch into a local change branch. Route to `local-branch-integration`.

## Required Inputs

- Repository Git-dir evidence, hooks-path classification, guard artifact, user consent, and local-system write authorization.

Also require exact target identity, authority, mutation boundary, evidence consumer, cleanup or rollback, and declared unknowns where applicable.

## Procedure

1. Verify repository Git-dir, current hooksPath and ownership, tracked or committed status, existing hooks, approved guard artifact hash, consent, local-system authority, backup, and uninstall plan.
2. Refuse committed, shared, custom, managed, or ambiguous hook paths unless an exact non-destructive plan is separately approved.
3. Back up affected local config or hook state, install only the approved artifact, and do not rename or overwrite unrelated hooks silently.
4. Verify safe and blocked fixtures in the installed path and record config, hash, exit, backup, restore, uninstall, or safe refusal.

## Output Contract

Produce:
- local guard installation receipt or refusal
- hooks-path classification
- installed verification evidence
- backup, restore, and uninstall instructions

Every material action, command, result, finding, score, capture, provider receipt, or completion claim must bind to exact target identity and current evidence or be labeled assumption/unknown.

## Coverage

- `hooks-path-classification`
- `explicit-consent`
- `no-committed-hook-change`
- `backup`
- `verification`
- `uninstall`

## Hard Gates

- Never silently enable a guard or modify a committed, shared, custom, or ambiguous hooks directory; explicit consent, backup, verification, and uninstall are mandatory.
- Preserve source, build, dataset, model, workflow, provider, browser, session, or local-system identity; command, version, exit, duration, artifacts, hashes, limitations, and cleanup must remain explicit when applicable.
- Return `needs-input` when a named owner can provide missing scope, authority, evidence, governance, target, or decision.
- Return `blocked` when proceeding would exceed mutation authority, expose credentials, violate governance, erase failed evidence, perform an undeclared remote or destructive action, or mix independent review with repair.

## Human Decision Authority

The Skill may return evidence, findings, options, and a recommendation. Scope approval, repair authorization, risk acceptance, publication, experiment submission, local-system change, remote action, and release disposition remain explicit human decisions under the declared identity.

## External or Local-System Action Boundary

This candidate defines an action contract but Phase 6 candidate construction and evaluation planning do not execute the action. Any real local-system, external-session, provider, publication, or remote write requires fresh per-action authorization, exact target and scope, preview, durable receipt, expiry or cleanup, and rollback, revocation, deletion, or cancellation terms as applicable.

## Status Mapping

- `passed`: the atomic output and every gate have current target-bound evidence.
- `needs-input`: a requestable scope, authority, target, fixture, governance term, or decision is absent.
- `blocked`: safe work requires prohibited access, unavailable authority, secret values, destructive or remote action, or an incompatible identity.
- `failed`: the authorized action ran but a deterministic check or required output failed.

## Non-Responsibilities

Does not absorb unrelated lifecycle responsibilities or expand provider, workspace, or remote-write authority implicitly.

Adjacent capabilities:
- `git-destructive-command-guard`
- `local-branch-integration`
- `tool-runtime-readiness`
- `workflow-runtime-upgrade`

Never silently expand source, command, browser, data, credential, local-system, provider, or remote authority. Independent review, QA, audit, evidence acquisition, analysis, and triage never repair source. Setup and authentication never imply authority to perform the downstream action.
