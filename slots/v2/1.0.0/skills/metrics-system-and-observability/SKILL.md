---
name: metrics-system-and-observability
description: Define an evidence-linked metric system of outcomes, inputs, secondary and guardrail metrics with baselines, instrumentation contracts, dashboards, and alert recommendations without provider mutation. Do not use for create or update provider monitors and alert routing or configure provider log ingestion and parsing.
---

# Metrics System And Observability

## Responsibility

Define an evidence-linked metric system of outcomes, inputs, secondary and guardrail metrics with baselines, instrumentation contracts, dashboards, and alert recommendations without provider mutation.

## Trigger

Use when the requested outcome is: Define an evidence-linked metric system of outcomes, inputs, secondary and guardrail metrics with baselines, instrumentation contracts, dashboards, and alert recommendations without provider mutation.

Do not use when:
- Create or update provider monitors and alert routing. Route to `monitoring-and-alert-configuration`.
- Configure provider log ingestion and parsing. Route to `log-observability-configuration`.

## Required Inputs

- Business goals, user outcomes, risks, data sources, and observable events.

Also require exact repository, provider, environment, service, incident, release, artifact, telemetry, or local destination identity; authority; evidence window; and recovery or cleanup where applicable.

## Procedure

1. Freeze decisions, user and system outcomes, services, SLOs, data sources, current instrumentation, metric definitions, owners, privacy, cost, and reporting cadence.
2. Define exact numerator, denominator, unit, aggregation, window, dimensions, freshness, exclusions, baseline, target, guardrail, and known bias for each metric.
3. Map outcome to controllable inputs, diagnostic and guardrail metrics, instrumentation events, dashboards, owner, and decision or response.
4. Return metric and instrumentation contract, dashboard and alert recommendations, gaps, and validation plan; do not configure providers.

## Output Contract

Produce:
- metric tree and exact definitions
- baseline, target, and guardrail contract
- instrumentation and dashboard specification
- ownership, gap, and alert recommendation

Every material command, request, observation, provider response, finding, decision recommendation, or completion claim must bind to exact target identity and current evidence or be labeled assumption/unknown.

## Coverage

- `exact-formula`
- `numerator-denominator`
- `window-dimensions`
- `baseline-target`
- `guardrail`
- `owner`
- `linked-action`

## Hard Gates

- A metric is not operational without exact formula, unit, aggregation, window, dimensions, data source, owner, baseline, target or threshold, bias, and linked decision or action.
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

Does not approve upstream product decisions, expand authority, or perform remote writes beyond its explicit permission identity.

Adjacent capabilities:
- `monitoring-and-alert-configuration`
- `log-observability-configuration`
- `release-observability-configuration`
- `feedback-and-continuous-learning-loop`

Never silently expand local, repository, provider, production, telemetry, incident, or release authority. Preflight never changes; observation never recovers; coordination never performs specialist actions; rollback never invents a target; one remote authorization never cascades to another action.
