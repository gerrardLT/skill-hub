---
name: persona-jtbd-and-journey-modeling
description: Model evidence-bounded actors, jobs, circumstances, desired progress, forces, and cross-touchpoint journeys without inventing persona facts. Do not use for segment the whole market and estimate demand attractiveness or design the interface flow that implements this journey.
---

# Persona Jtbd And Journey Modeling

## Responsibility

Model evidence-bounded actors, jobs, circumstances, desired progress, forces, and cross-touchpoint journeys without inventing persona facts.

## Trigger

Use when the requested outcome is: Model evidence-bounded actors, jobs, circumstances, desired progress, forces, and cross-touchpoint journeys without inventing persona facts.

Do not use when:
- Segment the whole market and estimate demand attractiveness. Route to `market-segmentation-and-demand-intelligence`.
- Design the interface flow that implements this journey. Route to `design-context-and-direction-contract`.

## Required Inputs

- Interview evidence, behavioral context, user hypotheses, and touchpoint observations.

Also require source identities, authority, decision owner, scope, and declared unknowns where applicable.

## Procedure

1. Establish evidence sources, target decision, actor granularity, and confidence.
2. Separate role, context, behavior, goal, job, desired progress, and unsupported demographic detail.
3. Map trigger, consideration, action, use, failure, recovery, and follow-up touchpoints.
4. Record functional, emotional, and social forces only when supported.
5. Return model, evidence links, contradictions, and research gaps.

## Output Contract

Produce:
- persona or actor model
- JTBD statement set
- journey map
- evidence and gap register

Every material claim, score, recommendation, or finding must link to a supplied or authorized source, or be labeled assumption/unknown.

## Hard Gates

- Proto-persona decoration, invented demographics, and generic journey stages must never be presented as customer evidence.
- Preserve conflicts, counterevidence, unknowns, source identity, and authority boundaries.
- Return `needs-input` when an identifiable owner can supply a missing requirement or decision.
- Return `blocked` when required authority, evidence, governance, or a safe execution boundary is unavailable.

## Data Governance

Before using interviews, customer or proprietary data, recordings, or an external LLM Judge, require explicit authorization, minimization, redaction, retention, external-transfer, access, deletion, and incident boundaries. Missing governance returns `needs-input`; unavailable or prohibited authority returns `blocked`.

## Status Mapping

- `passed`: output contract and every hard gate are satisfied.
- `needs-input`: a requestable source, decision, or governance term is missing.
- `blocked`: proceeding would exceed authority, violate governance, or rely on unavailable critical evidence.
- `failed`: supplied inputs were processed but a deterministic gate or required output failed.

## Non-Responsibilities

Does not approve upstream product decisions, expand authority, or perform remote writes beyond its explicit permission identity.

Adjacent capabilities:
- `market-segmentation-and-demand-intelligence`
- `qualitative-evidence-synthesis`
- `design-context-and-direction-contract`

Never perform remote Git, external-system writes, merge, deploy, cloud mutation, participant recruitment/contact, or downstream implementation unless a different explicitly authorized capability owns that action.
