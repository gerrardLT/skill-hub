---
name: web-hosting-deployment
description: "Deploy one immutable Web application artifact through one selected hosting provider adapter with exact environment, configuration, health, domain, and rollback controls. Use when One web application artifact must be deployed through a hosting provider's CLI or API with exact environment and domain controls; Someone asks for the exact provider deploy command, preview diff and rollback target for a specific project. Do not use for: Prepare local hosting configuration and dry-run evidence first (-> deployment-environment-setup); Observe the deployment and production health after the provider action (-> deployment-observation); Deploy an edge worker or serverless bundle (-> edge-worker-deployment); Deploy containers to an existing Kubernetes cluster (-> kubernetes-application-deployment); Push the commit that triggers a Git-integrated provider deployment (-> remote-git-push)."
---

# Web Hosting Deployment

## Responsibility

Deploy one immutable Web application artifact through one selected hosting provider adapter with exact environment, configuration, health, domain, and rollback controls.

## Trigger

Use when the request matches any of:
- One web application artifact must be deployed through a hosting provider's CLI or API with exact environment and domain controls
- Someone asks for the exact provider deploy command, preview diff and rollback target for a specific project

Do not use when:
- Prepare local hosting configuration and dry-run evidence first. Route to `deployment-environment-setup`.
- Observe the deployment and production health after the provider action. Route to `deployment-observation`.
- Deploy an edge worker or serverless bundle. Route to `edge-worker-deployment`.
- Deploy containers to an existing Kubernetes cluster. Route to `kubernetes-application-deployment`.
- Push the commit that triggers a Git-integrated provider deployment. Route to `remote-git-push`.

## Required Inputs

- Build artifact, provider project, environment, secrets boundary, deployment plan, and authorization.

## Procedure

1. Select the deploy method from link and Git remote state; if the provider deploys from Git, hand off to remote-git-push and stop.
2. Verify provider and project, environment, immutable artifact or commit digest, build config, runtime, regions, domains, environment-variable references, identity, cache, migrations, preview diff, health, timeout, traffic, rollback target, cost, and fresh per-action authorization.
3. Build or validate the frozen artifact and preview exact provider changes without exposing secret values.
4. Perform one bounded deploy to the exact environment; do not merge, change unrelated domains or projects, rotate credentials, or auto-promote beyond authorization.
5. Record deployment URL and immutable ID, provider receipt, artifact and config identity, status, health handoff, partial-failure cleanup, and rollback reference.

## Domain Guidance

- Select the method first: linked project with a Git remote (deploy happens on push: hand off to remote-git-push and stop), linked project without a remote (CLI deploy), unlinked project (tarball or CLI deploy with explicit project binding). This Skill covers CLI and API deploys only.
- Tarball or CLI deploys exclude node_modules, .git and .env by default; state the exclusions in the preview.
- Browser-exposed build variables such as VITE_ are not secrets storage. Domain binding or DNS changes need their own exact authority and must not be folded into a deployment proposal implicitly.

## Output Contract

Produce:
- hosting deployment receipt
- deployment URL and immutable identity
- artifact and configuration evidence
- observation handoff and rollback reference

Every material command, request, observation, provider response, finding, decision recommendation, or completion claim must bind to exact target identity and current evidence or be labeled assumption/unknown.

Deliver each output as the artifact itself (tables, commands, patches, plans, records), not as a description of how it would be produced.

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
- `edge-worker-deployment`
- `kubernetes-application-deployment`
- `remote-git-push`

Never silently expand local, repository, provider, production, telemetry, incident, or release authority. Preflight never changes; observation never recovers; coordination never performs specialist actions; rollback never invents a target; one remote authorization never cascades to another action.
