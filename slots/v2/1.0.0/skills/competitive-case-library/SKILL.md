---
name: competitive-case-library
description: Build a traceable case library from supplied or authorized competitor evidence for later comparison. Do not use for set up an ongoing competitor alert and response cadence or choose our final market position against these competitors.
---

# Competitive Case Library

## Responsibility

Build a traceable case library from supplied or authorized competitor evidence for later comparison.

## Trigger

Use when the requested outcome is: Build a traceable case library from supplied or authorized competitor evidence for later comparison.

Do not use when:
- Set up an ongoing competitor alert and response cadence. Route to `competitive-response-and-monitoring`.
- Choose our final market position against these competitors. Route to `market-positioning-and-competitive-power`.

## Required Inputs

- A competitive question, case material, historical context, and applicability boundary.

Also require source identities, authority, decision owner, scope, and declared unknowns where applicable.

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

## Hard Gates

- A case without a source, observation date, and fact-versus-inference label cannot enter the library.
- Preserve conflicts, counterevidence, unknowns, source identity, and authority boundaries.
- Return `needs-input` when an identifiable owner can supply a missing requirement or decision.
- Return `blocked` when required authority, evidence, governance, or a safe execution boundary is unavailable.

## Data Governance

Before using interviews, customer or proprietary data, recordings, or an external LLM Judge, require explicit authorization, minimization, redaction, retention, external-transfer, access, deletion, and incident boundaries. Missing governance returns `needs-input`; unavailable or prohibited authority returns `blocked`.

## Status Mapping

- `passed`: output contract and every hard gate are satisfied.
- `needs-input`: a requestable source, decision, or governance term is missing.
- `blocked`: proceeding would exceed authority, violate governance, or rely on unavailable critical evidence.
- `failed`: supplied inputs were processed but a deterministic gate or required output failed.

## Non-Responsibilities

Does not approve upstream product decisions, expand authority, or perform remote writes beyond its explicit permission identity.

Adjacent capabilities:
- `competitive-response-and-monitoring`
- `market-positioning-and-competitive-power`
- `qualitative-evidence-synthesis`

Never perform remote Git, external-system writes, merge, deploy, cloud mutation, participant recruitment/contact, or downstream implementation unless a different explicitly authorized capability owns that action.
