---
name: rendered-ui-critique-and-release-disposition
description: Independently critique current rendered UI and animation behavior, prioritize reproducible findings, and recommend a bounded disposition without source mutation. Do not use for define which routes, states, viewports, traces, and tools must be captured for review or edit the product source to fix the accepted ui findings.
---

# Rendered Ui Critique And Release Disposition

## Responsibility

Independently critique current rendered UI and animation behavior, prioritize reproducible findings, and recommend a bounded disposition without source mutation.

## Trigger

Use when the requested outcome is: Independently critique current rendered UI and animation behavior, prioritize reproducible findings, and recommend a bounded disposition without source mutation.

Do not use when:
- Define which routes, states, viewports, traces, and tools must be captured for review. Route to `ui-review-scope-and-evidence-acquisition`.
- Edit the product source to fix the accepted UI findings. Route to `ui-remediation`.

## Required Inputs

- Rendered captures, interaction traces, design criteria, accessibility context, and implementation constraints.

Also require source or render identity, authorization, target surfaces, supported states, decision owner, and declared unknowns where applicable.

## Procedure

1. Verify evidence identity, recency, route, viewport, state, zoom, theme, input mode, runtime, and contract coverage before critique.
2. Review user-flow clarity, information hierarchy, typography, color, spacing, content authenticity, responsive reflow, states, accessibility signals, and animation behavior in real renders.
3. Write one reproducible finding per issue with evidence citation, affected task and state, severity, principle, consequence, and bounded repair direction.
4. Separate blockers, high-value improvements, taste choices, evidence gaps, and accepted residual risk.
5. Recommend pass, needs-repair, recapture, or blocked to the human owner; never mutate product source or perform release.

## Output Contract

Produce:
- rendered critique
- prioritized reproducible findings
- remediation hierarchy
- recapture and disposition recommendation

Every material design choice, implementation claim, finding, score, capture, or disposition must link to supplied authority or current evidence, or be labeled assumption/unknown.

## UI Coverage

- `real-renders`
- `multi-viewport`
- `interaction-traces`
- `reproducible-findings`
- `no-source-mutation`

## Hard Gates

- Static source review, DOM assertions, or a single ideal screenshot cannot substitute for current rendered evidence across the declared routes, states, viewports, input modes, and motion behavior.
- Preserve product truth, user task, semantic order, authentic content, accessibility, responsive behavior, state coverage, source identity, and authority boundaries where applicable.
- Return `needs-input` when an identifiable owner can supply a missing requirement, asset authority, capture, state, or decision.
- Return `blocked` when required authorization, safe mutation scope, rendered evidence, tooling, or specialist dependency is unavailable.

## Rendered Evidence

When this capability assesses or validates a rendered interface, static source inspection, DOM assertions, model self-attestation, or a single ideal screenshot are insufficient. Require current provenance-bound captures or traces for the declared routes, states, viewports, zoom, input modes, themes, and motion behavior. Missing evidence returns `needs-input` or `blocked`, never `passed`.

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
- `ui-review-scope-and-evidence-acquisition`
- `evidence-based-ui-review-and-release-gates`
- `ui-remediation`
- `cross-domain-ui-preflight-checklists`

Never perform remote Git, external-system writes, merge, deploy, release, or an adjacent capability's work. Review and preflight capabilities never repair product source; evidence-acquisition capabilities never issue design findings.
