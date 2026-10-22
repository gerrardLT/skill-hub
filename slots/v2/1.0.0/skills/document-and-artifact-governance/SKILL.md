---
name: document-and-artifact-governance
description: Define artifact identities, owners, source of truth, lifecycle state, staleness, retention, and invalidation without authoring their content. Do not use for write the actual architecture explanation document or persist a completed artifact to disk.
---

# Document And Artifact Governance

## Responsibility

Define artifact identities, owners, source of truth, lifecycle state, staleness, retention, and invalidation without authoring their content.

## Trigger

Use when the requested outcome is: Define artifact identities, owners, source of truth, lifecycle state, staleness, retention, and invalidation without authoring their content.

Do not use when:
- Write the actual architecture explanation document. Route to `documentation-authoring`.
- Persist a completed artifact to disk. Route to `artifact-persistence-and-tool-actions`.

## Required Inputs

- A document or artifact purpose, audience, source evidence, and required fields.

Also require source identities, authority, decision owner, scope, and declared unknowns where applicable.

## Procedure

1. Inventory artifact types, consumers, producers, authority, and trust-boundary crossings.
2. Assign stable identity, owner, canonical location, state, and replacement rules.
3. Define required metadata, evidence links, retention, deletion, and access boundary.
4. Define staleness and upstream-change invalidation rules.
5. Publish the governance map and unresolved ownership gaps.

## Output Contract

Produce:
- artifact registry
- ownership matrix
- state-transition policy
- staleness and retention rules

Every material claim, score, recommendation, or finding must link to a supplied or authorized source, or be labeled assumption/unknown.

## Hard Gates

- Governance may define where and when artifacts exist but must not invent, approve, or silently rewrite their contents.
- Preserve conflicts, counterevidence, unknowns, source identity, and authority boundaries.
- Return `needs-input` when an identifiable owner can supply a missing requirement or decision.
- Return `blocked` when required authority, evidence, governance, or a safe execution boundary is unavailable.

## Status Mapping

- `passed`: output contract and every hard gate are satisfied.
- `needs-input`: a requestable source, decision, or governance term is missing.
- `blocked`: proceeding would exceed authority, violate governance, or rely on unavailable critical evidence.
- `failed`: supplied inputs were processed but a deterministic gate or required output failed.

## Non-Responsibilities

Does not approve upstream product decisions, expand authority, or perform remote writes beyond its explicit permission identity.

Adjacent capabilities:
- `documentation-authoring`
- `source-metadata-and-provenance`
- `artifact-persistence-and-tool-actions`

Never perform remote Git, external-system writes, merge, deploy, cloud mutation, participant recruitment/contact, or downstream implementation unless a different explicitly authorized capability owns that action.
