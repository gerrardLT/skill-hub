---
name: test-case-design-and-export
description: Derive traceable executable test cases, risk priority, data needs, coverage gaps, and one consumer-specific export from approved requirements without implementing tests. Do not use for choose the overall test-layer portfolio and ownership strategy or implement the selected cases in playwright.
---

# Test Case Design And Export

## Responsibility

Derive traceable executable test cases, risk priority, data needs, coverage gaps, and one consumer-specific export from approved requirements without implementing tests.

## Trigger

Use when the requested outcome is: Derive traceable executable test cases, risk priority, data needs, coverage gaps, and one consumer-specific export from approved requirements without implementing tests.

Do not use when:
- Choose the overall test-layer portfolio and ownership strategy. Route to `testing-portfolio-strategy`.
- Implement the selected cases in Playwright. Route to `playwright-test-engineering`.

## Required Inputs

- Approved requirements, risk profile, platform, test level, data constraints, and downstream format.

Also require exact target identity, authority, mutation boundary, evidence consumer, cleanup or rollback, and declared unknowns where applicable.

## Procedure

1. Freeze requirement and design versions, risks, platform, test level, data governance, downstream schema, and stable case IDs.
2. Derive normal, boundary, invalid, permission, concurrency, interruption, error, recovery, migration, and accessibility cases as applicable.
3. Define preconditions, data, steps, expected observable results, priority, layer, automation suitability, and traceability for each case.
4. Score coverage and gaps, validate the export structure, and write only the approved artifact format; do not install dependencies or implement tests.

## Output Contract

Produce:
- traceable prioritized test cases
- coverage and gap matrix
- governed test-data plan
- validated consumer-specific export

Every material action, command, result, finding, score, capture, provider receipt, or completion claim must bind to exact target identity and current evidence or be labeled assumption/unknown.

## Coverage

- `stable-case-id`
- `requirement-traceability`
- `preconditions`
- `test-data`
- `observable-result`
- `priority`
- `coverage-gap`

## Hard Gates

- Every test case must trace to approved behavior or risk and state preconditions, data, action, observable expected result, priority, and test level; exported volume cannot substitute for coverage quality.
- Preserve source, build, dataset, model, workflow, provider, browser, session, or local-system identity; command, version, exit, duration, artifacts, hashes, limitations, and cleanup must remain explicit when applicable.
- Return `needs-input` when a named owner can provide missing scope, authority, evidence, governance, target, or decision.
- Return `blocked` when proceeding would exceed mutation authority, expose credentials, violate governance, erase failed evidence, perform an undeclared remote or destructive action, or mix independent review with repair.

## Data and Credential Governance

For customer, proprietary, browser, evaluation, experiment, or externally transferred data, require authority, minimization, redaction, retention, access, transfer, deletion, and incident boundaries. Credential and secret values never enter prompts, logs, hashes, receipts, or artifacts. Missing governance returns `needs-input`; prohibited or unavailable authority returns `blocked`.

## Status Mapping

- `passed`: the atomic output and every gate have current target-bound evidence.
- `needs-input`: a requestable scope, authority, target, fixture, governance term, or decision is absent.
- `blocked`: safe work requires prohibited access, unavailable authority, secret values, destructive or remote action, or an incompatible identity.
- `failed`: the authorized action ran but a deterministic check or required output failed.

## Non-Responsibilities

Does not absorb unrelated lifecycle responsibilities or expand provider, workspace, or remote-write authority implicitly.

Adjacent capabilities:
- `testing-portfolio-strategy`
- `playwright-test-engineering`
- `vitest-tooling`
- `requirements-and-delivery-contract`

Never silently expand source, command, browser, data, credential, local-system, provider, or remote authority. Independent review, QA, audit, evidence acquisition, analysis, and triage never repair source. Setup and authentication never imply authority to perform the downstream action.
