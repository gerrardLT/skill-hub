# tool-runtime-readiness

Status: draft candidate; source-index skeleton only. This file has not been purified, evaluated, or released.

## Candidate Responsibility

Validate that a requested browser, audit, or test tool is available and its invocation boundary is safe before setup.

## Source Boundaries

- Input: A tool request, project path, shell environment, and declared prerequisite contract.
- Output: A prerequisite verdict, supported wrapper boundary, or explicit unavailable-tool failure.

## Required Upstream Dependencies

- None recorded.

## Source Units

See `provenance.json` for the complete unit-by-unit source index and recorded dispositions.

## Fail-Closed Protocol

Do not execute, publish, or claim completion from this skeleton. Stop when required inputs, permissions, dependency contracts, source evidence, evaluation evidence, or release evidence are missing or unresolved. Never fabricate evidence or treat `not-run`, `pending`, or `draft` as a passing gate.
