---
name: browser-authentication-setup
description: "Configure authorized authentication state in one local browser profile for exact origins without exposing values or granting unrelated browsing authority. Use when A browser profile needs logged-in state for one exact origin so later read-only acquisition can proceed; Someone asks to import or configure authentication for a site without exposing credential values. Do not use for: Acquire governed page data using an already-authenticated browser session (-> browser-data-acquisition-runtime); Provision credentials that pair an external agent with the browser (-> browser-agent-pairing-provisioning)."
---

# Browser Authentication Setup

## Responsibility

Configure authorized authentication state in one local browser profile for exact origins without exposing values or granting unrelated browsing authority.

## Trigger

Use when the request matches any of:
- A browser profile needs logged-in state for one exact origin so later read-only acquisition can proceed
- Someone asks to import or configure authentication for a site without exposing credential values

Do not use when:
- Acquire governed page data using an already-authenticated browser session. Route to `browser-data-acquisition-runtime`.
- Provision credentials that pair an external agent with the browser. Route to `browser-agent-pairing-provisioning`.

## Required Inputs

- Browser profile, target origin, credential authority, local-system write authorization, retention, and deletion policy.

## Procedure

1. Check whether the runtime is already attached to the user's authenticated browser; if so return a no-write outcome.
2. Verify browser profile, exact origins, credential owner, authentication method, local-system authorization, storage, retention, expiry, deletion, allowed validation, and prohibited output.
3. Back up or identify reversible profile state and preview exact files or browser stores affected without reading values into model context.
4. Perform only the approved local setup through the host, using native secure storage where available and never logging or persisting credential values in evidence.
5. Validate non-secret authentication status for the exact origin and record storage boundary, expiry, cleanup, rollback, and failure evidence.

## Domain Guidance

- First check whether the runtime is already attached to the user's real, already authenticated browser. If so, return a no-write outcome stating that no import is needed, and do not copy any cookies.

## Output Contract

Produce:
- configured local authentication state
- non-secret validation receipt
- storage and origin boundary
- expiry, cleanup, and rollback instructions

Every material action, command, result, finding, score, capture, provider receipt, or completion claim must bind to exact target identity and current evidence or be labeled assumption/unknown.

Deliver each output as the artifact itself (tables, commands, patches, plans, records), not as a description of how it would be produced.

## Coverage

- `exact-origin`
- `secure-storage`
- `no-credential-output`
- `non-secret-validation`
- `expiry`
- `cleanup`
- `no-data-authority`

## Hard Gates

- Authentication setup grants neither page-data authority nor general browsing scope; credential values never enter prompts, logs, hashes, receipts, or artifacts.
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
- `browser-data-acquisition-runtime`
- `browser-agent-pairing-provisioning`
- `browser-session-and-runtime-configuration`
- `secrets-and-environment-governance`

Never silently expand source, command, browser, data, credential, local-system, provider, or remote authority. Independent review, QA, audit, evidence acquisition, analysis, and triage never repair source. Setup and authentication never imply authority to perform the downstream action.
