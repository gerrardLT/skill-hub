---
name: problem-framing-and-customer-research
description: "Create a solution-free problem frame by classifying supplied customer evidence, facts, assumptions, conflicts, impacts, and gaps. Use when Raw notes, a request or a hypothesis must be reframed as a customer problem before any solution is discussed; Someone asks whether a problem is real, who has it, how painful it is and what evidence is missing. Do not use for: Design experiments for a proposed solution hypothesis (-> solution-hypothesis-and-experiment-design); Synthesize themes across multiple raw interview records (-> qualitative-evidence-synthesis)."
---

# Problem Framing And Customer Research

## Responsibility

Create a solution-free problem frame by classifying supplied customer evidence, facts, assumptions, conflicts, impacts, and gaps.

## Trigger

Use when the request matches any of:
- Raw notes, a request or a hypothesis must be reframed as a customer problem before any solution is discussed
- Someone asks whether a problem is real, who has it, how painful it is and what evidence is missing

Do not use when:
- Design experiments for a proposed solution hypothesis. Route to `solution-hypothesis-and-experiment-design`.
- Synthesize themes across multiple raw interview records. Route to `qualitative-evidence-synthesis`.

## Required Inputs

- A problem hypothesis, target users, prior research, access constraints, and a decision to support.

## Procedure

1. Inventory supplied claims, sources, authority, target users, and stated unknowns.
2. Interrogate the frame with the forcing questions (demand evidence, status quo, specific user, narrowest version) and restate any solution-shaped input as a problem.
3. Classify each material claim as fact, assumption, open question, or conflict.
4. Describe observed problem, context, behavior, workaround, impact, and evidence without solution language.
5. Preserve conflicting accounts and unknowns that change scope, outcome, authority, or safety.
6. Return a solution-free frame or needs-input/blocked status.

## Domain Guidance

- Interrogate the frame with forcing questions: what is the strongest evidence of demand (not interest), what do people do today instead (the status quo), who specifically needs this most, and what is the narrowest version that would matter.
- Problem statement format: who has the problem, what it is, why it hurts, and the evidence (quotes, data) with source ids. It names no feature, mechanism or vendor. When the request is already solution-shaped, restate it as the underlying problem and list the solution as an unvalidated assumption.

## Output Contract

Produce:
- problem frame
- classification register
- conflict register
- critical gap list
- structured problem statement with evidence and source ids

Every material claim, score, recommendation, or finding must link to a supplied or authorized source, or be labeled assumption/unknown.

Deliver each output as the artifact itself (tables, commands, patches, plans, records), not as a description of how it would be produced.

## Hard Gates

- Any proposed feature, mechanism, vendor, architecture, or implied solution in the problem frame is a boundary failure.
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
- `qualitative-evidence-synthesis`
- `solution-hypothesis-and-experiment-design`
- `requirements-and-delivery-contract`

Never perform remote Git, external-system writes, merge, deploy, cloud mutation, participant recruitment/contact, or downstream implementation unless a different explicitly authorized capability owns that action.
