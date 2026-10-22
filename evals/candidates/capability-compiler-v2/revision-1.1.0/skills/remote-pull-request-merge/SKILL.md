---
name: remote-pull-request-merge
description: "Merge one identified pull request with one allowed repository method after a fresh passing readiness gate and explicit per-action authorization, without deployment. Use when One identified pull request with a fresh passing readiness result must be merged by one allowed method under fresh authorization; Someone asks for the exact merge command pinned to a head SHA and the receipt fields to record. Do not use for: Run the fresh merge and deploy readiness gate first (-> merge-and-deploy-readiness); Trigger the approved deployment after merge under a separate authorization (-> deployment-trigger-execution); Create or update the pull request title, body or base (-> remote-pull-request-change)."
---

# Remote Pull Request Merge

## Responsibility

Merge one identified pull request with one allowed repository method after a fresh passing readiness gate and explicit per-action authorization, without deployment.

## Trigger

Use when the request matches any of:
- One identified pull request with a fresh passing readiness result must be merged by one allowed method under fresh authorization
- Someone asks for the exact merge command pinned to a head SHA and the receipt fields to record

Do not use when:
- Run the fresh merge and deploy readiness gate first. Route to `merge-and-deploy-readiness`.
- Trigger the approved deployment after merge under a separate authorization. Route to `deployment-trigger-execution`.
- Create or update the pull request title, body or base. Route to `remote-pull-request-change`.

## Required Inputs

- Pull request identity, fresh CI and review evidence, mergeability, approved method, current authorization, and rollback plan.

## Procedure

1. Verify repository and PR identity, base and head SHAs, current open state, fresh readiness timestamp, checks, reviews, conflicts, merge queue or method, title and message, protected policy, expected result, rollback or revert path, and fresh per-action authorization.
2. Use the supplied head SHA literally in the merge command and treat optional checks as non-blocking; add no requirement that policy and task did not state.
3. Refresh provider state immediately before merge and block on any SHA, check, review, conflict, policy, or readiness drift.
4. Perform one merge action only with the allowed method; do not push, update PR metadata, delete branches unless separately authorized, tag, release, or deploy.
5. Record provider merge receipt, resulting commit SHA, PR state, branch deletion state, failure, and separate deployment handoff.

## Domain Guidance

- Pin the merge to the head SHA supplied in the task; use it literally in the command. Use a placeholder only when no SHA was supplied, and then say so.
- Treat optional or neutral checks as non-blocking and say so; do not add requirements the repository policy and task did not state.
- Merge queues: entering the queue is an allowed method that returns 'queued' with a pending-result handoff. It is never reported as merged. Direct merge in a queue-protected repository is a blocker.
- List the receipt fields to capture: check run ids, resulting merge commit, PR state and branch-deletion state.

## Output Contract

Produce:
- pull-request merge receipt
- resulting merge commit identity
- fresh readiness and provider evidence
- failure and separate deployment handoff

Every material command, request, observation, provider response, finding, decision recommendation, or completion claim must bind to exact target identity and current evidence or be labeled assumption/unknown.

Deliver each output as the artifact itself (tables, commands, patches, plans, records), not as a description of how it would be produced.

## Coverage

- `exact-PR-head`
- `fresh-readiness`
- `allowed-merge-method`
- `per-action-authorization`
- `merge-receipt`
- `no-deploy`

## Hard Gates

- Merge authorization is one-shot for one PR at one exact head SHA after a fresh gate; it never authorizes deployment or any action after readiness drift.
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

## Human Decision Authority

The Skill may return evidence, options, findings, and a recommendation. Merge, deploy, rollback, risk acceptance, incident closure, provider configuration, identity change, adoption, persistence, and release decisions remain explicit human decisions under the declared action identity.

## Remote or Local-System Action Boundary

This Skill defines an action contract and does not execute the action by itself. Any real provider, repository, production, external-session, or local-system write requires fresh per-action authorization, one exact target and immutable input identity, preview or dry run where available, idempotency, durable receipt, bounded failure handling, and rollback, revocation, deletion, cancellation, or cleanup terms as applicable.

## Status Mapping

- `passed`: the atomic output and every gate have current target-bound evidence.
- `needs-input`: a requestable target, source, authority, evidence, governance term, or decision is absent. Deliver every supported part first and name the owner for the missing part.
- `blocked`: safe work requires prohibited access, unavailable authority, secret values, stale evidence, or an incompatible identity.
- `failed`: the authorized action ran but a deterministic gate or required output failed.

## Non-Responsibilities

Adjacent capabilities:
- `merge-and-deploy-readiness`
- `deployment-trigger-execution`
- `remote-pull-request-change`
- `remote-git-push`

Never silently expand local, repository, provider, production, telemetry, incident, or release authority. Preflight never changes; observation never recovers; coordination never performs specialist actions; rollback never invents a target; one remote authorization never cascades to another action.
