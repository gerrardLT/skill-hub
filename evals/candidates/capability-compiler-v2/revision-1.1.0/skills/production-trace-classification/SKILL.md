---
name: production-trace-classification
description: "Classify authorized production LLM traces into evidence-backed behavior and failure categories while preserving provenance, uncertainty, minority cases, and governance. Use when A sample of production LLM traces needs sorting into behavior and failure categories with counts and minority cases; Someone asks what kinds of failures an assistant has in production before anyone looks for causes. Do not use for: Diagnose root causes within a classified production LLM failure cohort (-> production-llm-trace-root-cause-analysis); Configure which AI trace fields the provider collects (-> ai-observability-configuration)."
---

# Production Trace Classification

## Responsibility

Classify authorized production LLM traces into evidence-backed behavior and failure categories while preserving provenance, uncertainty, minority cases, and governance.

## Trigger

Use when the request matches any of:
- A sample of production LLM traces needs sorting into behavior and failure categories with counts and minority cases
- Someone asks what kinds of failures an assistant has in production before anyone looks for causes

Do not use when:
- Diagnose root causes within a classified production LLM failure cohort. Route to `production-llm-trace-root-cause-analysis`.
- Configure which AI trace fields the provider collects. Route to `ai-observability-configuration`.

## Required Inputs

- Authorized trace scope, provider read access, time window, sampling policy, and data-governance boundary.

## Procedure

1. Verify trace source, application, environment, release, prompt and model versions, sample window, selection, consent or rights, minimization, redaction, retention, transfer, access, and deletion.
2. Define operational category criteria and unknown or multi-label handling before reading outcomes broadly.
3. Classify behavior, retrieval, generation, factuality, tool, policy, latency, cost, interaction, and recovery signals with trace IDs and confidence; preserve counterexamples and uncategorized cases.
4. Return taxonomy, counts, evidence, uncertainty, and cohorts for root-cause analysis without changing provider config or claiming causality.

## Domain Guidance

- Label each trace with an outcome of yes, partial or no against the stated task, and report the pass rate as yes over classified traces alongside the counts for partial and no, with the failure-mode table.

## Output Contract

Produce:
- production trace taxonomy
- trace-to-category ledger
- counts, confidence, and minority cases
- governed root-cause cohorts
- outcome labels (yes, partial, no) with pass rate and failure-mode counts

Every material command, request, observation, provider response, finding, decision recommendation, or completion claim must bind to exact target identity and current evidence or be labeled assumption/unknown.

Deliver each output as the artifact itself (tables, commands, patches, plans, records), not as a description of how it would be produced.

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

## Status Mapping

- `passed`: the atomic output and every gate have current target-bound evidence.
- `needs-input`: a requestable target, source, authority, evidence, governance term, or decision is absent. Deliver every supported part first and name the owner for the missing part.
- `blocked`: safe work requires prohibited access, unavailable authority, secret values, stale evidence, or an incompatible identity.
- `failed`: the authorized action ran but a deterministic gate or required output failed.

## Non-Responsibilities

Adjacent capabilities:
- `production-llm-trace-root-cause-analysis`
- `ai-observability-configuration`
- `llm-quality-evaluation`
- `qualitative-evidence-synthesis`

Never silently expand local, repository, provider, production, telemetry, incident, or release authority. Preflight never changes; observation never recovers; coordination never performs specialist actions; rollback never invents a target; one remote authorization never cascades to another action.
