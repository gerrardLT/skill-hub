---
name: remote-git-push
description: "Push one verified local branch to one approved remote ref without force under fresh per-action authorization and exact lease expectations. Use when One verified local branch must be pushed to one approved remote ref without force; Someone asks for the exact refspec, expected remote SHA and receipt for a push under fresh authorization. Do not use for: Package and verify the local changes before any remote action (-> change-packaging-and-versioning); Create or update the pull request after the push receipt exists (-> remote-pull-request-change)."
---

# Remote Git Push

## Responsibility

Push one verified local branch to one approved remote ref without force under fresh per-action authorization and exact lease expectations.

## Trigger

Use when the request matches any of:
- One verified local branch must be pushed to one approved remote ref without force
- Someone asks for the exact refspec, expected remote SHA and receipt for a push under fresh authorization

Do not use when:
- Package and verify the local changes before any remote action. Route to `change-packaging-and-versioning`.
- Create or update the pull request after the push receipt exists. Route to `remote-pull-request-change`.

## Required Inputs

- Verified source ref, approved remote and target ref, current authorization, credential boundary, and redaction result.

## Procedure

1. Verify repository, clean local branch, source SHA, remote URL identity, destination ref, expected remote SHA or absence, credential status, protected-branch policy, object and secret checks, and fresh per-action authorization.
2. Preview exact refspec and reject force, force-with-lease not explicitly approved, wildcard, tag, deletion, multiple refs, or destination mismatch.
3. Perform one non-force push for the exact refspec and stop on non-fast-forward or policy failure without retrying a different target.
4. Record provider or Git receipt, before and after SHAs, refspec, exit, duration, failure, and next PR handoff.

## Domain Guidance

- If the task or policy names a credential-redaction or pre-push hook, verify that it is installed and active, including a custom hooks path, and treat a missing one as a blocker unless the owner waives it in writing. If the task names no such hook, list it as an optional check the owner may require; do not add it as a blocker.

## Output Contract

Produce:
- remote push receipt
- source and destination ref identity
- before and after remote SHA
- failure and pull-request handoff

Every material command, request, observation, provider response, finding, decision recommendation, or completion claim must bind to exact target identity and current evidence or be labeled assumption/unknown.

Deliver each output as the artifact itself (tables, commands, patches, plans, records), not as a description of how it would be produced.

## Coverage

- `exact-refspec`
- `non-force`
- `expected-remote-SHA`
- `per-action-authorization`
- `push-receipt`
- `no-PR-action`

## Hard Gates

- Push authorization covers one exact non-force refspec and expected remote state; it does not authorize force, deletion, tags, other refs, PR changes, merge, or deploy.
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
- `change-packaging-and-versioning`
- `remote-pull-request-change`
- `change-delivery-preflight`
- `remote-pull-request-merge`

Never silently expand local, repository, provider, production, telemetry, incident, or release authority. Preflight never changes; observation never recovers; coordination never performs specialist actions; rollback never invents a target; one remote authorization never cascades to another action.
