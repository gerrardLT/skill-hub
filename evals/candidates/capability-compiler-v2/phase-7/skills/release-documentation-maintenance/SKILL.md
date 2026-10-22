---
name: release-documentation-maintenance
description: Update release-facing local documentation from one evidence-bounded shipped or release-candidate diff and preserve coverage, source links, and verification. Do not use for package commits, version metadata, changelog, and pr body before remote delivery or configure release and commit association in the observability provider.
---

# Release Documentation Maintenance

## Responsibility

Update release-facing local documentation from one evidence-bounded shipped or release-candidate diff and preserve coverage, source links, and verification.

## Trigger

Use when the requested outcome is: Update release-facing local documentation from one evidence-bounded shipped or release-candidate diff and preserve coverage, source links, and verification.

Do not use when:
- Package commits, version metadata, changelog, and PR body before remote delivery. Route to `change-packaging-and-versioning`.
- Configure release and commit association in the observability provider. Route to `release-observability-configuration`.

## Required Inputs

- Shipped change evidence, documentation inventory, audience, release metadata, and write authority.

Also require exact repository, provider, environment, service, incident, release, artifact, telemetry, or local destination identity; authority; evidence window; and recovery or cleanup where applicable.

## Procedure

1. Freeze version, shipped or candidate diff, commit and artifact identities, requirements, migration, deprecation, configuration, known issues, and documentation scope.
2. Map each externally visible change to verified code, tests, issue or requirement, and target audience; classify added, changed, fixed, deprecated, removed, migration, and operator impact.
3. Update only authorized local release docs and links, preserve unknown or unreleased items, and avoid credentials, internal-only detail, or fabricated deployment status.
4. Run approved local link, format, or render checks and return coverage map, changed docs, hashes, and publication handoff.

## Output Contract

Produce:
- release documentation updates
- change-to-document coverage map
- link and render validation
- publication handoff and known gaps

Every material command, request, observation, provider response, finding, decision recommendation, or completion claim must bind to exact target identity and current evidence or be labeled assumption/unknown.

## Coverage

- `exact-version`
- `diff-evidence`
- `coverage-map`
- `migration-notes`
- `known-issues`
- `no-deploy-claim`

## Hard Gates

- Release documentation may describe only evidence-backed changes for the exact version and cannot convert a release candidate, merged code, or local artifact into a deployed claim.
- Preserve source, ref, pull request, artifact, release, environment, provider, service, incident, telemetry, baseline, or local-record identity; authority, evidence, limitations, cleanup, and recovery remain explicit.
- Return `needs-input` when a named owner can supply missing scope, target, authority, data governance, evidence, rollback, or decision.
- Return `blocked` when proceeding would expose credentials, exceed mutation authority, use stale evidence, mix readiness with action, mix observation with rollback, or perform undeclared remote or production work.

## Status Mapping

- `passed`: the atomic output and every gate have current target-bound evidence.
- `needs-input`: a requestable target, source, authority, evidence, governance term, or decision is absent.
- `blocked`: safe work requires prohibited access, unavailable authority, secret values, stale evidence, or an incompatible identity.
- `failed`: the authorized action ran but a deterministic gate or required output failed.

## Non-Responsibilities

Does not absorb unrelated lifecycle responsibilities or expand provider, workspace, or remote-write authority implicitly.

Adjacent capabilities:
- `change-packaging-and-versioning`
- `release-observability-configuration`
- `documentation-authoring`
- `deployment-observation`

Never silently expand local, repository, provider, production, telemetry, incident, or release authority. Preflight never changes; observation never recovers; coordination never performs specialist actions; rollback never invents a target; one remote authorization never cascades to another action.
