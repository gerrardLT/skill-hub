---
name: ai-product-opportunity-and-wedge
description: Assess whether AI creates defensible user value and choose a narrow evidence-backed entry wedge. Do not use for design the model, vector database, and inference architecture for this approved ai feature or write acceptance criteria for the approved ai assistant scope.
---

# Ai Product Opportunity And Wedge

## Responsibility

Assess whether AI creates defensible user value and choose a narrow evidence-backed entry wedge.

## Trigger

Use when the requested outcome is: Assess whether AI creates defensible user value and choose a narrow evidence-backed entry wedge.

Do not use when:
- Design the model, vector database, and inference architecture for this approved AI feature. Route to `ai-model-and-data-architecture`.
- Write acceptance criteria for the approved AI assistant scope. Route to `requirements-and-delivery-contract`.

## Required Inputs

- A validated customer problem, workflow friction, model trajectory, data advantage, and business constraint.

Also require source identities, authority, decision owner, scope, and declared unknowns where applicable.

## Procedure

1. State the user job, current workaround, pain, and evidence strength.
2. Compare AI leverage with a simpler deterministic or human process.
3. Map required data rights, feedback loop, failure cost, and human-control boundary.
4. Select the smallest wedge that can test differentiated value; preserve alternatives and unknowns.
5. Return a recommendation and falsification conditions for human decision.

## Output Contract

Produce:
- AI opportunity brief
- wedge hypothesis
- non-AI alternative
- data and feedback-loop risks

Every material claim, score, recommendation, or finding must link to a supplied or authorized source, or be labeled assumption/unknown.

## Hard Gates

- Do not treat probabilistic behavior, novelty, or model availability as proof of user value or product approval.
- Preserve conflicts, counterevidence, unknowns, source identity, and authority boundaries.
- Return `needs-input` when an identifiable owner can supply a missing requirement or decision.
- Return `blocked` when required authority, evidence, governance, or a safe execution boundary is unavailable.

## Data Governance

Before using interviews, customer or proprietary data, recordings, or an external LLM Judge, require explicit authorization, minimization, redaction, retention, external-transfer, access, deletion, and incident boundaries. Missing governance returns `needs-input`; unavailable or prohibited authority returns `blocked`.

## Human Decision Authority

Output evidence, options, tradeoffs, unknowns, and a recommendation. GO/PIVOT/KILL, scope approval, strategic selection, taste choices, and build approval remain human decisions; record the owner and decision separately.

## Status Mapping

- `passed`: output contract and every hard gate are satisfied.
- `needs-input`: a requestable source, decision, or governance term is missing.
- `blocked`: proceeding would exceed authority, violate governance, or rely on unavailable critical evidence.
- `failed`: supplied inputs were processed but a deterministic gate or required output failed.

## Non-Responsibilities

Does not approve upstream product decisions, expand authority, or perform remote writes beyond its explicit permission identity.

Adjacent capabilities:
- `solution-hypothesis-and-experiment-design`
- `ai-model-and-data-architecture`
- `strategic-choice-and-differentiation`

Never perform remote Git, external-system writes, merge, deploy, cloud mutation, participant recruitment/contact, or downstream implementation unless a different explicitly authorized capability owns that action.
