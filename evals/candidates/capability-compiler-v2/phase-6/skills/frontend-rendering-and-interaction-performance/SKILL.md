---
name: frontend-rendering-and-interaction-performance
description: Measure current frontend rendering and interaction performance under a frozen user journey and identify evidence-backed bottlenecks without source repair. Do not use for audit broad page-load, network, cache, image, and core web vitals behavior or apply the approved performance optimization to frontend source.
---

# Frontend Rendering And Interaction Performance

## Responsibility

Measure current frontend rendering and interaction performance under a frozen user journey and identify evidence-backed bottlenecks without source repair.

## Trigger

Use when the requested outcome is: Measure current frontend rendering and interaction performance under a frozen user journey and identify evidence-backed bottlenecks without source repair.

Do not use when:
- Audit broad page-load, network, cache, image, and Core Web Vitals behavior. Route to `web-performance-diagnostics`.
- Apply the approved performance optimization to frontend source. Route to `defect-remediation`.

## Required Inputs

- A rendered frontend, interaction traces, performance measurements, and device constraints.

Also require exact target identity, authority, mutation boundary, evidence consumer, cleanup or rollback, and declared unknowns where applicable.

## Procedure

1. Freeze source identity, journey, viewport, device or CPU profile, browser, data, cache state, warmup, sample count, budgets, and instrumentation.
2. Run approved local measurements for render phases, input delay, long tasks, layout work, hydration, state updates, and animation frames.
3. Report distributions and traces, distinguish noise from repeatable bottlenecks, and link suspected causes to source or runtime evidence.
4. Return baseline, bottlenecks, uncertainty, and optimization hypotheses without editing source or claiming production impact.

## Output Contract

Produce:
- interaction performance baseline
- trace and distribution evidence
- repeatable bottleneck findings
- optimization hypotheses and limits

Every material action, command, result, finding, score, capture, provider receipt, or completion claim must bind to exact target identity and current evidence or be labeled assumption/unknown.

## Coverage

- `frozen-journey`
- `device-profile`
- `warmup`
- `sample-count`
- `distribution`
- `interaction-latency`
- `trace`

## Hard Gates

- A frontend performance finding requires a frozen journey, representative device profile, warmup, sample count, distribution, budget, and repeatable trace; one fast or slow run is not evidence.
- Preserve source, build, dataset, model, workflow, provider, browser, session, or local-system identity; command, version, exit, duration, artifacts, hashes, limitations, and cleanup must remain explicit when applicable.
- Return `needs-input` when a named owner can provide missing scope, authority, evidence, governance, target, or decision.
- Return `blocked` when proceeding would exceed mutation authority, expose credentials, violate governance, erase failed evidence, perform an undeclared remote or destructive action, or mix independent review with repair.

## Status Mapping

- `passed`: the atomic output and every gate have current target-bound evidence.
- `needs-input`: a requestable scope, authority, target, fixture, governance term, or decision is absent.
- `blocked`: safe work requires prohibited access, unavailable authority, secret values, destructive or remote action, or an incompatible identity.
- `failed`: the authorized action ran but a deterministic check or required output failed.

## Non-Responsibilities

Does not approve upstream product decisions, expand authority, or perform remote writes beyond its explicit permission identity.

Adjacent capabilities:
- `web-performance-diagnostics`
- `defect-remediation`
- `purposeful-motion-and-animation-engineering`
- `baseline-regression-control`

Never silently expand source, command, browser, data, credential, local-system, provider, or remote authority. Independent review, QA, audit, evidence acquisition, analysis, and triage never repair source. Setup and authentication never imply authority to perform the downstream action.
