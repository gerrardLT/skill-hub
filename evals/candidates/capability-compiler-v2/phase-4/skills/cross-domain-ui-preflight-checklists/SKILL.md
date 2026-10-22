---
name: cross-domain-ui-preflight-checklists
description: Run one bounded preflight across accessibility, authentic content, interaction states, responsiveness, motion, AI states, and release evidence without repairing source. Do not use for capture the missing browser renders and interaction traces required for review or apply the approved fixes to product source after the findings are accepted.
---

# Cross Domain Ui Preflight Checklists

## Responsibility

Run one bounded preflight across accessibility, authentic content, interaction states, responsiveness, motion, AI states, and release evidence without repairing source.

## Trigger

Use when the requested outcome is: Run one bounded preflight across accessibility, authentic content, interaction states, responsiveness, motion, AI states, and release evidence without repairing source.

Do not use when:
- Capture the missing browser renders and interaction traces required for review. Route to `ui-review-scope-and-evidence-acquisition`.
- Apply the approved fixes to product source after the findings are accepted. Route to `ui-remediation`.

## Required Inputs

- A rendered UI, acceptance criteria, content, supported devices, and release boundary.

Also require source or render identity, authorization, target surfaces, supported states, decision owner, and declared unknowns where applicable.

## Procedure

1. Freeze acceptance criteria, supported surfaces, applicable UI domains, release boundary, and current evidence manifest.
2. Select only applicable checks and state why any domain is not applicable.
3. Verify required states, widths, zoom, input modes, assistive behavior, motion reduction, content provenance, and AI uncertainty against cited evidence.
4. Classify findings by severity, reproducibility, affected task, owner, and evidence needed to close.
5. Stop on blocking gaps and route missing capture or authorized remediation; never mark a checklist item passed from assertion alone.

## Output Contract

Produce:
- UI preflight result
- blocking-finding register
- evidence-gap list
- residual-risk summary

Every material design choice, implementation claim, finding, score, capture, or disposition must link to supplied authority or current evidence, or be labeled assumption/unknown.

## UI Coverage

- `cross-domain-preflight`
- `current-evidence`
- `blocking-findings`
- `residual-risk`

## Hard Gates

- A preflight item passes only with current criterion-linked evidence; unchecked, not-applicable without rationale, and source-inspection-only items remain unresolved.
- Preserve product truth, user task, semantic order, authentic content, accessibility, responsive behavior, state coverage, source identity, and authority boundaries where applicable.
- Return `needs-input` when an identifiable owner can supply a missing requirement, asset authority, capture, state, or decision.
- Return `blocked` when required authorization, safe mutation scope, rendered evidence, tooling, or specialist dependency is unavailable.

## Rendered Evidence

When this capability assesses or validates a rendered interface, static source inspection, DOM assertions, model self-attestation, or a single ideal screenshot are insufficient. Require current provenance-bound captures or traces for the declared routes, states, viewports, zoom, input modes, themes, and motion behavior. Missing evidence returns `needs-input` or `blocked`, never `passed`.

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
- `accessibility-contracts-and-assistive-validation`

Never perform remote Git, external-system writes, merge, deploy, release, or an adjacent capability's work. Review and preflight capabilities never repair product source; evidence-acquisition capabilities never issue design findings.
