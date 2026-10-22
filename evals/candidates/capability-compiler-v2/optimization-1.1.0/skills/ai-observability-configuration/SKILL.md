---
name: ai-observability-configuration
description: "Configure one provider's AI or LLM observability for exact applications and environments under explicit telemetry governance and per-action authorization. Use when An LLM or agent application needs its generation spans, token usage and tool calls traced in one provider under a telemetry governance policy; Someone asks which prompt, response and tool fields may be collected, at what sampling, retention and access. Do not use for: Define the AI model, prompt, retrieval, and data architecture first (-> ai-model-and-data-architecture); Classify already-collected production traces without changing configuration (-> production-trace-classification); Configure log collection, parsing and routing (-> log-observability-configuration); Handle release and commit association for services and environments (-> release-observability-configuration); Handle monitors and alert routes from approved SLOs (-> monitoring-and-alert-configuration)."
---

# AI Observability Configuration

## Responsibility

Configure one provider's AI or LLM observability for exact applications and environments under explicit telemetry governance and per-action authorization.

## Trigger

Use when the request matches any of:
- An LLM or agent application needs its generation spans, token usage and tool calls traced in one provider under a telemetry governance policy
- Someone asks which prompt, response and tool fields may be collected, at what sampling, retention and access

Do not use when:
- Define the AI model, prompt, retrieval, and data architecture first. Route to `ai-model-and-data-architecture`.
- Classify already-collected production traces without changing configuration. Route to `production-trace-classification`.
- Configure log collection, parsing and routing. Route to `log-observability-configuration`.
- Handle release and commit association for services and environments. Route to `release-observability-configuration`.
- Handle monitors and alert routes from approved SLOs. Route to `monitoring-and-alert-configuration`.

## Required Inputs

- AI application, traces, sensitive-data policy, provider, evaluation signals, retention, and authorization.

## Procedure

1. Verify provider, account, application, environments, models, traces, fields, data classes, consent, minimization, redaction, sampling, retention, region, access, cost, deletion, dashboards, alerts, and fresh authorization.
2. Preview exact instrumentation or provider settings and sample payload schema; block prompt, response, user, tool, or retrieved content that exceeds governance.
3. Perform one bounded configuration change without altering models, prompts, application behavior, unrelated services, or autonomous action rights.
4. Record provider receipt, configuration version, governed fields, sampling, validation, cost estimate, propagation, deletion, and rollback.

## Domain Guidance

- Default schema: the gen_ai.* span attribute conventions (operation name, system, request and response model, token counts, finish reason, tool name). Record the convention version used.
- Detect a supported SDK or auto-instrumentation first and use it; add manual spans only when no supported SDK is detected, and never run both for the same call.
- Prompt, response, tool, user and retrieved content are denied by default; collect a field only when the governance record names it, with sampling, redaction, retention and access.
- Discriminator by signal type: this Skill handles model calls, prompts, traces and evaluation telemetry.

## Output Contract

Produce:
- AI observability configuration receipt
- governed telemetry schema
- sampling, redaction, retention, and access record
- validation and rollback evidence

Every material command, request, observation, provider response, finding, decision recommendation, or completion claim must bind to exact target identity and current evidence or be labeled assumption/unknown.

Deliver each output as the artifact itself (tables, commands, patches, plans, records), not as a description of how it would be produced.

## Coverage

- `exact-application`
- `telemetry-schema`
- `minimization`
- `redaction`
- `sampling`
- `retention`
- `access`
- `deletion`

## Hard Gates

- AI observability may collect only explicitly governed fields at approved sampling, retention, region, and access; prompt, response, tool, user, or retrieved content is denied by default.
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
- `ai-model-and-data-architecture`
- `production-trace-classification`
- `production-llm-trace-root-cause-analysis`
- `monitoring-and-alert-configuration`
- `log-observability-configuration`
- `release-observability-configuration`

Never silently expand local, repository, provider, production, telemetry, incident, or release authority. Preflight never changes; observation never recovers; coordination never performs specialist actions; rollback never invents a target; one remote authorization never cascades to another action.
