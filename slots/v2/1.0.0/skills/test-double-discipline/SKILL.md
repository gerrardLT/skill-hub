---
name: test-double-discipline
description: Assess or design the smallest behavior-focused test double boundary so tests use complete data shapes and do not pollute production interfaces. Do not use for implement and run the full test through the selected framework or design the project-wide balance of unit, integration, contract, and end-to-end tests.
---

# Test Double Discipline

## Responsibility

Assess or design the smallest behavior-focused test double boundary so tests use complete data shapes and do not pollute production interfaces.

## Trigger

Use when the requested outcome is: Assess or design the smallest behavior-focused test double boundary so tests use complete data shapes and do not pollute production interfaces.

Do not use when:
- Implement and run the full test through the selected framework. Route to `vitest-tooling`.
- Design the project-wide balance of unit, integration, contract, and end-to-end tests. Route to `testing-portfolio-strategy`.

## Required Inputs

- A test design that requires dependency isolation or an existing test double.

Also require exact target identity, authority, mutation boundary, evidence consumer, cleanup or rollback, and declared unknowns where applicable.

## Procedure

1. Freeze the behavior under test, real dependency contract, failure modes, speed or isolation need, existing double, and production boundary.
2. Prefer real code, in-memory implementation, fake server, contract fixture, or dependency injection before mocks and spies.
3. Keep the double at an owned boundary, provide complete realistic shapes and failures, and avoid test-only methods in production APIs.
4. Use approved local analysis or tests to expose brittle coupling and return a minimal strategy or candidate artifact without project-source mutation.

## Output Contract

Produce:
- test-double decision
- owned boundary and contract
- complete fixture or fake design
- anti-pattern and verification evidence

Every material action, command, result, finding, score, capture, provider receipt, or completion claim must bind to exact target identity and current evidence or be labeled assumption/unknown.

## Coverage

- `owned-boundary`
- `real-code-first`
- `complete-shape`
- `meaningful-failure`
- `no-internal-mock`
- `no-test-only-production-api`

## Hard Gates

- A double is justified only at a real owned boundary and must preserve complete contract shapes and meaningful failures; mocking internals or adding test-only production APIs fails.
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
- `vitest-tooling`
- `playwright-test-engineering`
- `testing-portfolio-strategy`
- `tdd-change-loop`

Never silently expand source, command, browser, data, credential, local-system, provider, or remote authority. Independent review, QA, audit, evidence acquisition, analysis, and triage never repair source. Setup and authentication never imply authority to perform the downstream action.
