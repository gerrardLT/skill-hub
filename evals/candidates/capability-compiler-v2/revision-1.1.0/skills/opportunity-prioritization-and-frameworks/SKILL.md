---
name: opportunity-prioritization-and-frameworks
description: "Apply an explicitly named prioritization framework and exact formula variant to an evidence-bounded opportunity set. Use when A set of opportunities must be ranked with a named formula such as RICE, ICE or Opportunity Score; Someone asks for a reproducible score and how the ranking changes if the inputs change. Do not use for: Synthesize raw evidence into opportunity statements before scoring (-> evidence-synthesis-and-opportunity-prioritization); Approve the highest-scoring item for delivery (-> decision-and-outcome-roadmapping)."
---

# Opportunity Prioritization And Frameworks

## Responsibility

Apply an explicitly named prioritization framework and exact formula variant to an evidence-bounded opportunity set.

## Trigger

Use when the request matches any of:
- A set of opportunities must be ranked with a named formula such as RICE, ICE or Opportunity Score
- Someone asks for a reproducible score and how the ranking changes if the inputs change

Do not use when:
- Synthesize raw evidence into opportunity statements before scoring. Route to `evidence-synthesis-and-opportunity-prioritization`.
- Approve the highest-scoring item for delivery. Route to `decision-and-outcome-roadmapping`.

## Required Inputs

- Validated problems, opportunities, evidence strength, constraints, and decision criteria.

## Procedure

1. Verify comparable opportunity definitions, decision owner, time horizon, and required input evidence.
2. Name the framework and exact formula variant; define every variable, scale, direction, and normalization.
3. Record observed values, estimates, confidence, missing data, and sensitivity ranges.
4. Compute scores reproducibly and show how alternate variants or assumptions change ranking.
5. Return ranking as advice with caveats and human selection points.

## Domain Guidance

- Canonical variants: RICE = (Reach x Impact x Confidence) / Effort with Reach in users per period, Impact on a stated scale, Confidence 0-100% and Effort in person-months; ICE = (Impact + Confidence + Ease) / 3 or the product, as named; Opportunity Score = Importance + max(Importance - Satisfaction, 0). Compute the variant the owner named. If the owner names a mix, compute the closest canonical variant and state the difference.
- Always compute the scores, show the arithmetic, and show the ranking under at least one alternate assumption (sensitivity).
- When an input is missing (for example an effort estimate), still deliver: compute provisional scores with the assumption labelled, give the ranking for items with known inputs, show how the ranking moves across the plausible range of the missing value, and name the owner who can supply it. Never declare the ranking indeterminate with no scores. Where sources conflict (survey versus usage), tie the conflict to the confidence score.

## Output Contract

Produce:
- framework declaration
- scoring table
- sensitivity analysis
- human decision brief
- canonical variant definition and arithmetic for every score

Every material claim, score, recommendation, or finding must link to a supplied or authorized source, or be labeled assumption/unknown.

Deliver each output as the artifact itself (tables, commands, patches, plans, records), not as a description of how it would be produced.

## Hard Gates

- Reject any unnamed, hybrid, or partially specified RICE, ICE, Opportunity Score, or custom formula.
- Preserve conflicts, counterevidence, unknowns, source identity, and authority boundaries.
- Return `needs-input` when an identifiable owner can supply a missing requirement or decision.
- Return `blocked` when required authority, evidence, governance, or a safe execution boundary is unavailable.
- Deliver every part the supplied evidence and authority support, label assumptions, and list each missing item with the owner who can supply it; `needs-input` or `blocked` applies to the unsupported part, not to the whole deliverable.

## Forbidden Actions

- remote Git, pull-request mutation, merge, deploy, cloud mutation, or external-system write
- invent facts, evidence, authority, approval, or customer data
- perform adjacent or downstream capability responsibilities
- claim evaluation, approval, release, or completion evidence that has not been produced

## Named Formula Variants

When using RICE, ICE, Opportunity Score, or another named framework, record the framework name, exact formula variant, every variable and scale, assumptions, missing values, and sensitivity. Never silently combine formulas.

## Human Decision Authority

Output evidence, options, tradeoffs, unknowns, and a recommendation. GO/PIVOT/KILL, scope approval, strategic selection, taste choices, and build approval remain human decisions; record the owner and decision separately.

## Status Mapping

- `passed`: output contract and every hard gate are satisfied.
- `needs-input`: a requestable source, decision, or governance term is missing. Deliver every supported part first and name the owner for the missing part.
- `blocked`: proceeding would exceed authority, violate governance, or rely on unavailable critical evidence.
- `failed`: supplied inputs were processed but a deterministic gate or required output failed.

## Non-Responsibilities

Adjacent capabilities:
- `evidence-synthesis-and-opportunity-prioritization`
- `decision-and-outcome-roadmapping`
- `results-analysis-and-decision-readout`

Never perform remote Git, external-system writes, merge, deploy, cloud mutation, participant recruitment/contact, or downstream implementation unless a different explicitly authorized capability owns that action.
