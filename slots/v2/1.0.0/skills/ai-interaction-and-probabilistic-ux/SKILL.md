---
name: ai-interaction-and-probabilistic-ux
description: Design bounded user interaction for AI latency, uncertainty, correction, personalization, escalation, and safe failure without hiding probabilistic behavior. Do not use for choose the model, retrieval stack, memory, and serving architecture or perform the system threat model and autonomous-action safety assessment.
---

# Ai Interaction And Probabilistic Ux

## Responsibility

Design bounded user interaction for AI latency, uncertainty, correction, personalization, escalation, and safe failure without hiding probabilistic behavior.

## Trigger

Use when the requested outcome is: Design bounded user interaction for AI latency, uncertainty, correction, personalization, escalation, and safe failure without hiding probabilistic behavior.

Do not use when:
- Choose the model, retrieval stack, memory, and serving architecture. Route to `ai-model-and-data-architecture`.
- Perform the system threat model and autonomous-action safety assessment. Route to `ai-safety-and-action-governance`.

## Required Inputs

- Probabilistic outputs, user context, interaction latency, correction signals, and accessibility needs.

Also require source or render identity, authorization, target surfaces, supported states, decision owner, and declared unknowns where applicable.

## Procedure

1. Freeze the approved user job, AI role, latency budget, error cost, data boundary, autonomy level, and human escalation owner.
2. Model deterministic, loading, partial, uncertain, conflicting, unsafe, unavailable, and recovery states.
3. Define provenance and uncertainty communication in task language rather than decorative confidence theater.
4. Provide correction, undo, retry, compare, opt-out, feedback, and human-escalation controls proportionate to consequence.
5. Test adversarial misunderstandings, personalization drift, stale memory, and failure recovery; preserve unresolved safety dependencies.

## Output Contract

Produce:
- AI interaction-state model
- uncertainty and provenance contract
- correction and escalation flow
- safe-failure acceptance criteria

Every material design choice, implementation claim, finding, score, capture, or disposition must link to supplied authority or current evidence, or be labeled assumption/unknown.

## UI Coverage

- `latency`
- `uncertainty`
- `provenance`
- `correction`
- `undo`
- `escalation`
- `safe-failure`

## Hard Gates

- Never present generated content, confidence, personalization, or autonomous action as certain, authoritative, or irreversible when the system cannot prove it.
- Preserve product truth, user task, semantic order, authentic content, accessibility, responsive behavior, state coverage, source identity, and authority boundaries where applicable.
- Return `needs-input` when an identifiable owner can supply a missing requirement, asset authority, capture, state, or decision.
- Return `blocked` when required authorization, safe mutation scope, rendered evidence, tooling, or specialist dependency is unavailable.

## Human Design Authority

The Skill may preserve evidence, alternatives, tradeoffs, findings, and a recommendation. Final taste selection, prototype promotion, accepted risk, scope approval, source-repair approval, and release disposition remain explicit human decisions with a named owner.

## Status Mapping

- `passed`: output contract and every hard gate are satisfied with current evidence.
- `needs-input`: a requestable source, state, decision, capture, or authorization term is missing.
- `blocked`: proceeding would exceed authority, mix review with repair, or rely on unavailable critical evidence.
- `failed`: authorized work ran but a deterministic gate or required output failed.

## Non-Responsibilities

Does not approve upstream product decisions, expand authority, or perform remote writes beyond its explicit permission identity.

Adjacent capabilities:
- `interaction-states-forms-and-navigation`
- `ai-model-and-data-architecture`
- `ai-safety-and-action-governance`
- `accessibility-contracts-and-assistive-validation`

Never perform remote Git, external-system writes, merge, deploy, release, or an adjacent capability's work. Review and preflight capabilities never repair product source; evidence-acquisition capabilities never issue design findings.
