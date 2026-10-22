---
name: divergent-prototyping-and-variant-selection
description: Build genuinely divergent working UI variants in isolation, compare them on frozen criteria, and preserve human selection before promotion. Do not use for polish the selected direction into the production design system and responsive source or run an independent release review on the promoted production implementation.
---

# Divergent Prototyping And Variant Selection

## Responsibility

Build genuinely divergent working UI variants in isolation, compare them on frozen criteria, and preserve human selection before promotion.

## Trigger

Use when the requested outcome is: Build genuinely divergent working UI variants in isolation, compare them on frozen criteria, and preserve human selection before promotion.

Do not use when:
- Polish the selected direction into the production design system and responsive source. Route to `design-system-foundation-and-token-extraction`.
- Run an independent release review on the promoted production implementation. Route to `rendered-ui-critique-and-release-disposition`.

## Required Inputs

- One UI brief, project tokens, authentic context, and named axes of divergence.

Also require source or render identity, authorization, target surfaces, supported states, decision owner, and declared unknowns where applicable.

## Procedure

1. Freeze one brief, authentic content set, project tokens, supported viewport, comparison criteria, and named axes of divergence.
2. Build each variant in an isolated path or artifact without altering production routes or shared behavior.
3. Make variants structurally different in information hierarchy, composition, interaction, or density; reject superficial palette swaps.
4. Capture equivalent states and compare task clarity, accessibility implications, responsiveness, feasibility, and tradeoffs.
5. Record the human selection, rejected alternatives, rationale, and promotion handoff; never self-select or auto-promote.

## Output Contract

Produce:
- isolated working variants
- equivalent comparison captures
- tradeoff matrix
- human selection and promotion handoff

Every material design choice, implementation claim, finding, score, capture, or disposition must link to supplied authority or current evidence, or be labeled assumption/unknown.

## UI Coverage

- `divergence`
- `isolation`
- `authentic-content`
- `fair-comparison`
- `human-selection`

## Hard Gates

- At least two variants must differ structurally on declared axes; palette-only or typography-only alternatives do not count as divergence.
- Preserve product truth, user task, semantic order, authentic content, accessibility, responsive behavior, state coverage, source identity, and authority boundaries where applicable.
- Return `needs-input` when an identifiable owner can supply a missing requirement, asset authority, capture, state, or decision.
- Return `blocked` when required authorization, safe mutation scope, rendered evidence, tooling, or specialist dependency is unavailable.

## Rendered Evidence

When this capability assesses or validates a rendered interface, static source inspection, DOM assertions, model self-attestation, or a single ideal screenshot are insufficient. Require current provenance-bound captures or traces for the declared routes, states, viewports, zoom, input modes, themes, and motion behavior. Missing evidence returns `needs-input` or `blocked`, never `passed`.

## Human Design Authority

The Skill may preserve evidence, alternatives, tradeoffs, findings, and a recommendation. Final taste selection, prototype promotion, accepted risk, scope approval, source-repair approval, and release disposition remain explicit human decisions with a named owner.

## Status Mapping

- `passed`: output contract and every hard gate are satisfied with current evidence.
- `needs-input`: a requestable source, state, decision, capture, or authorization term is missing.
- `blocked`: proceeding would exceed authority, mix review with repair, or rely on unavailable critical evidence.
- `failed`: authorized work ran but a deterministic gate or required output failed.

## Non-Responsibilities

Does not approve upstream product decisions, expand authority, or perform remote writes beyond its explicit permission identity.

Adjacent capabilities:
- `design-context-and-direction-contract`
- `design-system-foundation-and-token-extraction`
- `responsive-layout-and-spatial-composition`
- `rendered-ui-critique-and-release-disposition`

Never perform remote Git, external-system writes, merge, deploy, release, or an adjacent capability's work. Review and preflight capabilities never repair product source; evidence-acquisition capabilities never issue design findings.
