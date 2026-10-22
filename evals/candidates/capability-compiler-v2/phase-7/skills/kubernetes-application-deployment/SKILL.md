---
name: kubernetes-application-deployment
description: Deploy one immutable application version to an existing Kubernetes platform with validated manifests, identity, rollout, health, and rollback controls under per-action authorization. Do not use for assess cluster, workload, identity, network, scaling, and rollback readiness or install or modify the observability agent on the cluster.
---

# Kubernetes Application Deployment

## Responsibility

Deploy one immutable application version to an existing Kubernetes platform with validated manifests, identity, rollout, health, and rollback controls under per-action authorization.

## Trigger

Use when the requested outcome is: Deploy one immutable application version to an existing Kubernetes platform with validated manifests, identity, rollout, health, and rollback controls under per-action authorization.

Do not use when:
- Assess cluster, workload, identity, network, scaling, and rollback readiness. Route to `kubernetes-deployment-readiness`.
- Install or modify the observability agent on the cluster. Route to `observability-agent-installation`.

## Required Inputs

- Application artifact, existing cluster context, provider adapter, manifests, credentials, and deployment authorization.

Also require exact repository, provider, environment, service, incident, release, artifact, telemetry, or local destination identity; authority; evidence window; and recovery or cleanup where applicable.

## Procedure

1. Verify readiness report, cluster and context, namespace, workload, immutable image digest, reviewed manifest hashes, service account, secret references, policy, resources, probes, networking, autoscaling, migration order, rollout, disruption, health, timeout, rollback revision, blast radius, and per-action authorization.
2. Preview server-side diff or dry run and reject unexpected resource, namespace, identity, policy, or immutable-field changes.
3. Perform only the approved apply or rollout and bounded wait; stop on health, timeout, policy, migration, or rollout failure without widening scope.
4. Record applied revisions, resource identities, image digest, provider or kubectl evidence, status, partial failure, recovery, observation handoff, and exact rollback reference.

## Output Contract

Produce:
- Kubernetes deployment receipt
- applied resource and image identity
- rollout and health status
- recovery, observation, and rollback handoff

Every material command, request, observation, provider response, finding, decision recommendation, or completion claim must bind to exact target identity and current evidence or be labeled assumption/unknown.

## Coverage

- `cluster-namespace`
- `manifest-hash`
- `image-digest`
- `server-dry-run`
- `rollout-health`
- `blast-radius`
- `rollback-revision`

## Hard Gates

- Kubernetes deployment is bound to one cluster, namespace, manifest set, image digest, identity, rollout, health gate, and rollback revision; readiness failure or unexpected diff blocks apply.
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
- `kubernetes-deployment-readiness`
- `deployment-observation`
- `release-rollback-execution`
- `observability-agent-installation`

Never silently expand local, repository, provider, production, telemetry, incident, or release authority. Preflight never changes; observation never recovers; coordination never performs specialist actions; rollback never invents a target; one remote authorization never cascades to another action.
