---
name: browser-agent-pairing-provisioning
description: Provision one scoped expiring browser-agent pairing identity after explicit local-system, credential, and network-exposure authorization, with revocation and cleanup. Do not use for verify an existing pairing's connection and observed scope without changing it or configure browser authentication material for a target origin locally.
---

# Browser Agent Pairing Provisioning

## Responsibility

Provision one scoped expiring browser-agent pairing identity after explicit local-system, credential, and network-exposure authorization, with revocation and cleanup.

## Trigger

Use when the requested outcome is: Provision one scoped expiring browser-agent pairing identity after explicit local-system, credential, and network-exposure authorization, with revocation and cleanup.

Do not use when:
- Verify an existing pairing's connection and observed scope without changing it. Route to `browser-agent-pairing-verification`.
- Configure browser authentication material for a target origin locally. Route to `browser-authentication-setup`.

## Required Inputs

- Running browser daemon, selected agent, local or remote mode, scope restrictions, credential retention, and explicit authorization.

Also require exact target identity, authority, mutation boundary, evidence consumer, cleanup or rollback, and declared unknowns where applicable.

## Procedure

1. Verify daemon identity and health, selected agent, local or remote mode, origins and actions, network exposure, credential owner, expiry, retention, revocation, cleanup, and per-action authorization.
2. Preview exact listening interface, transport, credential storage, scope, lifetime, and exposure; refuse wildcard or indefinite access by default.
3. Perform only the approved pairing and local receipt update without revealing credential values in output or evidence.
4. Record non-secret pairing identity, scope, expiry, connection instructions, storage boundary, revocation command, exposure, and cleanup status.

## Output Contract

Produce:
- scoped pairing identity
- non-secret local configuration receipt
- expiry and revocation instructions
- network exposure and cleanup evidence

Every material action, command, result, finding, score, capture, provider receipt, or completion claim must bind to exact target identity and current evidence or be labeled assumption/unknown.

## Coverage

- `per-action-authorization`
- `scoped-agent`
- `origin-action-scope`
- `expiry`
- `revocation`
- `network-exposure`
- `no-secret-output`

## Hard Gates

- Pairing requires per-action authorization for exact agent, origins, actions, transport, exposure, and expiry; wildcard, hidden, reusable, or non-revocable credentials are blocked.
- Preserve source, build, dataset, model, workflow, provider, browser, session, or local-system identity; command, version, exit, duration, artifacts, hashes, limitations, and cleanup must remain explicit when applicable.
- Return `needs-input` when a named owner can provide missing scope, authority, evidence, governance, target, or decision.
- Return `blocked` when proceeding would exceed mutation authority, expose credentials, violate governance, erase failed evidence, perform an undeclared remote or destructive action, or mix independent review with repair.

## Data and Credential Governance

For customer, proprietary, browser, evaluation, experiment, or externally transferred data, require authority, minimization, redaction, retention, access, transfer, deletion, and incident boundaries. Credential and secret values never enter prompts, logs, hashes, receipts, or artifacts. Missing governance returns `needs-input`; prohibited or unavailable authority returns `blocked`.

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
- `browser-agent-pairing-verification`
- `browser-authentication-setup`
- `browser-session-and-runtime-configuration`
- `provider-cli-authentication-setup`

Never silently expand source, command, browser, data, credential, local-system, provider, or remote authority. Independent review, QA, audit, evidence acquisition, analysis, and triage never repair source. Setup and authentication never imply authority to perform the downstream action.
