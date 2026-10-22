---
name: remote-pull-request-change
description: "Create or update one pull or merge request from one verified pushed ref after redaction and per-action authorization, without merge or deployment. Use when One pull request must be created or updated from an already pushed ref with redacted text under fresh authorization; Someone asks for the exact PR title, body and base for a specific branch. Do not use for: Push the local branch to the approved remote ref first (-> remote-git-push); Merge the identified pull request after a fresh readiness gate (-> remote-pull-request-merge)."
---

# Remote Pull Request Change

## Responsibility

Create or update one pull or merge request from one verified pushed ref after redaction and per-action authorization, without merge or deployment.

## Trigger

Use when the request matches any of:
- One pull request must be created or updated from an already pushed ref with redacted text under fresh authorization
- Someone asks for the exact PR title, body and base for a specific branch

Do not use when:
- Push the local branch to the approved remote ref first. Route to `remote-git-push`.
- Merge the identified pull request after a fresh readiness gate. Route to `remote-pull-request-merge`.

## Required Inputs

- Verified remote refs, approved base, title and body artifacts, redaction result, provider, and current authorization.

## Procedure

1. Verify repository, head and base refs and SHAs, push receipt, PR identity or create intent, title, body, issue links, test evidence, labels or reviewers, draft state, redaction, provider target, and fresh per-action authorization.
2. Preview exact create or update diff and reject credentials, unsupported claims, unrelated metadata, source changes, auto-merge, merge, or deployment side effects.
3. Perform one PR create or update action only for the exact target.
4. Record PR URL and ID, provider receipt, resulting base and head SHA, metadata hash, status, failure, and readiness handoff.

## Domain Guidance

- On update, regenerate the body from current evidence and remove sections that no longer hold; never carry stale text from an earlier run.
- Scan the title and body for secrets and internal-only detail at the point of sending; if the scan cannot run, refuse to send.

## Output Contract

Produce:
- pull-request create or update receipt
- PR identity and URL
- base, head, and metadata evidence
- failure and readiness handoff

Every material command, request, observation, provider response, finding, decision recommendation, or completion claim must bind to exact target identity and current evidence or be labeled assumption/unknown.

Deliver each output as the artifact itself (tables, commands, patches, plans, records), not as a description of how it would be produced.

## Coverage

- `verified-pushed-ref`
- `exact-base-head`
- `redaction`
- `per-action-authorization`
- `PR-receipt`
- `no-merge`

## Hard Gates

- PR-change authorization covers one exact create or update and cannot push, edit source, respond to unrelated comments, enable auto-merge, merge, or deploy.
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
- `remote-git-push`
- `remote-pull-request-merge`
- `pull-request-comment-response`
- `merge-and-deploy-readiness`

Never silently expand local, repository, provider, production, telemetry, incident, or release authority. Preflight never changes; observation never recovers; coordination never performs specialist actions; rollback never invents a target; one remote authorization never cascades to another action.
