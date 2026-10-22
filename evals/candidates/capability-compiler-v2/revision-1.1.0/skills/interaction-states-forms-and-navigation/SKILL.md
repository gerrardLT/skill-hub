---
name: interaction-states-forms-and-navigation
description: "Define and implement coherent controls, navigation, forms, validation, loading, empty, error, permission, disabled, success, interruption, and recovery states. Use when A form, flow or navigation needs every control state and failure recovery defined and implemented; Someone asks what happens on validation error, timeout, permission denial, refresh or back navigation. Do not use for: Specify the assistive-technology acceptance and test matrix for the completed interaction (-> accessibility-contracts-and-assistive-validation); Choose the page-level visual hierarchy, grid, density, and breakpoint composition (-> responsive-layout-and-spatial-composition)."
---

# Interaction States Forms And Navigation

## Responsibility

Define and implement coherent controls, navigation, forms, validation, loading, empty, error, permission, disabled, success, interruption, and recovery states.

## Trigger

Use when the request matches any of:
- A form, flow or navigation needs every control state and failure recovery defined and implemented
- Someone asks what happens on validation error, timeout, permission denial, refresh or back navigation

Do not use when:
- Specify the assistive-technology acceptance and test matrix for the completed interaction. Route to `accessibility-contracts-and-assistive-validation`.
- Choose the page-level visual hierarchy, grid, density, and breakpoint composition. Route to `responsive-layout-and-spatial-composition`.

## Required Inputs

- User flows, acceptance criteria, a component system, content, state model, and platform behavior.

## Procedure

1. Freeze the approved user flow, routes, roles, data states, validation rules, destructive actions, recovery behavior, and component foundation.
2. Model every control and transition including default, hover, focus, active, selected, disabled, pending, success, error, interrupted, expired, and permission-denied states as applicable.
3. Implement semantic controls, URL and history behavior, labels, inline and summary errors, confirmation, undo, idempotency cues, and safe destructive-action handling.
4. Preserve user input and context through validation, async failure, navigation, timeout, and retry where safe.
5. Verify keyboard order, focus movement, deep links, refresh/back behavior, variable content, and failure recovery; record unresolved service dependencies.

## Domain Guidance

- Default target size: at least 44 by 44 pt (Apple) or 48 by 48 dp (Material), with at least 8 px between targets; extend the hit area beyond the visible bounds when needed. Never rely on hover alone for a primary action.
- During verification capture console errors for each flow, keyboard order and focus movement, and deep-link, refresh and back behavior.

## Output Contract

Produce:
- interaction and state model
- implemented controls/forms/navigation
- state coverage matrix
- recovery verification evidence

Every material design choice, implementation claim, finding, score, capture, or disposition must link to supplied authority or current evidence, or be labeled assumption/unknown.

Deliver each output as the artifact itself (tables, commands, patches, plans, records), not as a description of how it would be produced.

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
- `responsive-layout-and-spatial-composition`
- `accessibility-contracts-and-assistive-validation`
- `content-copy-and-authentic-assets`
- `purposeful-motion-and-animation-engineering`

Never perform remote Git, external-system writes, merge, deploy, release, or an adjacent capability's work. Review and preflight capabilities never repair product source; evidence-acquisition capabilities never issue design findings.
