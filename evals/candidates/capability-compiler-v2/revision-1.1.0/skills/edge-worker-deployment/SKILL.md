---
name: edge-worker-deployment
description: "Deploy one immutable edge-worker artifact through one approved provider adapter after build, binding, route, limit, and rollback preflight. Use when One edge worker or serverless function bundle must be deployed with bindings, routes and limits under fresh authorization; A worker deployment needs an exact preflight covering bindings, compatibility date and rollback version. Do not use for: Prepare local edge deployment configuration and dry-run evidence (-> deployment-environment-setup); Observe production signals after the worker deployment (-> deployment-observation); Deploy a static or server-rendered web application project (-> web-hosting-deployment); Deploy containers to an existing Kubernetes cluster (-> kubernetes-application-deployment)."
---

# Edge Worker Deployment

## Responsibility

Deploy one immutable edge-worker artifact through one approved provider adapter after build, binding, route, limit, and rollback preflight.

## Trigger

Use when the request matches any of:
- One edge worker or serverless function bundle must be deployed with bindings, routes and limits under fresh authorization
- A worker deployment needs an exact preflight covering bindings, compatibility date and rollback version

Do not use when:
- Prepare local edge deployment configuration and dry-run evidence. Route to `deployment-environment-setup`.
- Observe production signals after the worker deployment. Route to `deployment-observation`.
- Deploy a static or server-rendered web application project. Route to `web-hosting-deployment`.
- Deploy containers to an existing Kubernetes cluster. Route to `kubernetes-application-deployment`.

## Required Inputs

- Worker source, environment bindings, provider account, compatibility target, and authorization.

## Procedure

1. Verify provider account and project, environment, immutable bundle hash, compatibility/runtime version, bindings by reference, routes, domains, data stores, permissions, limits, cost, health checks, traffic plan, rollback target, and per-action authorization.
2. Build or validate the frozen artifact locally and preview provider diff or dry run without revealing secrets.
3. Perform one provider-specific deploy with bounded timeout and idempotency; do not modify unrelated routes, data, identities, or traffic.
4. Record deployment/version receipt, artifact hash, routes, config identity, status, health handoff, partial failure cleanup, and exact rollback reference.

## Domain Guidance

- A successful dry run proves build and packaging only. It does not prove that bindings, routes or remote resources work, so the health handoff must check them against the live environment.
- After any config or binding change, regenerate the generated types with the project's own command instead of hand-editing them, then run the project's typecheck and tests before the dry run.

## Output Contract

Produce:
- edge deployment receipt
- immutable worker and binding manifest
- route and environment identity
- health handoff and rollback reference

Every material command, request, observation, provider response, finding, decision recommendation, or completion claim must bind to exact target identity and current evidence or be labeled assumption/unknown.

Deliver each output as the artifact itself (tables, commands, patches, plans, records), not as a description of how it would be produced.

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
- `deployment-environment-setup`
- `deployment-observation`
- `release-rollback-execution`
- `release-observability-configuration`
- `web-hosting-deployment`
- `kubernetes-application-deployment`

Never silently expand local, repository, provider, production, telemetry, incident, or release authority. Preflight never changes; observation never recovers; coordination never performs specialist actions; rollback never invents a target; one remote authorization never cascades to another action.
