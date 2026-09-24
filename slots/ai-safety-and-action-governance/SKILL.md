# ai-safety-and-action-governance

Status: draft candidate; source-index skeleton only. This file has not been purified, evaluated, or released.

## Candidate Responsibility

Assess prompt and action risks, preserve human checkpoints, and prevent unsafe autonomy or unsupported safety claims.

## Source Boundaries

- Input: An AI capability, tools and permissions, threat scenarios, failure evidence, and consequence level.
- Output: A safety boundary, red-team scope, human checkpoint, stop condition, and residual risk.

## Required Upstream Dependencies

- `cluster:ai-agent-autonomy-and-human-control`
- `cluster:ai-interaction-and-probabilistic-ux`

## Source Units

See `provenance.json` for the complete unit-by-unit source index and recorded dispositions.

## Fail-Closed Protocol

Do not execute, publish, or claim completion from this skeleton. Stop when required inputs, permissions, dependency contracts, source evidence, evaluation evidence, or release evidence are missing or unresolved. Never fabricate evidence or treat `not-run`, `pending`, or `draft` as a passing gate.
