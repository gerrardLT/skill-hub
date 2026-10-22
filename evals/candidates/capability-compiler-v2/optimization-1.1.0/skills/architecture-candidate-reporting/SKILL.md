---
name: architecture-candidate-reporting
description: "Present already-developed architecture candidates as traceable comparable views, rankings, diagrams, and a bounded recommendation without inventing options or implementing one. Use when Several architecture candidates already exist and must be compared on the same criteria with a ranking and a bounded recommendation; A decision maker needs candidate cards, a sensitivity view and diagrams before choosing an architecture. Do not use for: Generate independent interface alternatives for this module before any candidates exist (-> architecture-interface-alternative-evaluation); Generate traceable diagrams from the approved architecture facts (-> diagram-and-architecture-artifact-generation)."
---

# Architecture Candidate Reporting

## Responsibility

Present already-developed architecture candidates as traceable comparable views, rankings, diagrams, and a bounded recommendation without inventing options or implementing one.

## Trigger

Use when the request matches any of:
- Several architecture candidates already exist and must be compared on the same criteria with a ranking and a bounded recommendation
- A decision maker needs candidate cards, a sensitivity view and diagrams before choosing an architecture

Do not use when:
- Generate independent interface alternatives for this module before any candidates exist. Route to `architecture-interface-alternative-evaluation`.
- Generate traceable diagrams from the approved architecture facts. Route to `diagram-and-architecture-artifact-generation`.

## Required Inputs

- Already discovered architecture candidates with code evidence.

## Procedure

1. Freeze candidate identities, common requirements, evidence, constraints, decision criteria, owners, and unresolved disagreements.
2. Normalize each candidate into context, boundary, interfaces, dependencies, data flow, failure behavior, security, operability, migration, cost, and evidence quality.
3. Create comparable tables, cards, and supplied-diagram references without erasing candidate-specific assumptions.
4. Compute weighted totals with the arithmetic shown and rank; mark criteria without evidence instead of scoring them.
5. Apply declared criteria and sensitivity; separate fact, estimate, inference, and human preference.
6. Recommend or abstain, preserving dissent, unknowns, and the named human architecture decision.

## Domain Guidance

- When criteria and weights are supplied, compute the weighted totals and rank the candidates, showing the arithmetic and a sensitivity check (how the ranking changes if the top weight moves). Withhold a ranking only for criteria that lack evidence, and say which.
- Give a conditional recommendation stating what would change it; abstain only when evidence gaps make any ranking misleading.
- Choose the diagram pattern per candidate type: a dependency or call-flow graph for coupling, a layered view for boundaries, a sequence view for failure behavior. Vary patterns rather than one template for all candidates.

## Output Contract

Produce:
- architecture candidate cards
- comparison and sensitivity matrix
- traceable diagram index
- bounded recommendation and dissent ledger
- weighted ranking with arithmetic and sensitivity

Every material fact, boundary, recommendation, finding, test claim, migration step, or risk must cite supplied or authorized evidence or be labeled assumption/unknown.

Deliver each output as the artifact itself (tables, commands, patches, plans, records), not as a description of how it would be produced.

## Coverage

- `candidate-identity`
- `common-criteria`
- `evidence-quality`
- `sensitivity`
- `dissent`
- `human-decision`

## Hard Gates

- Candidates may be ranked only against the same declared criteria and evidence basis; missing evidence, human preference, and uncertainty cannot be converted into fabricated scores.
- Review, reporting, contract, and audit candidates never imply implementation, live policy change, production mutation, or risk acceptance.
- Preserve trust boundaries, authorization, data and secret governance, compatibility, migration, rollback or containment, source identity, counterevidence, and residual risk where applicable.
- Return `needs-input` when a named owner can supply a missing fact, policy, evidence, or approval.
- Return `blocked` when safe analysis or mutation would require unavailable authority, secret values, prohibited tests, remote writes, or unresolved high-impact risk.
- Deliver every part the supplied evidence and authority support, label assumptions, and list each missing item with the owner who can supply it; `needs-input` or `blocked` applies to the unsupported part, not to the whole deliverable.

## Forbidden Actions

- request, read, print, persist, hash, or transmit secret values
- remote Git, merge, deploy, release, provider-policy mutation, production-data mutation, or AI action-right activation
- invent architecture facts, data rights, authorization, evidence, approval, migration safety, or risk acceptance
- combine independent review or audit with source remediation
- claim evaluation, approval, release, or completion evidence that has not been produced

## Human Architecture and Risk Authority

The Skill may produce evidence, alternatives, tradeoffs, findings, and a recommendation. Architecture selection, autonomy expansion, risk acceptance, policy approval, migration approval, remediation authorization, and release decisions remain explicit human decisions with a named owner.

## Status Mapping

- `passed`: output contract and every hard gate are satisfied with current evidence.
- `needs-input`: a requestable source, policy, compatibility fact, or decision is missing. Deliver every supported part first and name the owner for the missing part.
- `blocked`: proceeding would exceed authority, access secret values, mutate production, or cross a prohibited safety boundary.
- `failed`: authorized work ran but a deterministic gate or required output failed.

## Non-Responsibilities

Adjacent capabilities:
- `architecture-interface-alternative-evaluation`
- `diagram-and-architecture-artifact-generation`
- `architecture-deep-module-design`
- `implementation-planning-and-handoff`

Never access or emit secret values, mutate production data or provider policy, grant AI action rights, execute remote Git, merge, deploy, release, or perform an adjacent capability. Review, reporting, and audit candidates never repair source.
