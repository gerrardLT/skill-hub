---
name: workflow-runtime-upgrade
description: Upgrade one installed workflow runtime under explicit local-system authorization with version detection, backup, compatibility checks, rollback, and no hidden credential or provider changes. Do not use for verify whether the current runtime is already ready without changing it or install or authenticate a provider cli and external session.
---

# Workflow Runtime Upgrade

## Responsibility

Upgrade one installed workflow runtime under explicit local-system authorization with version detection, backup, compatibility checks, rollback, and no hidden credential or provider changes.

## Trigger

Use when the requested outcome is: Upgrade one installed workflow runtime under explicit local-system authorization with version detection, backup, compatibility checks, rollback, and no hidden credential or provider changes.

Do not use when:
- Verify whether the current runtime is already ready without changing it. Route to `tool-runtime-readiness`.
- Install or authenticate a provider CLI and external session. Route to `provider-cli-authentication-setup`.

## Required Inputs

- Installed runtime, target version, local-system write authorization, compatibility constraints, and rollback path.

Also require exact target identity, authority, mutation boundary, evidence consumer, cleanup or rollback, and declared unknowns where applicable.

## Procedure

1. Verify installed runtime identity and version, source, target version and integrity, compatibility, local-system authority, files and services affected, configuration, data migration, backup, rollback, and downtime.
2. Preview exact commands, package or binary source, changes, migrations, restarts, and credential boundaries; refuse unpinned or untrusted updates.
3. Back up state, perform only the approved upgrade through the host, stop on migration or verification failure, and avoid provider login or unrelated global changes.
4. Run version and compatibility checks, record before and after identity, commands, exits, duration, changed paths, health, rollback test or instructions, and cleanup.

## Output Contract

Produce:
- runtime upgrade receipt
- before and after version evidence
- compatibility and health checks
- backup, rollback, and cleanup record

Every material action, command, result, finding, score, capture, provider receipt, or completion claim must bind to exact target identity and current evidence or be labeled assumption/unknown.

## Coverage

- `detected-version`
- `pinned-target`
- `trusted-source`
- `compatibility`
- `backup`
- `rollback`
- `health-check`

## Hard Gates

- A runtime upgrade requires a pinned trusted target, explicit affected paths, compatibility and migration plan, backup, rollback, and current post-upgrade health evidence; unpinned latest upgrades fail closed.
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
- `tool-runtime-readiness`
- `provider-cli-authentication-setup`
- `local-agent-memory-setup`
- `test-runtime-bootstrap`

Never silently expand source, command, browser, data, credential, local-system, provider, or remote authority. Independent review, QA, audit, evidence acquisition, analysis, and triage never repair source. Setup and authentication never imply authority to perform the downstream action.
