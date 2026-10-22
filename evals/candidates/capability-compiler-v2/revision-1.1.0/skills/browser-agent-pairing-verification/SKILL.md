---
name: browser-agent-pairing-verification
description: "Verify and diagnose an existing browser-agent pairing through approved local checks and read-only external observation without creating credentials or changing configuration. Use when An existing browser-agent pairing must be checked for health, expiry and whether its scope matches what was approved; Someone asks why a paired agent cannot act, or whether a pairing is broader than intended. Do not use for: Create or renew the pairing credential and local configuration (-> browser-agent-pairing-provisioning); Configure target-origin authentication material in the browser profile (-> browser-authentication-setup)."
---

# Browser Agent Pairing Verification

## Responsibility

Verify and diagnose an existing browser-agent pairing through approved local checks and read-only external observation without creating credentials or changing configuration.

## Trigger

Use when the request matches any of:
- An existing browser-agent pairing must be checked for health, expiry and whether its scope matches what was approved
- Someone asks why a paired agent cannot act, or whether a pairing is broader than intended

Do not use when:
- Create or renew the pairing credential and local configuration. Route to `browser-agent-pairing-provisioning`.
- Configure target-origin authentication material in the browser profile. Route to `browser-authentication-setup`.

## Required Inputs

- Pairing identity, browser status, expected scope, target platform, and permitted external read boundary.

## Procedure

1. Freeze pairing identity, expected agent, transport, origins, actions, expiry, browser status, permitted external read, and prohibited changes.
2. Run approved health, connection, expiry, origin, and observed-scope checks without reading credential values.
3. Compare expected and observed identity and scope; classify disconnected, expired, mismatched, overbroad, healthy, or unverifiable.
4. Return evidence and a bounded re-provisioning recommendation; do not mint, renew, restart, widen, or edit configuration.

## Domain Guidance

- Diagnosis table: 'tab not owned by your agent' means the agent acted on a tab it did not create and must open its own tab; 'domain not allowed' means the token restricts domains and the pairing needs re-provisioning with the needed origin; an expired token needs renewal through the provisioning Skill.
- After the remote agent is told to connect, confirm the connection from the browser status output and report which agent and scope appear.

## Output Contract

Produce:
- pairing connection verdict
- expected-versus-observed scope
- diagnosis evidence
- bounded re-provisioning recommendation

Every material action, command, result, finding, score, capture, provider receipt, or completion claim must bind to exact target identity and current evidence or be labeled assumption/unknown.

Deliver each output as the artifact itself (tables, commands, patches, plans, records), not as a description of how it would be produced.

## Coverage

- `existing-pairing`
- `expected-observed-scope`
- `read-only-verification`
- `no-mint`
- `no-config-change`
- `no-data-authority`

## Hard Gates

- Verification authority is read-only: it cannot mint or renew credentials, restart the daemon, change config, widen scope, or treat connectivity as data-access authorization.
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

## External or Local-System Action Boundary

This Skill defines an action contract and does not execute the action by itself. Any real local-system, external-session, provider, publication, or remote write requires fresh per-action authorization, exact target and scope, preview, durable receipt, expiry or cleanup, and rollback, revocation, deletion, or cancellation terms as applicable.

## Status Mapping

- `passed`: the atomic output and every gate have current target-bound evidence.
- `needs-input`: a requestable scope, authority, target, fixture, governance term, or decision is absent. Deliver every supported part first and name the owner for the missing part.
- `blocked`: safe work requires prohibited access, unavailable authority, secret values, destructive or remote action, or an incompatible identity.
- `failed`: the authorized action ran but a deterministic check or required output failed.

## Non-Responsibilities

Adjacent capabilities:
- `browser-agent-pairing-provisioning`
- `browser-authentication-setup`
- `browser-data-acquisition-runtime`
- `tool-runtime-readiness`

Never silently expand source, command, browser, data, credential, local-system, provider, or remote authority. Independent review, QA, audit, evidence acquisition, analysis, and triage never repair source. Setup and authentication never imply authority to perform the downstream action.
