---
name: ai-model-and-data-architecture
description: "Classify an approved AI opportunity's capability needs with a non-AI fallback, then design a bounded model, prompt, retrieval, data-rights, freshness, routing, cost, and evaluation architecture for it. Use when An approved AI capability needs its model, prompt, retrieval and data design, including whether AI is needed at all; Someone asks whether to use prompting, RAG, fine-tuning or tools, and what data rights, freshness and evaluation that choice needs. Do not use for: Define which agent actions require confirmation, interruption, rollback, and autonomy graduation (-> ai-agent-autonomy-and-human-control); Design uncertainty, correction, and human escalation in the user experience (-> ai-interaction-and-probabilistic-ux)."
---

# AI Model And Data Architecture

## Responsibility

Classify an approved AI opportunity's capability needs with a non-AI fallback, then design a bounded model, prompt, retrieval, data-rights, freshness, routing, cost, and evaluation architecture for it.

## Trigger

Use when the request matches any of:
- An approved AI capability needs its model, prompt, retrieval and data design, including whether AI is needed at all
- Someone asks whether to use prompting, RAG, fine-tuning or tools, and what data rights, freshness and evaluation that choice needs

Do not use when:
- Define which agent actions require confirmation, interruption, rollback, and autonomy graduation. Route to `ai-agent-autonomy-and-human-control`.
- Design uncertainty, correction, and human escalation in the user experience. Route to `ai-interaction-and-probabilistic-ux`.

## Required Inputs

- An approved AI opportunity or task, data sources, latency and cost constraints, model options, and quality targets.

## Procedure

1. Classify the capability needs and state the non-AI fallback; list unresolved agency, interaction and safety questions as named specialist handoffs.
2. Freeze task quality, latency, cost, privacy, residency, licensing, freshness, availability, and evaluation requirements.
3. Inventory candidate models and deterministic alternatives with versions, context limits, provider boundaries, and failure modes.
4. Define data sources, rights, minimization, redaction, lineage, chunking or feature preparation, freshness, deletion, and contamination controls.
5. Design routing, prompt and tool context, retrieval, caching, fallback, observability, and versioned interfaces without exposing secrets.
6. Define offline and online evaluation, slices, thresholds, cost and latency budgets, drift triggers, and migration or rollback before recommending an option.

## Domain Guidance

- Technique decision table: prompting or role instructions when the gap is instructions; RAG when the model needs live, private or changing context it was not trained on (an open-book test); fine-tuning when behavior or style must be consistently specialized; tools when a deterministic system of record must be called. Choose on dynamic context versus behavior specialization.
- Classify capability needs across deterministic logic, generation, retrieval, prediction, tools, memory, autonomy, interaction and safety, and always state the non-AI fallback.
- Questions this design does not own stay with their specialists: action rights to ai-agent-autonomy-and-human-control, interaction states to ai-interaction-and-probabilistic-ux, abuse and injection risk to ai-safety-and-action-governance. List each as a handoff rather than deciding it here.
- Discriminator: owns which model, data and capability design an AI feature uses, including which steps may act autonomously; it does not set the human-control model, the safety policy or the interaction design.

## Output Contract

Produce:
- model and routing architecture
- governed data and freshness contract
- prompt and retrieval boundary
- evaluation, migration, and rollback plan
- capability classification with non-AI fallback
- specialist handoff map

Every material fact, boundary, recommendation, finding, test claim, migration step, or risk must cite supplied or authorized evidence or be labeled assumption/unknown.

Deliver each output as the artifact itself (tables, commands, patches, plans, records), not as a description of how it would be produced.

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
- Review, reporting, contract, and audit candidates never imply implementation, live policy change, production mutation, or risk acceptance.
- Preserve trust boundaries, authorization, data and secret governance, compatibility, migration, rollback or containment, source identity, counterevidence, and residual risk where applicable.
- Return `needs-input` when a named owner can supply a missing fact, policy, evidence, or approval.
- Return `blocked` when safe analysis or mutation would require unavailable authority, secret values, prohibited tests, remote writes, or unresolved high-impact risk.
- Deliver every part the supplied evidence and authority support, label assumptions, and list each missing item with the owner who can supply it; `needs-input` or `blocked` applies to the unsupported part, not to the whole deliverable.

## Forbidden Actions

- request, read, print, persist, hash, or transmit secret values
- remote Git, merge, deploy, release, provider-policy mutation, production-data mutation, or AI action-right activation
- invent architecture facts, data rights, authorization, evidence, approval, migration safety, or risk acceptance
- combine independent review or audit with source remediation
- claim evaluation, approval, release, or completion evidence that has not been produced

## Data and Secret Governance

Require explicit authority, purpose limitation, minimization, provenance, residency or transfer, retention, deletion, and incident boundaries for customer, proprietary, evaluation, or AI data. Never request or expose secret values. Missing governance returns `needs-input`; prohibited or unavailable authority returns `blocked`.

## Human Architecture and Risk Authority

The Skill may produce evidence, alternatives, tradeoffs, findings, and a recommendation. Architecture selection, autonomy expansion, risk acceptance, policy approval, migration approval, remediation authorization, and release decisions remain explicit human decisions with a named owner.

## Status Mapping

- `passed`: output contract and every hard gate are satisfied with current evidence.
- `needs-input`: a requestable source, policy, compatibility fact, or decision is missing. Deliver every supported part first and name the owner for the missing part.
- `blocked`: proceeding would exceed authority, access secret values, mutate production, or cross a prohibited safety boundary.
- `failed`: authorized work ran but a deterministic gate or required output failed.

## Non-Responsibilities

Adjacent capabilities:
- `ai-agent-autonomy-and-human-control`
- `ai-interaction-and-probabilistic-ux`
- `data-and-api-contract-design`

Never access or emit secret values, mutate production data or provider policy, grant AI action rights, execute remote Git, merge, deploy, release, or perform an adjacent capability. Review, reporting, and audit candidates never repair source.
