---
name: decision-and-outcome-roadmapping
description: Build an outcome- and decision-based roadmap from approved strategy without converting unvalidated features into commitments. Do not use for rank raw opportunities before strategy is approved or break an approved roadmap item into implementation tasks.
---

# Decision And Outcome Roadmapping

## Responsibility

Build an outcome- and decision-based roadmap from approved strategy without converting unvalidated features into commitments.

## Trigger

Use when the requested outcome is: Build an outcome- and decision-based roadmap from approved strategy without converting unvalidated features into commitments.

Do not use when:
- Rank raw opportunities before strategy is approved. Route to `opportunity-prioritization-and-frameworks`.
- Break an approved roadmap item into implementation tasks. Route to `implementation-planning-and-handoff`.

## Required Inputs

- Strategy, candidate initiatives, experiment conclusions, priorities, capacity, and dependencies.

Also require source identities, authority, decision owner, scope, and declared unknowns where applicable.

## Procedure

1. Freeze approved outcomes, constraints, strategic choices, and decision owners.
2. Map assumptions and evidence needed to unlock each decision.
3. Sequence now/next/later horizons by dependency and learning value, not false date precision.
4. Represent options, kill criteria, and reversible commitments explicitly.
5. Define review cadence and handoff criteria without approving work.

## Output Contract

Produce:
- outcome roadmap
- decision map
- assumption ledger
- review cadence

Every material claim, score, recommendation, or finding must link to a supplied or authorized source, or be labeled assumption/unknown.

## Hard Gates

- A roadmap item must link to an approved outcome and decision gate; feature presence alone is not sufficient.
- Preserve conflicts, counterevidence, unknowns, source identity, and authority boundaries.
- Return `needs-input` when an identifiable owner can supply a missing requirement or decision.
- Return `blocked` when required authority, evidence, governance, or a safe execution boundary is unavailable.

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
- `opportunity-prioritization-and-frameworks`
- `implementation-planning-and-handoff`
- `strategic-choice-and-differentiation`

Never perform remote Git, external-system writes, merge, deploy, cloud mutation, participant recruitment/contact, or downstream implementation unless a different explicitly authorized capability owns that action.
