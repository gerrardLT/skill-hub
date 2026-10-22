---
name: website-audit-assessment
description: Independently assess an authorized website using local and read-only external evidence across content, accessibility, SEO, performance, security signals, links, and behavior without remediation. Do not use for apply the accepted website audit fixes to authorized source or run a narrow web performance diagnostic under controlled conditions.
---

# Website Audit Assessment

## Responsibility

Independently assess an authorized website using local and read-only external evidence across content, accessibility, SEO, performance, security signals, links, and behavior without remediation.

## Trigger

Use when the requested outcome is: Independently assess an authorized website using local and read-only external evidence across content, accessibility, SEO, performance, security signals, links, and behavior without remediation.

Do not use when:
- Apply the accepted website audit fixes to authorized source. Route to `website-audit-remediation`.
- Run a narrow Web performance diagnostic under controlled conditions. Route to `web-performance-diagnostics`.

## Required Inputs

- A scannable site, audit CLI, permitted external read scope, and optional frozen baseline.

Also require exact target identity, authority, mutation boundary, evidence consumer, cleanup or rollback, and declared unknowns where applicable.

## Procedure

1. Freeze authorized origins, routes, crawl limits, authentication boundary, data policy, source or deployment identity, devices, criteria, and prohibited actions.
2. Use approved local commands and read-only external requests or browser actions; respect robots, rate, privacy, account, purchase, and destructive-state boundaries.
3. Record route, request, tool, version, timestamp, state, viewport, response, capture, hash, and reproducibility for each assessed criterion.
4. Issue deduplicated findings with severity, evidence, affected routes, owner, and reassessment requirement; do not repair, deploy, or post externally.

## Output Contract

Produce:
- website assessment evidence manifest
- deduplicated reproducible findings
- route and criterion coverage
- reassessment and residual-risk report

Every material action, command, result, finding, score, capture, provider receipt, or completion claim must bind to exact target identity and current evidence or be labeled assumption/unknown.

## Coverage

- `authorized-origins`
- `read-only-external`
- `crawl-limit`
- `criterion-evidence`
- `reproducible-finding`
- `no-remediation`

## Hard Gates

- Assessment authority is read-only: no source repair, form submission with consequential state, account change, provider mutation, deployment, or finding closure is permitted.
- Preserve source, build, dataset, model, workflow, provider, browser, session, or local-system identity; command, version, exit, duration, artifacts, hashes, limitations, and cleanup must remain explicit when applicable.
- Return `needs-input` when a named owner can provide missing scope, authority, evidence, governance, target, or decision.
- Return `blocked` when proceeding would exceed mutation authority, expose credentials, violate governance, erase failed evidence, perform an undeclared remote or destructive action, or mix independent review with repair.

## Data and Credential Governance

For customer, proprietary, browser, evaluation, experiment, or externally transferred data, require authority, minimization, redaction, retention, access, transfer, deletion, and incident boundaries. Credential and secret values never enter prompts, logs, hashes, receipts, or artifacts. Missing governance returns `needs-input`; prohibited or unavailable authority returns `blocked`.

## Human Decision Authority

The Skill may return evidence, findings, options, and a recommendation. Scope approval, repair authorization, risk acceptance, publication, experiment submission, local-system change, remote action, and release disposition remain explicit human decisions under the declared identity.

## External or Local-System Action Boundary

This candidate defines an action contract but Phase 6 candidate construction and evaluation planning do not execute the action. Any real local-system, external-session, provider, publication, or remote write requires fresh per-action authorization, exact target and scope, preview, durable receipt, expiry or cleanup, and rollback, revocation, deletion, or cancellation terms as applicable.

## Status Mapping

- `passed`: the atomic output and every gate have current target-bound evidence.
- `needs-input`: a requestable scope, authority, target, fixture, governance term, or decision is absent.
- `blocked`: safe work requires prohibited access, unavailable authority, secret values, destructive or remote action, or an incompatible identity.
- `failed`: the authorized action ran but a deterministic check or required output failed.

## Non-Responsibilities

Does not approve upstream product decisions, expand authority, or perform remote writes beyond its explicit permission identity.

Adjacent capabilities:
- `website-audit-remediation`
- `web-performance-diagnostics`
- `safe-browser-probing`
- `ui-review-scope-and-evidence-acquisition`

Never silently expand source, command, browser, data, credential, local-system, provider, or remote authority. Independent review, QA, audit, evidence acquisition, analysis, and triage never repair source. Setup and authentication never imply authority to perform the downstream action.
