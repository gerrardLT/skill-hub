---
name: metrics-system-and-observability
description: "Define an evidence-linked metric system of outcomes, inputs, secondary and guardrail metrics with baselines, instrumentation contracts, dashboards, and alert recommendations without provider mutation. Use when A feature or service needs a metric tree with exact definitions, baselines, guardrails and owners; Someone asks which single metric a change must move and how often the team reviews it. Do not use for: Create or update provider monitors and alert routing (-> monitoring-and-alert-configuration); Configure provider log ingestion and parsing (-> log-observability-configuration)."
---

# Metrics System And Observability

## Responsibility

Define an evidence-linked metric system of outcomes, inputs, secondary and guardrail metrics with baselines, instrumentation contracts, dashboards, and alert recommendations without provider mutation.

## Trigger

Use when the request matches any of:
- A feature or service needs a metric tree with exact definitions, baselines, guardrails and owners
- Someone asks which single metric a change must move and how often the team reviews it

Do not use when:
- Create or update provider monitors and alert routing. Route to `monitoring-and-alert-configuration`.
- Configure provider log ingestion and parsing. Route to `log-observability-configuration`.

## Required Inputs

- Business goals, user outcomes, risks, data sources, and observable events.

## Procedure

1. Freeze decisions, user and system outcomes, services, SLOs, data sources, current instrumentation, metric definitions, owners, privacy, cost, and reporting cadence.
2. Define exact numerator, denominator, unit, aggregation, window, dimensions, freshness, exclusions, baseline, target, guardrail, and known bias for each metric.
3. Map outcome to controllable inputs, diagnostic and guardrail metrics, instrumentation events, dashboards, owner, and decision or response.
4. Return metric and instrumentation contract, dashboard and alert recommendations, gaps, and validation plan; do not configure providers.

## Domain Guidance

- Name one primary metric the work must move, with numerator, denominator, unit and window, plus input, secondary and guardrail metrics. When a denominator is ambiguous in the request, state the options, pick one explicitly with the reason, and show how the value changes under the other.
- Set a review cadence: weekly check for health and experiments (15 to 30 minutes), monthly review of the outcome trend; each review names attendees and what is examined.

## Output Contract

Produce:
- metric tree and exact definitions
- baseline, target, and guardrail contract
- instrumentation and dashboard specification
- ownership, gap, and alert recommendation
- one primary metric with exact definition and review cadence

Every material command, request, observation, provider response, finding, decision recommendation, or completion claim must bind to exact target identity and current evidence or be labeled assumption/unknown.

Deliver each output as the artifact itself (tables, commands, patches, plans, records), not as a description of how it would be produced.

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
- `monitoring-and-alert-configuration`
- `log-observability-configuration`
- `release-observability-configuration`
- `feedback-and-continuous-learning-loop`

Never silently expand local, repository, provider, production, telemetry, incident, or release authority. Preflight never changes; observation never recovers; coordination never performs specialist actions; rollback never invents a target; one remote authorization never cascades to another action.
