---
name: website-audit-remediation
description: "Apply explicitly accepted website audit findings to authorized source, verify affected checks, and preserve a separate reassessment boundary. Use when Accepted website audit findings (SEO, content, links, accessibility, performance) must be fixed in source; An audit report exists and the approved fixes should be applied in batches with re-audit evidence prepared. Do not use for: Assess the website and produce independent audit findings first (-> website-audit-assessment); Publish or deploy the repaired website (-> deployment-trigger-execution); Fix accepted findings from a rendered UI critique (-> ui-remediation); Repair a defect whose root cause was confirmed outside a website audit (-> defect-remediation)."
---

# Website Audit Remediation

## Responsibility

Apply explicitly accepted website audit findings to authorized source, verify affected checks, and preserve a separate reassessment boundary.

## Trigger

Use when the request matches any of:
- Accepted website audit findings (SEO, content, links, accessibility, performance) must be fixed in source
- An audit report exists and the approved fixes should be applied in batches with re-audit evidence prepared

Do not use when:
- Assess the website and produce independent audit findings first. Route to `website-audit-assessment`.
- Publish or deploy the repaired website. Route to `deployment-trigger-execution`.
- Fix accepted findings from a rendered UI critique. Route to `ui-remediation`.
- Repair a defect whose root cause was confirmed outside a website audit. Route to `defect-remediation`.

## Required Inputs

- Confirmed audit finding, source mapping, approved repair scope, workspace, and local verification command.

## Procedure

1. Verify accepted finding IDs, original evidence, repair criteria, authorized files, content and SEO authority, test commands, and rollback boundary.
2. Deduplicate shared causes and order the smallest fixes that close findings without masking evidence or broad redesign.
3. Apply only authorized source, content, or local configuration changes; preserve unrelated routes, analytics, SEO, and behavior.
4. Run approved focused checks and prepare reassessment evidence; never deploy, close findings from self-attestation, or perform the independent audit.

## Domain Guidance

- Discriminator: use when accepted website audit findings exist and need source changes.

## Output Contract

Produce:
- bounded website repair patch
- finding-to-fix traceability
- focused verification records
- independent reassessment handoff

Every material action, command, result, finding, score, capture, provider receipt, or completion claim must bind to exact target identity and current evidence or be labeled assumption/unknown.

Deliver each output as the artifact itself (tables, commands, patches, plans, records), not as a description of how it would be produced.

## Coverage

- `accepted-audit-findings`
- `bounded-repair`
- `SEO-preservation`
- `reassessment`
- `no-deploy`
- `no-self-close`

## Hard Gates

- Website remediation cannot begin without accepted audit findings and cannot close them without separate current reassessment; repair authority never includes deployment.
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
- `website-audit-assessment`
- `ui-remediation`
- `deployment-trigger-execution`
- `completion-evidence-gate`
- `defect-remediation`

Never silently expand source, command, browser, data, credential, local-system, provider, or remote authority. Independent review, QA, audit, evidence acquisition, analysis, and triage never repair source. Setup and authentication never imply authority to perform the downstream action.
