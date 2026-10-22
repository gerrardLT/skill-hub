---
name: divergent-prototyping-and-variant-selection
description: "Build genuinely divergent working UI variants in isolation, compare them on frozen criteria, and preserve human selection before promotion. Use when A UI decision is uncertain enough to build two or more genuinely different working variants to compare; Someone asks for isolated prototypes with equivalent captures and a tradeoff matrix before choosing. Do not use for: Polish the selected direction into the production design system and responsive source (-> design-system-foundation-and-token-extraction); Run an independent release review on the promoted production implementation (-> rendered-ui-critique-and-release-disposition)."
---

# Divergent Prototyping And Variant Selection

## Responsibility

Build genuinely divergent working UI variants in isolation, compare them on frozen criteria, and preserve human selection before promotion.

## Trigger

Use when the request matches any of:
- A UI decision is uncertain enough to build two or more genuinely different working variants to compare
- Someone asks for isolated prototypes with equivalent captures and a tradeoff matrix before choosing

Do not use when:
- Polish the selected direction into the production design system and responsive source. Route to `design-system-foundation-and-token-extraction`.
- Run an independent release review on the promoted production implementation. Route to `rendered-ui-critique-and-release-disposition`.

## Required Inputs

- One UI brief, project tokens, authentic context, and named axes of divergence.

## Procedure

1. Freeze one brief, authentic content set, project tokens, supported viewport, comparison criteria, and named axes of divergence.
2. Build each variant in an isolated path or artifact without altering production routes or shared behavior.
3. Make variants structurally different in information hierarchy, composition, interaction, or density; reject superficial palette swaps.
4. Capture equivalent states and compare task clarity, accessibility implications, responsiveness, feasibility, and tradeoffs.
5. Record the human selection, rejected alternatives, rationale, and promotion handoff; never self-select or auto-promote.

## Domain Guidance

- Before comparison, render every variant with a clean console: all variants render, every interaction responds, and no console errors. Fix or report a variant that fails this check instead of comparing it.
- Present the set and stop; the choice belongs to the named human owner.

## Output Contract

Produce:
- isolated working variants
- equivalent comparison captures
- tradeoff matrix
- human selection and promotion handoff

Every material design choice, implementation claim, finding, score, capture, or disposition must link to supplied authority or current evidence, or be labeled assumption/unknown.

Deliver each output as the artifact itself (tables, commands, patches, plans, records), not as a description of how it would be produced.

## UI Coverage

- `divergence`
- `isolation`
- `authentic-content`
- `fair-comparison`
- `human-selection`

## Hard Gates

- At least two variants must differ structurally on declared axes; palette-only or typography-only alternatives do not count as divergence.
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

## Human Design Authority

The Skill may preserve evidence, alternatives, tradeoffs, findings, and a recommendation. Final taste selection, prototype promotion, accepted risk, scope approval, source-repair approval, and release disposition remain explicit human decisions with a named owner.

## Status Mapping

- `passed`: output contract and every hard gate are satisfied with current evidence.
- `needs-input`: a requestable source, state, decision, capture, or authorization term is missing. Deliver every supported part first and name the owner for the missing part.
- `blocked`: proceeding would exceed authority, mix review with repair, or rely on unavailable critical evidence.
- `failed`: authorized work ran but a deterministic gate or required output failed.

## Non-Responsibilities

Adjacent capabilities:
- `design-context-and-direction-contract`
- `design-system-foundation-and-token-extraction`
- `responsive-layout-and-spatial-composition`
- `rendered-ui-critique-and-release-disposition`

Never perform remote Git, external-system writes, merge, deploy, release, or an adjacent capability's work. Review and preflight capabilities never repair product source; evidence-acquisition capabilities never issue design findings.
