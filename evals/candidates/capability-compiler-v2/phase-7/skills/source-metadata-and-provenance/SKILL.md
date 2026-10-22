---
name: source-metadata-and-provenance
description: Preserve exact source identity, revision, artifact lineage, license or provenance facts, and the boundary between evidence, inference, and interpretation without provider mutation. Do not use for configure release and commit association in an observability provider or remap a telemetry service identity in the provider.
---

# Source Metadata And Provenance

## Responsibility

Preserve exact source identity, revision, artifact lineage, license or provenance facts, and the boundary between evidence, inference, and interpretation without provider mutation.

## Trigger

Use when the requested outcome is: Preserve exact source identity, revision, artifact lineage, license or provenance facts, and the boundary between evidence, inference, and interpretation without provider mutation.

Do not use when:
- Configure release and commit association in an observability provider. Route to `release-observability-configuration`.
- Remap a telemetry service identity in the provider. Route to `service-identity-remapping`.

## Required Inputs

- A curated unit, source declaration, citation context, or provenance concern.

Also require exact repository, provider, environment, service, incident, release, artifact, telemetry, or local destination identity; authority; evidence window; and recovery or cleanup where applicable.

## Procedure

1. Freeze source repositories or origins, refs, versions, artifacts, licenses, ownership, timestamps, transformations, environments, and evidence consumers.
2. Record exact source identity, commit or version, normalized artifact hashes, lineage edges, transformation commands where supplied, license and use constraints, and freshness.
3. Separate observed metadata, provider claims, analyst inference, interpretation, unknowns, and conflicts; never infer deployment from commit or association.
4. Return a bounded provenance record and gaps; no source, provider, release, service identity, or deployment mutation.

## Output Contract

Produce:
- source and revision identity record
- artifact lineage and normalized hashes
- license and use constraints
- fact, inference, interpretation, and gap labels

Every material command, request, observation, provider response, finding, decision recommendation, or completion claim must bind to exact target identity and current evidence or be labeled assumption/unknown.

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
- Preserve source, ref, pull request, artifact, release, environment, provider, service, incident, telemetry, baseline, or local-record identity; authority, evidence, limitations, cleanup, and recovery remain explicit.
- Return `needs-input` when a named owner can supply missing scope, target, authority, data governance, evidence, rollback, or decision.
- Return `blocked` when proceeding would expose credentials, exceed mutation authority, use stale evidence, mix readiness with action, mix observation with rollback, or perform undeclared remote or production work.

## Status Mapping

- `passed`: the atomic output and every gate have current target-bound evidence.
- `needs-input`: a requestable target, source, authority, evidence, governance term, or decision is absent.
- `blocked`: safe work requires prohibited access, unavailable authority, secret values, stale evidence, or an incompatible identity.
- `failed`: the authorized action ran but a deterministic gate or required output failed.

## Non-Responsibilities

Does not approve upstream product decisions, expand authority, or perform remote writes beyond its explicit permission identity.

Adjacent capabilities:
- `release-observability-configuration`
- `service-identity-remapping`
- `artifact-persistence-and-tool-actions`
- `reference-library-and-deferred-material`

Never silently expand local, repository, provider, production, telemetry, incident, or release authority. Preflight never changes; observation never recovers; coordination never performs specialist actions; rollback never invents a target; one remote authorization never cascades to another action.
