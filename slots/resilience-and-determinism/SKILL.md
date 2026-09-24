# resilience-and-determinism

Status: draft candidate; source-index skeleton only. This file has not been purified, evaluated, or released.

## Candidate Responsibility

Use layered defenses, condition waits, isolated fixtures, stable assertions, and controlled time to prevent flakiness.

## Source Boundaries

- Input: A confirmed cause involving invalid data, races, environment contamination, fragile waits, or flaky tests.
- Output: Defensive validation, deterministic synchronization, and isolation mechanisms.

## Required Upstream Dependencies

- `cluster:root-cause-investigation`

## Source Units

See `provenance.json` for the complete unit-by-unit source index and recorded dispositions.

## Fail-Closed Protocol

Do not execute, publish, or claim completion from this skeleton. Stop when required inputs, permissions, dependency contracts, source evidence, evaluation evidence, or release evidence are missing or unresolved. Never fabricate evidence or treat `not-run`, `pending`, or `draft` as a passing gate.
