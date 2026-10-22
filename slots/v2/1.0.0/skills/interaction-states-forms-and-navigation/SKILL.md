---
name: interaction-states-forms-and-navigation
description: Define and implement coherent controls, navigation, forms, validation, loading, empty, error, permission, disabled, success, interruption, and recovery states. Do not use for specify the assistive-technology acceptance and test matrix for the completed interaction or choose the page-level visual hierarchy, grid, density, and breakpoint composition.
---

# Interaction States Forms And Navigation

## Responsibility

Define and implement coherent controls, navigation, forms, validation, loading, empty, error, permission, disabled, success, interruption, and recovery states.

## Trigger

Use when the requested outcome is: Define and implement coherent controls, navigation, forms, validation, loading, empty, error, permission, disabled, success, interruption, and recovery states.

Do not use when:
- Specify the assistive-technology acceptance and test matrix for the completed interaction. Route to `accessibility-contracts-and-assistive-validation`.
- Choose the page-level visual hierarchy, grid, density, and breakpoint composition. Route to `responsive-layout-and-spatial-composition`.

## Required Inputs

- User flows, acceptance criteria, a component system, content, state model, and platform behavior.

Also require source or render identity, authorization, target surfaces, supported states, decision owner, and declared unknowns where applicable.

## Procedure

1. Freeze the approved user flow, routes, roles, data states, validation rules, destructive actions, recovery behavior, and component foundation.
2. Model every control and transition including default, hover, focus, active, selected, disabled, pending, success, error, interrupted, expired, and permission-denied states as applicable.
3. Implement semantic controls, URL and history behavior, labels, inline and summary errors, confirmation, undo, idempotency cues, and safe destructive-action handling.
4. Preserve user input and context through validation, async failure, navigation, timeout, and retry where safe.
5. Verify keyboard order, focus movement, deep links, refresh/back behavior, variable content, and failure recovery; record unresolved service dependencies.

## Output Contract

Produce:
- interaction and state model
- implemented controls/forms/navigation
- state coverage matrix
- recovery verification evidence

Every material design choice, implementation claim, finding, score, capture, or disposition must link to supplied authority or current evidence, or be labeled assumption/unknown.

## UI Coverage

- `controls`
- `navigation`
- `forms`
- `loading`
- `empty`
- `error`
- `permission`
- `disabled`
- `success`
- `interruption`
- `recovery`

## Hard Gates

- The happy path cannot pass alone: every applicable loading, empty, validation, error, permission, disabled, interruption, success, and recovery state must exist and be reachable for verification.
- Preserve product truth, user task, semantic order, authentic content, accessibility, responsive behavior, state coverage, source identity, and authority boundaries where applicable.
- Return `needs-input` when an identifiable owner can supply a missing requirement, asset authority, capture, state, or decision.
- Return `blocked` when required authorization, safe mutation scope, rendered evidence, tooling, or specialist dependency is unavailable.

## Status Mapping

- `passed`: output contract and every hard gate are satisfied with current evidence.
- `needs-input`: a requestable source, state, decision, capture, or authorization term is missing.
- `blocked`: proceeding would exceed authority, mix review with repair, or rely on unavailable critical evidence.
- `failed`: authorized work ran but a deterministic gate or required output failed.

## Non-Responsibilities

Does not approve upstream product decisions, expand authority, or perform remote writes beyond its explicit permission identity.

Adjacent capabilities:
- `responsive-layout-and-spatial-composition`
- `accessibility-contracts-and-assistive-validation`
- `content-copy-and-authentic-assets`
- `purposeful-motion-and-animation-engineering`

Never perform remote Git, external-system writes, merge, deploy, release, or an adjacent capability's work. Review and preflight capabilities never repair product source; evidence-acquisition capabilities never issue design findings.
