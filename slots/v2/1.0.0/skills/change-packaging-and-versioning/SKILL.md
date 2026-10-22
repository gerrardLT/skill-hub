---
name: change-packaging-and-versioning
description: Package verified local changes into bisectable commits, coherent version and changelog metadata, credential-safe PR material, and a push handoff without remote writes. Do not use for check whether the unpackaged branch is ready for delivery first or push the completed package to the approved remote ref.
---

# Change Packaging And Versioning

## Responsibility

Package verified local changes into bisectable commits, coherent version and changelog metadata, credential-safe PR material, and a push handoff without remote writes.

## Trigger

Use when the requested outcome is: Package verified local changes into bisectable commits, coherent version and changelog metadata, credential-safe PR material, and a push handoff without remote writes.

Do not use when:
- Check whether the unpackaged branch is ready for delivery first. Route to `change-delivery-preflight`.
- Push the completed package to the approved remote ref. Route to `remote-git-push`.

## Required Inputs

- Implemented and reviewed changes with fresh verification evidence.

Also require exact repository, provider, environment, service, incident, release, artifact, telemetry, or local destination identity; authority; evidence window; and recovery or cleanup where applicable.

## Procedure

1. Verify preflight result, frozen diff, local branch, commit policy, version scheme, changelog authority, release scope, evidence, and secret or credential exclusions.
2. Group changes into the smallest coherent bisectable local commits without rewriting unrelated history or fabricating test claims.
3. Update only authorized local version, changelog, and release or PR metadata with evidence-linked content and redaction.
4. Run approved local packaging checks and return commit IDs, version, changed files, metadata hashes, and exact push handoff; no remote action.

## Output Contract

Produce:
- bisectable local commits
- version and changelog updates
- redacted PR and release metadata
- local packaging evidence and push handoff

Every material command, request, observation, provider response, finding, decision recommendation, or completion claim must bind to exact target identity and current evidence or be labeled assumption/unknown.

## Coverage

- `local-only`
- `bisectable-commits`
- `version`
- `changelog`
- `redaction`
- `no-push`

## Hard Gates

- Packaging is local only: it may create approved commits and metadata but cannot push, create or update a PR, merge, tag remotely, deploy, or claim remote delivery.
- Preserve source, ref, pull request, artifact, release, environment, provider, service, incident, telemetry, baseline, or local-record identity; authority, evidence, limitations, cleanup, and recovery remain explicit.
- Return `needs-input` when a named owner can supply missing scope, target, authority, data governance, evidence, rollback, or decision.
- Return `blocked` when proceeding would expose credentials, exceed mutation authority, use stale evidence, mix readiness with action, mix observation with rollback, or perform undeclared remote or production work.

## Human Decision Authority

The Skill may return evidence, options, findings, and a recommendation. Merge, deploy, rollback, risk acceptance, incident closure, provider configuration, identity change, adoption, persistence, and release decisions remain explicit human decisions under the declared action identity.

## Status Mapping

- `passed`: the atomic output and every gate have current target-bound evidence.
- `needs-input`: a requestable target, source, authority, evidence, governance term, or decision is absent.
- `blocked`: safe work requires prohibited access, unavailable authority, secret values, stale evidence, or an incompatible identity.
- `failed`: the authorized action ran but a deterministic gate or required output failed.

## Non-Responsibilities

Does not approve upstream product decisions, expand authority, or perform remote writes beyond its explicit permission identity.

Adjacent capabilities:
- `change-delivery-preflight`
- `remote-git-push`
- `remote-pull-request-change`
- `release-documentation-maintenance`

Never silently expand local, repository, provider, production, telemetry, incident, or release authority. Preflight never changes; observation never recovers; coordination never performs specialist actions; rollback never invents a target; one remote authorization never cascades to another action.
