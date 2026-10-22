---
name: visual-language-and-anti-template-controls
description: "Establish and implement a purposeful visual language that reinforces hierarchy and brand evidence while rejecting generic template patterns and unsupported decoration. Use when An interface needs a deliberate visual language for type, color, shape and emphasis that stays tied to brand evidence; Someone asks to remove generic template patterns and unsupported decoration from a design. Do not use for: Define page-level grid, responsive reflow, and spatial density across widths (-> responsive-layout-and-spatial-composition); Write the truthful product copy, realistic records, and authorized assets (-> content-copy-and-authentic-assets); Decide the overall design direction, flow and hierarchy (-> design-context-and-direction-contract)."
---

# Visual Language And Anti Template Controls

## Responsibility

Establish and implement a purposeful visual language that reinforces hierarchy and brand evidence while rejecting generic template patterns and unsupported decoration.

## Trigger

Use when the request matches any of:
- An interface needs a deliberate visual language for type, color, shape and emphasis that stays tied to brand evidence
- Someone asks to remove generic template patterns and unsupported decoration from a design

Do not use when:
- Define page-level grid, responsive reflow, and spatial density across widths. Route to `responsive-layout-and-spatial-composition`.
- Write the truthful product copy, realistic records, and authorized assets. Route to `content-copy-and-authentic-assets`.
- Decide the overall design direction, flow and hierarchy. Route to `design-context-and-direction-contract`.

## Required Inputs

- A direction contract, brand, tokens, audience, surface mode, and content.

## Procedure

1. Freeze the design contract, brand evidence, authentic content, accessibility constraints, existing system, and explicit anti-goals.
2. Name a small visual thesis and map typography, color, shape, border, surface, imagery, icon, and emphasis roles to it.
3. Audit and remove generic hero, card-grid, gradient, pill, floating-panel, decorative-chart, and icon patterns that lack task or brand purpose.
4. Implement reusable visual rules through the existing token and component foundation rather than one-off styling.
5. Stress hierarchy, contrast, dense and sparse content, themes, and states; preserve human-owned taste alternatives when evidence cannot decide.

## Domain Guidance

- Tells to avoid unless the brief earns them: neon or outer glows, pure black (#000000), oversaturated accents, same-size icon-heading-text card grids as page structure, gradient heroes, floating pill clusters, and decorative charts. A brief that asks for one can earn it; otherwise say what replaced it.
- When a color or type value is contested, give provisional roles with the owner named, offer local preparation of the change for review, state the fallback font stack, and give concrete sizes and touch targets. Keep contested values non-final until the owner decides.

## Output Contract

Produce:
- visual-language specification
- implemented visual grammar
- anti-template audit
- taste-decision register

Every material design choice, implementation claim, finding, score, capture, or disposition must link to supplied authority or current evidence, or be labeled assumption/unknown.

Deliver each output as the artifact itself (tables, commands, patches, plans, records), not as a description of how it would be produced.

## UI Coverage

- `typography`
- `color`
- `shape`
- `hierarchy`
- `brand`
- `anti-template`
- `accessibility`

## Hard Gates

- Every prominent visual device must serve hierarchy, task, content, state, or evidenced brand identity; unsupported decoration and generic template motifs must be removed.
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
- `design-context-and-direction-contract`
- `design-system-foundation-and-token-extraction`
- `responsive-layout-and-spatial-composition`
- `content-copy-and-authentic-assets`

Never perform remote Git, external-system writes, merge, deploy, release, or an adjacent capability's work. Review and preflight capabilities never repair product source; evidence-acquisition capabilities never issue design findings.
