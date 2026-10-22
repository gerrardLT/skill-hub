---
name: edge-worker-deployment
description: Deploy one immutable edge-worker artifact through one approved provider adapter after build, binding, route, limit, and rollback preflight. Do not use for prepare local edge deployment configuration and dry-run evidence or observe production signals after the worker deployment.
---

# Edge Worker Deployment

## Responsibility

Deploy one immutable edge-worker artifact through one approved provider adapter after build, binding, route, limit, and rollback preflight.

## Trigger

Use when the requested outcome is: Deploy one immutable edge-worker artifact through one approved provider adapter after build, binding, route, limit, and rollback preflight.

Do not use when:
- Prepare local edge deployment configuration and dry-run evidence. Route to `deployment-environment-setup`.
- Observe production signals after the worker deployment. Route to `deployment-observation`.

## Required Inputs

- Worker source, environment bindings, provider account, compatibility target, and authorization.

Also require exact repository, provider, environment, service, incident, release, artifact, telemetry, or local destination identity; authority; evidence window; and recovery or cleanup where applicable.

## Procedure

1. Verify provider account and project, environment, immutable bundle hash, compatibility/runtime version, bindings by reference, routes, domains, data stores, permissions, limits, cost, health checks, traffic plan, rollback target, and per-action authorization.
2. Build or validate the frozen artifact locally and preview provider diff or dry run without revealing secrets.
3. Perform one provider-specific deploy with bounded timeout and idempotency; do not modify unrelated routes, data, identities, or traffic.
4. Record deployment/version receipt, artifact hash, routes, config identity, status, health handoff, partial failure cleanup, and exact rollback reference.

## Output Contract

Produce:
- edge deployment receipt
- immutable worker and binding manifest
- route and environment identity
- health handoff and rollback reference

Every material command, request, observation, provider response, finding, decision recommendation, or completion claim must bind to exact target identity and current evidence or be labeled assumption/unknown.

## Coverage

- `immutable-worker`
- `bindings`
- `routes`
- `compatibility-version`
- `limits`
- `per-action-authorization`
- `rollback-target`

## Hard Gates

- Edge deployment requires exact immutable code, bindings, routes, limits, traffic scope, health criteria, and rollback target; wildcard route or binding changes and unrelated resource mutations are blocked.
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
