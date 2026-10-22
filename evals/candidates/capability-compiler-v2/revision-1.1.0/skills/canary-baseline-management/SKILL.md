---
name: canary-baseline-management
description: "Create or update immutable local canary baseline evidence only for explicitly selected production pages, without application or provider mutation. Use when Chosen production pages need a frozen baseline capture to compare future canary samples against; A healthy release should replace the old baseline and the change must be recorded without deleting the old one. Do not use for: Continuously observe production pages and diff signals against the baseline (-> production-canary-monitoring); Fix the application after an accepted canary finding (-> defect-remediation)."
---

# Canary Baseline Management

## Responsibility

Create or update immutable local canary baseline evidence only for explicitly selected production pages, without application or provider mutation.

## Trigger

Use when the request matches any of:
- Chosen production pages need a frozen baseline capture to compare future canary samples against
- A healthy release should replace the old baseline and the change must be recorded without deleting the old one

Do not use when:
- Continuously observe production pages and diff signals against the baseline. Route to `production-canary-monitoring`.
- Fix the application after an accepted canary finding. Route to `defect-remediation`.

## Required Inputs

- Approved URL and pages, external read authority, artifact directory, prior baseline, and baseline-write decision.

## Procedure

1. Freeze deployment and source identity, selected allowlisted pages, states, viewport, browser, data boundary, capture fields, masking, retention, baseline version, replacement approval, and artifact destination.
2. Use approved local and read-only external capture, avoid authenticated or sensitive pages unless separately governed, and record complete provenance.
3. Write immutable baseline artifacts, manifest, hashes, masks, thresholds, and supersession links without changing application source or provider config.
4. Return baseline identity, old and new relationship, capture evidence, limitations, and deletion path.

## Domain Guidance

- Capture a baseline before the deploy; replace it only after a healthy canary, with the prior version kept and linked in an explicit supersession record (old id, new id, reason, approver).
- Define concrete invalidation triggers for each baseline (release changes layout, A/B test active, data-dependent content) and flag measurable shifts the new capture shows, for example a rise in largest contentful paint.

## Output Contract

Produce:
- versioned canary baseline artifacts
- capture provenance manifest
- threshold and masking policy
- supersession and deletion record
- supersession record and baseline invalidation triggers

Every material command, request, observation, provider response, finding, decision recommendation, or completion claim must bind to exact target identity and current evidence or be labeled assumption/unknown.

Deliver each output as the artifact itself (tables, commands, patches, plans, records), not as a description of how it would be produced.

## Coverage

- `allowlisted-pages`
- `immutable-baseline`
- `capture-provenance`
- `masking`
- `thresholds`
- `supersession`

## Hard Gates

- A canary baseline is an immutable evidence artifact for explicit pages and states; replacing it requires approval and preserves the prior version, reason, and comparison continuity.
- Preflight never changes remote state; observation never executes recovery; coordination never performs specialist actions; one remote authorization never cascades.
- Preserve source, ref, pull request, artifact, release, environment, provider, service, incident, telemetry, baseline, or local-record identity; authority, evidence, limitations, cleanup, and recovery remain explicit.
- Return `needs-input` when a named owner can supply missing scope, target, authority, data governance, evidence, rollback, or decision.
- Return `blocked` when proceeding would expose credentials, exceed mutation authority, use stale evidence, mix readiness with action, mix observation with rollback, or perform undeclared remote or production work.
- Deliver every part the supplied evidence and authority support, label assumptions, and list each missing item with the owner who can supply it; `needs-input` or `blocked` applies to the unsupported part, not to the whole deliverable.

## Forbidden Actions

- request, reveal, print, persist, hash, or transmit credential or secret values
- perform repository, provider, production, telemetry, incident, local-system, deployment, merge, or rollback mutation outside the exact atomic scope and fresh per-action authorization
- invent commands, provider receipts, deployment status, production evidence, incident actions, rollback result, approval, or release evidence
- combine readiness with action, observation with rollback, coordination with mitigation execution, or learning with unapproved persistence
- claim evaluation, approval, release, or completion evidence that has not been produced

## Data and Credential Governance

For customer, production, incident, telemetry, trace, log, browser, or externally transferred data, require authority, minimization, redaction, sampling, access, region, retention, deletion, and incident boundaries. Credential and secret values never enter prompts, logs, hashes, receipts, or artifacts. Missing governance returns `needs-input`; prohibited or unavailable authority returns `blocked`.

## Human Decision Authority

The Skill may return evidence, options, findings, and a recommendation. Merge, deploy, rollback, risk acceptance, incident closure, provider configuration, identity change, adoption, persistence, and release decisions remain explicit human decisions under the declared action identity.

## Status Mapping

- `passed`: the atomic output and every gate have current target-bound evidence.
- `needs-input`: a requestable target, source, authority, evidence, governance term, or decision is absent. Deliver every supported part first and name the owner for the missing part.
- `blocked`: safe work requires prohibited access, unavailable authority, secret values, stale evidence, or an incompatible identity.
- `failed`: the authorized action ran but a deterministic gate or required output failed.

## Non-Responsibilities

Adjacent capabilities:
- `production-canary-monitoring`
- `deployment-observation`
- `defect-remediation`
- `source-metadata-and-provenance`

Never silently expand local, repository, provider, production, telemetry, incident, or release authority. Preflight never changes; observation never recovers; coordination never performs specialist actions; rollback never invents a target; one remote authorization never cascades to another action.
