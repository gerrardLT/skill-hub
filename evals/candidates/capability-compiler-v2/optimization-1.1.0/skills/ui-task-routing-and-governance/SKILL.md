---
name: ui-task-routing-and-governance
description: "Classify UI work, authorization, current lifecycle state, target surfaces, evidence needs, and one next atomic capability without doing downstream design or review. Use when A UI request arrives and someone must classify design, redesign, token import, implementation, preflight, capture, critique, repair or release intent; A UI task needs its write boundary and the next single UI capability decided before any work. Do not use for: Create the actual design direction and user-flow contract (-> design-context-and-direction-contract); Capture browser renders and traces for independent review (-> ui-review-scope-and-evidence-acquisition); Classify a request that is not UI-only or spans several domains (-> context-intake-and-routing); Sequence capabilities for a workflow that no Recipe covers (-> workflow-orchestration-and-lifecycle)."
---

# UI Task Routing And Governance

## Responsibility

Classify UI work, authorization, current lifecycle state, target surfaces, evidence needs, and one next atomic capability without doing downstream design or review.

## Trigger

Use when the request matches any of:
- A UI request arrives and someone must classify design, redesign, token import, implementation, preflight, capture, critique, repair or release intent
- A UI task needs its write boundary and the next single UI capability decided before any work

Do not use when:
- Create the actual design direction and user-flow contract. Route to `design-context-and-direction-contract`.
- Capture browser renders and traces for independent review. Route to `ui-review-scope-and-evidence-acquisition`.
- Classify a request that is not UI-only or spans several domains. Route to `context-intake-and-routing`.
- Sequence capabilities for a workflow that no Recipe covers. Route to `workflow-orchestration-and-lifecycle`.

## Required Inputs

- A UI request, project state, existing interface, target files, authorization, and design artifacts.

## Procedure

1. Inventory requested outcome, supplied artifacts, product authority, target surfaces, current source or render state, external sources, and explicit exclusions.
2. Classify new design, existing redesign, token import, implementation, preflight, evidence capture, critique, repair, or release-decision intent.
3. Determine source-write, artifact-write, local-exec, external-read, and human-decision boundaries before route selection.
4. Identify missing prerequisites, incompatible identities, applicable specialist branches, and stop conditions.
5. Return one next capability and conditional follow-ups only; preserve unknowns and perform no downstream work.

## Domain Guidance

- Routing ownership: this Skill classifies UI-only work; cross-domain requests go to context-intake-and-routing and Recipe selection belongs to the router.

## Output Contract

Produce:
- UI task classification
- authorization and write-boundary record
- next-capability route
- missing-input and stop-condition list

Every material design choice, implementation claim, finding, score, capture, or disposition must link to supplied authority or current evidence, or be labeled assumption/unknown.

Deliver each output as the artifact itself (tables, commands, patches, plans, records), not as a description of how it would be produced.

## UI Coverage

- `classification`
- `authorization`
- `write-boundary`
- `next-capability`
- `no-downstream-work`

## Hard Gates

- Routing must not smuggle design, review, source mutation, browser capture, or release judgment into the intake artifact.
- Review, evidence acquisition, preflight, and preservation audit never imply source remediation or release authority.
- Preserve product truth, user task, semantic order, authentic content, accessibility, responsive behavior, state coverage, source identity, and authority boundaries where applicable.
- Return `needs-input` when an identifiable owner can supply a missing requirement, asset authority, capture, state, or decision.
- Return `blocked` when required authorization, safe mutation scope, rendered evidence, tooling, or specialist dependency is unavailable.
- Deliver every part the supplied evidence and authority support, label assumptions, and list each missing item with the owner who can supply it; `needs-input` or `blocked` applies to the unsupported part, not to the whole deliverable.

## Forbidden Actions

- remote Git, merge, deploy, release, cloud mutation, or external-system write
- invent product facts, brand authority, copy claims, customer data, assets, evidence, or approval
- perform an adjacent capability or combine independent review with source repair
- treat static inspection, stale capture, or model self-report as current rendered evidence
- claim evaluation, approval, release, or completion evidence that has not been produced

## Status Mapping

- `passed`: output contract and every hard gate are satisfied with current evidence.
- `needs-input`: a requestable source, state, decision, capture, or authorization term is missing. Deliver every supported part first and name the owner for the missing part.
- `blocked`: proceeding would exceed authority, mix review with repair, or rely on unavailable critical evidence.
- `failed`: authorized work ran but a deterministic gate or required output failed.

## Non-Responsibilities

Adjacent capabilities:
- `design-context-and-direction-contract`
- `existing-interface-redesign-and-preservation`
- `ui-review-scope-and-evidence-acquisition`
- `ui-remediation`
- `context-intake-and-routing`
- `workflow-orchestration-and-lifecycle`

Never perform remote Git, external-system writes, merge, deploy, release, or an adjacent capability's work. Review and preflight capabilities never repair product source; evidence-acquisition capabilities never issue design findings.
