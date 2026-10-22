---
name: responsive-layout-and-spatial-composition
description: "Design and implement semantic information hierarchy, layout, density, grid, reflow, and content rhythm across supported viewports and zoom levels. Use when A page or component needs a layout and reflow design across desktop, tablet and mobile widths; Someone asks for breakpoints, grid, density and what happens at intermediate widths, zoom and long content. Do not use for: Define the component token system and theme foundation (-> design-system-foundation-and-token-extraction); Implement form validation, async, permission, and recovery states inside the completed layout (-> interaction-states-forms-and-navigation)."
---

# Responsive Layout And Spatial Composition

## Responsibility

Design and implement semantic information hierarchy, layout, density, grid, reflow, and content rhythm across supported viewports and zoom levels.

## Trigger

Use when the request matches any of:
- A page or component needs a layout and reflow design across desktop, tablet and mobile widths
- Someone asks for breakpoints, grid, density and what happens at intermediate widths, zoom and long content

Do not use when:
- Define the component token system and theme foundation. Route to `design-system-foundation-and-token-extraction`.
- Implement form validation, async, permission, and recovery states inside the completed layout. Route to `interaction-states-forms-and-navigation`.

## Required Inputs

- A visual direction, content structure, device classes, breakpoints, and existing layout constraints.

## Procedure

1. Freeze user flow, information hierarchy, authentic content extremes, supported viewport range, zoom target, input modes, and existing layout constraints.
2. Order content semantically before choosing columns; define primary, supporting, progressive, and deferrable regions.
3. Implement content-driven width constraints, grids or flex rules, spacing rhythm, alignment, density, and reflow without device-specific duplication.
4. Handle narrow, intermediate, wide, short-height, long-content, localization, zoom, overflow, safe areas, keyboard, and touch targets.
5. Capture representative widths and stress states; record clipping, reordering, hidden-content, and interaction risks for review.

## Domain Guidance

- Hard rules: the hero fits the initial viewport with a headline of at most two lines; never disable zoom; body text at least 16 px; systematic breakpoints (for example 375, 768, 1024, 1440).
- A control rail taller than the viewport scrolls internally and keeps Apply and Clear controls sticky; manage focus when it opens and closes so the filters stay reachable.
- Give an executable overflow check for each width (document.scrollingElement.scrollWidth equals clientWidth, so no horizontal overflow) and state where each inserted block, such as a promo banner, lands after reflow at every breakpoint.

## Output Contract

Produce:
- responsive composition source
- breakpoint and reflow contract
- spatial hierarchy map
- multi-width stress evidence
- per-breakpoint reflow table with overflow check for each tested width

Every material design choice, implementation claim, finding, score, capture, or disposition must link to supplied authority or current evidence, or be labeled assumption/unknown.

Deliver each output as the artifact itself (tables, commands, patches, plans, records), not as a description of how it would be produced.

## UI Coverage

- `information-hierarchy`
- `mobile`
- `tablet`
- `desktop`
- `intermediate-widths`
- `zoom`
- `overflow`
- `density`
- `touch-targets`

## Hard Gates

- Desktop and mobile endpoints are insufficient: the layout must survive intermediate widths, 200% zoom, long or localized content, overflow, and touch-target constraints without losing task order.
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

## Rendered Evidence

When this capability assesses or validates a rendered interface, static source inspection, DOM assertions, model self-attestation, or a single ideal screenshot are insufficient. Require current provenance-bound captures or traces for the declared routes, states, viewports, zoom, input modes, themes, and motion behavior. Missing evidence returns `needs-input` or `blocked`, never `passed`.

## Status Mapping

- `passed`: output contract and every hard gate are satisfied with current evidence.
- `needs-input`: a requestable source, state, decision, capture, or authorization term is missing. Deliver every supported part first and name the owner for the missing part.
- `blocked`: proceeding would exceed authority, mix review with repair, or rely on unavailable critical evidence.
- `failed`: authorized work ran but a deterministic gate or required output failed.

## Non-Responsibilities

Adjacent capabilities:
- `design-system-foundation-and-token-extraction`
- `visual-language-and-anti-template-controls`
- `interaction-states-forms-and-navigation`
- `accessibility-contracts-and-assistive-validation`

Never perform remote Git, external-system writes, merge, deploy, release, or an adjacent capability's work. Review and preflight capabilities never repair product source; evidence-acquisition capabilities never issue design findings.
