---
name: web-hosting-deployment
description: Deploy one immutable Web application artifact through one selected hosting provider adapter with exact environment, configuration, health, domain, and rollback controls. Do not use for prepare local hosting configuration and dry-run evidence first or observe the deployment and production health after the provider action.
---

# Web Hosting Deployment

## Responsibility

Deploy one immutable Web application artifact through one selected hosting provider adapter with exact environment, configuration, health, domain, and rollback controls.

## Trigger

Use when the requested outcome is: Deploy one immutable Web application artifact through one selected hosting provider adapter with exact environment, configuration, health, domain, and rollback controls.

Do not use when:
- Prepare local hosting configuration and dry-run evidence first. Route to `deployment-environment-setup`.
- Observe the deployment and production health after the provider action. Route to `deployment-observation`.

## Required Inputs

- Build artifact, provider project, environment, secrets boundary, deployment plan, and authorization.

Also require exact repository, provider, environment, service, incident, release, artifact, telemetry, or local destination identity; authority; evidence window; and recovery or cleanup where applicable.

## Procedure

1. Verify provider and project, environment, immutable artifact or commit digest, build config, runtime, regions, domains, environment-variable references, identity, cache, migrations, preview diff, health, timeout, traffic, rollback target, cost, and fresh per-action authorization.
2. Build or validate the frozen artifact and preview exact provider changes without exposing secret values.
3. Perform one bounded deploy to the exact environment; do not merge, change unrelated domains or projects, rotate credentials, or auto-promote beyond authorization.
4. Record deployment URL and immutable ID, provider receipt, artifact and config identity, status, health handoff, partial-failure cleanup, and rollback reference.

## Output Contract

Produce:
- hosting deployment receipt
- deployment URL and immutable identity
- artifact and configuration evidence
- observation handoff and rollback reference

Every material command, request, observation, provider response, finding, decision recommendation, or completion claim must bind to exact target identity and current evidence or be labeled assumption/unknown.

## Coverage

- `provider-project`
- `environment`
- `artifact-digest`
- `config-identity`
- `domain-traffic`
- `health-gate`
- `rollback-target`

## Hard Gates

- Web deployment requires one exact provider project, environment, immutable artifact, configuration, domain and traffic scope, health gate, and rollback target; preview or identity drift blocks deployment.
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
- `deployment-environment-setup`
- `deployment-observation`
- `release-rollback-execution`
- `release-observability-configuration`

Never silently expand local, repository, provider, production, telemetry, incident, or release authority. Preflight never changes; observation never recovers; coordination never performs specialist actions; rollback never invents a target; one remote authorization never cascades to another action.
