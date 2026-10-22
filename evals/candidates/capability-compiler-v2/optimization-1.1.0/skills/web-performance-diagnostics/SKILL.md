---
name: web-performance-diagnostics
description: "Measure a frozen Web page or journey for navigation, network, caching, assets, rendering, and Core Web Vitals under declared conditions without repair. Use when A page or journey needs a page-load, network, caching or Core Web Vitals baseline under declared conditions; Someone asks why a page is slow and needs waterfall, asset and bundle evidence rather than one Lighthouse score. Do not use for: Profile component-level rendering and interaction latency (-> frontend-rendering-and-interaction-performance); Apply the approved Web performance fixes (-> defect-remediation)."
---

# Web Performance Diagnostics

## Responsibility

Measure a frozen Web page or journey for navigation, network, caching, assets, rendering, and Core Web Vitals under declared conditions without repair.

## Trigger

Use when the request matches any of:
- A page or journey needs a page-load, network, caching or Core Web Vitals baseline under declared conditions
- Someone asks why a page is slow and needs waterfall, asset and bundle evidence rather than one Lighthouse score

Do not use when:
- Profile component-level rendering and interaction latency. Route to `frontend-rendering-and-interaction-performance`.
- Apply the approved Web performance fixes. Route to `defect-remediation`.

## Required Inputs

- A web application, controlled sampling environment, network waterfall, and build information.

## Procedure

1. Freeze URL or build, source identity, journey, browser, device and network profile, cache mode, warmup, sample count, budgets, and third-party boundary.
2. Run approved local diagnostics and record navigation, Web Vitals, waterfall, CPU, assets, cache, server timing, and screenshots or traces.
3. Report distributions, outliers, repeatable bottlenecks, suspected ownership, and environmental uncertainty rather than one score.
4. Return baseline and prioritized hypotheses without editing source, changing production, or claiming user impact beyond conditions.

## Domain Guidance

- Core Web Vitals thresholds at p75: LCP good <= 2.5 s, poor > 4 s; INP good <= 200 ms, poor > 500 ms; CLS good <= 0.1, poor > 0.25. Label every number as lab or field data and never mix them in one verdict.
- Detect the framework and bundler from config files and package.json, then attribute large bundles to owning packages and check tree-shaking (sideEffects, usedExports, production mode) before proposing hypotheses.
- Field INP ownership sits here; component-level interaction traces belong to frontend-rendering-and-interaction-performance.
- Ownership: field and lab INP, LCP, CLS and other Core Web Vitals belong here; component-level interaction traces belong to frontend-rendering-and-interaction-performance.

## Output Contract

Produce:
- Web performance baseline
- Core Web Vitals and waterfall evidence
- repeatable bottleneck findings
- optimization hypotheses and limitations
- threshold table with lab or field label per metric

Every material action, command, result, finding, score, capture, provider receipt, or completion claim must bind to exact target identity and current evidence or be labeled assumption/unknown.

Deliver each output as the artifact itself (tables, commands, patches, plans, records), not as a description of how it would be produced.

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
- `frontend-rendering-and-interaction-performance`
- `defect-remediation`
- `website-audit-assessment`
- `baseline-regression-control`

Never silently expand source, command, browser, data, credential, local-system, provider, or remote authority. Independent review, QA, audit, evidence acquisition, analysis, and triage never repair source. Setup and authentication never imply authority to perform the downstream action.
