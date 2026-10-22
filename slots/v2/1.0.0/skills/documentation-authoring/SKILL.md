---
name: documentation-authoring
description: Author one evidence-grounded reference, explanation, how-to, or tutorial for a declared audience and purpose. Do not use for decide the lifecycle, owner, and retention of all project documents or update release notes from a shipped diff.
---

# Documentation Authoring

## Responsibility

Author one evidence-grounded reference, explanation, how-to, or tutorial for a declared audience and purpose.

## Trigger

Use when the requested outcome is: Author one evidence-grounded reference, explanation, how-to, or tutorial for a declared audience and purpose.

Do not use when:
- Decide the lifecycle, owner, and retention of all project documents. Route to `document-and-artifact-governance`.
- Update release notes from a shipped diff. Route to `release-documentation-maintenance`.

## Required Inputs

- Approved source facts, audience, documentation type, scope, style, and output path.

Also require source identities, authority, decision owner, scope, and declared unknowns where applicable.

## Procedure

1. Choose exactly one documentation intent and audience; state prerequisites and exclusions.
2. Build a source map from approved facts, commands, and decisions.
3. Draft the minimum structure appropriate to reference, explanation, how-to, or tutorial.
4. Mark unknowns and avoid claiming unexecuted commands or unsupported behavior.
5. Self-check links, examples, accessibility, and handoff for rendering or review.

## Output Contract

Produce:
- documentation artifact
- source map
- validation notes
- unresolved-facts register

Every material claim, score, recommendation, or finding must link to a supplied or authorized source, or be labeled assumption/unknown.

## Hard Gates

- Never blend documentation types or turn an unverified command, feature, or future plan into present-tense fact.
- Preserve conflicts, counterevidence, unknowns, source identity, and authority boundaries.
- Return `needs-input` when an identifiable owner can supply a missing requirement or decision.
- Return `blocked` when required authority, evidence, governance, or a safe execution boundary is unavailable.

## Status Mapping

- `passed`: output contract and every hard gate are satisfied.
- `needs-input`: a requestable source, decision, or governance term is missing.
- `blocked`: proceeding would exceed authority, violate governance, or rely on unavailable critical evidence.
- `failed`: supplied inputs were processed but a deterministic gate or required output failed.

## Non-Responsibilities

Does not absorb unrelated lifecycle responsibilities or expand provider, workspace, or remote-write authority implicitly.

Adjacent capabilities:
- `document-and-artifact-governance`
- `release-documentation-maintenance`
- `document-rendering-and-validation`

Never perform remote Git, external-system writes, merge, deploy, cloud mutation, participant recruitment/contact, or downstream implementation unless a different explicitly authorized capability owns that action.
