---
name: research-planning-and-governance
description: "Consolidated capability with 2 selectable modes: architecture-deepening-discovery; research-planning-and-governance. Choose exactly one mode per invocation."
version: 1.1.0-consolidated
modes: [architecture-deepening-discovery, research-planning-and-governance]
---

# Research Planning And Governance

## Responsibility

Consolidated capability covering 2 related modes: Find evidence-backed shallow modules, leaked boundaries, repeated orchestration, and change hotspots, and recommend deepen or leave unchanged under YAGNI.; Design a research plan with decision linkage, method, sampling, consent, minimization, retention, external-transfer, and deletion boundaries.

## Mode selection

This capability has several distinct modes. Read this table first, pick exactly one
mode for the current request, then follow only that mode's section. Do not blend
modes: each carries its own permission identity, gates, and stop conditions. The
permission column is binding - a run uses the permission of the mode it selected,
never the widest permission in this document.

| Mode | Permission | Use when | Routes elsewhere |
| --- | --- | --- | --- |
| `architecture-deepening-discovery` | `workspace-write` | A codebase has maintenance friction and someone wants to know which modules are worth deepening and which to leave alone; Repeated orchestration, leaked boundaries or change hotspots must be found wit | Design the selected module's exact boundary, interface, seams, migration, and tests (-> architecture-deep-module-design) |
| `research-planning-and-governance` | `workspace-write` | A research effort needs its decision link, method, sampling and data-governance terms set before anyone is contacted; Someone asks what consent, retention and transfer terms are needed to run intervie | Conduct the already approved customer interviews (-> customer-interview-execution); Synthesize the completed qualitative |

## Mode: `architecture-deepening-discovery`

### architecture-deepening-discovery

#### Responsibility

Find evidence-backed shallow modules, leaked boundaries, repeated orchestration, and change hotspots, and recommend deepen or leave unchanged under YAGNI.

#### Trigger

Use when the request matches any of:
- A codebase has maintenance friction and someone wants to know which modules are worth deepening and which to leave alone
- Repeated orchestration, leaked boundaries or change hotspots must be found with evidence before any redesign

Do not use when:
- Design the selected module's exact boundary, interface, seams, migration, and tests. Route to `architecture-deep-module-design`.
- Review an implementation plan for architecture, data, failure, security, and operability gaps. Route to `engineering-plan-review`.

#### Required Inputs

- A codebase, change hotspots, repeated logic, and maintenance-friction evidence.

#### Procedure

1. Freeze repository scope, observed maintenance pain, change history, ownership, incidents, repeated logic, and excluded areas.
2. Trace callers and dependencies for shallow delegation, knowledge leakage, repeated orchestration, unstable interfaces, and coupled changes.
3. Quantify or cite friction, frequency, blast radius, and existing test seams; distinguish style dislike from maintenance evidence.
4. Generate bounded candidates and a leave-unchanged option with expected benefit, migration cost, risk, and evidence gaps.
5. Rank investigation priority without designing or implementing modules; reject speculative abstractions.

#### Domain Guidance

- When the user names no direction, weight areas by recent change frequency (walk back a good stretch of history) before scanning; code that rarely changes rarely pays back a refactor.
- If the user named a module or pain point, take it and skip the inference.

#### Output Contract

Produce:
- architecture friction inventory
- deepening candidate register
- YAGNI leave-unchanged cases
- evidence and priority report

Every material fact, boundary, recommendation, finding, test claim, migration step, or risk must cite supplied or authorized evidence or be labeled assumption/unknown.

Deliver each output as the artifact itself (tables, commands, patches, plans, records), not as a description of how it would be produced.

#### Coverage

- `shallow-module`
- `boundary-leak`
- `change-coupling`
- `maintenance-evidence`
- `YAGNI`
- `leave-unchanged`

#### Hard Gates

- No deepening candidate passes on aesthetics or hypothetical reuse alone; it needs cited recurring friction, boundary leakage, change coupling, or operational cost that exceeds migration risk.
- Review, reporting, contract, and audit candidates never imply implementation, live policy change, production mutation, or risk acceptance.
- Preserve trust boundaries, authorization, data and secret governance, compatibility, migration, rollback or containment, source identity, counterevidence, and residual risk where applicable.
- Return `needs-input` when a named owner can supply a missing fact, policy, evidence, or approval.
- Return `blocked` when safe analysis or mutation would require unavailable authority, secret values, prohibited tests, remote writes, or unresolved high-impact risk.
- Deliver every part the supplied evidence and authority support, label assumptions, and list each missing item with the owner who can supply it; `needs-input` or `blocked` applies to the unsupported part, not to the whole deliverable.

#### Forbidden Actions

- request, read, print, persist, hash, or transmit secret values
- remote Git, merge, deploy, release, provider-policy mutation, production-data mutation, or AI action-right activation
- invent architecture facts, data rights, authorization, evidence, approval, migration safety, or risk acceptance
- combine independent review or audit with source remediation
- claim evaluation, approval, release, or completion evidence that has not been produced

#### Status Mapping

- `passed`: output contract and every hard gate are satisfied with current evidence.
- `needs-input`: a requestable source, policy, compatibility fact, or decision is missing. Deliver every supported part first and name the owner for the missing part.
- `blocked`: proceeding would exceed authority, access secret values, mutate production, or cross a prohibited safety boundary.
- `failed`: authorized work ran but a deterministic gate or required output failed.

#### Non-Responsibilities

Adjacent capabilities:
- `architecture-deep-module-design`
- `architecture-interface-alternative-evaluation`
- `architecture-candidate-reporting`
- `engineering-plan-review`

Never access or emit secret values, mutate production data or provider policy, grant AI action rights, execute remote Git, merge, deploy, release, or perform an adjacent capability. Review, reporting, and audit candidates never repair source.

## Mode: `research-planning-and-governance`

### research-planning-and-governance

#### Responsibility

Design a research plan with decision linkage, method, sampling, consent, minimization, retention, external-transfer, and deletion boundaries.

#### Trigger

Use when the request matches any of:
- A research effort needs its decision link, method, sampling and data-governance terms set before anyone is contacted
- Someone asks what consent, retention and transfer terms are needed to run interviews or a survey

Do not use when:
- Conduct the already approved customer interviews. Route to `customer-interview-execution`.
- Synthesize the completed qualitative corpus. Route to `qualitative-evidence-synthesis`.

#### Required Inputs

- A research question, target population, access constraints, ethical boundary, and timebox.

#### Procedure

1. State the decision, research question, prior evidence, unknown, owner, and stopping rule.
2. Select method and sampling logic appropriate to the claim; name bias and representativeness limits.
3. Define authorization, consent, minimization, redaction, recording, retention, access, external-transfer, and deletion policy.
4. Specify protocol, evidence schema, quality checks, analysis plan, and recruitment boundary.
5. Return the plan and blocked governance inputs; do not recruit or collect data.

#### Output Contract

Produce:
- research plan
- sampling and method rationale
- data-governance contract
- analysis and stopping plan

Every material claim, score, recommendation, or finding must link to a supplied or authorized source, or be labeled assumption/unknown.

Deliver each output as the artifact itself (tables, commands, patches, plans, records), not as a description of how it would be produced.

#### Hard Gates

- No participant contact, collection, recording, external Judge use, or proprietary-data transfer may begin from an incomplete governance contract.
- Preserve conflicts, counterevidence, unknowns, source identity, and authority boundaries.
- Return `needs-input` when an identifiable owner can supply a missing requirement or decision.
- Return `blocked` when required authority, evidence, governance, or a safe execution boundary is unavailable.
- Deliver every part the supplied evidence and authority support, label assumptions, and list each missing item with the owner who can supply it; `needs-input` or `blocked` applies to the unsupported part, not to the whole deliverable.

#### Forbidden Actions

- remote Git, pull-request mutation, merge, deploy, cloud mutation, or external-system write
- invent facts, evidence, authority, approval, or customer data
- perform adjacent or downstream capability responsibilities
- claim evaluation, approval, release, or completion evidence that has not been produced

#### Data Governance

Before using interviews, customer or proprietary data, recordings, or an external LLM Judge, require explicit authorization, minimization, redaction, retention, external-transfer, access, deletion, and incident boundaries. Missing governance returns `needs-input`; unavailable or prohibited authority returns `blocked`.

#### Status Mapping

- `passed`: output contract and every hard gate are satisfied.
- `needs-input`: a requestable source, decision, or governance term is missing. Deliver every supported part first and name the owner for the missing part.
- `blocked`: proceeding would exceed authority, violate governance, or rely on unavailable critical evidence.
- `failed`: supplied inputs were processed but a deterministic gate or required output failed.

#### Non-Responsibilities

Adjacent capabilities:
- `customer-interview-execution`
- `data-analysis-validation`
- `qualitative-evidence-synthesis`

Never perform remote Git, external-system writes, merge, deploy, cloud mutation, participant recruitment/contact, or downstream implementation unless a different explicitly authorized capability owns that action.
