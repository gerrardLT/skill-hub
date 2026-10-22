---
name: frontend-runtime-boundaries-and-dependency-safety
description: Audit and minimally repair authorized frontend source so server-only logic, credentials, privileged actions, assets, dependencies, and runtime assumptions remain on safe explicit boundaries. Do not use for design the visual token and component foundation for the interface or benchmark and optimize frontend rendering and interaction performance.
---

# Frontend Runtime Boundaries And Dependency Safety

## Responsibility

Audit and minimally repair authorized frontend source so server-only logic, credentials, privileged actions, assets, dependencies, and runtime assumptions remain on safe explicit boundaries.

## Trigger

Use when the requested outcome is: Audit and minimally repair authorized frontend source so server-only logic, credentials, privileged actions, assets, dependencies, and runtime assumptions remain on safe explicit boundaries.

Do not use when:
- Design the visual token and component foundation for the interface. Route to `design-system-foundation-and-token-extraction`.
- Benchmark and optimize frontend rendering and interaction performance. Route to `frontend-rendering-and-interaction-performance`.

## Required Inputs

- A frontend implementation, dependency graph, rendering environment, and integration constraints.

Also require target identity, authorization, trust boundaries, data classes, decision owner, compatibility window, and declared unknowns where applicable.

## Procedure

1. Freeze authorized source scope, rendering environments, entry points, dependency graph, bundler behavior, environment variables, assets, browser targets, and existing tests.
2. Trace client imports, server-only modules, secrets, privileged APIs, dynamic code, third-party scripts, assets, globals, hydration, and environment branches across the build boundary.
3. Prefer platform or existing dependencies; remove or isolate unsafe or unnecessary packages and move privileged computation or credentials behind server-enforced interfaces.
4. Apply the smallest authorized source/config patch with explicit client-server modules, asset handling, runtime guards, and dependency rationale.
5. Define host-run build, bundle, browser, SSR or hydration, and security checks; report unavailable verification and never expose secret values.

## Output Contract

Produce:
- runtime-boundary audit
- minimal authorized source or dependency patch
- dependency and environment decision
- host verification and residual-risk plan

Every material fact, boundary, recommendation, finding, test claim, migration step, or risk must cite supplied or authorized evidence or be labeled assumption/unknown.

## Coverage

- `client-server-boundary`
- `no-client-secret`
- `server-enforcement`
- `dependency-safety`
- `assets`
- `SSR-hydration`
- `host-verification`

## Hard Gates

- No server credential, secret-derived value, privileged authorization decision, filesystem or process API, or unsafe dynamic dependency may cross into a client bundle or browser-executable path.
- Preserve trust boundaries, authorization, data and secret governance, compatibility, migration, rollback or containment, source identity, counterevidence, and residual risk where applicable.
- Return `needs-input` when a named owner can supply a missing fact, policy, evidence, or approval.
- Return `blocked` when safe analysis or mutation would require unavailable authority, secret values, prohibited tests, remote writes, or unresolved high-impact risk.

## Status Mapping

- `passed`: output contract and every hard gate are satisfied with current evidence.
- `needs-input`: a requestable source, policy, compatibility fact, or decision is missing.
- `blocked`: proceeding would exceed authority, access secret values, mutate production, or cross a prohibited safety boundary.
- `failed`: authorized work ran but a deterministic gate or required output failed.

## Non-Responsibilities

Does not approve upstream product decisions, expand authority, or perform remote writes beyond its explicit permission identity.

Adjacent capabilities:
- `design-system-foundation-and-token-extraction`
- `frontend-rendering-and-interaction-performance`
- `secrets-and-environment-governance`
- `authorization-and-permission-contracts`

Never access or emit secret values, mutate production data or provider policy, grant AI action rights, execute remote Git, merge, deploy, release, or perform an adjacent capability. Review, reporting, and audit candidates never repair source.
