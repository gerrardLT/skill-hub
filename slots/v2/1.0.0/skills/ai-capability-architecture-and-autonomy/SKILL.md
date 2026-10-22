---
name: ai-capability-architecture-and-autonomy
description: Classify an approved AI opportunity and route its model/data, agency, interaction, and safety questions to atomic specialist contracts without solving them here. Do not use for design the concrete model routing, retrieval corpus, prompts, and evaluation architecture or define exact action rights, human checkpoints, graduation, revocation, and fallback.
---

# Ai Capability Architecture And Autonomy

## Responsibility

Classify an approved AI opportunity and route its model/data, agency, interaction, and safety questions to atomic specialist contracts without solving them here.

## Trigger

Use when the requested outcome is: Classify an approved AI opportunity and route its model/data, agency, interaction, and safety questions to atomic specialist contracts without solving them here.

Do not use when:
- Design the concrete model routing, retrieval corpus, prompts, and evaluation architecture. Route to `ai-model-and-data-architecture`.
- Define exact action rights, human checkpoints, graduation, revocation, and fallback. Route to `ai-agent-autonomy-and-human-control`.

## Required Inputs

- A customer problem, AI opportunity thesis, quality target, cost constraint, and capability-selection question.

Also require target identity, authorization, trust boundaries, data classes, decision owner, compatibility window, and declared unknowns where applicable.

## Procedure

1. Freeze the approved user value, quality target, latency and cost bounds, data constraints, action needs, and current evidence.
2. Classify capability needs across deterministic logic, generation, retrieval, prediction, tools, memory, autonomy, interaction, and safety.
3. Identify which questions require model/data, agency, AI UX, authorization, or safety specialist contracts and their prerequisites.
4. Expose coupling, conflicts, unknowns, and the non-AI fallback without inventing specialist decisions.
5. Emit a handoff map and bounded architecture options for human prioritization; execute no specialist work.

## Output Contract

Produce:
- AI capability classification
- specialist handoff map
- bounded option set
- unresolved capability-risk ledger

Every material fact, boundary, recommendation, finding, test claim, migration step, or risk must cite supplied or authorized evidence or be labeled assumption/unknown.

## Coverage

- `classification`
- `specialist-routing`
- `non-AI-fallback`
- `unresolved-risks`
- `no-specialist-implementation`

## Hard Gates

- Routing cannot pass by renaming one giant AI design: every unresolved model/data, agency, interaction, authorization, and safety question must remain assigned to its specialist owner.
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
- `ai-model-and-data-architecture`
- `ai-agent-autonomy-and-human-control`
- `ai-interaction-and-probabilistic-ux`
- `ai-safety-and-action-governance`

Never access or emit secret values, mutate production data or provider policy, grant AI action rights, execute remote Git, merge, deploy, release, or perform an adjacent capability. Review, reporting, and audit candidates never repair source.
