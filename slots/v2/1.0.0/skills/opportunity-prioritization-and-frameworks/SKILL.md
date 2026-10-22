---
name: opportunity-prioritization-and-frameworks
description: Apply an explicitly named prioritization framework and exact formula variant to an evidence-bounded opportunity set. Do not use for synthesize raw evidence into opportunity statements before scoring or approve the highest-scoring item for delivery.
---

# Opportunity Prioritization And Frameworks

## Responsibility

Apply an explicitly named prioritization framework and exact formula variant to an evidence-bounded opportunity set.

## Trigger

Use when the requested outcome is: Apply an explicitly named prioritization framework and exact formula variant to an evidence-bounded opportunity set.

Do not use when:
- Synthesize raw evidence into opportunity statements before scoring. Route to `evidence-synthesis-and-opportunity-prioritization`.
- Approve the highest-scoring item for delivery. Route to `decision-and-outcome-roadmapping`.

## Required Inputs

- Validated problems, opportunities, evidence strength, constraints, and decision criteria.

Also require source identities, authority, decision owner, scope, and declared unknowns where applicable.

## Procedure

1. Verify comparable opportunity definitions, decision owner, time horizon, and required input evidence.
2. Name the framework and exact formula variant; define every variable, scale, direction, and normalization.
3. Record observed values, estimates, confidence, missing data, and sensitivity ranges.
4. Compute scores reproducibly and show how alternate variants or assumptions change ranking.
5. Return ranking as advice with caveats and human selection points.

## Output Contract

Produce:
- framework declaration
- scoring table
- sensitivity analysis
- human decision brief

Every material claim, score, recommendation, or finding must link to a supplied or authorized source, or be labeled assumption/unknown.

## Hard Gates

- Reject any unnamed, hybrid, or partially specified RICE, ICE, Opportunity Score, or custom formula.
- Preserve conflicts, counterevidence, unknowns, source identity, and authority boundaries.
- Return `needs-input` when an identifiable owner can supply a missing requirement or decision.
- Return `blocked` when required authority, evidence, governance, or a safe execution boundary is unavailable.

## Named Formula Variants

When using RICE, ICE, Opportunity Score, or another named framework, record the framework name, exact formula variant, every variable and scale, assumptions, missing values, and sensitivity. Never silently combine formulas.

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
- `evidence-synthesis-and-opportunity-prioritization`
- `decision-and-outcome-roadmapping`
- `results-analysis-and-decision-readout`

Never perform remote Git, external-system writes, merge, deploy, cloud mutation, participant recruitment/contact, or downstream implementation unless a different explicitly authorized capability owns that action.
