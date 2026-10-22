---
name: requirements-and-delivery-contract
description: "Translate approved intent into traceable, observable, testable requirements and acceptance criteria while preserving unknowns and scope. Use when Approved intent must become numbered requirements with observable acceptance criteria; A feature needs an explicit scope boundary, including what is out of scope and why. Do not use for: Discover whether this is the right customer problem to solve (-> problem-framing-and-customer-research); Design the technical architecture and interfaces for approved requirements (-> architecture-candidate-reporting)."
---

# Requirements And Delivery Contract

## Responsibility

Translate approved intent into traceable, observable, testable requirements and acceptance criteria while preserving unknowns and scope.

## Trigger

Use when the request matches any of:
- Approved intent must become numbered requirements with observable acceptance criteria
- A feature needs an explicit scope boundary, including what is out of scope and why

Do not use when:
- Discover whether this is the right customer problem to solve. Route to `problem-framing-and-customer-research`.
- Design the technical architecture and interfaces for approved requirements. Route to `architecture-candidate-reporting`.

## Required Inputs

- Problem and solution evidence, target users, strategy, metrics, risks, and delivery constraints.

## Procedure

1. Verify approved problem, scope, users, outcomes, constraints, authority, and unresolved decisions.
2. Assign stable requirement IDs and write actor-trigger-condition-observable-response statements.
3. Cover normal, alternate, error, empty, boundary, recovery, permission, and non-functional behavior where applicable.
4. Link acceptance criteria to requirements and evidence; reject implementation-only or subjective criteria.
5. Run completeness, consistency, testability, scope, and unknown-preservation gate.

## Domain Guidance

- Every requirement reads actor, trigger, condition, observable response and carries a stable id. Out-of-scope items are listed with the reason they are excluded now.

## Output Contract

Produce:
- requirements specification
- acceptance criteria
- traceability matrix
- unknown and conflict register
- explicit out-of-scope list with rationale and dependencies

Every material claim, score, recommendation, or finding must link to a supplied or authorized source, or be labeled assumption/unknown.

Deliver each output as the artifact itself (tables, commands, patches, plans, records), not as a description of how it would be produced.

## Hard Gates

- Do not invent product behavior, choose architecture, or mark subjective and unobservable outcomes as acceptance criteria.
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
- `problem-framing-and-customer-research`
- `implementation-planning-and-handoff`
- `risk-preflight-and-safety-governance`
- `architecture-candidate-reporting`

Never perform remote Git, external-system writes, merge, deploy, cloud mutation, participant recruitment/contact, or downstream implementation unless a different explicitly authorized capability owns that action.
