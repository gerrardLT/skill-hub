---
name: website-audit-remediation
description: Apply explicitly accepted website audit findings to authorized source, verify affected checks, and preserve a separate reassessment boundary. Do not use for assess the website and produce independent audit findings first or publish or deploy the repaired website.
---

# Website Audit Remediation

## Responsibility

Apply explicitly accepted website audit findings to authorized source, verify affected checks, and preserve a separate reassessment boundary.

## Trigger

Use when the requested outcome is: Apply explicitly accepted website audit findings to authorized source, verify affected checks, and preserve a separate reassessment boundary.

Do not use when:
- Assess the website and produce independent audit findings first. Route to `website-audit-assessment`.
- Publish or deploy the repaired website. Route to `deployment-trigger-execution`.

## Required Inputs

- Confirmed audit finding, source mapping, approved repair scope, workspace, and local verification command.

Also require exact target identity, authority, mutation boundary, evidence consumer, cleanup or rollback, and declared unknowns where applicable.

## Procedure

1. Verify accepted finding IDs, original evidence, repair criteria, authorized files, content and SEO authority, test commands, and rollback boundary.
2. Deduplicate shared causes and order the smallest fixes that close findings without masking evidence or broad redesign.
3. Apply only authorized source, content, or local configuration changes; preserve unrelated routes, analytics, SEO, and behavior.
4. Run approved focused checks and prepare reassessment evidence; never deploy, close findings from self-attestation, or perform the independent audit.

## Output Contract

Produce:
- bounded website repair patch
- finding-to-fix traceability
- focused verification records
- independent reassessment handoff

Every material action, command, result, finding, score, capture, provider receipt, or completion claim must bind to exact target identity and current evidence or be labeled assumption/unknown.

## Coverage

- `accepted-audit-findings`
- `bounded-repair`
- `SEO-preservation`
- `reassessment`
- `no-deploy`
- `no-self-close`

## Hard Gates

- Website remediation cannot begin without accepted audit findings and cannot close them without separate current reassessment; repair authority never includes deployment.
- Preserve source, build, dataset, model, workflow, provider, browser, session, or local-system identity; command, version, exit, duration, artifacts, hashes, limitations, and cleanup must remain explicit when applicable.
- Return `needs-input` when a named owner can provide missing scope, authority, evidence, governance, target, or decision.
- Return `blocked` when proceeding would exceed mutation authority, expose credentials, violate governance, erase failed evidence, perform an undeclared remote or destructive action, or mix independent review with repair.

## Human Decision Authority

The Skill may return evidence, findings, options, and a recommendation. Scope approval, repair authorization, risk acceptance, publication, experiment submission, local-system change, remote action, and release disposition remain explicit human decisions under the declared identity.

## Status Mapping

- `passed`: the atomic output and every gate have current target-bound evidence.
- `needs-input`: a requestable scope, authority, target, fixture, governance term, or decision is absent.
- `blocked`: safe work requires prohibited access, unavailable authority, secret values, destructive or remote action, or an incompatible identity.
- `failed`: the authorized action ran but a deterministic check or required output failed.

## Non-Responsibilities

Does not absorb unrelated lifecycle responsibilities or expand provider, workspace, or remote-write authority implicitly.

Adjacent capabilities:
- `website-audit-assessment`
- `ui-remediation`
- `deployment-trigger-execution`
- `completion-evidence-gate`

Never silently expand source, command, browser, data, credential, local-system, provider, or remote authority. Independent review, QA, audit, evidence acquisition, analysis, and triage never repair source. Setup and authentication never imply authority to perform the downstream action.
