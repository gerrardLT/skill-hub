---
name: ui-review-scope-and-evidence-acquisition
description: "Define independent UI review scope and acquire authorized current rendered evidence without evaluating findings or repairing source. Use when A UI review needs a scope matrix and provenance-bound captures before anyone judges the design; Someone asks which routes, states, viewports and input modes must be captured and whether the evidence is complete. Do not use for: Critique the completed capture set and prioritize UI defects (-> rendered-ui-critique-and-release-disposition); Modify product source in response to previously accepted findings (-> ui-remediation)."
---

# UI Review Scope And Evidence Acquisition

## Responsibility

Define independent UI review scope and acquire authorized current rendered evidence without evaluating findings or repairing source.

## Trigger

Use when the request matches any of:
- A UI review needs a scope matrix and provenance-bound captures before anyone judges the design
- Someone asks which routes, states, viewports and input modes must be captured and whether the evidence is complete

Do not use when:
- Critique the completed capture set and prioritize UI defects. Route to `rendered-ui-critique-and-release-disposition`.
- Modify product source in response to previously accepted findings. Route to `ui-remediation`.

## Required Inputs

- A UI brief, target files, runtime, rendered surfaces, and review criteria.

## Procedure

1. Freeze changed surfaces, user tasks, acceptance criteria, supported browsers and devices, high-risk states, source identity, and review independence.
2. Build a route-state-viewport-theme-input-motion matrix with explicit inclusions, exclusions, and rationale.
3. Use only approved local commands and authorized external reads to capture screenshots, traces, recordings, accessibility snapshots, and console or network evidence.
4. Bind each artifact to timestamp, source revision, environment, route, state setup, viewport, zoom, input mode, theme, tool, and hash.
5. Assess evidence completeness only; route a complete manifest to critique or return needs-input/blocked without judging design quality.

## Domain Guidance

- Unknown capture commands are proposed, not executed: map project markers to a candidate command and offer it; run only commands already approved.
- Capture dedicated views for state-specific content (for example a discounted price in each viewport), not only the default state.
- When a captured artifact shows a measurable defect, record it as a routed observation with its evidence (for example a computed contrast ratio against the 4.5:1 and 3:1 thresholds) and send it to rendered-ui-critique-and-release-disposition. Do not judge design quality and do not withhold the observation.

## Output Contract

Produce:
- UI review scope matrix
- rendered evidence bundle
- capture provenance manifest
- evidence completeness result
- routed observations with evidence, forwarded to critique

Every material design choice, implementation claim, finding, score, capture, or disposition must link to supplied authority or current evidence, or be labeled assumption/unknown.

Deliver each output as the artifact itself (tables, commands, patches, plans, records), not as a description of how it would be produced.

## UI Coverage

- `scope-matrix`
- `capture`
- `provenance`
- `current-evidence`
- `independence`
- `no-critique`

## Hard Gates

- No capture is review evidence unless its source revision, runtime, route, state, viewport, zoom or scale, input mode, timestamp, tool, and hash are recorded and current.
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
- `rendered-ui-critique-and-release-disposition`
- `evidence-based-ui-review-and-release-gates`
- `ui-remediation`

Never perform remote Git, external-system writes, merge, deploy, release, or an adjacent capability's work. Review and preflight capabilities never repair product source; evidence-acquisition capabilities never issue design findings.
