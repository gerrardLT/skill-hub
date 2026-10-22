---
name: baseline-regression-control
description: "Run and compare a frozen baseline and candidate check set under matched conditions, attribute regressions, and preserve current evidence without source repair. Use when A frozen baseline and a candidate must be run under matched conditions to find which differences are real regressions; Someone asks whether a failure is new, pre-existing, flaky or an intended change. Do not use for: Design the project-wide mix of test layers and quality checks (-> testing-portfolio-strategy); Apply the accepted repair for a confirmed regression (-> defect-remediation)."
---

# Baseline Regression Control

## Responsibility

Run and compare a frozen baseline and candidate check set under matched conditions, attribute regressions, and preserve current evidence without source repair.

## Trigger

Use when the request matches any of:
- A frozen baseline and a candidate must be run under matched conditions to find which differences are real regressions
- Someone asks whether a failure is new, pre-existing, flaky or an intended change

Do not use when:
- Design the project-wide mix of test layers and quality checks. Route to `testing-portfolio-strategy`.
- Apply the accepted repair for a confirmed regression. Route to `defect-remediation`.

## Required Inputs

- A trusted historical baseline and a current measurement made under the same contract.

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

Deliver each output as the artifact itself (tables, commands, patches, plans, records), not as a description of how it would be produced.

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
- Independent review, QA, audit, acquisition, analysis, and triage never imply remediation; setup or authentication never implies downstream action authority.
- Preserve source, build, dataset, model, workflow, provider, browser, session, or local-system identity; command, version, exit, duration, artifacts, hashes, limitations, and cleanup must remain explicit when applicable.
- Return `needs-input` when a named owner can provide missing scope, authority, evidence, governance, target, or decision.
- Return `blocked` when proceeding would exceed mutation authority, expose credentials, violate governance, erase failed evidence, perform an undeclared remote or destructive action, or mix independent review with repair.
- Deliver every part the supplied evidence and authority support, label assumptions, and list each missing item with the owner who can supply it; `needs-input` or `blocked` applies to the unsupported part, not to the whole deliverable.

## Forbidden Actions

- request, reveal, print, persist, hash, or transmit credential or secret values
- perform source, local-system, browser, provider, publication, or remote mutations outside the exact atomic scope and fresh authorization
- invent commands, exits, duration, artifacts, captures, provider receipts, benchmark results, approval, or completion evidence
- combine independent evidence or findings with remediation, risk acceptance, publication, deployment, or release
- claim evaluation, approval, release, or completion evidence that has not been produced

## Status Mapping

- `passed`: the atomic output and every gate have current target-bound evidence.
- `needs-input`: a requestable scope, authority, target, fixture, governance term, or decision is absent. Deliver every supported part first and name the owner for the missing part.
- `blocked`: safe work requires prohibited access, unavailable authority, secret values, destructive or remote action, or an incompatible identity.
- `failed`: the authorized action ran but a deterministic check or required output failed.

## Non-Responsibilities

Adjacent capabilities:
- `testing-portfolio-strategy`
- `resilience-and-determinism`
- `defect-remediation`
- `completion-evidence-gate`

Never silently expand source, command, browser, data, credential, local-system, provider, or remote authority. Independent review, QA, audit, evidence acquisition, analysis, and triage never repair source. Setup and authentication never imply authority to perform the downstream action.
