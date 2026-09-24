# browser-session-and-runtime-configuration

Status: draft candidate; source-index skeleton only. This file has not been purified, evaluated, or released.

## Candidate Responsibility

Configure browser sessions, wrapper dispatch, CLI settings, and isolated project context after prerequisites pass.

## Source Boundaries

- Input: A validated browser task, session identifier, project path, wrapper contract, and CLI configuration.
- Output: A configured isolated session and reproducible browser invocation settings.

## Required Upstream Dependencies

- `cluster:tool-runtime-readiness`

## Source Units

See `provenance.json` for the complete unit-by-unit source index and recorded dispositions.

## Fail-Closed Protocol

Do not execute, publish, or claim completion from this skeleton. Stop when required inputs, permissions, dependency contracts, source evidence, evaluation evidence, or release evidence are missing or unresolved. Never fabricate evidence or treat `not-run`, `pending`, or `draft` as a passing gate.
