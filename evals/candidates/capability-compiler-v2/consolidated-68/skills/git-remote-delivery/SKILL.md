---
name: git-remote-delivery
description: "Consolidated capability with 3 selectable modes: remote-git-push; remote-pull-request-change; remote-pull-request-merge. Choose exactly one mode per invocation."
version: 1.1.0-consolidated
modes: [remote-git-push, remote-pull-request-change, remote-pull-request-merge]
---

# Git Remote Delivery

## Responsibility

Consolidated capability covering 3 related modes: Push one verified local branch to one approved remote ref without force under fresh per-action authorization and exact lease expectations.; Create or update one pull or merge request from one verified pushed ref after redaction and per-action authorization, without merge or deployment.; Merge one identified pull request with one allowed repository method after a fresh passing readiness gate and explicit per-action authorization, without deployment.

## Mode selection

This capability has several distinct modes. Read this table first, pick exactly one
mode for the current request, then follow only that mode's section. Do not blend
modes: each carries its own permission identity, gates, and stop conditions. The
permission column is binding - a run uses the permission of the mode it selected,
never the widest permission in this document.

| Mode | Permission | Use when | Routes elsewhere |
| --- | --- | --- | --- |
| `remote-git-push` | `remote-write-authorized-only` | One verified local branch must be pushed to one approved remote ref without force; Someone asks for the exact refspec, expected remote SHA and receipt for a push under fresh authorization. | Package and verify the local changes before any remote action (-> change-packaging-and-versioning); Create or update the |
| `remote-pull-request-change` | `remote-write-authorized-only` | One pull request must be created or updated from an already pushed ref with redacted text under fresh authorization; Someone asks for the exact PR title, body and base for a specific branch. | Push the local branch to the approved remote ref first (-> remote-git-push); Merge the identified pull request after a f |
| `remote-pull-request-merge` | `remote-write-authorized-only` | One identified pull request with a fresh passing readiness result must be merged by one allowed method under fresh authorization; Someone asks for the exact merge command pinned to a head SHA and the  | Run the fresh merge and deploy readiness gate first (-> merge-and-deploy-readiness); Trigger the approved deployment aft |

## Mode: `remote-git-push`

### remote-git-push

#### Responsibility

Push one verified local branch to one approved remote ref without force under fresh per-action authorization and exact lease expectations.

#### Trigger

Use when the request matches any of:
- One verified local branch must be pushed to one approved remote ref without force
- Someone asks for the exact refspec, expected remote SHA and receipt for a push under fresh authorization

Do not use when:
- Package and verify the local changes before any remote action. Route to `change-packaging-and-versioning`.
- Create or update the pull request after the push receipt exists. Route to `remote-pull-request-change`.

#### Required Inputs

- Verified source ref, approved remote and target ref, current authorization, credential boundary, and redaction result.

#### Procedure

1. Verify repository, clean local branch, source SHA, remote URL identity, destination ref, expected remote SHA or absence, credential status, protected-branch policy, object and secret checks, and fresh per-action authorization.
2. Preview exact refspec and reject force, force-with-lease not explicitly approved, wildcard, tag, deletion, multiple refs, or destination mismatch.
3. Perform one non-force push for the exact refspec and stop on non-fast-forward or policy failure without retrying a different target.
4. Record provider or Git receipt, before and after SHAs, refspec, exit, duration, failure, and next PR handoff.

#### Domain Guidance

- If the task or policy names a credential-redaction or pre-push hook, verify that it is installed and active, including a custom hooks path, and treat a missing one as a blocker unless the owner waives it in writing. If the task names no such hook, list it as an optional check the owner may require; do not add it as a blocker.

#### Output Contract

Produce:
- remote push receipt
- source and destination ref identity
- before and after remote SHA
- failure and pull-request handoff

Every material command, request, observation, provider response, finding, decision recommendation, or completion claim must bind to exact target identity and current evidence or be labeled assumption/unknown.

Deliver each output as the artifact itself (tables, commands, patches, plans, records), not as a description of how it would be produced.

#### Coverage

- `exact-refspec`
- `non-force`
- `expected-remote-SHA`
- `per-action-authorization`
- `push-receipt`
- `no-PR-action`

#### Hard Gates

- Push authorization covers one exact non-force refspec and expected remote state; it does not authorize force, deletion, tags, other refs, PR changes, merge, or deploy.
- Preflight never changes remote state; observation never executes recovery; coordination never performs specialist actions; one remote authorization never cascades.
- Preserve source, ref, pull request, artifact, release, environment, provider, service, incident, telemetry, baseline, or local-record identity; authority, evidence, limitations, cleanup, and recovery remain explicit.
- Return `needs-input` when a named owner can supply missing scope, target, authority, data governance, evidence, rollback, or decision.
- Return `blocked` when proceeding would expose credentials, exceed mutation authority, use stale evidence, mix readiness with action, mix observation with rollback, or perform undeclared remote or production work.
- Deliver every part the supplied evidence and authority support, label assumptions, and list each missing item with the owner who can supply it; `needs-input` or `blocked` applies to the unsupported part, not to the whole deliverable.

#### Forbidden Actions

- request, reveal, print, persist, hash, or transmit credential or secret values
- perform repository, provider, production, telemetry, incident, local-system, deployment, merge, or rollback mutation outside the exact atomic scope and fresh per-action authorization
- invent commands, provider receipts, deployment status, production evidence, incident actions, rollback result, approval, or release evidence
- combine readiness with action, observation with rollback, coordination with mitigation execution, or learning with unapproved persistence
- claim evaluation, approval, release, or completion evidence that has not been produced

#### Human Decision Authority

The Skill may return evidence, options, findings, and a recommendation. Merge, deploy, rollback, risk acceptance, incident closure, provider configuration, identity change, adoption, persistence, and release decisions remain explicit human decisions under the declared action identity.

#### Remote or Local-System Action Boundary

This Skill defines an action contract and does not execute the action by itself. Any real provider, repository, production, external-session, or local-system write requires fresh per-action authorization, one exact target and immutable input identity, preview or dry run where available, idempotency, durable receipt, bounded failure handling, and rollback, revocation, deletion, cancellation, or cleanup terms as applicable.

#### Status Mapping

- `passed`: the atomic output and every gate have current target-bound evidence.
- `needs-input`: a requestable target, source, authority, evidence, governance term, or decision is absent. Deliver every supported part first and name the owner for the missing part.
- `blocked`: safe work requires prohibited access, unavailable authority, secret values, stale evidence, or an incompatible identity.
- `failed`: the authorized action ran but a deterministic gate or required output failed.

#### Non-Responsibilities

Adjacent capabilities:
- `change-packaging-and-versioning`
- `remote-pull-request-change`
- `change-delivery-preflight`
- `remote-pull-request-merge`

Never silently expand local, repository, provider, production, telemetry, incident, or release authority. Preflight never changes; observation never recovers; coordination never performs specialist actions; rollback never invents a target; one remote authorization never cascades to another action.

## Mode: `remote-pull-request-change`

### remote-pull-request-change

#### Responsibility

Create or update one pull or merge request from one verified pushed ref after redaction and per-action authorization, without merge or deployment.

#### Trigger

Use when the request matches any of:
- One pull request must be created or updated from an already pushed ref with redacted text under fresh authorization
- Someone asks for the exact PR title, body and base for a specific branch

Do not use when:
- Push the local branch to the approved remote ref first. Route to `remote-git-push`.
- Merge the identified pull request after a fresh readiness gate. Route to `remote-pull-request-merge`.

#### Required Inputs

- Verified remote refs, approved base, title and body artifacts, redaction result, provider, and current authorization.

#### Procedure

1. Verify repository, head and base refs and SHAs, push receipt, PR identity or create intent, title, body, issue links, test evidence, labels or reviewers, draft state, redaction, provider target, and fresh per-action authorization.
2. Preview exact create or update diff and reject credentials, unsupported claims, unrelated metadata, source changes, auto-merge, merge, or deployment side effects.
3. Perform one PR create or update action only for the exact target.
4. Record PR URL and ID, provider receipt, resulting base and head SHA, metadata hash, status, failure, and readiness handoff.

#### Domain Guidance

- On update, regenerate the body from current evidence and remove sections that no longer hold; never carry stale text from an earlier run.
- Scan the title and body for secrets and internal-only detail at the point of sending; if the scan cannot run, refuse to send.
- Use only provider/CLI parameters whose interface is supplied or verified. Unknown flags remain unresolved, not executable examples. Preserve approved description content verbatim using a documented file/body API form.

#### Output Contract

Produce:
- pull-request create or update receipt
- PR identity and URL
- base, head, and metadata evidence
- failure and readiness handoff

Every material command, request, observation, provider response, finding, decision recommendation, or completion claim must bind to exact target identity and current evidence or be labeled assumption/unknown.

Deliver each output as the artifact itself (tables, commands, patches, plans, records), not as a description of how it would be produced.

#### Coverage

- `verified-pushed-ref`
- `exact-base-head`
- `redaction`
- `per-action-authorization`
- `PR-receipt`
- `no-merge`

#### Hard Gates

- PR-change authorization covers one exact create or update and cannot push, edit source, respond to unrelated comments, enable auto-merge, merge, or deploy.
- Preflight never changes remote state; observation never executes recovery; coordination never performs specialist actions; one remote authorization never cascades.
- Preserve source, ref, pull request, artifact, release, environment, provider, service, incident, telemetry, baseline, or local-record identity; authority, evidence, limitations, cleanup, and recovery remain explicit.
- Return `needs-input` when a named owner can supply missing scope, target, authority, data governance, evidence, rollback, or decision.
- Return `blocked` when proceeding would expose credentials, exceed mutation authority, use stale evidence, mix readiness with action, mix observation with rollback, or perform undeclared remote or production work.
- Deliver every part the supplied evidence and authority support, label assumptions, and list each missing item with the owner who can supply it; `needs-input` or `blocked` applies to the unsupported part, not to the whole deliverable.

#### Forbidden Actions

- request, reveal, print, persist, hash, or transmit credential or secret values
- perform repository, provider, production, telemetry, incident, local-system, deployment, merge, or rollback mutation outside the exact atomic scope and fresh per-action authorization
- invent commands, provider receipts, deployment status, production evidence, incident actions, rollback result, approval, or release evidence
- combine readiness with action, observation with rollback, coordination with mitigation execution, or learning with unapproved persistence
- claim evaluation, approval, release, or completion evidence that has not been produced

#### Human Decision Authority

The Skill may return evidence, options, findings, and a recommendation. Merge, deploy, rollback, risk acceptance, incident closure, provider configuration, identity change, adoption, persistence, and release decisions remain explicit human decisions under the declared action identity.

#### Remote or Local-System Action Boundary

This Skill defines an action contract and does not execute the action by itself. Any real provider, repository, production, external-session, or local-system write requires fresh per-action authorization, one exact target and immutable input identity, preview or dry run where available, idempotency, durable receipt, bounded failure handling, and rollback, revocation, deletion, cancellation, or cleanup terms as applicable.

#### Status Mapping

- `passed`: the atomic output and every gate have current target-bound evidence.
- `needs-input`: a requestable target, source, authority, evidence, governance term, or decision is absent. Deliver every supported part first and name the owner for the missing part.
- `blocked`: safe work requires prohibited access, unavailable authority, secret values, stale evidence, or an incompatible identity.
- `failed`: the authorized action ran but a deterministic gate or required output failed.

#### Non-Responsibilities

Adjacent capabilities:
- `remote-git-push`
- `remote-pull-request-merge`
- `pull-request-comment-response`
- `merge-and-deploy-readiness`

Never silently expand local, repository, provider, production, telemetry, incident, or release authority. Preflight never changes; observation never recovers; coordination never performs specialist actions; rollback never invents a target; one remote authorization never cascades to another action.

## Mode: `remote-pull-request-merge`

### remote-pull-request-merge

#### Responsibility

Merge one identified pull request with one allowed repository method after a fresh passing readiness gate and explicit per-action authorization, without deployment.

#### Trigger

Use when the request matches any of:
- One identified pull request with a fresh passing readiness result must be merged by one allowed method under fresh authorization
- Someone asks for the exact merge command pinned to a head SHA and the receipt fields to record

Do not use when:
- Run the fresh merge and deploy readiness gate first. Route to `merge-and-deploy-readiness`.
- Trigger the approved deployment after merge under a separate authorization. Route to `deployment-trigger-execution`.
- Create or update the pull request title, body or base. Route to `remote-pull-request-change`.

#### Required Inputs

- Pull request identity, fresh CI and review evidence, mergeability, approved method, current authorization, and rollback plan.

#### Procedure

1. Verify repository and PR identity, base and head SHAs, current open state, fresh readiness timestamp, checks, reviews, conflicts, merge queue or method, title and message, protected policy, expected result, rollback or revert path, and fresh per-action authorization.
2. Use the supplied head SHA literally in the merge command and treat optional checks as non-blocking; add no requirement that policy and task did not state.
3. Refresh provider state immediately before merge and block on any SHA, check, review, conflict, policy, or readiness drift.
4. Perform one merge action only with the allowed method; do not push, update PR metadata, delete branches unless separately authorized, tag, release, or deploy.
5. Record provider merge receipt, resulting commit SHA, PR state, branch deletion state, failure, and separate deployment handoff.

#### Domain Guidance

- Pin the merge to the head SHA supplied in the task; use it literally in the command. Use a placeholder only when no SHA was supplied, and then say so.
- Treat optional or neutral checks as non-blocking and say so; do not add requirements the repository policy and task did not state.
- Merge queues: entering the queue is an allowed method that returns 'queued' with a pending-result handoff. It is never reported as merged. Direct merge in a queue-protected repository is a blocker.
- List the receipt fields to capture: check run ids, resulting merge commit, PR state and branch-deletion state.
- Treat open/closed state as unknown unless explicitly present in current provider evidence. A heading such as MR state does not establish open state. Refresh that exact state before proposing a ready verdict; maintain SHA guard, merge method and no-branch-deletion authorization.
- A proposed merge receipt includes repository/provider, PR number, exact head and resulting merge SHA, method, executor identity, authorization reference, timestamp, branch retention, and observed provider result. Before execution these are a schema or placeholders, not an invented receipt.
- Begin proposal-only assessments with explicit disclosure: supplied snapshot not independently refreshed, no live provider access, and no merge performed. This disclosure does not negate a conditional readiness recommendation.

#### Output Contract

Produce:
- pull-request merge receipt
- resulting merge commit identity
- fresh readiness and provider evidence
- failure and separate deployment handoff

Every material command, request, observation, provider response, finding, decision recommendation, or completion claim must bind to exact target identity and current evidence or be labeled assumption/unknown.

Deliver each output as the artifact itself (tables, commands, patches, plans, records), not as a description of how it would be produced.

#### Coverage

- `exact-PR-head`
- `fresh-readiness`
- `allowed-merge-method`
- `per-action-authorization`
- `merge-receipt`
- `no-deploy`

#### Hard Gates

- Merge authorization is one-shot for one PR at one exact head SHA after a fresh gate; it never authorizes deployment or any action after readiness drift.
- Preflight never changes remote state; observation never executes recovery; coordination never performs specialist actions; one remote authorization never cascades.
- Preserve source, ref, pull request, artifact, release, environment, provider, service, incident, telemetry, baseline, or local-record identity; authority, evidence, limitations, cleanup, and recovery remain explicit.
- Return `needs-input` when a named owner can supply missing scope, target, authority, data governance, evidence, rollback, or decision.
- Return `blocked` when proceeding would expose credentials, exceed mutation authority, use stale evidence, mix readiness with action, mix observation with rollback, or perform undeclared remote or production work.
- Deliver every part the supplied evidence and authority support, label assumptions, and list each missing item with the owner who can supply it; `needs-input` or `blocked` applies to the unsupported part, not to the whole deliverable.

#### Forbidden Actions

- request, reveal, print, persist, hash, or transmit credential or secret values
- perform repository, provider, production, telemetry, incident, local-system, deployment, merge, or rollback mutation outside the exact atomic scope and fresh per-action authorization
- invent commands, provider receipts, deployment status, production evidence, incident actions, rollback result, approval, or release evidence
- combine readiness with action, observation with rollback, coordination with mitigation execution, or learning with unapproved persistence
- claim evaluation, approval, release, or completion evidence that has not been produced

#### Human Decision Authority

The Skill may return evidence, options, findings, and a recommendation. Merge, deploy, rollback, risk acceptance, incident closure, provider configuration, identity change, adoption, persistence, and release decisions remain explicit human decisions under the declared action identity.

#### Remote or Local-System Action Boundary

This Skill defines an action contract and does not execute the action by itself. Any real provider, repository, production, external-session, or local-system write requires fresh per-action authorization, one exact target and immutable input identity, preview or dry run where available, idempotency, durable receipt, bounded failure handling, and rollback, revocation, deletion, cancellation, or cleanup terms as applicable.

#### Status Mapping

- `passed`: the atomic output and every gate have current target-bound evidence.
- `needs-input`: a requestable target, source, authority, evidence, governance term, or decision is absent. Deliver every supported part first and name the owner for the missing part.
- `blocked`: safe work requires prohibited access, unavailable authority, secret values, stale evidence, or an incompatible identity.
- `failed`: the authorized action ran but a deterministic gate or required output failed.

#### Non-Responsibilities

Adjacent capabilities:
- `merge-and-deploy-readiness`
- `deployment-trigger-execution`
- `remote-pull-request-change`
- `remote-git-push`

Never silently expand local, repository, provider, production, telemetry, incident, or release authority. Preflight never changes; observation never recovers; coordination never performs specialist actions; rollback never invents a target; one remote authorization never cascades to another action.
