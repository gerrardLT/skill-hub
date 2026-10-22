---
name: problem-framing-and-customer-research
description: Create a solution-free problem frame by classifying supplied customer evidence, facts, assumptions, conflicts, impacts, and gaps. Do not use for design experiments for a proposed solution hypothesis or synthesize themes across multiple raw interview records.
---

# Problem Framing And Customer Research

## Responsibility

Create a solution-free problem frame by classifying supplied customer evidence, facts, assumptions, conflicts, impacts, and gaps.

## Trigger

Use when the requested outcome is: Create a solution-free problem frame by classifying supplied customer evidence, facts, assumptions, conflicts, impacts, and gaps.

Do not use when:
- Design experiments for a proposed solution hypothesis. Route to `solution-hypothesis-and-experiment-design`.
- Synthesize themes across multiple raw interview records. Route to `qualitative-evidence-synthesis`.

## Required Inputs

- A problem hypothesis, target users, prior research, access constraints, and a decision to support.

Also require source identities, authority, decision owner, scope, and declared unknowns where applicable.

## Procedure

1. Inventory supplied claims, sources, authority, target users, and stated unknowns.
2. Classify each material claim as fact, assumption, open question, or conflict.
3. Describe observed problem, context, behavior, workaround, impact, and evidence without solution language.
4. Preserve conflicting accounts and unknowns that change scope, outcome, authority, or safety.
5. Return a solution-free frame or needs-input/blocked status.

## Output Contract

Produce:
- problem frame
- classification register
- conflict register
- critical gap list

Every material claim, score, recommendation, or finding must link to a supplied or authorized source, or be labeled assumption/unknown.

## Hard Gates

- Any proposed feature, mechanism, vendor, architecture, or implied solution in the problem frame is a boundary failure.
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
- `qualitative-evidence-synthesis`
- `solution-hypothesis-and-experiment-design`
- `requirements-and-delivery-contract`

Never perform remote Git, external-system writes, merge, deploy, cloud mutation, participant recruitment/contact, or downstream implementation unless a different explicitly authorized capability owns that action.
