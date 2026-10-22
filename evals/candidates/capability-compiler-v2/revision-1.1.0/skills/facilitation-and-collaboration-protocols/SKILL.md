---
name: facilitation-and-collaboration-protocols
description: "Design a bounded collaborative session that elicits evidence, preserves dissent, records decisions, and assigns follow-up authority. Use when A group needs a structured session to surface evidence, disagreement and decisions, and someone must design how it runs; An AI-led or AI-assisted workshop needs turn-taking rules, pacing and a decision log. Do not use for: Make the disputed product decision for the group (-> plan-review-decision-synthesis); Interview customers one-on-one about past behavior (-> customer-interview-execution)."
---

# Facilitation And Collaboration Protocols

## Responsibility

Design a bounded collaborative session that elicits evidence, preserves dissent, records decisions, and assigns follow-up authority.

## Trigger

Use when the request matches any of:
- A group needs a structured session to surface evidence, disagreement and decisions, and someone must design how it runs
- An AI-led or AI-assisted workshop needs turn-taking rules, pacing and a decision log

Do not use when:
- Make the disputed product decision for the group. Route to `plan-review-decision-synthesis`.
- Interview customers one-on-one about past behavior. Route to `customer-interview-execution`.

## Required Inputs

- A multi-role task, incomplete context, stakeholder set, and decision boundary.

## Procedure

1. Define the session question, participants, roles, authority, pre-reads, and data boundary.
2. Select activities that elicit independent evidence before convergence.
3. Timebox divergence, synthesis, decision, dissent, and follow-up.
4. Record decision owner, rationale, objections, unknowns, and expiry conditions.
5. Produce actions and unresolved items without fabricating consensus.

## Domain Guidance

- Default protocol for AI-facilitated sessions: open with a heads-up and an entry mode (guided, context dump, best guess); ask one question per turn in plain language; show progress labels such as Context 3/8; handle interruptions with pause and resume; offer numbered recommendations at decision points.
- Collect independent input before convergence, then timebox divergence, synthesis and decision; record dissent and the named decision owner.

## Output Contract

Produce:
- facilitation plan
- role and authority map
- decision log template
- follow-up register
- session script with entry mode, question sequence and progress labels

Every material claim, score, recommendation, or finding must link to a supplied or authorized source, or be labeled assumption/unknown.

Deliver each output as the artifact itself (tables, commands, patches, plans, records), not as a description of how it would be produced.

## Hard Gates

- A facilitator may structure and record the decision but must not manufacture consensus or decide for the named owner.
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
- `customer-interview-execution`
- `plan-review-decision-synthesis`
- `document-and-artifact-governance`

Never perform remote Git, external-system writes, merge, deploy, cloud mutation, participant recruitment/contact, or downstream implementation unless a different explicitly authorized capability owns that action.
