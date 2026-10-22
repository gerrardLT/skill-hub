---
name: browser-agent-pairing-verification
description: Verify and diagnose an existing browser-agent pairing through approved local checks and read-only external observation without creating credentials or changing configuration. Do not use for create or renew the pairing credential and local configuration or configure target-origin authentication material in the browser profile.
---

# Browser Agent Pairing Verification

## Responsibility

Verify and diagnose an existing browser-agent pairing through approved local checks and read-only external observation without creating credentials or changing configuration.

## Trigger

Use when the requested outcome is: Verify and diagnose an existing browser-agent pairing through approved local checks and read-only external observation without creating credentials or changing configuration.

Do not use when:
- Create or renew the pairing credential and local configuration. Route to `browser-agent-pairing-provisioning`.
- Configure target-origin authentication material in the browser profile. Route to `browser-authentication-setup`.

## Required Inputs

- Pairing identity, browser status, expected scope, target platform, and permitted external read boundary.

Also require exact target identity, authority, mutation boundary, evidence consumer, cleanup or rollback, and declared unknowns where applicable.

## Procedure

1. Freeze pairing identity, expected agent, transport, origins, actions, expiry, browser status, permitted external read, and prohibited changes.
2. Run approved health, connection, expiry, origin, and observed-scope checks without reading credential values.
3. Compare expected and observed identity and scope; classify disconnected, expired, mismatched, overbroad, healthy, or unverifiable.
4. Return evidence and a bounded re-provisioning recommendation; do not mint, renew, restart, widen, or edit configuration.

## Output Contract

Produce:
- pairing connection verdict
- expected-versus-observed scope
- diagnosis evidence
- bounded re-provisioning recommendation

Every material action, command, result, finding, score, capture, provider receipt, or completion claim must bind to exact target identity and current evidence or be labeled assumption/unknown.

## Coverage

- `existing-pairing`
- `expected-observed-scope`
- `read-only-verification`
- `no-mint`
- `no-config-change`
- `no-data-authority`

## Hard Gates

- Verification authority is read-only: it cannot mint or renew credentials, restart the daemon, change config, widen scope, or treat connectivity as data-access authorization.
- Preserve source, build, dataset, model, workflow, provider, browser, session, or local-system identity; command, version, exit, duration, artifacts, hashes, limitations, and cleanup must remain explicit when applicable.
- Return `needs-input` when a named owner can provide missing scope, authority, evidence, governance, target, or decision.
- Return `blocked` when proceeding would exceed mutation authority, expose credentials, violate governance, erase failed evidence, perform an undeclared remote or destructive action, or mix independent review with repair.

## Data and Credential Governance

For customer, proprietary, browser, evaluation, experiment, or externally transferred data, require authority, minimization, redaction, retention, access, transfer, deletion, and incident boundaries. Credential and secret values never enter prompts, logs, hashes, receipts, or artifacts. Missing governance returns `needs-input`; prohibited or unavailable authority returns `blocked`.

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
- `browser-agent-pairing-provisioning`
- `browser-authentication-setup`
- `browser-data-acquisition-runtime`
- `tool-runtime-readiness`

Never silently expand source, command, browser, data, credential, local-system, provider, or remote authority. Independent review, QA, audit, evidence acquisition, analysis, and triage never repair source. Setup and authentication never imply authority to perform the downstream action.
