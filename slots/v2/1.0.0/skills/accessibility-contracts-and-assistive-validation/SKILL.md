---
name: accessibility-contracts-and-assistive-validation
description: Define and validate semantic, keyboard, focus, assistive-technology, visual-input, motion, and error-recovery behavior for specified user tasks. Do not use for implement the missing form controls and navigation states in the product source or capture the live page at target viewports for an independent visual release review.
---

# Accessibility Contracts And Assistive Validation

## Responsibility

Define and validate semantic, keyboard, focus, assistive-technology, visual-input, motion, and error-recovery behavior for specified user tasks.

## Trigger

Use when the requested outcome is: Define and validate semantic, keyboard, focus, assistive-technology, visual-input, motion, and error-recovery behavior for specified user tasks.

Do not use when:
- Implement the missing form controls and navigation states in the product source. Route to `interaction-states-forms-and-navigation`.
- Capture the live page at target viewports for an independent visual release review. Route to `ui-review-scope-and-evidence-acquisition`.

## Required Inputs

- User tasks, supported browser and assistive technology, interaction states, WCAG scope, and an implementation.

Also require source or render identity, authorization, target surfaces, supported states, decision owner, and declared unknowns where applicable.

## Procedure

1. Freeze user tasks, supported browsers and assistive technologies, interaction states, WCAG scope, and implementation evidence.
2. Specify semantic structure, accessible names, relationships, keyboard model, focus entry/order/return, announcements, and error recovery per task.
3. Cover contrast, zoom/reflow, pointer and touch alternatives, reduced motion, and authentication or timeout constraints where applicable.
4. Evaluate only supplied current deterministic-check outputs and manual assistive records; record tool, version, viewport, evidence, and untested combinations.
5. Map each criterion to passed, failed, needs-input, or blocked with residual risk; do not repair source.

## Output Contract

Produce:
- accessibility acceptance contract
- assistive-technology test matrix
- criterion evidence ledger
- residual-risk report

Every material design choice, implementation claim, finding, score, capture, or disposition must link to supplied authority or current evidence, or be labeled assumption/unknown.

## UI Coverage

- `semantics`
- `keyboard`
- `focus`
- `assistive-technology`
- `contrast`
- `zoom-reflow`
- `visual-input`
- `reduced-motion`
- `error-recovery`

## Hard Gates

- A generic WCAG checklist cannot pass: every criterion must name a user task, state, expected observable behavior, and current evidence or explicit untested risk.
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
- `interaction-states-forms-and-navigation`
- `responsive-layout-and-spatial-composition`
- `purposeful-motion-and-animation-engineering`
- `ui-review-scope-and-evidence-acquisition`

Never perform remote Git, external-system writes, merge, deploy, release, or an adjacent capability's work. Review and preflight capabilities never repair product source; evidence-acquisition capabilities never issue design findings.
