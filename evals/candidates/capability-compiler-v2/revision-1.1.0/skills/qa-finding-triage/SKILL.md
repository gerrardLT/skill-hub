---
name: qa-finding-triage
description: "Triage independently observed QA findings by reproducibility, severity, duplication, scope, ownership, and next capability without source repair. Use when A batch of QA findings must be deduplicated, severity-rated and routed to owners before a release decision; Someone asks which findings block release under the severity policy and which can be deferred. Do not use for: Run a new black-box QA campaign against the product (-> independent-blackbox-qa); Apply the accepted defect repair to source (-> defect-remediation)."
---

# QA Finding Triage

## Responsibility

Triage independently observed QA findings by reproducibility, severity, duplication, scope, ownership, and next capability without source repair.

## Trigger

Use when the request matches any of:
- A batch of QA findings must be deduplicated, severity-rated and routed to owners before a release decision
- Someone asks which findings block release under the severity policy and which can be deferred

Do not use when:
- Run a new black-box QA campaign against the product. Route to `independent-blackbox-qa`.
- Apply the accepted defect repair to source. Route to `defect-remediation`.

## Required Inputs

- QA findings, evidence, affected surface, release context, and severity policy.

## Procedure

1. Freeze finding identities, build or source identity, evidence, reproduction records, acceptance criteria, severity policy, and ownership map.
2. Normalize expected and observed behavior, environment, frequency, scope, impact, and evidence freshness.
3. Reproduce only from supplied evidence where permitted; merge true duplicates without losing affected variants or independent reports.
4. Assign disposition, severity rationale, owner, next capability, and missing evidence; do not fix, close from assertion, or accept risk.

## Domain Guidance

- Recommend a disposition by release tier: quick fixes critical and high only, standard adds medium, exhaustive includes low; mark the rest deferred with the reason.
- Deduplicate against findings a reviewer already skipped on this branch so the same item is not re-raised; merge true duplicates without losing affected variants.

## Output Contract

Produce:
- deduplicated QA finding register
- reproducibility and severity rationale
- ownership and routing map
- blocked and missing-evidence list

Every material action, command, result, finding, score, capture, provider receipt, or completion claim must bind to exact target identity and current evidence or be labeled assumption/unknown.

Deliver each output as the artifact itself (tables, commands, patches, plans, records), not as a description of how it would be produced.

## Coverage

- `deduplication`
- `reproducibility`
- `severity`
- `ownership`
- `routing`
- `no-fix`
- `no-risk-acceptance`

## Hard Gates

- Triage may classify and route findings but cannot repair source, waive risk, close defects without current evidence, or overwrite independent severity ownership.
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
- `independent-blackbox-qa`
- `root-cause-investigation`
- `defect-remediation`
- `rendered-ui-critique-and-release-disposition`

Never silently expand source, command, browser, data, credential, local-system, provider, or remote authority. Independent review, QA, audit, evidence acquisition, analysis, and triage never repair source. Setup and authentication never imply authority to perform the downstream action.
