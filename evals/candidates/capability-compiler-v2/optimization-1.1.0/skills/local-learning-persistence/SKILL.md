---
name: local-learning-persistence
description: "Persist one validated evidence-bounded learning, metric, review outcome, or project-context record to one approved local destination under privacy, retention, deletion, and rollback controls. Use when One already validated learning, metric or review outcome must be written to one approved local store with read-back; A record must be saved with provenance, retention and deletion terms and a rollback path. Do not use for: Synthesize current signals into a learning recommendation first (-> feedback-and-continuous-learning-loop); Synchronize learning records to an external service or another machine (-> project-context-and-learning-store); Create the store or runtime that will hold records (-> local-agent-memory-setup)."
---

# Local Learning Persistence

## Responsibility

Persist one validated evidence-bounded learning, metric, review outcome, or project-context record to one approved local destination under privacy, retention, deletion, and rollback controls.

## Trigger

Use when the request matches any of:
- One already validated learning, metric or review outcome must be written to one approved local store with read-back
- A record must be saved with provenance, retention and deletion terms and a rollback path

Do not use when:
- Synthesize current signals into a learning recommendation first. Route to `feedback-and-continuous-learning-loop`.
- Synchronize learning records to an external service or another machine. Route to `project-context-and-learning-store`.
- Create the store or runtime that will hold records. Route to `local-agent-memory-setup`.

## Required Inputs

- Validated record, project identity, local destination, privacy and retention policy, and local-system write authorization.

## Procedure

1. Normalize the destination path and reject any key or branch name that would create a subdirectory or escape the approved store.
2. Verify validated record and approval, project and local destination identity, source refs, evidence status, privacy class, minimization, retention, deletion, conflict policy, backup, rollback, and local-system authorization.
3. Reject secrets, credentials, raw customer data beyond approval, unverified inference, unrelated project context, indefinite retention, and any external or cross-machine target.
4. Write one normalized local record and metadata without changing the source evidence or promoting interpretation to fact.
5. Validate read-back, record identity, hash where safe, provenance, retention, deletion path, conflict result, rollback, and explicit no-write or failure outcome.

## Domain Guidance

- Use the record schema the store or task defines. When none is defined, still deliver an appendable record using these fields as a labelled proposal: type (pattern, pitfall, preference, architecture, tool, operational), key, insight, source, created-at, retention, project id, and optional confidence and files. Never present proposed fields as requirements the task did not state, and never withhold the record because a proposed field is unknown; mark it as an assumption instead.
- Normalize the destination path before writing: resolve to an absolute path under the approved store, reject path separators or traversal in branch or key names, and never build paths by hand from a branch name.
- Write through the store's own logging helper when one exists so slug and directory handling stay consistent.
- Local memory split: local-agent-memory-setup creates the runtime, local-learning-persistence writes one new record, project-context-and-learning-store restores, searches, prunes and reconciles existing records.

## Output Contract

Produce:
- persisted local learning identity
- source, evidence-status, and provenance metadata
- retention and deletion path
- read-back, hash, conflict, and rollback evidence
- normalized record in the store's schema, or in a labelled proposed schema

Every material command, request, observation, provider response, finding, decision recommendation, or completion claim must bind to exact target identity and current evidence or be labeled assumption/unknown.

Deliver each output as the artifact itself (tables, commands, patches, plans, records), not as a description of how it would be produced.

## Coverage

- `one-validated-record`
- `local-only`
- `evidence-status`
- `provenance`
- `retention`
- `deletion`
- `read-back`
- `rollback`

## Hard Gates

- Local persistence accepts one validated approved record only; secrets, unverified inference, unrelated context, external synchronization, and indefinite retention are blocked.
- Preflight never changes remote state; observation never executes recovery; coordination never performs specialist actions; one remote authorization never cascades.
- Preserve source, ref, pull request, artifact, release, environment, provider, service, incident, telemetry, baseline, or local-record identity; authority, evidence, limitations, cleanup, and recovery remain explicit.
- Return `needs-input` when a named owner can supply missing scope, target, authority, data governance, evidence, rollback, or decision.
- Return `blocked` when proceeding would expose credentials, exceed mutation authority, use stale evidence, mix readiness with action, mix observation with rollback, or perform undeclared remote or production work.
- Deliver every part the supplied evidence and authority support, label assumptions, and list each missing item with the owner who can supply it; `needs-input` or `blocked` applies to the unsupported part, not to the whole deliverable.

## Forbidden Actions

- request, reveal, print, persist, hash, or transmit credential or secret values
- perform repository, provider, production, telemetry, incident, local-system, deployment, merge, or rollback mutation outside the exact atomic scope and fresh per-action authorization
- invent commands, provider receipts, deployment status, production evidence, incident actions, rollback result, approval, or release evidence
- combine readiness with action, observation with rollback, coordination with mitigation execution, or learning with unapproved persistence
- claim evaluation, approval, release, or completion evidence that has not been produced

## Data and Credential Governance

For customer, production, incident, telemetry, trace, log, browser, or externally transferred data, require authority, minimization, redaction, sampling, access, region, retention, deletion, and incident boundaries. Credential and secret values never enter prompts, logs, hashes, receipts, or artifacts. Missing governance returns `needs-input`; prohibited or unavailable authority returns `blocked`.

## Human Decision Authority

The Skill may return evidence, options, findings, and a recommendation. Merge, deploy, rollback, risk acceptance, incident closure, provider configuration, identity change, adoption, persistence, and release decisions remain explicit human decisions under the declared action identity.

## Remote or Local-System Action Boundary

This Skill defines an action contract and does not execute the action by itself. Any real provider, repository, production, external-session, or local-system write requires fresh per-action authorization, one exact target and immutable input identity, preview or dry run where available, idempotency, durable receipt, bounded failure handling, and rollback, revocation, deletion, cancellation, or cleanup terms as applicable.

## Status Mapping

- `passed`: the atomic output and every gate have current target-bound evidence.
- `needs-input`: a requestable target, source, authority, evidence, governance term, or decision is absent. Deliver every supported part first and name the owner for the missing part.
- `blocked`: safe work requires prohibited access, unavailable authority, secret values, stale evidence, or an incompatible identity.
- `failed`: the authorized action ran but a deterministic gate or required output failed.

## Non-Responsibilities

Adjacent capabilities:
- `feedback-and-continuous-learning-loop`
- `engineering-retrospective-and-improvement`
- `project-context-and-learning-store`
- `secrets-and-environment-governance`
- `local-agent-memory-setup`

Never silently expand local, repository, provider, production, telemetry, incident, or release authority. Preflight never changes; observation never recovers; coordination never performs specialist actions; rollback never invents a target; one remote authorization never cascades to another action.
