---
name: project-context-and-learning-store
description: Save, restore, search, prune, or reconcile explicitly selected records inside one project-isolated local context store under privacy, retention, provenance, and deletion controls. Do not use for initialize the local memory runtime and project isolation first or persist one ordinary lifecycle artifact in the workspace.
---

# Project Context And Learning Store

## Responsibility

Save, restore, search, prune, or reconcile explicitly selected records inside one project-isolated local context store under privacy, retention, provenance, and deletion controls.

## Trigger

Use when the requested outcome is: Save, restore, search, prune, or reconcile explicitly selected records inside one project-isolated local context store under privacy, retention, provenance, and deletion controls.

Do not use when:
- Initialize the local memory runtime and project isolation first. Route to `local-agent-memory-setup`.
- Persist one ordinary lifecycle artifact in the workspace. Route to `artifact-persistence-and-tool-actions`.

## Required Inputs

- Project identity, context artifacts, privacy boundary, retention, synchronization mode, and local-system write authorization when persistence is requested.

Also require exact target identity, authority, mutation boundary, evidence consumer, cleanup or rollback, and declared unknowns where applicable.

## Procedure

1. Verify project and store identity, selected records, provenance, privacy class, minimization, retention, deletion, local reconciliation mode, conflict policy, and local-system authorization.
2. Perform only the requested local save, restore, search, prune, or same-store reconciliation; never ingest broad logs, secrets, credentials, sibling projects, or external stores by default.
3. Preserve record IDs, source refs, timestamps, versions, tombstones, and conflict outcomes without converting guesses into learnings.
4. Return restorable pointers, local results, counts, hashes where safe, deletion evidence, and rollback or partial-failure status; block cross-machine or external synchronization pending a separate authorized capability.

## Output Contract

Produce:
- local project context or learning records
- provenance and retention metadata
- search, restore, prune, or reconciliation result
- deletion and conflict evidence

Every material action, command, result, finding, score, capture, provider receipt, or completion claim must bind to exact target identity and current evidence or be labeled assumption/unknown.

## Coverage

- `per-record-opt-in`
- `project-isolation`
- `provenance`
- `retention`
- `deletion`
- `local-only`
- `no-secrets`

## Hard Gates

- Context storage is opt-in per record and project; secrets, unrelated sessions, unverified claims, indefinite retention, cross-machine sync, and external services are blocked under this local-only identity.
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
- `local-agent-memory-setup`
- `artifact-persistence-and-tool-actions`
- `workflow-runtime-upgrade`
- `secrets-and-environment-governance`

Never silently expand source, command, browser, data, credential, local-system, provider, or remote authority. Independent review, QA, audit, evidence acquisition, analysis, and triage never repair source. Setup and authentication never imply authority to perform the downstream action.
