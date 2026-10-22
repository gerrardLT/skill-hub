---
name: testing-portfolio-strategy
description: "Design a risk-based portfolio of static, unit, integration, contract, browser, performance, accessibility, security, and manual checks with ownership and feedback goals. Use when A system needs a risk-based choice of which checks run at which layer, who owns them and how fast feedback is; Someone asks where tests are missing or duplicated across unit, integration, contract and browser layers. Do not use for: Derive the concrete test cases and export format from approved requirements (-> test-case-design-and-export); Install the selected test framework in the project (-> test-runtime-bootstrap)."
---

# Testing Portfolio Strategy

## Responsibility

Design a risk-based portfolio of static, unit, integration, contract, browser, performance, accessibility, security, and manual checks with ownership and feedback goals.

## Trigger

Use when the request matches any of:
- A system needs a risk-based choice of which checks run at which layer, who owns them and how fast feedback is
- Someone asks where tests are missing or duplicated across unit, integration, contract and browser layers

Do not use when:
- Derive the concrete test cases and export format from approved requirements. Route to `test-case-design-and-export`.
- Install the selected test framework in the project. Route to `test-runtime-bootstrap`.

## Required Inputs

- System architecture, risks, component types, environments, and data constraints.

## Procedure

1. Freeze system boundaries, requirements, risks, failure cost, change frequency, environments, current tests, team skills, CI budget, and release policy.
2. Map each risk to the cheapest layer that can observe it while preserving critical cross-boundary and user-journey checks.
3. Define ownership, fixtures and data, hermeticity, execution cadence, budgets, flake policy, quarantine limits, and evidence consumers.
4. Return portfolio, gaps, sequencing, and framework requirements without implementing tests or installing tools.

## Domain Guidance

- Preserve actual access: a remote-push restriction does not imply no local file or repository access. Mark unmentioned access unknown.

## Output Contract

Produce:
- risk-to-test-layer matrix
- test portfolio and ownership
- runtime and data requirements
- coverage gaps and sequencing

Every material action, command, result, finding, score, capture, provider receipt, or completion claim must bind to exact target identity and current evidence or be labeled assumption/unknown.

Deliver each output as the artifact itself (tables, commands, patches, plans, records), not as a description of how it would be produced.

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

## Human Decision Authority

The Skill may return evidence, findings, options, and a recommendation. Scope approval, repair authorization, risk acceptance, publication, experiment submission, local-system change, remote action, and release disposition remain explicit human decisions under the declared identity.

## Status Mapping

- `passed`: the atomic output and every gate have current target-bound evidence.
- `needs-input`: a requestable scope, authority, target, fixture, governance term, or decision is absent. Deliver every supported part first and name the owner for the missing part.
- `blocked`: safe work requires prohibited access, unavailable authority, secret values, destructive or remote action, or an incompatible identity.
- `failed`: the authorized action ran but a deterministic check or required output failed.

## Non-Responsibilities

Adjacent capabilities:
- `test-case-design-and-export`
- `test-runtime-bootstrap`
- `baseline-regression-control`
- `independent-blackbox-qa`

Never silently expand source, command, browser, data, credential, local-system, provider, or remote authority. Independent review, QA, audit, evidence acquisition, analysis, and triage never repair source. Setup and authentication never imply authority to perform the downstream action.
