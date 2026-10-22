---
name: web-performance-diagnostics
description: Measure a frozen Web page or journey for navigation, network, caching, assets, rendering, and Core Web Vitals under declared conditions without repair. Do not use for profile component-level rendering and interaction latency or apply the approved web performance fixes.
---

# Web Performance Diagnostics

## Responsibility

Measure a frozen Web page or journey for navigation, network, caching, assets, rendering, and Core Web Vitals under declared conditions without repair.

## Trigger

Use when the requested outcome is: Measure a frozen Web page or journey for navigation, network, caching, assets, rendering, and Core Web Vitals under declared conditions without repair.

Do not use when:
- Profile component-level rendering and interaction latency. Route to `frontend-rendering-and-interaction-performance`.
- Apply the approved Web performance fixes. Route to `defect-remediation`.

## Required Inputs

- A web application, controlled sampling environment, network waterfall, and build information.

Also require exact target identity, authority, mutation boundary, evidence consumer, cleanup or rollback, and declared unknowns where applicable.

## Procedure

1. Freeze URL or build, source identity, journey, browser, device and network profile, cache mode, warmup, sample count, budgets, and third-party boundary.
2. Run approved local diagnostics and record navigation, Web Vitals, waterfall, CPU, assets, cache, server timing, and screenshots or traces.
3. Report distributions, outliers, repeatable bottlenecks, suspected ownership, and environmental uncertainty rather than one score.
4. Return baseline and prioritized hypotheses without editing source, changing production, or claiming user impact beyond conditions.

## Output Contract

Produce:
- Web performance baseline
- Core Web Vitals and waterfall evidence
- repeatable bottleneck findings
- optimization hypotheses and limitations

Every material action, command, result, finding, score, capture, provider receipt, or completion claim must bind to exact target identity and current evidence or be labeled assumption/unknown.

## Coverage

- `Core-Web-Vitals`
- `waterfall`
- `cache-mode`
- `network-profile`
- `warmup`
- `sample-count`
- `distribution`

## Hard Gates

- A Web performance claim requires repeated runs with recorded browser, device, network, cache, warmup, sample count, distribution, budget, and target identity; a single Lighthouse score cannot pass.
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
- `frontend-rendering-and-interaction-performance`
- `defect-remediation`
- `website-audit-assessment`
- `baseline-regression-control`

Never silently expand source, command, browser, data, credential, local-system, provider, or remote authority. Independent review, QA, audit, evidence acquisition, analysis, and triage never repair source. Setup and authentication never imply authority to perform the downstream action.
