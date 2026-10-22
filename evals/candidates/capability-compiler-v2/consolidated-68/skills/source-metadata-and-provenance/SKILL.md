---
name: source-metadata-and-provenance
description: "Preserve exact source identity, revision, artifact lineage, license or provenance facts, and the boundary between evidence, inference, and interpretation without provider mutation. Use when An artifact, unit or claim needs its exact source, revision, license and lineage recorded before it is cited or reused; Someone must separate what was observed from what a provider claims or an analyst inferred. Do not use for: Update release documentation from a shipped diff (-> release-documentation-maintenance); Record material that is historical or deferred and not current guidance (-> reference-library-and-deferred-material)."
---

# Source Metadata And Provenance

## Responsibility

Preserve exact source identity, revision, artifact lineage, license or provenance facts, and the boundary between evidence, inference, and interpretation without provider mutation.

## Trigger

Use when the request matches any of:
- An artifact, unit or claim needs its exact source, revision, license and lineage recorded before it is cited or reused
- Someone must separate what was observed from what a provider claims or an analyst inferred

Do not use when:
- Update release documentation from a shipped diff. Route to `release-documentation-maintenance`.
- Record material that is historical or deferred and not current guidance. Route to `reference-library-and-deferred-material`.

## Required Inputs

- A curated unit, source declaration, citation context, or provenance concern.

## Procedure

1. Freeze source repositories or origins, refs, versions, artifacts, licenses, ownership, timestamps, transformations, environments, and evidence consumers.
2. Record exact source identity, commit or version, normalized artifact hashes, lineage edges, transformation commands where supplied, license and use constraints, and freshness.
3. Separate observed metadata, provider claims, analyst inference, interpretation, unknowns, and conflicts; never infer deployment from commit or association.
4. Return a bounded provenance record and gaps; no source, provider, release, service identity, or deployment mutation.

## Domain Guidance

- License fields use SPDX identifiers (for example Apache-2.0, MIT) plus the exact file and line of the license text; unknown stays unknown.
- Lineage is a list of edges: input artifact hash, transformation (command or tool and version), output artifact hash, timestamp.
- Keep commit, build, release association, deployment and production health as separate facts; never infer one from another.

## Output Contract

Produce:
- source and revision identity record
- artifact lineage and normalized hashes
- license and use constraints
- fact, inference, interpretation, and gap labels

Every material command, request, observation, provider response, finding, decision recommendation, or completion claim must bind to exact target identity and current evidence or be labeled assumption/unknown.

Deliver each output as the artifact itself (tables, commands, patches, plans, records), not as a description of how it would be produced.

## Coverage

- `source-identity`
- `revision`
- `artifact-lineage`
- `license`
- `normalized-hash`
- `fact-inference-interpretation`
- `no-deploy-inference`

## Hard Gates

- Provenance must distinguish observed identity, provider claim, inference, and interpretation; commit, build, release association, deployment, and production health are separate facts.
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

## Status Mapping

- `passed`: the atomic output and every gate have current target-bound evidence.
- `needs-input`: a requestable target, source, authority, evidence, governance term, or decision is absent. Deliver every supported part first and name the owner for the missing part.
- `blocked`: safe work requires prohibited access, unavailable authority, secret values, stale evidence, or an incompatible identity.
- `failed`: the authorized action ran but a deterministic gate or required output failed.

## Non-Responsibilities

Adjacent capabilities:
- `release-observability-configuration`
- `service-identity-remapping`
- `artifact-persistence-and-tool-actions`
- `reference-library-and-deferred-material`
- `release-documentation-maintenance`

Never silently expand local, repository, provider, production, telemetry, incident, or release authority. Preflight never changes; observation never recovers; coordination never performs specialist actions; rollback never invents a target; one remote authorization never cascades to another action.
