---
name: kubernetes-deployment-readiness
description: "Read-only assess Kubernetes workload, cluster, identity, policy, scaling, networking, migration, health, and rollback readiness before deployment. Use when A Kubernetes workload needs a read-only go/no-go before deployment covering rollout, scaling, policy and rollback; Manifests or a cluster must be checked against AKS Automatic or platform safeguards before anything is applied. Do not use for: Deploy the approved manifests and image to the cluster (-> kubernetes-application-deployment); Troubleshoot missing APM signals after deployment (-> apm-instrumentation-troubleshooting)."
---

# Kubernetes Deployment Readiness

## Responsibility

Read-only assess Kubernetes workload, cluster, identity, policy, scaling, networking, migration, health, and rollback readiness before deployment.

## Trigger

Use when the request matches any of:
- A Kubernetes workload needs a read-only go/no-go before deployment covering rollout, scaling, policy and rollback
- Manifests or a cluster must be checked against AKS Automatic or platform safeguards before anything is applied

Do not use when:
- Deploy the approved manifests and image to the cluster. Route to `kubernetes-application-deployment`.
- Troubleshoot missing APM signals after deployment. Route to `apm-instrumentation-troubleshooting`.

## Required Inputs

- Cluster and workload configuration, provider controls, expected traffic, failure budget, and deployment plan.

## Procedure

1. Freeze target cluster, namespace, workload, manifest and image identities, read-only credentials, policies, quotas, dependencies, migrations, traffic, health, and rollback requirements.
2. Use only authorized read-only provider or Kubernetes evidence to inspect APIs, versions, nodes, quotas, identities, policies, secrets references, networking, storage, probes, resources, scaling, disruption, and current conflicts.
3. Run schema or server dry-run only if it is guaranteed non-mutating and authorized; otherwise mark it unavailable.
4. Return concrete recommended values for rollout strategy, autoscaling and disruption budgets, each with its arithmetic, instead of naming the topic only.
5. Return ready or blocked with evidence, unexpected diffs, safeguards, missing inputs, and exact deployment prerequisites; never apply or patch resources.

## Domain Guidance

- Severity taxonomy per issue: incompatible (migration blocker), requiresChanges, autoFixed by the platform, cluster-config. Order blockers first; group by constraint id when more than 10 issues.
- Per-issue record: constraint id, severity, affected namespace/resource (Kind), current value, required value, fix summary, documentation link.
- AKS Automatic variant: check container resource requests and limits, probes, non-root and privilege settings, and disallowed host access against the safeguard constraints.
- Give concrete rollout values when the plan lacks them (for example maxUnavailable 0, maxSurge 1, replica count, PodDisruptionBudget minAvailable, HPA bounds) and compute rollback cost arithmetic explicitly.

## Output Contract

Produce:
- Kubernetes readiness assessment
- cluster and workload evidence
- blocker and safeguard register
- deployment prerequisites and rollback requirements
- per-issue severity record with current and required values

Every material command, request, observation, provider response, finding, decision recommendation, or completion claim must bind to exact target identity and current evidence or be labeled assumption/unknown.

Deliver each output as the artifact itself (tables, commands, patches, plans, records), not as a description of how it would be produced.

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

## Status Mapping

- `passed`: the atomic output and every gate have current target-bound evidence.
- `needs-input`: a requestable target, source, authority, evidence, governance term, or decision is absent. Deliver every supported part first and name the owner for the missing part.
- `blocked`: safe work requires prohibited access, unavailable authority, secret values, stale evidence, or an incompatible identity.
- `failed`: the authorized action ran but a deterministic gate or required output failed.

## Non-Responsibilities

Adjacent capabilities:
- `kubernetes-application-deployment`
- `observability-agent-installation`
- `cloud-reliability-assessment`
- `merge-and-deploy-readiness`
- `apm-instrumentation-troubleshooting`

Never silently expand local, repository, provider, production, telemetry, incident, or release authority. Preflight never changes; observation never recovers; coordination never performs specialist actions; rollback never invents a target; one remote authorization never cascades to another action.
