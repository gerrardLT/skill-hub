---
name: resilience-and-determinism
description: Diagnose and verify nondeterminism, retries, timeouts, cleanup, isolation, ordering, and recovery behavior under a frozen workload without source repair. Do not use for apply the accepted source fix for the confirmed flaky root cause or design the overall test portfolio and layer allocation.
---

# Resilience And Determinism

## Responsibility

Diagnose and verify nondeterminism, retries, timeouts, cleanup, isolation, ordering, and recovery behavior under a frozen workload without source repair.

## Trigger

Use when the requested outcome is: Diagnose and verify nondeterminism, retries, timeouts, cleanup, isolation, ordering, and recovery behavior under a frozen workload without source repair.

Do not use when:
- Apply the accepted source fix for the confirmed flaky root cause. Route to `defect-remediation`.
- Design the overall test portfolio and layer allocation. Route to `testing-portfolio-strategy`.

## Required Inputs

- A confirmed cause involving invalid data, races, environment contamination, fragile waits, or flaky tests.

Also require exact target identity, authority, mutation boundary, evidence consumer, cleanup or rollback, and declared unknowns where applicable.

## Procedure

1. Freeze target identity, workload, environment, seeds, clocks, ordering, resources, retries, timeouts, and success criteria.
2. Repeat approved runs while varying one declared factor at a time and record exits, duration, logs, artifacts, and cleanup state.
3. Distinguish true recovery from retry masking, leaked state, non-idempotent side effects, race, external variance, and measurement noise.
4. Return a reproducible failure model, determinism or resilience verdict, and repair recommendation without editing source.

## Output Contract

Produce:
- determinism experiment record
- retry and timeout analysis
- cleanup and recovery evidence
- root-cause hypothesis and bounded recommendation

Every material action, command, result, finding, score, capture, provider receipt, or completion claim must bind to exact target identity and current evidence or be labeled assumption/unknown.

## Coverage

- `seed`
- `ordering`
- `timeout`
- `retry-masking`
- `idempotency`
- `cleanup`
- `failure-injection`
- `repeated-evidence`

## Hard Gates

- A resilience claim requires repeated target-bound evidence with recorded seeds, ordering, environment, retries, timeouts, side effects, cleanup, and failure injection; one passing retry proves nothing.
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
- `root-cause-investigation`
- `defect-remediation`
- `baseline-regression-control`
- `testing-portfolio-strategy`

Never silently expand source, command, browser, data, credential, local-system, provider, or remote authority. Independent review, QA, audit, evidence acquisition, analysis, and triage never repair source. Setup and authentication never imply authority to perform the downstream action.
