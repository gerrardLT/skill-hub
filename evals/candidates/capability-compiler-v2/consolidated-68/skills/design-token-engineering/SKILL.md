---
name: design-token-engineering
description: "Consolidated capability with 2 selectable modes: design-system-foundation-and-token-extraction; external-design-token-extraction-and-normalization. Choose exactly one mode per invocation."
version: 1.1.0-consolidated
modes: [design-system-foundation-and-token-extraction, external-design-token-extraction-and-normalization]
---

# Design Token Engineering

## Responsibility

Consolidated capability covering 2 related modes: Choose or generate an in-project design-system foundation with semantic tokens, component contracts, states, themes, and persistence rules.; Extract observable design primitives from supplied authorized external captures or files, normalize them with provenance and confidence, and stop before project token writes.

## Mode selection

This capability has several distinct modes. Read this table first, pick exactly one
mode for the current request, then follow only that mode's section. Do not blend
modes: each carries its own permission identity, gates, and stop conditions. The
permission column is binding - a run uses the permission of the mode it selected,
never the widest permission in this document.

| Mode | Permission | Use when | Routes elsewhere |
| --- | --- | --- | --- |
| `design-system-foundation-and-token-extraction` | `workspace-write` | A project needs semantic tokens, component contracts and theme rules, or needs to confirm its existing system already covers a new need; Someone asks for candidate token and theme files with a change  | Extract primitives from this external authorized site without writing project tokens (-> external-design-token-extractio |
| `external-design-token-extraction-and-normalization` | `workspace-write` | A supplied capture or file of an authorized external site must be turned into an inventory of design primitives with provenance; Someone asks which colors, type and spacing a reference uses, with conf | Persist approved semantic tokens and components into this project's design system (-> design-system-foundation-and-token |

## Mode: `design-system-foundation-and-token-extraction`

### design-system-foundation-and-token-extraction

#### Responsibility

Choose or generate an in-project design-system foundation with semantic tokens, component contracts, states, themes, and persistence rules.

#### Trigger

Use when the request matches any of:
- A project needs semantic tokens, component contracts and theme rules, or needs to confirm its existing system already covers a new need
- Someone asks for candidate token and theme files with a change table and version

Do not use when:
- Extract primitives from this external authorized site without writing project tokens. Route to `external-design-token-extraction-and-normalization`.
- Define the page-level responsive composition and reflow behavior. Route to `responsive-layout-and-spatial-composition`.

#### Required Inputs

- A UI brief, stack, design references, existing tokens, and project conventions.

#### Procedure

1. Inventory existing tokens, components, CSS conventions, dependencies, themes, and approved design direction before adding anything.
2. Reuse the project foundation where sufficient; add only semantic color, type, spacing, radius, elevation, motion, and layout tokens required by real states.
3. Define component anatomy, variants, sizes, content bounds, interaction states, accessibility behavior, and composition rules.
4. Map raw or imported values to semantic roles with provenance; prohibit one-off values unless recorded as an exception.
5. Persist the smallest working foundation and verify representative components across themes and states.

#### Domain Guidance

- Reuse first: inventory the existing tokens and components and show which required states they already express. Add a token only for a real state the foundation cannot express.
- Prefer the official package when the brief matches a known design system (component library or platform guidelines) rather than inventing CSS for it.
- When approval is still pending, still produce candidate token and theme files labelled pending, with a change table, a version rationale and a checked contrast figure; never persist them as approved and name the approver.

#### Output Contract

Produce:
- semantic token set
- component contract catalog
- theme and state rules
- persistence and exception ledger
- candidate token and theme files labelled pending approval, with change table and version rationale

Every material design choice, implementation claim, finding, score, capture, or disposition must link to supplied authority or current evidence, or be labeled assumption/unknown.

Deliver each output as the artifact itself (tables, commands, patches, plans, records), not as a description of how it would be produced.

#### UI Coverage

- `semantic-tokens`
- `component-contracts`
- `states`
- `themes`
- `persistence`
- `provenance`

#### Hard Gates

- Do not create a parallel design system, token alias maze, or component abstraction when the existing project foundation can express the required states.
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
- `external-design-token-extraction-and-normalization`
- `visual-language-and-anti-template-controls`
- `responsive-layout-and-spatial-composition`
- `interaction-states-forms-and-navigation`

Never perform remote Git, external-system writes, merge, deploy, release, or an adjacent capability's work. Review and preflight capabilities never repair product source; evidence-acquisition capabilities never issue design findings.

## Mode: `external-design-token-extraction-and-normalization`

### external-design-token-extraction-and-normalization

#### Responsibility

Extract observable design primitives from supplied authorized external captures or files, normalize them with provenance and confidence, and stop before project token writes.

#### Trigger

Use when the request matches any of:
- A supplied capture or file of an authorized external site must be turned into an inventory of design primitives with provenance
- Someone asks which colors, type and spacing a reference uses, with confidence and conflicts, before anything is written to the project

Do not use when:
- Persist approved semantic tokens and components into this project's design system. Route to `design-system-foundation-and-token-extraction`.
- Copy the external product's layout, brand, assets, or interaction wholesale. Route to `design-context-and-direction-contract`.
- Acquire the capture or crawl the external site itself. Route to `browser-data-acquisition-runtime`.

#### Required Inputs

- An authorized public reference, extraction runtime, and requested analysis mode.

#### Procedure

1. Verify source authorization, supplied capture or file identity, scope, timestamp, terms, and prohibited assets or personal data.
2. Read only supplied authorized captures or files; do not browse, fetch, bypass access controls, or perform external writes.
3. Record exact source, selector or artifact location, viewport, observed value, confidence, and state for every primitive.
4. Cluster raw values and propose semantic roles while preserving contradictions, one-offs, responsive variants, and unknown intent.
5. Emit a normalization report and candidate mapping only; require separate human approval and design-system capability for project writes.

#### Domain Guidance

- This Skill reads only supplied authorized captures or files. It cannot browse or fetch; acquisition of the capture belongs to a browser acquisition capability, and the Coverage tag external-read refers to the external origin of the supplied material, not to live access.
- Extraction is for initialization, not pixel-perfect reproduction: give extract-only output by default and offer starter files only when the owner asks.

#### Output Contract

Produce:
- authorized external primitive inventory
- provenance and confidence ledger
- normalized candidate token map
- unknown and conflict register

Every material design choice, implementation claim, finding, score, capture, or disposition must link to supplied authority or current evidence, or be labeled assumption/unknown.

Deliver each output as the artifact itself (tables, commands, patches, plans, records), not as a description of how it would be produced.

#### UI Coverage

- `authorization`
- `external-read`
- `primitive-extraction`
- `normalization`
- `provenance`
- `no-project-write`

#### Hard Gates

- Observed external values are evidence, not project authority: no project token, copied asset, or design decision may be written or approved by this capability.
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
- `design-system-foundation-and-token-extraction`
- `design-context-and-direction-contract`
- `source-metadata-and-provenance`
- `ui-review-scope-and-evidence-acquisition`
- `browser-data-acquisition-runtime`

Never perform remote Git, external-system writes, merge, deploy, release, or an adjacent capability's work. Review and preflight capabilities never repair product source; evidence-acquisition capabilities never issue design findings.
