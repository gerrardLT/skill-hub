---
name: remote-pull-request-merge
description: Merge one identified pull request with one allowed repository method after a fresh passing readiness gate and explicit per-action authorization, without deployment. Do not use for run the fresh merge and deploy readiness gate first or trigger the approved deployment after merge under a separate authorization.
---

# Remote Pull Request Merge

## Responsibility

Merge one identified pull request with one allowed repository method after a fresh passing readiness gate and explicit per-action authorization, without deployment.

## Trigger

Use when the requested outcome is: Merge one identified pull request with one allowed repository method after a fresh passing readiness gate and explicit per-action authorization, without deployment.

Do not use when:
- Run the fresh merge and deploy readiness gate first. Route to `merge-and-deploy-readiness`.
- Trigger the approved deployment after merge under a separate authorization. Route to `deployment-trigger-execution`.

## Required Inputs

- Pull request identity, fresh CI and review evidence, mergeability, approved method, current authorization, and rollback plan.

Also require exact repository, provider, environment, service, incident, release, artifact, telemetry, or local destination identity; authority; evidence window; and recovery or cleanup where applicable.

## Procedure

1. Verify repository and PR identity, base and head SHAs, current open state, fresh readiness timestamp, checks, reviews, conflicts, merge queue or method, title and message, protected policy, expected result, rollback or revert path, and fresh per-action authorization.
2. Refresh provider state immediately before merge and block on any SHA, check, review, conflict, policy, or readiness drift.
3. Perform one merge action only with the allowed method; do not push, update PR metadata, delete branches unless separately authorized, tag, release, or deploy.
4. Record provider merge receipt, resulting commit SHA, PR state, branch deletion state, failure, and separate deployment handoff.

## Output Contract

Produce:
- pull-request merge receipt
- resulting merge commit identity
- fresh readiness and provider evidence
- failure and separate deployment handoff

Every material command, request, observation, provider response, finding, decision recommendation, or completion claim must bind to exact target identity and current evidence or be labeled assumption/unknown.

## Coverage

- `exact-PR-head`
- `fresh-readiness`
- `allowed-merge-method`
- `per-action-authorization`
- `merge-receipt`
- `no-deploy`

## Hard Gates

- Merge authorization is one-shot for one PR at one exact head SHA after a fresh gate; it never authorizes deployment or any action after readiness drift.
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
- `merge-and-deploy-readiness`
- `deployment-trigger-execution`
- `remote-pull-request-change`
- `remote-git-push`

Never silently expand local, repository, provider, production, telemetry, incident, or release authority. Preflight never changes; observation never recovers; coordination never performs specialist actions; rollback never invents a target; one remote authorization never cascades to another action.
