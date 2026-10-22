---
name: customer-interview-execution
description: Prepare and conduct a non-leading, consented interview session and preserve observation separately from interpretation. Do not use for synthesize themes across these completed interview records or recruit or contact customers using their private details.
---

# Customer Interview Execution

## Responsibility

Prepare and conduct a non-leading, consented interview session and preserve observation separately from interpretation.

## Trigger

Use when the requested outcome is: Prepare and conduct a non-leading, consented interview session and preserve observation separately from interpretation.

Do not use when:
- Synthesize themes across these completed interview records. Route to `qualitative-evidence-synthesis`.
- Recruit or contact customers using their private details. Route to `research-planning-and-governance`.

## Required Inputs

- A research objective, participant context, consent boundary, and interview script.

Also require source identities, authority, decision owner, scope, and declared unknowns where applicable.

## Procedure

1. Verify purpose, participant authority, consent, minimization, recording, retention, deletion, and external-transfer boundaries.
2. Write behavior-first questions about past events; remove pitching, hypotheticals, and confirmation cues.
3. Run or guide the session without contacting participants autonomously.
4. Record quotes and observations with source IDs; label interviewer inference separately.
5. Close with consented follow-up and deletion commitments.

## Output Contract

Produce:
- interview guide
- consent and governance record
- observation log
- follow-up register

Every material claim, score, recommendation, or finding must link to a supplied or authorized source, or be labeled assumption/unknown.

## Hard Gates

- Do not recruit, contact, record, retain, or transfer participant data without explicit authorization and governance terms.
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
- `research-planning-and-governance`
- `qualitative-evidence-synthesis`
- `problem-framing-and-customer-research`

Never perform remote Git, external-system writes, merge, deploy, cloud mutation, participant recruitment/contact, or downstream implementation unless a different explicitly authorized capability owns that action.
