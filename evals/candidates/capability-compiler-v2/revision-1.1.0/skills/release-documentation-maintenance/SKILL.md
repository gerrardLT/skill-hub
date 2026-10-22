---
name: release-documentation-maintenance
description: "Update release-facing local documentation from one evidence-bounded shipped or release-candidate diff and preserve coverage, source links, and verification. Use when A change has shipped or is a release candidate and the README, guides, API docs or changelog must be brought in line with the diff; Someone needs to know which externally visible changes are documented and which are not. Do not use for: Package commits, version metadata, changelog, and PR body before remote delivery (-> change-packaging-and-versioning); Configure release and commit association in the observability provider (-> release-observability-configuration)."
---

# Release Documentation Maintenance

## Responsibility

Update release-facing local documentation from one evidence-bounded shipped or release-candidate diff and preserve coverage, source links, and verification.

## Trigger

Use when the request matches any of:
- A change has shipped or is a release candidate and the README, guides, API docs or changelog must be brought in line with the diff
- Someone needs to know which externally visible changes are documented and which are not

Do not use when:
- Package commits, version metadata, changelog, and PR body before remote delivery. Route to `change-packaging-and-versioning`.
- Configure release and commit association in the observability provider. Route to `release-observability-configuration`.

## Required Inputs

- Shipped change evidence, documentation inventory, audience, release metadata, and write authority.

## Procedure

1. Freeze version, shipped or candidate diff, commit and artifact identities, requirements, migration, deprecation, configuration, known issues, and documentation scope.
2. Map each externally visible change to verified code, tests, issue or requirement, and target audience; classify added, changed, fixed, deprecated, removed, migration, and operator impact.
3. Update only authorized local release docs and links, preserve unknown or unreleased items, and avoid credentials, internal-only detail, or fabricated deployment status.
4. Run approved local link, format, or render checks and return coverage map, changed docs, hashes, and publication handoff.

## Domain Guidance

- Extract the public surface from the diff: new or removed exports, commands, CLI flags, config options, endpoints, environment variables and renamed modules. Each one needs a documentation target or an explicit gap.
- Tag every touched document as tutorial, how-to, reference or explanation and keep one type per document.
- Apply obvious factual updates directly. Return subjective wording, tone or structure changes as proposals that need the document owner's decision.

## Output Contract

Produce:
- release documentation updates
- change-to-document coverage map
- link and render validation
- publication handoff and known gaps
- proposals for subjective edits awaiting owner decision

Every material command, request, observation, provider response, finding, decision recommendation, or completion claim must bind to exact target identity and current evidence or be labeled assumption/unknown.

Deliver each output as the artifact itself (tables, commands, patches, plans, records), not as a description of how it would be produced.

## Coverage

- `exact-version`
- `diff-evidence`
- `coverage-map`
- `migration-notes`
- `known-issues`
- `no-deploy-claim`

## Hard Gates

- Release documentation may describe only evidence-backed changes for the exact version and cannot convert a release candidate, merged code, or local artifact into a deployed claim.
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

## Status Mapping

- `passed`: the atomic output and every gate have current target-bound evidence.
- `needs-input`: a requestable target, source, authority, evidence, governance term, or decision is absent. Deliver every supported part first and name the owner for the missing part.
- `blocked`: safe work requires prohibited access, unavailable authority, secret values, stale evidence, or an incompatible identity.
- `failed`: the authorized action ran but a deterministic gate or required output failed.

## Non-Responsibilities

Adjacent capabilities:
- `change-packaging-and-versioning`
- `release-observability-configuration`
- `documentation-authoring`
- `deployment-observation`

Never silently expand local, repository, provider, production, telemetry, incident, or release authority. Preflight never changes; observation never recovers; coordination never performs specialist actions; rollback never invents a target; one remote authorization never cascades to another action.
