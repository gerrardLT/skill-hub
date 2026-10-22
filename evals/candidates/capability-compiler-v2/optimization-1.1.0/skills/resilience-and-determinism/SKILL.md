---
name: resilience-and-determinism
description: "Diagnose and verify nondeterminism, retries, timeouts, cleanup, isolation, ordering, and recovery behavior under a frozen workload without source repair. Use when A test or job fails intermittently and needs a reproducible failure model before anyone edits code; Retries, timeouts, ordering or cleanup may be masking a race, leaked state or an arbitrary sleep. Do not use for: Apply the accepted source fix for the confirmed flaky root cause (-> defect-remediation); Design the overall test portfolio and layer allocation (-> testing-portfolio-strategy)."
---

# Resilience And Determinism

## Responsibility

Diagnose and verify nondeterminism, retries, timeouts, cleanup, isolation, ordering, and recovery behavior under a frozen workload without source repair.

## Trigger

Use when the request matches any of:
- A test or job fails intermittently and needs a reproducible failure model before anyone edits code
- Retries, timeouts, ordering or cleanup may be masking a race, leaked state or an arbitrary sleep

Do not use when:
- Apply the accepted source fix for the confirmed flaky root cause. Route to `defect-remediation`.
- Design the overall test portfolio and layer allocation. Route to `testing-portfolio-strategy`.

## Required Inputs

- An observed nondeterministic or resilience failure with reproduction context: the failing test or job, logs, environment, and any suspected cause (invalid data, race, contamination, fragile wait).

## Procedure

1. Freeze target identity, workload, environment, seeds, clocks, ordering, resources, retries, timeouts, and success criteria.
2. Repeat approved runs while varying one declared factor at a time and record exits, duration, logs, artifacts, and cleanup state.
3. List the candidate causes including arbitrary sleeps or fixed timeouts, and rank them by the evidence from the repeated runs.
4. Distinguish true recovery from retry masking, leaked state, non-idempotent side effects, race, external variance, and measurement noise.
5. Return a reproducible failure model, determinism or resilience verdict, and repair recommendation without editing source.

## Domain Guidance

- First-class hypothesis: an arbitrary sleep or fixed timeout. Prefer condition-based waiting (poll for the specific state with a bounded timeout and a failure message naming the expected and last observed state) over longer sleeps.
- When the cause is invalid data, recommend validation at four layers: entry point, business logic, environment guard, and debug instrumentation.
- Deliver the concrete fix as a patch or code block for the owner to apply; do not withhold it as a vague candidate when the race is confirmed, and state exactly what remains unverified.
- Preserve existing approved timezone and business semantics. A proposed policyholder-zone change is a separate product decision, not an assumed implementation fix. Reproduction and repeat checks must use the unchanged semantics until that decision is approved.

## Output Contract

Produce:
- determinism experiment record
- retry and timeout analysis
- cleanup and recovery evidence
- root-cause hypothesis and bounded recommendation

Every material action, command, result, finding, score, capture, provider receipt, or completion claim must bind to exact target identity and current evidence or be labeled assumption/unknown.

Deliver each output as the artifact itself (tables, commands, patches, plans, records), not as a description of how it would be produced.

## Coverage

- `seed`
- `ordering`
- `timeout`
- `retry-masking`
- `idempotency`
- `cleanup`
- `failure-injection`
- `repeated-evidence`

## Hard Gates

- A resilience claim requires repeated target-bound evidence with recorded seeds, ordering, environment, retries, timeouts, side effects, cleanup, and failure injection; one passing retry proves nothing.
- Independent review, QA, audit, acquisition, analysis, and triage never imply remediation; setup or authentication never implies downstream action authority.
- Preserve source, build, dataset, model, workflow, provider, browser, session, or local-system identity; command, version, exit, duration, artifacts, hashes, limitations, and cleanup must remain explicit when applicable.
- Return `needs-input` when a named owner can provide missing scope, authority, evidence, governance, target, or decision.
- Return `blocked` when proceeding would exceed mutation authority, expose credentials, violate governance, erase failed evidence, perform an undeclared remote or destructive action, or mix independent review with repair.
- Deliver every part the supplied evidence and authority support, label assumptions, and list each missing item with the owner who can supply it; `needs-input` or `blocked` applies to the unsupported part, not to the whole deliverable.

## Forbidden Actions

- request, reveal, print, persist, hash, or transmit credential or secret values
- perform source, local-system, browser, provider, publication, or remote mutations outside the exact atomic scope and fresh authorization
- invent commands, exits, duration, artifacts, captures, provider receipts, benchmark results, approval, or completion evidence
- combine independent evidence or findings with remediation, risk acceptance, publication, deployment, or release
- claim evaluation, approval, release, or completion evidence that has not been produced

## Status Mapping

- `passed`: the atomic output and every gate have current target-bound evidence.
- `needs-input`: a requestable scope, authority, target, fixture, governance term, or decision is absent. Deliver every supported part first and name the owner for the missing part.
- `blocked`: safe work requires prohibited access, unavailable authority, secret values, destructive or remote action, or an incompatible identity.
- `failed`: the authorized action ran but a deterministic check or required output failed.

## Non-Responsibilities

Adjacent capabilities:
- `root-cause-investigation`
- `defect-remediation`
- `baseline-regression-control`
- `testing-portfolio-strategy`

Never silently expand source, command, browser, data, credential, local-system, provider, or remote authority. Independent review, QA, audit, evidence acquisition, analysis, and triage never repair source. Setup and authentication never imply authority to perform the downstream action.
