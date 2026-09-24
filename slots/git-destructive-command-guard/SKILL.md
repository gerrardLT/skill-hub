# git-destructive-command-guard

Status: draft candidate; source-index skeleton only. This file has not been purified, evaluated, or released.

## Candidate Responsibility

Intercept destructive Git commands before execution and provide a configurable, verifiable local guardrail.

## Source Boundaries

- Input: A command hook environment, dangerous-command policy, and local configuration.
- Output: An installed and tested command guard; normal release packaging remains out of scope.

## Required Upstream Dependencies

- None recorded.

## Source Units

See `provenance.json` for the complete unit-by-unit source index and recorded dispositions.

## Fail-Closed Protocol

Do not execute, publish, or claim completion from this skeleton. Stop when required inputs, permissions, dependency contracts, source evidence, evaluation evidence, or release evidence are missing or unresolved. Never fabricate evidence or treat `not-run`, `pending`, or `draft` as a passing gate.
