---
name: artifact-persistence-and-tool-actions
description: Select the already-authorized tool action and persist one validated lifecycle artifact at the declared bounded location without expanding the task. Do not use for render and validate the document's layout, links, and accessibility before persistence or publish this artifact to an external provider or repository.
---

# Artifact Persistence And Tool Actions

## Responsibility

Select the already-authorized tool action and persist one validated lifecycle artifact at the declared bounded location without expanding the task.

## Trigger

Use when the requested outcome is: Select the already-authorized tool action and persist one validated lifecycle artifact at the declared bounded location without expanding the task.

Do not use when:
- Render and validate the document's layout, links, and accessibility before persistence. Route to `document-rendering-and-validation`.
- Publish this artifact to an external provider or repository. Route to `evaluation-dataset-publication`.

## Required Inputs

- A validated task, tool boundary, output location, and write authorization.

Also require exact target identity, authority, mutation boundary, evidence consumer, cleanup or rollback, and declared unknowns where applicable.

## Procedure

1. Verify the validated input, exact tool or write action, destination class, overwrite policy, authorization, and expected artifact identity.
2. Refuse path escape, undeclared files, source mutation disguised as persistence, remote targets, or destructive replacement without recovery.
3. Perform only the bounded action; preserve source bytes or declared normalization and record before/after identity.
4. Return the saved artifact or explicit no-write outcome with path, tool, exit status when applicable, hash, and limitations.

## Output Contract

Produce:
- bounded tool-action record
- persisted lifecycle artifact or no-write outcome
- path and hash evidence
- overwrite or recovery record

Every material action, command, result, finding, score, capture, provider receipt, or completion claim must bind to exact target identity and current evidence or be labeled assumption/unknown.

## Coverage

- `bounded-action`
- `declared-path`
- `path-containment`
- `artifact-hash`
- `no-extra-files`
- `recovery`

## Hard Gates

- Persistence authority applies only to the declared artifact and location; it cannot authorize adjacent analysis, product-source edits, external publication, or additional files.
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
- `document-rendering-and-validation`
- `evaluation-dataset-publication`
- `completion-evidence-gate`
- `workflow-skill-authoring`

Never silently expand source, command, browser, data, credential, local-system, provider, or remote authority. Independent review, QA, audit, evidence acquisition, analysis, and triage never repair source. Setup and authentication never imply authority to perform the downstream action.
