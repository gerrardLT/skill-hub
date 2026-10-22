---
name: safe-browser-probing
description: "Run a bounded unauthenticated or already-authorized browser probe for one declared question and capture non-destructive evidence without source or session mutation. Use when One question about a page must be answered by a short, non-destructive browser session with captured evidence; Someone asks what a public page shows at a viewport, or whether a specific element renders, without logging in or changing state. Do not use for: Acquire authenticated page data using a governed browser session (-> browser-data-acquisition-runtime); Build maintainable Playwright test artifacts for repeated regression use (-> playwright-test-engineering)."
---

# Safe Browser Probing

## Responsibility

Run a bounded unauthenticated or already-authorized browser probe for one declared question and capture non-destructive evidence without source or session mutation.

## Trigger

Use when the request matches any of:
- One question about a page must be answered by a short, non-destructive browser session with captured evidence
- Someone asks what a public page shows at a viewport, or whether a specific element renders, without logging in or changing state

Do not use when:
- Acquire authenticated page data using a governed browser session. Route to `browser-data-acquisition-runtime`.
- Build maintainable Playwright test artifacts for repeated regression use. Route to `playwright-test-engineering`.

## Required Inputs

- A target page, authorized interactions, and a ready browser runtime.

## Procedure

1. Freeze URL, question, allowed origin, browser runtime, viewport, authentication state, prohibited actions, data boundary, and capture plan.
2. Navigate only approved origins and perform read-only or explicitly reversible interactions; never submit destructive, purchase, publish, account, or privilege-changing actions.
3. Record route, timestamp, viewport, browser version, requests or console evidence where authorized, screenshot or trace, and cleanup.
4. Return observed evidence and limits; do not generalize one probe into a full audit or persistent test.

## Output Contract

Produce:
- bounded browser probe record
- screenshot or trace evidence
- origin and action log
- cleanup and limitation report

Every material action, command, result, finding, score, capture, provider receipt, or completion claim must bind to exact target identity and current evidence or be labeled assumption/unknown.

Deliver each output as the artifact itself (tables, commands, patches, plans, records), not as a description of how it would be produced.

## Coverage

- `one-question`
- `allowlisted-origin`
- `non-destructive`
- `no-credentials`
- `capture-provenance`
- `cleanup`

## Hard Gates

- A safe probe has one declared question, allowlisted origins and actions, no credential or destructive state change, and complete capture provenance and cleanup.
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

## Status Mapping

- `passed`: the atomic output and every gate have current target-bound evidence.
- `needs-input`: a requestable scope, authority, target, fixture, governance term, or decision is absent. Deliver every supported part first and name the owner for the missing part.
- `blocked`: safe work requires prohibited access, unavailable authority, secret values, destructive or remote action, or an incompatible identity.
- `failed`: the authorized action ran but a deterministic check or required output failed.

## Non-Responsibilities

Adjacent capabilities:
- `browser-data-acquisition-runtime`
- `playwright-test-engineering`
- `website-audit-assessment`
- `ui-review-scope-and-evidence-acquisition`

Never silently expand source, command, browser, data, credential, local-system, provider, or remote authority. Independent review, QA, audit, evidence acquisition, analysis, and triage never repair source. Setup and authentication never imply authority to perform the downstream action.
