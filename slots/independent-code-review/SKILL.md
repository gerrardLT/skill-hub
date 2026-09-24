# independent-code-review

Status: draft candidate; source-index skeleton only. This file has not been purified, evaluated, or released.

## Candidate Responsibility

Independently compare specifications and diffs for correctness, security, performance, architecture, tests, and maintainability.

## Source Boundaries

- Input: A specification, change description, and precise code-diff boundary.
- Output: Prioritized findings with locations, rationale, remediation, and a merge verdict; no direct repair by default.

## Required Upstream Dependencies

- `cluster:developer-self-check-and-fix`
- `cluster:plan-execution-control`
- `cluster:subagent-task-pipeline`

## Source Units

See `provenance.json` for the complete unit-by-unit source index and recorded dispositions.

## Fail-Closed Protocol

Do not execute, publish, or claim completion from this skeleton. Stop when required inputs, permissions, dependency contracts, source evidence, evaluation evidence, or release evidence are missing or unresolved. Never fabricate evidence or treat `not-run`, `pending`, or `draft` as a passing gate.
