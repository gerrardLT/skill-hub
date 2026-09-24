# website-audit-remediation

Status: draft candidate; source-index skeleton only. This file has not been purified, evaluated, or released.

## Candidate Responsibility

Run broad website audits, map SEO, performance, security, content, and accessibility findings to source, and recheck fixes.

## Source Boundaries

- Input: A scannable site, audit CLI, and an authorized source-edit scope.
- Output: A categorized report, remediation loop, score targets, and fresh audit evidence.

## Required Upstream Dependencies

- `cluster:tool-runtime-readiness`

## Source Units

See `provenance.json` for the complete unit-by-unit source index and recorded dispositions.

## Fail-Closed Protocol

Do not execute, publish, or claim completion from this skeleton. Stop when required inputs, permissions, dependency contracts, source evidence, evaluation evidence, or release evidence are missing or unresolved. Never fabricate evidence or treat `not-run`, `pending`, or `draft` as a passing gate.
