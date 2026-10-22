---
name: local-learning-persistence
description: Persist one validated evidence-bounded learning, metric, review outcome, or project-context record to one approved local destination under privacy, retention, deletion, and rollback controls. Do not use for synthesize current signals into a learning recommendation first or synchronize learning records to an external service or another machine.
---

# Local Learning Persistence

## Responsibility

Persist one validated evidence-bounded learning, metric, review outcome, or project-context record to one approved local destination under privacy, retention, deletion, and rollback controls.

## Trigger

Use when the requested outcome is: Persist one validated evidence-bounded learning, metric, review outcome, or project-context record to one approved local destination under privacy, retention, deletion, and rollback controls.

Do not use when:
- Synthesize current signals into a learning recommendation first. Route to `feedback-and-continuous-learning-loop`.
- Synchronize learning records to an external service or another machine. Route to `project-context-and-learning-store`.

## Required Inputs

- Validated record, project identity, local destination, privacy and retention policy, and local-system write authorization.

Also require exact repository, provider, environment, service, incident, release, artifact, telemetry, or local destination identity; authority; evidence window; and recovery or cleanup where applicable.

## Procedure

1. Verify validated record and approval, project and local destination identity, source refs, evidence status, privacy class, minimization, retention, deletion, conflict policy, backup, rollback, and local-system authorization.
2. Reject secrets, credentials, raw customer data beyond approval, unverified inference, unrelated project context, indefinite retention, and any external or cross-machine target.
3. Write one normalized local record and metadata without changing the source evidence or promoting interpretation to fact.
4. Validate read-back, record identity, hash where safe, provenance, retention, deletion path, conflict result, rollback, and explicit no-write or failure outcome.

## Output Contract

Produce:
- persisted local learning identity
- source, evidence-status, and provenance metadata
- retention and deletion path
- read-back, hash, conflict, and rollback evidence

Every material command, request, observation, provider response, finding, decision recommendation, or completion claim must bind to exact target identity and current evidence or be labeled assumption/unknown.

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
- Preserve source, ref, pull request, artifact, release, environment, provider, service, incident, telemetry, baseline, or local-record identity; authority, evidence, limitations, cleanup, and recovery remain explicit.
- Return `needs-input` when a named owner can supply missing scope, target, authority, data governance, evidence, rollback, or decision.
- Return `blocked` when proceeding would expose credentials, exceed mutation authority, use stale evidence, mix readiness with action, mix observation with rollback, or perform undeclared remote or production work.

## Data and Credential Governance

For customer, production, incident, telemetry, trace, log, browser, or externally transferred data, require authority, minimization, redaction, sampling, access, region, retention, deletion, and incident boundaries. Credential and secret values never enter prompts, logs, hashes, receipts, or artifacts. Missing governance returns `needs-input`; prohibited or unavailable authority returns `blocked`.

## Human Decision Authority

The Skill may return evidence, options, findings, and a recommendation. Merge, deploy, rollback, risk acceptance, incident closure, provider configuration, identity change, adoption, persistence, and release decisions remain explicit human decisions under the declared action identity.

## Remote or Local-System Action Boundary

This candidate defines an action contract, but Phase 7 candidate construction does not execute the action. Any real provider, repository, production, external-session, or local-system write requires fresh per-action authorization, one exact target and immutable input identity, preview or dry run where available, idempotency, durable receipt, bounded failure handling, and rollback, revocation, deletion, cancellation, or cleanup terms as applicable.

## Status Mapping

- `passed`: the atomic output and every gate have current target-bound evidence.
- `needs-input`: a requestable target, source, authority, evidence, governance term, or decision is absent.
- `blocked`: safe work requires prohibited access, unavailable authority, secret values, stale evidence, or an incompatible identity.
- `failed`: the authorized action ran but a deterministic gate or required output failed.

## Non-Responsibilities

Does not absorb unrelated lifecycle responsibilities or expand provider, workspace, or remote-write authority implicitly.

Adjacent capabilities:
- `feedback-and-continuous-learning-loop`
- `engineering-retrospective-and-improvement`
- `project-context-and-learning-store`
- `secrets-and-environment-governance`

Never silently expand local, repository, provider, production, telemetry, incident, or release authority. Preflight never changes; observation never recovers; coordination never performs specialist actions; rollback never invents a target; one remote authorization never cascades to another action.
