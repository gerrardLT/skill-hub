---
name: ui-remediation
description: "Apply only accepted evidence-backed UI findings to authorized source and recapture the affected states without performing independent review. Use when Accepted UI findings must be fixed in source and the affected states recaptured for independent review; A reviewer's visual, responsive or interaction findings have been approved for repair. Do not use for: Independently critique current rendered UI and issue findings (-> rendered-ui-critique-and-release-disposition); Define the UI review matrix and acquire current captures before judgment (-> ui-review-scope-and-evidence-acquisition); Fix accepted findings from a website audit tool (SEO, content, links, performance) (-> website-audit-remediation)."
---

# UI Remediation

## Responsibility

Apply only accepted evidence-backed UI findings to authorized source and recapture the affected states without performing independent review.

## Trigger

Use when the request matches any of:
- Accepted UI findings must be fixed in source and the affected states recaptured for independent review
- A reviewer's visual, responsive or interaction findings have been approved for repair

Do not use when:
- Independently critique current rendered UI and issue findings. Route to `rendered-ui-critique-and-release-disposition`.
- Define the UI review matrix and acquire current captures before judgment. Route to `ui-review-scope-and-evidence-acquisition`.
- Fix accepted findings from a website audit tool (SEO, content, links, performance). Route to `website-audit-remediation`.

## Required Inputs

- UI findings, source workspace, design system, platform variant, and write authority.

## Procedure

1. Capture the pre-fix state of each affected route and viewport before changing source.
2. Verify accepted finding IDs, evidence, severity, repair direction, authorized files, design contract, affected states, review owner, and recapture plan.
3. Trace each finding to the smallest source change and preserve product truth, responsive behavior, content, accessibility, and interaction invariants.
4. Apply only approved repairs; route ambiguous taste, expanded scope, or architecture changes back to their owners.
5. Run approved focused checks and recapture affected route-state-viewport evidence; hand off to an independent reviewer without issuing disposition.

## Domain Guidance

- Capture the pre-fix state of each affected route and viewport first. Where the app supports restoring state, add a regression fixture that restores the pre-fix state and asserts the fixed behavior.
- Discriminator: use when accepted, evidence-backed UI findings exist and need source changes.

## Output Contract

Produce:
- bounded UI repair patch
- finding-to-change map
- focused verification evidence
- recapture bundle and independent-review handoff

Every material action, command, result, finding, score, capture, provider receipt, or completion claim must bind to exact target identity and current evidence or be labeled assumption/unknown.

Deliver each output as the artifact itself (tables, commands, patches, plans, records), not as a description of how it would be produced.

## Coverage

- `accepted-findings`
- `bounded-source-repair`
- `recapture`
- `reviewer-separation`
- `no-self-approval`

## Hard Gates

- UI remediation requires accepted reproducible findings and separate authorization; the remediator cannot create its own findings, waive risk, judge its recaptures, or issue release disposition.
- Independent review, QA, audit, acquisition, analysis, and triage never imply remediation; setup or authentication never implies downstream action authority.
- Preserve source, build, dataset, model, workflow, provider, browser, session, or local-system identity; command, version, exit, duration, artifacts, hashes, limitations, and cleanup must remain explicit when applicable.
- Return `needs-input` when a named owner can provide missing scope, authority, evidence, governance, target, or decision.
- Return `blocked` when proceeding would exceed mutation authority, expose credentials, violate governance, erase failed evidence, perform an undeclared remote or destructive action, or mix independent review with repair.
- Deliver every part the supplied evidence and authority support, label assumptions, and list each missing item with the owner who can supply it; `needs-input` or `blocked` applies to the unsupported part, not to the whole deliverable.

## Forbidden Actions

- request, reveal, print, persist, hash, or transmit credential or secret values
- perform source, local-system, browser, provider, publication, or remote mutations outside the exact atomic scope and fresh authorization
- invent commands, exits, duration, artifacts, captures, provider receipts, benchmark results, approval, or completion evidence
- combine independent evidence or findings with remediation, risk acceptance, publication, deployment, or release
- claim evaluation, approval, release, or completion evidence that has not been produced

## Human Decision Authority

The Skill may return evidence, findings, options, and a recommendation. Scope approval, repair authorization, risk acceptance, publication, experiment submission, local-system change, remote action, and release disposition remain explicit human decisions under the declared identity.

## Status Mapping

- `passed`: the atomic output and every gate have current target-bound evidence.
- `needs-input`: a requestable scope, authority, target, fixture, governance term, or decision is absent. Deliver every supported part first and name the owner for the missing part.
- `blocked`: safe work requires prohibited access, unavailable authority, secret values, destructive or remote action, or an incompatible identity.
- `failed`: the authorized action ran but a deterministic check or required output failed.

## Non-Responsibilities

Adjacent capabilities:
- `rendered-ui-critique-and-release-disposition`
- `ui-review-scope-and-evidence-acquisition`
- `evidence-based-ui-review-and-release-gates`
- `website-audit-remediation`

Never silently expand source, command, browser, data, credential, local-system, provider, or remote authority. Independent review, QA, audit, evidence acquisition, analysis, and triage never repair source. Setup and authentication never imply authority to perform the downstream action.
