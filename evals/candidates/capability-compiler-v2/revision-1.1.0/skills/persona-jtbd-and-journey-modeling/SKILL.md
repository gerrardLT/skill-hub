---
name: persona-jtbd-and-journey-modeling
description: "Model evidence-bounded actors, jobs, circumstances, desired progress, forces, and cross-touchpoint journeys without inventing persona facts. Use when Interview or behavioral evidence must become actors, jobs and a journey without inventing persona details; Someone asks what job a customer hires the product for and what pushes or blocks the switch. Do not use for: Segment the whole market and estimate demand attractiveness (-> market-segmentation-and-demand-intelligence); Design the interface flow that implements this journey (-> design-context-and-direction-contract)."
---

# Persona JTBD And Journey Modeling

## Responsibility

Model evidence-bounded actors, jobs, circumstances, desired progress, forces, and cross-touchpoint journeys without inventing persona facts.

## Trigger

Use when the request matches any of:
- Interview or behavioral evidence must become actors, jobs and a journey without inventing persona details
- Someone asks what job a customer hires the product for and what pushes or blocks the switch

Do not use when:
- Segment the whole market and estimate demand attractiveness. Route to `market-segmentation-and-demand-intelligence`.
- Design the interface flow that implements this journey. Route to `design-context-and-direction-contract`.

## Required Inputs

- Interview evidence, behavioral context, user hypotheses, and touchpoint observations.

## Procedure

1. Establish evidence sources, target decision, actor granularity, and confidence.
2. Separate role, context, behavior, goal, job, desired progress, and unsupported demographic detail.
3. Map trigger, consideration, action, use, failure, recovery, and follow-up touchpoints.
4. Record functional, emotional, and social forces only when supported.
5. Return model, evidence links, contradictions, and research gaps.

## Domain Guidance

- JTBD statement: 'When <situation>, I want to <motivation>, so I can <expected outcome>', each part supported by evidence.
- Forces: push away from the current solution, pull toward the new one, anxiety about switching, and habit of the current way; record only forces that evidence supports.

## Output Contract

Produce:
- persona or actor model
- JTBD statement set
- journey map
- evidence and gap register
- JTBD statements in the standard template with the four forces

Every material claim, score, recommendation, or finding must link to a supplied or authorized source, or be labeled assumption/unknown.

Deliver each output as the artifact itself (tables, commands, patches, plans, records), not as a description of how it would be produced.

## Hard Gates

- Proto-persona decoration, invented demographics, and generic journey stages must never be presented as customer evidence.
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
- `market-segmentation-and-demand-intelligence`
- `qualitative-evidence-synthesis`
- `design-context-and-direction-contract`

Never perform remote Git, external-system writes, merge, deploy, cloud mutation, participant recruitment/contact, or downstream implementation unless a different explicitly authorized capability owns that action.
