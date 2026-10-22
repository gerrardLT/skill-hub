---
name: competitive-response-and-monitoring
description: Define bounded competitor signals, thresholds, and response options without auto-executing strategy changes. Do not use for build a one-time repository of historical competitor cases or write the approved launch response copy and assets.
---

# Competitive Response And Monitoring

## Responsibility

Define bounded competitor signals, thresholds, and response options without auto-executing strategy changes.

## Trigger

Use when the requested outcome is: Define bounded competitor signals, thresholds, and response options without auto-executing strategy changes.

Do not use when:
- Build a one-time repository of historical competitor cases. Route to `competitive-case-library`.
- Write the approved launch response copy and assets. Route to `documentation-authoring`.

## Required Inputs

- Competitor releases, market signals, comparable products, and monitoring evidence.

Also require source identities, authority, decision owner, scope, and declared unknowns where applicable.

## Procedure

1. Name the competitive assumption and signals that could change it.
2. Define legal, ethical, source, cadence, owner, and staleness boundaries.
3. Separate noise, watch, investigate, and decision thresholds.
4. Draft no-response, reversible probe, and strategic-response options with evidence needs.
5. Escalate threshold crossings to human strategy owners.

## Output Contract

Produce:
- monitoring contract
- signal register
- response option matrix
- escalation record

Every material claim, score, recommendation, or finding must link to a supplied or authorized source, or be labeled assumption/unknown.

## Hard Gates

- Monitoring may recommend options but must not scrape unauthorized sources or auto-change product, price, or messaging.
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
- `competitive-case-library`
- `strategic-choice-and-differentiation`
- `results-analysis-and-decision-readout`

Never perform remote Git, external-system writes, merge, deploy, cloud mutation, participant recruitment/contact, or downstream implementation unless a different explicitly authorized capability owns that action.
