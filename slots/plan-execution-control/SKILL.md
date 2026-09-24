# plan-execution-control

Status: draft candidate; source-index skeleton only. This file has not been purified, evaluated, or released.

## Candidate Responsibility

Load and review a plan, execute task states with checkpoints, stop on blockers, and hand off branch completion.

## Source Boundaries

- Input: An executable implementation plan and an isolated work environment.
- Output: Plan-aligned implementation status with task-level verification and explicit blockers.

## Required Upstream Dependencies

- `cluster:implementation-planning-and-handoff`

## Source Units

See `provenance.json` for the complete unit-by-unit source index and recorded dispositions.

## Fail-Closed Protocol

Do not execute, publish, or claim completion from this skeleton. Stop when required inputs, permissions, dependency contracts, source evidence, evaluation evidence, or release evidence are missing or unresolved. Never fabricate evidence or treat `not-run`, `pending`, or `draft` as a passing gate.
