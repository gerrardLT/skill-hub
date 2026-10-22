---
name: facilitation-and-collaboration-protocols
description: Design a bounded collaborative session that elicits evidence, preserves dissent, records decisions, and assigns follow-up authority. Do not use for make the disputed product decision for the group or interview customers one-on-one about past behavior.
---

# Facilitation And Collaboration Protocols

## Responsibility

Design a bounded collaborative session that elicits evidence, preserves dissent, records decisions, and assigns follow-up authority.

## Trigger

Use when the requested outcome is: Design a bounded collaborative session that elicits evidence, preserves dissent, records decisions, and assigns follow-up authority.

Do not use when:
- Make the disputed product decision for the group. Route to `plan-review-decision-synthesis`.
- Interview customers one-on-one about past behavior. Route to `customer-interview-execution`.

## Required Inputs

- A multi-role task, incomplete context, stakeholder set, and decision boundary.

Also require source identities, authority, decision owner, scope, and declared unknowns where applicable.

## Procedure

1. Define the session question, participants, roles, authority, pre-reads, and data boundary.
2. Select activities that elicit independent evidence before convergence.
3. Timebox divergence, synthesis, decision, dissent, and follow-up.
4. Record decision owner, rationale, objections, unknowns, and expiry conditions.
5. Produce actions and unresolved items without fabricating consensus.

## Output Contract

Produce:
- facilitation plan
- role and authority map
- decision log template
- follow-up register

Every material claim, score, recommendation, or finding must link to a supplied or authorized source, or be labeled assumption/unknown.

## Hard Gates

- A facilitator may structure and record the decision but must not manufacture consensus or decide for the named owner.
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
- `customer-interview-execution`
- `plan-review-decision-synthesis`
- `document-and-artifact-governance`

Never perform remote Git, external-system writes, merge, deploy, cloud mutation, participant recruitment/contact, or downstream implementation unless a different explicitly authorized capability owns that action.
