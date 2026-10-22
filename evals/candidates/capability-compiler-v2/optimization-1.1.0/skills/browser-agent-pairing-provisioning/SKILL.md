---
name: browser-agent-pairing-provisioning
description: "Provision one scoped expiring browser-agent pairing identity after explicit local-system, credential, and network-exposure authorization, with revocation and cleanup. Use when Another AI agent needs scoped, expiring access to a local browser session and someone must set up the pairing; Someone asks what a pairing would expose, for how long and how to revoke it. Do not use for: Verify an existing pairing's connection and observed scope without changing it (-> browser-agent-pairing-verification); Configure browser authentication material for a target origin locally (-> browser-authentication-setup)."
---

# Browser Agent Pairing Provisioning

## Responsibility

Provision one scoped expiring browser-agent pairing identity after explicit local-system, credential, and network-exposure authorization, with revocation and cleanup.

## Trigger

Use when the request matches any of:
- Another AI agent needs scoped, expiring access to a local browser session and someone must set up the pairing
- Someone asks what a pairing would expose, for how long and how to revoke it

Do not use when:
- Verify an existing pairing's connection and observed scope without changing it. Route to `browser-agent-pairing-verification`.
- Configure browser authentication material for a target origin locally. Route to `browser-authentication-setup`.

## Required Inputs

- Running browser daemon, selected agent, local or remote mode, scope restrictions, credential retention, and explicit authorization.

## Procedure

1. Verify daemon identity and health, selected agent, local or remote mode, origins and actions, network exposure, credential owner, expiry, retention, revocation, cleanup, and per-action authorization.
2. State whether the pairing relaunches the browser daemon and what open tabs, cookies and sessions would be lost; require explicit consent for that loss.
3. Preview exact listening interface, transport, credential storage, scope, lifetime, and exposure; refuse wildcard or indefinite access by default.
4. Perform only the approved pairing and local receipt update without revealing credential values in output or evidence.
5. Record non-secret pairing identity, scope, expiry, connection instructions, storage boundary, revocation command, exposure, and cleanup status.

## Domain Guidance

- Preview the session-loss consequence before anything runs: pairing can relaunch the browser daemon, and a relaunch kills open tabs, cookies and logged-in sessions. Require explicit consent for a relaunch as a one-way action, and offer a pairing path that does not relaunch when one exists.
- Treat daemon relaunch and session loss as conditional provider behavior: claim it only when supplied or observed for the exact pairing path. Otherwise mark relaunch, tabs, cookies and login-session impact unknown and request provider evidence before consent.
- Do not import relaunch/session-loss rules from other browser pairing providers. Apply them only when the exact provider path supplies or verifies that behavior. Keep revocation command semantics separate from verified credential-file deletion; a --wipe flag does not prove deletion.

## Output Contract

Produce:
- scoped pairing identity
- non-secret local configuration receipt
- expiry and revocation instructions
- network exposure and cleanup evidence

Every material action, command, result, finding, score, capture, provider receipt, or completion claim must bind to exact target identity and current evidence or be labeled assumption/unknown.

Deliver each output as the artifact itself (tables, commands, patches, plans, records), not as a description of how it would be produced.

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

## Data and Credential Governance

For customer, proprietary, browser, evaluation, experiment, or externally transferred data, require authority, minimization, redaction, retention, access, transfer, deletion, and incident boundaries. Credential and secret values never enter prompts, logs, hashes, receipts, or artifacts. Missing governance returns `needs-input`; prohibited or unavailable authority returns `blocked`.

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
- `browser-agent-pairing-verification`
- `browser-authentication-setup`
- `browser-session-and-runtime-configuration`
- `provider-cli-authentication-setup`

Never silently expand source, command, browser, data, credential, local-system, provider, or remote authority. Independent review, QA, audit, evidence acquisition, analysis, and triage never repair source. Setup and authentication never imply authority to perform the downstream action.
