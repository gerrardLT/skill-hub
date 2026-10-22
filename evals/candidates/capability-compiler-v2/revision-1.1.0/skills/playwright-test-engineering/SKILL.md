---
name: playwright-test-engineering
description: "Design Playwright test source as a candidate artifact and execute or diagnose authorized existing Playwright tests without writing project source. Use when A browser behavior needs an end-to-end Playwright test designed, or existing Playwright tests need running and diagnosing; Someone asks for role-based locators, web-first assertions and isolated fixtures for a user journey. Do not use for: Install and configure Playwright in the project and write a real first test (-> test-runtime-bootstrap); Perform product-level black-box QA and issue release findings (-> independent-blackbox-qa); Write or run unit or integration tests for Node modules with Vitest (-> vitest-tooling)."
---

# Playwright Test Engineering

## Responsibility

Design Playwright test source as a candidate artifact and execute or diagnose authorized existing Playwright tests without writing project source.

## Trigger

Use when the request matches any of:
- A browser behavior needs an end-to-end Playwright test designed, or existing Playwright tests need running and diagnosing
- Someone asks for role-based locators, web-first assertions and isolated fixtures for a user journey

Do not use when:
- Install and configure Playwright in the project and write a real first test. Route to `test-runtime-bootstrap`.
- Perform product-level black-box QA and issue release findings. Route to `independent-blackbox-qa`.
- Write or run unit or integration tests for Node modules with Vitest. Route to `vitest-tooling`.

## Required Inputs

- Browser behaviors, test environments, risks, data, and automation acceptance goals.

## Procedure

1. Freeze behavior, environment, project conventions, runtime availability, data and auth boundary, browser matrix, risks, and acceptance goal.
2. Prefer user-visible behavior, role or contract locators, web-first assertions, isolated data, complete auth state, and deterministic waiting; avoid implementation selectors and sleeps.
3. Emit candidate test, fixture, config, or locator changes as an artifact; only run authorized existing project tests and collect traces, screenshots, video, and exits.
4. Return candidate source, run evidence or blocked bootstrap handoff, flake controls, and limitations; do not modify project files under a local-exec identity.

## Domain Guidance

- Candidate tests are delivered as artifacts. Applying them to the project is a separate authorized step owned by tdd-change-loop or isolated-task-implementation; name the one that fits and hand the artifact over.

## Output Contract

Produce:
- Playwright candidate test artifact
- fixture and locator design
- existing-test execution evidence
- flake and bootstrap handoff

Every material action, command, result, finding, score, capture, provider receipt, or completion claim must bind to exact target identity and current evidence or be labeled assumption/unknown.

Deliver each output as the artifact itself (tables, commands, patches, plans, records), not as a description of how it would be produced.

## Coverage

- `candidate-test-artifact`
- `role-locator`
- `web-first-assertion`
- `isolated-fixture`
- `deterministic-wait`
- `no-project-write`

## Hard Gates

- A local-exec Playwright candidate cannot modify project tests or config; project installation or source writes require a separate authorized workspace capability.
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
- `test-runtime-bootstrap`
- `independent-blackbox-qa`
- `safe-browser-probing`
- `test-double-discipline`
- `vitest-tooling`

Never silently expand source, command, browser, data, credential, local-system, provider, or remote authority. Independent review, QA, audit, evidence acquisition, analysis, and triage never repair source. Setup and authentication never imply authority to perform the downstream action.
