---
name: design-context-and-direction-contract
description: "Consolidated capability with 3 selectable modes: design-context-and-direction-contract; document-and-artifact-governance; ui-task-routing-and-governance. Choose exactly one mode per invocation."
version: 1.1.0-consolidated
modes: [design-context-and-direction-contract, document-and-artifact-governance, ui-task-routing-and-governance]
---

# Design Context And Direction Contract

## Responsibility

Consolidated capability covering 3 related modes: Translate approved product behavior, audience, brand evidence, surface mode, content needs, and success criteria into an auditable design direction contract.; Define artifact identities, owners, source of truth, lifecycle state, staleness, retention, and invalidation without authoring their content.; Classify UI work, authorization, current lifecycle state, target surfaces, evidence needs, and one next atomic capability without doing downstream design or review.

## Mode selection

This capability has several distinct modes. Read this table first, pick exactly one
mode for the current request, then follow only that mode's section. Do not blend
modes: each carries its own permission identity, gates, and stop conditions. The
permission column is binding - a run uses the permission of the mode it selected,
never the widest permission in this document.

| Mode | Permission | Use when | Routes elsewhere |
| --- | --- | --- | --- |
| `design-context-and-direction-contract` | `workspace-write` | A new or approved-redesign interface needs a design direction tied to product behavior, audience and brand evidence; Someone asks for user flow, hierarchy, spatial and visual decisions with the author | Implement the responsive layouts and component source from an approved direction (-> responsive-layout-and-spatial-compo |
| `document-and-artifact-governance` | `workspace-write` | A project needs rules for which documents exist, who owns them, which copy is the source of truth and when they go stale; Artifacts are drifting or duplicated and someone must define lifecycle state,  | Write the actual architecture explanation document (-> documentation-authoring); Persist a completed artifact to disk (- |
| `ui-task-routing-and-governance` | `read-only` | A UI request arrives and someone must classify design, redesign, token import, implementation, preflight, capture, critique, repair or release intent; A UI task needs its write boundary and the next s | Create the actual design direction and user-flow contract (-> design-context-and-direction-contract); Capture browser re |

## Mode: `design-context-and-direction-contract`

### design-context-and-direction-contract

#### Responsibility

Translate approved product behavior, audience, brand evidence, surface mode, content needs, and success criteria into an auditable design direction contract.

#### Trigger

Use when the request matches any of:
- A new or approved-redesign interface needs a design direction tied to product behavior, audience and brand evidence
- Someone asks for user flow, hierarchy, spatial and visual decisions with the authority behind each choice

Do not use when:
- Implement the responsive layouts and component source from an approved direction. Route to `responsive-layout-and-spatial-composition`.
- Independently critique the rendered implementation and issue a release recommendation. Route to `rendered-ui-critique-and-release-disposition`.
- Implement the visual grammar, type, color and anti-template rules. Route to `visual-language-and-anti-template-controls`.

#### Required Inputs

- Product facts, a brief, design assets, tokens, components, surface context, and references.

#### Procedure

1. Classify product facts, acceptance criteria, audience evidence, brand assets, existing tokens, platform constraints, references, conflicts, and unknowns.
2. Choose the surface mode and state the user flow, information hierarchy, content priorities, and success criteria before visual styling.
3. Derive a spatial thesis, density, typography role, color role, imagery or icon direction, and interaction tone from cited authority.
4. Separate required constraints, reversible proposals, unresolved taste decisions, and forbidden unsupported decoration.
5. Emit a contract with invariants, target surfaces, decision owners, and handoff gates; do not implement or approve release.

#### Domain Guidance

- Intake in one consolidated question that pre-fills what the codebase and assets already show (product, audience, project type, existing patterns, constraints); ask only for what cannot be inferred.
- Make the spatial thesis concrete: derive a width budget, column structure, padding and density from the supplied content and viewports, with the numbers shown, instead of deferring exact values.
- State the sort order and severity ordering that drive hierarchy (for example critical first), and trace each major choice to product purpose, audience, content or brand authority; untraceable choices are listed as taste decisions for the owner.

#### Output Contract

Produce:
- design evidence read
- user-flow and information-hierarchy contract
- visual and spatial direction
- design decision ledger

Every material design choice, implementation claim, finding, score, capture, or disposition must link to supplied authority or current evidence, or be labeled assumption/unknown.

Deliver each output as the artifact itself (tables, commands, patches, plans, records), not as a description of how it would be produced.

#### UI Coverage

- `user-flow`
- `information-hierarchy`
- `brand-authority`
- `spatial-thesis`
- `success-criteria`
- `taste-decision`

#### Hard Gates

- The design direction cannot pass unless each major visual or spatial choice traces to product purpose, audience, content, brand authority, or an explicitly human-owned taste decision.
- Review, evidence acquisition, preflight, and preservation audit never imply source remediation or release authority.
- Preserve product truth, user task, semantic order, authentic content, accessibility, responsive behavior, state coverage, source identity, and authority boundaries where applicable.
- Return `needs-input` when an identifiable owner can supply a missing requirement, asset authority, capture, state, or decision.
- Return `blocked` when required authorization, safe mutation scope, rendered evidence, tooling, or specialist dependency is unavailable.
- Deliver every part the supplied evidence and authority support, label assumptions, and list each missing item with the owner who can supply it; `needs-input` or `blocked` applies to the unsupported part, not to the whole deliverable.

#### Forbidden Actions

- remote Git, merge, deploy, release, cloud mutation, or external-system write
- invent product facts, brand authority, copy claims, customer data, assets, evidence, or approval
- perform an adjacent capability or combine independent review with source repair
- treat static inspection, stale capture, or model self-report as current rendered evidence
- claim evaluation, approval, release, or completion evidence that has not been produced

#### Human Design Authority

The Skill may preserve evidence, alternatives, tradeoffs, findings, and a recommendation. Final taste selection, prototype promotion, accepted risk, scope approval, source-repair approval, and release disposition remain explicit human decisions with a named owner.

#### Status Mapping

- `passed`: output contract and every hard gate are satisfied with current evidence.
- `needs-input`: a requestable source, state, decision, capture, or authorization term is missing. Deliver every supported part first and name the owner for the missing part.
- `blocked`: proceeding would exceed authority, mix review with repair, or rely on unavailable critical evidence.
- `failed`: authorized work ran but a deterministic gate or required output failed.

#### Non-Responsibilities

Adjacent capabilities:
- `ui-task-routing-and-governance`
- `visual-language-and-anti-template-controls`
- `responsive-layout-and-spatial-composition`
- `rendered-ui-critique-and-release-disposition`

Never perform remote Git, external-system writes, merge, deploy, release, or an adjacent capability's work. Review and preflight capabilities never repair product source; evidence-acquisition capabilities never issue design findings.

## Mode: `document-and-artifact-governance`

### document-and-artifact-governance

#### Responsibility

Define artifact identities, owners, source of truth, lifecycle state, staleness, retention, and invalidation without authoring their content.

#### Trigger

Use when the request matches any of:
- A project needs rules for which documents exist, who owns them, which copy is the source of truth and when they go stale
- Artifacts are drifting or duplicated and someone must define lifecycle state, retention and invalidation

Do not use when:
- Write the actual architecture explanation document. Route to `documentation-authoring`.
- Persist a completed artifact to disk. Route to `artifact-persistence-and-tool-actions`.

#### Required Inputs

- A document or artifact purpose, audience, source evidence, and required fields.

#### Procedure

1. Inventory artifact types, consumers, producers, authority, and trust-boundary crossings.
2. Assign stable identity, owner, canonical location, state, and replacement rules.
3. Define required metadata, evidence links, retention, deletion, and access boundary.
4. Define staleness and upstream-change invalidation rules.
5. Publish the governance map and unresolved ownership gaps.

#### Domain Guidance

- Default lifecycle states: draft, approved, superseded, stale, retired. A state change needs an owner and a reason; a change to an upstream artifact marks dependents stale until reviewed.
- Default staleness triggers: upstream artifact hash changed, owner change, review date passed, referenced system version changed.
- Define identity (stable id, canonical location), metadata, retention and deletion for each artifact class. This governance method is authored; the cited sources are document templates.

#### Output Contract

Produce:
- artifact registry
- ownership matrix
- state-transition policy
- staleness and retention rules

Every material claim, score, recommendation, or finding must link to a supplied or authorized source, or be labeled assumption/unknown.

Deliver each output as the artifact itself (tables, commands, patches, plans, records), not as a description of how it would be produced.

#### Hard Gates

- Governance may define where and when artifacts exist but must not invent, approve, or silently rewrite their contents.
- Preserve conflicts, counterevidence, unknowns, source identity, and authority boundaries.
- Return `needs-input` when an identifiable owner can supply a missing requirement or decision.
- Return `blocked` when required authority, evidence, governance, or a safe execution boundary is unavailable.
- Deliver every part the supplied evidence and authority support, label assumptions, and list each missing item with the owner who can supply it; `needs-input` or `blocked` applies to the unsupported part, not to the whole deliverable.

#### Forbidden Actions

- remote Git, pull-request mutation, merge, deploy, cloud mutation, or external-system write
- invent facts, evidence, authority, approval, or customer data
- perform adjacent or downstream capability responsibilities
- claim evaluation, approval, release, or completion evidence that has not been produced

#### Status Mapping

- `passed`: output contract and every hard gate are satisfied.
- `needs-input`: a requestable source, decision, or governance term is missing. Deliver every supported part first and name the owner for the missing part.
- `blocked`: proceeding would exceed authority, violate governance, or rely on unavailable critical evidence.
- `failed`: supplied inputs were processed but a deterministic gate or required output failed.

#### Non-Responsibilities

Adjacent capabilities:
- `documentation-authoring`
- `source-metadata-and-provenance`
- `artifact-persistence-and-tool-actions`

Never perform remote Git, external-system writes, merge, deploy, cloud mutation, participant recruitment/contact, or downstream implementation unless a different explicitly authorized capability owns that action.

## Mode: `ui-task-routing-and-governance`

### ui-task-routing-and-governance

#### Responsibility

Classify UI work, authorization, current lifecycle state, target surfaces, evidence needs, and one next atomic capability without doing downstream design or review.

#### Trigger

Use when the request matches any of:
- A UI request arrives and someone must classify design, redesign, token import, implementation, preflight, capture, critique, repair or release intent
- A UI task needs its write boundary and the next single UI capability decided before any work

Do not use when:
- Create the actual design direction and user-flow contract. Route to `design-context-and-direction-contract`.
- Capture browser renders and traces for independent review. Route to `ui-review-scope-and-evidence-acquisition`.
- Classify a request that is not UI-only or spans several domains. Route to `context-intake-and-routing`.
- Sequence capabilities for a workflow that no Recipe covers. Route to `workflow-orchestration-and-lifecycle`.

#### Required Inputs

- A UI request, project state, existing interface, target files, authorization, and design artifacts.

#### Procedure

1. Inventory requested outcome, supplied artifacts, product authority, target surfaces, current source or render state, external sources, and explicit exclusions.
2. Classify new design, existing redesign, token import, implementation, preflight, evidence capture, critique, repair, or release-decision intent.
3. Determine source-write, artifact-write, local-exec, external-read, and human-decision boundaries before route selection.
4. Identify missing prerequisites, incompatible identities, applicable specialist branches, and stop conditions.
5. Return one next capability and conditional follow-ups only; preserve unknowns and perform no downstream work.

#### Domain Guidance

- Routing ownership: this Skill classifies UI-only work; cross-domain requests go to context-intake-and-routing and Recipe selection belongs to the router.

#### Output Contract

Produce:
- UI task classification
- authorization and write-boundary record
- next-capability route
- missing-input and stop-condition list

Every material design choice, implementation claim, finding, score, capture, or disposition must link to supplied authority or current evidence, or be labeled assumption/unknown.

Deliver each output as the artifact itself (tables, commands, patches, plans, records), not as a description of how it would be produced.

#### UI Coverage

- `classification`
- `authorization`
- `write-boundary`
- `next-capability`
- `no-downstream-work`

#### Hard Gates

- Routing must not smuggle design, review, source mutation, browser capture, or release judgment into the intake artifact.
- Review, evidence acquisition, preflight, and preservation audit never imply source remediation or release authority.
- Preserve product truth, user task, semantic order, authentic content, accessibility, responsive behavior, state coverage, source identity, and authority boundaries where applicable.
- Return `needs-input` when an identifiable owner can supply a missing requirement, asset authority, capture, state, or decision.
- Return `blocked` when required authorization, safe mutation scope, rendered evidence, tooling, or specialist dependency is unavailable.
- Deliver every part the supplied evidence and authority support, label assumptions, and list each missing item with the owner who can supply it; `needs-input` or `blocked` applies to the unsupported part, not to the whole deliverable.

#### Forbidden Actions

- remote Git, merge, deploy, release, cloud mutation, or external-system write
- invent product facts, brand authority, copy claims, customer data, assets, evidence, or approval
- perform an adjacent capability or combine independent review with source repair
- treat static inspection, stale capture, or model self-report as current rendered evidence
- claim evaluation, approval, release, or completion evidence that has not been produced

#### Status Mapping

- `passed`: output contract and every hard gate are satisfied with current evidence.
- `needs-input`: a requestable source, state, decision, capture, or authorization term is missing. Deliver every supported part first and name the owner for the missing part.
- `blocked`: proceeding would exceed authority, mix review with repair, or rely on unavailable critical evidence.
- `failed`: authorized work ran but a deterministic gate or required output failed.

#### Non-Responsibilities

Adjacent capabilities:
- `design-context-and-direction-contract`
- `existing-interface-redesign-and-preservation`
- `ui-review-scope-and-evidence-acquisition`
- `ui-remediation`
- `context-intake-and-routing`
- `workflow-orchestration-and-lifecycle`

Never perform remote Git, external-system writes, merge, deploy, release, or an adjacent capability's work. Review and preflight capabilities never repair product source; evidence-acquisition capabilities never issue design findings.
