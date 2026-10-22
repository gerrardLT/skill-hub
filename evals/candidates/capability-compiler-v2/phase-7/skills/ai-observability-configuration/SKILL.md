---
name: ai-observability-configuration
description: Configure one provider's AI or LLM observability for exact applications and environments under explicit telemetry governance and per-action authorization. Do not use for define the ai model, prompt, retrieval, and data architecture first or classify already-collected production traces without changing configuration.
---

# Ai Observability Configuration

## Responsibility

Configure one provider's AI or LLM observability for exact applications and environments under explicit telemetry governance and per-action authorization.

## Trigger

Use when the requested outcome is: Configure one provider's AI or LLM observability for exact applications and environments under explicit telemetry governance and per-action authorization.

Do not use when:
- Define the AI model, prompt, retrieval, and data architecture first. Route to `ai-model-and-data-architecture`.
- Classify already-collected production traces without changing configuration. Route to `production-trace-classification`.

## Required Inputs

- AI application, traces, sensitive-data policy, provider, evaluation signals, retention, and authorization.

Also require exact repository, provider, environment, service, incident, release, artifact, telemetry, or local destination identity; authority; evidence window; and recovery or cleanup where applicable.

## Procedure

1. Verify provider, account, application, environments, models, traces, fields, data classes, consent, minimization, redaction, sampling, retention, region, access, cost, deletion, dashboards, alerts, and fresh authorization.
2. Preview exact instrumentation or provider settings and sample payload schema; block prompt, response, user, tool, or retrieved content that exceeds governance.
3. Perform one bounded configuration change without altering models, prompts, application behavior, unrelated services, or autonomous action rights.
4. Record provider receipt, configuration version, governed fields, sampling, validation, cost estimate, propagation, deletion, and rollback.

## Output Contract

Produce:
- AI observability configuration receipt
- governed telemetry schema
- sampling, redaction, retention, and access record
- validation and rollback evidence

Every material command, request, observation, provider response, finding, decision recommendation, or completion claim must bind to exact target identity and current evidence or be labeled assumption/unknown.

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
- `ai-model-and-data-architecture`
- `production-trace-classification`
- `production-llm-trace-root-cause-analysis`
- `monitoring-and-alert-configuration`

Never silently expand local, repository, provider, production, telemetry, incident, or release authority. Preflight never changes; observation never recovers; coordination never performs specialist actions; rollback never invents a target; one remote authorization never cascades to another action.
