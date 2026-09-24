# Capability 1: Problem Framing

## 1. Status
**Status**: `needs-input`

## 2. Classification Register
| ID | Category | Statement | Evidence / Source Citation | Stated Authority |
|---|---|---|---|---|
| **FACT-01** | `fact` | The requirements depend on an external analytics export. | Supplied Task statement: *"The requirements depend on an external analytics export"* | Task Brief |
| **FACT-02** | `fact` | The external analytics tool is unavailable. | Supplied Task statement: *"the analytics tool is unavailable"* | Task Brief |
| **FACT-03** | `fact` | No external analytics export is attached. | Supplied Task statement: *"no export is attached"* | Task Brief |
| **FACT-04** | `fact` | The external analytics tool was not queried. | Supplied Task constraint & offline execution boundary: *"do not claim that the tool was queried"* | Task Brief |
| **OQ-01** | `open-question` | What is the schema, data format, and content of the external analytics export required by the dependent requirements? | Inferred directly from FACT-01, FACT-02, and FACT-03; export artifact is absent. | External Analytics Authority / Data Provider |

*Note: No conflicting statements were supplied (`conflict`: none).*

## 3. Solution-Free Problem Framing
- **Target Users**: Consumers and engineering stakeholders of the analytics-dependent requirements.
- **Observed Problem**: The requirements have a direct dependency on an external analytics export, but the analytics tool is currently unavailable and no export file or payload has been attached to the input.
- **User / Business Impact**: Specifications, concrete data validation rules, and acceptance verification that rely on the external analytics export cannot be completed or tested with actual data schemas without obtaining the export artifact.
- **Evidence Links**: Task brief supplied statements (FACT-01, FACT-02, FACT-03, FACT-04).
- **Critical Gaps**: Missing external analytics export artifact (OQ-01).

---

# Capability 2: Requirements Rules

## 1. Status
**Status**: `needs-input`

## 2. Requirements Register (`REQ-n`)
- **REQ-01**: The system specification shall define and process behaviors dependent on the external analytics export once the export artifact is supplied.
  - **Source Link**: FACT-01, FACT-03.
  - **Authority**: Task Brief.
  - **Rationale**: The requirements specifically depend on data from an external analytics export.
  - **Relationships**: Depends on `DEP-01`, governed by `RULE-01`, `RULE-02`.
- **REQ-02**: The requirements artifact shall be derived strictly from supplied facts without querying the unavailable external analytics tool.
  - **Source Link**: FACT-02, FACT-04.
  - **Authority**: Task Brief.
  - **Rationale**: The analytics tool is unavailable and offline execution boundaries prohibit querying or claiming a query.
  - **Relationships**: Governs all requirements generation.

## 3. Rules Register (`RULE-n`)
- **RULE-01 (No Synthetic Fabrication)**: In the absence of the external analytics export, requirements and downstream criteria shall not invent schema structures, data fields, or analytical values.
  - **Source Link**: FACT-02, FACT-03, FACT-04.
  - **Authority**: Task Brief.
  - **Rationale**: Invented premises propagate false certainty and violate boundary constraints.
- **RULE-02 (Needs-Input Gating)**: Any acceptance criterion or requirement rule directly contingent upon the external analytics export shall be designated as `needs-input` until the export artifact is provided by an authorized source.
  - **Source Link**: TASK instruction (*"mark the analytics-dependent acceptance criteria as needs-input"*).
  - **Authority**: Task Brief.
  - **Rationale**: Preserves unresolved dependency boundary without failing closed prematurely when the artifact can be requested.

## 4. Dependency Register (`DEP-n`)
- **DEP-01**: External Analytics Export.
  - **Source**: FACT-01, FACT-02, FACT-03.
  - **Status**: Unavailable / Not Attached.
  - **Required Authority / Provider**: External Analytics Tool / Data Engineering Owner.
  - **Impact**: Blocks completion of analytics-dependent acceptance verification.

## 5. Scope Register (`SCOPE-n`)
- **SCOPE-01 (In-Scope)**:
  - Identification and normalization of supplied facts and constraints.
  - Explicit marking of analytics-dependent downstream criteria as `needs-input`.
  - Preservation of dependencies and unknowns without fabricating export data.
- **SCOPE-02 (Out-of-Scope)**:
  - Querying or accessing the external analytics tool.
  - Inventing schemas, thresholds, or payload contents of the analytics export.
  - Resolving analytics-dependent behavior prior to export delivery.

## 6. Open Items Register (`OPEN-n`)
- **OPEN-01**: Delivery of external analytics export file or formal export schema definition.
  - **Source**: OQ-01, DEP-01.
  - **Resolution Authority**: External Analytics Tool Administrator / Provider.
  - **Target Outcome**: Unblock analytics-dependent criteria.

---

# Capability 3: Acceptance Criteria

## 1. Status
**Status**: `needs-input`

## 2. Acceptance Criteria Set (`AC-n`)

### AC-01: Offline Specification Boundary (Non-Regression / Boundary Path)
- **Traceability**: Maps to `REQ-02`, `RULE-01`, `SCOPE-01`.
- **Class**: Boundary / Non-regression.
- **Criterion Status**: `passed` (Ready and verifiable).
- **Scenario**:
  - **Given** the external analytics tool is unavailable and no export artifact is attached,
  - **When** the requirements baseline is generated,
  - **Then** the artifact is produced solely from verified supplied facts,
  - **And** the external analytics tool is not queried,
  - **And** no fabricated export values, data fields, or schemas are asserted.

### AC-02: Analytics-Dependent Processing (Functional Success Path)
- **Traceability**: Maps to `REQ-01`, `DEP-01`, `RULE-02`, `OPEN-01`.
- **Class**: Success path (Analytics-dependent).
- **Criterion Status**: `needs-input` (Analytics-dependent; awaiting external analytics export).
- **Scenario**:
  - **Given** the system is configured to process the external analytics export,
  - **And** the external analytics export has not been attached and the analytics tool was not queried,
  - **When** analytics-dependent validation and calculation rules are evaluated,
  - **Then** the acceptance evaluation cannot proceed to completion and must remain in a `needs-input` status pending receipt of the external analytics export artifact.

### AC-03: Analytics Export Ingestion and Schema Conformance (Boundary / Error Path)
- **Traceability**: Maps to `REQ-01`, `RULE-01`, `RULE-02`, `DEP-01`.
- **Class**: Error / Boundary path (Analytics-dependent).
- **Criterion Status**: `needs-input` (Analytics-dependent; awaiting external analytics export schema).
- **Scenario**:
  - **Given** an external analytics export is required for downstream verification,
  - **And** the analytics tool is unavailable,
  - **When** verification of export contents is required,
  - **Then** the verification process halts without assuming schema conformance or fabricating fallback values,
  - **And** an explicit request for the external analytics export artifact is issued.

## 3. Applicable-Class Coverage & Traceability Register
| Criteria ID | Covered Requirement / Rule | Coverage Class | Criterion Status | Notes / Unresolved Inputs |
|---|---|---|---|---|
| **AC-01** | REQ-02, RULE-01, SCOPE-01 | Boundary / Non-regression | `passed` | Fully testable against supplied task facts. Tool not queried. |
| **AC-02** | REQ-01, DEP-01, RULE-02 | Success (Analytics-dependent) | `needs-input` | Blocked on missing external analytics export (`DEP-01`). |
| **AC-03** | REQ-01, RULE-01, RULE-02 | Boundary / Error (Analytics-dependent) | `needs-input` | Blocked on missing export schema (`DEP-01`, `OPEN-01`). |
| *Permission* | N/A | Permission | `not-applicable` | No permission or access control rules supplied in task brief. |
| *Recovery* | N/A | Recovery | `not-applicable` | Recovery rules contingent upon obtaining missing export artifact. |

## 4. Unresolved Inputs
- **UNRES-01**: External analytics export artifact/file.
  - **Impact**: Precludes concrete assertion of data fields, thresholds, and success criteria in `AC-02` and `AC-03`.
  - **Tool Query Confirmation**: The external analytics tool was not queried.

---

# Capability 4: Requirements Quality Gate

## 1. Review Status
**Status**: `needs-input`

## 2. Gate Results Register
| Gate Name | Verdict | Positive Evidence Cited / Justification |
|---|---|---|
| **artifact-availability** | `passed` | Problem Frame, Requirements & Rules, and Acceptance Criteria are fully produced within this artifact. External export dependency is formally registered. |
| **end-to-end-traceability** | `passed` | Complete traceability maintained: `FACT-01..04` -> `REQ-01..02`, `RULE-01..02`, `DEP-01` -> `AC-01..03`. |
| **critical-rule-retention** | `passed` | `RULE-01` (no synthetic fabrication) and `RULE-02` (needs-input gating) are enforced across all artifacts. |
| **scope-and-authority** | `passed` | Authority boundaries strictly respected; no out-of-scope tool queries or unauthorized assumptions made. |
| **unknown-preservation** | `passed` | Missing export dependency (`DEP-01`, `OPEN-01`, `UNRES-01`) is preserved explicitly; no defaults or mock schemas invented. |
| **ac-testability** | `passed` | Criteria formatted in Given/When/Then; non-dependent AC (`AC-01`) is verifiable; analytics-dependent ACs (`AC-02`, `AC-03`) are designated `needs-input`. |
| **applicable-path-coverage** | `passed` | Boundary, non-regression, success, and error paths addressed; permissions and recovery marked not-applicable based on supplied material. |
| **evidence-backed-verdict** | `passed` | Findings and statuses cite direct statements from the supplied task brief. |
| **read-only-review** | `passed` | Read-only evaluation performed without mutating upstream contracts or fabricating missing domain context. |

## 3. Findings Register (`FIND-n`)
- **FIND-01**:
  - **Severity**: Informational / Gate Precondition.
  - **Violated Gate**: None (Contract compliance verified).
  - **Location**: Capability 3 (Acceptance Criteria, `AC-02`, `AC-03`).
  - **Evidence**: Task states: *"The requirements depend on an external analytics export, but the analytics tool is unavailable and no export is attached."*
  - **Consequence**: Full execution of acceptance criteria `AC-02` and `AC-03` requires delivery of the external analytics export. Per capability contract, missing evidence that can be requested from an identifiable authority yields `needs-input`.

## 4. Tool Status Confirmation
- The external analytics tool was not queried.

Status: needs-input
