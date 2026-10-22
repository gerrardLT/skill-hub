---
name: research-planning-and-governance
description: "Design a research plan with decision linkage, method, sampling, consent, minimization, retention, external-transfer, and deletion boundaries. Use when A research effort needs its decision link, method, sampling and data-governance terms set before anyone is contacted; Someone asks what consent, retention and transfer terms are needed to run interviews or a survey. Do not use for: Conduct the already approved customer interviews (-> customer-interview-execution); Synthesize the completed qualitative corpus (-> qualitative-evidence-synthesis)."
---

# Research Planning And Governance

## Responsibility

Design a research plan with decision linkage, method, sampling, consent, minimization, retention, external-transfer, and deletion boundaries.

## Trigger

Use when the request matches any of:
- A research effort needs its decision link, method, sampling and data-governance terms set before anyone is contacted
- Someone asks what consent, retention and transfer terms are needed to run interviews or a survey

Do not use when:
- Conduct the already approved customer interviews. Route to `customer-interview-execution`.
- Synthesize the completed qualitative corpus. Route to `qualitative-evidence-synthesis`.

## Required Inputs

- A research question, target population, access constraints, ethical boundary, and timebox.

## Procedure

1. State the decision, research question, prior evidence, unknown, owner, and stopping rule.
2. Select method and sampling logic appropriate to the claim; name bias and representativeness limits.
3. Define authorization, consent, minimization, redaction, recording, retention, access, external-transfer, and deletion policy.
4. Specify protocol, evidence schema, quality checks, analysis plan, and recruitment boundary.
5. Return the plan and blocked governance inputs; do not recruit or collect data.

## Output Contract

Produce:
- research plan
- sampling and method rationale
- data-governance contract
- analysis and stopping plan

Every material claim, score, recommendation, or finding must link to a supplied or authorized source, or be labeled assumption/unknown.

Deliver each output as the artifact itself (tables, commands, patches, plans, records), not as a description of how it would be produced.

## Hard Gates

- No participant contact, collection, recording, external Judge use, or proprietary-data transfer may begin from an incomplete governance contract.
- Preserve conflicts, counterevidence, unknowns, source identity, and authority boundaries.
- Return `needs-input` when an identifiable owner can supply a missing requirement or decision.
- Return `blocked` when required authority, evidence, governance, or a safe execution boundary is unavailable.
- Deliver every part the supplied evidence and authority support, label assumptions, and list each missing item with the owner who can supply it; `needs-input` or `blocked` applies to the unsupported part, not to the whole deliverable.

## Forbidden Actions

- remote Git, pull-request mutation, merge, deploy, cloud mutation, or external-system write
- invent facts, evidence, authority, approval, or customer data
- perform adjacent or downstream capability responsibilities
- claim evaluation, approval, release, or completion evidence that has not been produced

## Data Governance

Before using interviews, customer or proprietary data, recordings, or an external LLM Judge, require explicit authorization, minimization, redaction, retention, external-transfer, access, deletion, and incident boundaries. Missing governance returns `needs-input`; unavailable or prohibited authority returns `blocked`.

## Status Mapping

- `passed`: output contract and every hard gate are satisfied.
- `needs-input`: a requestable source, decision, or governance term is missing. Deliver every supported part first and name the owner for the missing part.
- `blocked`: proceeding would exceed authority, violate governance, or rely on unavailable critical evidence.
- `failed`: supplied inputs were processed but a deterministic gate or required output failed.

## Non-Responsibilities

Adjacent capabilities:
- `customer-interview-execution`
- `data-analysis-validation`
- `qualitative-evidence-synthesis`

Never perform remote Git, external-system writes, merge, deploy, cloud mutation, participant recruitment/contact, or downstream implementation unless a different explicitly authorized capability owns that action.
