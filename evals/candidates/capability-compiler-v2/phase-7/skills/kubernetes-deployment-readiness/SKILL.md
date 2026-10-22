---
name: kubernetes-deployment-readiness
description: Read-only assess Kubernetes workload, cluster, identity, policy, scaling, networking, migration, health, and rollback readiness before deployment. Do not use for deploy the approved manifests and image to the cluster or troubleshoot missing apm signals after deployment.
---

# Kubernetes Deployment Readiness

## Responsibility

Read-only assess Kubernetes workload, cluster, identity, policy, scaling, networking, migration, health, and rollback readiness before deployment.

## Trigger

Use when the requested outcome is: Read-only assess Kubernetes workload, cluster, identity, policy, scaling, networking, migration, health, and rollback readiness before deployment.

Do not use when:
- Deploy the approved manifests and image to the cluster. Route to `kubernetes-application-deployment`.
- Troubleshoot missing APM signals after deployment. Route to `apm-instrumentation-troubleshooting`.

## Required Inputs

- Cluster and workload configuration, provider controls, expected traffic, failure budget, and deployment plan.

Also require exact repository, provider, environment, service, incident, release, artifact, telemetry, or local destination identity; authority; evidence window; and recovery or cleanup where applicable.

## Procedure

1. Freeze target cluster, namespace, workload, manifest and image identities, read-only credentials, policies, quotas, dependencies, migrations, traffic, health, and rollback requirements.
2. Use only authorized read-only provider or Kubernetes evidence to inspect APIs, versions, nodes, quotas, identities, policies, secrets references, networking, storage, probes, resources, scaling, disruption, and current conflicts.
3. Run schema or server dry-run only if it is guaranteed non-mutating and authorized; otherwise mark it unavailable.
4. Return ready or blocked with evidence, unexpected diffs, safeguards, missing inputs, and exact deployment prerequisites; never apply or patch resources.

## Output Contract

Produce:
- Kubernetes readiness assessment
- cluster and workload evidence
- blocker and safeguard register
- deployment prerequisites and rollback requirements

Every material command, request, observation, provider response, finding, decision recommendation, or completion claim must bind to exact target identity and current evidence or be labeled assumption/unknown.

## Coverage

- `read-only`
- `cluster-namespace`
- `identity-policy`
- `network-storage`
- `probes-resources`
- `rollback-readiness`
- `no-apply`

## Hard Gates

- Readiness authority is read-only: no apply, patch, rollout, scale, restart, secret read, policy change, or namespace mutation is permitted.
- Preserve source, ref, pull request, artifact, release, environment, provider, service, incident, telemetry, baseline, or local-record identity; authority, evidence, limitations, cleanup, and recovery remain explicit.
- Return `needs-input` when a named owner can supply missing scope, target, authority, data governance, evidence, rollback, or decision.
- Return `blocked` when proceeding would expose credentials, exceed mutation authority, use stale evidence, mix readiness with action, mix observation with rollback, or perform undeclared remote or production work.

## Data and Credential Governance

For customer, production, incident, telemetry, trace, log, browser, or externally transferred data, require authority, minimization, redaction, sampling, access, region, retention, deletion, and incident boundaries. Credential and secret values never enter prompts, logs, hashes, receipts, or artifacts. Missing governance returns `needs-input`; prohibited or unavailable authority returns `blocked`.

## Status Mapping

- `passed`: the atomic output and every gate have current target-bound evidence.
- `needs-input`: a requestable target, source, authority, evidence, governance term, or decision is absent.
- `blocked`: safe work requires prohibited access, unavailable authority, secret values, stale evidence, or an incompatible identity.
- `failed`: the authorized action ran but a deterministic gate or required output failed.

## Non-Responsibilities

Does not absorb unrelated lifecycle responsibilities or expand provider, workspace, or remote-write authority implicitly.

Adjacent capabilities:
- `kubernetes-application-deployment`
- `observability-agent-installation`
- `cloud-reliability-assessment`
- `merge-and-deploy-readiness`

Never silently expand local, repository, provider, production, telemetry, incident, or release authority. Preflight never changes; observation never recovers; coordination never performs specialist actions; rollback never invents a target; one remote authorization never cascades to another action.
