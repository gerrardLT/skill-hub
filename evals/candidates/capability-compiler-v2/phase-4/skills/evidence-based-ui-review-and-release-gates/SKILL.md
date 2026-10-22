---
name: evidence-based-ui-review-and-release-gates
description: Apply explicit UI release criteria to current rendered evidence, aggregate blocking findings, and recommend a bounded release disposition without source repair. Do not use for collect missing viewport captures, traces, and runtime evidence before judgment or modify product source to fix the accepted review findings.
---

# Evidence Based Ui Review And Release Gates

## Responsibility

Apply explicit UI release criteria to current rendered evidence, aggregate blocking findings, and recommend a bounded release disposition without source repair.

## Trigger

Use when the requested outcome is: Apply explicit UI release criteria to current rendered evidence, aggregate blocking findings, and recommend a bounded release disposition without source repair.

Do not use when:
- Collect missing viewport captures, traces, and runtime evidence before judgment. Route to `ui-review-scope-and-evidence-acquisition`.
- Modify product source to fix the accepted review findings. Route to `ui-remediation`.

## Required Inputs

- An implementation, desktop and mobile captures, a brief, direction contract, target files, and findings.

Also require source or render identity, authorization, target surfaces, supported states, decision owner, and declared unknowns where applicable.

## Procedure

1. Freeze release criteria, current evidence manifest, target commit or artifact identity, supported surfaces, and accepted-risk authority.
2. Reject stale, mismatched, source-only, or self-attested evidence and route recapture needs.
3. Map each criterion to evidence and consolidate duplicate findings without erasing domain-specific impact.
4. Classify blockers, non-blockers, waived risks, recapture requirements, and invalidated prior evidence.
5. Recommend pass, pass-with-explicit-risk, needs-repair, or blocked to the human release owner; do not edit source or release.

## Output Contract

Produce:
- criterion-to-evidence matrix
- deduplicated release findings
- UI release recommendation
- risk and recapture ledger

Every material design choice, implementation claim, finding, score, capture, or disposition must link to supplied authority or current evidence, or be labeled assumption/unknown.

## UI Coverage

- `criterion-evidence`
- `current-render`
- `blocking-findings`
- `release-recommendation`
- `recapture`

## Hard Gates

- No release criterion may pass from source inspection, prior screenshots, or reviewer assertion when current rendered or interaction evidence is required.
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
- `rendered-ui-critique-and-release-disposition`
- `cross-domain-ui-preflight-checklists`
- `ui-remediation`

Never perform remote Git, external-system writes, merge, deploy, release, or an adjacent capability's work. Review and preflight capabilities never repair product source; evidence-acquisition capabilities never issue design findings.
