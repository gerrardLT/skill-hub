---
name: kubernetes-application-deployment
description: "Deploy one immutable application version to an existing Kubernetes platform with validated manifests, identity, rollout, health, and rollback controls under per-action authorization. Use when One container image must be rolled out to an existing Kubernetes cluster with validated manifests and a health gate; Someone asks for the exact dry-run, apply and rollout commands for a release under fresh authorization. Do not use for: Assess cluster, workload, identity, network, scaling, and rollback readiness (-> kubernetes-deployment-readiness); Install or modify the observability agent on the cluster (-> observability-agent-installation); Deploy an edge worker or serverless bundle (-> edge-worker-deployment); Deploy a web application through a hosting provider (-> web-hosting-deployment)."
---

# Kubernetes Application Deployment

## Responsibility

Deploy one immutable application version to an existing Kubernetes platform with validated manifests, identity, rollout, health, and rollback controls under per-action authorization.

## Trigger

Use when the request matches any of:
- One container image must be rolled out to an existing Kubernetes cluster with validated manifests and a health gate
- Someone asks for the exact dry-run, apply and rollout commands for a release under fresh authorization

Do not use when:
- Assess cluster, workload, identity, network, scaling, and rollback readiness. Route to `kubernetes-deployment-readiness`.
- Install or modify the observability agent on the cluster. Route to `observability-agent-installation`.
- Deploy an edge worker or serverless bundle. Route to `edge-worker-deployment`.
- Deploy a web application through a hosting provider. Route to `web-hosting-deployment`.

## Required Inputs

- Application artifact, existing cluster context, provider adapter, manifests, credentials, and deployment authorization.

## Procedure

1. Verify readiness report, cluster and context, namespace, workload, immutable image digest, reviewed manifest hashes, service account, secret references, policy, resources, probes, networking, autoscaling, migration order, rollout, disruption, health, timeout, rollback revision, blast radius, and per-action authorization.
2. Preview server-side diff or dry run and reject unexpected resource, namespace, identity, policy, or immutable-field changes.
3. Perform only the approved apply or rollout and bounded wait; stop on health, timeout, policy, migration, or rollout failure without widening scope.
4. Record applied revisions, resource identities, image digest, provider or kubectl evidence, status, partial failure, recovery, observation handoff, and exact rollback reference.

## Domain Guidance

- When a blocker stops the rollout, still return the exact commands you would run once it clears (context-pinned server dry-run, apply, rollout status and rollback), clearly marked do-not-run until the named blocker is resolved, plus the minimal namespaced Role and RoleBinding needed if RBAC is the blocker.
- Map known deploy failure codes from the platform's failure catalog to a stop or recovery action in the rollout step; an unknown failure stops the rollout and preserves evidence.

## Output Contract

Produce:
- Kubernetes deployment receipt
- applied resource and image identity
- rollout and health status
- recovery, observation, and rollback handoff
- conditional command set marked do-not-run until blockers clear

Every material command, request, observation, provider response, finding, decision recommendation, or completion claim must bind to exact target identity and current evidence or be labeled assumption/unknown.

Deliver each output as the artifact itself (tables, commands, patches, plans, records), not as a description of how it would be produced.

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
- `kubernetes-deployment-readiness`
- `deployment-observation`
- `release-rollback-execution`
- `observability-agent-installation`
- `edge-worker-deployment`
- `web-hosting-deployment`

Never silently expand local, repository, provider, production, telemetry, incident, or release authority. Preflight never changes; observation never recovers; coordination never performs specialist actions; rollback never invents a target; one remote authorization never cascades to another action.
