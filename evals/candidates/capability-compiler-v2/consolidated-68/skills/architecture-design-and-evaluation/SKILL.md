---
name: architecture-design-and-evaluation
description: "Consolidated capability with 5 selectable modes: architecture-candidate-reporting; architecture-deep-module-design; architecture-interface-alternative-evaluation; frontend-runtime-boundaries-and-dependency-safety; resilience-and-determinism. Choose exactly one mode per invocation."
version: 1.1.0-consolidated
modes: [architecture-candidate-reporting, architecture-deep-module-design, architecture-interface-alternative-evaluation, frontend-runtime-boundaries-and-dependency-safety, resilience-and-determinism]
---

# Architecture Design And Evaluation

## Responsibility

Consolidated capability covering 5 related modes: Present already-developed architecture candidates as traceable comparable views, rankings, diagrams, and a bounded recommendation without inventing options or implementing one.; Design one module boundary and interface that hides complexity, enforces dependency direction, preserves seams, and supports migration and verification.; Generate at least two independent interface alternatives and compare information hiding, caller complexity, dependencies, failure behavior, testability, compatibility, and migration cost.; Audit authorized frontend source so server-only logic, credentials, privileged actions, assets, dependencies, and runtime assumptions stay on safe explicit boundaries, and hand accepted repairs to the repair owner without editing source.; Diagnose and verify nondeterminism, retries, timeouts, cleanup, isolation, ordering, and recovery behavior under a frozen workload without source repair.

## Mode selection

This capability has several distinct modes. Read this table first, pick exactly one
mode for the current request, then follow only that mode's section. Do not blend
modes: each carries its own permission identity, gates, and stop conditions. The
permission column is binding - a run uses the permission of the mode it selected,
never the widest permission in this document.

| Mode | Permission | Use when | Routes elsewhere |
| --- | --- | --- | --- |
| `architecture-candidate-reporting` | `workspace-write` | Several architecture candidates already exist and must be compared on the same criteria with a ranking and a bounded recommendation; A decision maker needs candidate cards, a sensitivity view and diag | Generate independent interface alternatives for this module before any candidates exist (-> architecture-interface-alter |
| `architecture-deep-module-design` | `workspace-write` | One module needs a smaller, deeper interface that hides complexity with a migration path; Callers know too much about a module and someone must redesign its boundary without rewriting everything. | Scan the codebase for evidence-backed module-deepening opportunities (-> architecture-deepening-discovery); Generate at  |
| `architecture-interface-alternative-evaluation` | `workspace-write` | A module interface is being chosen and several structurally different designs should be compared before committing; Someone asks for alternative interface designs with their information hiding, failur | Design the full chosen module boundary, dependency direction, seams, and test plan (-> architecture-deep-module-design); |
| `frontend-runtime-boundaries-and-dependency-safety` | `read-only` | A frontend build may leak server-only code, secrets or privileged logic into the browser bundle; Someone asks whether client and server boundaries, third-party scripts and dependencies are safe before | Design the visual token and component foundation for the interface (-> design-system-foundation-and-token-extraction); B |
| `resilience-and-determinism` | `local-exec` | A test or job fails intermittently and needs a reproducible failure model before anyone edits code; Retries, timeouts, ordering or cleanup may be masking a race, leaked state or an arbitrary sleep. | Apply the accepted source fix for the confirmed flaky root cause (-> defect-remediation); Design the overall test portfo |

## Mode: `architecture-candidate-reporting`

### architecture-candidate-reporting

#### Responsibility

Present already-developed architecture candidates as traceable comparable views, rankings, diagrams, and a bounded recommendation without inventing options or implementing one.

#### Trigger

Use when the request matches any of:
- Several architecture candidates already exist and must be compared on the same criteria with a ranking and a bounded recommendation
- A decision maker needs candidate cards, a sensitivity view and diagrams before choosing an architecture

Do not use when:
- Generate independent interface alternatives for this module before any candidates exist. Route to `architecture-interface-alternative-evaluation`.
- Generate traceable diagrams from the approved architecture facts. Route to `diagram-and-architecture-artifact-generation`.

#### Required Inputs

- Already discovered architecture candidates with code evidence.

#### Procedure

1. Freeze candidate identities, common requirements, evidence, constraints, decision criteria, owners, and unresolved disagreements.
2. Normalize each candidate into context, boundary, interfaces, dependencies, data flow, failure behavior, security, operability, migration, cost, and evidence quality.
3. Create comparable tables, cards, and supplied-diagram references without erasing candidate-specific assumptions.
4. Compute weighted totals with the arithmetic shown and rank; mark criteria without evidence instead of scoring them.
5. Apply declared criteria and sensitivity; separate fact, estimate, inference, and human preference.
6. Recommend or abstain, preserving dissent, unknowns, and the named human architecture decision.

#### Domain Guidance

- When criteria and weights are supplied, compute the weighted totals and rank the candidates, showing the arithmetic and a sensitivity check (how the ranking changes if the top weight moves). Withhold a ranking only for criteria that lack evidence, and say which.
- Give a conditional recommendation stating what would change it; abstain only when evidence gaps make any ranking misleading.
- Choose the diagram pattern per candidate type: a dependency or call-flow graph for coupling, a layered view for boundaries, a sequence view for failure behavior. Vary patterns rather than one template for all candidates.

#### Output Contract

Produce:
- architecture candidate cards
- comparison and sensitivity matrix
- traceable diagram index
- bounded recommendation and dissent ledger
- weighted ranking with arithmetic and sensitivity

Every material fact, boundary, recommendation, finding, test claim, migration step, or risk must cite supplied or authorized evidence or be labeled assumption/unknown.

Deliver each output as the artifact itself (tables, commands, patches, plans, records), not as a description of how it would be produced.

#### Coverage

- `candidate-identity`
- `common-criteria`
- `evidence-quality`
- `sensitivity`
- `dissent`
- `human-decision`

#### Hard Gates

- Candidates may be ranked only against the same declared criteria and evidence basis; missing evidence, human preference, and uncertainty cannot be converted into fabricated scores.
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

#### Human Architecture and Risk Authority

The Skill may produce evidence, alternatives, tradeoffs, findings, and a recommendation. Architecture selection, autonomy expansion, risk acceptance, policy approval, migration approval, remediation authorization, and release decisions remain explicit human decisions with a named owner.

#### Status Mapping

- `passed`: output contract and every hard gate are satisfied with current evidence.
- `needs-input`: a requestable source, policy, compatibility fact, or decision is missing. Deliver every supported part first and name the owner for the missing part.
- `blocked`: proceeding would exceed authority, access secret values, mutate production, or cross a prohibited safety boundary.
- `failed`: authorized work ran but a deterministic gate or required output failed.

#### Non-Responsibilities

Adjacent capabilities:
- `architecture-interface-alternative-evaluation`
- `diagram-and-architecture-artifact-generation`
- `architecture-deep-module-design`
- `implementation-planning-and-handoff`

Never access or emit secret values, mutate production data or provider policy, grant AI action rights, execute remote Git, merge, deploy, release, or perform an adjacent capability. Review, reporting, and audit candidates never repair source.

## Mode: `architecture-deep-module-design`

### architecture-deep-module-design

#### Responsibility

Design one module boundary and interface that hides complexity, enforces dependency direction, preserves seams, and supports migration and verification.

#### Trigger

Use when the request matches any of:
- One module needs a smaller, deeper interface that hides complexity with a migration path
- Callers know too much about a module and someone must redesign its boundary without rewriting everything

Do not use when:
- Scan the codebase for evidence-backed module-deepening opportunities. Route to `architecture-deepening-discovery`.
- Generate at least two independent interface alternatives and compare them before choosing. Route to `architecture-interface-alternative-evaluation`.

#### Required Inputs

- A module, its interfaces and dependencies, or evidenced architectural friction.

#### Procedure

1. Freeze the module responsibility, callers, dependencies, data ownership, invariants, failure modes, change history, tests, and observed friction.
2. Identify what complexity must be hidden versus exposed as stable policy and reject boundaries based only on file layout or naming.
3. Define the smallest coherent interface, invariants, ownership, dependency direction, seams, failure behavior, and observability.
4. Map old-to-new behavior, compatibility, incremental migration, rollback, and affected tests without implementing the change.
5. Challenge the design for leakage, shallow delegation, temporal coupling, test fragility, and speculative extensibility before recommendation.

#### Domain Guidance

- Testability rules for the challenge step: accept dependencies instead of creating them inside the module, and return results instead of producing side effects, so the interface can be tested without mocking internals.

#### Output Contract

Produce:
- deep-module boundary
- interface and invariant contract
- dependency and seam map
- compatibility, migration, rollback, and test plan

Every material fact, boundary, recommendation, finding, test claim, migration step, or risk must cite supplied or authorized evidence or be labeled assumption/unknown.

Deliver each output as the artifact itself (tables, commands, patches, plans, records), not as a description of how it would be produced.

#### Coverage

- `information-hiding`
- `deep-module`
- `interface`
- `invariants`
- `dependency-direction`
- `seams`
- `migration-rollback`

#### Hard Gates

- A module is not deeper merely because code moved: the proposed interface must hide material complexity, reduce caller knowledge, preserve behavior, and have an incremental migration and rollback path.
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

#### Human Architecture and Risk Authority

The Skill may produce evidence, alternatives, tradeoffs, findings, and a recommendation. Architecture selection, autonomy expansion, risk acceptance, policy approval, migration approval, remediation authorization, and release decisions remain explicit human decisions with a named owner.

#### Status Mapping

- `passed`: output contract and every hard gate are satisfied with current evidence.
- `needs-input`: a requestable source, policy, compatibility fact, or decision is missing. Deliver every supported part first and name the owner for the missing part.
- `blocked`: proceeding would exceed authority, access secret values, mutate production, or cross a prohibited safety boundary.
- `failed`: authorized work ran but a deterministic gate or required output failed.

#### Non-Responsibilities

Adjacent capabilities:
- `architecture-deepening-discovery`
- `architecture-interface-alternative-evaluation`
- `data-and-api-contract-design`
- `implementation-planning-and-handoff`

Never access or emit secret values, mutate production data or provider policy, grant AI action rights, execute remote Git, merge, deploy, release, or perform an adjacent capability. Review, reporting, and audit candidates never repair source.

## Mode: `architecture-interface-alternative-evaluation`

### architecture-interface-alternative-evaluation

#### Responsibility

Generate at least two independent interface alternatives and compare information hiding, caller complexity, dependencies, failure behavior, testability, compatibility, and migration cost.

#### Trigger

Use when the request matches any of:
- A module interface is being chosen and several structurally different designs should be compared before committing
- Someone asks for alternative interface designs with their information hiding, failure behavior and migration cost

Do not use when:
- Design the full chosen module boundary, dependency direction, seams, and test plan. Route to `architecture-deep-module-design`.
- Format already-developed candidates into the final architecture decision report. Route to `architecture-candidate-reporting`.

#### Required Inputs

- A bounded module problem, constraints, and an interface-design objective.

#### Procedure

1. Freeze the problem, callers, invariants, constraints, compatibility needs, and evaluation criteria before ideation.
2. Generate at least two structurally independent alternatives rather than renamed signatures over the same boundary.
3. Specify each alternative's contract, hidden and exposed knowledge, dependencies, failure and concurrency semantics, tests, compatibility, migration, and rollback.
4. Compare with declared evidence and sensitivity, including a minimal-change or no-change option where valid.
5. Recommend or abstain for a named human owner; do not implement or silently choose based on taste.

#### Domain Guidance

- Default to three alternatives, each generated from its own brief so they differ in responsibility boundary or information hiding; use two only when constraints leave room for just two. Renamed signatures over the same boundary do not count.
- Include a minimal-change or no-change option when valid, and compare all options on the same declared criteria.
- Compare structurally distinct interface alternatives rather than several parameter variants of one facade. Give one provisional recommendation with explicit tradeoffs and what evidence would reverse it.
- Recompute every migration total from the supplied categories and show the arithmetic. Keep migratable sites, frozen compatibility sites and total call sites distinct; never relabel their sum.

#### Output Contract

Produce:
- independent interface alternatives
- contract and failure comparison
- migration and compatibility matrix
- human-owned recommendation

Every material fact, boundary, recommendation, finding, test claim, migration step, or risk must cite supplied or authorized evidence or be labeled assumption/unknown.

Deliver each output as the artifact itself (tables, commands, patches, plans, records), not as a description of how it would be produced.

#### Coverage

- `independent-alternatives`
- `information-hiding`
- `caller-complexity`
- `failure-semantics`
- `compatibility`
- `migration`

#### Hard Gates

- Alternatives must differ in responsibility boundary or information hiding; cosmetic signature variants do not satisfy divergent architecture evaluation.
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

#### Human Architecture and Risk Authority

The Skill may produce evidence, alternatives, tradeoffs, findings, and a recommendation. Architecture selection, autonomy expansion, risk acceptance, policy approval, migration approval, remediation authorization, and release decisions remain explicit human decisions with a named owner.

#### Status Mapping

- `passed`: output contract and every hard gate are satisfied with current evidence.
- `needs-input`: a requestable source, policy, compatibility fact, or decision is missing. Deliver every supported part first and name the owner for the missing part.
- `blocked`: proceeding would exceed authority, access secret values, mutate production, or cross a prohibited safety boundary.
- `failed`: authorized work ran but a deterministic gate or required output failed.

#### Non-Responsibilities

Adjacent capabilities:
- `architecture-deep-module-design`
- `architecture-candidate-reporting`
- `data-and-api-contract-design`
- `engineering-plan-review`

Never access or emit secret values, mutate production data or provider policy, grant AI action rights, execute remote Git, merge, deploy, release, or perform an adjacent capability. Review, reporting, and audit candidates never repair source.

## Mode: `frontend-runtime-boundaries-and-dependency-safety`

### frontend-runtime-boundaries-and-dependency-safety

#### Responsibility

Audit authorized frontend source so server-only logic, credentials, privileged actions, assets, dependencies, and runtime assumptions stay on safe explicit boundaries, and hand accepted repairs to the repair owner without editing source.

#### Trigger

Use when the request matches any of:
- A frontend build may leak server-only code, secrets or privileged logic into the browser bundle
- Someone asks whether client and server boundaries, third-party scripts and dependencies are safe before release

Do not use when:
- Design the visual token and component foundation for the interface. Route to `design-system-foundation-and-token-extraction`.
- Benchmark and optimize frontend rendering and interaction performance. Route to `frontend-rendering-and-interaction-performance`.
- Apply the accepted boundary or dependency repairs to source. Route to `defect-remediation`.

#### Required Inputs

- A frontend implementation, dependency graph, rendering environment, and integration constraints.

#### Procedure

1. Freeze authorized source scope, rendering environments, entry points, dependency graph, bundler behavior, environment variables, assets, browser targets, and existing tests.
2. Trace client imports, server-only modules, secrets, privileged APIs, dynamic code, third-party scripts, assets, globals, hydration, and environment branches across the build boundary.
3. Prefer platform or existing dependencies; identify unsafe or unnecessary packages and the server-enforced interface that should hold privileged computation or credentials.
4. Write each finding with file and line, the boundary crossed, the consequence, and the smallest recommended change, ready for defect-remediation after the owner accepts it.
5. Define host-run build, bundle, browser, SSR or hydration, and security checks for the repair to pass; report unavailable verification and never expose secret values.

#### Domain Guidance

- React Server Components: global state works only in client components; wrap providers in a 'use client' component and keep interactive leaves isolated. A server-only module imported from a client component is a boundary violation.
- Audit only. Repairs are a separate accepted action owned by defect-remediation.

#### Output Contract

Produce:
- runtime-boundary audit
- findings with file, line, boundary crossed and recommended change
- dependency and environment decision
- host verification and residual-risk plan

Every material fact, boundary, recommendation, finding, test claim, migration step, or risk must cite supplied or authorized evidence or be labeled assumption/unknown.

Deliver each output as the artifact itself (tables, commands, patches, plans, records), not as a description of how it would be produced.

#### Coverage

- `client-server-boundary`
- `no-client-secret`
- `server-enforcement`
- `dependency-safety`
- `assets`
- `SSR-hydration`
- `host-verification`

#### Hard Gates

- No server credential, secret-derived value, privileged authorization decision, filesystem or process API, or unsafe dynamic dependency may cross into a client bundle or browser-executable path.
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
- `design-system-foundation-and-token-extraction`
- `frontend-rendering-and-interaction-performance`
- `secrets-and-environment-governance`
- `authorization-and-permission-contracts`
- `defect-remediation`

Never access or emit secret values, mutate production data or provider policy, grant AI action rights, execute remote Git, merge, deploy, release, or perform an adjacent capability. Review, reporting, and audit candidates never repair source.

## Mode: `resilience-and-determinism`

### resilience-and-determinism

#### Responsibility

Diagnose and verify nondeterminism, retries, timeouts, cleanup, isolation, ordering, and recovery behavior under a frozen workload without source repair.

#### Trigger

Use when the request matches any of:
- A test or job fails intermittently and needs a reproducible failure model before anyone edits code
- Retries, timeouts, ordering or cleanup may be masking a race, leaked state or an arbitrary sleep

Do not use when:
- Apply the accepted source fix for the confirmed flaky root cause. Route to `defect-remediation`.
- Design the overall test portfolio and layer allocation. Route to `testing-portfolio-strategy`.

#### Required Inputs

- An observed nondeterministic or resilience failure with reproduction context: the failing test or job, logs, environment, and any suspected cause (invalid data, race, contamination, fragile wait).

#### Procedure

1. Freeze target identity, workload, environment, seeds, clocks, ordering, resources, retries, timeouts, and success criteria.
2. Repeat approved runs while varying one declared factor at a time and record exits, duration, logs, artifacts, and cleanup state.
3. List the candidate causes including arbitrary sleeps or fixed timeouts, and rank them by the evidence from the repeated runs.
4. Distinguish true recovery from retry masking, leaked state, non-idempotent side effects, race, external variance, and measurement noise.
5. Return a reproducible failure model, determinism or resilience verdict, and repair recommendation without editing source.

#### Domain Guidance

- First-class hypothesis: an arbitrary sleep or fixed timeout. Prefer condition-based waiting (poll for the specific state with a bounded timeout and a failure message naming the expected and last observed state) over longer sleeps.
- When the cause is invalid data, recommend validation at four layers: entry point, business logic, environment guard, and debug instrumentation.
- Deliver the concrete fix as a patch or code block for the owner to apply; do not withhold it as a vague candidate when the race is confirmed, and state exactly what remains unverified.
- Preserve existing approved timezone and business semantics. A proposed policyholder-zone change is a separate product decision, not an assumed implementation fix. Reproduction and repeat checks must use the unchanged semantics until that decision is approved.

#### Output Contract

Produce:
- determinism experiment record
- retry and timeout analysis
- cleanup and recovery evidence
- root-cause hypothesis and bounded recommendation

Every material action, command, result, finding, score, capture, provider receipt, or completion claim must bind to exact target identity and current evidence or be labeled assumption/unknown.

Deliver each output as the artifact itself (tables, commands, patches, plans, records), not as a description of how it would be produced.

#### Coverage

- `seed`
- `ordering`
- `timeout`
- `retry-masking`
- `idempotency`
- `cleanup`
- `failure-injection`
- `repeated-evidence`

#### Hard Gates

- A resilience claim requires repeated target-bound evidence with recorded seeds, ordering, environment, retries, timeouts, side effects, cleanup, and failure injection; one passing retry proves nothing.
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
- `root-cause-investigation`
- `defect-remediation`
- `baseline-regression-control`
- `testing-portfolio-strategy`

Never silently expand source, command, browser, data, credential, local-system, provider, or remote authority. Independent review, QA, audit, evidence acquisition, analysis, and triage never repair source. Setup and authentication never imply authority to perform the downstream action.
