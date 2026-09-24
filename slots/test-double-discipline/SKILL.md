# test-double-discipline

Status: draft candidate; source-index skeleton only. This file has not been purified, evaluated, or released.

## Candidate Responsibility

Constrain mocks, spies, and test-only interfaces so tests exercise meaningful behavior and complete data shapes.

## Source Boundaries

- Input: A test design that requires dependency isolation or an existing test double.
- Output: A minimal, behavior-focused test-double strategy that does not pollute production APIs.

## Required Upstream Dependencies

- `cluster:tdd-change-loop`
- `cluster:testing-portfolio-strategy`

## Source Units

See `provenance.json` for the complete unit-by-unit source index and recorded dispositions.

## Fail-Closed Protocol

Do not execute, publish, or claim completion from this skeleton. Stop when required inputs, permissions, dependency contracts, source evidence, evaluation evidence, or release evidence are missing or unresolved. Never fabricate evidence or treat `not-run`, `pending`, or `draft` as a passing gate.
