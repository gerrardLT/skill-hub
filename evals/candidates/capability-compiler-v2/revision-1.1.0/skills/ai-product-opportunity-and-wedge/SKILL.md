---
name: ai-product-opportunity-and-wedge
description: "Assess whether AI creates defensible user value and choose a narrow evidence-backed entry wedge. Use when A team asks whether AI gives real, defensible user value for a workflow and which narrow entry point to start with; Someone wants AI wedge candidates compared against a simpler non-AI alternative with falsification conditions. Do not use for: Design the model, vector database, and inference architecture for this approved AI feature (-> ai-model-and-data-architecture); Write acceptance criteria for the approved AI assistant scope (-> requirements-and-delivery-contract)."
---

# AI Product Opportunity And Wedge

## Responsibility

Assess whether AI creates defensible user value and choose a narrow evidence-backed entry wedge.

## Trigger

Use when the request matches any of:
- A team asks whether AI gives real, defensible user value for a workflow and which narrow entry point to start with
- Someone wants AI wedge candidates compared against a simpler non-AI alternative with falsification conditions

Do not use when:
- Design the model, vector database, and inference architecture for this approved AI feature. Route to `ai-model-and-data-architecture`.
- Write acceptance criteria for the approved AI assistant scope. Route to `requirements-and-delivery-contract`.

## Required Inputs

- A validated customer problem, workflow friction, model trajectory, data advantage, and business constraint.

## Procedure

1. State the user job, current workaround, pain, and evidence strength.
2. Compare AI leverage with a simpler deterministic or human process.
3. Map required data rights, feedback loop, failure cost, and human-control boundary.
4. Select the smallest wedge that can test differentiated value; preserve alternatives and unknowns.
5. Return a recommendation and falsification conditions for human decision.

## Domain Guidance

- Score each candidate wedge on promise to payoff: the ratio of user effort removed to reward delivered, how often the workflow runs, and how repeatable its steps are. Pick the smallest wedge that tests differentiated value.
- Rate defensibility by layer, most to least durable: proprietary or uniquely accessible data, then interface and workflow integration, then the model itself. A model-only advantage is rated weak because any competitor can buy the same model.
- Always state the non-AI alternative and the condition under which the AI wedge would be falsified.

## Output Contract

Produce:
- AI opportunity brief
- wedge hypothesis
- non-AI alternative
- data and feedback-loop risks
- wedge scoring table (promise-to-payoff) and defensibility rating by data, interface and model layer

Every material claim, score, recommendation, or finding must link to a supplied or authorized source, or be labeled assumption/unknown.

Deliver each output as the artifact itself (tables, commands, patches, plans, records), not as a description of how it would be produced.

## Hard Gates

- Do not treat probabilistic behavior, novelty, or model availability as proof of user value or product approval.
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

## Human Decision Authority

Output evidence, options, tradeoffs, unknowns, and a recommendation. GO/PIVOT/KILL, scope approval, strategic selection, taste choices, and build approval remain human decisions; record the owner and decision separately.

## Status Mapping

- `passed`: output contract and every hard gate are satisfied.
- `needs-input`: a requestable source, decision, or governance term is missing. Deliver every supported part first and name the owner for the missing part.
- `blocked`: proceeding would exceed authority, violate governance, or rely on unavailable critical evidence.
- `failed`: supplied inputs were processed but a deterministic gate or required output failed.

## Non-Responsibilities

Adjacent capabilities:
- `solution-hypothesis-and-experiment-design`
- `ai-model-and-data-architecture`
- `strategic-choice-and-differentiation`
- `requirements-and-delivery-contract`

Never perform remote Git, external-system writes, merge, deploy, cloud mutation, participant recruitment/contact, or downstream implementation unless a different explicitly authorized capability owns that action.
