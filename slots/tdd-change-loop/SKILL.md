# tdd-change-loop

Status: draft candidate; source-index skeleton only. This file has not been purified, evaluated, or released.

## Candidate Responsibility

Drive behavior changes through a real red-green-refactor loop and a final fresh verification.

## Source Boundaries

- Input: A feature, defect, refactor, or other behavior change.
- Output: Minimal code supported by observed RED, GREEN, cleanup, and completion evidence.

## Required Upstream Dependencies

- `cluster:implementation-planning-and-handoff`

## Source Units

See `provenance.json` for the complete unit-by-unit source index and recorded dispositions.

## Fail-Closed Protocol

Do not execute, publish, or claim completion from this skeleton. Stop when required inputs, permissions, dependency contracts, source evidence, evaluation evidence, or release evidence are missing or unresolved. Never fabricate evidence or treat `not-run`, `pending`, or `draft` as a passing gate.
