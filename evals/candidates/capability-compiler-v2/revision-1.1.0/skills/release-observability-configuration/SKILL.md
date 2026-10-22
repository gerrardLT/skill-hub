---
name: release-observability-configuration
description: "Configure one provider's release and commit association for exact services and environments under per-action authorization without deploying or changing source. Use when A release and its commits must be registered in an observability provider so new errors can be tied to a release; Someone asks for the exact release identifier, commit range and commands to associate a build with its services. Do not use for: Define and preserve source revision and provenance metadata locally (-> source-metadata-and-provenance); Deploy the release artifact to the provider environment (-> deployment-trigger-execution); Handle model calls, prompts, traces and evaluation telemetry (-> ai-observability-configuration); Handle log collection, parsing, routing and retention (-> log-observability-configuration); Handle monitors and alert routes from approved SLOs (-> monitoring-and-alert-configuration)."
---

# Release Observability Configuration

## Responsibility

Configure one provider's release and commit association for exact services and environments under per-action authorization without deploying or changing source.

## Trigger

Use when the request matches any of:
- A release and its commits must be registered in an observability provider so new errors can be tied to a release
- Someone asks for the exact release identifier, commit range and commands to associate a build with its services

Do not use when:
- Define and preserve source revision and provenance metadata locally. Route to `source-metadata-and-provenance`.
- Deploy the release artifact to the provider environment. Route to `deployment-trigger-execution`.
- Handle model calls, prompts, traces and evaluation telemetry. Route to `ai-observability-configuration`.
- Handle log collection, parsing, routing and retention. Route to `log-observability-configuration`.
- Handle monitors and alert routes from approved SLOs. Route to `monitoring-and-alert-configuration`.

## Required Inputs

- Release naming, repository, build metadata, provider project, credentials, and authorization.

## Procedure

1. Diagnose which half of release wiring already exists and plan only the missing half; use the exact, untruncated release identifier throughout.
2. Verify provider, account, services, environments, repository, exact commit and release IDs, version scheme, artifact digest, source-map or metadata references, retention, access, collision, historical continuity, rollback, and fresh authorization.
3. Preview exact release create or association diff and reject ambiguous, duplicate, mutable, or mismatched identities.
4. Perform one bounded provider configuration action without deployment, source write, service remap, unrelated release change, or issue mutation.
5. Record provider receipt, release identity, linked commits, services and environments, propagation validation, collision status, and rollback or deletion path.

## Domain Guidance

- Diagnose which half of release wiring exists before changing anything: the release tag on events in the SDK, or the release created in CI with commits and a deploy. Do only the missing half.
- Derive the release identifier from the supplied full commit SHA or version exactly; never truncate it, and use the same identifier in every command, verification and rollback step. Use the exact commit range between the previous and current release.
- Discriminator by signal type: this Skill handles release and commit association for services and environments.

## Output Contract

Produce:
- release association receipt
- release, commit, service, and environment map
- propagation and collision evidence
- rollback or deletion record

Every material command, request, observation, provider response, finding, decision recommendation, or completion claim must bind to exact target identity and current evidence or be labeled assumption/unknown.

Deliver each output as the artifact itself (tables, commands, patches, plans, records), not as a description of how it would be produced.

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
- `source-metadata-and-provenance`
- `deployment-trigger-execution`
- `service-identity-remapping`
- `deployment-observation`
- `ai-observability-configuration`
- `log-observability-configuration`
- `monitoring-and-alert-configuration`

Never silently expand local, repository, provider, production, telemetry, incident, or release authority. Preflight never changes; observation never recovers; coordination never performs specialist actions; rollback never invents a target; one remote authorization never cascades to another action.
