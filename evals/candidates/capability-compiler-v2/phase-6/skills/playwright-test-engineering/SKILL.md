---
name: playwright-test-engineering
description: Design Playwright test source as a candidate artifact and execute or diagnose authorized existing Playwright tests without writing project source. Do not use for install and configure playwright in the project and write a real first test or perform product-level black-box qa and issue release findings.
---

# Playwright Test Engineering

## Responsibility

Design Playwright test source as a candidate artifact and execute or diagnose authorized existing Playwright tests without writing project source.

## Trigger

Use when the requested outcome is: Design Playwright test source as a candidate artifact and execute or diagnose authorized existing Playwright tests without writing project source.

Do not use when:
- Install and configure Playwright in the project and write a real first test. Route to `test-runtime-bootstrap`.
- Perform product-level black-box QA and issue release findings. Route to `independent-blackbox-qa`.

## Required Inputs

- Browser behaviors, test environments, risks, data, and automation acceptance goals.

Also require exact target identity, authority, mutation boundary, evidence consumer, cleanup or rollback, and declared unknowns where applicable.

## Procedure

1. Freeze behavior, environment, project conventions, runtime availability, data and auth boundary, browser matrix, risks, and acceptance goal.
2. Prefer user-visible behavior, role or contract locators, web-first assertions, isolated data, complete auth state, and deterministic waiting; avoid implementation selectors and sleeps.
3. Emit candidate test, fixture, config, or locator changes as an artifact; only run authorized existing project tests and collect traces, screenshots, video, and exits.
4. Return candidate source, run evidence or blocked bootstrap handoff, flake controls, and limitations; do not modify project files under a local-exec identity.

## Output Contract

Produce:
- Playwright candidate test artifact
- fixture and locator design
- existing-test execution evidence
- flake and bootstrap handoff

Every material action, command, result, finding, score, capture, provider receipt, or completion claim must bind to exact target identity and current evidence or be labeled assumption/unknown.

## Coverage

- `candidate-test-artifact`
- `role-locator`
- `web-first-assertion`
- `isolated-fixture`
- `deterministic-wait`
- `no-project-write`

## Hard Gates

- A local-exec Playwright candidate cannot modify project tests or config; project installation or source writes require a separate authorized workspace capability.
- Preserve source, build, dataset, model, workflow, provider, browser, session, or local-system identity; command, version, exit, duration, artifacts, hashes, limitations, and cleanup must remain explicit when applicable.
- Return `needs-input` when a named owner can provide missing scope, authority, evidence, governance, target, or decision.
- Return `blocked` when proceeding would exceed mutation authority, expose credentials, violate governance, erase failed evidence, perform an undeclared remote or destructive action, or mix independent review with repair.

## Status Mapping

- `passed`: the atomic output and every gate have current target-bound evidence.
- `needs-input`: a requestable scope, authority, target, fixture, governance term, or decision is absent.
- `blocked`: safe work requires prohibited access, unavailable authority, secret values, destructive or remote action, or an incompatible identity.
- `failed`: the authorized action ran but a deterministic check or required output failed.

## Non-Responsibilities

Does not approve upstream product decisions, expand authority, or perform remote writes beyond its explicit permission identity.

Adjacent capabilities:
- `test-runtime-bootstrap`
- `independent-blackbox-qa`
- `safe-browser-probing`
- `test-double-discipline`

Never silently expand source, command, browser, data, credential, local-system, provider, or remote authority. Independent review, QA, audit, evidence acquisition, analysis, and triage never repair source. Setup and authentication never imply authority to perform the downstream action.
