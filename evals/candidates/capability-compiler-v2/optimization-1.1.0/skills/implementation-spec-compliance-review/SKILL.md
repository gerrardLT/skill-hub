---
name: implementation-spec-compliance-review
description: "Independently compare an implementation and its evidence with frozen requirements, design, interfaces, and scope without editing source. Use when An implementation must be checked against its approved requirements for missing, extra or contradicting behavior; Someone asks whether what was built is what was requested, nothing more and nothing less. Do not use for: Review the same patch broadly for correctness, security, and code-quality defects (-> independent-code-review); Fix accepted compliance gaps in the source (-> defect-remediation)."
---

# Implementation Spec Compliance Review

## Responsibility

Independently compare an implementation and its evidence with frozen requirements, design, interfaces, and scope without editing source.

## Trigger

Use when the request matches any of:
- An implementation must be checked against its approved requirements for missing, extra or contradicting behavior
- Someone asks whether what was built is what was requested, nothing more and nothing less

Do not use when:
- Review the same patch broadly for correctness, security, and code-quality defects. Route to `independent-code-review`.
- Fix accepted compliance gaps in the source. Route to `defect-remediation`.

## Required Inputs

- Approved task requirements, implementation diff, source snapshot, and implementer report as an untrusted claim.

## Procedure

1. Freeze requirement and design versions, source ref, patch, scope contract, test evidence, and review exclusions.
2. Map each stable requirement and design decision to implementation locations, tests, runtime evidence, or an explicit missing item.
3. Identify omitted, extra, contradictory, stale, or unverifiable behavior and distinguish spec defects from implementation defects.
4. Return a compliance matrix, findings, and revise-or-block recommendation for the human owner without edits.

## Domain Guidance

- Check both direction and date when deriving future time windows: replacing the hour on the same date may schedule in the past. Trace opt-out, timezones and added behavior against each requirement.

## Output Contract

Produce:
- requirement-to-implementation matrix
- compliance findings
- extra and missing behavior register
- human-owned disposition recommendation

Every material action, command, result, finding, score, capture, provider receipt, or completion claim must bind to exact target identity and current evidence or be labeled assumption/unknown.

Deliver each output as the artifact itself (tables, commands, patches, plans, records), not as a description of how it would be produced.

## Coverage

- `frozen-spec`
- `source-ref`
- `traceability`
- `missing-behavior`
- `extra-behavior`
- `no-source-edit`

## Hard Gates

- Compliance passes only when every frozen requirement and design obligation has current implementation and verification evidence and no unapproved behavior is silently introduced.
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
- `independent-code-review`
- `defect-remediation`
- `requirements-and-delivery-contract`
- `engineering-plan-review`

Never silently expand source, command, browser, data, credential, local-system, provider, or remote authority. Independent review, QA, audit, evidence acquisition, analysis, and triage never repair source. Setup and authentication never imply authority to perform the downstream action.
