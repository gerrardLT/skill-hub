---
name: design-context-and-direction-contract
description: Translate approved product behavior, audience, brand evidence, surface mode, content needs, and success criteria into an auditable design direction contract. Do not use for implement the responsive layouts and component source from an approved direction or independently critique the rendered implementation and issue a release recommendation.
---

# Design Context And Direction Contract

## Responsibility

Translate approved product behavior, audience, brand evidence, surface mode, content needs, and success criteria into an auditable design direction contract.

## Trigger

Use when the requested outcome is: Translate approved product behavior, audience, brand evidence, surface mode, content needs, and success criteria into an auditable design direction contract.

Do not use when:
- Implement the responsive layouts and component source from an approved direction. Route to `responsive-layout-and-spatial-composition`.
- Independently critique the rendered implementation and issue a release recommendation. Route to `rendered-ui-critique-and-release-disposition`.

## Required Inputs

- Product facts, a brief, design assets, tokens, components, surface context, and references.

Also require source or render identity, authorization, target surfaces, supported states, decision owner, and declared unknowns where applicable.

## Procedure

1. Classify product facts, acceptance criteria, audience evidence, brand assets, existing tokens, platform constraints, references, conflicts, and unknowns.
2. Choose the surface mode and state the user flow, information hierarchy, content priorities, and success criteria before visual styling.
3. Derive a spatial thesis, density, typography role, color role, imagery or icon direction, and interaction tone from cited authority.
4. Separate required constraints, reversible proposals, unresolved taste decisions, and forbidden unsupported decoration.
5. Emit a contract with invariants, target surfaces, decision owners, and handoff gates; do not implement or approve release.

## Output Contract

Produce:
- design evidence read
- user-flow and information-hierarchy contract
- visual and spatial direction
- design decision ledger

Every material design choice, implementation claim, finding, score, capture, or disposition must link to supplied authority or current evidence, or be labeled assumption/unknown.

## UI Coverage

- `user-flow`
- `information-hierarchy`
- `brand-authority`
- `spatial-thesis`
- `success-criteria`
- `taste-decision`

## Hard Gates

- The design direction cannot pass unless each major visual or spatial choice traces to product purpose, audience, content, brand authority, or an explicitly human-owned taste decision.
- Preserve product truth, user task, semantic order, authentic content, accessibility, responsive behavior, state coverage, source identity, and authority boundaries where applicable.
- Return `needs-input` when an identifiable owner can supply a missing requirement, asset authority, capture, state, or decision.
- Return `blocked` when required authorization, safe mutation scope, rendered evidence, tooling, or specialist dependency is unavailable.

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
- `ui-task-routing-and-governance`
- `visual-language-and-anti-template-controls`
- `responsive-layout-and-spatial-composition`
- `rendered-ui-critique-and-release-disposition`

Never perform remote Git, external-system writes, merge, deploy, release, or an adjacent capability's work. Review and preflight capabilities never repair product source; evidence-acquisition capabilities never issue design findings.
