---
name: design-system-foundation-and-token-extraction
description: Choose or generate an in-project design-system foundation with semantic tokens, component contracts, states, themes, and persistence rules. Do not use for extract primitives from this external authorized site without writing project tokens or define the page-level responsive composition and reflow behavior.
---

# Design System Foundation And Token Extraction

## Responsibility

Choose or generate an in-project design-system foundation with semantic tokens, component contracts, states, themes, and persistence rules.

## Trigger

Use when the requested outcome is: Choose or generate an in-project design-system foundation with semantic tokens, component contracts, states, themes, and persistence rules.

Do not use when:
- Extract primitives from this external authorized site without writing project tokens. Route to `external-design-token-extraction-and-normalization`.
- Define the page-level responsive composition and reflow behavior. Route to `responsive-layout-and-spatial-composition`.

## Required Inputs

- A UI brief, stack, design references, existing tokens, and project conventions.

Also require source or render identity, authorization, target surfaces, supported states, decision owner, and declared unknowns where applicable.

## Procedure

1. Inventory existing tokens, components, CSS conventions, dependencies, themes, and approved design direction before adding anything.
2. Reuse the project foundation where sufficient; add only semantic color, type, spacing, radius, elevation, motion, and layout tokens required by real states.
3. Define component anatomy, variants, sizes, content bounds, interaction states, accessibility behavior, and composition rules.
4. Map raw or imported values to semantic roles with provenance; prohibit one-off values unless recorded as an exception.
5. Persist the smallest working foundation and verify representative components across themes and states.

## Output Contract

Produce:
- semantic token set
- component contract catalog
- theme and state rules
- persistence and exception ledger

Every material design choice, implementation claim, finding, score, capture, or disposition must link to supplied authority or current evidence, or be labeled assumption/unknown.

## UI Coverage

- `semantic-tokens`
- `component-contracts`
- `states`
- `themes`
- `persistence`
- `provenance`

## Hard Gates

- Do not create a parallel design system, token alias maze, or component abstraction when the existing project foundation can express the required states.
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
- `external-design-token-extraction-and-normalization`
- `visual-language-and-anti-template-controls`
- `responsive-layout-and-spatial-composition`
- `interaction-states-forms-and-navigation`

Never perform remote Git, external-system writes, merge, deploy, release, or an adjacent capability's work. Review and preflight capabilities never repair product source; evidence-acquisition capabilities never issue design findings.
