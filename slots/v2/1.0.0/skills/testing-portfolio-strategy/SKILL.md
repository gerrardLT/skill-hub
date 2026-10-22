---
name: testing-portfolio-strategy
description: Design a risk-based portfolio of static, unit, integration, contract, browser, performance, accessibility, security, and manual checks with ownership and feedback goals. Do not use for derive the concrete test cases and export format from approved requirements or install the selected test framework in the project.
---

# Testing Portfolio Strategy

## Responsibility

Design a risk-based portfolio of static, unit, integration, contract, browser, performance, accessibility, security, and manual checks with ownership and feedback goals.

## Trigger

Use when the requested outcome is: Design a risk-based portfolio of static, unit, integration, contract, browser, performance, accessibility, security, and manual checks with ownership and feedback goals.

Do not use when:
- Derive the concrete test cases and export format from approved requirements. Route to `test-case-design-and-export`.
- Install the selected test framework in the project. Route to `test-runtime-bootstrap`.

## Required Inputs

- System architecture, risks, component types, environments, and data constraints.

Also require exact target identity, authority, mutation boundary, evidence consumer, cleanup or rollback, and declared unknowns where applicable.

## Procedure

1. Freeze system boundaries, requirements, risks, failure cost, change frequency, environments, current tests, team skills, CI budget, and release policy.
2. Map each risk to the cheapest layer that can observe it while preserving critical cross-boundary and user-journey checks.
3. Define ownership, fixtures and data, hermeticity, execution cadence, budgets, flake policy, quarantine limits, and evidence consumers.
4. Return portfolio, gaps, sequencing, and framework requirements without implementing tests or installing tools.

## Output Contract

Produce:
- risk-to-test-layer matrix
- test portfolio and ownership
- runtime and data requirements
- coverage gaps and sequencing

Every material action, command, result, finding, score, capture, provider receipt, or completion claim must bind to exact target identity and current evidence or be labeled assumption/unknown.

## Coverage

- `risk-based`
- `test-layer`
- `feedback-speed`
- `hermeticity`
- `ownership`
- `flake-policy`
- `budget`

## Hard Gates

- A portfolio must justify every layer by observable risk and feedback value; test-count targets, pyramid dogma, and duplicate assertions across layers are not strategy.
- Preserve source, build, dataset, model, workflow, provider, browser, session, or local-system identity; command, version, exit, duration, artifacts, hashes, limitations, and cleanup must remain explicit when applicable.
- Return `needs-input` when a named owner can provide missing scope, authority, evidence, governance, target, or decision.
- Return `blocked` when proceeding would exceed mutation authority, expose credentials, violate governance, erase failed evidence, perform an undeclared remote or destructive action, or mix independent review with repair.

## Human Decision Authority

The Skill may return evidence, findings, options, and a recommendation. Scope approval, repair authorization, risk acceptance, publication, experiment submission, local-system change, remote action, and release disposition remain explicit human decisions under the declared identity.

## Status Mapping

- `passed`: the atomic output and every gate have current target-bound evidence.
- `needs-input`: a requestable scope, authority, target, fixture, governance term, or decision is absent.
- `blocked`: safe work requires prohibited access, unavailable authority, secret values, destructive or remote action, or an incompatible identity.
- `failed`: the authorized action ran but a deterministic check or required output failed.

## Non-Responsibilities

Does not approve upstream product decisions, expand authority, or perform remote writes beyond its explicit permission identity.

Adjacent capabilities:
- `test-case-design-and-export`
- `test-runtime-bootstrap`
- `baseline-regression-control`
- `independent-blackbox-qa`

Never silently expand source, command, browser, data, credential, local-system, provider, or remote authority. Independent review, QA, audit, evidence acquisition, analysis, and triage never repair source. Setup and authentication never imply authority to perform the downstream action.
