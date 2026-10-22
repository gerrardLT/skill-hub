---
name: production-trace-classification
description: Classify authorized production LLM traces into evidence-backed behavior and failure categories while preserving provenance, uncertainty, minority cases, and governance. Do not use for diagnose root causes within a classified production llm failure cohort or configure which ai trace fields the provider collects.
---

# Production Trace Classification

## Responsibility

Classify authorized production LLM traces into evidence-backed behavior and failure categories while preserving provenance, uncertainty, minority cases, and governance.

## Trigger

Use when the requested outcome is: Classify authorized production LLM traces into evidence-backed behavior and failure categories while preserving provenance, uncertainty, minority cases, and governance.

Do not use when:
- Diagnose root causes within a classified production LLM failure cohort. Route to `production-llm-trace-root-cause-analysis`.
- Configure which AI trace fields the provider collects. Route to `ai-observability-configuration`.

## Required Inputs

- Authorized trace scope, provider read access, time window, sampling policy, and data-governance boundary.

Also require exact repository, provider, environment, service, incident, release, artifact, telemetry, or local destination identity; authority; evidence window; and recovery or cleanup where applicable.

## Procedure

1. Verify trace source, application, environment, release, prompt and model versions, sample window, selection, consent or rights, minimization, redaction, retention, transfer, access, and deletion.
2. Define operational category criteria and unknown or multi-label handling before reading outcomes broadly.
3. Classify behavior, retrieval, generation, factuality, tool, policy, latency, cost, interaction, and recovery signals with trace IDs and confidence; preserve counterexamples and uncategorized cases.
4. Return taxonomy, counts, evidence, uncertainty, and cohorts for root-cause analysis without changing provider config or claiming causality.

## Output Contract

Produce:
- production trace taxonomy
- trace-to-category ledger
- counts, confidence, and minority cases
- governed root-cause cohorts

Every material command, request, observation, provider response, finding, decision recommendation, or completion claim must bind to exact target identity and current evidence or be labeled assumption/unknown.

## Coverage

- `authorized-sample`
- `redaction`
- `taxonomy`
- `trace-provenance`
- `confidence`
- `uncategorized`
- `no-causality`

## Hard Gates

- Trace classification describes observed behavior only; it cannot infer root cause, authorize reuse, or expand beyond the approved sample, fields, retention, and deletion boundary.
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
- `production-llm-trace-root-cause-analysis`
- `ai-observability-configuration`
- `llm-quality-evaluation`
- `qualitative-evidence-synthesis`

Never silently expand local, repository, provider, production, telemetry, incident, or release authority. Preflight never changes; observation never recovers; coordination never performs specialist actions; rollback never invents a target; one remote authorization never cascades to another action.
