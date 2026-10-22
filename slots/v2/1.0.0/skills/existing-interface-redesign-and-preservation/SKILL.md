---
name: existing-interface-redesign-and-preservation
description: Audit an existing interface and define a redesign preservation contract for product truth, user flow, information architecture, routes, SEO, analytics, behavior, and content. Do not use for choose a visual direction for a new interface with no existing product behavior to preserve or apply accepted redesign fixes to product source after review.
---

# Existing Interface Redesign And Preservation

## Responsibility

Audit an existing interface and define a redesign preservation contract for product truth, user flow, information architecture, routes, SEO, analytics, behavior, and content.

## Trigger

Use when the requested outcome is: Audit an existing interface and define a redesign preservation contract for product truth, user flow, information architecture, routes, SEO, analytics, behavior, and content.

Do not use when:
- Choose a visual direction for a new interface with no existing product behavior to preserve. Route to `design-context-and-direction-contract`.
- Apply accepted redesign fixes to product source after review. Route to `ui-remediation`.

## Required Inputs

- An existing UI, brand, tokens, information architecture, content, routes, analytics, and redesign brief.

Also require source or render identity, authorization, target surfaces, supported states, decision owner, and declared unknowns where applicable.

## Procedure

1. Freeze the redesign brief and inspect authorized current routes, content, components, analytics, SEO metadata, accessibility behavior, and known business invariants.
2. Separate verified product truth from visual debt, implementation accident, unknown dependency, and explicitly removable behavior.
3. Map current user flows, information architecture, deep links, forms, state transitions, tracking, and search or sharing contracts.
4. Define preserve, migrate, replace, and remove decisions with owner, rationale, tests, and rollback or compatibility needs.
5. Sequence a reversible migration and hand off constraints to design direction; do not redesign or repair source in this audit.

## Output Contract

Produce:
- current-state UI audit
- preservation and migration contract
- invariant test map
- redesign risk ledger

Every material design choice, implementation claim, finding, score, capture, or disposition must link to supplied authority or current evidence, or be labeled assumption/unknown.

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
- `design-context-and-direction-contract`
- `ui-task-routing-and-governance`
- `ui-remediation`
- `rendered-ui-critique-and-release-disposition`

Never perform remote Git, external-system writes, merge, deploy, release, or an adjacent capability's work. Review and preflight capabilities never repair product source; evidence-acquisition capabilities never issue design findings.
