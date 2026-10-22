---
name: architecture-candidate-reporting
description: Present already-developed architecture candidates as traceable comparable views, rankings, diagrams, and a bounded recommendation without inventing options or implementing one. Do not use for generate independent interface alternatives for this module before any candidates exist or generate traceable diagrams from the approved architecture facts.
---

# Architecture Candidate Reporting

## Responsibility

Present already-developed architecture candidates as traceable comparable views, rankings, diagrams, and a bounded recommendation without inventing options or implementing one.

## Trigger

Use when the requested outcome is: Present already-developed architecture candidates as traceable comparable views, rankings, diagrams, and a bounded recommendation without inventing options or implementing one.

Do not use when:
- Generate independent interface alternatives for this module before any candidates exist. Route to `architecture-interface-alternative-evaluation`.
- Generate traceable diagrams from the approved architecture facts. Route to `diagram-and-architecture-artifact-generation`.

## Required Inputs

- Already discovered architecture candidates with code evidence.

Also require target identity, authorization, trust boundaries, data classes, decision owner, compatibility window, and declared unknowns where applicable.

## Procedure

1. Freeze candidate identities, common requirements, evidence, constraints, decision criteria, owners, and unresolved disagreements.
2. Normalize each candidate into context, boundary, interfaces, dependencies, data flow, failure behavior, security, operability, migration, cost, and evidence quality.
3. Create comparable tables, cards, and supplied-diagram references without erasing candidate-specific assumptions.
4. Apply declared criteria and sensitivity; separate fact, estimate, inference, and human preference.
5. Recommend or abstain, preserving dissent, unknowns, and the named human architecture decision.

## Output Contract

Produce:
- architecture candidate cards
- comparison and sensitivity matrix
- traceable diagram index
- bounded recommendation and dissent ledger

Every material fact, boundary, recommendation, finding, test claim, migration step, or risk must cite supplied or authorized evidence or be labeled assumption/unknown.

## Coverage

- `candidate-identity`
- `common-criteria`
- `evidence-quality`
- `sensitivity`
- `dissent`
- `human-decision`

## Hard Gates

- Candidates may be ranked only against the same declared criteria and evidence basis; missing evidence, human preference, and uncertainty cannot be converted into fabricated scores.
- Preserve trust boundaries, authorization, data and secret governance, compatibility, migration, rollback or containment, source identity, counterevidence, and residual risk where applicable.
- Return `needs-input` when a named owner can supply a missing fact, policy, evidence, or approval.
- Return `blocked` when safe analysis or mutation would require unavailable authority, secret values, prohibited tests, remote writes, or unresolved high-impact risk.

## Human Architecture and Risk Authority

The Skill may produce evidence, alternatives, tradeoffs, findings, and a recommendation. Architecture selection, autonomy expansion, risk acceptance, policy approval, migration approval, remediation authorization, and release decisions remain explicit human decisions with a named owner.

## Status Mapping

- `passed`: output contract and every hard gate are satisfied with current evidence.
- `needs-input`: a requestable source, policy, compatibility fact, or decision is missing.
- `blocked`: proceeding would exceed authority, access secret values, mutate production, or cross a prohibited safety boundary.
- `failed`: authorized work ran but a deterministic gate or required output failed.

## Non-Responsibilities

Does not approve upstream product decisions, expand authority, or perform remote writes beyond its explicit permission identity.

Adjacent capabilities:
- `architecture-interface-alternative-evaluation`
- `diagram-and-architecture-artifact-generation`
- `architecture-deep-module-design`
- `implementation-planning-and-handoff`

Never access or emit secret values, mutate production data or provider policy, grant AI action rights, execute remote Git, merge, deploy, release, or perform an adjacent capability. Review, reporting, and audit candidates never repair source.
