---
name: change-delivery-preflight
description: Preflight one verified local change for delivery by checking branch and ref identity, merge base, credentials status, automation stops, evidence, documentation, and remote readiness without mutation. Do not use for package the verified local changes into commits, version, changelog, and pr metadata or push the already-packaged branch to its exact remote ref.
---

# Change Delivery Preflight

## Responsibility

Preflight one verified local change for delivery by checking branch and ref identity, merge base, credentials status, automation stops, evidence, documentation, and remote readiness without mutation.

## Trigger

Use when the requested outcome is: Preflight one verified local change for delivery by checking branch and ref identity, merge base, credentials status, automation stops, evidence, documentation, and remote readiness without mutation.

Do not use when:
- Package the verified local changes into commits, version, changelog, and PR metadata. Route to `change-packaging-and-versioning`.
- Push the already-packaged branch to its exact remote ref. Route to `remote-git-push`.

## Required Inputs

- A reviewed change, repository state, delivery policy, and intended publication boundary.

Also require exact repository, provider, environment, service, incident, release, artifact, telemetry, or local destination identity; authority; evidence window; and recovery or cleanup where applicable.

## Procedure

1. Freeze repository, branch, base and head refs, expected remote, delivery policy, required checks, documentation, credential metadata boundary, and prohibited actions.
2. Inspect local state and approved read-only remote metadata for divergence, stale base, uncommitted files, forbidden files, secret indicators, version or changelog gaps, and automation stops.
3. Validate current test and completion evidence without rerunning source mutation or trusting stale status.
4. Return ready or blocked with exact findings and required next owner; do not commit, push, create PRs, merge, deploy, or alter provider state.

## Output Contract

Produce:
- delivery preflight report
- branch and ref evidence
- credential and automation-stop status
- blocker and next-owner register

Every material command, request, observation, provider response, finding, decision recommendation, or completion claim must bind to exact target identity and current evidence or be labeled assumption/unknown.

## Coverage

- `branch-ref-identity`
- `merge-base`
- `clean-state`
- `credential-status`
- `automation-stops`
- `no-remote-mutation`

## Hard Gates

- Preflight is read-only: readiness never authorizes packaging, push, pull-request change, merge, deployment, or provider mutation.
- Preserve source, ref, pull request, artifact, release, environment, provider, service, incident, telemetry, baseline, or local-record identity; authority, evidence, limitations, cleanup, and recovery remain explicit.
- Return `needs-input` when a named owner can supply missing scope, target, authority, data governance, evidence, rollback, or decision.
- Return `blocked` when proceeding would expose credentials, exceed mutation authority, use stale evidence, mix readiness with action, mix observation with rollback, or perform undeclared remote or production work.

## Status Mapping

- `passed`: the atomic output and every gate have current target-bound evidence.
- `needs-input`: a requestable target, source, authority, evidence, governance term, or decision is absent.
- `blocked`: safe work requires prohibited access, unavailable authority, secret values, stale evidence, or an incompatible identity.
- `failed`: the authorized action ran but a deterministic gate or required output failed.

## Non-Responsibilities

Does not approve upstream product decisions, expand authority, or perform remote writes beyond its explicit permission identity.

Adjacent capabilities:
- `change-packaging-and-versioning`
- `remote-git-push`
- `remote-pull-request-change`
- `merge-and-deploy-readiness`

Never silently expand local, repository, provider, production, telemetry, incident, or release authority. Preflight never changes; observation never recovers; coordination never performs specialist actions; rollback never invents a target; one remote authorization never cascades to another action.
