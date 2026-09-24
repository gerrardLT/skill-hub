# baseline-regression-control

Status: draft candidate; source-index skeleton only. This file has not been purified, evaluated, or released.

## Candidate Responsibility

Compare current audit, visual, performance, model, or production measures with trusted baselines and control updates.

## Source Boundaries

- Input: A trusted historical baseline and a current measurement made under the same contract.
- Output: A diff, regression decision, and controlled baseline-update decision.

## Required Upstream Dependencies

- `cluster:llm-quality-evaluation`
- `cluster:playwright-test-engineering`
- `cluster:web-performance-diagnostics`
- `cluster:website-audit-remediation`

## Source Units

See `provenance.json` for the complete unit-by-unit source index and recorded dispositions.

## Fail-Closed Protocol

Do not execute, publish, or claim completion from this skeleton. Stop when required inputs, permissions, dependency contracts, source evidence, evaluation evidence, or release evidence are missing or unresolved. Never fabricate evidence or treat `not-run`, `pending`, or `draft` as a passing gate.
