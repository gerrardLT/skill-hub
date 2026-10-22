---
name: competitive-case-library
description: "Build a traceable case library from supplied or authorized competitor evidence for later comparison. Use when Dated competitor or comparable-company moves need to be recorded as reusable, sourced cases; Someone asks for a library of what rivals did, in what context and with what observed outcome. Do not use for: Set up an ongoing competitor alert and response cadence (-> competitive-response-and-monitoring); Choose our final market position against these competitors (-> market-positioning-and-competitive-power); Code customer interview or research notes into themes (-> qualitative-evidence-synthesis)."
---

# Competitive Case Library

## Responsibility

Build a traceable case library from supplied or authorized competitor evidence for later comparison.

## Trigger

Use when the request matches any of:
- Dated competitor or comparable-company moves need to be recorded as reusable, sourced cases
- Someone asks for a library of what rivals did, in what context and with what observed outcome

Do not use when:
- Set up an ongoing competitor alert and response cadence. Route to `competitive-response-and-monitoring`.
- Choose our final market position against these competitors. Route to `market-positioning-and-competitive-power`.
- Code customer interview or research notes into themes. Route to `qualitative-evidence-synthesis`.

## Required Inputs

- A competitive question, case material, historical context, and applicability boundary.

## Procedure

1. Define inclusion criteria, time window, and source authority.
2. Record each case as actor, context, move, observed outcome, source, date, and confidence.
3. Normalize comparable dimensions without erasing source-specific context.
4. Separate observed outcomes from causal claims and analyst inference.
5. Index gaps, stale cases, and reusable comparison tags.

## Output Contract

Produce:
- competitive case records
- evidence-quality register
- case taxonomy
- staleness queue

Every material claim, score, recommendation, or finding must link to a supplied or authorized source, or be labeled assumption/unknown.

Deliver each output as the artifact itself (tables, commands, patches, plans, records), not as a description of how it would be produced.

## Hard Gates

- A case without a source, observation date, and fact-versus-inference label cannot enter the library.
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
- `competitive-response-and-monitoring`
- `market-positioning-and-competitive-power`
- `qualitative-evidence-synthesis`

Never perform remote Git, external-system writes, merge, deploy, cloud mutation, participant recruitment/contact, or downstream implementation unless a different explicitly authorized capability owns that action.
