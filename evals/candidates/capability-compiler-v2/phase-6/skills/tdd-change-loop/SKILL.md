---
name: tdd-change-loop
description: Implement one authorized behavior change through a preserved RED, minimal GREEN, refactor, and current host-verification loop. Do not use for design the project-wide testing portfolio and choose test layers or independently inspect and judge the finished patch.
---

# Tdd Change Loop

## Responsibility

Implement one authorized behavior change through a preserved RED, minimal GREEN, refactor, and current host-verification loop.

## Trigger

Use when the requested outcome is: Implement one authorized behavior change through a preserved RED, minimal GREEN, refactor, and current host-verification loop.

Do not use when:
- Design the project-wide testing portfolio and choose test layers. Route to `testing-portfolio-strategy`.
- Independently inspect and judge the finished patch. Route to `independent-code-review`.

## Required Inputs

- A feature, defect, refactor, or other behavior change.

Also require exact target identity, authority, mutation boundary, evidence consumer, cleanup or rollback, and declared unknowns where applicable.

## Procedure

1. Verify frozen behavior, authorized workspace, target source identity, existing test convention, focused command, regression surface, and one writer.
2. Write the smallest user-observable or contract-level test and run it through the host; preserve proof that it fails for the expected reason before source repair.
3. Write the minimum production change to pass the RED test, then run focused tests and only the affected broader regressions.
4. Refactor only while green, rerun current checks, and return RED/GREEN/refactor command evidence, patch, hashes, and limitations for independent review.

## Output Contract

Produce:
- RED test and failure evidence
- minimal GREEN source patch
- refactor and regression evidence
- reviewable patch handoff

Every material action, command, result, finding, score, capture, provider receipt, or completion claim must bind to exact target identity and current evidence or be labeled assumption/unknown.

## Coverage

- `RED-before-code`
- `minimal-GREEN`
- `refactor-while-green`
- `host-verification`
- `affected-regression`
- `single-writer`

## Hard Gates

- No TDD completion without a target-bound failing test observed before the production change, a minimal passing patch, and fresh post-change focused plus affected-regression evidence.
- Preserve source, build, dataset, model, workflow, provider, browser, session, or local-system identity; command, version, exit, duration, artifacts, hashes, limitations, and cleanup must remain explicit when applicable.
- Return `needs-input` when a named owner can provide missing scope, authority, evidence, governance, target, or decision.
- Return `blocked` when proceeding would exceed mutation authority, expose credentials, violate governance, erase failed evidence, perform an undeclared remote or destructive action, or mix independent review with repair.

## Status Mapping

- `passed`: the atomic output and every gate have current target-bound evidence.
- `needs-input`: a requestable scope, authority, target, fixture, governance term, or decision is absent.
- `blocked`: safe work requires prohibited access, unavailable authority, secret values, destructive or remote action, or an incompatible identity.
- `failed`: the authorized action ran but a deterministic check or required output failed.

## Non-Responsibilities

Does not approve upstream product decisions, expand authority, or perform remote writes beyond its explicit permission identity.

Adjacent capabilities:
- `testing-portfolio-strategy`
- `test-case-design-and-export`
- `defect-remediation`
- `independent-code-review`

Never silently expand source, command, browser, data, credential, local-system, provider, or remote authority. Independent review, QA, audit, evidence acquisition, analysis, and triage never repair source. Setup and authentication never imply authority to perform the downstream action.
