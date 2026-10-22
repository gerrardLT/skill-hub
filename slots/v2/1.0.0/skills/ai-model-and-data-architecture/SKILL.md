---
name: ai-model-and-data-architecture
description: Design a bounded model, prompt, retrieval, data-rights, freshness, routing, cost, and evaluation architecture for an approved AI capability. Do not use for define which agent actions require confirmation, interruption, rollback, and autonomy graduation or design uncertainty, correction, and human escalation in the user experience.
---

# Ai Model And Data Architecture

## Responsibility

Design a bounded model, prompt, retrieval, data-rights, freshness, routing, cost, and evaluation architecture for an approved AI capability.

## Trigger

Use when the requested outcome is: Design a bounded model, prompt, retrieval, data-rights, freshness, routing, cost, and evaluation architecture for an approved AI capability.

Do not use when:
- Define which agent actions require confirmation, interruption, rollback, and autonomy graduation. Route to `ai-agent-autonomy-and-human-control`.
- Design uncertainty, correction, and human escalation in the user experience. Route to `ai-interaction-and-probabilistic-ux`.

## Required Inputs

- An AI task, data sources, latency and cost constraints, model options, and quality targets.

Also require target identity, authorization, trust boundaries, data classes, decision owner, compatibility window, and declared unknowns where applicable.

## Procedure

1. Freeze task quality, latency, cost, privacy, residency, licensing, freshness, availability, and evaluation requirements.
2. Inventory candidate models and deterministic alternatives with versions, context limits, provider boundaries, and failure modes.
3. Define data sources, rights, minimization, redaction, lineage, chunking or feature preparation, freshness, deletion, and contamination controls.
4. Design routing, prompt and tool context, retrieval, caching, fallback, observability, and versioned interfaces without exposing secrets.
5. Define offline and online evaluation, slices, thresholds, cost and latency budgets, drift triggers, and migration or rollback before recommending an option.

## Output Contract

Produce:
- model and routing architecture
- governed data and freshness contract
- prompt and retrieval boundary
- evaluation, migration, and rollback plan

Every material fact, boundary, recommendation, finding, test claim, migration step, or risk must cite supplied or authorized evidence or be labeled assumption/unknown.

## Coverage

- `model-routing`
- `data-rights`
- `lineage`
- `freshness`
- `prompt-boundary`
- `evaluation`
- `cost-latency`
- `migration-rollback`

## Hard Gates

- No model or data path may be recommended without lawful authority, provenance, minimization, freshness and deletion behavior, evaluation slices, failure fallback, and migration or rollback.
- Preserve trust boundaries, authorization, data and secret governance, compatibility, migration, rollback or containment, source identity, counterevidence, and residual risk where applicable.
- Return `needs-input` when a named owner can supply a missing fact, policy, evidence, or approval.
- Return `blocked` when safe analysis or mutation would require unavailable authority, secret values, prohibited tests, remote writes, or unresolved high-impact risk.

## Data and Secret Governance

Require explicit authority, purpose limitation, minimization, provenance, residency or transfer, retention, deletion, and incident boundaries for customer, proprietary, evaluation, or AI data. Never request or expose secret values. Missing governance returns `needs-input`; prohibited or unavailable authority returns `blocked`.

## Human Architecture and Risk Authority

The Skill may produce evidence, alternatives, tradeoffs, findings, and a recommendation. Architecture selection, autonomy expansion, risk acceptance, policy approval, migration approval, remediation authorization, and release decisions remain explicit human decisions with a named owner.

## Status Mapping

- `passed`: output contract and every hard gate are satisfied with current evidence.
- `needs-input`: a requestable source, policy, compatibility fact, or decision is missing.
- `blocked`: proceeding would exceed authority, access secret values, mutate production, or cross a prohibited safety boundary.
- `failed`: authorized work ran but a deterministic gate or required output failed.

## Non-Responsibilities

Does not approve upstream product decisions, expand authority, or perform remote writes beyond its explicit permission identity.

Adjacent capabilities:
- `ai-capability-architecture-and-autonomy`
- `ai-agent-autonomy-and-human-control`
- `ai-interaction-and-probabilistic-ux`
- `data-and-api-contract-design`

Never access or emit secret values, mutate production data or provider policy, grant AI action rights, execute remote Git, merge, deploy, release, or perform an adjacent capability. Review, reporting, and audit candidates never repair source.
