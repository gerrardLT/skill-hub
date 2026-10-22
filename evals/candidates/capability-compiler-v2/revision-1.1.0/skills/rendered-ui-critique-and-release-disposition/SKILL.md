---
name: rendered-ui-critique-and-release-disposition
description: "Independently critique current rendered UI and animation behavior and prioritize reproducible findings; recommend recapture or hand the findings to the release gate, without issuing the release disposition or mutating source. Use when Current rendered captures and traces exist and someone needs a critique with reproducible, prioritized findings; A UI review needs blockers separated from improvements, taste choices and evidence gaps. Do not use for: Define which routes, states, viewports, traces, and tools must be captured for review (-> ui-review-scope-and-evidence-acquisition); Edit the product source to fix the accepted UI findings (-> ui-remediation)."
---

# Rendered UI Critique And Release Disposition

## Responsibility

Independently critique current rendered UI and animation behavior and prioritize reproducible findings; recommend recapture or hand the findings to the release gate, without issuing the release disposition or mutating source.

## Trigger

Use when the request matches any of:
- Current rendered captures and traces exist and someone needs a critique with reproducible, prioritized findings
- A UI review needs blockers separated from improvements, taste choices and evidence gaps

Do not use when:
- Define which routes, states, viewports, traces, and tools must be captured for review. Route to `ui-review-scope-and-evidence-acquisition`.
- Edit the product source to fix the accepted UI findings. Route to `ui-remediation`.

## Required Inputs

- Rendered captures, interaction traces, design criteria, accessibility context, and implementation constraints.

## Procedure

1. Verify evidence identity, recency, route, viewport, state, zoom, theme, input mode, runtime, and contract coverage before critique.
2. Review user-flow clarity, information hierarchy, typography, color, spacing, content authenticity, responsive reflow, states, accessibility signals, and animation behavior in real renders.
3. Write one reproducible finding per issue with evidence citation, affected task and state, severity, principle, consequence, and bounded repair direction.
4. Separate blockers, high-value improvements, taste choices, evidence gaps, and accepted residual risk.
5. Recommend pass, needs-repair, recapture, or blocked to the human owner; never mutate product source or perform release.

## Domain Guidance

- Audit categories: visual hierarchy and composition, typography, color and contrast, spacing and layout, interaction states, responsive reflow, motion, content and copy, accessibility signals, and perceived performance. Rate each finding high, medium or polish impact and give a category.
- The release disposition belongs to evidence-based-ui-review-and-release-gates; this Skill ends with the prioritized findings and a recapture need.
- Boundary: this Skill produces prioritized findings from rendered evidence; applying explicit release criteria and the final disposition recommendation belong to evidence-based-ui-review-and-release-gates.

## Output Contract

Produce:
- rendered critique
- prioritized reproducible findings
- remediation hierarchy
- recapture recommendation and release-gate handoff

Every material design choice, implementation claim, finding, score, capture, or disposition must link to supplied authority or current evidence, or be labeled assumption/unknown.

Deliver each output as the artifact itself (tables, commands, patches, plans, records), not as a description of how it would be produced.

## UI Coverage

- `real-renders`
- `multi-viewport`
- `interaction-traces`
- `reproducible-findings`
- `no-source-mutation`

## Hard Gates

- Static source review, DOM assertions, or a single ideal screenshot cannot substitute for current rendered evidence across the declared routes, states, viewports, input modes, and motion behavior.
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

## Human Design Authority

The Skill may preserve evidence, alternatives, tradeoffs, findings, and a recommendation. Final taste selection, prototype promotion, accepted risk, scope approval, source-repair approval, and release disposition remain explicit human decisions with a named owner.

## Status Mapping

- `passed`: output contract and every hard gate are satisfied with current evidence.
- `needs-input`: a requestable source, state, decision, capture, or authorization term is missing. Deliver every supported part first and name the owner for the missing part.
- `blocked`: proceeding would exceed authority, mix review with repair, or rely on unavailable critical evidence.
- `failed`: authorized work ran but a deterministic gate or required output failed.

## Non-Responsibilities

Adjacent capabilities:
- `ui-review-scope-and-evidence-acquisition`
- `evidence-based-ui-review-and-release-gates`
- `ui-remediation`

Never perform remote Git, external-system writes, merge, deploy, release, or an adjacent capability's work. Review and preflight capabilities never repair product source; evidence-acquisition capabilities never issue design findings.
