---
name: design-system-foundation-and-token-extraction
description: "Choose or generate an in-project design-system foundation with semantic tokens, component contracts, states, themes, and persistence rules. Use when A project needs semantic tokens, component contracts and theme rules, or needs to confirm its existing system already covers a new need; Someone asks for candidate token and theme files with a change table and version. Do not use for: Extract primitives from this external authorized site without writing project tokens (-> external-design-token-extraction-and-normalization); Define the page-level responsive composition and reflow behavior (-> responsive-layout-and-spatial-composition)."
---

# Design System Foundation And Token Extraction

## Responsibility

Choose or generate an in-project design-system foundation with semantic tokens, component contracts, states, themes, and persistence rules.

## Trigger

Use when the request matches any of:
- A project needs semantic tokens, component contracts and theme rules, or needs to confirm its existing system already covers a new need
- Someone asks for candidate token and theme files with a change table and version

Do not use when:
- Extract primitives from this external authorized site without writing project tokens. Route to `external-design-token-extraction-and-normalization`.
- Define the page-level responsive composition and reflow behavior. Route to `responsive-layout-and-spatial-composition`.

## Required Inputs

- A UI brief, stack, design references, existing tokens, and project conventions.

## Procedure

1. Inventory existing tokens, components, CSS conventions, dependencies, themes, and approved design direction before adding anything.
2. Reuse the project foundation where sufficient; add only semantic color, type, spacing, radius, elevation, motion, and layout tokens required by real states.
3. Define component anatomy, variants, sizes, content bounds, interaction states, accessibility behavior, and composition rules.
4. Map raw or imported values to semantic roles with provenance; prohibit one-off values unless recorded as an exception.
5. Persist the smallest working foundation and verify representative components across themes and states.

## Domain Guidance

- Reuse first: inventory the existing tokens and components and show which required states they already express. Add a token only for a real state the foundation cannot express.
- Prefer the official package when the brief matches a known design system (component library or platform guidelines) rather than inventing CSS for it.
- When approval is still pending, still produce candidate token and theme files labelled pending, with a change table, a version rationale and a checked contrast figure; never persist them as approved and name the approver.

## Output Contract

Produce:
- semantic token set
- component contract catalog
- theme and state rules
- persistence and exception ledger
- candidate token and theme files labelled pending approval, with change table and version rationale

Every material design choice, implementation claim, finding, score, capture, or disposition must link to supplied authority or current evidence, or be labeled assumption/unknown.

Deliver each output as the artifact itself (tables, commands, patches, plans, records), not as a description of how it would be produced.

## UI Coverage

- `semantic-tokens`
- `component-contracts`
- `states`
- `themes`
- `persistence`
- `provenance`

## Hard Gates

- Do not create a parallel design system, token alias maze, or component abstraction when the existing project foundation can express the required states.
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
- `external-design-token-extraction-and-normalization`
- `visual-language-and-anti-template-controls`
- `responsive-layout-and-spatial-composition`
- `interaction-states-forms-and-navigation`

Never perform remote Git, external-system writes, merge, deploy, release, or an adjacent capability's work. Review and preflight capabilities never repair product source; evidence-acquisition capabilities never issue design findings.
