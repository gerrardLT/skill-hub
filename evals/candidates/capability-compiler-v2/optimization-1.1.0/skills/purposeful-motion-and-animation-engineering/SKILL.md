---
name: purposeful-motion-and-animation-engineering
description: "Implement deterministic, interruptible, reduced-motion-safe animation that communicates hierarchy, causality, navigation, feedback, or state. Use when A transition or animation must communicate hierarchy, causality or feedback and remain safe for reduced-motion users; Someone asks for interruptible, deterministic motion that does not drop frames. Do not use for: Choose the static visual language, typography, color, and anti-template direction (-> visual-language-and-anti-template-controls); Perform the final rendered animation critique and release disposition (-> rendered-ui-critique-and-release-disposition)."
---

# Purposeful Motion And Animation Engineering

## Responsibility

Implement deterministic, interruptible, reduced-motion-safe animation that communicates hierarchy, causality, navigation, feedback, or state.

## Trigger

Use when the request matches any of:
- A transition or animation must communicate hierarchy, causality or feedback and remain safe for reduced-motion users
- Someone asks for interruptible, deterministic motion that does not drop frames

Do not use when:
- Choose the static visual language, typography, color, and anti-template direction. Route to `visual-language-and-anti-template-controls`.
- Perform the final rendered animation critique and release disposition. Route to `rendered-ui-critique-and-release-disposition`.

## Required Inputs

- Interaction states, motion intent, frequency, platform capability, and accessibility constraints.

## Procedure

1. Freeze the communication purpose, state transition, runtime, performance budget, input behavior, and reduced-motion requirement.
2. Choose the smallest motion primitive that clarifies hierarchy, causality, continuity, progress, feedback, or navigation.
3. Implement from explicit state with deterministic timing; support interruption, rapid repeat, reverse or replacement, and cleanup.
4. Provide reduced or absent motion without losing information, order, focus, or task completion.
5. Verify slow devices, input during motion, resize, hidden tabs, route changes, reduced motion, and animation completion state.

## Domain Guidance

- Default implementation rule: animate only transform and opacity, which skip layout and paint. Animating width, height, top, left, padding or margin triggers layout. Set transform directly on the element instead of driving children through a parent CSS variable.
- Choose shared duration tokens by distance and context and verify that feedback stays responsive rather than treating one duration as universal.
- When reduced motion disables transitions, commit final open/closed state synchronously; never wait for transitionend that will not fire. Restore focus after close. For animated mode handle interrupted transitions and ensure entrance start and end values differ. Assess flashing against the three-flashes-per-second safety threshold, including applicable area/luminance conditions; do not approve an unverified 4 Hz flash.

## Output Contract

Produce:
- motion purpose map
- implemented deterministic animation
- reduced-motion behavior
- interaction and performance evidence

Every material design choice, implementation claim, finding, score, capture, or disposition must link to supplied authority or current evidence, or be labeled assumption/unknown.

Deliver each output as the artifact itself (tables, commands, patches, plans, records), not as a description of how it would be produced.

## UI Coverage

- `purpose`
- `determinism`
- `interruption`
- `reduced-motion`
- `performance`
- `state`

## Hard Gates

- Motion without a named communication purpose, deterministic end state, interruption behavior, and information-equivalent reduced-motion path must be removed or blocked.
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
- `visual-language-and-anti-template-controls`
- `interaction-states-forms-and-navigation`
- `accessibility-contracts-and-assistive-validation`
- `rendered-ui-critique-and-release-disposition`

Never perform remote Git, external-system writes, merge, deploy, release, or an adjacent capability's work. Review and preflight capabilities never repair product source; evidence-acquisition capabilities never issue design findings.
