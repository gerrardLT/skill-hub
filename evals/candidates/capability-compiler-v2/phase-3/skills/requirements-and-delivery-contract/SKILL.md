---
name: requirements-and-delivery-contract
description: Translate approved intent into traceable, observable, testable requirements and acceptance criteria while preserving unknowns and scope. Do not use for discover whether this is the right customer problem to solve or design the technical architecture and interfaces for approved requirements.
---

# Requirements And Delivery Contract

## Responsibility

Translate approved intent into traceable, observable, testable requirements and acceptance criteria while preserving unknowns and scope.

## Trigger

Use when the requested outcome is: Translate approved intent into traceable, observable, testable requirements and acceptance criteria while preserving unknowns and scope.

Do not use when:
- Discover whether this is the right customer problem to solve. Route to `problem-framing-and-customer-research`.
- Design the technical architecture and interfaces for approved requirements. Route to `architecture-candidate-reporting`.

## Required Inputs

- Problem and solution evidence, target users, strategy, metrics, risks, and delivery constraints.

Also require source identities, authority, decision owner, scope, and declared unknowns where applicable.

## Procedure

1. Verify approved problem, scope, users, outcomes, constraints, authority, and unresolved decisions.
2. Assign stable requirement IDs and write actor-trigger-condition-observable-response statements.
3. Cover normal, alternate, error, empty, boundary, recovery, permission, and non-functional behavior where applicable.
4. Link acceptance criteria to requirements and evidence; reject implementation-only or subjective criteria.
5. Run completeness, consistency, testability, scope, and unknown-preservation gate.

## Output Contract

Produce:
- requirements specification
- acceptance criteria
- traceability matrix
- unknown and conflict register

Every material claim, score, recommendation, or finding must link to a supplied or authorized source, or be labeled assumption/unknown.

## Hard Gates

- Do not invent product behavior, choose architecture, or mark subjective and unobservable outcomes as acceptance criteria.
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
- `problem-framing-and-customer-research`
- `implementation-planning-and-handoff`
- `risk-preflight-and-safety-governance`

Never perform remote Git, external-system writes, merge, deploy, cloud mutation, participant recruitment/contact, or downstream implementation unless a different explicitly authorized capability owns that action.
