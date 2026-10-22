---
name: content-copy-and-authentic-assets
description: "Create truthful task-specific interface copy, realistic content data, and authorized assets with provenance and state coverage. Use when An interface needs real labels, messages, sample records and licensed images instead of placeholders; Someone asks for copy for every state (empty, error, loading, success) without inventing claims or testimonials. Do not use for: Define the product requirements and acceptance criteria for this feature (-> requirements-and-delivery-contract); Choose the final visual direction, palette, type, and composition (-> design-context-and-direction-contract)."
---

# Content Copy And Authentic Assets

## Responsibility

Create truthful task-specific interface copy, realistic content data, and authorized assets with provenance and state coverage.

## Trigger

Use when the request matches any of:
- An interface needs real labels, messages, sample records and licensed images instead of placeholders
- Someone asks for copy for every state (empty, error, loading, success) without inventing claims or testimonials

Do not use when:
- Define the product requirements and acceptance criteria for this feature. Route to `requirements-and-delivery-contract`.
- Choose the final visual direction, palette, type, and composition. Route to `design-context-and-direction-contract`.

## Required Inputs

- Product facts, brand voice, content needs, licensed material, and asset-generation capability.

## Procedure

1. Freeze product facts, audience language, legal or brand constraints, content schema, localization boundary, and asset authority.
2. Map content to user intent and every loading, empty, error, permission, validation, success, and recovery state.
3. Write specific labels and messages that explain consequence and next action; remove lorem ipsum, fake testimonials, invented metrics, and decorative jargon.
4. Use only authorized assets and record source, license, transformation, alt intent, and replacement rule.
5. Check truncation, pluralization, variable data, localization expansion, and screen-reader comprehension before handoff.

## Domain Guidance

- Density defaults for marketing surfaces: headline at most 8 words, supporting paragraph at most 25 words, and one visual asset or one call to action per section; anything longer needs a stated reason.
- Asset priority: generate or license an authentic image first, then real product screenshots; never fake a screenshot with styled boxes. Record source, license and alt intent for each.

## Output Contract

Produce:
- interface copy deck
- realistic content fixtures
- asset provenance ledger
- state-content matrix

Every material design choice, implementation claim, finding, score, capture, or disposition must link to supplied authority or current evidence, or be labeled assumption/unknown.

Deliver each output as the artifact itself (tables, commands, patches, plans, records), not as a description of how it would be produced.

## UI Coverage

- `truthful-copy`
- `authentic-content`
- `asset-provenance`
- `localization`
- `state-content`

## Hard Gates

- No placeholder, invented claim, unverifiable metric, fake social proof, or unlicensed asset may enter a candidate presented as realistic or release-ready.
- Review, evidence acquisition, preflight, and preservation audit never imply source remediation or release authority.
- Preserve product truth, user task, semantic order, authentic content, accessibility, responsive behavior, state coverage, source identity, and authority boundaries where applicable.
- Return `needs-input` when an identifiable owner can supply a missing requirement, asset authority, capture, state, or decision.
- Return `blocked` when required authorization, safe mutation scope, rendered evidence, tooling, or specialist dependency is unavailable.
- Deliver every part the supplied evidence and authority support, label assumptions, and list each missing item with the owner who can supply it; `needs-input` or `blocked` applies to the unsupported part, not to the whole deliverable.

## Forbidden Actions

- remote Git, merge, deploy, release, cloud mutation, or external-system write
- invent product facts, brand authority, copy claims, customer data, assets, evidence, or approval
- perform an adjacent capability or combine independent review with source repair
- treat static inspection, stale capture, or model self-report as current rendered evidence
- claim evaluation, approval, release, or completion evidence that has not been produced

## Status Mapping

- `passed`: output contract and every hard gate are satisfied with current evidence.
- `needs-input`: a requestable source, state, decision, capture, or authorization term is missing. Deliver every supported part first and name the owner for the missing part.
- `blocked`: proceeding would exceed authority, mix review with repair, or rely on unavailable critical evidence.
- `failed`: authorized work ran but a deterministic gate or required output failed.

## Non-Responsibilities

Adjacent capabilities:
- `visual-language-and-anti-template-controls`
- `interaction-states-forms-and-navigation`
- `accessibility-contracts-and-assistive-validation`
- `documentation-authoring`
- `requirements-and-delivery-contract`
- `design-context-and-direction-contract`

Never perform remote Git, external-system writes, merge, deploy, release, or an adjacent capability's work. Review and preflight capabilities never repair product source; evidence-acquisition capabilities never issue design findings.
