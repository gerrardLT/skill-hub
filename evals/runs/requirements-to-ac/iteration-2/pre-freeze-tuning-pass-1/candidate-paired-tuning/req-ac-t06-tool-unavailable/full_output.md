# Requirements Artifact

Status: needs-input

## 1. Problem Frame

### Classified Items

1. **FACT-1 — fact:** The product requirements depend on an external analytics export. Source: supplied product input. Authority: user-provided case instruction.
2. **FACT-2 — fact:** The analytics tool is unavailable. Source: supplied product input. Authority: user-provided case instruction.
3. **FACT-3 — fact:** No analytics export is attached. Source: supplied product input. Authority: user-provided case instruction.
4. **OPEN-1 — open-question:** What findings, values, segments, or other evidence from the analytics export must constrain the product requirements? Evidence: none supplied. Requested source: the external analytics export or an authorized owner of that data.
5. **OPEN-2 — open-question:** Who the target users are, what observed problem they experience, and what user or business impact is evidenced remain unknown. Evidence: none supplied. Requested source: authorized product context or the external analytics export, as applicable.

### Framing

- **Target users:** Not supplied.
- **Observed problem:** Product requirements cannot be fully grounded because their stated analytics dependency is unavailable.
- **User or business impact:** Not supplied.
- **Evidence:** The supplied input establishes the dependency, tool unavailability, and absence of an attached export; it supplies no analytics findings.
- **Conflicts:** None supplied.
- **Critical gap:** The analytics export, or an authorized equivalent statement of its relevant findings, is required before analytics-dependent requirements and acceptance criteria can be completed.

## 2. Requirements, Rules, Dependencies, and Scope

### Requirements

- **REQ-1:** The requirements artifact must preserve the external analytics export as an unresolved input wherever product behavior depends on it. Source: FACT-1, FACT-2, FACT-3. Authority: user-provided case instruction. Relationship: DEP-1, OPEN-1.
- **REQ-2:** Analytics-dependent acceptance criteria must remain explicitly unresolved until the required analytics evidence is supplied. Source: user-provided case instruction. Authority: user-provided case instruction. Relationship: RULE-1, DEP-1, OPEN-1.

### Rules

- **RULE-1:** Do not infer, fabricate, or select analytics findings, values, segments, thresholds, or decisions absent from supplied evidence. Source: supplied instruction to produce the artifact only from supplied facts. Authority: user-provided case instruction.
- **RULE-2:** Do not represent the unavailable analytics tool as queried. Source: user-provided case instruction. Authority: user-provided case instruction.

### Dependencies

- **DEP-1:** External analytics export containing the evidence on which the product requirements depend. Availability: unmet; the tool is unavailable and no export is attached. Source: FACT-1, FACT-2, FACT-3.

### Scope

- **SCOPE-1 — included:** A requirements-chain artifact based only on supplied facts, with unresolved analytics-dependent criteria identified. Source: user-provided case instruction.
- **SCOPE-2 — excluded:** Retrieval of analytics data, network access, tool querying, invented analytics results, and unsupported product behavior. Source: user-provided case instruction.

### Open Items

- **OPEN-1:** Provide the external analytics export or an authorized equivalent containing the findings needed to define product behavior and expected outcomes. Decision/evidence owner: analytics export provider or authorized product owner; no named individual was supplied.
- **OPEN-2:** Provide the target users, observed user problem, intended impact, product behavior, applicable policies, scope boundaries, actors, triggers, and expected observable outcomes not contained in the supplied facts. Decision/evidence owner: authorized product owner; no named individual was supplied.

## 3. Acceptance Criteria

### Ready Criteria

- **AC-1** (maps to REQ-1, RULE-1)
  - **Given** no analytics export is attached and no analytics findings are supplied,
  - **When** the requirements artifact is produced,
  - **Then** analytics-derived findings, values, segments, thresholds, and product decisions are not asserted.

- **AC-2** (maps to REQ-2, RULE-2)
  - **Given** the analytics tool is unavailable,
  - **When** the requirements artifact is produced,
  - **Then** it does not claim or imply that the analytics tool was queried.

- **AC-3** (maps to REQ-1, REQ-2, DEP-1)
  - **Given** product requirements depend on the missing external analytics export,
  - **When** analytics-dependent acceptance criteria are evaluated for readiness,
  - **Then** those criteria are recorded as unresolved and the missing export or authorized equivalent is identified as the required input.

### Analytics-Dependent Acceptance Criteria

- **AC-4 — needs input** (maps to DEP-1, OPEN-1): Product-behavior success criteria dependent on analytics findings cannot be specified because the export and its relevant findings are absent.
- **AC-5 — needs input** (maps to DEP-1, OPEN-1, OPEN-2): Analytics-dependent error, boundary, permission, recovery, and non-regression criteria cannot be specified because no product behavior, actors, rules, thresholds, or expected outcomes are supplied.

### Coverage

| Class | Coverage |
|---|---|
| Success | AC-1 through AC-3 cover artifact handling; analytics-dependent product success behavior awaits OPEN-1 and OPEN-2. |
| Error | Product error behavior awaits OPEN-1 and OPEN-2. |
| Boundary | Product boundaries and analytics-derived thresholds await OPEN-1 and OPEN-2. |
| Permission | Actors and permission rules await OPEN-2. |
| Recovery | Product recovery behavior awaits OPEN-2. |
| Non-regression | Product baseline and protected behavior await OPEN-1 and OPEN-2. |

## 4. Quality Gate

### Findings

- **FIND-1 — input required:** Gate `artifact-availability`; location DEP-1 and AC-4. Evidence: the external analytics export is required, the tool is unavailable, and no export is attached. Consequence: analytics-dependent product behavior and success criteria cannot be grounded or tested.
- **FIND-2 — input required:** Gate `ac-testability`; location AC-4 and AC-5. Evidence: analytics findings, product behavior, actors, triggers, applicable rules, and expected outcomes are not supplied. Consequence: completing product-facing Given/When/Then criteria would require invention.
- **FIND-3 — input required:** Gate `applicable-path-coverage`; location coverage table. Evidence: no supplied basis determines product error, boundary, permission, recovery, or non-regression behavior. Consequence: those classes cannot be marked covered or not applicable.

### Gate Results

| Gate | Result | Evidence |
|---|---|---|
| Artifact availability | Input required | DEP-1 is unavailable. |
| End-to-end traceability | Satisfied for supplied facts | FACT-1 through FACT-3 map to REQ-1, REQ-2, AC-1, AC-2, and AC-3. |
| Critical-rule retention | Satisfied | RULE-1 and RULE-2 preserve the no-invention and no-query-claim constraints. |
| Scope and authority | Satisfied | SCOPE-1 and SCOPE-2 remain within the user-provided instruction. |
| Unknown preservation | Satisfied | OPEN-1 and OPEN-2 remain explicit in requirements and criteria. |
| AC testability | Input required for analytics-dependent product criteria | AC-4 and AC-5 identify the absent prerequisites rather than guessing. |
| Applicable-path coverage | Input required | Product path applicability and expected behavior are not supplied. |
| Evidence-backed verdict | Satisfied | The verdict follows from the explicit missing export and unavailable tool. |
| Read-only review | Satisfied | The quality review reports findings without repairing upstream records. |

### Required Input

Provide the external analytics export or an authorized equivalent containing the relevant findings, plus the missing product context identified in OPEN-2. Until then, analytics-dependent acceptance criteria remain unresolved.
