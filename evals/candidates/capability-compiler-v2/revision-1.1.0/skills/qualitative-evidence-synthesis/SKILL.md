---
name: qualitative-evidence-synthesis
description: "Code authorized qualitative observations into traceable themes, counterexamples, contradictions, and confidence without ranking solutions. Use when Interview notes and quotes must be coded into themes with counterexamples and contradictions preserved; Someone asks what the qualitative evidence actually supports and where it is thin or split. Do not use for: Turn the synthesized themes into prioritized opportunities (-> evidence-synthesis-and-opportunity-prioritization); Run the interviews that produce the raw evidence (-> customer-interview-execution)."
---

# Qualitative Evidence Synthesis

## Responsibility

Code authorized qualitative observations into traceable themes, counterexamples, contradictions, and confidence without ranking solutions.

## Trigger

Use when the request matches any of:
- Interview notes and quotes must be coded into themes with counterexamples and contradictions preserved
- Someone asks what the qualitative evidence actually supports and where it is thin or split

Do not use when:
- Turn the synthesized themes into prioritized opportunities. Route to `evidence-synthesis-and-opportunity-prioritization`.
- Run the interviews that produce the raw evidence. Route to `customer-interview-execution`.

## Required Inputs

- Interview notes, direct quotes, affinity material, journey evidence, and known bias.

## Procedure

1. Verify consent, minimization, redaction, retention, external-transfer, corpus identity, and analysis question.
2. Separate quote, observation, analyst code, interpretation, and unsupported inference.
3. Code records consistently and retain source IDs.
4. Synthesize themes with prevalence context, counterexamples, contradictions, and saturation limits.
5. Return findings and gaps without making priority or product decisions.

## Domain Guidance

- Characterize each theme by depth (how strongly it affects those who hold it) and breadth (how many participants) as description only; this is not prioritization. Keep every minority or contradicting account as its own entry with its source id and say how it limits the theme.

## Output Contract

Produce:
- coded evidence table
- theme map
- counterexample register
- confidence and saturation notes
- depth and breadth characterization per theme

Every material claim, score, recommendation, or finding must link to a supplied or authorized source, or be labeled assumption/unknown.

Deliver each output as the artifact itself (tables, commands, patches, plans, records), not as a description of how it would be produced.

## Hard Gates

- Do not expose raw participant data, count quotes as population prevalence, or erase minority and contradictory evidence.
- Preserve conflicts, counterevidence, unknowns, source identity, and authority boundaries.
- Return `needs-input` when an identifiable owner can supply a missing requirement or decision.
- Return `blocked` when required authority, evidence, governance, or a safe execution boundary is unavailable.
- Deliver every part the supplied evidence and authority support, label assumptions, and list each missing item with the owner who can supply it; `needs-input` or `blocked` applies to the unsupported part, not to the whole deliverable.

## Forbidden Actions

- remote Git, pull-request mutation, merge, deploy, cloud mutation, or external-system write
- invent facts, evidence, authority, approval, or customer data
- perform adjacent or downstream capability responsibilities
- claim evaluation, approval, release, or completion evidence that has not been produced

## Data Governance

Before using interviews, customer or proprietary data, recordings, or an external LLM Judge, require explicit authorization, minimization, redaction, retention, external-transfer, access, deletion, and incident boundaries. Missing governance returns `needs-input`; unavailable or prohibited authority returns `blocked`.

## Status Mapping

- `passed`: output contract and every hard gate are satisfied.
- `needs-input`: a requestable source, decision, or governance term is missing. Deliver every supported part first and name the owner for the missing part.
- `blocked`: proceeding would exceed authority, violate governance, or rely on unavailable critical evidence.
- `failed`: supplied inputs were processed but a deterministic gate or required output failed.

## Non-Responsibilities

Adjacent capabilities:
- `customer-interview-execution`
- `evidence-synthesis-and-opportunity-prioritization`
- `data-analysis-validation`

Never perform remote Git, external-system writes, merge, deploy, cloud mutation, participant recruitment/contact, or downstream implementation unless a different explicitly authorized capability owns that action.
