---
name: design-context-and-direction-contract
description: "Translate approved product behavior, audience, brand evidence, surface mode, content needs, and success criteria into an auditable design direction contract. Use when A new or approved-redesign interface needs a design direction tied to product behavior, audience and brand evidence; Someone asks for user flow, hierarchy, spatial and visual decisions with the authority behind each choice. Do not use for: Implement the responsive layouts and component source from an approved direction (-> responsive-layout-and-spatial-composition); Independently critique the rendered implementation and issue a release recommendation (-> rendered-ui-critique-and-release-disposition); Implement the visual grammar, type, color and anti-template rules (-> visual-language-and-anti-template-controls)."
---

# Design Context And Direction Contract

## Responsibility

Translate approved product behavior, audience, brand evidence, surface mode, content needs, and success criteria into an auditable design direction contract.

## Trigger

Use when the request matches any of:
- A new or approved-redesign interface needs a design direction tied to product behavior, audience and brand evidence
- Someone asks for user flow, hierarchy, spatial and visual decisions with the authority behind each choice

Do not use when:
- Implement the responsive layouts and component source from an approved direction. Route to `responsive-layout-and-spatial-composition`.
- Independently critique the rendered implementation and issue a release recommendation. Route to `rendered-ui-critique-and-release-disposition`.
- Implement the visual grammar, type, color and anti-template rules. Route to `visual-language-and-anti-template-controls`.

## Required Inputs

- Product facts, a brief, design assets, tokens, components, surface context, and references.

## Procedure

1. Classify product facts, acceptance criteria, audience evidence, brand assets, existing tokens, platform constraints, references, conflicts, and unknowns.
2. Choose the surface mode and state the user flow, information hierarchy, content priorities, and success criteria before visual styling.
3. Derive a spatial thesis, density, typography role, color role, imagery or icon direction, and interaction tone from cited authority.
4. Separate required constraints, reversible proposals, unresolved taste decisions, and forbidden unsupported decoration.
5. Emit a contract with invariants, target surfaces, decision owners, and handoff gates; do not implement or approve release.

## Domain Guidance

- Intake in one consolidated question that pre-fills what the codebase and assets already show (product, audience, project type, existing patterns, constraints); ask only for what cannot be inferred.
- Make the spatial thesis concrete: derive a width budget, column structure, padding and density from the supplied content and viewports, with the numbers shown, instead of deferring exact values.
- State the sort order and severity ordering that drive hierarchy (for example critical first), and trace each major choice to product purpose, audience, content or brand authority; untraceable choices are listed as taste decisions for the owner.

## Output Contract

Produce:
- design evidence read
- user-flow and information-hierarchy contract
- visual and spatial direction
- design decision ledger

Every material design choice, implementation claim, finding, score, capture, or disposition must link to supplied authority or current evidence, or be labeled assumption/unknown.

Deliver each output as the artifact itself (tables, commands, patches, plans, records), not as a description of how it would be produced.

## UI Coverage

- `user-flow`
- `information-hierarchy`
- `brand-authority`
- `spatial-thesis`
- `success-criteria`
- `taste-decision`

## Hard Gates

- The design direction cannot pass unless each major visual or spatial choice traces to product purpose, audience, content, brand authority, or an explicitly human-owned taste decision.
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

## Human Design Authority

The Skill may preserve evidence, alternatives, tradeoffs, findings, and a recommendation. Final taste selection, prototype promotion, accepted risk, scope approval, source-repair approval, and release disposition remain explicit human decisions with a named owner.

## Status Mapping

- `passed`: output contract and every hard gate are satisfied with current evidence.
- `needs-input`: a requestable source, state, decision, capture, or authorization term is missing. Deliver every supported part first and name the owner for the missing part.
- `blocked`: proceeding would exceed authority, mix review with repair, or rely on unavailable critical evidence.
- `failed`: authorized work ran but a deterministic gate or required output failed.

## Non-Responsibilities

Adjacent capabilities:
- `ui-task-routing-and-governance`
- `visual-language-and-anti-template-controls`
- `responsive-layout-and-spatial-composition`
- `rendered-ui-critique-and-release-disposition`

Never perform remote Git, external-system writes, merge, deploy, release, or an adjacent capability's work. Review and preflight capabilities never repair product source; evidence-acquisition capabilities never issue design findings.
