---
name: existing-interface-redesign-and-preservation
description: "Audit an existing interface and define a redesign preservation contract for product truth, user flow, information architecture, routes, SEO, analytics, behavior, and content. Use when An existing product or site is being redesigned and must keep its routes, SEO, analytics and user tasks working; Someone asks what in the current interface must be preserved, migrated, replaced or removed, and who decides. Do not use for: Choose a visual direction for a new interface with no existing product behavior to preserve (-> design-context-and-direction-contract); Apply accepted redesign fixes to product source after review (-> ui-remediation)."
---

# Existing Interface Redesign And Preservation

## Responsibility

Audit an existing interface and define a redesign preservation contract for product truth, user flow, information architecture, routes, SEO, analytics, behavior, and content.

## Trigger

Use when the request matches any of:
- An existing product or site is being redesigned and must keep its routes, SEO, analytics and user tasks working
- Someone asks what in the current interface must be preserved, migrated, replaced or removed, and who decides

Do not use when:
- Choose a visual direction for a new interface with no existing product behavior to preserve. Route to `design-context-and-direction-contract`.
- Apply accepted redesign fixes to product source after review. Route to `ui-remediation`.

## Required Inputs

- An existing UI, brand, tokens, information architecture, content, routes, analytics, and redesign brief.

## Procedure

1. Classify the mode (greenfield, redesign that preserves behavior, or approved overhaul) and state the evidence for it.
2. Freeze the redesign brief and inspect authorized current routes, content, components, analytics, SEO metadata, accessibility behavior, and known business invariants.
3. Separate verified product truth from visual debt, implementation accident, unknown dependency, and explicitly removable behavior.
4. Map current user flows, information architecture, deep links, forms, state transitions, tracking, and search or sharing contracts.
5. Define preserve, migrate, replace, and remove decisions with owner, rationale, tests, and rollback or compatibility needs.
6. Sequence a reversible migration and hand off constraints to design direction; do not redesign or repair source in this audit.

## Domain Guidance

- Step 1 is mode classification: greenfield (no existing behavior to keep), redesign that preserves behavior, or an approved full overhaul. Misclassifying the mode is the largest source of bad redesign output; state the mode and the evidence for it.

## Output Contract

Produce:
- current-state UI audit
- preservation and migration contract
- invariant test map
- redesign risk ledger

Every material design choice, implementation claim, finding, score, capture, or disposition must link to supplied authority or current evidence, or be labeled assumption/unknown.

Deliver each output as the artifact itself (tables, commands, patches, plans, records), not as a description of how it would be produced.

## UI Coverage

- `preservation`
- `user-flow`
- `information-architecture`
- `SEO`
- `analytics`
- `behavior`
- `migration`

## Hard Gates

- No existing route, content obligation, analytics event, SEO contract, user task, or behavior may be silently removed because it appears visually obsolete.
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
- `ui-task-routing-and-governance`
- `ui-remediation`
- `rendered-ui-critique-and-release-disposition`

Never perform remote Git, external-system writes, merge, deploy, release, or an adjacent capability's work. Review and preflight capabilities never repair product source; evidence-acquisition capabilities never issue design findings.
