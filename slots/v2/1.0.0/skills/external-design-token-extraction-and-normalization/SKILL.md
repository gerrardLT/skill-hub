---
name: external-design-token-extraction-and-normalization
description: Extract observable design primitives from supplied authorized external captures or files, normalize them with provenance and confidence, and stop before project token writes. Do not use for persist approved semantic tokens and components into this project's design system or copy the external product's layout, brand, assets, or interaction wholesale.
---

# External Design Token Extraction And Normalization

## Responsibility

Extract observable design primitives from supplied authorized external captures or files, normalize them with provenance and confidence, and stop before project token writes.

## Trigger

Use when the requested outcome is: Extract observable design primitives from supplied authorized external captures or files, normalize them with provenance and confidence, and stop before project token writes.

Do not use when:
- Persist approved semantic tokens and components into this project's design system. Route to `design-system-foundation-and-token-extraction`.
- Copy the external product's layout, brand, assets, or interaction wholesale. Route to `design-context-and-direction-contract`.

## Required Inputs

- An authorized public reference, extraction runtime, and requested analysis mode.

Also require source or render identity, authorization, target surfaces, supported states, decision owner, and declared unknowns where applicable.

## Procedure

1. Verify source authorization, supplied capture or file identity, scope, timestamp, terms, and prohibited assets or personal data.
2. Read only supplied authorized captures or files; do not browse, fetch, bypass access controls, or perform external writes.
3. Record exact source, selector or artifact location, viewport, observed value, confidence, and state for every primitive.
4. Cluster raw values and propose semantic roles while preserving contradictions, one-offs, responsive variants, and unknown intent.
5. Emit a normalization report and candidate mapping only; require separate human approval and design-system capability for project writes.

## Output Contract

Produce:
- authorized external primitive inventory
- provenance and confidence ledger
- normalized candidate token map
- unknown and conflict register

Every material design choice, implementation claim, finding, score, capture, or disposition must link to supplied authority or current evidence, or be labeled assumption/unknown.

## UI Coverage

- `authorization`
- `external-read`
- `primitive-extraction`
- `normalization`
- `provenance`
- `no-project-write`

## Hard Gates

- Observed external values are evidence, not project authority: no project token, copied asset, or design decision may be written or approved by this capability.
- Preserve product truth, user task, semantic order, authentic content, accessibility, responsive behavior, state coverage, source identity, and authority boundaries where applicable.
- Return `needs-input` when an identifiable owner can supply a missing requirement, asset authority, capture, state, or decision.
- Return `blocked` when required authorization, safe mutation scope, rendered evidence, tooling, or specialist dependency is unavailable.

## Status Mapping

- `passed`: output contract and every hard gate are satisfied with current evidence.
- `needs-input`: a requestable source, state, decision, capture, or authorization term is missing.
- `blocked`: proceeding would exceed authority, mix review with repair, or rely on unavailable critical evidence.
- `failed`: authorized work ran but a deterministic gate or required output failed.

## Non-Responsibilities

Does not approve upstream product decisions, expand authority, or perform remote writes beyond its explicit permission identity.

Adjacent capabilities:
- `design-system-foundation-and-token-extraction`
- `design-context-and-direction-contract`
- `source-metadata-and-provenance`
- `ui-review-scope-and-evidence-acquisition`

Never perform remote Git, external-system writes, merge, deploy, release, or an adjacent capability's work. Review and preflight capabilities never repair product source; evidence-acquisition capabilities never issue design findings.
