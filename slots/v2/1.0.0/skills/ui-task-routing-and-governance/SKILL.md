---
name: ui-task-routing-and-governance
description: Classify UI work, authorization, current lifecycle state, target surfaces, evidence needs, and one next atomic capability without doing downstream design or review. Do not use for create the actual design direction and user-flow contract or capture browser renders and traces for independent review.
---

# Ui Task Routing And Governance

## Responsibility

Classify UI work, authorization, current lifecycle state, target surfaces, evidence needs, and one next atomic capability without doing downstream design or review.

## Trigger

Use when the requested outcome is: Classify UI work, authorization, current lifecycle state, target surfaces, evidence needs, and one next atomic capability without doing downstream design or review.

Do not use when:
- Create the actual design direction and user-flow contract. Route to `design-context-and-direction-contract`.
- Capture browser renders and traces for independent review. Route to `ui-review-scope-and-evidence-acquisition`.

## Required Inputs

- A UI request, project state, existing interface, target files, authorization, and design artifacts.

Also require source or render identity, authorization, target surfaces, supported states, decision owner, and declared unknowns where applicable.

## Procedure

1. Inventory requested outcome, supplied artifacts, product authority, target surfaces, current source or render state, external sources, and explicit exclusions.
2. Classify new design, existing redesign, token import, implementation, preflight, evidence capture, critique, repair, or release-decision intent.
3. Determine source-write, artifact-write, local-exec, external-read, and human-decision boundaries before route selection.
4. Identify missing prerequisites, incompatible identities, applicable specialist branches, and stop conditions.
5. Return one next capability and conditional follow-ups only; preserve unknowns and perform no downstream work.

## Output Contract

Produce:
- UI task classification
- authorization and write-boundary record
- next-capability route
- missing-input and stop-condition list

Every material design choice, implementation claim, finding, score, capture, or disposition must link to supplied authority or current evidence, or be labeled assumption/unknown.

## UI Coverage

- `classification`
- `authorization`
- `write-boundary`
- `next-capability`
- `no-downstream-work`

## Hard Gates

- Routing must not smuggle design, review, source mutation, browser capture, or release judgment into the intake artifact.
- Preserve product truth, user task, semantic order, authentic content, accessibility, responsive behavior, state coverage, source identity, and authority boundaries where applicable.
- Return `needs-input` when an identifiable owner can supply a missing requirement, asset authority, capture, state, or decision.
- Return `blocked` when required authorization, safe mutation scope, rendered evidence, tooling, or specialist dependency is unavailable.

## Status Mapping

- `passed`: output contract and every hard gate are satisfied with current evidence.
- `needs-input`: a requestable source, state, decision, capture, or authorization term is missing.
- `blocked`: proceeding would exceed authority, mix review with repair, or rely on unavailable critical evidence.
- `failed`: authorized work ran but a deterministic gate or required output failed.

## Non-Responsibilities

Does not approve upstream product decisions, expand authority, or perform remote writes beyond its explicit permission identity.

Adjacent capabilities:
- `design-context-and-direction-contract`
- `existing-interface-redesign-and-preservation`
- `ui-review-scope-and-evidence-acquisition`
- `ui-remediation`

Never perform remote Git, external-system writes, merge, deploy, release, or an adjacent capability's work. Review and preflight capabilities never repair product source; evidence-acquisition capabilities never issue design findings.
