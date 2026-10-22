---
name: evaluation-dataset-publication
description: "Publish one frozen versioned evaluation dataset to one exact provider target only under per-action remote-write and data-governance authorization. Use when One frozen, versioned evaluation dataset must be uploaded to one exact provider target after governance checks; Someone asks what must be true (rights, redaction, retention, visibility) before a dataset may be published. Do not use for: Design or modify the local evaluation samples and schema before publication (-> test-case-design-and-export); Run the reviewed LLM experiment against the published dataset (-> llm-experiment-execution)."
---

# Evaluation Dataset Publication

## Responsibility

Publish one frozen versioned evaluation dataset to one exact provider target only under per-action remote-write and data-governance authorization.

## Trigger

Use when the request matches any of:
- One frozen, versioned evaluation dataset must be uploaded to one exact provider target after governance checks
- Someone asks what must be true (rights, redaction, retention, visibility) before a dataset may be published

Do not use when:
- Design or modify the local evaluation samples and schema before publication. Route to `test-case-design-and-export`.
- Run the reviewed LLM experiment against the published dataset. Route to `llm-experiment-execution`.

## Required Inputs

- Approved samples, schema, minimization and redaction policy, provider target, retention policy, and authorization.

## Procedure

1. Verify frozen local manifest and hashes, schema, provenance, consent or license, minimization, redaction, sensitive fields, external-transfer authority, provider target, region, retention, deletion, owner, budget, and per-action authorization.
2. Preview the exact sample count, bytes, metadata, visibility, version identity, and provider request without exposing secret values.
3. Perform one idempotent provider create or upload action, refusing overwrite, public visibility, unrelated target, or mutable latest aliases unless explicitly authorized.
4. Record provider response, immutable dataset identity, request and local hashes, count, duration, cost if any, retention, deletion or rollback path, and partial-failure cleanup.

## Domain Guidance

- Redaction gaps block every publish target that would carry the affected fields, not only the requested one. When a safer target such as a staging dataset is available after the gaps are fixed, propose it as a conditional path with its own authorization need.
- The proposed action must name a target that satisfies the governance terms; never propose the prohibited production-shared target.

## Output Contract

Produce:
- versioned provider dataset identity
- publication request and receipt
- local-provider hash and count evidence
- governance, retention, deletion, and failure-cleanup record
- conditional alternative target with its own authorization need

Every material action, command, result, finding, score, capture, provider receipt, or completion claim must bind to exact target identity and current evidence or be labeled assumption/unknown.

Deliver each output as the artifact itself (tables, commands, patches, plans, records), not as a description of how it would be produced.

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

## Data and Credential Governance

For customer, proprietary, browser, evaluation, experiment, or externally transferred data, require authority, minimization, redaction, retention, access, transfer, deletion, and incident boundaries. Credential and secret values never enter prompts, logs, hashes, receipts, or artifacts. Missing governance returns `needs-input`; prohibited or unavailable authority returns `blocked`.

## Human Decision Authority

The Skill may return evidence, findings, options, and a recommendation. Scope approval, repair authorization, risk acceptance, publication, experiment submission, local-system change, remote action, and release disposition remain explicit human decisions under the declared identity.

## External or Local-System Action Boundary

This Skill defines an action contract and does not execute the action by itself. Any real local-system, external-session, provider, publication, or remote write requires fresh per-action authorization, exact target and scope, preview, durable receipt, expiry or cleanup, and rollback, revocation, deletion, or cancellation terms as applicable.

## Status Mapping

- `passed`: the atomic output and every gate have current target-bound evidence.
- `needs-input`: a requestable scope, authority, target, fixture, governance term, or decision is absent. Deliver every supported part first and name the owner for the missing part.
- `blocked`: safe work requires prohibited access, unavailable authority, secret values, destructive or remote action, or an incompatible identity.
- `failed`: the authorized action ran but a deterministic check or required output failed.

## Non-Responsibilities

Adjacent capabilities:
- `test-case-design-and-export`
- `llm-experiment-execution`
- `llm-evaluator-engineering`
- `artifact-persistence-and-tool-actions`

Never silently expand source, command, browser, data, credential, local-system, provider, or remote authority. Independent review, QA, audit, evidence acquisition, analysis, and triage never repair source. Setup and authentication never imply authority to perform the downstream action.
