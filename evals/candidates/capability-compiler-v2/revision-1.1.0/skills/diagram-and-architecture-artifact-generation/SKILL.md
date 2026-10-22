---
name: diagram-and-architecture-artifact-generation
description: "Generate traceable architecture or process diagram source from approved evidence without inventing nodes, edges, trust boundaries, or runtime facts. Use when An architecture or process diagram must be drawn from approved facts without inventing nodes or edges; Someone asks for diagram source with a source map and a list of unknown or disputed elements. Do not use for: Discover the actual architecture by inspecting code and runtime evidence first (-> architecture-deepening-discovery); Choose among competing architecture interfaces and recommend one (-> architecture-interface-alternative-evaluation)."
---

# Diagram And Architecture Artifact Generation

## Responsibility

Generate traceable architecture or process diagram source from approved evidence without inventing nodes, edges, trust boundaries, or runtime facts.

## Trigger

Use when the request matches any of:
- An architecture or process diagram must be drawn from approved facts without inventing nodes or edges
- Someone asks for diagram source with a source map and a list of unknown or disputed elements

Do not use when:
- Discover the actual architecture by inspecting code and runtime evidence first. Route to `architecture-deepening-discovery`.
- Choose among competing architecture interfaces and recommend one. Route to `architecture-interface-alternative-evaluation`.

## Required Inputs

- Approved source facts, diagram purpose, notation, audience, and output format.

## Procedure

1. Freeze diagram audience, question, scope, notation, approved source artifacts, versions, and unresolved assumptions.
2. Extract actors, systems, containers or modules, data stores, edges, direction, protocols, trust boundaries, and environments only from cited evidence.
3. Choose the smallest diagram type that answers the declared question and avoid mixing abstraction levels.
4. Generate stable IDs, labels, legend, source mapping, and explicit unknown or disputed elements.
5. Perform a structural source check, prepare an exact host renderer or syntax-validation request, and route factual gaps back to discovery rather than inventing them.

## Domain Guidance

- Persist the diagram source file first, then prepare a single render request for the whole set of outputs; a render is never a substitute for the source.

## Output Contract

Produce:
- diagram source
- host render or syntax-validation request
- node-and-edge source map
- unknown and conflict ledger

Every material fact, boundary, recommendation, finding, test claim, migration step, or risk must cite supplied or authorized evidence or be labeled assumption/unknown.

Deliver each output as the artifact itself (tables, commands, patches, plans, records), not as a description of how it would be produced.

## Coverage

- `diagram-scope`
- `abstraction-level`
- `node-edge-provenance`
- `trust-boundary`
- `host-validation-request`
- `unknowns`

## Hard Gates

- Every node, edge, boundary, protocol, and environment label must trace to approved evidence or be visibly marked unknown; a syntactically valid invented diagram fails.
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

## Status Mapping

- `passed`: output contract and every hard gate are satisfied with current evidence.
- `needs-input`: a requestable source, policy, compatibility fact, or decision is missing. Deliver every supported part first and name the owner for the missing part.
- `blocked`: proceeding would exceed authority, access secret values, mutate production, or cross a prohibited safety boundary.
- `failed`: authorized work ran but a deterministic gate or required output failed.

## Non-Responsibilities

Adjacent capabilities:
- `architecture-candidate-reporting`
- `architecture-deepening-discovery`
- `security-audit-and-threat-modeling`
- `documentation-authoring`
- `architecture-interface-alternative-evaluation`

Never access or emit secret values, mutate production data or provider policy, grant AI action rights, execute remote Git, merge, deploy, release, or perform an adjacent capability. Review, reporting, and audit candidates never repair source.
