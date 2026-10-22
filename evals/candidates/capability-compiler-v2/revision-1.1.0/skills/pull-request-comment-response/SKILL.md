---
name: pull-request-comment-response
description: "Post one evidence-backed response to one identified pull-request review comment under per-action authorization, without changing source or resolving unrelated threads. Use when One identified pull request review comment needs a single evidence-backed reply posted under fresh authorization; Someone asks for the exact reply text and target for a specific review thread. Do not use for: Acquire read-only pull-request and diff evidence before drafting a response (-> code-review-evidence-acquisition); Apply the accepted requested source change (-> defect-remediation)."
---

# Pull Request Comment Response

## Responsibility

Post one evidence-backed response to one identified pull-request review comment under per-action authorization, without changing source or resolving unrelated threads.

## Trigger

Use when the request matches any of:
- One identified pull request review comment needs a single evidence-backed reply posted under fresh authorization
- Someone asks for the exact reply text and target for a specific review thread

Do not use when:
- Acquire read-only pull-request and diff evidence before drafting a response. Route to `code-review-evidence-acquisition`.
- Apply the accepted requested source change. Route to `defect-remediation`.

## Required Inputs

- Comment identity, verified finding classification, response artifact, evidence links, provider, and current authorization.

## Procedure

1. Classify the comment as line-level or top-level and bind the reply target and endpoint to that class.
2. Verify repository, PR, comment or thread ID, author request, current refs, source and test evidence, response text, redaction, thread action, and fresh per-action authorization.
3. Ensure the response addresses only the identified comment, distinguishes fixed, declined, needs-input, and follow-up states, and cites current evidence without fabricated claims.
4. Preview exact body and target; perform one comment or reply write only, with no source edit, label, assignment, resolution, merge, or unrelated thread action.
5. Record provider receipt, comment URL or ID, request hash, resulting state, and failure or retry status.

## Domain Guidance

- Classify the target first: a line-level review comment is answered as a reply in its thread; a top-level conversation comment is answered as a new conversation comment. Bind the reply target to that class and never post a line-level reply to the wrong endpoint.
- If a reply fails (closed PR, no permission), report the failure and stop; do not retry to a different target.

## Output Contract

Produce:
- provider comment receipt
- posted response and evidence links
- target PR and thread identity
- failure or bounded retry record

Every material command, request, observation, provider response, finding, decision recommendation, or completion claim must bind to exact target identity and current evidence or be labeled assumption/unknown.

Deliver each output as the artifact itself (tables, commands, patches, plans, records), not as a description of how it would be produced.

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
- `code-review-evidence-acquisition`
- `defect-remediation`
- `remote-pull-request-change`
- `remote-pull-request-merge`

Never silently expand local, repository, provider, production, telemetry, incident, or release authority. Preflight never changes; observation never recovers; coordination never performs specialist actions; rollback never invents a target; one remote authorization never cascades to another action.
