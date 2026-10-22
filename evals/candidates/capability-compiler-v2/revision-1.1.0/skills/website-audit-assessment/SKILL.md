---
name: website-audit-assessment
description: "Independently assess an authorized website using local and read-only external evidence across content, accessibility, SEO, performance, security signals, links, and behavior without remediation. Use when An authorized website needs an independent audit across content, accessibility, SEO, performance, security signals and links; Someone asks for a reproducible findings list and a before and after comparison with an earlier audit. Do not use for: Apply the accepted website audit fixes to authorized source (-> website-audit-remediation); Run a narrow Web performance diagnostic under controlled conditions (-> web-performance-diagnostics)."
---

# Website Audit Assessment

## Responsibility

Independently assess an authorized website using local and read-only external evidence across content, accessibility, SEO, performance, security signals, links, and behavior without remediation.

## Trigger

Use when the request matches any of:
- An authorized website needs an independent audit across content, accessibility, SEO, performance, security signals and links
- Someone asks for a reproducible findings list and a before and after comparison with an earlier audit

Do not use when:
- Apply the accepted website audit fixes to authorized source. Route to `website-audit-remediation`.
- Run a narrow Web performance diagnostic under controlled conditions. Route to `web-performance-diagnostics`.

## Required Inputs

- A scannable site, audit CLI, permitted external read scope, and optional frozen baseline.

## Procedure

1. Freeze authorized origins, routes, crawl limits, authentication boundary, data policy, source or deployment identity, devices, criteria, and prohibited actions.
2. Use approved local commands and read-only external requests or browser actions; respect robots, rate, privacy, account, purchase, and destructive-state boundaries.
3. Record route, request, tool, version, timestamp, state, viewport, response, capture, hash, and reproducibility for each assessed criterion.
4. Issue deduplicated findings with severity, evidence, affected routes, owner, and reassessment requirement; do not repair, deploy, or post externally.

## Domain Guidance

- When a prior audit exists, reassess with a baseline diff (regression since the baseline) and report new, fixed and unchanged findings rather than only a fresh list.

## Output Contract

Produce:
- website assessment evidence manifest
- deduplicated reproducible findings
- route and criterion coverage
- reassessment and residual-risk report

Every material action, command, result, finding, score, capture, provider receipt, or completion claim must bind to exact target identity and current evidence or be labeled assumption/unknown.

Deliver each output as the artifact itself (tables, commands, patches, plans, records), not as a description of how it would be produced.

## Coverage

- `authorized-origins`
- `read-only-external`
- `crawl-limit`
- `criterion-evidence`
- `reproducible-finding`
- `no-remediation`

## Hard Gates

- Assessment authority is read-only: no source repair, form submission with consequential state, account change, provider mutation, deployment, or finding closure is permitted.
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

## Data and Credential Governance

For customer, proprietary, browser, evaluation, experiment, or externally transferred data, require authority, minimization, redaction, retention, access, transfer, deletion, and incident boundaries. Credential and secret values never enter prompts, logs, hashes, receipts, or artifacts. Missing governance returns `needs-input`; prohibited or unavailable authority returns `blocked`.

## Human Decision Authority

The Skill may return evidence, findings, options, and a recommendation. Scope approval, repair authorization, risk acceptance, publication, experiment submission, local-system change, remote action, and release disposition remain explicit human decisions under the declared identity.

## External or Local-System Action Boundary

This Skill defines an action contract and does not execute the action by itself. Any real local-system, external-session, provider, publication, or remote write requires fresh per-action authorization, exact target and scope, preview, durable receipt, expiry or cleanup, and rollback, revocation, deletion, or cancellation terms as applicable.

## Status Mapping

- `passed`: the atomic output and every gate have current target-bound evidence.
- `needs-input`: a requestable scope, authority, target, fixture, governance term, or decision is absent. Deliver every supported part first and name the owner for the missing part.
- `blocked`: safe work requires prohibited access, unavailable authority, secret values, destructive or remote action, or an incompatible identity.
- `failed`: the authorized action ran but a deterministic check or required output failed.

## Non-Responsibilities

Adjacent capabilities:
- `website-audit-remediation`
- `web-performance-diagnostics`
- `safe-browser-probing`
- `ui-review-scope-and-evidence-acquisition`

Never silently expand source, command, browser, data, credential, local-system, provider, or remote authority. Independent review, QA, audit, evidence acquisition, analysis, and triage never repair source. Setup and authentication never imply authority to perform the downstream action.
