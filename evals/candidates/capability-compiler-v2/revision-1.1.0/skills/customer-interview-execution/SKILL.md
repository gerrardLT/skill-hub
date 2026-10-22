---
name: customer-interview-execution
description: "Prepare and conduct a non-leading, consented interview session and preserve observation separately from interpretation. Use when An interview script or session needs to be non-leading, consented and recorded without mixing observation and interpretation; Someone asks for behavior-first interview questions and a note template for customer conversations. Do not use for: Synthesize themes across these completed interview records (-> qualitative-evidence-synthesis); Recruit or contact customers using their private details (-> research-planning-and-governance)."
---

# Customer Interview Execution

## Responsibility

Prepare and conduct a non-leading, consented interview session and preserve observation separately from interpretation.

## Trigger

Use when the request matches any of:
- An interview script or session needs to be non-leading, consented and recorded without mixing observation and interpretation
- Someone asks for behavior-first interview questions and a note template for customer conversations

Do not use when:
- Synthesize themes across these completed interview records. Route to `qualitative-evidence-synthesis`.
- Recruit or contact customers using their private details. Route to `research-planning-and-governance`.

## Required Inputs

- A research objective, participant context, consent boundary, and interview script.

## Procedure

1. Verify purpose, participant authority, consent, minimization, recording, retention, deletion, and external-transfer boundaries.
2. Write behavior-first questions about past events; remove pitching, hypotheticals, and confirmation cues.
3. Run or guide the session without contacting participants autonomously.
4. Record quotes and observations with source IDs; label interviewer inference separately.
5. Close with consented follow-up and deletion commitments.

## Domain Guidance

- Restate the consent boundary exactly as the participant and owner gave it and do not invent extra terms. When a request goes past that boundary (external or commercial use, quoting in a roadmap, sharing beyond the team), deliver the part inside consent, propose asking for separate explicit consent for the wider use, and name the decision owner for any roadmap or status claim. Never block a follow-up the participant agreed to.
- Probes: 'tell me more about that', a gentle repeated 'why' (two or three times), 'can you give me a specific example', 'what happened next'.
- Observation log fields: participant id, date, key jobs, current solution, biggest pain, desired outcome, willingness to pay, direct quotes with source ids, and interviewer inference labelled separately.
- Record gaps in the evidence (for example a lost or inaudible segment) as follow-up: say what was lost and plan to re-collect it.

## Output Contract

Produce:
- interview guide
- consent and governance record
- observation log
- follow-up register
- probe list and observation-log template

Every material claim, score, recommendation, or finding must link to a supplied or authorized source, or be labeled assumption/unknown.

Deliver each output as the artifact itself (tables, commands, patches, plans, records), not as a description of how it would be produced.

## Hard Gates

- Do not recruit, contact, record, retain, or transfer participant data without explicit authorization and governance terms.
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
- `research-planning-and-governance`
- `qualitative-evidence-synthesis`
- `problem-framing-and-customer-research`

Never perform remote Git, external-system writes, merge, deploy, cloud mutation, participant recruitment/contact, or downstream implementation unless a different explicitly authorized capability owns that action.
