---
name: release-rollback-execution
description: "Execute one exact approved release rollback when current post-deploy evidence meets a predeclared rollback condition, with bounded blast radius and recovery verification. Use when A deployed release met its predeclared rollback condition and one exact provider rollback is authorized; Someone asks for the exact rollback target, blast radius, health verification and receipt for a release. Do not use for: Observe the deployment and recommend rollback without changing production (-> deployment-observation); Coordinate incident roles, communication, and decision log without executing specialist actions (-> incident-response-coordination); Revert through a new commit and push instead of a provider rollback (-> change-packaging-and-versioning)."
---

# Release Rollback Execution

## Responsibility

Execute one exact approved release rollback when current post-deploy evidence meets a predeclared rollback condition, with bounded blast radius and recovery verification.

## Trigger

Use when the request matches any of:
- A deployed release met its predeclared rollback condition and one exact provider rollback is authorized
- Someone asks for the exact rollback target, blast radius, health verification and receipt for a release

Do not use when:
- Observe the deployment and recommend rollback without changing production. Route to `deployment-observation`.
- Coordinate incident roles, communication, and decision log without executing specialist actions. Route to `incident-response-coordination`.
- Revert through a new commit and push instead of a provider rollback. Route to `change-packaging-and-versioning`.

## Required Inputs

- A deployed change, health evidence, provider state, and rollback authorization.

## Procedure

1. Verify incident or release identity, provider and environment, deployed and target artifact identities, triggering evidence, rollback condition, data and migration compatibility, blast radius, traffic, health criteria, timeout, stop conditions, communication owner, exact recovery command or provider action, and fresh per-action authorization.
2. Preview the exact rollback and irreversible consequences; refuse guessed targets, stale evidence, incompatible schema or data, or rollback beyond the authorized service and environment.
3. Perform one bounded rollback, stop on unexpected diff or health failure, and do not repair, redeploy a new version, alter unrelated configuration, or close the incident.
4. Record provider receipt, before and after versions, command or request, status, health verification, partial failure, recovery escalation, and observation handoff.

## Domain Guidance

- Method: provider-native rollback to the named previous release. A revert-commit rollback requires packaging and a push, which belong to change-packaging-and-versioning and remote-git-push under their own authorization; do not perform it here.
- Verify after rollback with the same health criteria that triggered it and record before and after release identity.

## Output Contract

Produce:
- rollback execution receipt
- before and after release identity
- health and recovery evidence
- partial-failure and incident handoff

Every material command, request, observation, provider response, finding, decision recommendation, or completion claim must bind to exact target identity and current evidence or be labeled assumption/unknown.

Deliver each output as the artifact itself (tables, commands, patches, plans, records), not as a description of how it would be produced.

## Coverage

- `exact-recovery-target`
- `rollback-condition`
- `current-evidence`
- `migration-compatibility`
- `blast-radius`
- `health-verification`
- `rollback-receipt`

## Hard Gates

- Rollback requires a named exact recovery target, met predeclared condition, current evidence, migration compatibility, bounded blast radius, health verification, and fresh per-action authorization; observation alone cannot execute it.
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
- `deployment-observation`
- `incident-response-coordination`
- `deployment-trigger-execution`
- `production-canary-monitoring`
- `change-packaging-and-versioning`

Never silently expand local, repository, provider, production, telemetry, incident, or release authority. Preflight never changes; observation never recovers; coordination never performs specialist actions; rollback never invents a target; one remote authorization never cascades to another action.
