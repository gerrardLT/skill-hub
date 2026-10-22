---
name: remote-git-push
description: Push one verified local branch to one approved remote ref without force under fresh per-action authorization and exact lease expectations. Do not use for package and verify the local changes before any remote action or create or update the pull request after the push receipt exists.
---

# Remote Git Push

## Responsibility

Push one verified local branch to one approved remote ref without force under fresh per-action authorization and exact lease expectations.

## Trigger

Use when the requested outcome is: Push one verified local branch to one approved remote ref without force under fresh per-action authorization and exact lease expectations.

Do not use when:
- Package and verify the local changes before any remote action. Route to `change-packaging-and-versioning`.
- Create or update the pull request after the push receipt exists. Route to `remote-pull-request-change`.

## Required Inputs

- Verified source ref, approved remote and target ref, current authorization, credential boundary, and redaction result.

Also require exact repository, provider, environment, service, incident, release, artifact, telemetry, or local destination identity; authority; evidence window; and recovery or cleanup where applicable.

## Procedure

1. Verify repository, clean local branch, source SHA, remote URL identity, destination ref, expected remote SHA or absence, credential status, protected-branch policy, object and secret checks, and fresh per-action authorization.
2. Preview exact refspec and reject force, force-with-lease not explicitly approved, wildcard, tag, deletion, multiple refs, or destination mismatch.
3. Perform one non-force push for the exact refspec and stop on non-fast-forward or policy failure without retrying a different target.
4. Record provider or Git receipt, before and after SHAs, refspec, exit, duration, failure, and next PR handoff.

## Output Contract

Produce:
- remote push receipt
- source and destination ref identity
- before and after remote SHA
- failure and pull-request handoff

Every material command, request, observation, provider response, finding, decision recommendation, or completion claim must bind to exact target identity and current evidence or be labeled assumption/unknown.

## Coverage

- `exact-refspec`
- `non-force`
- `expected-remote-SHA`
- `per-action-authorization`
- `push-receipt`
- `no-PR-action`

## Hard Gates

- Push authorization covers one exact non-force refspec and expected remote state; it does not authorize force, deletion, tags, other refs, PR changes, merge, or deploy.
- Preserve source, ref, pull request, artifact, release, environment, provider, service, incident, telemetry, baseline, or local-record identity; authority, evidence, limitations, cleanup, and recovery remain explicit.
- Return `needs-input` when a named owner can supply missing scope, target, authority, data governance, evidence, rollback, or decision.
- Return `blocked` when proceeding would expose credentials, exceed mutation authority, use stale evidence, mix readiness with action, mix observation with rollback, or perform undeclared remote or production work.

## Human Decision Authority

The Skill may return evidence, options, findings, and a recommendation. Merge, deploy, rollback, risk acceptance, incident closure, provider configuration, identity change, adoption, persistence, and release decisions remain explicit human decisions under the declared action identity.

## Remote or Local-System Action Boundary

This candidate defines an action contract, but Phase 7 candidate construction does not execute the action. Any real provider, repository, production, external-session, or local-system write requires fresh per-action authorization, one exact target and immutable input identity, preview or dry run where available, idempotency, durable receipt, bounded failure handling, and rollback, revocation, deletion, cancellation, or cleanup terms as applicable.

## Status Mapping

- `passed`: the atomic output and every gate have current target-bound evidence.
- `needs-input`: a requestable target, source, authority, evidence, governance term, or decision is absent.
- `blocked`: safe work requires prohibited access, unavailable authority, secret values, stale evidence, or an incompatible identity.
- `failed`: the authorized action ran but a deterministic gate or required output failed.

## Non-Responsibilities

Does not absorb unrelated lifecycle responsibilities or expand provider, workspace, or remote-write authority implicitly.

Adjacent capabilities:
- `change-packaging-and-versioning`
- `remote-pull-request-change`
- `change-delivery-preflight`
- `remote-pull-request-merge`

Never silently expand local, repository, provider, production, telemetry, incident, or release authority. Preflight never changes; observation never recovers; coordination never performs specialist actions; rollback never invents a target; one remote authorization never cascades to another action.
