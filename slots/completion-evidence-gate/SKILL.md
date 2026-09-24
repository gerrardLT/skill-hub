# completion-evidence-gate

Status: draft candidate; source-index skeleton only. This file has not been purified, evaluated, or released.

## Candidate Responsibility

Require a fresh complete command, output inspection, and exit-code check before any success or completion claim.

## Source Boundaries

- Input: A proposed status claim and the command capable of proving it.
- Output: An evidence-supported conclusion or an explicit failure, never confidence or delegated self-report.

## Required Upstream Dependencies

- `cluster:independent-code-review`
- `cluster:playwright-test-engineering`
- `cluster:tdd-change-loop`
- `cluster:vitest-tooling`

## Source Units

See `provenance.json` for the complete unit-by-unit source index and recorded dispositions.

## Fail-Closed Protocol

Do not execute, publish, or claim completion from this skeleton. Stop when required inputs, permissions, dependency contracts, source evidence, evaluation evidence, or release evidence are missing or unresolved. Never fabricate evidence or treat `not-run`, `pending`, or `draft` as a passing gate.
