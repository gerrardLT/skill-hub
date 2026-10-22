---
name: llm-quality-evaluation
description: Evaluate supplied model outputs with governed deterministic metrics, factuality checks, calibrated judges, human agreement, statistics, and regression comparisons without provider activation. Do not use for implement or revise the evaluator definitions and calibration fixtures or execute a new provider experiment to generate outputs.
---

# Llm Quality Evaluation

## Responsibility

Evaluate supplied model outputs with governed deterministic metrics, factuality checks, calibrated judges, human agreement, statistics, and regression comparisons without provider activation.

## Trigger

Use when the requested outcome is: Evaluate supplied model outputs with governed deterministic metrics, factuality checks, calibrated judges, human agreement, statistics, and regression comparisons without provider activation.

Do not use when:
- Implement or revise the evaluator definitions and calibration fixtures. Route to `llm-evaluator-engineering`.
- Execute a new provider experiment to generate outputs. Route to `llm-experiment-execution`.

## Required Inputs

- Model outputs, references, criteria, annotations, and trusted historical baselines.

Also require exact target identity, authority, mutation boundary, evidence consumer, cleanup or rollback, and declared unknowns where applicable.

## Procedure

1. Freeze output, reference, dataset, model and prompt identities, criteria, evaluator versions, annotations, baseline, statistical plan, and governance boundary.
2. Validate completeness, contamination, label quality, inter-annotator agreement, slice definitions, and evaluator applicability.
3. Run approved local deterministic metrics and supplied or locally available judges; an external LLM Judge requires explicit transfer and provider authorization or remains blocked.
4. Compute scores, confidence or variance, agreement, regressions, failure slices, examples, and evaluator limitations; preserve invalid and failed cases.

## Output Contract

Produce:
- repeatable quality scores
- factuality and groundedness evidence
- human-judge agreement and calibration
- confidence, regression, and failure-slice report

Every material action, command, result, finding, score, capture, provider receipt, or completion claim must bind to exact target identity and current evidence or be labeled assumption/unknown.

## Coverage

- `deterministic-metrics`
- `factuality`
- `judge-calibration`
- `human-agreement`
- `confidence`
- `regression`
- `external-judge-authorization`

## Hard Gates

- External LLM Judge use is not implicit in local evaluation authority; without explicit data-transfer, provider, retention, deletion, and cost authorization, judge-dependent results remain blocked.
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

Does not approve upstream product decisions, expand authority, or perform remote writes beyond its explicit permission identity.

Adjacent capabilities:
- `llm-evaluator-engineering`
- `llm-experiment-execution`
- `evaluation-results-analysis`
- `model-and-workflow-benchmarking`

Never silently expand source, command, browser, data, credential, local-system, provider, or remote authority. Independent review, QA, audit, evidence acquisition, analysis, and triage never repair source. Setup and authentication never imply authority to perform the downstream action.
