---
name: release-observability-configuration
description: Configure one provider's release and commit association for exact services and environments under per-action authorization without deploying or changing source. Do not use for define and preserve source revision and provenance metadata locally or deploy the release artifact to the provider environment.
---

# Release Observability Configuration

## Responsibility

Configure one provider's release and commit association for exact services and environments under per-action authorization without deploying or changing source.

## Trigger

Use when the requested outcome is: Configure one provider's release and commit association for exact services and environments under per-action authorization without deploying or changing source.

Do not use when:
- Define and preserve source revision and provenance metadata locally. Route to `source-metadata-and-provenance`.
- Deploy the release artifact to the provider environment. Route to `deployment-trigger-execution`.

## Required Inputs

- Release naming, repository, build metadata, provider project, credentials, and authorization.

Also require exact repository, provider, environment, service, incident, release, artifact, telemetry, or local destination identity; authority; evidence window; and recovery or cleanup where applicable.

## Procedure

1. Verify provider, account, services, environments, repository, exact commit and release IDs, version scheme, artifact digest, source-map or metadata references, retention, access, collision, historical continuity, rollback, and fresh authorization.
2. Preview exact release create or association diff and reject ambiguous, duplicate, mutable, or mismatched identities.
3. Perform one bounded provider configuration action without deployment, source write, service remap, unrelated release change, or issue mutation.
4. Record provider receipt, release identity, linked commits, services and environments, propagation validation, collision status, and rollback or deletion path.

## Output Contract

Produce:
- release association receipt
- release, commit, service, and environment map
- propagation and collision evidence
- rollback or deletion record

Every material command, request, observation, provider response, finding, decision recommendation, or completion claim must bind to exact target identity and current evidence or be labeled assumption/unknown.

## Coverage

- `exact-release`
- `commit-identity`
- `artifact-digest`
- `service-environment`
- `collision-check`
- `no-deploy`
- `rollback`

## Hard Gates

- Release observability requires exact immutable release, commit, artifact, service, and environment identities; association does not prove deployment or authorize provider actions beyond the mapping.
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
- `source-metadata-and-provenance`
- `deployment-trigger-execution`
- `service-identity-remapping`
- `deployment-observation`

Never silently expand local, repository, provider, production, telemetry, incident, or release authority. Preflight never changes; observation never recovers; coordination never performs specialist actions; rollback never invents a target; one remote authorization never cascades to another action.
