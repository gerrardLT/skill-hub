---
name: ui-review-scope-and-evidence-acquisition
description: Define independent UI review scope and acquire authorized current rendered evidence without evaluating findings or repairing source. Do not use for critique the completed capture set and prioritize ui defects or modify product source in response to previously accepted findings.
---

# Ui Review Scope And Evidence Acquisition

## Responsibility

Define independent UI review scope and acquire authorized current rendered evidence without evaluating findings or repairing source.

## Trigger

Use when the requested outcome is: Define independent UI review scope and acquire authorized current rendered evidence without evaluating findings or repairing source.

Do not use when:
- Critique the completed capture set and prioritize UI defects. Route to `rendered-ui-critique-and-release-disposition`.
- Modify product source in response to previously accepted findings. Route to `ui-remediation`.

## Required Inputs

- A UI brief, target files, runtime, rendered surfaces, and review criteria.

Also require source or render identity, authorization, target surfaces, supported states, decision owner, and declared unknowns where applicable.

## Procedure

1. Freeze changed surfaces, user tasks, acceptance criteria, supported browsers and devices, high-risk states, source identity, and review independence.
2. Build a route-state-viewport-theme-input-motion matrix with explicit inclusions, exclusions, and rationale.
3. Use only approved local commands and authorized external reads to capture screenshots, traces, recordings, accessibility snapshots, and console or network evidence.
4. Bind each artifact to timestamp, source revision, environment, route, state setup, viewport, zoom, input mode, theme, tool, and hash.
5. Assess evidence completeness only; route a complete manifest to critique or return needs-input/blocked without judging design quality.

## Output Contract

Produce:
- UI review scope matrix
- rendered evidence bundle
- capture provenance manifest
- evidence completeness result

Every material design choice, implementation claim, finding, score, capture, or disposition must link to supplied authority or current evidence, or be labeled assumption/unknown.

## UI Coverage

- `scope-matrix`
- `capture`
- `provenance`
- `current-evidence`
- `independence`
- `no-critique`

## Hard Gates

- No capture is review evidence unless its source revision, runtime, route, state, viewport, zoom or scale, input mode, timestamp, tool, and hash are recorded and current.
- Preserve product truth, user task, semantic order, authentic content, accessibility, responsive behavior, state coverage, source identity, and authority boundaries where applicable.
- Return `needs-input` when an identifiable owner can supply a missing requirement, asset authority, capture, state, or decision.
- Return `blocked` when required authorization, safe mutation scope, rendered evidence, tooling, or specialist dependency is unavailable.

## Rendered Evidence

When this capability assesses or validates a rendered interface, static source inspection, DOM assertions, model self-attestation, or a single ideal screenshot are insufficient. Require current provenance-bound captures or traces for the declared routes, states, viewports, zoom, input modes, themes, and motion behavior. Missing evidence returns `needs-input` or `blocked`, never `passed`.

## Status Mapping

- `passed`: output contract and every hard gate are satisfied with current evidence.
- `needs-input`: a requestable source, state, decision, capture, or authorization term is missing.
- `blocked`: proceeding would exceed authority, mix review with repair, or rely on unavailable critical evidence.
- `failed`: authorized work ran but a deterministic gate or required output failed.

## Non-Responsibilities

Does not approve upstream product decisions, expand authority, or perform remote writes beyond its explicit permission identity.

Adjacent capabilities:
- `rendered-ui-critique-and-release-disposition`
- `evidence-based-ui-review-and-release-gates`
- `ui-remediation`
- `cross-domain-ui-preflight-checklists`

Never perform remote Git, external-system writes, merge, deploy, release, or an adjacent capability's work. Review and preflight capabilities never repair product source; evidence-acquisition capabilities never issue design findings.
