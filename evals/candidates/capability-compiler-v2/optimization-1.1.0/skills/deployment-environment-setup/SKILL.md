---
name: deployment-environment-setup
description: "Prepare local deployment configuration, provider choice, environment boundaries, secret references, and dry-run instructions without provisioning or deploying. Use when An application needs local deployment configuration, environment boundaries and a dry-run plan for a chosen provider; Someone asks which platform adapter, health check and rollback steps a project needs before any provisioning. Do not use for: Trigger the approved deployment workflow after readiness passes (-> deployment-trigger-execution); Deploy the Web application through the selected hosting provider (-> web-hosting-deployment)."
---

# Deployment Environment Setup

## Responsibility

Prepare local deployment configuration, provider choice, environment boundaries, secret references, and dry-run instructions without provisioning or deploying.

## Trigger

Use when the request matches any of:
- An application needs local deployment configuration, environment boundaries and a dry-run plan for a chosen provider
- Someone asks which platform adapter, health check and rollback steps a project needs before any provisioning

Do not use when:
- Trigger the approved deployment workflow after readiness passes. Route to `deployment-trigger-execution`.
- Deploy the Web application through the selected hosting provider. Route to `web-hosting-deployment`.

## Required Inputs

- Application, providers, environments, secrets policy, target, and deployment constraints.

## Procedure

1. Freeze application artifact, provider options, environments, regions, domains, build and runtime settings, secret reference names, identities, quotas, costs, health criteria, and rollback requirements.
2. Select or document a provider adapter from approved constraints and separate local configuration from provider resources.
3. Write only authorized local config candidates, templates, dry-run commands, and environment validation artifacts; never place secret values in source.
4. Validate schema and local dry run where available, then return provider handoff, unknowns, and teardown or rollback plan without provisioning.

## Domain Guidance

- Detect the platform from repository files (for example fly.toml, vercel.json, netlify.toml, render.yaml, Dockerfile, workflow files) and derive its adapter, URL pattern, status command and health check.
- Never write a realistic-looking connection string, key or token in any file or command. Reference secrets by name through environment variables or the provider's secret store, and show placeholders that cannot be mistaken for real values.
- Required output block: platform, production URL, deploy workflow or trigger, status command, merge method, project type, post-deploy health check, pre-merge hook, deploy trigger, and rollback plan.

## Output Contract

Produce:
- local deployment configuration candidate
- environment and secret-reference contract
- dry-run and validation evidence
- provider handoff and teardown plan
- deploy configuration block (platform, URL, workflow, status command, merge method, project type, health check, hooks, rollback) consumed by readiness and trigger Skills

Every material command, request, observation, provider response, finding, decision recommendation, or completion claim must bind to exact target identity and current evidence or be labeled assumption/unknown.

Deliver each output as the artifact itself (tables, commands, patches, plans, records), not as a description of how it would be produced.

## Coverage

- `local-config-only`
- `provider-adapter`
- `environment-boundary`
- `secret-references`
- `dry-run`
- `teardown-plan`
- `no-provision`

## Hard Gates

- Environment setup writes local configuration only; it cannot create provider resources, credentials, domains, environments, deployments, or production state.
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

## Human Decision Authority

The Skill may return evidence, options, findings, and a recommendation. Merge, deploy, rollback, risk acceptance, incident closure, provider configuration, identity change, adoption, persistence, and release decisions remain explicit human decisions under the declared action identity.

## Status Mapping

- `passed`: the atomic output and every gate have current target-bound evidence.
- `needs-input`: a requestable target, source, authority, evidence, governance term, or decision is absent. Deliver every supported part first and name the owner for the missing part.
- `blocked`: safe work requires prohibited access, unavailable authority, secret values, stale evidence, or an incompatible identity.
- `failed`: the authorized action ran but a deterministic gate or required output failed.

## Non-Responsibilities

Adjacent capabilities:
- `deployment-trigger-execution`
- `web-hosting-deployment`
- `edge-worker-deployment`
- `kubernetes-application-deployment`

Never silently expand local, repository, provider, production, telemetry, incident, or release authority. Preflight never changes; observation never recovers; coordination never performs specialist actions; rollback never invents a target; one remote authorization never cascades to another action.
