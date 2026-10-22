---
name: interaction-states-forms-and-navigation
description: "Consolidated capability with 4 selectable modes: ai-interaction-and-probabilistic-ux; diagram-and-architecture-artifact-generation; document-rendering-and-validation; interaction-states-forms-and-navigation. Choose exactly one mode per invocation."
version: 1.1.0-consolidated
modes: [ai-interaction-and-probabilistic-ux, diagram-and-architecture-artifact-generation, document-rendering-and-validation, interaction-states-forms-and-navigation]
---

# Interaction States Forms And Navigation

## Responsibility

Consolidated capability covering 4 related modes: Design bounded user interaction for AI latency, uncertainty, correction, personalization, escalation, and safe failure without hiding probabilistic behavior.; Generate traceable architecture or process diagram source from approved evidence without inventing nodes, edges, trust boundaries, or runtime facts.; Render one approved document source into a declared local artifact and validate layout, accessibility, links, output integrity, and limitations.; Define and implement coherent controls, navigation, forms, validation, loading, empty, error, permission, disabled, success, interruption, and recovery states.

## Mode selection

This capability has several distinct modes. Read this table first, pick exactly one
mode for the current request, then follow only that mode's section. Do not blend
modes: each carries its own permission identity, gates, and stop conditions. The
permission column is binding - a run uses the permission of the mode it selected,
never the widest permission in this document.

| Mode | Permission | Use when | Routes elsewhere |
| --- | --- | --- | --- |
| `ai-interaction-and-probabilistic-ux` | `workspace-write` | A feature shows generated or probabilistic output and needs loading, uncertainty, correction and failure states designed; Someone asks how users should correct, undo, retry or escalate when an AI resu | Choose the model, retrieval stack, memory, and serving architecture (-> ai-model-and-data-architecture); Perform the sys |
| `diagram-and-architecture-artifact-generation` | `workspace-write` | An architecture or process diagram must be drawn from approved facts without inventing nodes or edges; Someone asks for diagram source with a source map and a list of unknown or disputed elements. | Discover the actual architecture by inspecting code and runtime evidence first (-> architecture-deepening-discovery); Ch |
| `document-rendering-and-validation` | `workspace-write-local-exec` | An approved document source must be rendered to PDF or HTML and the output checked for layout, links and accessibility; Someone asks whether a rendered file matches the approved source and release has | Author or substantively edit the source document first (-> documentation-authoring); Package and version the verified re |
| `interaction-states-forms-and-navigation` | `workspace-write` | A form, flow or navigation needs every control state and failure recovery defined and implemented; Someone asks what happens on validation error, timeout, permission denial, refresh or back navigation | Specify the assistive-technology acceptance and test matrix for the completed interaction (-> accessibility-contracts-an |

## Mode: `ai-interaction-and-probabilistic-ux`

### ai-interaction-and-probabilistic-ux

#### Responsibility

Design bounded user interaction for AI latency, uncertainty, correction, personalization, escalation, and safe failure without hiding probabilistic behavior.

#### Trigger

Use when the request matches any of:
- A feature shows generated or probabilistic output and needs loading, uncertainty, correction and failure states designed
- Someone asks how users should correct, undo, retry or escalate when an AI result is wrong

Do not use when:
- Choose the model, retrieval stack, memory, and serving architecture. Route to `ai-model-and-data-architecture`.
- Perform the system threat model and autonomous-action safety assessment. Route to `ai-safety-and-action-governance`.

#### Required Inputs

- Probabilistic outputs, user context, interaction latency, correction signals, and accessibility needs.

#### Procedure

1. Freeze the approved user job, AI role, latency budget, error cost, data boundary, autonomy level, and human escalation owner.
2. Model deterministic, loading, partial, uncertain, conflicting, unsafe, unavailable, and recovery states.
3. Define provenance and uncertainty communication in task language rather than decorative confidence theater.
4. Provide correction, undo, retry, compare, opt-out, feedback, and human-escalation controls proportionate to consequence.
5. Test adversarial misunderstandings, personalization drift, stale memory, and failure recovery; preserve unresolved safety dependencies.

#### Domain Guidance

- Pattern per state. Latency: streamed partial output or a skeleton with an expected wait and a cancel control. Uncertainty: task-language wording of what is known and unknown, never a decorative confidence percentage. Provenance: inline citations or source links the user can open. Correction: edit in place, undo, regenerate with a changed instruction. Failure: a plain message, the retry path and a human escalation route.
- Model the states deterministic, loading, partial, uncertain, conflicting, unsafe, unavailable and recovered, and give each its visible UI, controls and exit.
- Discriminator: owns how uncertain AI output is shown to and corrected by users; it does not choose models or autonomy levels.

#### Output Contract

Produce:
- AI interaction-state model
- uncertainty and provenance contract
- correction and escalation flow
- safe-failure acceptance criteria

Every material design choice, implementation claim, finding, score, capture, or disposition must link to supplied authority or current evidence, or be labeled assumption/unknown.

Deliver each output as the artifact itself (tables, commands, patches, plans, records), not as a description of how it would be produced.

#### UI Coverage

- `latency`
- `uncertainty`
- `provenance`
- `correction`
- `undo`
- `escalation`
- `safe-failure`

#### Hard Gates

- Never present generated content, confidence, personalization, or autonomous action as certain, authoritative, or irreversible when the system cannot prove it.
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
- `interaction-states-forms-and-navigation`
- `ai-model-and-data-architecture`
- `ai-safety-and-action-governance`
- `accessibility-contracts-and-assistive-validation`

Never perform remote Git, external-system writes, merge, deploy, release, or an adjacent capability's work. Review and preflight capabilities never repair product source; evidence-acquisition capabilities never issue design findings.

## Mode: `diagram-and-architecture-artifact-generation`

### diagram-and-architecture-artifact-generation

#### Responsibility

Generate traceable architecture or process diagram source from approved evidence without inventing nodes, edges, trust boundaries, or runtime facts.

#### Trigger

Use when the request matches any of:
- An architecture or process diagram must be drawn from approved facts without inventing nodes or edges
- Someone asks for diagram source with a source map and a list of unknown or disputed elements

Do not use when:
- Discover the actual architecture by inspecting code and runtime evidence first. Route to `architecture-deepening-discovery`.
- Choose among competing architecture interfaces and recommend one. Route to `architecture-interface-alternative-evaluation`.

#### Required Inputs

- Approved source facts, diagram purpose, notation, audience, and output format.

#### Procedure

1. Freeze diagram audience, question, scope, notation, approved source artifacts, versions, and unresolved assumptions.
2. Extract actors, systems, containers or modules, data stores, edges, direction, protocols, trust boundaries, and environments only from cited evidence.
3. Choose the smallest diagram type that answers the declared question and avoid mixing abstraction levels.
4. Generate stable IDs, labels, legend, source mapping, and explicit unknown or disputed elements.
5. Perform a structural source check, prepare an exact host renderer or syntax-validation request, and route factual gaps back to discovery rather than inventing them.

#### Domain Guidance

- Persist the diagram source file first, then prepare a single render request for the whole set of outputs; a render is never a substitute for the source.

#### Output Contract

Produce:
- diagram source
- host render or syntax-validation request
- node-and-edge source map
- unknown and conflict ledger

Every material fact, boundary, recommendation, finding, test claim, migration step, or risk must cite supplied or authorized evidence or be labeled assumption/unknown.

Deliver each output as the artifact itself (tables, commands, patches, plans, records), not as a description of how it would be produced.

#### Coverage

- `diagram-scope`
- `abstraction-level`
- `node-edge-provenance`
- `trust-boundary`
- `host-validation-request`
- `unknowns`

#### Hard Gates

- Every node, edge, boundary, protocol, and environment label must trace to approved evidence or be visibly marked unknown; a syntactically valid invented diagram fails.
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
- `architecture-candidate-reporting`
- `architecture-deepening-discovery`
- `security-audit-and-threat-modeling`
- `documentation-authoring`
- `architecture-interface-alternative-evaluation`

Never access or emit secret values, mutate production data or provider policy, grant AI action rights, execute remote Git, merge, deploy, release, or perform an adjacent capability. Review, reporting, and audit candidates never repair source.

## Mode: `document-rendering-and-validation`

### document-rendering-and-validation

#### Responsibility

Render one approved document source into a declared local artifact and validate layout, accessibility, links, output integrity, and limitations.

#### Trigger

Use when the request matches any of:
- An approved document source must be rendered to PDF or HTML and the output checked for layout, links and accessibility
- Someone asks whether a rendered file matches the approved source and release hash

Do not use when:
- Author or substantively edit the source document first. Route to `documentation-authoring`.
- Package and version the verified rendered artifact for change delivery. Route to `change-packaging-and-versioning`.

#### Required Inputs

- Approved document source, renderer, format, template, accessibility target, and output path.

#### Procedure

1. Freeze source and template hashes, renderer and version, target format and path, fonts or assets, page and accessibility criteria, link policy, and overwrite authorization.
2. Render only the approved source through the declared local command and record exit, duration, logs, and output identity.
3. Inspect pagination, clipping, overflow, fonts, images, links, headings, metadata, text extraction, language, and accessible structure where tooling supports it.
4. Return artifact, hash, validation evidence, unresolved rendering limitations, and rollback or no-write outcome; do not rewrite content or publish.

#### Domain Guidance

- Compare the source hash with the approved value and state the result plainly: when it matches, say it matches and cite the approval; when it does not, say exactly which hash differs. A mismatch between an intermediate file and the release hash is not an integrity failure of the source.
- Separate template defects from author-content defects in the fix list so each goes to its owner.

#### Output Contract

Produce:
- rendered document artifact
- renderer command evidence
- layout, link, and accessibility validation
- hash and residual-limitations report

Every material action, command, result, finding, score, capture, provider receipt, or completion claim must bind to exact target identity and current evidence or be labeled assumption/unknown.

Deliver each output as the artifact itself (tables, commands, patches, plans, records), not as a description of how it would be produced.

#### Coverage

- `source-hash`
- `renderer-version`
- `output-hash`
- `layout-validation`
- `link-validation`
- `accessibility-limitations`

#### Hard Gates

- A successful renderer exit is insufficient: the declared output must have current hash and inspected layout, links, text, metadata, and accessibility evidence or explicit unsupported limitations.
- Independent review, QA, audit, acquisition, analysis, and triage never imply remediation; setup or authentication never implies downstream action authority.
- Preserve source, build, dataset, model, workflow, provider, browser, session, or local-system identity; command, version, exit, duration, artifacts, hashes, limitations, and cleanup must remain explicit when applicable.
- Return `needs-input` when a named owner can provide missing scope, authority, evidence, governance, target, or decision.
- Return `blocked` when proceeding would exceed mutation authority, expose credentials, violate governance, erase failed evidence, perform an undeclared remote or destructive action, or mix independent review with repair.
- Deliver every part the supplied evidence and authority support, label assumptions, and list each missing item with the owner who can supply it; `needs-input` or `blocked` applies to the unsupported part, not to the whole deliverable.

#### Forbidden Actions

- request, reveal, print, persist, hash, or transmit credential or secret values
- perform source, local-system, browser, provider, publication, or remote mutations outside the exact atomic scope and fresh authorization
- invent commands, exits, duration, artifacts, captures, provider receipts, benchmark results, approval, or completion evidence
- combine independent evidence or findings with remediation, risk acceptance, publication, deployment, or release
- claim evaluation, approval, release, or completion evidence that has not been produced

#### Status Mapping

- `passed`: the atomic output and every gate have current target-bound evidence.
- `needs-input`: a requestable scope, authority, target, fixture, governance term, or decision is absent. Deliver every supported part first and name the owner for the missing part.
- `blocked`: safe work requires prohibited access, unavailable authority, secret values, destructive or remote action, or an incompatible identity.
- `failed`: the authorized action ran but a deterministic check or required output failed.

#### Non-Responsibilities

Adjacent capabilities:
- `documentation-authoring`
- `artifact-persistence-and-tool-actions`
- `completion-evidence-gate`
- `change-packaging-and-versioning`

Never silently expand source, command, browser, data, credential, local-system, provider, or remote authority. Independent review, QA, audit, evidence acquisition, analysis, and triage never repair source. Setup and authentication never imply authority to perform the downstream action.

## Mode: `interaction-states-forms-and-navigation`

### interaction-states-forms-and-navigation

#### Responsibility

Define and implement coherent controls, navigation, forms, validation, loading, empty, error, permission, disabled, success, interruption, and recovery states.

#### Trigger

Use when the request matches any of:
- A form, flow or navigation needs every control state and failure recovery defined and implemented
- Someone asks what happens on validation error, timeout, permission denial, refresh or back navigation

Do not use when:
- Specify the assistive-technology acceptance and test matrix for the completed interaction. Route to `accessibility-contracts-and-assistive-validation`.
- Choose the page-level visual hierarchy, grid, density, and breakpoint composition. Route to `responsive-layout-and-spatial-composition`.

#### Required Inputs

- User flows, acceptance criteria, a component system, content, state model, and platform behavior.

#### Procedure

1. Freeze the approved user flow, routes, roles, data states, validation rules, destructive actions, recovery behavior, and component foundation.
2. Model every control and transition including default, hover, focus, active, selected, disabled, pending, success, error, interrupted, expired, and permission-denied states as applicable.
3. Implement semantic controls, URL and history behavior, labels, inline and summary errors, confirmation, undo, idempotency cues, and safe destructive-action handling.
4. Preserve user input and context through validation, async failure, navigation, timeout, and retry where safe.
5. Verify keyboard order, focus movement, deep links, refresh/back behavior, variable content, and failure recovery; record unresolved service dependencies.

#### Domain Guidance

- Default target size: at least 44 by 44 pt (Apple) or 48 by 48 dp (Material), with at least 8 px between targets; extend the hit area beyond the visible bounds when needed. Never rely on hover alone for a primary action.
- During verification capture console errors for each flow, keyboard order and focus movement, and deep-link, refresh and back behavior.

#### Output Contract

Produce:
- interaction and state model
- implemented controls/forms/navigation
- state coverage matrix
- recovery verification evidence

Every material design choice, implementation claim, finding, score, capture, or disposition must link to supplied authority or current evidence, or be labeled assumption/unknown.

Deliver each output as the artifact itself (tables, commands, patches, plans, records), not as a description of how it would be produced.

#### UI Coverage

- `controls`
- `navigation`
- `forms`
- `loading`
- `empty`
- `error`
- `permission`
- `disabled`
- `success`
- `interruption`
- `recovery`

#### Hard Gates

- The happy path cannot pass alone: every applicable loading, empty, validation, error, permission, disabled, interruption, success, and recovery state must exist and be reachable for verification.
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
- `responsive-layout-and-spatial-composition`
- `accessibility-contracts-and-assistive-validation`
- `content-copy-and-authentic-assets`
- `purposeful-motion-and-animation-engineering`

Never perform remote Git, external-system writes, merge, deploy, release, or an adjacent capability's work. Review and preflight capabilities never repair product source; evidence-acquisition capabilities never issue design findings.
