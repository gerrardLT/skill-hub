---
name: test-double-discipline
description: "Assess or design the smallest behavior-focused test double boundary so tests use complete data shapes and do not pollute production interfaces. Use when A test needs isolation from a dependency and someone must decide between real code, a fake, a stub or a mock; Someone asks whether a mock is testing behavior or just mirroring the implementation. Do not use for: Implement and run the full test through the selected framework (-> vitest-tooling); Design the project-wide balance of unit, integration, contract, and end-to-end tests (-> testing-portfolio-strategy)."
---

# Test Double Discipline

## Responsibility

Assess or design the smallest behavior-focused test double boundary so tests use complete data shapes and do not pollute production interfaces.

## Trigger

Use when the request matches any of:
- A test needs isolation from a dependency and someone must decide between real code, a fake, a stub or a mock
- Someone asks whether a mock is testing behavior or just mirroring the implementation

Do not use when:
- Implement and run the full test through the selected framework. Route to `vitest-tooling`.
- Design the project-wide balance of unit, integration, contract, and end-to-end tests. Route to `testing-portfolio-strategy`.

## Required Inputs

- A test design that requires dependency isolation or an existing test double.

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

Deliver each output as the artifact itself (tables, commands, patches, plans, records), not as a description of how it would be produced.

## Coverage

- `owned-boundary`
- `real-code-first`
- `complete-shape`
- `meaningful-failure`
- `no-internal-mock`
- `no-test-only-production-api`

## Hard Gates

- A double is justified only at a real owned boundary and must preserve complete contract shapes and meaningful failures; mocking internals or adding test-only production APIs fails.
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
- `vitest-tooling`
- `playwright-test-engineering`
- `testing-portfolio-strategy`
- `tdd-change-loop`

Never silently expand source, command, browser, data, credential, local-system, provider, or remote authority. Independent review, QA, audit, evidence acquisition, analysis, and triage never repair source. Setup and authentication never imply authority to perform the downstream action.
