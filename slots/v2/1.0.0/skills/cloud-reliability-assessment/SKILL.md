---
name: cloud-reliability-assessment
description: Assess an authorized cloud architecture against provider-specific failure, recovery, scaling, dependency, and operational practices using read-only evidence. Do not use for apply the accepted cloud reliability changes or coordinate an active production incident and mitigation decisions.
---

# Cloud Reliability Assessment

## Responsibility

Assess an authorized cloud architecture against provider-specific failure, recovery, scaling, dependency, and operational practices using read-only evidence.

## Trigger

Use when the requested outcome is: Assess an authorized cloud architecture against provider-specific failure, recovery, scaling, dependency, and operational practices using read-only evidence.

Do not use when:
- Apply the accepted cloud reliability changes. Route to `defect-remediation`.
- Coordinate an active production incident and mitigation decisions. Route to `incident-response-coordination`.

## Required Inputs

- Architecture evidence, provider, availability target, dependencies, traffic, and recovery objectives.

Also require exact repository, provider, environment, service, incident, release, artifact, telemetry, or local destination identity; authority; evidence window; and recovery or cleanup where applicable.

## Procedure

1. Freeze provider, accounts, regions, services, architecture, critical journeys, SLOs, RTO/RPO, data and dependency classes, read-only authority, and excluded tests.
2. Inspect read-only evidence for redundancy, failure domains, scaling, quotas, backups, restore tests, failover, load shedding, timeouts, retries, circuit breaking, dependencies, observability, and runbooks.
3. Map plausible failures to detection, containment, recovery, evidence, and current test coverage without conducting destructive experiments.
4. Return prioritized reliability findings, confidence, residual risk, and controlled validation or remediation recommendations.

## Output Contract

Produce:
- cloud reliability assessment
- failure-domain and dependency map
- RTO/RPO and recovery gaps
- prioritized validation and remediation recommendations

Every material command, request, observation, provider response, finding, decision recommendation, or completion claim must bind to exact target identity and current evidence or be labeled assumption/unknown.

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
- Preserve source, ref, pull request, artifact, release, environment, provider, service, incident, telemetry, baseline, or local-record identity; authority, evidence, limitations, cleanup, and recovery remain explicit.
- Return `needs-input` when a named owner can supply missing scope, target, authority, data governance, evidence, rollback, or decision.
- Return `blocked` when proceeding would expose credentials, exceed mutation authority, use stale evidence, mix readiness with action, mix observation with rollback, or perform undeclared remote or production work.

## Data and Credential Governance

For customer, production, incident, telemetry, trace, log, browser, or externally transferred data, require authority, minimization, redaction, sampling, access, region, retention, deletion, and incident boundaries. Credential and secret values never enter prompts, logs, hashes, receipts, or artifacts. Missing governance returns `needs-input`; prohibited or unavailable authority returns `blocked`.

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
- `incident-response-coordination`
- `deployment-environment-setup`
- `monitoring-and-alert-configuration`
- `release-rollback-execution`

Never silently expand local, repository, provider, production, telemetry, incident, or release authority. Preflight never changes; observation never recovers; coordination never performs specialist actions; rollback never invents a target; one remote authorization never cascades to another action.
