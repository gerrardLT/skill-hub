---
name: evaluation-dataset-publication
description: Publish one frozen versioned evaluation dataset to one exact provider target only under per-action remote-write and data-governance authorization. Do not use for design or modify the local evaluation samples and schema before publication or run the reviewed llm experiment against the published dataset.
---

# Evaluation Dataset Publication

## Responsibility

Publish one frozen versioned evaluation dataset to one exact provider target only under per-action remote-write and data-governance authorization.

## Trigger

Use when the requested outcome is: Publish one frozen versioned evaluation dataset to one exact provider target only under per-action remote-write and data-governance authorization.

Do not use when:
- Design or modify the local evaluation samples and schema before publication. Route to `test-case-design-and-export`.
- Run the reviewed LLM experiment against the published dataset. Route to `llm-experiment-execution`.

## Required Inputs

- Approved samples, schema, minimization and redaction policy, provider target, retention policy, and authorization.

Also require exact target identity, authority, mutation boundary, evidence consumer, cleanup or rollback, and declared unknowns where applicable.

## Procedure

1. Verify frozen local manifest and hashes, schema, provenance, consent or license, minimization, redaction, sensitive fields, external-transfer authority, provider target, region, retention, deletion, owner, budget, and per-action authorization.
2. Preview the exact sample count, bytes, metadata, visibility, version identity, and provider request without exposing secret values.
3. Perform one idempotent provider create or upload action, refusing overwrite, public visibility, unrelated target, or mutable latest aliases unless explicitly authorized.
4. Record provider response, immutable dataset identity, request and local hashes, count, duration, cost if any, retention, deletion or rollback path, and partial-failure cleanup.

## Output Contract

Produce:
- versioned provider dataset identity
- publication request and receipt
- local-provider hash and count evidence
- governance, retention, deletion, and failure-cleanup record

Every material action, command, result, finding, score, capture, provider receipt, or completion claim must bind to exact target identity and current evidence or be labeled assumption/unknown.

## Coverage

- `per-action-authorization`
- `exact-provider-target`
- `frozen-version`
- `redaction`
- `external-transfer`
- `idempotency`
- `publication-receipt`
- `deletion-path`

## Hard Gates

- Remote dataset publication is one per-action-authorized write to an exact provider target and version; missing rights, redaction, transfer, retention, deletion, visibility, idempotency, or cleanup terms blocks publication.
- Preserve source, build, dataset, model, workflow, provider, browser, session, or local-system identity; command, version, exit, duration, artifacts, hashes, limitations, and cleanup must remain explicit when applicable.
- Return `needs-input` when a named owner can provide missing scope, authority, evidence, governance, target, or decision.
- Return `blocked` when proceeding would exceed mutation authority, expose credentials, violate governance, erase failed evidence, perform an undeclared remote or destructive action, or mix independent review with repair.

## Data and Credential Governance

For customer, proprietary, browser, evaluation, experiment, or externally transferred data, require authority, minimization, redaction, retention, access, transfer, deletion, and incident boundaries. Credential and secret values never enter prompts, logs, hashes, receipts, or artifacts. Missing governance returns `needs-input`; prohibited or unavailable authority returns `blocked`.

## Human Decision Authority

The Skill may return evidence, findings, options, and a recommendation. Scope approval, repair authorization, risk acceptance, publication, experiment submission, local-system change, remote action, and release disposition remain explicit human decisions under the declared identity.

## External or Local-System Action Boundary

This candidate defines an action contract but Phase 6 candidate construction and evaluation planning do not execute the action. Any real local-system, external-session, provider, publication, or remote write requires fresh per-action authorization, exact target and scope, preview, durable receipt, expiry or cleanup, and rollback, revocation, deletion, or cancellation terms as applicable.

## Status Mapping

- `passed`: the atomic output and every gate have current target-bound evidence.
- `needs-input`: a requestable scope, authority, target, fixture, governance term, or decision is absent.
- `blocked`: safe work requires prohibited access, unavailable authority, secret values, destructive or remote action, or an incompatible identity.
- `failed`: the authorized action ran but a deterministic check or required output failed.

## Non-Responsibilities

Does not absorb unrelated lifecycle responsibilities or expand provider, workspace, or remote-write authority implicitly.

Adjacent capabilities:
- `test-case-design-and-export`
- `llm-experiment-execution`
- `llm-evaluator-engineering`
- `artifact-persistence-and-tool-actions`

Never silently expand source, command, browser, data, credential, local-system, provider, or remote authority. Independent review, QA, audit, evidence acquisition, analysis, and triage never repair source. Setup and authentication never imply authority to perform the downstream action.
