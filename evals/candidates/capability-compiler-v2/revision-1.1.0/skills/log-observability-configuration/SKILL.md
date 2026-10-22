---
name: log-observability-configuration
description: "Configure one provider's log collection, parsing, routing, retention, access, and sensitive-data controls for exact services and environments under per-action authorization. Use when Logs from exact services need collection, parsing, routing and retention set up in one provider with sensitive fields controlled; Someone asks for the pipeline, exclusion filters and cost estimate for a log source. Do not use for: Define metrics, dashboards, and alert semantics from approved outcomes (-> metrics-system-and-observability); Install the observability agent required to collect host logs (-> observability-agent-installation); Configure AI or LLM trace spans and token telemetry (-> ai-observability-configuration); Handle release and commit association for services and environments (-> release-observability-configuration); Handle monitors and alert routes from approved SLOs (-> monitoring-and-alert-configuration)."
---

# Log Observability Configuration

## Responsibility

Configure one provider's log collection, parsing, routing, retention, access, and sensitive-data controls for exact services and environments under per-action authorization.

## Trigger

Use when the request matches any of:
- Logs from exact services need collection, parsing, routing and retention set up in one provider with sensitive fields controlled
- Someone asks for the pipeline, exclusion filters and cost estimate for a log source

Do not use when:
- Define metrics, dashboards, and alert semantics from approved outcomes. Route to `metrics-system-and-observability`.
- Install the observability agent required to collect host logs. Route to `observability-agent-installation`.
- Configure AI or LLM trace spans and token telemetry. Route to `ai-observability-configuration`.
- Handle release and commit association for services and environments. Route to `release-observability-configuration`.
- Handle monitors and alert routes from approved SLOs. Route to `monitoring-and-alert-configuration`.

## Required Inputs

- Log sources, schemas, provider, authorization, retention, redaction, and routing requirements.

## Procedure

1. Verify provider, account, sources, services, environments, log schemas, fields, PII and secret classes, minimization, redaction, parsing, routing, sampling, retention, region, access, cost, deletion, failure handling, and fresh authorization.
2. Preview exact sources, pipelines, indexes, destinations, transformations, and sample redacted events; block credential or sensitive-value capture.
3. Perform one bounded configuration change without modifying applications, unrelated pipelines, monitors, or retention outside scope.
4. Record provider receipt, config version, sample validation, volume and cost estimate, access, retention, deletion, propagation, and rollback.

## Domain Guidance

- Cost control order: exclusion filters first (drop debug and health-check noise), then sampling, then shorter retention on low-value indexes. Estimate volume and cost per index before the change.
- Pipeline pattern: a filter selecting the service, a parser (for example grok for a known line format) with sample lines, then remappers for status, service and trace id.
- Troubleshooting map: logs not appearing (check agent and pipeline filters), high cost (add exclusions), slow search (narrow time range and use indexes), missing attributes (check the parser).
- Discriminator by signal type: this Skill handles log collection, parsing, routing and retention.

## Output Contract

Produce:
- log configuration receipt
- source, parse, and route schema
- redaction, retention, access, and cost record
- sample validation and rollback evidence

Every material command, request, observation, provider response, finding, decision recommendation, or completion claim must bind to exact target identity and current evidence or be labeled assumption/unknown.

Deliver each output as the artifact itself (tables, commands, patches, plans, records), not as a description of how it would be produced.

## Coverage

- `exact-log-sources`
- `parsing`
- `routing`
- `redaction`
- `retention`
- `access`
- `volume-cost`
- `deletion`

## Hard Gates

- Logs deny secret and sensitive fields by default and require exact source, parsing, routing, retention, access, deletion, volume, and cost boundaries before provider mutation.
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
- `metrics-system-and-observability`
- `monitoring-and-alert-configuration`
- `observability-agent-installation`
- `source-metadata-and-provenance`
- `ai-observability-configuration`
- `release-observability-configuration`

Never silently expand local, repository, provider, production, telemetry, incident, or release authority. Preflight never changes; observation never recovers; coordination never performs specialist actions; rollback never invents a target; one remote authorization never cascades to another action.
