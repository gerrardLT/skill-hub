---
name: prototyping-and-variant-selection
description: "Consolidated capability with 3 selectable modes: divergent-prototyping-and-variant-selection; existing-interface-redesign-and-preservation; visual-language-and-anti-template-controls. Choose exactly one mode per invocation."
version: 1.1.0-consolidated
modes: [divergent-prototyping-and-variant-selection, existing-interface-redesign-and-preservation, visual-language-and-anti-template-controls]
---

# Prototyping And Variant Selection

## Responsibility

Consolidated capability covering 3 related modes: Build genuinely divergent working UI variants in isolation, compare them on frozen criteria, and preserve human selection before promotion.; Audit an existing interface and define a redesign preservation contract for product truth, user flow, information architecture, routes, SEO, analytics, behavior, and content.; Establish and implement a purposeful visual language that reinforces hierarchy and brand evidence while rejecting generic template patterns and unsupported decoration.

## Mode selection

This capability has several distinct modes. Read this table first, pick exactly one
mode for the current request, then follow only that mode's section. Do not blend
modes: each carries its own permission identity, gates, and stop conditions. The
permission column is binding - a run uses the permission of the mode it selected,
never the widest permission in this document.

| Mode | Permission | Use when | Routes elsewhere |
| --- | --- | --- | --- |
| `divergent-prototyping-and-variant-selection` | `workspace-write` | A UI decision is uncertain enough to build two or more genuinely different working variants to compare; Someone asks for isolated prototypes with equivalent captures and a tradeoff matrix before choos | Polish the selected direction into the production design system and responsive source (-> design-system-foundation-and-t |
| `existing-interface-redesign-and-preservation` | `workspace-write` | An existing product or site is being redesigned and must keep its routes, SEO, analytics and user tasks working; Someone asks what in the current interface must be preserved, migrated, replaced or rem | Choose a visual direction for a new interface with no existing product behavior to preserve (-> design-context-and-direc |
| `visual-language-and-anti-template-controls` | `workspace-write` | An interface needs a deliberate visual language for type, color, shape and emphasis that stays tied to brand evidence; Someone asks to remove generic template patterns and unsupported decoration from  | Define page-level grid, responsive reflow, and spatial density across widths (-> responsive-layout-and-spatial-compositi |

## Mode: `divergent-prototyping-and-variant-selection`

### divergent-prototyping-and-variant-selection

#### Responsibility

Build genuinely divergent working UI variants in isolation, compare them on frozen criteria, and preserve human selection before promotion.

#### Trigger

Use when the request matches any of:
- A UI decision is uncertain enough to build two or more genuinely different working variants to compare
- Someone asks for isolated prototypes with equivalent captures and a tradeoff matrix before choosing

Do not use when:
- Polish the selected direction into the production design system and responsive source. Route to `design-system-foundation-and-token-extraction`.
- Run an independent release review on the promoted production implementation. Route to `rendered-ui-critique-and-release-disposition`.

#### Required Inputs

- One UI brief, project tokens, authentic context, and named axes of divergence.

#### Procedure

1. Freeze one brief, authentic content set, project tokens, supported viewport, comparison criteria, and named axes of divergence.
2. Build each variant in an isolated path or artifact without altering production routes or shared behavior.
3. Make variants structurally different in information hierarchy, composition, interaction, or density; reject superficial palette swaps.
4. Capture equivalent states and compare task clarity, accessibility implications, responsiveness, feasibility, and tradeoffs.
5. Record the human selection, rejected alternatives, rationale, and promotion handoff; never self-select or auto-promote.

#### Domain Guidance

- Before comparison, render every variant with a clean console: all variants render, every interaction responds, and no console errors. Fix or report a variant that fails this check instead of comparing it.
- Present the set and stop; the choice belongs to the named human owner.

#### Output Contract

Produce:
- isolated working variants
- equivalent comparison captures
- tradeoff matrix
- human selection and promotion handoff

Every material design choice, implementation claim, finding, score, capture, or disposition must link to supplied authority or current evidence, or be labeled assumption/unknown.

Deliver each output as the artifact itself (tables, commands, patches, plans, records), not as a description of how it would be produced.

#### UI Coverage

- `divergence`
- `isolation`
- `authentic-content`
- `fair-comparison`
- `human-selection`

#### Hard Gates

- At least two variants must differ structurally on declared axes; palette-only or typography-only alternatives do not count as divergence.
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

#### Rendered Evidence

When this capability assesses or validates a rendered interface, static source inspection, DOM assertions, model self-attestation, or a single ideal screenshot are insufficient. Require current provenance-bound captures or traces for the declared routes, states, viewports, zoom, input modes, themes, and motion behavior. Missing evidence returns `needs-input` or `blocked`, never `passed`.

#### Human Design Authority

The Skill may preserve evidence, alternatives, tradeoffs, findings, and a recommendation. Final taste selection, prototype promotion, accepted risk, scope approval, source-repair approval, and release disposition remain explicit human decisions with a named owner.

#### Status Mapping

- `passed`: output contract and every hard gate are satisfied with current evidence.
- `needs-input`: a requestable source, state, decision, capture, or authorization term is missing. Deliver every supported part first and name the owner for the missing part.
- `blocked`: proceeding would exceed authority, mix review with repair, or rely on unavailable critical evidence.
- `failed`: authorized work ran but a deterministic gate or required output failed.

#### Non-Responsibilities

Adjacent capabilities:
- `design-context-and-direction-contract`
- `design-system-foundation-and-token-extraction`
- `responsive-layout-and-spatial-composition`
- `rendered-ui-critique-and-release-disposition`

Never perform remote Git, external-system writes, merge, deploy, release, or an adjacent capability's work. Review and preflight capabilities never repair product source; evidence-acquisition capabilities never issue design findings.

## Mode: `existing-interface-redesign-and-preservation`

### existing-interface-redesign-and-preservation

#### Responsibility

Audit an existing interface and define a redesign preservation contract for product truth, user flow, information architecture, routes, SEO, analytics, behavior, and content.

#### Trigger

Use when the request matches any of:
- An existing product or site is being redesigned and must keep its routes, SEO, analytics and user tasks working
- Someone asks what in the current interface must be preserved, migrated, replaced or removed, and who decides

Do not use when:
- Choose a visual direction for a new interface with no existing product behavior to preserve. Route to `design-context-and-direction-contract`.
- Apply accepted redesign fixes to product source after review. Route to `ui-remediation`.

#### Required Inputs

- An existing UI, brand, tokens, information architecture, content, routes, analytics, and redesign brief.

#### Procedure

1. Classify the mode (greenfield, redesign that preserves behavior, or approved overhaul) and state the evidence for it.
2. Freeze the redesign brief and inspect authorized current routes, content, components, analytics, SEO metadata, accessibility behavior, and known business invariants.
3. Separate verified product truth from visual debt, implementation accident, unknown dependency, and explicitly removable behavior.
4. Map current user flows, information architecture, deep links, forms, state transitions, tracking, and search or sharing contracts.
5. Define preserve, migrate, replace, and remove decisions with owner, rationale, tests, and rollback or compatibility needs.
6. Sequence a reversible migration and hand off constraints to design direction; do not redesign or repair source in this audit.

#### Domain Guidance

- Step 1 is mode classification: greenfield (no existing behavior to keep), redesign that preserves behavior, or an approved full overhaul. Misclassifying the mode is the largest source of bad redesign output; state the mode and the evidence for it.

#### Output Contract

Produce:
- current-state UI audit
- preservation and migration contract
- invariant test map
- redesign risk ledger

Every material design choice, implementation claim, finding, score, capture, or disposition must link to supplied authority or current evidence, or be labeled assumption/unknown.

Deliver each output as the artifact itself (tables, commands, patches, plans, records), not as a description of how it would be produced.

#### UI Coverage

- `preservation`
- `user-flow`
- `information-architecture`
- `SEO`
- `analytics`
- `behavior`
- `migration`

#### Hard Gates

- No existing route, content obligation, analytics event, SEO contract, user task, or behavior may be silently removed because it appears visually obsolete.
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

#### Human Design Authority

The Skill may preserve evidence, alternatives, tradeoffs, findings, and a recommendation. Final taste selection, prototype promotion, accepted risk, scope approval, source-repair approval, and release disposition remain explicit human decisions with a named owner.

#### Status Mapping

- `passed`: output contract and every hard gate are satisfied with current evidence.
- `needs-input`: a requestable source, state, decision, capture, or authorization term is missing. Deliver every supported part first and name the owner for the missing part.
- `blocked`: proceeding would exceed authority, mix review with repair, or rely on unavailable critical evidence.
- `failed`: authorized work ran but a deterministic gate or required output failed.

#### Non-Responsibilities

Adjacent capabilities:
- `design-context-and-direction-contract`
- `ui-task-routing-and-governance`
- `ui-remediation`
- `rendered-ui-critique-and-release-disposition`

Never perform remote Git, external-system writes, merge, deploy, release, or an adjacent capability's work. Review and preflight capabilities never repair product source; evidence-acquisition capabilities never issue design findings.

## Mode: `visual-language-and-anti-template-controls`

### visual-language-and-anti-template-controls

#### Responsibility

Establish and implement a purposeful visual language that reinforces hierarchy and brand evidence while rejecting generic template patterns and unsupported decoration.

#### Trigger

Use when the request matches any of:
- An interface needs a deliberate visual language for type, color, shape and emphasis that stays tied to brand evidence
- Someone asks to remove generic template patterns and unsupported decoration from a design

Do not use when:
- Define page-level grid, responsive reflow, and spatial density across widths. Route to `responsive-layout-and-spatial-composition`.
- Write the truthful product copy, realistic records, and authorized assets. Route to `content-copy-and-authentic-assets`.
- Decide the overall design direction, flow and hierarchy. Route to `design-context-and-direction-contract`.

#### Required Inputs

- A direction contract, brand, tokens, audience, surface mode, and content.

#### Procedure

1. Freeze the design contract, brand evidence, authentic content, accessibility constraints, existing system, and explicit anti-goals.
2. Name a small visual thesis and map typography, color, shape, border, surface, imagery, icon, and emphasis roles to it.
3. Audit and remove generic hero, card-grid, gradient, pill, floating-panel, decorative-chart, and icon patterns that lack task or brand purpose.
4. Implement reusable visual rules through the existing token and component foundation rather than one-off styling.
5. Stress hierarchy, contrast, dense and sparse content, themes, and states; preserve human-owned taste alternatives when evidence cannot decide.

#### Domain Guidance

- Tells to avoid unless the brief earns them: neon or outer glows, pure black (#000000), oversaturated accents, same-size icon-heading-text card grids as page structure, gradient heroes, floating pill clusters, and decorative charts. A brief that asks for one can earn it; otherwise say what replaced it.
- When a color or type value is contested, give provisional roles with the owner named, offer local preparation of the change for review, state the fallback font stack, and give concrete sizes and touch targets. Keep contested values non-final until the owner decides.

#### Output Contract

Produce:
- visual-language specification
- implemented visual grammar
- anti-template audit
- taste-decision register

Every material design choice, implementation claim, finding, score, capture, or disposition must link to supplied authority or current evidence, or be labeled assumption/unknown.

Deliver each output as the artifact itself (tables, commands, patches, plans, records), not as a description of how it would be produced.

#### UI Coverage

- `typography`
- `color`
- `shape`
- `hierarchy`
- `brand`
- `anti-template`
- `accessibility`

#### Hard Gates

- Every prominent visual device must serve hierarchy, task, content, state, or evidenced brand identity; unsupported decoration and generic template motifs must be removed.
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

#### Human Design Authority

The Skill may preserve evidence, alternatives, tradeoffs, findings, and a recommendation. Final taste selection, prototype promotion, accepted risk, scope approval, source-repair approval, and release disposition remain explicit human decisions with a named owner.

#### Status Mapping

- `passed`: output contract and every hard gate are satisfied with current evidence.
- `needs-input`: a requestable source, state, decision, capture, or authorization term is missing. Deliver every supported part first and name the owner for the missing part.
- `blocked`: proceeding would exceed authority, mix review with repair, or rely on unavailable critical evidence.
- `failed`: authorized work ran but a deterministic gate or required output failed.

#### Non-Responsibilities

Adjacent capabilities:
- `design-context-and-direction-contract`
- `design-system-foundation-and-token-extraction`
- `responsive-layout-and-spatial-composition`
- `content-copy-and-authentic-assets`

Never perform remote Git, external-system writes, merge, deploy, release, or an adjacent capability's work. Review and preflight capabilities never repair product source; evidence-acquisition capabilities never issue design findings.
