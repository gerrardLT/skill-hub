---
name: frontend-runtime-boundaries-and-dependency-safety
description: "Audit authorized frontend source so server-only logic, credentials, privileged actions, assets, dependencies, and runtime assumptions stay on safe explicit boundaries, and hand accepted repairs to the repair owner without editing source. Use when A frontend build may leak server-only code, secrets or privileged logic into the browser bundle; Someone asks whether client and server boundaries, third-party scripts and dependencies are safe before release. Do not use for: Design the visual token and component foundation for the interface (-> design-system-foundation-and-token-extraction); Benchmark and optimize frontend rendering and interaction performance (-> frontend-rendering-and-interaction-performance); Apply the accepted boundary or dependency repairs to source (-> defect-remediation)."
---

# Frontend Runtime Boundaries And Dependency Safety

## Responsibility

Audit authorized frontend source so server-only logic, credentials, privileged actions, assets, dependencies, and runtime assumptions stay on safe explicit boundaries, and hand accepted repairs to the repair owner without editing source.

## Trigger

Use when the request matches any of:
- A frontend build may leak server-only code, secrets or privileged logic into the browser bundle
- Someone asks whether client and server boundaries, third-party scripts and dependencies are safe before release

Do not use when:
- Design the visual token and component foundation for the interface. Route to `design-system-foundation-and-token-extraction`.
- Benchmark and optimize frontend rendering and interaction performance. Route to `frontend-rendering-and-interaction-performance`.
- Apply the accepted boundary or dependency repairs to source. Route to `defect-remediation`.

## Required Inputs

- A frontend implementation, dependency graph, rendering environment, and integration constraints.

## Procedure

1. Freeze authorized source scope, rendering environments, entry points, dependency graph, bundler behavior, environment variables, assets, browser targets, and existing tests.
2. Trace client imports, server-only modules, secrets, privileged APIs, dynamic code, third-party scripts, assets, globals, hydration, and environment branches across the build boundary.
3. Prefer platform or existing dependencies; identify unsafe or unnecessary packages and the server-enforced interface that should hold privileged computation or credentials.
4. Write each finding with file and line, the boundary crossed, the consequence, and the smallest recommended change, ready for defect-remediation after the owner accepts it.
5. Define host-run build, bundle, browser, SSR or hydration, and security checks for the repair to pass; report unavailable verification and never expose secret values.

## Domain Guidance

- React Server Components: global state works only in client components; wrap providers in a 'use client' component and keep interactive leaves isolated. A server-only module imported from a client component is a boundary violation.
- Audit only. Repairs are a separate accepted action owned by defect-remediation.

## Output Contract

Produce:
- runtime-boundary audit
- findings with file, line, boundary crossed and recommended change
- dependency and environment decision
- host verification and residual-risk plan

Every material fact, boundary, recommendation, finding, test claim, migration step, or risk must cite supplied or authorized evidence or be labeled assumption/unknown.

Deliver each output as the artifact itself (tables, commands, patches, plans, records), not as a description of how it would be produced.

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
- Review, reporting, contract, and audit candidates never imply implementation, live policy change, production mutation, or risk acceptance.
- Preserve trust boundaries, authorization, data and secret governance, compatibility, migration, rollback or containment, source identity, counterevidence, and residual risk where applicable.
- Return `needs-input` when a named owner can supply a missing fact, policy, evidence, or approval.
- Return `blocked` when safe analysis or mutation would require unavailable authority, secret values, prohibited tests, remote writes, or unresolved high-impact risk.
- Deliver every part the supplied evidence and authority support, label assumptions, and list each missing item with the owner who can supply it; `needs-input` or `blocked` applies to the unsupported part, not to the whole deliverable.

## Forbidden Actions

- request, read, print, persist, hash, or transmit secret values
- remote Git, merge, deploy, release, provider-policy mutation, production-data mutation, or AI action-right activation
- invent architecture facts, data rights, authorization, evidence, approval, migration safety, or risk acceptance
- combine independent review or audit with source remediation
- claim evaluation, approval, release, or completion evidence that has not been produced

## Status Mapping

- `passed`: output contract and every hard gate are satisfied with current evidence.
- `needs-input`: a requestable source, policy, compatibility fact, or decision is missing. Deliver every supported part first and name the owner for the missing part.
- `blocked`: proceeding would exceed authority, access secret values, mutate production, or cross a prohibited safety boundary.
- `failed`: authorized work ran but a deterministic gate or required output failed.

## Non-Responsibilities

Adjacent capabilities:
- `design-system-foundation-and-token-extraction`
- `frontend-rendering-and-interaction-performance`
- `secrets-and-environment-governance`
- `authorization-and-permission-contracts`
- `defect-remediation`

Never access or emit secret values, mutate production data or provider policy, grant AI action rights, execute remote Git, merge, deploy, release, or perform an adjacent capability. Review, reporting, and audit candidates never repair source.
