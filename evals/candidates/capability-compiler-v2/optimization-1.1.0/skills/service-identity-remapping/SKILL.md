---
name: service-identity-remapping
description: "Remap one telemetry service identity in one exact provider scope after collision, continuity, retention, dashboard, alert, and rollback checks under per-action authorization. Use when A telemetry service name must be renamed in the provider without breaking dashboards, monitors and history; Someone asks what a service remap would affect before it is applied. Do not use for: Define source revision and release metadata carried by telemetry (-> source-metadata-and-provenance); Verify whether instrumentation already emits the expected service and environment identity (-> apm-instrumentation-verification)."
---

# Service Identity Remapping

## Responsibility

Remap one telemetry service identity in one exact provider scope after collision, continuity, retention, dashboard, alert, and rollback checks under per-action authorization.

## Trigger

Use when the request matches any of:
- A telemetry service name must be renamed in the provider without breaking dashboards, monitors and history
- Someone asks what a service remap would affect before it is applied

Do not use when:
- Define source revision and release metadata carried by telemetry. Route to `source-metadata-and-provenance`.
- Verify whether instrumentation already emits the expected service and environment identity. Route to `apm-instrumentation-verification`.

## Required Inputs

- Current service names, desired taxonomy, provider configuration, downstream dashboards, and authorization.

## Procedure

1. Verify provider, account or org, environment, old and new identity, source or runtime emitters, collision search, aliases, retention, dashboards, monitors, SLOs, ownership, access, historical continuity, propagation, rollback, and fresh authorization.
2. Preview exact remapping and affected queries, routes, tags, alerts, and integrations; block on collision or ambiguous producers.
3. Perform one bounded provider configuration change without altering instrumentation, unrelated services, or deleting historical data.
4. Record provider receipt, old and new mapping, affected resources, propagation verification, residual gaps, and rollback command or action.

## Domain Guidance

- Show an impact preview of every monitor and dashboard that references the old name before planning the rule. For an inferred-entity remap, confirm the outbound spans carry peer.service first.

## Output Contract

Produce:
- service identity remap receipt
- collision and continuity evidence
- affected dashboard, alert, and integration map
- verification and rollback record

Every material command, request, observation, provider response, finding, decision recommendation, or completion claim must bind to exact target identity and current evidence or be labeled assumption/unknown.

Deliver each output as the artifact itself (tables, commands, patches, plans, records), not as a description of how it would be produced.

## Coverage

- `old-new-identity`
- `collision-check`
- `historical-continuity`
- `affected-resources`
- `per-action-authorization`
- `rollback`

## Hard Gates

- Identity remapping requires collision-free exact old and new identities, bounded provider scope, continuity plan, affected-resource inventory, verification, and rollback; renaming telemetry emitters is separate.
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
- `apm-instrumentation-verification`
- `release-observability-configuration`
- `monitoring-and-alert-configuration`

Never silently expand local, repository, provider, production, telemetry, incident, or release authority. Preflight never changes; observation never recovers; coordination never performs specialist actions; rollback never invents a target; one remote authorization never cascades to another action.
