---
name: document-and-artifact-governance
description: "Define artifact identities, owners, source of truth, lifecycle state, staleness, retention, and invalidation without authoring their content. Use when A project needs rules for which documents exist, who owns them, which copy is the source of truth and when they go stale; Artifacts are drifting or duplicated and someone must define lifecycle state, retention and invalidation. Do not use for: Write the actual architecture explanation document (-> documentation-authoring); Persist a completed artifact to disk (-> artifact-persistence-and-tool-actions)."
---

# Document And Artifact Governance

## Responsibility

Define artifact identities, owners, source of truth, lifecycle state, staleness, retention, and invalidation without authoring their content.

## Trigger

Use when the request matches any of:
- A project needs rules for which documents exist, who owns them, which copy is the source of truth and when they go stale
- Artifacts are drifting or duplicated and someone must define lifecycle state, retention and invalidation

Do not use when:
- Write the actual architecture explanation document. Route to `documentation-authoring`.
- Persist a completed artifact to disk. Route to `artifact-persistence-and-tool-actions`.

## Required Inputs

- A document or artifact purpose, audience, source evidence, and required fields.

## Procedure

1. Inventory artifact types, consumers, producers, authority, and trust-boundary crossings.
2. Assign stable identity, owner, canonical location, state, and replacement rules.
3. Define required metadata, evidence links, retention, deletion, and access boundary.
4. Define staleness and upstream-change invalidation rules.
5. Publish the governance map and unresolved ownership gaps.

## Domain Guidance

- Default lifecycle states: draft, approved, superseded, stale, retired. A state change needs an owner and a reason; a change to an upstream artifact marks dependents stale until reviewed.
- Default staleness triggers: upstream artifact hash changed, owner change, review date passed, referenced system version changed.
- Define identity (stable id, canonical location), metadata, retention and deletion for each artifact class. This governance method is authored; the cited sources are document templates.

## Output Contract

Produce:
- artifact registry
- ownership matrix
- state-transition policy
- staleness and retention rules

Every material claim, score, recommendation, or finding must link to a supplied or authorized source, or be labeled assumption/unknown.

Deliver each output as the artifact itself (tables, commands, patches, plans, records), not as a description of how it would be produced.

## Hard Gates

- Governance may define where and when artifacts exist but must not invent, approve, or silently rewrite their contents.
- Preserve conflicts, counterevidence, unknowns, source identity, and authority boundaries.
- Return `needs-input` when an identifiable owner can supply a missing requirement or decision.
- Return `blocked` when required authority, evidence, governance, or a safe execution boundary is unavailable.
- Deliver every part the supplied evidence and authority support, label assumptions, and list each missing item with the owner who can supply it; `needs-input` or `blocked` applies to the unsupported part, not to the whole deliverable.

## Forbidden Actions

- remote Git, pull-request mutation, merge, deploy, cloud mutation, or external-system write
- invent facts, evidence, authority, approval, or customer data
- perform adjacent or downstream capability responsibilities
- claim evaluation, approval, release, or completion evidence that has not been produced

## Status Mapping

- `passed`: output contract and every hard gate are satisfied.
- `needs-input`: a requestable source, decision, or governance term is missing. Deliver every supported part first and name the owner for the missing part.
- `blocked`: proceeding would exceed authority, violate governance, or rely on unavailable critical evidence.
- `failed`: supplied inputs were processed but a deterministic gate or required output failed.

## Non-Responsibilities

Adjacent capabilities:
- `documentation-authoring`
- `source-metadata-and-provenance`
- `artifact-persistence-and-tool-actions`

Never perform remote Git, external-system writes, merge, deploy, cloud mutation, participant recruitment/contact, or downstream implementation unless a different explicitly authorized capability owns that action.
