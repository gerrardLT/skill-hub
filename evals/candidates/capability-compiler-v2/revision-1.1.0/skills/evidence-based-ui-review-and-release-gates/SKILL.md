---
name: evidence-based-ui-review-and-release-gates
description: "Apply explicit UI release criteria to current rendered evidence, or run a bounded cross-domain preflight before capture, aggregate blocking findings, and recommend a bounded release disposition without source repair. Use when Current rendered evidence and specialist findings exist and someone needs a release recommendation against explicit UI criteria; Before capture, a UI build needs a bounded cross-domain preflight across accessibility, content, states, responsiveness and motion. Do not use for: Collect missing viewport captures, traces, and runtime evidence before judgment (-> ui-review-scope-and-evidence-acquisition); Modify product source to fix the accepted review findings (-> ui-remediation); Discover and prioritize new UI findings from rendered evidence (-> rendered-ui-critique-and-release-disposition)."
---

# Evidence Based UI Review And Release Gates

## Responsibility

Apply explicit UI release criteria to current rendered evidence, or run a bounded cross-domain preflight before capture, aggregate blocking findings, and recommend a bounded release disposition without source repair.

## Trigger

Use when the request matches any of:
- Current rendered evidence and specialist findings exist and someone needs a release recommendation against explicit UI criteria
- Before capture, a UI build needs a bounded cross-domain preflight across accessibility, content, states, responsiveness and motion

Do not use when:
- Collect missing viewport captures, traces, and runtime evidence before judgment. Route to `ui-review-scope-and-evidence-acquisition`.
- Modify product source to fix the accepted review findings. Route to `ui-remediation`.
- Discover and prioritize new UI findings from rendered evidence. Route to `rendered-ui-critique-and-release-disposition`.

## Required Inputs

- An implementation, desktop and mobile captures, a brief, direction contract, target files, and findings; in preflight mode, a rendered UI or build, acceptance criteria, content, supported devices, and the release boundary.

## Procedure

1. Freeze release criteria, current evidence manifest, target commit or artifact identity, supported surfaces, and accepted-risk authority.
2. Reject stale, mismatched, source-only, or self-attested evidence and route recapture needs.
3. Map each criterion to evidence and consolidate duplicate findings without erasing domain-specific impact.
4. Classify blockers, non-blockers, waived risks, recapture requirements, and invalidated prior evidence.
5. Recommend pass, pass-with-explicit-risk, needs-repair, or blocked to the human release owner; do not edit source or release.

## Domain Guidance

- Preflight mode runs before evidence capture. Select only the applicable domains, state why any domain is not applicable, and mark unchecked, not-applicable-without-rationale and source-inspection-only items as unresolved, never passed.
- Canonical preflight items: text contrast 4.5:1 (3:1 large) and visible focus states; descriptive alt text and accessible names for icon-only controls; keyboard reach and order; touch targets at least 44 by 44 with 8 px spacing; zoom never disabled and body text at least 16 px; no horizontal overflow at 320 px; loading, empty, error and success states present; reduced-motion path; authentic content with no placeholder text; clean console on the primary journey.
- Release mode consumes the findings issued by rendered-ui-critique-and-release-disposition and owns the disposition. Critique produces findings, this Skill decides what blocks release and recommends pass, pass with explicit risk, needs repair, or blocked.
- Boundary: this Skill owns release criteria, blocking-finding aggregation and the disposition recommendation, including the preflight checklists absorbed from the former cross-domain checklist Skill; new finding discovery belongs to rendered-ui-critique-and-release-disposition.
- Preflight checks absorbed from the former checklist Skill: a defect that is deterministic from supplied static source (a missing input label or dialog accessible name, a fixed width that overflows at 360px, a text colour whose contrast ratio you can compute against its background) is a finding, not a risk. Grade findings by severity. Automated scans do not prove keyboard operability; say so and list it as unverified evidence needed.
- Give one clear disposition from the allowed set and state why. When part of the evidence is missing and part is failing, lead with the failing item (blocked or needs-repair) and list the missing evidence underneath instead of mixing two statuses.

## Output Contract

Produce:
- criterion-to-evidence matrix
- deduplicated release findings
- UI release recommendation
- risk and recapture ledger
- preflight result with blocking-finding register, evidence-gap list and residual-risk summary

Every material design choice, implementation claim, finding, score, capture, or disposition must link to supplied authority or current evidence, or be labeled assumption/unknown.

Deliver each output as the artifact itself (tables, commands, patches, plans, records), not as a description of how it would be produced.

## UI Coverage

- `criterion-evidence`
- `current-render`
- `blocking-findings`
- `release-recommendation`
- `recapture`

## Hard Gates

- No release criterion may pass from source inspection, prior screenshots, or reviewer assertion when current rendered or interaction evidence is required.
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
- `rendered-ui-critique-and-release-disposition`
- `ui-remediation`

Never perform remote Git, external-system writes, merge, deploy, release, or an adjacent capability's work. Review and preflight capabilities never repair product source; evidence-acquisition capabilities never issue design findings.
