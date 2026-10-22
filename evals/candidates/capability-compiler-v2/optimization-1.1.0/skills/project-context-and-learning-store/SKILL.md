---
name: project-context-and-learning-store
description: "Restore, search, prune, or reconcile records inside one project-isolated local context store under privacy, retention, provenance, and deletion controls; writes of new records route to local-learning-persistence. Use when Saved project context or learnings must be restored, searched, pruned or reconciled inside one project-isolated local store; Someone asks to recover the state before a change or to clean up stale records with a deletion trail. Do not use for: Initialize the local memory runtime and project isolation first (-> local-agent-memory-setup); Persist one ordinary lifecycle artifact in the workspace (-> artifact-persistence-and-tool-actions); Write one new validated learning or context record (-> local-learning-persistence)."
---

# Project Context And Learning Store

## Responsibility

Restore, search, prune, or reconcile records inside one project-isolated local context store under privacy, retention, provenance, and deletion controls; writes of new records route to local-learning-persistence.

## Trigger

Use when the request matches any of:
- Saved project context or learnings must be restored, searched, pruned or reconciled inside one project-isolated local store
- Someone asks to recover the state before a change or to clean up stale records with a deletion trail

Do not use when:
- Initialize the local memory runtime and project isolation first. Route to `local-agent-memory-setup`.
- Persist one ordinary lifecycle artifact in the workspace. Route to `artifact-persistence-and-tool-actions`.
- Write one new validated learning or context record. Route to `local-learning-persistence`.

## Required Inputs

- Project identity, context artifacts, privacy boundary, retention, synchronization mode, and local-system write authorization when persistence is requested.

## Procedure

1. Verify project and store identity, selected records, provenance, privacy class, minimization, retention, deletion, local reconciliation mode, conflict policy, and local-system authorization.
2. Perform only the requested local save, restore, search, prune, or same-store reconciliation; never ingest broad logs, secrets, credentials, sibling projects, or external stores by default.
3. Preserve record IDs, source refs, timestamps, versions, tombstones, and conflict outcomes without converting guesses into learnings.
4. Return restorable pointers, local results, counts, hashes where safe, deletion evidence, and rollback or partial-failure status; block cross-machine or external synchronization pending a separate authorized capability.

## Domain Guidance

- Restore-point record: capture the verbatim prior state with timestamp, branch and commit, and add re-run instructions, so a change can be rolled back and reproduced.
- Pruning writes a tombstone with the reason; reconciliation keeps both versions on conflict and never guesses.
- Local memory split: local-agent-memory-setup creates the runtime, local-learning-persistence writes one new record, project-context-and-learning-store restores, searches, prunes and reconciles existing records.
- Describe an adjacent responsibility generically when no registered capability identity is supplied. Do not invent an unavailable named capability or use it as a blocker.

## Output Contract

Produce:
- local project context or learning records
- provenance and retention metadata
- search, restore, prune, or reconciliation result
- deletion and conflict evidence

Every material action, command, result, finding, score, capture, provider receipt, or completion claim must bind to exact target identity and current evidence or be labeled assumption/unknown.

Deliver each output as the artifact itself (tables, commands, patches, plans, records), not as a description of how it would be produced.

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
- `local-agent-memory-setup`
- `artifact-persistence-and-tool-actions`
- `workflow-runtime-upgrade`
- `secrets-and-environment-governance`
- `local-learning-persistence`

Never silently expand source, command, browser, data, credential, local-system, provider, or remote authority. Independent review, QA, audit, evidence acquisition, analysis, and triage never repair source. Setup and authentication never imply authority to perform the downstream action.
