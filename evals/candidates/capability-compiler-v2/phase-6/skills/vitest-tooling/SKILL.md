---
name: vitest-tooling
description: Design Vitest test or configuration source as a candidate artifact and execute or diagnose authorized existing Vitest tests without writing project source. Do not use for install and configure vitest in a project that lacks a test runtime or define the minimal test-double boundary before writing mocks.
---

# Vitest Tooling

## Responsibility

Design Vitest test or configuration source as a candidate artifact and execute or diagnose authorized existing Vitest tests without writing project source.

## Trigger

Use when the requested outcome is: Design Vitest test or configuration source as a candidate artifact and execute or diagnose authorized existing Vitest tests without writing project source.

Do not use when:
- Install and configure Vitest in a project that lacks a test runtime. Route to `test-runtime-bootstrap`.
- Define the minimal test-double boundary before writing mocks. Route to `test-double-discipline`.

## Required Inputs

- A JavaScript or TypeScript unit or integration test project using Vitest.

Also require exact target identity, authority, mutation boundary, evidence consumer, cleanup or rollback, and declared unknowns where applicable.

## Procedure

1. Freeze behavior, project conventions, existing config, runtime availability, module boundaries, data, environment, and accepted command.
2. Use behavior-focused assertions, complete fixtures, controlled time, explicit cleanup, isolated modules, and stable snapshots only where semantically useful.
3. Emit candidate test or config source as an artifact; run only existing authorized project tests and record command, version, exit, duration, and output.
4. Return candidate source, diagnosis, test-double concerns, and bootstrap handoff; do not modify project files under a local-exec identity.

## Output Contract

Produce:
- Vitest candidate test artifact
- configuration or fixture design
- existing-suite execution evidence
- diagnosis and bootstrap handoff

Every material action, command, result, finding, score, capture, provider receipt, or completion claim must bind to exact target identity and current evidence or be labeled assumption/unknown.

## Coverage

- `candidate-test-artifact`
- `behavior-assertion`
- `controlled-time`
- `cleanup`
- `isolation`
- `no-project-write`

## Hard Gates

- A local-exec Vitest candidate cannot modify project tests or config; project installation or source writes require a separate authorized workspace capability.
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
- `test-double-discipline`
- `tdd-change-loop`
- `testing-portfolio-strategy`

Never silently expand source, command, browser, data, credential, local-system, provider, or remote authority. Independent review, QA, audit, evidence acquisition, analysis, and triage never repair source. Setup and authentication never imply authority to perform the downstream action.
