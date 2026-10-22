---
name: cloud-and-edge-application-deployment
description: "Consolidated capability with 5 selectable modes: deployment-environment-setup; edge-worker-deployment; kubernetes-application-deployment; kubernetes-deployment-readiness; web-hosting-deployment. Choose exactly one mode per invocation."
version: 1.1.0-consolidated
modes: [deployment-environment-setup, edge-worker-deployment, kubernetes-application-deployment, kubernetes-deployment-readiness, web-hosting-deployment]
---

# Cloud And Edge Application Deployment

## Responsibility

Consolidated capability covering 5 related modes: Prepare local deployment configuration, provider choice, environment boundaries, secret references, and dry-run instructions without provisioning or deploying.; Deploy one immutable edge-worker artifact through one approved provider adapter after build, binding, route, limit, and rollback preflight.; Deploy one immutable application version to an existing Kubernetes platform with validated manifests, identity, rollout, health, and rollback controls under per-action authorization.; Read-only assess Kubernetes workload, cluster, identity, policy, scaling, networking, migration, health, and rollback readiness before deployment.; Deploy one immutable Web application artifact through one selected hosting provider adapter with exact environment, configuration, health, domain, and rollback controls.

## Mode selection

This capability has several distinct modes. Read this table first, pick exactly one
mode for the current request, then follow only that mode's section. Do not blend
modes: each carries its own permission identity, gates, and stop conditions. The
permission column is binding - a run uses the permission of the mode it selected,
never the widest permission in this document.

| Mode | Permission | Use when | Routes elsewhere |
| --- | --- | --- | --- |
| `deployment-environment-setup` | `workspace-write` | An application needs local deployment configuration, environment boundaries and a dry-run plan for a chosen provider; Someone asks which platform adapter, health check and rollback steps a project nee | Trigger the approved deployment workflow after readiness passes (-> deployment-trigger-execution); Deploy the Web applic |
| `edge-worker-deployment` | `remote-write-authorized-only` | One edge worker or serverless function bundle must be deployed with bindings, routes and limits under fresh authorization; A worker deployment needs an exact preflight covering bindings, compatibility | Prepare local edge deployment configuration and dry-run evidence (-> deployment-environment-setup); Observe production s |
| `kubernetes-application-deployment` | `remote-write-authorized-only` | One container image must be rolled out to an existing Kubernetes cluster with validated manifests and a health gate; Someone asks for the exact dry-run, apply and rollout commands for a release under  | Assess cluster, workload, identity, network, scaling, and rollback readiness (-> kubernetes-deployment-readiness); Insta |
| `kubernetes-deployment-readiness` | `external-read` | A Kubernetes workload needs a read-only go/no-go before deployment covering rollout, scaling, policy and rollback; Manifests or a cluster must be checked against AKS Automatic or platform safeguards b | Deploy the approved manifests and image to the cluster (-> kubernetes-application-deployment); Troubleshoot missing APM  |
| `web-hosting-deployment` | `remote-write-authorized-only` | One web application artifact must be deployed through a hosting provider's CLI or API with exact environment and domain controls; Someone asks for the exact provider deploy command, preview diff and r | Prepare local hosting configuration and dry-run evidence first (-> deployment-environment-setup); Observe the deployment |

## Mode: `deployment-environment-setup`

### deployment-environment-setup

#### Responsibility

Prepare local deployment configuration, provider choice, environment boundaries, secret references, and dry-run instructions without provisioning or deploying.

#### Trigger

Use when the request matches any of:
- An application needs local deployment configuration, environment boundaries and a dry-run plan for a chosen provider
- Someone asks which platform adapter, health check and rollback steps a project needs before any provisioning

Do not use when:
- Trigger the approved deployment workflow after readiness passes. Route to `deployment-trigger-execution`.
- Deploy the Web application through the selected hosting provider. Route to `web-hosting-deployment`.

#### Required Inputs

- Application, providers, environments, secrets policy, target, and deployment constraints.

#### Procedure

1. Freeze application artifact, provider options, environments, regions, domains, build and runtime settings, secret reference names, identities, quotas, costs, health criteria, and rollback requirements.
2. Select or document a provider adapter from approved constraints and separate local configuration from provider resources.
3. Write only authorized local config candidates, templates, dry-run commands, and environment validation artifacts; never place secret values in source.
4. Validate schema and local dry run where available, then return provider handoff, unknowns, and teardown or rollback plan without provisioning.

#### Domain Guidance

- Detect the platform from repository files (for example fly.toml, vercel.json, netlify.toml, render.yaml, Dockerfile, workflow files) and derive its adapter, URL pattern, status command and health check.
- Never write a realistic-looking connection string, key or token in any file or command. Reference secrets by name through environment variables or the provider's secret store, and show placeholders that cannot be mistaken for real values.
- Required output block: platform, production URL, deploy workflow or trigger, status command, merge method, project type, post-deploy health check, pre-merge hook, deploy trigger, and rollback plan.

#### Output Contract

Produce:
- local deployment configuration candidate
- environment and secret-reference contract
- dry-run and validation evidence
- provider handoff and teardown plan
- deploy configuration block (platform, URL, workflow, status command, merge method, project type, health check, hooks, rollback) consumed by readiness and trigger Skills

Every material command, request, observation, provider response, finding, decision recommendation, or completion claim must bind to exact target identity and current evidence or be labeled assumption/unknown.

Deliver each output as the artifact itself (tables, commands, patches, plans, records), not as a description of how it would be produced.

#### Coverage

- `local-config-only`
- `provider-adapter`
- `environment-boundary`
- `secret-references`
- `dry-run`
- `teardown-plan`
- `no-provision`

#### Hard Gates

- Environment setup writes local configuration only; it cannot create provider resources, credentials, domains, environments, deployments, or production state.
- Preflight never changes remote state; observation never executes recovery; coordination never performs specialist actions; one remote authorization never cascades.
- Preserve source, ref, pull request, artifact, release, environment, provider, service, incident, telemetry, baseline, or local-record identity; authority, evidence, limitations, cleanup, and recovery remain explicit.
- Return `needs-input` when a named owner can supply missing scope, target, authority, data governance, evidence, rollback, or decision.
- Return `blocked` when proceeding would expose credentials, exceed mutation authority, use stale evidence, mix readiness with action, mix observation with rollback, or perform undeclared remote or production work.
- Deliver every part the supplied evidence and authority support, label assumptions, and list each missing item with the owner who can supply it; `needs-input` or `blocked` applies to the unsupported part, not to the whole deliverable.

#### Forbidden Actions

- request, reveal, print, persist, hash, or transmit credential or secret values
- perform repository, provider, production, telemetry, incident, local-system, deployment, merge, or rollback mutation outside the exact atomic scope and fresh per-action authorization
- invent commands, provider receipts, deployment status, production evidence, incident actions, rollback result, approval, or release evidence
- combine readiness with action, observation with rollback, coordination with mitigation execution, or learning with unapproved persistence
- claim evaluation, approval, release, or completion evidence that has not been produced

#### Human Decision Authority

The Skill may return evidence, options, findings, and a recommendation. Merge, deploy, rollback, risk acceptance, incident closure, provider configuration, identity change, adoption, persistence, and release decisions remain explicit human decisions under the declared action identity.

#### Status Mapping

- `passed`: the atomic output and every gate have current target-bound evidence.
- `needs-input`: a requestable target, source, authority, evidence, governance term, or decision is absent. Deliver every supported part first and name the owner for the missing part.
- `blocked`: safe work requires prohibited access, unavailable authority, secret values, stale evidence, or an incompatible identity.
- `failed`: the authorized action ran but a deterministic gate or required output failed.

#### Non-Responsibilities

Adjacent capabilities:
- `deployment-trigger-execution`
- `web-hosting-deployment`
- `edge-worker-deployment`
- `kubernetes-application-deployment`

Never silently expand local, repository, provider, production, telemetry, incident, or release authority. Preflight never changes; observation never recovers; coordination never performs specialist actions; rollback never invents a target; one remote authorization never cascades to another action.

## Mode: `edge-worker-deployment`

### edge-worker-deployment

#### Responsibility

Deploy one immutable edge-worker artifact through one approved provider adapter after build, binding, route, limit, and rollback preflight.

#### Trigger

Use when the request matches any of:
- One edge worker or serverless function bundle must be deployed with bindings, routes and limits under fresh authorization
- A worker deployment needs an exact preflight covering bindings, compatibility date and rollback version

Do not use when:
- Prepare local edge deployment configuration and dry-run evidence. Route to `deployment-environment-setup`.
- Observe production signals after the worker deployment. Route to `deployment-observation`.
- Deploy a static or server-rendered web application project. Route to `web-hosting-deployment`.
- Deploy containers to an existing Kubernetes cluster. Route to `kubernetes-application-deployment`.

#### Required Inputs

- Worker source, environment bindings, provider account, compatibility target, and authorization.

#### Procedure

1. Verify provider account and project, environment, immutable bundle hash, compatibility/runtime version, bindings by reference, routes, domains, data stores, permissions, limits, cost, health checks, traffic plan, rollback target, and per-action authorization.
2. Build or validate the frozen artifact locally and preview provider diff or dry run without revealing secrets.
3. Perform one provider-specific deploy with bounded timeout and idempotency; do not modify unrelated routes, data, identities, or traffic.
4. Record deployment/version receipt, artifact hash, routes, config identity, status, health handoff, partial failure cleanup, and exact rollback reference.

#### Domain Guidance

- A successful dry run proves build and packaging only. It does not prove that bindings, routes or remote resources work, so the health handoff must check them against the live environment.
- After any config or binding change, regenerate the generated types with the project's own command instead of hand-editing them, then run the project's typecheck and tests before the dry run.

#### Output Contract

Produce:
- edge deployment receipt
- immutable worker and binding manifest
- route and environment identity
- health handoff and rollback reference

Every material command, request, observation, provider response, finding, decision recommendation, or completion claim must bind to exact target identity and current evidence or be labeled assumption/unknown.

Deliver each output as the artifact itself (tables, commands, patches, plans, records), not as a description of how it would be produced.

#### Coverage

- `immutable-worker`
- `bindings`
- `routes`
- `compatibility-version`
- `limits`
- `per-action-authorization`
- `rollback-target`

#### Hard Gates

- Edge deployment requires exact immutable code, bindings, routes, limits, traffic scope, health criteria, and rollback target; wildcard route or binding changes and unrelated resource mutations are blocked.
- Preflight never changes remote state; observation never executes recovery; coordination never performs specialist actions; one remote authorization never cascades.
- Preserve source, ref, pull request, artifact, release, environment, provider, service, incident, telemetry, baseline, or local-record identity; authority, evidence, limitations, cleanup, and recovery remain explicit.
- Return `needs-input` when a named owner can supply missing scope, target, authority, data governance, evidence, rollback, or decision.
- Return `blocked` when proceeding would expose credentials, exceed mutation authority, use stale evidence, mix readiness with action, mix observation with rollback, or perform undeclared remote or production work.
- Deliver every part the supplied evidence and authority support, label assumptions, and list each missing item with the owner who can supply it; `needs-input` or `blocked` applies to the unsupported part, not to the whole deliverable.

#### Forbidden Actions

- request, reveal, print, persist, hash, or transmit credential or secret values
- perform repository, provider, production, telemetry, incident, local-system, deployment, merge, or rollback mutation outside the exact atomic scope and fresh per-action authorization
- invent commands, provider receipts, deployment status, production evidence, incident actions, rollback result, approval, or release evidence
- combine readiness with action, observation with rollback, coordination with mitigation execution, or learning with unapproved persistence
- claim evaluation, approval, release, or completion evidence that has not been produced

#### Data and Credential Governance

For customer, production, incident, telemetry, trace, log, browser, or externally transferred data, require authority, minimization, redaction, sampling, access, region, retention, deletion, and incident boundaries. Credential and secret values never enter prompts, logs, hashes, receipts, or artifacts. Missing governance returns `needs-input`; prohibited or unavailable authority returns `blocked`.

#### Human Decision Authority

The Skill may return evidence, options, findings, and a recommendation. Merge, deploy, rollback, risk acceptance, incident closure, provider configuration, identity change, adoption, persistence, and release decisions remain explicit human decisions under the declared action identity.

#### Remote or Local-System Action Boundary

This Skill defines an action contract and does not execute the action by itself. Any real provider, repository, production, external-session, or local-system write requires fresh per-action authorization, one exact target and immutable input identity, preview or dry run where available, idempotency, durable receipt, bounded failure handling, and rollback, revocation, deletion, cancellation, or cleanup terms as applicable.

#### Status Mapping

- `passed`: the atomic output and every gate have current target-bound evidence.
- `needs-input`: a requestable target, source, authority, evidence, governance term, or decision is absent. Deliver every supported part first and name the owner for the missing part.
- `blocked`: safe work requires prohibited access, unavailable authority, secret values, stale evidence, or an incompatible identity.
- `failed`: the authorized action ran but a deterministic gate or required output failed.

#### Non-Responsibilities

Adjacent capabilities:
- `deployment-environment-setup`
- `deployment-observation`
- `release-rollback-execution`
- `release-observability-configuration`
- `web-hosting-deployment`
- `kubernetes-application-deployment`

Never silently expand local, repository, provider, production, telemetry, incident, or release authority. Preflight never changes; observation never recovers; coordination never performs specialist actions; rollback never invents a target; one remote authorization never cascades to another action.

## Mode: `kubernetes-application-deployment`

### kubernetes-application-deployment

#### Responsibility

Deploy one immutable application version to an existing Kubernetes platform with validated manifests, identity, rollout, health, and rollback controls under per-action authorization.

#### Trigger

Use when the request matches any of:
- One container image must be rolled out to an existing Kubernetes cluster with validated manifests and a health gate
- Someone asks for the exact dry-run, apply and rollout commands for a release under fresh authorization

Do not use when:
- Assess cluster, workload, identity, network, scaling, and rollback readiness. Route to `kubernetes-deployment-readiness`.
- Install or modify the observability agent on the cluster. Route to `observability-agent-installation`.
- Deploy an edge worker or serverless bundle. Route to `edge-worker-deployment`.
- Deploy a web application through a hosting provider. Route to `web-hosting-deployment`.

#### Required Inputs

- Application artifact, existing cluster context, provider adapter, manifests, credentials, and deployment authorization.

#### Procedure

1. Verify readiness report, cluster and context, namespace, workload, immutable image digest, reviewed manifest hashes, service account, secret references, policy, resources, probes, networking, autoscaling, migration order, rollout, disruption, health, timeout, rollback revision, blast radius, and per-action authorization.
2. Preview server-side diff or dry run and reject unexpected resource, namespace, identity, policy, or immutable-field changes.
3. Perform only the approved apply or rollout and bounded wait; stop on health, timeout, policy, migration, or rollout failure without widening scope.
4. Record applied revisions, resource identities, image digest, provider or kubectl evidence, status, partial failure, recovery, observation handoff, and exact rollback reference.

#### Domain Guidance

- When a blocker stops the rollout, still return the exact commands you would run once it clears (context-pinned server dry-run, apply, rollout status and rollback), clearly marked do-not-run until the named blocker is resolved, plus the minimal namespaced Role and RoleBinding needed if RBAC is the blocker.
- Map known deploy failure codes from the platform's failure catalog to a stop or recovery action in the rollout step; an unknown failure stops the rollout and preserves evidence.
- Build an authorization-to-action table linking the exact change ticket, approver, context, namespace, version and execution window. Preserve supplied previous revision and digest in rollback instructions, with verification after rollback. Never expand authorized clusters, namespaces or resource scope.

#### Output Contract

Produce:
- Kubernetes deployment receipt
- applied resource and image identity
- rollout and health status
- recovery, observation, and rollback handoff
- conditional command set marked do-not-run until blockers clear

Every material command, request, observation, provider response, finding, decision recommendation, or completion claim must bind to exact target identity and current evidence or be labeled assumption/unknown.

Deliver each output as the artifact itself (tables, commands, patches, plans, records), not as a description of how it would be produced.

#### Coverage

- `cluster-namespace`
- `manifest-hash`
- `image-digest`
- `server-dry-run`
- `rollout-health`
- `blast-radius`
- `rollback-revision`

#### Hard Gates

- Kubernetes deployment is bound to one cluster, namespace, manifest set, image digest, identity, rollout, health gate, and rollback revision; readiness failure or unexpected diff blocks apply.
- Preflight never changes remote state; observation never executes recovery; coordination never performs specialist actions; one remote authorization never cascades.
- Preserve source, ref, pull request, artifact, release, environment, provider, service, incident, telemetry, baseline, or local-record identity; authority, evidence, limitations, cleanup, and recovery remain explicit.
- Return `needs-input` when a named owner can supply missing scope, target, authority, data governance, evidence, rollback, or decision.
- Return `blocked` when proceeding would expose credentials, exceed mutation authority, use stale evidence, mix readiness with action, mix observation with rollback, or perform undeclared remote or production work.
- Deliver every part the supplied evidence and authority support, label assumptions, and list each missing item with the owner who can supply it; `needs-input` or `blocked` applies to the unsupported part, not to the whole deliverable.

#### Forbidden Actions

- request, reveal, print, persist, hash, or transmit credential or secret values
- perform repository, provider, production, telemetry, incident, local-system, deployment, merge, or rollback mutation outside the exact atomic scope and fresh per-action authorization
- invent commands, provider receipts, deployment status, production evidence, incident actions, rollback result, approval, or release evidence
- combine readiness with action, observation with rollback, coordination with mitigation execution, or learning with unapproved persistence
- claim evaluation, approval, release, or completion evidence that has not been produced

#### Data and Credential Governance

For customer, production, incident, telemetry, trace, log, browser, or externally transferred data, require authority, minimization, redaction, sampling, access, region, retention, deletion, and incident boundaries. Credential and secret values never enter prompts, logs, hashes, receipts, or artifacts. Missing governance returns `needs-input`; prohibited or unavailable authority returns `blocked`.

#### Human Decision Authority

The Skill may return evidence, options, findings, and a recommendation. Merge, deploy, rollback, risk acceptance, incident closure, provider configuration, identity change, adoption, persistence, and release decisions remain explicit human decisions under the declared action identity.

#### Remote or Local-System Action Boundary

This Skill defines an action contract and does not execute the action by itself. Any real provider, repository, production, external-session, or local-system write requires fresh per-action authorization, one exact target and immutable input identity, preview or dry run where available, idempotency, durable receipt, bounded failure handling, and rollback, revocation, deletion, cancellation, or cleanup terms as applicable.

#### Status Mapping

- `passed`: the atomic output and every gate have current target-bound evidence.
- `needs-input`: a requestable target, source, authority, evidence, governance term, or decision is absent. Deliver every supported part first and name the owner for the missing part.
- `blocked`: safe work requires prohibited access, unavailable authority, secret values, stale evidence, or an incompatible identity.
- `failed`: the authorized action ran but a deterministic gate or required output failed.

#### Non-Responsibilities

Adjacent capabilities:
- `kubernetes-deployment-readiness`
- `deployment-observation`
- `release-rollback-execution`
- `observability-agent-installation`
- `edge-worker-deployment`
- `web-hosting-deployment`

Never silently expand local, repository, provider, production, telemetry, incident, or release authority. Preflight never changes; observation never recovers; coordination never performs specialist actions; rollback never invents a target; one remote authorization never cascades to another action.

## Mode: `kubernetes-deployment-readiness`

### kubernetes-deployment-readiness

#### Responsibility

Read-only assess Kubernetes workload, cluster, identity, policy, scaling, networking, migration, health, and rollback readiness before deployment.

#### Trigger

Use when the request matches any of:
- A Kubernetes workload needs a read-only go/no-go before deployment covering rollout, scaling, policy and rollback
- Manifests or a cluster must be checked against AKS Automatic or platform safeguards before anything is applied

Do not use when:
- Deploy the approved manifests and image to the cluster. Route to `kubernetes-application-deployment`.
- Troubleshoot missing APM signals after deployment. Route to `apm-instrumentation-troubleshooting`.

#### Required Inputs

- Cluster and workload configuration, provider controls, expected traffic, failure budget, and deployment plan.

#### Procedure

1. Freeze target cluster, namespace, workload, manifest and image identities, read-only credentials, policies, quotas, dependencies, migrations, traffic, health, and rollback requirements.
2. Use only authorized read-only provider or Kubernetes evidence to inspect APIs, versions, nodes, quotas, identities, policies, secrets references, networking, storage, probes, resources, scaling, disruption, and current conflicts.
3. Run schema or server dry-run only if it is guaranteed non-mutating and authorized; otherwise mark it unavailable.
4. Return concrete recommended values for rollout strategy, autoscaling and disruption budgets, each with its arithmetic, instead of naming the topic only.
5. Return ready or blocked with evidence, unexpected diffs, safeguards, missing inputs, and exact deployment prerequisites; never apply or patch resources.

#### Domain Guidance

- Severity taxonomy per issue: incompatible (migration blocker), requiresChanges, autoFixed by the platform, cluster-config. Order blockers first; group by constraint id when more than 10 issues.
- Per-issue record: constraint id, severity, affected namespace/resource (Kind), current value, required value, fix summary, documentation link.
- AKS Automatic variant: check container resource requests and limits, probes, non-root and privilege settings, and disallowed host access against the safeguard constraints.
- Give concrete rollout values when the plan lacks them (for example maxUnavailable 0, maxSurge 1, replica count, PodDisruptionBudget minAvailable, HPA bounds) and compute rollback cost arithmetic explicitly.

#### Output Contract

Produce:
- Kubernetes readiness assessment
- cluster and workload evidence
- blocker and safeguard register
- deployment prerequisites and rollback requirements
- per-issue severity record with current and required values

Every material command, request, observation, provider response, finding, decision recommendation, or completion claim must bind to exact target identity and current evidence or be labeled assumption/unknown.

Deliver each output as the artifact itself (tables, commands, patches, plans, records), not as a description of how it would be produced.

#### Coverage

- `read-only`
- `cluster-namespace`
- `identity-policy`
- `network-storage`
- `probes-resources`
- `rollback-readiness`
- `no-apply`

#### Hard Gates

- Readiness authority is read-only: no apply, patch, rollout, scale, restart, secret read, policy change, or namespace mutation is permitted.
- Preflight never changes remote state; observation never executes recovery; coordination never performs specialist actions; one remote authorization never cascades.
- Preserve source, ref, pull request, artifact, release, environment, provider, service, incident, telemetry, baseline, or local-record identity; authority, evidence, limitations, cleanup, and recovery remain explicit.
- Return `needs-input` when a named owner can supply missing scope, target, authority, data governance, evidence, rollback, or decision.
- Return `blocked` when proceeding would expose credentials, exceed mutation authority, use stale evidence, mix readiness with action, mix observation with rollback, or perform undeclared remote or production work.
- Deliver every part the supplied evidence and authority support, label assumptions, and list each missing item with the owner who can supply it; `needs-input` or `blocked` applies to the unsupported part, not to the whole deliverable.

#### Forbidden Actions

- request, reveal, print, persist, hash, or transmit credential or secret values
- perform repository, provider, production, telemetry, incident, local-system, deployment, merge, or rollback mutation outside the exact atomic scope and fresh per-action authorization
- invent commands, provider receipts, deployment status, production evidence, incident actions, rollback result, approval, or release evidence
- combine readiness with action, observation with rollback, coordination with mitigation execution, or learning with unapproved persistence
- claim evaluation, approval, release, or completion evidence that has not been produced

#### Data and Credential Governance

For customer, production, incident, telemetry, trace, log, browser, or externally transferred data, require authority, minimization, redaction, sampling, access, region, retention, deletion, and incident boundaries. Credential and secret values never enter prompts, logs, hashes, receipts, or artifacts. Missing governance returns `needs-input`; prohibited or unavailable authority returns `blocked`.

#### Status Mapping

- `passed`: the atomic output and every gate have current target-bound evidence.
- `needs-input`: a requestable target, source, authority, evidence, governance term, or decision is absent. Deliver every supported part first and name the owner for the missing part.
- `blocked`: safe work requires prohibited access, unavailable authority, secret values, stale evidence, or an incompatible identity.
- `failed`: the authorized action ran but a deterministic gate or required output failed.

#### Non-Responsibilities

Adjacent capabilities:
- `kubernetes-application-deployment`
- `observability-agent-installation`
- `cloud-reliability-assessment`
- `merge-and-deploy-readiness`
- `apm-instrumentation-troubleshooting`

Never silently expand local, repository, provider, production, telemetry, incident, or release authority. Preflight never changes; observation never recovers; coordination never performs specialist actions; rollback never invents a target; one remote authorization never cascades to another action.

## Mode: `web-hosting-deployment`

### web-hosting-deployment

#### Responsibility

Deploy one immutable Web application artifact through one selected hosting provider adapter with exact environment, configuration, health, domain, and rollback controls.

#### Trigger

Use when the request matches any of:
- One web application artifact must be deployed through a hosting provider's CLI or API with exact environment and domain controls
- Someone asks for the exact provider deploy command, preview diff and rollback target for a specific project

Do not use when:
- Prepare local hosting configuration and dry-run evidence first. Route to `deployment-environment-setup`.
- Observe the deployment and production health after the provider action. Route to `deployment-observation`.
- Deploy an edge worker or serverless bundle. Route to `edge-worker-deployment`.
- Deploy containers to an existing Kubernetes cluster. Route to `kubernetes-application-deployment`.
- Push the commit that triggers a Git-integrated provider deployment. Route to `remote-git-push`.

#### Required Inputs

- Build artifact, provider project, environment, secrets boundary, deployment plan, and authorization.

#### Procedure

1. Select the deploy method from link and Git remote state; if the provider deploys from Git, hand off to remote-git-push and stop.
2. Verify provider and project, environment, immutable artifact or commit digest, build config, runtime, regions, domains, environment-variable references, identity, cache, migrations, preview diff, health, timeout, traffic, rollback target, cost, and fresh per-action authorization.
3. Build or validate the frozen artifact and preview exact provider changes without exposing secret values.
4. Perform one bounded deploy to the exact environment; do not merge, change unrelated domains or projects, rotate credentials, or auto-promote beyond authorization.
5. Record deployment URL and immutable ID, provider receipt, artifact and config identity, status, health handoff, partial-failure cleanup, and rollback reference.

#### Domain Guidance

- Select the method first: linked project with a Git remote (deploy happens on push: hand off to remote-git-push and stop), linked project without a remote (CLI deploy), unlinked project (tarball or CLI deploy with explicit project binding). This Skill covers CLI and API deploys only.
- Tarball or CLI deploys exclude node_modules, .git and .env by default; state the exclusions in the preview.
- Browser-exposed build variables such as VITE_ are not secrets storage. Domain binding or DNS changes need their own exact authority and must not be folded into a deployment proposal implicitly.

#### Output Contract

Produce:
- hosting deployment receipt
- deployment URL and immutable identity
- artifact and configuration evidence
- observation handoff and rollback reference

Every material command, request, observation, provider response, finding, decision recommendation, or completion claim must bind to exact target identity and current evidence or be labeled assumption/unknown.

Deliver each output as the artifact itself (tables, commands, patches, plans, records), not as a description of how it would be produced.

#### Coverage

- `provider-project`
- `environment`
- `artifact-digest`
- `config-identity`
- `domain-traffic`
- `health-gate`
- `rollback-target`

#### Hard Gates

- Web deployment requires one exact provider project, environment, immutable artifact, configuration, domain and traffic scope, health gate, and rollback target; preview or identity drift blocks deployment.
- Preflight never changes remote state; observation never executes recovery; coordination never performs specialist actions; one remote authorization never cascades.
- Preserve source, ref, pull request, artifact, release, environment, provider, service, incident, telemetry, baseline, or local-record identity; authority, evidence, limitations, cleanup, and recovery remain explicit.
- Return `needs-input` when a named owner can supply missing scope, target, authority, data governance, evidence, rollback, or decision.
- Return `blocked` when proceeding would expose credentials, exceed mutation authority, use stale evidence, mix readiness with action, mix observation with rollback, or perform undeclared remote or production work.
- Deliver every part the supplied evidence and authority support, label assumptions, and list each missing item with the owner who can supply it; `needs-input` or `blocked` applies to the unsupported part, not to the whole deliverable.

#### Forbidden Actions

- request, reveal, print, persist, hash, or transmit credential or secret values
- perform repository, provider, production, telemetry, incident, local-system, deployment, merge, or rollback mutation outside the exact atomic scope and fresh per-action authorization
- invent commands, provider receipts, deployment status, production evidence, incident actions, rollback result, approval, or release evidence
- combine readiness with action, observation with rollback, coordination with mitigation execution, or learning with unapproved persistence
- claim evaluation, approval, release, or completion evidence that has not been produced

#### Data and Credential Governance

For customer, production, incident, telemetry, trace, log, browser, or externally transferred data, require authority, minimization, redaction, sampling, access, region, retention, deletion, and incident boundaries. Credential and secret values never enter prompts, logs, hashes, receipts, or artifacts. Missing governance returns `needs-input`; prohibited or unavailable authority returns `blocked`.

#### Human Decision Authority

The Skill may return evidence, options, findings, and a recommendation. Merge, deploy, rollback, risk acceptance, incident closure, provider configuration, identity change, adoption, persistence, and release decisions remain explicit human decisions under the declared action identity.

#### Remote or Local-System Action Boundary

This Skill defines an action contract and does not execute the action by itself. Any real provider, repository, production, external-session, or local-system write requires fresh per-action authorization, one exact target and immutable input identity, preview or dry run where available, idempotency, durable receipt, bounded failure handling, and rollback, revocation, deletion, cancellation, or cleanup terms as applicable.

#### Status Mapping

- `passed`: the atomic output and every gate have current target-bound evidence.
- `needs-input`: a requestable target, source, authority, evidence, governance term, or decision is absent. Deliver every supported part first and name the owner for the missing part.
- `blocked`: safe work requires prohibited access, unavailable authority, secret values, stale evidence, or an incompatible identity.
- `failed`: the authorized action ran but a deterministic gate or required output failed.

#### Non-Responsibilities

Adjacent capabilities:
- `deployment-environment-setup`
- `deployment-observation`
- `release-rollback-execution`
- `release-observability-configuration`
- `edge-worker-deployment`
- `kubernetes-application-deployment`
- `remote-git-push`

Never silently expand local, repository, provider, production, telemetry, incident, or release authority. Preflight never changes; observation never recovers; coordination never performs specialist actions; rollback never invents a target; one remote authorization never cascades to another action.
