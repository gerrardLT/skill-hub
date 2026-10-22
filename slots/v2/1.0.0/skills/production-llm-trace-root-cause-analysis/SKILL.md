---
name: production-llm-trace-root-cause-analysis
description: Diagnose governed production LLM traces to evidence-bounded root-cause hypotheses across prompts, retrieval, models, tools, data, latency, and user context without remediation. Do not use for classify raw production traces into behavior and failure categories first or apply the accepted ai model, prompt, retrieval, or code remediation.
---

# Production Llm Trace Root Cause Analysis

## Responsibility

Diagnose governed production LLM traces to evidence-bounded root-cause hypotheses across prompts, retrieval, models, tools, data, latency, and user context without remediation.

## Trigger

Use when the requested outcome is: Diagnose governed production LLM traces to evidence-bounded root-cause hypotheses across prompts, retrieval, models, tools, data, latency, and user context without remediation.

Do not use when:
- Classify raw production traces into behavior and failure categories first. Route to `production-trace-classification`.
- Apply the accepted AI model, prompt, retrieval, or code remediation. Route to `defect-remediation`.

## Required Inputs

- Authorized trace data, incident scope, time window, privacy boundary, and service context.

Also require exact repository, provider, environment, service, incident, release, artifact, telemetry, or local destination identity; authority; evidence window; and recovery or cleanup where applicable.

## Procedure

1. Freeze trace and release identities, time window, classified failure cohort, expected behavior, prompt and model versions, retrieval and tool versions, data policy, minimization, read-only authority, and investigation question.
2. Compare successful and failed traces across inputs, prompt assembly, retrieval, model route, output, tool calls, retries, latency, cost, safety, and user or tenant context under governance.
3. Test competing hypotheses and locate the first divergent invariant while separating correlation, classification error, downstream symptom, and root cause.
4. Return evidence, confidence, affected slice, and bounded model, data, prompt, tool, UX, or source remediation hypothesis; no config or source change.

## Output Contract

Produce:
- LLM trace root-cause evidence
- competing hypothesis ledger
- first-divergent-stage analysis
- bounded remediation and owner handoff

Every material command, request, observation, provider response, finding, decision recommendation, or completion claim must bind to exact target identity and current evidence or be labeled assumption/unknown.

## Coverage

- `governed-traces`
- `versioned-components`
- `success-failure-comparison`
- `competing-hypotheses`
- `first-divergent-stage`
- `no-remediation`

## Hard Gates

- Production LLM root cause requires governed trace provenance, versioned components, successful comparison cases, competing hypotheses, and a first divergent invariant; one bad output or model label is insufficient.
- Preserve source, ref, pull request, artifact, release, environment, provider, service, incident, telemetry, baseline, or local-record identity; authority, evidence, limitations, cleanup, and recovery remain explicit.
- Return `needs-input` when a named owner can supply missing scope, target, authority, data governance, evidence, rollback, or decision.
- Return `blocked` when proceeding would expose credentials, exceed mutation authority, use stale evidence, mix readiness with action, mix observation with rollback, or perform undeclared remote or production work.

## Data and Credential Governance

For customer, production, incident, telemetry, trace, log, browser, or externally transferred data, require authority, minimization, redaction, sampling, access, region, retention, deletion, and incident boundaries. Credential and secret values never enter prompts, logs, hashes, receipts, or artifacts. Missing governance returns `needs-input`; prohibited or unavailable authority returns `blocked`.

## Status Mapping

- `passed`: the atomic output and every gate have current target-bound evidence.
- `needs-input`: a requestable target, source, authority, evidence, governance term, or decision is absent.
- `blocked`: safe work requires prohibited access, unavailable authority, secret values, stale evidence, or an incompatible identity.
- `failed`: the authorized action ran but a deterministic gate or required output failed.

## Non-Responsibilities

Does not absorb unrelated lifecycle responsibilities or expand provider, workspace, or remote-write authority implicitly.

Adjacent capabilities:
- `production-trace-classification`
- `defect-remediation`
- `ai-model-and-data-architecture`
- `ai-observability-configuration`

Never silently expand local, repository, provider, production, telemetry, incident, or release authority. Preflight never changes; observation never recovers; coordination never performs specialist actions; rollback never invents a target; one remote authorization never cascades to another action.
