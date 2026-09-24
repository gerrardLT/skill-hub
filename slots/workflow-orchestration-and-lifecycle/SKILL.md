# workflow-orchestration-and-lifecycle

Status: draft candidate; source-index skeleton only. This file has not been purified, evaluated, or released.

## Candidate Responsibility

Sequence a capability workflow, route sub-capabilities, and preserve lifecycle state without performing the downstream work itself.

## Source Boundaries

- Input: A request, phase state, available capabilities, and execution constraints.
- Output: An ordered workflow, routing decision, handoff state, and stop or retry condition.

## Required Upstream Dependencies

- None recorded.

## Source Units

See `provenance.json` for the complete unit-by-unit source index and recorded dispositions.

## Fail-Closed Protocol

Do not execute, publish, or claim completion from this skeleton. Stop when required inputs, permissions, dependency contracts, source evidence, evaluation evidence, or release evidence are missing or unresolved. Never fabricate evidence or treat `not-run`, `pending`, or `draft` as a passing gate.
