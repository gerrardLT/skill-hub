---
name: purposeful-motion-and-animation-engineering
description: Implement deterministic, interruptible, reduced-motion-safe animation that communicates hierarchy, causality, navigation, feedback, or state. Do not use for choose the static visual language, typography, color, and anti-template direction or perform the final rendered animation critique and release disposition.
---

# Purposeful Motion And Animation Engineering

## Responsibility

Implement deterministic, interruptible, reduced-motion-safe animation that communicates hierarchy, causality, navigation, feedback, or state.

## Trigger

Use when the requested outcome is: Implement deterministic, interruptible, reduced-motion-safe animation that communicates hierarchy, causality, navigation, feedback, or state.

Do not use when:
- Choose the static visual language, typography, color, and anti-template direction. Route to `visual-language-and-anti-template-controls`.
- Perform the final rendered animation critique and release disposition. Route to `rendered-ui-critique-and-release-disposition`.

## Required Inputs

- Interaction states, motion intent, frequency, platform capability, and accessibility constraints.

Also require source or render identity, authorization, target surfaces, supported states, decision owner, and declared unknowns where applicable.

## Procedure

1. Freeze the communication purpose, state transition, runtime, performance budget, input behavior, and reduced-motion requirement.
2. Choose the smallest motion primitive that clarifies hierarchy, causality, continuity, progress, feedback, or navigation.
3. Implement from explicit state with deterministic timing; support interruption, rapid repeat, reverse or replacement, and cleanup.
4. Provide reduced or absent motion without losing information, order, focus, or task completion.
5. Verify slow devices, input during motion, resize, hidden tabs, route changes, reduced motion, and animation completion state.

## Output Contract

Produce:
- motion purpose map
- implemented deterministic animation
- reduced-motion behavior
- interaction and performance evidence

Every material design choice, implementation claim, finding, score, capture, or disposition must link to supplied authority or current evidence, or be labeled assumption/unknown.

## UI Coverage

- `purpose`
- `determinism`
- `interruption`
- `reduced-motion`
- `performance`
- `state`

## Hard Gates

- Motion without a named communication purpose, deterministic end state, interruption behavior, and information-equivalent reduced-motion path must be removed or blocked.
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
- `visual-language-and-anti-template-controls`
- `interaction-states-forms-and-navigation`
- `accessibility-contracts-and-assistive-validation`
- `rendered-ui-critique-and-release-disposition`

Never perform remote Git, external-system writes, merge, deploy, release, or an adjacent capability's work. Review and preflight capabilities never repair product source; evidence-acquisition capabilities never issue design findings.
