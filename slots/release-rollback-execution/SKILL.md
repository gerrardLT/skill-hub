# release-rollback-execution

Status: draft candidate; source-index skeleton only. This file has not been purified, evaluated, or released.

## Candidate Responsibility

Execute or prepare a reviewable release rollback when post-deploy evidence meets the rollback condition.

## Source Boundaries

- Input: A deployed change, health evidence, provider state, and rollback authorization.
- Output: A bounded revert or rollback pull request with evidence and recovery status.

## Required Upstream Dependencies

- `cluster:deployment-observation-and-recovery`

## Source Units

See `provenance.json` for the complete unit-by-unit source index and recorded dispositions.

## Fail-Closed Protocol

Do not execute, publish, or claim completion from this skeleton. Stop when required inputs, permissions, dependency contracts, source evidence, evaluation evidence, or release evidence are missing or unresolved. Never fabricate evidence or treat `not-run`, `pending`, or `draft` as a passing gate.
