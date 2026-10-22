---
name: plan-review-decision-synthesis
description: Synthesize independent plan-review findings, preserve dissent, classify decision types, and surface human approval points without rerunning reviews. Do not use for perform the independent design review that is missing or approve and edit the plan using the synthesized recommendations.
---

# Plan Review Decision Synthesis

## Responsibility

Synthesize independent plan-review findings, preserve dissent, classify decision types, and surface human approval points without rerunning reviews.

## Trigger

Use when the requested outcome is: Synthesize independent plan-review findings, preserve dissent, classify decision types, and surface human approval points without rerunning reviews.

Do not use when:
- Perform the independent design review that is missing. Route to `design-plan-review`.
- Approve and edit the plan using the synthesized recommendations. Route to `implementation-planning-and-handoff`.

## Required Inputs

- Independent review findings, plan version, decision policy, authority, and unresolved questions.

Also require source identities, authority, decision owner, scope, and declared unknowns where applicable.

## Procedure

1. Verify review identities, frozen plan version, citations, applicability, and independence.
2. Deduplicate findings by underlying decision without erasing distinct rationale.
3. Classify evidence defect, reversible choice, taste decision, one-way door, conflict, and non-applicable item.
4. Preserve agreement, dissent, dependencies, and proposed amendments.
5. Return an audit trail and explicit human decisions; do not approve or write the plan.

## Output Contract

Produce:
- review decision matrix
- dissent register
- proposed amendments
- human approval queue

Every material claim, score, recommendation, or finding must link to a supplied or authorized source, or be labeled assumption/unknown.

## Hard Gates

- Synthesis cannot manufacture reviewer consensus, downgrade a blocking dissent, or convert recommendations into approved scope.
- Preserve conflicts, counterevidence, unknowns, source identity, and authority boundaries.
- Return `needs-input` when an identifiable owner can supply a missing requirement or decision.
- Return `blocked` when required authority, evidence, governance, or a safe execution boundary is unavailable.

## Human Decision Authority

Output evidence, options, tradeoffs, unknowns, and a recommendation. GO/PIVOT/KILL, scope approval, strategic selection, taste choices, and build approval remain human decisions; record the owner and decision separately.

## Status Mapping

- `passed`: output contract and every hard gate are satisfied.
- `needs-input`: a requestable source, decision, or governance term is missing.
- `blocked`: proceeding would exceed authority, violate governance, or rely on unavailable critical evidence.
- `failed`: supplied inputs were processed but a deterministic gate or required output failed.

## Non-Responsibilities

Does not absorb unrelated lifecycle responsibilities or expand provider, workspace, or remote-write authority implicitly.

Adjacent capabilities:
- `independent-plan-review`
- `executive-plan-review`
- `design-plan-review`
- `developer-experience-plan-review`

Never perform remote Git, external-system writes, merge, deploy, cloud mutation, participant recruitment/contact, or downstream implementation unless a different explicitly authorized capability owns that action.
