# artifact-persistence-and-tool-actions

Status: draft candidate; source-index skeleton only. This file has not been purified, evaluated, or released.

## Candidate Responsibility

Select authorized tools and persist the resulting specification or artifact at the correct lifecycle point.

## Source Boundaries

- Input: A validated task, tool boundary, output location, and write authorization.
- Output: A tool action, saved artifact, or explicit no-write outcome.

## Required Upstream Dependencies

- `cluster:workflow-orchestration-and-lifecycle`

## Source Units

See `provenance.json` for the complete unit-by-unit source index and recorded dispositions.

## Fail-Closed Protocol

Do not execute, publish, or claim completion from this skeleton. Stop when required inputs, permissions, dependency contracts, source evidence, evaluation evidence, or release evidence are missing or unresolved. Never fabricate evidence or treat `not-run`, `pending`, or `draft` as a passing gate.
