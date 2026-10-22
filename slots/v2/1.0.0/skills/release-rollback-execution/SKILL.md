---
name: release-rollback-execution
description: Execute one exact approved release rollback when current post-deploy evidence meets a predeclared rollback condition, with bounded blast radius and recovery verification. Do not use for observe the deployment and recommend rollback without changing production or coordinate incident roles, communication, and decision log without executing specialist actions.
---

# Release Rollback Execution

## Responsibility

Execute one exact approved release rollback when current post-deploy evidence meets a predeclared rollback condition, with bounded blast radius and recovery verification.

## Trigger

Use when the requested outcome is: Execute one exact approved release rollback when current post-deploy evidence meets a predeclared rollback condition, with bounded blast radius and recovery verification.

Do not use when:
- Observe the deployment and recommend rollback without changing production. Route to `deployment-observation`.
- Coordinate incident roles, communication, and decision log without executing specialist actions. Route to `incident-response-coordination`.

## Required Inputs

- A deployed change, health evidence, provider state, and rollback authorization.

Also require exact repository, provider, environment, service, incident, release, artifact, telemetry, or local destination identity; authority; evidence window; and recovery or cleanup where applicable.

## Procedure

1. Verify incident or release identity, provider and environment, deployed and target artifact identities, triggering evidence, rollback condition, data and migration compatibility, blast radius, traffic, health criteria, timeout, stop conditions, communication owner, exact recovery command or provider action, and fresh per-action authorization.
2. Preview the exact rollback and irreversible consequences; refuse guessed targets, stale evidence, incompatible schema or data, or rollback beyond the authorized service and environment.
3. Perform one bounded rollback, stop on unexpected diff or health failure, and do not repair, redeploy a new version, alter unrelated configuration, or close the incident.
4. Record provider receipt, before and after versions, command or request, status, health verification, partial failure, recovery escalation, and observation handoff.

## Output Contract

Produce:
- rollback execution receipt
- before and after release identity
- health and recovery evidence
- partial-failure and incident handoff

Every material command, request, observation, provider response, finding, decision recommendation, or completion claim must bind to exact target identity and current evidence or be labeled assumption/unknown.

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

Does not approve upstream product decisions, expand authority, or perform remote writes beyond its explicit permission identity.

Adjacent capabilities:
- `deployment-observation`
- `incident-response-coordination`
- `deployment-trigger-execution`
- `production-canary-monitoring`

Never silently expand local, repository, provider, production, telemetry, incident, or release authority. Preflight never changes; observation never recovers; coordination never performs specialist actions; rollback never invents a target; one remote authorization never cascades to another action.
