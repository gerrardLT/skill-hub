---
name: deployment-environment-setup
description: Prepare local deployment configuration, provider choice, environment boundaries, secret references, and dry-run instructions without provisioning or deploying. Do not use for trigger the approved deployment workflow after readiness passes or deploy the web application through the selected hosting provider.
---

# Deployment Environment Setup

## Responsibility

Prepare local deployment configuration, provider choice, environment boundaries, secret references, and dry-run instructions without provisioning or deploying.

## Trigger

Use when the requested outcome is: Prepare local deployment configuration, provider choice, environment boundaries, secret references, and dry-run instructions without provisioning or deploying.

Do not use when:
- Trigger the approved deployment workflow after readiness passes. Route to `deployment-trigger-execution`.
- Deploy the Web application through the selected hosting provider. Route to `web-hosting-deployment`.

## Required Inputs

- Application, providers, environments, secrets policy, target, and deployment constraints.

Also require exact repository, provider, environment, service, incident, release, artifact, telemetry, or local destination identity; authority; evidence window; and recovery or cleanup where applicable.

## Procedure

1. Freeze application artifact, provider options, environments, regions, domains, build and runtime settings, secret reference names, identities, quotas, costs, health criteria, and rollback requirements.
2. Select or document a provider adapter from approved constraints and separate local configuration from provider resources.
3. Write only authorized local config candidates, templates, dry-run commands, and environment validation artifacts; never place secret values in source.
4. Validate schema and local dry run where available, then return provider handoff, unknowns, and teardown or rollback plan without provisioning.

## Output Contract

Produce:
- local deployment configuration candidate
- environment and secret-reference contract
- dry-run and validation evidence
- provider handoff and teardown plan

Every material command, request, observation, provider response, finding, decision recommendation, or completion claim must bind to exact target identity and current evidence or be labeled assumption/unknown.

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
- Preserve source, ref, pull request, artifact, release, environment, provider, service, incident, telemetry, baseline, or local-record identity; authority, evidence, limitations, cleanup, and recovery remain explicit.
- Return `needs-input` when a named owner can supply missing scope, target, authority, data governance, evidence, rollback, or decision.
- Return `blocked` when proceeding would expose credentials, exceed mutation authority, use stale evidence, mix readiness with action, mix observation with rollback, or perform undeclared remote or production work.

## Human Decision Authority

The Skill may return evidence, options, findings, and a recommendation. Merge, deploy, rollback, risk acceptance, incident closure, provider configuration, identity change, adoption, persistence, and release decisions remain explicit human decisions under the declared action identity.

## Status Mapping

- `passed`: the atomic output and every gate have current target-bound evidence.
- `needs-input`: a requestable target, source, authority, evidence, governance term, or decision is absent.
- `blocked`: safe work requires prohibited access, unavailable authority, secret values, stale evidence, or an incompatible identity.
- `failed`: the authorized action ran but a deterministic gate or required output failed.

## Non-Responsibilities

Does not absorb unrelated lifecycle responsibilities or expand provider, workspace, or remote-write authority implicitly.

Adjacent capabilities:
- `deployment-trigger-execution`
- `web-hosting-deployment`
- `edge-worker-deployment`
- `kubernetes-application-deployment`

Never silently expand local, repository, provider, production, telemetry, incident, or release authority. Preflight never changes; observation never recovers; coordination never performs specialist actions; rollback never invents a target; one remote authorization never cascades to another action.
