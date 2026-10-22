---
name: ai-interaction-and-probabilistic-ux
description: "Design bounded user interaction for AI latency, uncertainty, correction, personalization, escalation, and safe failure without hiding probabilistic behavior. Use when A feature shows generated or probabilistic output and needs loading, uncertainty, correction and failure states designed; Someone asks how users should correct, undo, retry or escalate when an AI result is wrong. Do not use for: Choose the model, retrieval stack, memory, and serving architecture (-> ai-model-and-data-architecture); Perform the system threat model and autonomous-action safety assessment (-> ai-safety-and-action-governance)."
---

# AI Interaction And Probabilistic UX

## Responsibility

Design bounded user interaction for AI latency, uncertainty, correction, personalization, escalation, and safe failure without hiding probabilistic behavior.

## Trigger

Use when the request matches any of:
- A feature shows generated or probabilistic output and needs loading, uncertainty, correction and failure states designed
- Someone asks how users should correct, undo, retry or escalate when an AI result is wrong

Do not use when:
- Choose the model, retrieval stack, memory, and serving architecture. Route to `ai-model-and-data-architecture`.
- Perform the system threat model and autonomous-action safety assessment. Route to `ai-safety-and-action-governance`.

## Required Inputs

- Probabilistic outputs, user context, interaction latency, correction signals, and accessibility needs.

## Procedure

1. Freeze the approved user job, AI role, latency budget, error cost, data boundary, autonomy level, and human escalation owner.
2. Model deterministic, loading, partial, uncertain, conflicting, unsafe, unavailable, and recovery states.
3. Define provenance and uncertainty communication in task language rather than decorative confidence theater.
4. Provide correction, undo, retry, compare, opt-out, feedback, and human-escalation controls proportionate to consequence.
5. Test adversarial misunderstandings, personalization drift, stale memory, and failure recovery; preserve unresolved safety dependencies.

## Domain Guidance

- Pattern per state. Latency: streamed partial output or a skeleton with an expected wait and a cancel control. Uncertainty: task-language wording of what is known and unknown, never a decorative confidence percentage. Provenance: inline citations or source links the user can open. Correction: edit in place, undo, regenerate with a changed instruction. Failure: a plain message, the retry path and a human escalation route.
- Model the states deterministic, loading, partial, uncertain, conflicting, unsafe, unavailable and recovered, and give each its visible UI, controls and exit.
- Discriminator: owns how uncertain AI output is shown to and corrected by users; it does not choose models or autonomy levels.

## Output Contract

Produce:
- AI interaction-state model
- uncertainty and provenance contract
- correction and escalation flow
- safe-failure acceptance criteria

Every material design choice, implementation claim, finding, score, capture, or disposition must link to supplied authority or current evidence, or be labeled assumption/unknown.

Deliver each output as the artifact itself (tables, commands, patches, plans, records), not as a description of how it would be produced.

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
- Review, evidence acquisition, preflight, and preservation audit never imply source remediation or release authority.
- Preserve product truth, user task, semantic order, authentic content, accessibility, responsive behavior, state coverage, source identity, and authority boundaries where applicable.
- Return `needs-input` when an identifiable owner can supply a missing requirement, asset authority, capture, state, or decision.
- Return `blocked` when required authorization, safe mutation scope, rendered evidence, tooling, or specialist dependency is unavailable.
- Deliver every part the supplied evidence and authority support, label assumptions, and list each missing item with the owner who can supply it; `needs-input` or `blocked` applies to the unsupported part, not to the whole deliverable.

## Forbidden Actions

- remote Git, merge, deploy, release, cloud mutation, or external-system write
- invent product facts, brand authority, copy claims, customer data, assets, evidence, or approval
- perform an adjacent capability or combine independent review with source repair
- treat static inspection, stale capture, or model self-report as current rendered evidence
- claim evaluation, approval, release, or completion evidence that has not been produced

## Human Design Authority

The Skill may preserve evidence, alternatives, tradeoffs, findings, and a recommendation. Final taste selection, prototype promotion, accepted risk, scope approval, source-repair approval, and release disposition remain explicit human decisions with a named owner.

## Status Mapping

- `passed`: output contract and every hard gate are satisfied with current evidence.
- `needs-input`: a requestable source, state, decision, capture, or authorization term is missing. Deliver every supported part first and name the owner for the missing part.
- `blocked`: proceeding would exceed authority, mix review with repair, or rely on unavailable critical evidence.
- `failed`: authorized work ran but a deterministic gate or required output failed.

## Non-Responsibilities

Adjacent capabilities:
- `interaction-states-forms-and-navigation`
- `ai-model-and-data-architecture`
- `ai-safety-and-action-governance`
- `accessibility-contracts-and-assistive-validation`

Never perform remote Git, external-system writes, merge, deploy, release, or an adjacent capability's work. Review and preflight capabilities never repair product source; evidence-acquisition capabilities never issue design findings.
