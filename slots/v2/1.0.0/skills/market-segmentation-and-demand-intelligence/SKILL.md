---
name: market-segmentation-and-demand-intelligence
description: Segment demand using evidence-backed differences in job, context, urgency, willingness, constraints, and reachability. Do not use for create a detailed evidence-bounded persona and journey for the selected segment or choose the final strategic segment and commit resources.
---

# Market Segmentation And Demand Intelligence

## Responsibility

Segment demand using evidence-backed differences in job, context, urgency, willingness, constraints, and reachability.

## Trigger

Use when the requested outcome is: Segment demand using evidence-backed differences in job, context, urgency, willingness, constraints, and reachability.

Do not use when:
- Create a detailed evidence-bounded persona and journey for the selected segment. Route to `persona-jtbd-and-journey-modeling`.
- Choose the final strategic segment and commit resources. Route to `strategic-choice-and-differentiation`.

## Required Inputs

- Customer situations, alternatives, segment constraints, incumbent observations, and market evidence.

Also require source identities, authority, decision owner, scope, and declared unknowns where applicable.

## Procedure

1. Define market boundary, unit of analysis, sources, time window, and decision use.
2. Identify candidate segments from job, trigger, pain, urgency, workaround, willingness, constraints, and reachability.
3. Estimate demand evidence and uncertainty without inventing market size.
4. Compare segment attractiveness, access, strategic fit, and exclusion risk.
5. Return segment hypotheses and validation gaps for human choice.

## Output Contract

Produce:
- segment model
- demand evidence matrix
- segment attractiveness comparison
- validation backlog

Every material claim, score, recommendation, or finding must link to a supplied or authorized source, or be labeled assumption/unknown.

## Hard Gates

- Demographics alone do not constitute a demand segment, and missing market evidence must not become fabricated TAM.
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
- `persona-jtbd-and-journey-modeling`
- `market-positioning-and-competitive-power`
- `strategic-choice-and-differentiation`

Never perform remote Git, external-system writes, merge, deploy, cloud mutation, participant recruitment/contact, or downstream implementation unless a different explicitly authorized capability owns that action.
