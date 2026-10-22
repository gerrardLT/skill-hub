---
name: browser-data-acquisition-runtime
description: "Acquire only authorized page evidence or structured data through an approved read-only browser session, preserving provenance, limits, and cleanup. Use when Authorized page evidence or structured fields must be captured read-only through an existing browser session; Someone asks for data from a logged-in page with provenance, limits and a deletion deadline. Do not use for: Configure authentication material in the local browser profile first (-> browser-authentication-setup); Perform a narrow unauthenticated public-page probe with no governed data extraction (-> safe-browser-probing)."
---

# Browser Data Acquisition Runtime

## Responsibility

Acquire only authorized page evidence or structured data through an approved read-only browser session, preserving provenance, limits, and cleanup.

## Trigger

Use when the request matches any of:
- Authorized page evidence or structured fields must be captured read-only through an existing browser session
- Someone asks for data from a logged-in page with provenance, limits and a deletion deadline

Do not use when:
- Configure authentication material in the local browser profile first. Route to `browser-authentication-setup`.
- Perform a narrow unauthenticated public-page probe with no governed data extraction. Route to `safe-browser-probing`.

## Required Inputs

- Target URL, authentication authority, data-governance boundary, browser runtime, and extraction scope.

## Procedure

1. Verify exact URLs and origins, authentication authority, data purpose, fields, minimization, consent or rights, external-transfer, retention, deletion, rate, session, and prohibited actions.
2. Use the approved existing runtime and read-only navigation or extraction; refuse forms, purchases, messages, account changes, deletes, privilege changes, or anti-access-control bypass.
3. Capture only declared fields or evidence and record route, timestamp, state, browser, session identity, request or selector, count, truncation, and source provenance without credential values.
4. Return captured artifact or structured data, access limitations, cleanup, deletion deadline, and blocked gaps; acquired data is not automatically authorized for reuse.

## Domain Guidance

- If the task invites a consequential action (submitting a form, buying, messaging, changing an account), refuse that part, say why, and continue with the read-only capture that is in scope.

## Output Contract

Produce:
- captured evidence or structured data
- route and field provenance
- access and reuse limits
- cleanup and deletion status

Every material action, command, result, finding, score, capture, provider receipt, or completion claim must bind to exact target identity and current evidence or be labeled assumption/unknown.

Deliver each output as the artifact itself (tables, commands, patches, plans, records), not as a description of how it would be produced.

## Coverage

- `authorized-origin`
- `authorized-fields`
- `purpose-limitation`
- `read-only`
- `provenance`
- `reuse-boundary`
- `cleanup-deletion`

## Hard Gates

- A valid login does not authorize acquisition or reuse: each origin, field, purpose, action, transfer, retention, and deletion boundary must be explicit, and all acquisition remains read-only.
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
- `browser-authentication-setup`
- `safe-browser-probing`
- `browser-session-and-runtime-configuration`
- `website-audit-assessment`

Never silently expand source, command, browser, data, credential, local-system, provider, or remote authority. Independent review, QA, audit, evidence acquisition, analysis, and triage never repair source. Setup and authentication never imply authority to perform the downstream action.
