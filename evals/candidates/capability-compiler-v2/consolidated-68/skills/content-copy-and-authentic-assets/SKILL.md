---
name: content-copy-and-authentic-assets
description: "Consolidated capability with 2 selectable modes: content-copy-and-authentic-assets; documentation-authoring. Choose exactly one mode per invocation."
version: 1.1.0-consolidated
modes: [content-copy-and-authentic-assets, documentation-authoring]
---

# Content Copy And Authentic Assets

## Responsibility

Consolidated capability covering 2 related modes: Create truthful task-specific interface copy, realistic content data, and authorized assets with provenance and state coverage.; Author one evidence-grounded reference, explanation, how-to, or tutorial for a declared audience and purpose.

## Mode selection

This capability has several distinct modes. Read this table first, pick exactly one
mode for the current request, then follow only that mode's section. Do not blend
modes: each carries its own permission identity, gates, and stop conditions. The
permission column is binding - a run uses the permission of the mode it selected,
never the widest permission in this document.

| Mode | Permission | Use when | Routes elsewhere |
| --- | --- | --- | --- |
| `content-copy-and-authentic-assets` | `workspace-write` | An interface needs real labels, messages, sample records and licensed images instead of placeholders; Someone asks for copy for every state (empty, error, loading, success) without inventing claims or | Define the product requirements and acceptance criteria for this feature (-> requirements-and-delivery-contract); Choose |
| `documentation-authoring` | `workspace-write` | A reference page, how-to, tutorial or explanation must be written for a named audience from verified facts; Code or a feature needs documentation and the author must first understand how it actually w | Decide the lifecycle, owner, and retention of all project documents (-> document-and-artifact-governance); Update releas |

## Mode: `content-copy-and-authentic-assets`

### content-copy-and-authentic-assets

#### Responsibility

Create truthful task-specific interface copy, realistic content data, and authorized assets with provenance and state coverage.

#### Trigger

Use when the request matches any of:
- An interface needs real labels, messages, sample records and licensed images instead of placeholders
- Someone asks for copy for every state (empty, error, loading, success) without inventing claims or testimonials

Do not use when:
- Define the product requirements and acceptance criteria for this feature. Route to `requirements-and-delivery-contract`.
- Choose the final visual direction, palette, type, and composition. Route to `design-context-and-direction-contract`.

#### Required Inputs

- Product facts, brand voice, content needs, licensed material, and asset-generation capability.

#### Procedure

1. Freeze product facts, audience language, legal or brand constraints, content schema, localization boundary, and asset authority.
2. Map content to user intent and every loading, empty, error, permission, validation, success, and recovery state.
3. Write specific labels and messages that explain consequence and next action; remove lorem ipsum, fake testimonials, invented metrics, and decorative jargon.
4. Use only authorized assets and record source, license, transformation, alt intent, and replacement rule.
5. Check truncation, pluralization, variable data, localization expansion, and screen-reader comprehension before handoff.

#### Domain Guidance

- Density defaults for marketing surfaces: headline at most 8 words, supporting paragraph at most 25 words, and one visual asset or one call to action per section; anything longer needs a stated reason.
- Asset priority: generate or license an authentic image first, then real product screenshots; never fake a screenshot with styled boxes. Record source, license and alt intent for each.

#### Output Contract

Produce:
- interface copy deck
- realistic content fixtures
- asset provenance ledger
- state-content matrix

Every material design choice, implementation claim, finding, score, capture, or disposition must link to supplied authority or current evidence, or be labeled assumption/unknown.

Deliver each output as the artifact itself (tables, commands, patches, plans, records), not as a description of how it would be produced.

#### UI Coverage

- `truthful-copy`
- `authentic-content`
- `asset-provenance`
- `localization`
- `state-content`

#### Hard Gates

- No placeholder, invented claim, unverifiable metric, fake social proof, or unlicensed asset may enter a candidate presented as realistic or release-ready.
- Review, evidence acquisition, preflight, and preservation audit never imply source remediation or release authority.
- Preserve product truth, user task, semantic order, authentic content, accessibility, responsive behavior, state coverage, source identity, and authority boundaries where applicable.
- Return `needs-input` when an identifiable owner can supply a missing requirement, asset authority, capture, state, or decision.
- Return `blocked` when required authorization, safe mutation scope, rendered evidence, tooling, or specialist dependency is unavailable.
- Deliver every part the supplied evidence and authority support, label assumptions, and list each missing item with the owner who can supply it; `needs-input` or `blocked` applies to the unsupported part, not to the whole deliverable.

#### Forbidden Actions

- remote Git, merge, deploy, release, cloud mutation, or external-system write
- invent product facts, brand authority, copy claims, customer data, assets, evidence, or approval
- perform an adjacent capability or combine independent review with source repair
- treat static inspection, stale capture, or model self-report as current rendered evidence
- claim evaluation, approval, release, or completion evidence that has not been produced

#### Status Mapping

- `passed`: output contract and every hard gate are satisfied with current evidence.
- `needs-input`: a requestable source, state, decision, capture, or authorization term is missing. Deliver every supported part first and name the owner for the missing part.
- `blocked`: proceeding would exceed authority, mix review with repair, or rely on unavailable critical evidence.
- `failed`: authorized work ran but a deterministic gate or required output failed.

#### Non-Responsibilities

Adjacent capabilities:
- `visual-language-and-anti-template-controls`
- `interaction-states-forms-and-navigation`
- `accessibility-contracts-and-assistive-validation`
- `documentation-authoring`
- `requirements-and-delivery-contract`
- `design-context-and-direction-contract`

Never perform remote Git, external-system writes, merge, deploy, release, or an adjacent capability's work. Review and preflight capabilities never repair product source; evidence-acquisition capabilities never issue design findings.

## Mode: `documentation-authoring`

### documentation-authoring

#### Responsibility

Author one evidence-grounded reference, explanation, how-to, or tutorial for a declared audience and purpose.

#### Trigger

Use when the request matches any of:
- A reference page, how-to, tutorial or explanation must be written for a named audience from verified facts
- Code or a feature needs documentation and the author must first understand how it actually works

Do not use when:
- Decide the lifecycle, owner, and retention of all project documents. Route to `document-and-artifact-governance`.
- Update release notes from a shipped diff. Route to `release-documentation-maintenance`.

#### Required Inputs

- Approved source facts, audience, documentation type, scope, style, and output path.

#### Procedure

1. Choose exactly one documentation intent and audience; state prerequisites and exclusions.
2. When the subject is code, read the entry points and trace the documented flow before drafting; record what was read.
3. Build a source map from approved facts, commands, and decisions.
4. Draft the minimum structure appropriate to reference, explanation, how-to, or tutorial.
5. Mark unknowns and avoid claiming unexecuted commands or unsupported behavior.
6. Self-check links, examples, accessibility, and handoff for rendering or review.

#### Domain Guidance

- Research before writing: when documenting code, map the structure, read the entry points and trace the documented flow end to end. Documentation quality is proportional to understanding of the code.
- One documentation type per page (reference, how-to, tutorial, explanation). Reference pages are neutral and structured per item (name, type, default, description); conflicts between sources are surfaced, not resolved silently.
- Exclude or flag any item that exists in only one unverified source, for example a flag mentioned in a request but absent from the code.
- Distinguish ungranted authority from an explicit prohibition. Say not authorized or unknown unless a supplied policy expressly forbids the action.
- When an exact expected validation exit and result placeholder format are supplied, copy both literally; do not replace unknown execution with passed or equivalent prose.
- Record the exact authorization identifier and scope when supplied. Do not state that workspace access or execution is unauthorized if a bounded workspace write is authorized; distinguish authorized write, unexecuted validation and prohibited publication.

#### Output Contract

Produce:
- documentation artifact
- source map
- validation notes
- unresolved-facts register

Every material claim, score, recommendation, or finding must link to a supplied or authorized source, or be labeled assumption/unknown.

Deliver each output as the artifact itself (tables, commands, patches, plans, records), not as a description of how it would be produced.

#### Hard Gates

- Never blend documentation types or turn an unverified command, feature, or future plan into present-tense fact.
- Preserve conflicts, counterevidence, unknowns, source identity, and authority boundaries.
- Return `needs-input` when an identifiable owner can supply a missing requirement or decision.
- Return `blocked` when required authority, evidence, governance, or a safe execution boundary is unavailable.
- Deliver every part the supplied evidence and authority support, label assumptions, and list each missing item with the owner who can supply it; `needs-input` or `blocked` applies to the unsupported part, not to the whole deliverable.

#### Forbidden Actions

- remote Git, pull-request mutation, merge, deploy, cloud mutation, or external-system write
- invent facts, evidence, authority, approval, or customer data
- perform adjacent or downstream capability responsibilities
- claim evaluation, approval, release, or completion evidence that has not been produced

#### Status Mapping

- `passed`: output contract and every hard gate are satisfied.
- `needs-input`: a requestable source, decision, or governance term is missing. Deliver every supported part first and name the owner for the missing part.
- `blocked`: proceeding would exceed authority, violate governance, or rely on unavailable critical evidence.
- `failed`: supplied inputs were processed but a deterministic gate or required output failed.

#### Non-Responsibilities

Adjacent capabilities:
- `document-and-artifact-governance`
- `release-documentation-maintenance`
- `document-rendering-and-validation`

Never perform remote Git, external-system writes, merge, deploy, cloud mutation, participant recruitment/contact, or downstream implementation unless a different explicitly authorized capability owns that action.
