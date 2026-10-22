---
name: project-context-and-learning-store
description: "Consolidated capability with 2 selectable modes: local-learning-persistence; project-context-and-learning-store. Choose exactly one mode per invocation."
version: 1.1.0-consolidated
modes: [local-learning-persistence, project-context-and-learning-store]
---

# Project Context And Learning Store

## Responsibility

Consolidated capability covering 2 related modes: Persist one validated evidence-bounded learning, metric, review outcome, or project-context record to one approved local destination under privacy, retention, deletion, and rollback controls.; Restore, search, prune, or reconcile records inside one project-isolated local context store under privacy, retention, provenance, and deletion controls; writes of new records route to local-learning-persistence.

## Mode selection

This capability has several distinct modes. Read this table first, pick exactly one
mode for the current request, then follow only that mode's section. Do not blend
modes: each carries its own permission identity, gates, and stop conditions. The
permission column is binding - a run uses the permission of the mode it selected,
never the widest permission in this document.

| Mode | Permission | Use when | Routes elsewhere |
| --- | --- | --- | --- |
| `local-learning-persistence` | `local-system-write-authorized-only` | One already validated learning, metric or review outcome must be written to one approved local store with read-back; A record must be saved with provenance, retention and deletion terms and a rollback | Synthesize current signals into a learning recommendation first (-> feedback-and-continuous-learning-loop); Synchronize  |
| `project-context-and-learning-store` | `local-system-write-authorized-only` | Saved project context or learnings must be restored, searched, pruned or reconciled inside one project-isolated local store; Someone asks to recover the state before a change or to clean up stale reco | Initialize the local memory runtime and project isolation first (-> local-agent-memory-setup); Persist one ordinary life |

## Mode: `local-learning-persistence`

### local-learning-persistence

#### Responsibility

Persist one validated evidence-bounded learning, metric, review outcome, or project-context record to one approved local destination under privacy, retention, deletion, and rollback controls.

#### Trigger

Use when the request matches any of:
- One already validated learning, metric or review outcome must be written to one approved local store with read-back
- A record must be saved with provenance, retention and deletion terms and a rollback path

Do not use when:
- Synthesize current signals into a learning recommendation first. Route to `feedback-and-continuous-learning-loop`.
- Synchronize learning records to an external service or another machine. Route to `project-context-and-learning-store`.
- Create the store or runtime that will hold records. Route to `local-agent-memory-setup`.

#### Required Inputs

- Validated record, project identity, local destination, privacy and retention policy, and local-system write authorization.

#### Procedure

1. Normalize the destination path and reject any key or branch name that would create a subdirectory or escape the approved store.
2. Verify validated record and approval, project and local destination identity, source refs, evidence status, privacy class, minimization, retention, deletion, conflict policy, backup, rollback, and local-system authorization.
3. Reject secrets, credentials, raw customer data beyond approval, unverified inference, unrelated project context, indefinite retention, and any external or cross-machine target.
4. Write one normalized local record and metadata without changing the source evidence or promoting interpretation to fact.
5. Validate read-back, record identity, hash where safe, provenance, retention, deletion path, conflict result, rollback, and explicit no-write or failure outcome.

#### Domain Guidance

- Use the record schema the store or task defines. When none is defined, still deliver an appendable record using these fields as a labelled proposal: type (pattern, pitfall, preference, architecture, tool, operational), key, insight, source, created-at, retention, project id, and optional confidence and files. Never present proposed fields as requirements the task did not state, and never withhold the record because a proposed field is unknown; mark it as an assumption instead.
- Normalize the destination path before writing: resolve to an absolute path under the approved store, reject path separators or traversal in branch or key names, and never build paths by hand from a branch name.
- Write through the store's own logging helper when one exists so slug and directory handling stay consistent.
- Local memory split: local-agent-memory-setup creates the runtime, local-learning-persistence writes one new record, project-context-and-learning-store restores, searches, prunes and reconciles existing records.

#### Output Contract

Produce:
- persisted local learning identity
- source, evidence-status, and provenance metadata
- retention and deletion path
- read-back, hash, conflict, and rollback evidence
- normalized record in the store's schema, or in a labelled proposed schema

Every material command, request, observation, provider response, finding, decision recommendation, or completion claim must bind to exact target identity and current evidence or be labeled assumption/unknown.

Deliver each output as the artifact itself (tables, commands, patches, plans, records), not as a description of how it would be produced.

#### Coverage

- `one-validated-record`
- `local-only`
- `evidence-status`
- `provenance`
- `retention`
- `deletion`
- `read-back`
- `rollback`

#### Hard Gates

- Local persistence accepts one validated approved record only; secrets, unverified inference, unrelated context, external synchronization, and indefinite retention are blocked.
- Preflight never changes remote state; observation never executes recovery; coordination never performs specialist actions; one remote authorization never cascades.
- Preserve source, ref, pull request, artifact, release, environment, provider, service, incident, telemetry, baseline, or local-record identity; authority, evidence, limitations, cleanup, and recovery remain explicit.
- Return `needs-input` when a named owner can supply missing scope, target, authority, data governance, evidence, rollback, or decision.
- Return `blocked` when proceeding would expose credentials, exceed mutation authority, use stale evidence, mix readiness with action, mix observation with rollback, or perform undeclared remote or production work.
- Deliver every part the supplied evidence and authority support, label assumptions, and list each missing item with the owner who can supply it; `needs-input` or `blocked` applies to the unsupported part, not to the whole deliverable.

#### Forbidden Actions

- request, reveal, print, persist, hash, or transmit credential or secret values
- perform repository, provider, production, telemetry, incident, local-system, deployment, merge, or rollback mutation outside the exact atomic scope and fresh per-action authorization
- invent commands, provider receipts, deployment status, production evidence, incident actions, rollback result, approval, or release evidence
- combine readiness with action, observation with rollback, coordination with mitigation execution, or learning with unapproved persistence
- claim evaluation, approval, release, or completion evidence that has not been produced

#### Data and Credential Governance

For customer, production, incident, telemetry, trace, log, browser, or externally transferred data, require authority, minimization, redaction, sampling, access, region, retention, deletion, and incident boundaries. Credential and secret values never enter prompts, logs, hashes, receipts, or artifacts. Missing governance returns `needs-input`; prohibited or unavailable authority returns `blocked`.

#### Human Decision Authority

The Skill may return evidence, options, findings, and a recommendation. Merge, deploy, rollback, risk acceptance, incident closure, provider configuration, identity change, adoption, persistence, and release decisions remain explicit human decisions under the declared action identity.

#### Remote or Local-System Action Boundary

This Skill defines an action contract and does not execute the action by itself. Any real provider, repository, production, external-session, or local-system write requires fresh per-action authorization, one exact target and immutable input identity, preview or dry run where available, idempotency, durable receipt, bounded failure handling, and rollback, revocation, deletion, cancellation, or cleanup terms as applicable.

#### Status Mapping

- `passed`: the atomic output and every gate have current target-bound evidence.
- `needs-input`: a requestable target, source, authority, evidence, governance term, or decision is absent. Deliver every supported part first and name the owner for the missing part.
- `blocked`: safe work requires prohibited access, unavailable authority, secret values, stale evidence, or an incompatible identity.
- `failed`: the authorized action ran but a deterministic gate or required output failed.

#### Non-Responsibilities

Adjacent capabilities:
- `feedback-and-continuous-learning-loop`
- `engineering-retrospective-and-improvement`
- `project-context-and-learning-store`
- `secrets-and-environment-governance`
- `local-agent-memory-setup`

Never silently expand local, repository, provider, production, telemetry, incident, or release authority. Preflight never changes; observation never recovers; coordination never performs specialist actions; rollback never invents a target; one remote authorization never cascades to another action.

## Mode: `project-context-and-learning-store`

### project-context-and-learning-store

#### Responsibility

Restore, search, prune, or reconcile records inside one project-isolated local context store under privacy, retention, provenance, and deletion controls; writes of new records route to local-learning-persistence.

#### Trigger

Use when the request matches any of:
- Saved project context or learnings must be restored, searched, pruned or reconciled inside one project-isolated local store
- Someone asks to recover the state before a change or to clean up stale records with a deletion trail

Do not use when:
- Initialize the local memory runtime and project isolation first. Route to `local-agent-memory-setup`.
- Persist one ordinary lifecycle artifact in the workspace. Route to `artifact-persistence-and-tool-actions`.
- Write one new validated learning or context record. Route to `local-learning-persistence`.

#### Required Inputs

- Project identity, context artifacts, privacy boundary, retention, synchronization mode, and local-system write authorization when persistence is requested.

#### Procedure

1. Verify project and store identity, selected records, provenance, privacy class, minimization, retention, deletion, local reconciliation mode, conflict policy, and local-system authorization.
2. Perform only the requested local save, restore, search, prune, or same-store reconciliation; never ingest broad logs, secrets, credentials, sibling projects, or external stores by default.
3. Preserve record IDs, source refs, timestamps, versions, tombstones, and conflict outcomes without converting guesses into learnings.
4. Return restorable pointers, local results, counts, hashes where safe, deletion evidence, and rollback or partial-failure status; block cross-machine or external synchronization pending a separate authorized capability.

#### Domain Guidance

- Restore-point record: capture the verbatim prior state with timestamp, branch and commit, and add re-run instructions, so a change can be rolled back and reproduced.
- Pruning writes a tombstone with the reason; reconciliation keeps both versions on conflict and never guesses.
- Local memory split: local-agent-memory-setup creates the runtime, local-learning-persistence writes one new record, project-context-and-learning-store restores, searches, prunes and reconciles existing records.
- Describe an adjacent responsibility generically when no registered capability identity is supplied. Do not invent an unavailable named capability or use it as a blocker.

#### Output Contract

Produce:
- local project context or learning records
- provenance and retention metadata
- search, restore, prune, or reconciliation result
- deletion and conflict evidence

Every material action, command, result, finding, score, capture, provider receipt, or completion claim must bind to exact target identity and current evidence or be labeled assumption/unknown.

Deliver each output as the artifact itself (tables, commands, patches, plans, records), not as a description of how it would be produced.

#### Coverage

- `per-record-opt-in`
- `project-isolation`
- `provenance`
- `retention`
- `deletion`
- `local-only`
- `no-secrets`

#### Hard Gates

- Context storage is opt-in per record and project; secrets, unrelated sessions, unverified claims, indefinite retention, cross-machine sync, and external services are blocked under this local-only identity.
- Independent review, QA, audit, acquisition, analysis, and triage never imply remediation; setup or authentication never implies downstream action authority.
- Preserve source, build, dataset, model, workflow, provider, browser, session, or local-system identity; command, version, exit, duration, artifacts, hashes, limitations, and cleanup must remain explicit when applicable.
- Return `needs-input` when a named owner can provide missing scope, authority, evidence, governance, target, or decision.
- Return `blocked` when proceeding would exceed mutation authority, expose credentials, violate governance, erase failed evidence, perform an undeclared remote or destructive action, or mix independent review with repair.
- Deliver every part the supplied evidence and authority support, label assumptions, and list each missing item with the owner who can supply it; `needs-input` or `blocked` applies to the unsupported part, not to the whole deliverable.

#### Forbidden Actions

- request, reveal, print, persist, hash, or transmit credential or secret values
- perform source, local-system, browser, provider, publication, or remote mutations outside the exact atomic scope and fresh authorization
- invent commands, exits, duration, artifacts, captures, provider receipts, benchmark results, approval, or completion evidence
- combine independent evidence or findings with remediation, risk acceptance, publication, deployment, or release
- claim evaluation, approval, release, or completion evidence that has not been produced

#### Data and Credential Governance

For customer, proprietary, browser, evaluation, experiment, or externally transferred data, require authority, minimization, redaction, retention, access, transfer, deletion, and incident boundaries. Credential and secret values never enter prompts, logs, hashes, receipts, or artifacts. Missing governance returns `needs-input`; prohibited or unavailable authority returns `blocked`.

#### Human Decision Authority

The Skill may return evidence, findings, options, and a recommendation. Scope approval, repair authorization, risk acceptance, publication, experiment submission, local-system change, remote action, and release disposition remain explicit human decisions under the declared identity.

#### External or Local-System Action Boundary

This Skill defines an action contract and does not execute the action by itself. Any real local-system, external-session, provider, publication, or remote write requires fresh per-action authorization, exact target and scope, preview, durable receipt, expiry or cleanup, and rollback, revocation, deletion, or cancellation terms as applicable.

#### Status Mapping

- `passed`: the atomic output and every gate have current target-bound evidence.
- `needs-input`: a requestable scope, authority, target, fixture, governance term, or decision is absent. Deliver every supported part first and name the owner for the missing part.
- `blocked`: safe work requires prohibited access, unavailable authority, secret values, destructive or remote action, or an incompatible identity.
- `failed`: the authorized action ran but a deterministic check or required output failed.

#### Non-Responsibilities

Adjacent capabilities:
- `local-agent-memory-setup`
- `artifact-persistence-and-tool-actions`
- `workflow-runtime-upgrade`
- `secrets-and-environment-governance`
- `local-learning-persistence`

Never silently expand source, command, browser, data, credential, local-system, provider, or remote authority. Independent review, QA, audit, evidence acquisition, analysis, and triage never repair source. Setup and authentication never imply authority to perform the downstream action.
