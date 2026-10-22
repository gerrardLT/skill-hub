---
name: browser-data-acquisition-runtime
description: Acquire only authorized page evidence or structured data through an approved read-only browser session, preserving provenance, limits, and cleanup. Do not use for configure authentication material in the local browser profile first or perform a narrow unauthenticated public-page probe with no governed data extraction.
---

# Browser Data Acquisition Runtime

## Responsibility

Acquire only authorized page evidence or structured data through an approved read-only browser session, preserving provenance, limits, and cleanup.

## Trigger

Use when the requested outcome is: Acquire only authorized page evidence or structured data through an approved read-only browser session, preserving provenance, limits, and cleanup.

Do not use when:
- Configure authentication material in the local browser profile first. Route to `browser-authentication-setup`.
- Perform a narrow unauthenticated public-page probe with no governed data extraction. Route to `safe-browser-probing`.

## Required Inputs

- Target URL, authentication authority, data-governance boundary, browser runtime, and extraction scope.

Also require exact target identity, authority, mutation boundary, evidence consumer, cleanup or rollback, and declared unknowns where applicable.

## Procedure

1. Verify exact URLs and origins, authentication authority, data purpose, fields, minimization, consent or rights, external-transfer, retention, deletion, rate, session, and prohibited actions.
2. Use the approved existing runtime and read-only navigation or extraction; refuse forms, purchases, messages, account changes, deletes, privilege changes, or anti-access-control bypass.
3. Capture only declared fields or evidence and record route, timestamp, state, browser, session identity, request or selector, count, truncation, and source provenance without credential values.
4. Return captured artifact or structured data, access limitations, cleanup, deletion deadline, and blocked gaps; acquired data is not automatically authorized for reuse.

## Output Contract

Produce:
- captured evidence or structured data
- route and field provenance
- access and reuse limits
- cleanup and deletion status

Every material action, command, result, finding, score, capture, provider receipt, or completion claim must bind to exact target identity and current evidence or be labeled assumption/unknown.

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
- `browser-authentication-setup`
- `safe-browser-probing`
- `browser-session-and-runtime-configuration`
- `website-audit-assessment`

Never silently expand source, command, browser, data, credential, local-system, provider, or remote authority. Independent review, QA, audit, evidence acquisition, analysis, and triage never repair source. Setup and authentication never imply authority to perform the downstream action.
