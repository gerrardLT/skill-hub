---
name: baseline-regression-control
description: Run and compare a frozen baseline and candidate check set under matched conditions, attribute regressions, and preserve current evidence without source repair. Do not use for design the project-wide mix of test layers and quality checks or apply the accepted repair for a confirmed regression.
---

# Baseline Regression Control

## Responsibility

Run and compare a frozen baseline and candidate check set under matched conditions, attribute regressions, and preserve current evidence without source repair.

## Trigger

Use when the requested outcome is: Run and compare a frozen baseline and candidate check set under matched conditions, attribute regressions, and preserve current evidence without source repair.

Do not use when:
- Design the project-wide mix of test layers and quality checks. Route to `testing-portfolio-strategy`.
- Apply the accepted repair for a confirmed regression. Route to `defect-remediation`.

## Required Inputs

- A trusted historical baseline and a current measurement made under the same contract.

Also require exact target identity, authority, mutation boundary, evidence consumer, cleanup or rollback, and declared unknowns where applicable.

## Procedure

1. Freeze baseline and candidate identities, environment, commands, data, seeds, warmup, thresholds, allowed variance, and comparison exclusions.
2. Run approved checks in matched conditions and record commands, versions, exits, duration, artifacts, hashes, and retries.
3. Separate new regression, pre-existing failure, flaky or environmental variance, intended change, and incomparable evidence.
4. Return a comparison and attribution report; never repair source, delete failures, or move thresholds after results.

## Output Contract

Produce:
- matched baseline and candidate evidence
- regression attribution matrix
- variance and comparability report
- bounded repair handoff

Every material action, command, result, finding, score, capture, provider receipt, or completion claim must bind to exact target identity and current evidence or be labeled assumption/unknown.

## Coverage

- `baseline-identity`
- `candidate-identity`
- `matched-environment`
- `threshold`
- `variance`
- `warmup`
- `regression-attribution`

## Hard Gates

- A regression verdict requires frozen identities and matched commands, environment, data, seeds, warmup, thresholds, and retry policy; unmatched or stale evidence is incomparable, not passing.
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
- `resilience-and-determinism`
- `defect-remediation`
- `completion-evidence-gate`

Never silently expand source, command, browser, data, credential, local-system, provider, or remote authority. Independent review, QA, audit, evidence acquisition, analysis, and triage never repair source. Setup and authentication never imply authority to perform the downstream action.
