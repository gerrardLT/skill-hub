---
name: context-intake-and-routing
description: "Classify a request, authority, evidence state, lifecycle stage, and next atomic capability without doing downstream work. Use when A request spans several domains or lifecycle stages and someone must decide which single capability should act first; A vague ask arrives with unclear authority, risk or evidence state and needs classification before any work starts. Do not use for: Research the customer's underlying problem from these notes (-> problem-framing-and-customer-research); Orchestrate the approved multi-stage capability workflow (-> workflow-orchestration-and-lifecycle); Classify a request that is purely about UI design, review or remediation (-> ui-task-routing-and-governance)."
---

# Context Intake And Routing

## Responsibility

Classify a request, authority, evidence state, lifecycle stage, and next atomic capability without doing downstream work.

## Trigger

Use when the request matches any of:
- A request spans several domains or lifecycle stages and someone must decide which single capability should act first
- A vague ask arrives with unclear authority, risk or evidence state and needs classification before any work starts

Do not use when:
- Research the customer's underlying problem from these notes. Route to `problem-framing-and-customer-research`.
- Orchestrate the approved multi-stage capability workflow. Route to `workflow-orchestration-and-lifecycle`.
- Classify a request that is purely about UI design, review or remediation. Route to `ui-task-routing-and-governance`.

## Required Inputs

- A request, existing artifacts, project context, and known constraints.

## Procedure

1. Inventory the request, supplied artifacts, requested outcome, and explicit exclusions.
2. Classify lifecycle stage, reversibility, risk, data sensitivity, and decision owner.
3. Identify missing prerequisites and incompatible authority.
4. Select one next capability or return needs-input/blocked with reasons.
5. Emit only a routing envelope and preserved unknowns.

## Domain Guidance

- Routing decision table: stage (discover, plan, design, build, verify, release, operate, learn) x risk (reversible, costly to reverse, irreversible) x authority (supplied, missing, conflicting). The next capability is the one that owns the earliest unmet prerequisite; irreversible or authority-missing rows stop at needs-input.
- Select exactly one next capability and at most two conditional follow-ups; name the Recipe when an existing Recipe already covers the request instead of composing a new path.
- Classification is authored method, not derived from an external source.
- Routing ownership: the V2 router selects Recipes; this Skill classifies cross-domain requests and names the next capability.

## Output Contract

Produce:
- intake register
- routing decision
- missing-input list
- authority boundary

Every material claim, score, recommendation, or finding must link to a supplied or authorized source, or be labeled assumption/unknown.

Deliver each output as the artifact itself (tables, commands, patches, plans, records), not as a description of how it would be produced.

## Hard Gates

- Never manufacture domain analysis merely to justify a route; route only from supplied evidence and declared scope.
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
- `workflow-orchestration-and-lifecycle`
- `risk-preflight-and-safety-governance`
- `problem-framing-and-customer-research`
- `ui-task-routing-and-governance`

Never perform remote Git, external-system writes, merge, deploy, cloud mutation, participant recruitment/contact, or downstream implementation unless a different explicitly authorized capability owns that action.
