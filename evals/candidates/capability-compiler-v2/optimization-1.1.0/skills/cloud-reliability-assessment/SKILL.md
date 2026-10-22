---
name: cloud-reliability-assessment
description: "Assess an authorized cloud architecture against provider-specific failure, recovery, scaling, dependency, and operational practices using read-only evidence. Use when An architecture, IaC or resource inventory needs an availability, failover and recovery assessment against stated SLO, RTO or RPO targets; Someone asks whether a cloud workload is zone redundant, backed up and restorable, using read-only evidence only. Do not use for: Apply the accepted cloud reliability changes (-> defect-remediation); Coordinate an active production incident and mitigation decisions (-> incident-response-coordination)."
---

# Cloud Reliability Assessment

## Responsibility

Assess an authorized cloud architecture against provider-specific failure, recovery, scaling, dependency, and operational practices using read-only evidence.

## Trigger

Use when the request matches any of:
- An architecture, IaC or resource inventory needs an availability, failover and recovery assessment against stated SLO, RTO or RPO targets
- Someone asks whether a cloud workload is zone redundant, backed up and restorable, using read-only evidence only

Do not use when:
- Apply the accepted cloud reliability changes. Route to `defect-remediation`.
- Coordinate an active production incident and mitigation decisions. Route to `incident-response-coordination`.

## Required Inputs

- Architecture evidence, provider, availability target, dependencies, traffic, and recovery objectives.

## Procedure

1. Freeze provider, accounts, regions, services, architecture, critical journeys, SLOs, RTO/RPO, data and dependency classes, read-only authority, and excluded tests.
2. Inspect read-only evidence for redundancy, failure domains, scaling, quotas, backups, restore tests, failover, load shedding, timeouts, retries, circuit breaking, dependencies, observability, and runbooks.
3. Map plausible failures to detection, containment, recovery, evidence, and current test coverage without conducting destructive experiments.
4. Return prioritized reliability findings, confidence, residual risk, and controlled validation or remediation recommendations.

## Domain Guidance

- Azure variant: for each App Service plan, Function app or storage account report zone redundancy, instance count, health-check path and storage redundancy (LRS/ZRS/GRS) in one row.
- Classify each recommendation as quick win (no downtime, no cost change), config change (brief impact) or migration (downtime or cost impact) so the owner can sequence it.

## Output Contract

Produce:
- cloud reliability assessment
- failure-domain and dependency map
- RTO/RPO and recovery gaps
- prioritized validation and remediation recommendations
- per-resource reliability table with severity, downtime impact and cost impact

Every material command, request, observation, provider response, finding, decision recommendation, or completion claim must bind to exact target identity and current evidence or be labeled assumption/unknown.

Deliver each output as the artifact itself (tables, commands, patches, plans, records), not as a description of how it would be produced.

## Coverage

- `failure-domains`
- `RTO-RPO`
- `backups-restore`
- `failover`
- `dependency-map`
- `read-only`
- `no-destructive-test`

## Hard Gates

- Reliability assessment is read-only and evidence-bounded; it cannot perform failover, scale, restart, reconfigure, restore, or claim resilience from architecture diagrams alone.
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

## Status Mapping

- `passed`: the atomic output and every gate have current target-bound evidence.
- `needs-input`: a requestable target, source, authority, evidence, governance term, or decision is absent. Deliver every supported part first and name the owner for the missing part.
- `blocked`: safe work requires prohibited access, unavailable authority, secret values, stale evidence, or an incompatible identity.
- `failed`: the authorized action ran but a deterministic gate or required output failed.

## Non-Responsibilities

Adjacent capabilities:
- `incident-response-coordination`
- `deployment-environment-setup`
- `monitoring-and-alert-configuration`
- `release-rollback-execution`
- `defect-remediation`

Never silently expand local, repository, provider, production, telemetry, incident, or release authority. Preflight never changes; observation never recovers; coordination never performs specialist actions; rollback never invents a target; one remote authorization never cascades to another action.
