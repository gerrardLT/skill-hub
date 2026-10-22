---
name: frontend-rendering-and-interaction-performance
description: "Measure current frontend rendering and interaction performance under a frozen user journey and identify evidence-backed bottlenecks without source repair. Use when A specific interaction (click, type, scroll, route change) feels slow or janky and needs a trace-backed explanation; Component-level rendering, long tasks, hydration or animation frame drops must be measured on a frozen journey. Do not use for: Audit broad page-load, network, cache, image, and Core Web Vitals behavior (-> web-performance-diagnostics); Apply the approved performance optimization to frontend source (-> defect-remediation)."
---

# Frontend Rendering And Interaction Performance

## Responsibility

Measure current frontend rendering and interaction performance under a frozen user journey and identify evidence-backed bottlenecks without source repair.

## Trigger

Use when the request matches any of:
- A specific interaction (click, type, scroll, route change) feels slow or janky and needs a trace-backed explanation
- Component-level rendering, long tasks, hydration or animation frame drops must be measured on a frozen journey

Do not use when:
- Audit broad page-load, network, cache, image, and Core Web Vitals behavior. Route to `web-performance-diagnostics`.
- Apply the approved performance optimization to frontend source. Route to `defect-remediation`.

## Required Inputs

- A rendered frontend, interaction traces, performance measurements, and device constraints.

## Procedure

1. Freeze source identity, journey, viewport, device or CPU profile, browser, data, cache state, warmup, sample count, budgets, and instrumentation.
2. Run approved local measurements for render phases, input delay, long tasks, layout work, hydration, state updates, and animation frames.
3. Report distributions and traces, distinguish noise from repeatable bottlenecks, and link suspected causes to source or runtime evidence.
4. Return baseline, bottlenecks, uncertainty, and optimization hypotheses without editing source or claiming production impact.

## Domain Guidance

- Default budgets when the user supplies none: long task <= 50 ms, frame <= 16.7 ms (60 fps), interaction latency (INP) <= 200 ms at p75; report every measured value against them and say when a default was used.
- Hypothesis catalog: animating width/height/top/left instead of transform/opacity triggers layout and paint; a parent CSS variable driving child transforms recalculates every child; Framer Motion x/y/scale shorthands run on the main thread and drop frames under load.
- Ownership: field INP belongs to web-performance-diagnostics; this Skill owns component-level interaction traces.
- Ownership: component-level render and interaction traces belong here; page-level Core Web Vitals, including field INP, belong to web-performance-diagnostics.

## Output Contract

Produce:
- interaction performance baseline
- trace and distribution evidence
- repeatable bottleneck findings
- optimization hypotheses and limits

Every material action, command, result, finding, score, capture, provider receipt, or completion claim must bind to exact target identity and current evidence or be labeled assumption/unknown.

Deliver each output as the artifact itself (tables, commands, patches, plans, records), not as a description of how it would be produced.

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
- `web-performance-diagnostics`
- `defect-remediation`
- `purposeful-motion-and-animation-engineering`
- `baseline-regression-control`

Never silently expand source, command, browser, data, credential, local-system, provider, or remote authority. Independent review, QA, audit, evidence acquisition, analysis, and triage never repair source. Setup and authentication never imply authority to perform the downstream action.
