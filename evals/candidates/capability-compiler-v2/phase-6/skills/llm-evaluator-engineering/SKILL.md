---
name: llm-evaluator-engineering
description: Implement bounded local or draft-online evaluator definitions and calibration checks against an explicit quality contract; provider activation remains separate. Do not use for run the frozen evaluator across model outputs and produce scores or activate an online provider experiment using the evaluator.
---

# Llm Evaluator Engineering

## Responsibility

Implement bounded local or draft-online evaluator definitions and calibration checks against an explicit quality contract; provider activation remains separate.

## Trigger

Use when the requested outcome is: Implement bounded local or draft-online evaluator definitions and calibration checks against an explicit quality contract; provider activation remains separate.

Do not use when:
- Run the frozen evaluator across model outputs and produce scores. Route to `llm-quality-evaluation`.
- Activate an online provider experiment using the evaluator. Route to `llm-experiment-execution`.

## Required Inputs

- Quality target, classified traces, evaluator mode, judge policy, local workspace, and data-governance boundary.

Also require exact target identity, authority, mutation boundary, evidence consumer, cleanup or rollback, and declared unknowns where applicable.

## Procedure

1. Freeze quality dimensions, observable criteria, trace classes, labels, evaluator mode, judge policy, data governance, workspace, expected errors, and calibration target.
2. Choose deterministic checks before model judges; define inputs, outputs, abstention, invalid cases, parsing, versions, and cost or transfer boundary.
3. Implement the smallest local evaluator, rubric, fixtures, and executable checks; online calls remain stubs or draft configuration unless separately authorized.
4. Calibrate against labeled cases and human disagreement, test adversarial and malformed inputs, record false positives or negatives, and return limitations and activation handoff.

## Output Contract

Produce:
- evaluator definitions and local source
- rubric and labeled calibration fixtures
- local executable check evidence
- limitations and provider-activation handoff

Every material action, command, result, finding, score, capture, provider receipt, or completion claim must bind to exact target identity and current evidence or be labeled assumption/unknown.

## Coverage

- `quality-contract`
- `deterministic-first`
- `versioned-evaluator`
- `calibration`
- `abstention`
- `malformed-input`
- `no-provider-activation`

## Hard Gates

- An evaluator cannot pass from plausible rubric prose: it needs versioned executable behavior, labeled calibration cases, abstention and invalid handling, disagreement evidence, and no unauthorized provider call.
- Preserve source, build, dataset, model, workflow, provider, browser, session, or local-system identity; command, version, exit, duration, artifacts, hashes, limitations, and cleanup must remain explicit when applicable.
- Return `needs-input` when a named owner can provide missing scope, authority, evidence, governance, target, or decision.
- Return `blocked` when proceeding would exceed mutation authority, expose credentials, violate governance, erase failed evidence, perform an undeclared remote or destructive action, or mix independent review with repair.

## Data and Credential Governance

For customer, proprietary, browser, evaluation, experiment, or externally transferred data, require authority, minimization, redaction, retention, access, transfer, deletion, and incident boundaries. Credential and secret values never enter prompts, logs, hashes, receipts, or artifacts. Missing governance returns `needs-input`; prohibited or unavailable authority returns `blocked`.

## Status Mapping

- `passed`: the atomic output and every gate have current target-bound evidence.
- `needs-input`: a requestable scope, authority, target, fixture, governance term, or decision is absent.
- `blocked`: safe work requires prohibited access, unavailable authority, secret values, destructive or remote action, or an incompatible identity.
- `failed`: the authorized action ran but a deterministic check or required output failed.

## Non-Responsibilities

Does not absorb unrelated lifecycle responsibilities or expand provider, workspace, or remote-write authority implicitly.

Adjacent capabilities:
- `llm-quality-evaluation`
- `llm-experiment-execution`
- `evaluation-results-analysis`
- `test-case-design-and-export`

Never silently expand source, command, browser, data, credential, local-system, provider, or remote authority. Independent review, QA, audit, evidence acquisition, analysis, and triage never repair source. Setup and authentication never imply authority to perform the downstream action.
