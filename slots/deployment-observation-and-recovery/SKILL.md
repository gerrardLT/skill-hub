# deployment-observation-and-recovery

Status: draft candidate; source-index skeleton only. This file has not been purified, evaluated, or released.

## Candidate Responsibility

Observe deployment providers, assess post-deploy health, and produce auditable rollback or revert recovery changes.

## Source Boundaries

- Input: A merged change, provider status, and post-deploy health signals.
- Output: Deployment evidence, a failure decision, or a reviewable rollback and recovery pull request.

## Required Upstream Dependencies

- `cluster:merge-and-deploy-readiness`

## Source Units

See `provenance.json` for the complete unit-by-unit source index and recorded dispositions.

## Fail-Closed Protocol

Do not execute, publish, or claim completion from this skeleton. Stop when required inputs, permissions, dependency contracts, source evidence, evaluation evidence, or release evidence are missing or unresolved. Never fabricate evidence or treat `not-run`, `pending`, or `draft` as a passing gate.
