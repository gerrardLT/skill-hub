---
name: documentation-authoring
description: "Author one evidence-grounded reference, explanation, how-to, or tutorial for a declared audience and purpose. Use when A reference page, how-to, tutorial or explanation must be written for a named audience from verified facts; Code or a feature needs documentation and the author must first understand how it actually works. Do not use for: Decide the lifecycle, owner, and retention of all project documents (-> document-and-artifact-governance); Update release notes from a shipped diff (-> release-documentation-maintenance)."
---

# Documentation Authoring

## Responsibility

Author one evidence-grounded reference, explanation, how-to, or tutorial for a declared audience and purpose.

## Trigger

Use when the request matches any of:
- A reference page, how-to, tutorial or explanation must be written for a named audience from verified facts
- Code or a feature needs documentation and the author must first understand how it actually works

Do not use when:
- Decide the lifecycle, owner, and retention of all project documents. Route to `document-and-artifact-governance`.
- Update release notes from a shipped diff. Route to `release-documentation-maintenance`.

## Required Inputs

- Approved source facts, audience, documentation type, scope, style, and output path.

## Procedure

1. Choose exactly one documentation intent and audience; state prerequisites and exclusions.
2. When the subject is code, read the entry points and trace the documented flow before drafting; record what was read.
3. Build a source map from approved facts, commands, and decisions.
4. Draft the minimum structure appropriate to reference, explanation, how-to, or tutorial.
5. Mark unknowns and avoid claiming unexecuted commands or unsupported behavior.
6. Self-check links, examples, accessibility, and handoff for rendering or review.

## Domain Guidance

- Research before writing: when documenting code, map the structure, read the entry points and trace the documented flow end to end. Documentation quality is proportional to understanding of the code.
- One documentation type per page (reference, how-to, tutorial, explanation). Reference pages are neutral and structured per item (name, type, default, description); conflicts between sources are surfaced, not resolved silently.
- Exclude or flag any item that exists in only one unverified source, for example a flag mentioned in a request but absent from the code.

## Output Contract

Produce:
- documentation artifact
- source map
- validation notes
- unresolved-facts register

Every material claim, score, recommendation, or finding must link to a supplied or authorized source, or be labeled assumption/unknown.

Deliver each output as the artifact itself (tables, commands, patches, plans, records), not as a description of how it would be produced.

## Hard Gates

- Never blend documentation types or turn an unverified command, feature, or future plan into present-tense fact.
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
- `document-and-artifact-governance`
- `release-documentation-maintenance`
- `document-rendering-and-validation`

Never perform remote Git, external-system writes, merge, deploy, cloud mutation, participant recruitment/contact, or downstream implementation unless a different explicitly authorized capability owns that action.
