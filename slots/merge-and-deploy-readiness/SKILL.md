# merge-and-deploy-readiness

Status: draft candidate; source-index skeleton only. This file has not been purified, evaluated, or released.

## Candidate Responsibility

Check branch, authentication, pull-request state, conflicts, CI, version drift, and deployment dry runs.

## Source Boundaries

- Input: A pull request, target branch, CI state, version state, and deployment configuration.
- Output: A merge/deploy authorization or explicit blockers; post-deploy observation remains downstream.

## Required Upstream Dependencies

- `cluster:change-packaging-and-versioning`
- `cluster:completion-evidence-gate`
- `cluster:independent-code-review`

## Source Units

See `provenance.json` for the complete unit-by-unit source index and recorded dispositions.

## Fail-Closed Protocol

Do not execute, publish, or claim completion from this skeleton. Stop when required inputs, permissions, dependency contracts, source evidence, evaluation evidence, or release evidence are missing or unresolved. Never fabricate evidence or treat `not-run`, `pending`, or `draft` as a passing gate.
