---
name: decision-and-outcome-roadmapping
description: "Build an outcome- and decision-based roadmap from approved strategy without converting unvalidated features into commitments. Use when An approved strategy must become a now, next, later roadmap organized by outcomes and decisions rather than features; Someone asks which assumptions must be resolved, and by when, before each roadmap item can be committed. Do not use for: Rank raw opportunities before strategy is approved (-> opportunity-prioritization-and-frameworks); Break an approved roadmap item into implementation tasks (-> implementation-planning-and-handoff)."
---

# Decision And Outcome Roadmapping

## Responsibility

Build an outcome- and decision-based roadmap from approved strategy without converting unvalidated features into commitments.

## Trigger

Use when the request matches any of:
- An approved strategy must become a now, next, later roadmap organized by outcomes and decisions rather than features
- Someone asks which assumptions must be resolved, and by when, before each roadmap item can be committed

Do not use when:
- Rank raw opportunities before strategy is approved. Route to `opportunity-prioritization-and-frameworks`.
- Break an approved roadmap item into implementation tasks. Route to `implementation-planning-and-handoff`.

## Required Inputs

- Strategy, candidate initiatives, experiment conclusions, priorities, capacity, and dependencies.

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

Deliver each output as the artifact itself (tables, commands, patches, plans, records), not as a description of how it would be produced.

## Hard Gates

- A roadmap item must link to an approved outcome and decision gate; feature presence alone is not sufficient.
- Preserve conflicts, counterevidence, unknowns, source identity, and authority boundaries.
- Return `needs-input` when an identifiable owner can supply a missing requirement or decision.
- Return `blocked` when required authority, evidence, governance, or a safe execution boundary is unavailable.
- Deliver every part the supplied evidence and authority support, label assumptions, and list each missing item with the owner who can supply it; `needs-input` or `blocked` applies to the unsupported part, not to the whole deliverable.

## Forbidden Actions

- remote Git, pull-request mutation, merge, deploy, cloud mutation, or external-system write
- invent facts, evidence, authority, approval, or customer data
- perform adjacent or downstream capability responsibilities
- claim evaluation, approval, release, or completion evidence that has not been produced

## Human Decision Authority

Output evidence, options, tradeoffs, unknowns, and a recommendation. GO/PIVOT/KILL, scope approval, strategic selection, taste choices, and build approval remain human decisions; record the owner and decision separately.

## Status Mapping

- `passed`: output contract and every hard gate are satisfied.
- `needs-input`: a requestable source, decision, or governance term is missing. Deliver every supported part first and name the owner for the missing part.
- `blocked`: proceeding would exceed authority, violate governance, or rely on unavailable critical evidence.
- `failed`: supplied inputs were processed but a deterministic gate or required output failed.

## Non-Responsibilities

Adjacent capabilities:
- `opportunity-prioritization-and-frameworks`
- `implementation-planning-and-handoff`
- `strategic-choice-and-differentiation`

Never perform remote Git, external-system writes, merge, deploy, cloud mutation, participant recruitment/contact, or downstream implementation unless a different explicitly authorized capability owns that action.
