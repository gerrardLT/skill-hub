---
name: competitive-response-and-monitoring
description: "Define bounded competitor signals, thresholds, and response options without auto-executing strategy changes. Use when Competitor moves need watch signals, thresholds and pre-agreed response options rather than ad hoc reactions; Someone asks when a competitor release should trigger an investigation or a strategy decision. Do not use for: Build a one-time repository of historical competitor cases (-> competitive-case-library); Write the approved launch response copy and assets (-> documentation-authoring)."
---

# Competitive Response And Monitoring

## Responsibility

Define bounded competitor signals, thresholds, and response options without auto-executing strategy changes.

## Trigger

Use when the request matches any of:
- Competitor moves need watch signals, thresholds and pre-agreed response options rather than ad hoc reactions
- Someone asks when a competitor release should trigger an investigation or a strategy decision

Do not use when:
- Build a one-time repository of historical competitor cases. Route to `competitive-case-library`.
- Write the approved launch response copy and assets. Route to `documentation-authoring`.

## Required Inputs

- Competitor releases, market signals, comparable products, and monitoring evidence.

## Procedure

1. Name the competitive assumption and signals that could change it.
2. Define legal, ethical, source, cadence, owner, and staleness boundaries.
3. Separate noise, watch, investigate, and decision thresholds.
4. Draft no-response, reversible probe, and strategic-response options with evidence needs.
5. Escalate threshold crossings to human strategy owners.

## Domain Guidance

- Monitor comparables as well as direct competitors: comparables tackle a similar problem in a different market and show patterns that will reach yours.
- Response options include no response, a reversible probe, a strategic response, and adopting a proven industry pattern when it is better than inventing a new one.

## Output Contract

Produce:
- monitoring contract
- signal register
- response option matrix
- escalation record

Every material claim, score, recommendation, or finding must link to a supplied or authorized source, or be labeled assumption/unknown.

Deliver each output as the artifact itself (tables, commands, patches, plans, records), not as a description of how it would be produced.

## Hard Gates

- Monitoring may recommend options but must not scrape unauthorized sources or auto-change product, price, or messaging.
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

## Human Decision Authority

Output evidence, options, tradeoffs, unknowns, and a recommendation. GO/PIVOT/KILL, scope approval, strategic selection, taste choices, and build approval remain human decisions; record the owner and decision separately.

## Status Mapping

- `passed`: output contract and every hard gate are satisfied.
- `needs-input`: a requestable source, decision, or governance term is missing. Deliver every supported part first and name the owner for the missing part.
- `blocked`: proceeding would exceed authority, violate governance, or rely on unavailable critical evidence.
- `failed`: supplied inputs were processed but a deterministic gate or required output failed.

## Non-Responsibilities

Adjacent capabilities:
- `competitive-case-library`
- `strategic-choice-and-differentiation`
- `results-analysis-and-decision-readout`
- `documentation-authoring`

Never perform remote Git, external-system writes, merge, deploy, cloud mutation, participant recruitment/contact, or downstream implementation unless a different explicitly authorized capability owns that action.
