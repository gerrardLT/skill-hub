---
name: workflow-runtime-upgrade
description: "Upgrade one installed workflow runtime under explicit local-system authorization with version detection, backup, compatibility checks, rollback, and no hidden credential or provider changes. Use when One installed workflow runtime must be upgraded to a pinned version with backup and rollback; Someone asks what an upgrade would change and how to verify the new version is actually the one running. Do not use for: Verify whether the current runtime is already ready without changing it (-> tool-runtime-readiness); Install or authenticate a provider CLI and external session (-> provider-cli-authentication-setup)."
---

# Workflow Runtime Upgrade

## Responsibility

Upgrade one installed workflow runtime under explicit local-system authorization with version detection, backup, compatibility checks, rollback, and no hidden credential or provider changes.

## Trigger

Use when the request matches any of:
- One installed workflow runtime must be upgraded to a pinned version with backup and rollback
- Someone asks what an upgrade would change and how to verify the new version is actually the one running

Do not use when:
- Verify whether the current runtime is already ready without changing it. Route to `tool-runtime-readiness`.
- Install or authenticate a provider CLI and external session. Route to `provider-cli-authentication-setup`.

## Required Inputs

- Installed runtime, target version, local-system write authorization, compatibility constraints, and rollback path.

## Procedure

1. Verify installed runtime identity and version, source, target version and integrity, compatibility, local-system authority, files and services affected, configuration, data migration, backup, rollback, and downtime.
2. Preview exact commands, package or binary source, changes, migrations, restarts, and credential boundaries; refuse unpinned or untrusted updates.
3. Stop any process started before the upgrade and handle a vendored copy, then restart and verify the version the new process reports.
4. Back up state, perform only the approved upgrade through the host, stop on migration or verification failure, and avoid provider login or unrelated global changes.
5. Run version and compatibility checks, record before and after identity, commands, exits, duration, changed paths, health, rollback test or instructions, and cleanup.

## Domain Guidance

- After the upgrade, stop any running daemon or background process that was started before it: a running process keeps serving the old binary and will make a health check pass against stale code. Then start fresh and verify the version it reports.
- Handle a local vendored copy of the runtime in the project explicitly: detect it, upgrade or report it separately, and note whether team mode requires the two to match.

## Output Contract

Produce:
- runtime upgrade receipt
- before and after version evidence
- compatibility and health checks
- backup, rollback, and cleanup record

Every material action, command, result, finding, score, capture, provider receipt, or completion claim must bind to exact target identity and current evidence or be labeled assumption/unknown.

Deliver each output as the artifact itself (tables, commands, patches, plans, records), not as a description of how it would be produced.

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

## External or Local-System Action Boundary

This Skill defines an action contract and does not execute the action by itself. Any real local-system, external-session, provider, publication, or remote write requires fresh per-action authorization, exact target and scope, preview, durable receipt, expiry or cleanup, and rollback, revocation, deletion, or cancellation terms as applicable.

## Status Mapping

- `passed`: the atomic output and every gate have current target-bound evidence.
- `needs-input`: a requestable scope, authority, target, fixture, governance term, or decision is absent. Deliver every supported part first and name the owner for the missing part.
- `blocked`: safe work requires prohibited access, unavailable authority, secret values, destructive or remote action, or an incompatible identity.
- `failed`: the authorized action ran but a deterministic check or required output failed.

## Non-Responsibilities

Adjacent capabilities:
- `tool-runtime-readiness`
- `provider-cli-authentication-setup`
- `local-agent-memory-setup`
- `test-runtime-bootstrap`

Never silently expand source, command, browser, data, credential, local-system, provider, or remote authority. Independent review, QA, audit, evidence acquisition, analysis, and triage never repair source. Setup and authentication never imply authority to perform the downstream action.
