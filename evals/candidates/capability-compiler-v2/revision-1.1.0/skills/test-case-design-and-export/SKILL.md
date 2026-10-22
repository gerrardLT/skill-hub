---
name: test-case-design-and-export
description: "Derive traceable executable test cases, risk priority, data needs, coverage gaps, and one consumer-specific export from approved requirements without implementing tests. Use when Approved requirements must become traceable test cases with priority, data and expected results in a consumer-ready format; Someone asks which boundary, invalid and permission cases are missing and how good the case set is. Do not use for: Choose the overall test-layer portfolio and ownership strategy (-> testing-portfolio-strategy); Implement the selected cases in Playwright (-> playwright-test-engineering)."
---

# Test Case Design And Export

## Responsibility

Derive traceable executable test cases, risk priority, data needs, coverage gaps, and one consumer-specific export from approved requirements without implementing tests.

## Trigger

Use when the request matches any of:
- Approved requirements must become traceable test cases with priority, data and expected results in a consumer-ready format
- Someone asks which boundary, invalid and permission cases are missing and how good the case set is

Do not use when:
- Choose the overall test-layer portfolio and ownership strategy. Route to `testing-portfolio-strategy`.
- Implement the selected cases in Playwright. Route to `playwright-test-engineering`.

## Required Inputs

- Approved requirements, risk profile, platform, test level, data constraints, and downstream format.

## Procedure

1. Freeze requirement and design versions, risks, platform, test level, data governance, downstream schema, and stable case IDs.
2. Derive normal, boundary, invalid, permission, concurrency, interruption, error, recovery, migration, and accessibility cases as applicable.
3. Define preconditions, data, steps, expected observable results, priority, layer, automation suitability, and traceability for each case.
4. Score coverage and gaps, validate the export structure, and write only the approved artifact format; do not install dependencies or implement tests.

## Domain Guidance

- Case-set quality, five dimensions: coverage of requirement points, executability, independence, maintainability, completeness of test types. Report each as a count (for example 14 of 16 requirement points covered) with the uncovered items listed. Do not print a bare numeric score that is not derived from counted items.
- Cover every boundary value on both sides and just beyond (for example 20, 21 and 22 days), plus explicit rounding-midpoint cases and the order of discount and rounding. When a requirement is ambiguous at a boundary, add a blocked case that names the open question rather than assuming an answer; also ask about edge bands (for example the top age band) and about states such as resolved or closed items. Map one synthetic data record to each case and export every case, stating the count exported versus designed; do not assume a currency the requirements did not state.

## Output Contract

Produce:
- traceable prioritized test cases
- coverage and gap matrix
- governed test-data plan
- validated consumer-specific export
- five-dimension case quality score in the coverage matrix
- per-case synthetic data mapping

Every material action, command, result, finding, score, capture, provider receipt, or completion claim must bind to exact target identity and current evidence or be labeled assumption/unknown.

Deliver each output as the artifact itself (tables, commands, patches, plans, records), not as a description of how it would be produced.

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

## Status Mapping

- `passed`: the atomic output and every gate have current target-bound evidence.
- `needs-input`: a requestable scope, authority, target, fixture, governance term, or decision is absent. Deliver every supported part first and name the owner for the missing part.
- `blocked`: safe work requires prohibited access, unavailable authority, secret values, destructive or remote action, or an incompatible identity.
- `failed`: the authorized action ran but a deterministic check or required output failed.

## Non-Responsibilities

Adjacent capabilities:
- `testing-portfolio-strategy`
- `playwright-test-engineering`
- `vitest-tooling`
- `requirements-and-delivery-contract`

Never silently expand source, command, browser, data, credential, local-system, provider, or remote authority. Independent review, QA, audit, evidence acquisition, analysis, and triage never repair source. Setup and authentication never imply authority to perform the downstream action.
