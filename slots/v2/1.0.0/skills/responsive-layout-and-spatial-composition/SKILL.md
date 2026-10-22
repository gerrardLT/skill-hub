---
name: responsive-layout-and-spatial-composition
description: Design and implement semantic information hierarchy, layout, density, grid, reflow, and content rhythm across supported viewports and zoom levels. Do not use for define the component token system and theme foundation or implement form validation, async, permission, and recovery states inside the completed layout.
---

# Responsive Layout And Spatial Composition

## Responsibility

Design and implement semantic information hierarchy, layout, density, grid, reflow, and content rhythm across supported viewports and zoom levels.

## Trigger

Use when the requested outcome is: Design and implement semantic information hierarchy, layout, density, grid, reflow, and content rhythm across supported viewports and zoom levels.

Do not use when:
- Define the component token system and theme foundation. Route to `design-system-foundation-and-token-extraction`.
- Implement form validation, async, permission, and recovery states inside the completed layout. Route to `interaction-states-forms-and-navigation`.

## Required Inputs

- A visual direction, content structure, device classes, breakpoints, and existing layout constraints.

Also require source or render identity, authorization, target surfaces, supported states, decision owner, and declared unknowns where applicable.

## Procedure

1. Freeze user flow, information hierarchy, authentic content extremes, supported viewport range, zoom target, input modes, and existing layout constraints.
2. Order content semantically before choosing columns; define primary, supporting, progressive, and deferrable regions.
3. Implement content-driven width constraints, grids or flex rules, spacing rhythm, alignment, density, and reflow without device-specific duplication.
4. Handle narrow, intermediate, wide, short-height, long-content, localization, zoom, overflow, safe areas, keyboard, and touch targets.
5. Capture representative widths and stress states; record clipping, reordering, hidden-content, and interaction risks for review.

## Output Contract

Produce:
- responsive composition source
- breakpoint and reflow contract
- spatial hierarchy map
- multi-width stress evidence

Every material design choice, implementation claim, finding, score, capture, or disposition must link to supplied authority or current evidence, or be labeled assumption/unknown.

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
- Preserve product truth, user task, semantic order, authentic content, accessibility, responsive behavior, state coverage, source identity, and authority boundaries where applicable.
- Return `needs-input` when an identifiable owner can supply a missing requirement, asset authority, capture, state, or decision.
- Return `blocked` when required authorization, safe mutation scope, rendered evidence, tooling, or specialist dependency is unavailable.

## Rendered Evidence

When this capability assesses or validates a rendered interface, static source inspection, DOM assertions, model self-attestation, or a single ideal screenshot are insufficient. Require current provenance-bound captures or traces for the declared routes, states, viewports, zoom, input modes, themes, and motion behavior. Missing evidence returns `needs-input` or `blocked`, never `passed`.

## Status Mapping

- `passed`: output contract and every hard gate are satisfied with current evidence.
- `needs-input`: a requestable source, state, decision, capture, or authorization term is missing.
- `blocked`: proceeding would exceed authority, mix review with repair, or rely on unavailable critical evidence.
- `failed`: authorized work ran but a deterministic gate or required output failed.

## Non-Responsibilities

Does not approve upstream product decisions, expand authority, or perform remote writes beyond its explicit permission identity.

Adjacent capabilities:
- `design-system-foundation-and-token-extraction`
- `visual-language-and-anti-template-controls`
- `interaction-states-forms-and-navigation`
- `accessibility-contracts-and-assistive-validation`

Never perform remote Git, external-system writes, merge, deploy, release, or an adjacent capability's work. Review and preflight capabilities never repair product source; evidence-acquisition capabilities never issue design findings.
