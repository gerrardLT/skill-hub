# subagent-task-pipeline

Status: draft candidate; source-index skeleton only. This file has not been purified, evaluated, or released.

## Candidate Responsibility

Dispatch plan tasks to isolated implementers and sequence status, specification review, and quality review.

## Source Boundaries

- Input: A complete plan, one task context, and an authorized edit scope.
- Output: Per-task implementations, structured status, review flow, and resolved blockers.

## Required Upstream Dependencies

- `cluster:implementation-planning-and-handoff`

## Source Units

See `provenance.json` for the complete unit-by-unit source index and recorded dispositions.

## Fail-Closed Protocol

Do not execute, publish, or claim completion from this skeleton. Stop when required inputs, permissions, dependency contracts, source evidence, evaluation evidence, or release evidence are missing or unresolved. Never fabricate evidence or treat `not-run`, `pending`, or `draft` as a passing gate.
