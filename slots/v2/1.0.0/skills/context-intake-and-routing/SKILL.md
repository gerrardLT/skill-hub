---
name: context-intake-and-routing
description: Classify a request, authority, evidence state, lifecycle stage, and next atomic capability without doing downstream work. Do not use for research the customer's underlying problem from these notes or orchestrate the approved multi-stage capability workflow.
---

# Context Intake And Routing

## Responsibility

Classify a request, authority, evidence state, lifecycle stage, and next atomic capability without doing downstream work.

## Trigger

Use when the requested outcome is: Classify a request, authority, evidence state, lifecycle stage, and next atomic capability without doing downstream work.

Do not use when:
- Research the customer's underlying problem from these notes. Route to `problem-framing-and-customer-research`.
- Orchestrate the approved multi-stage capability workflow. Route to `workflow-orchestration-and-lifecycle`.

## Required Inputs

- A request, existing artifacts, project context, and known constraints.

Also require source identities, authority, decision owner, scope, and declared unknowns where applicable.

## Procedure

1. Inventory the request, supplied artifacts, requested outcome, and explicit exclusions.
2. Classify lifecycle stage, reversibility, risk, data sensitivity, and decision owner.
3. Identify missing prerequisites and incompatible authority.
4. Select one next capability or return needs-input/blocked with reasons.
5. Emit only a routing envelope and preserved unknowns.

## Output Contract

Produce:
- intake register
- routing decision
- missing-input list
- authority boundary

Every material claim, score, recommendation, or finding must link to a supplied or authorized source, or be labeled assumption/unknown.

## Hard Gates

- Never manufacture domain analysis merely to justify a route; route only from supplied evidence and declared scope.
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
- `workflow-orchestration-and-lifecycle`
- `risk-preflight-and-safety-governance`
- `problem-framing-and-customer-research`

Never perform remote Git, external-system writes, merge, deploy, cloud mutation, participant recruitment/contact, or downstream implementation unless a different explicitly authorized capability owns that action.
