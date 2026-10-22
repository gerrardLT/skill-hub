---
name: pull-request-comment-response
description: Post one evidence-backed response to one identified pull-request review comment under per-action authorization, without changing source or resolving unrelated threads. Do not use for acquire read-only pull-request and diff evidence before drafting a response or apply the accepted requested source change.
---

# Pull Request Comment Response

## Responsibility

Post one evidence-backed response to one identified pull-request review comment under per-action authorization, without changing source or resolving unrelated threads.

## Trigger

Use when the requested outcome is: Post one evidence-backed response to one identified pull-request review comment under per-action authorization, without changing source or resolving unrelated threads.

Do not use when:
- Acquire read-only pull-request and diff evidence before drafting a response. Route to `code-review-evidence-acquisition`.
- Apply the accepted requested source change. Route to `defect-remediation`.

## Required Inputs

- Comment identity, verified finding classification, response artifact, evidence links, provider, and current authorization.

Also require exact repository, provider, environment, service, incident, release, artifact, telemetry, or local destination identity; authority; evidence window; and recovery or cleanup where applicable.

## Procedure

1. Verify repository, PR, comment or thread ID, author request, current refs, source and test evidence, response text, redaction, thread action, and fresh per-action authorization.
2. Ensure the response addresses only the identified comment, distinguishes fixed, declined, needs-input, and follow-up states, and cites current evidence without fabricated claims.
3. Preview exact body and target; perform one comment or reply write only, with no source edit, label, assignment, resolution, merge, or unrelated thread action.
4. Record provider receipt, comment URL or ID, request hash, resulting state, and failure or retry status.

## Output Contract

Produce:
- provider comment receipt
- posted response and evidence links
- target PR and thread identity
- failure or bounded retry record

Every material command, request, observation, provider response, finding, decision recommendation, or completion claim must bind to exact target identity and current evidence or be labeled assumption/unknown.

## Coverage

- `exact-comment`
- `evidence-backed`
- `redaction`
- `per-action-authorization`
- `comment-receipt`
- `no-source-change`
- `no-thread-resolution`

## Hard Gates

- Authorization covers one exact PR comment response and no other thread, source change, resolution, label, assignment, merge, or deployment action.
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
- `code-review-evidence-acquisition`
- `defect-remediation`
- `remote-pull-request-change`
- `remote-pull-request-merge`

Never silently expand local, repository, provider, production, telemetry, incident, or release authority. Preflight never changes; observation never recovers; coordination never performs specialist actions; rollback never invents a target; one remote authorization never cascades to another action.
