---
name: vitest-tooling
description: "Design Vitest test or configuration source as a candidate artifact and execute or diagnose authorized existing Vitest tests without writing project source. Use when A JavaScript or TypeScript unit or integration test needs designing, or an existing Vitest suite needs running and diagnosing; Someone asks for controlled time, isolated modules and cleanup in Vitest tests. Do not use for: Install and configure Vitest in a project that lacks a test runtime (-> test-runtime-bootstrap); Define the minimal test-double boundary before writing mocks (-> test-double-discipline); Write or run browser end-to-end tests (-> playwright-test-engineering)."
---

# Vitest Tooling

## Responsibility

Design Vitest test or configuration source as a candidate artifact and execute or diagnose authorized existing Vitest tests without writing project source.

## Trigger

Use when the request matches any of:
- A JavaScript or TypeScript unit or integration test needs designing, or an existing Vitest suite needs running and diagnosing
- Someone asks for controlled time, isolated modules and cleanup in Vitest tests

Do not use when:
- Install and configure Vitest in a project that lacks a test runtime. Route to `test-runtime-bootstrap`.
- Define the minimal test-double boundary before writing mocks. Route to `test-double-discipline`.
- Write or run browser end-to-end tests. Route to `playwright-test-engineering`.

## Required Inputs

- A JavaScript or TypeScript unit or integration test project using Vitest.

## Procedure

1. Freeze behavior, project conventions, existing config, runtime availability, module boundaries, data, environment, and accepted command.
2. Use behavior-focused assertions, complete fixtures, controlled time, explicit cleanup, isolated modules, and stable snapshots only where semantically useful.
3. Emit candidate test or config source as an artifact; run only existing authorized project tests and record command, version, exit, duration, and output.
4. Return candidate source, diagnosis, test-double concerns, and bootstrap handoff; do not modify project files under a local-exec identity.

## Domain Guidance

- Type tests use the .test-d.ts suffix with expectTypeOf. Run one test by file and line (vitest path/file.test.ts:10), use vitest run in CI, and pass a name filter to narrow a run.

## Output Contract

Produce:
- Vitest candidate test artifact
- configuration or fixture design
- existing-suite execution evidence
- diagnosis and bootstrap handoff

Every material action, command, result, finding, score, capture, provider receipt, or completion claim must bind to exact target identity and current evidence or be labeled assumption/unknown.

Deliver each output as the artifact itself (tables, commands, patches, plans, records), not as a description of how it would be produced.

## Coverage

- `candidate-test-artifact`
- `behavior-assertion`
- `controlled-time`
- `cleanup`
- `isolation`
- `no-project-write`

## Hard Gates

- A local-exec Vitest candidate cannot modify project tests or config; project installation or source writes require a separate authorized workspace capability.
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
- `test-double-discipline`
- `tdd-change-loop`
- `testing-portfolio-strategy`
- `playwright-test-engineering`

Never silently expand source, command, browser, data, credential, local-system, provider, or remote authority. Independent review, QA, audit, evidence acquisition, analysis, and triage never repair source. Setup and authentication never imply authority to perform the downstream action.
