Status: needs-input

# Requirements and Acceptance Criteria Evaluation: Analytics Dashboard

## 1. Problem Framing (`problem-framing` v0.2.0-candidate)

### 1.1 Responsibility and Boundaries
This problem frame captures and classifies all supplied statements without proposing solutions, inventing personas, assuming metrics, or converting open unknowns into false certainty.

### 1.2 Classification Register
- **ITEM-001 (Fact)**: Leadership requires improved visibility via an analytics dashboard.
  - *Source*: Task prompt statement ("leadership wants better visibility").
  - *Authority*: Leadership.
  - *Evidence*: Explicitly supplied in prompt.
- **ITEM-002 (Open-Question)**: Specific user roles, access levels, and consumer personas are unknown.
  - *Source*: Task prompt statement ("no users ... are provided").
  - *Authority Required*: Leadership / Product Owner.
  - *Evidence*: Explicitly identified as missing.
- **ITEM-003 (Open-Question)**: Relevant business events, metrics, tracking telemetry, and domain dimensions are unknown.
  - *Source*: Task prompt statement ("no ... events ... are provided").
  - *Authority Required*: Leadership / Data Owner.
  - *Evidence*: Explicitly identified as missing.
- **ITEM-004 (Open-Question)**: Current visibility baseline or existing reporting baseline is unknown.
  - *Source*: Task prompt statement ("no ... baseline ... provided").
  - *Authority Required*: Data Owner / Analytics Team.
  - *Evidence*: Explicitly identified as missing.
- **ITEM-005 (Open-Question)**: Target visibility levels, benchmark thresholds, and performance targets are unknown.
  - *Source*: Task prompt statement ("no ... target ... provided").
  - *Authority Required*: Leadership.
  - *Evidence*: Explicitly identified as missing.
- **ITEM-006 (Open-Question)**: Designee for data ownership, governance, and business definitions is unknown.
  - *Source*: Task prompt statement ("no ... data owner ... provided").
  - *Authority Required*: Leadership.
  - *Evidence*: Explicitly identified as missing.
- **ITEM-007 (Open-Question)**: Decision deadline and delivery timeline are unknown.
  - *Source*: Task prompt statement ("no ... decision deadline are provided").
  - *Authority Required*: Leadership.
  - *Evidence*: Explicitly identified as missing.

### 1.3 Target-User Framing
- **Stated Stakeholder**: "Leadership".
- **Identified End-Users / Personas**: None provided. In accordance with boundaries, no personas, user segments, or roles are invented.

### 1.4 Problem and Impact Framing
- **Observed Problem**: Current operational or business visibility is insufficient to meet leadership's needs ("wants better visibility").
- **Business Impact**: Impaired decision-making capability due to lack of visibility. Precise impact cannot be quantified without baseline and target metrics.
- **Conflicts**: None supplied.

### 1.5 Critical Gaps Register
- **GAP-01**: Missing target users/roles prevents framing user interaction and authorization boundaries.
- **GAP-02**: Missing event/metric definitions prevents framing domain boundaries and data ingestion scope.
- **GAP-03**: Missing baseline and target benchmarks prevents establishing measurable business impact.
- **GAP-04**: Missing data owner leaves data governance authority undefined.
- **GAP-05**: Missing decision deadline leaves initiative sequencing undefined.

**Stage Status**: `needs-input`

---

## 2. Requirements & Rules (`requirements-rules` v0.2.0-candidate)

### 2.1 Responsibility and Boundaries
Normalizes framed statements into numbered requirement, rule, dependency, scope, and open-item records. Excludes acceptance criteria authoring, solution implementation details, and invented policies.

### 2.2 Requirements Register
- **REQ-001**: The analytics dashboard shall provide operational visibility to leadership based on authorized metrics and events once defined.
  - *Source*: ITEM-001.
  - *Authority*: Leadership.
  - *Rationale*: Direct fulfillment of leadership's visibility objective.
  - *Status*: Parameterized / Incomplete pending resolution of OPEN-001 through OPEN-004.

### 2.3 Rules Register
- **RULE-001**: Metric definitions, event instrumentation schemas, and user personas shall not be implemented without sign-off from the designated Data Owner and Leadership.
  - *Source*: Task prompt constraint ("do not invent metrics or personas").
  - *Authority*: Governance / Task Boundary.
  - *Rationale*: Prevents false certainty and unverified data structures.

### 2.4 Scope Register
- **SCOPE-001 (Included Scope)**: Functional visibility dashboard for leadership based on verified events and metrics.
- **SCOPE-002 (Excluded / Deferred Scope)**: Specific data schemas, metric algorithms, UI layouts, report delivery mechanisms, and persona-specific dashboards until missing inputs are authorized.

### 2.5 Dependency Register
- **DEP-001**: REQ-001 is dependent on the formal designation of a Data Owner (resolving OPEN-005).
- **DEP-002**: REQ-001 is dependent on specification of target users and tracking events (resolving OPEN-001 and OPEN-002).
- **DEP-003**: Baseline and target definition (resolving OPEN-003 and OPEN-004) is required prior to defining performance and validation criteria.

### 2.6 Open Items Register
- **OPEN-001**: Target Users — Which specific user roles or leadership personas will access and use the dashboard? (Source: ITEM-002; Authority: Leadership / Product Owner).
- **OPEN-002**: Events & Metrics — What specific business events, activities, telemetry data, and metrics must be displayed? (Source: ITEM-003; Authority: Leadership / Data Owner).
- **OPEN-003**: Baseline — What is the current operational visibility baseline, data source, or reporting tool? (Source: ITEM-004; Authority: Data Owner / Analytics Team).
- **OPEN-004**: Target — What quantitative or qualitative target goals, refresh rates, or success thresholds must the dashboard achieve? (Source: ITEM-005; Authority: Leadership).
- **OPEN-005**: Data Owner — Who is the designated authority responsible for data integrity, governance, and metric approval? (Source: ITEM-006; Authority: Leadership).
- **OPEN-006**: Decision Deadline — What is the deadline for finalizing requirements and delivering the dashboard? (Source: ITEM-007; Authority: Leadership).

### 2.7 Traceability
- `REQ-001` traces to `ITEM-001`.
- `RULE-001` traces to Task prompt constraints.
- `SCOPE-001`, `SCOPE-002` trace to `ITEM-001` and `GAP-01` through `GAP-05`.
- `DEP-001`, `DEP-002`, `DEP-003` trace to `OPEN-001` through `OPEN-005`.

**Stage Status**: `needs-input`

---

## 3. Acceptance Criteria (`acceptance-criteria` v0.2.0-candidate)

### 3.1 Readiness Assessment & Precondition Check
- **Readiness Gate**: FAILED.
- **Evaluated Prerequisites**:
  - *Actor / Role Context*: Absent (no users or personas provided).
  - *Trigger / Event Context*: Absent (no business events or tracking telemetry provided).
  - *Observable Behavior & Thresholds*: Absent (no baseline, target, or metric formulas provided).
  - *Authoritative Approval*: Incomplete (data owner unassigned).
- **Enforcement of `unknown-precondition-stop`**:
  Under the contract rules, the author is forbidden from inventing preconditions, actors, thresholds, permissions, or recovery paths ("Never guess", "Fail closed because fabricated preconditions make criteria executable-looking but invalid").
  Because the observable direction, actors, and events are completely absent, criteria cannot be parameterized and scenario generation is halted.

### 3.2 Criteria Register
- No Given/When/Then criteria are authored at this stage.
- *Rationale*: Authoring criteria such as "Given a leadership user..." or "When viewing monthly events..." would constitute `fabricated-fact` and `untestable-acceptance-criteria`.

### 3.3 Coverage Class Register (Pending Inputs)
- **Success Paths**: Pending resolution of OPEN-001, OPEN-002, OPEN-004.
- **Error Paths**: Pending resolution of OPEN-002, OPEN-005.
- **Boundary Paths**: Pending resolution of OPEN-003, OPEN-004.
- **Permission Paths**: Pending resolution of OPEN-001, OPEN-005.
- **Recovery Paths**: Pending resolution of OPEN-005.
- **Non-Regression Paths**: Pending resolution of OPEN-003, OPEN-005.

### 3.4 Unresolved Inputs
- Full authoring of acceptance criteria is blocked until OPEN-001 through OPEN-006 are resolved by authorized leadership and data ownership.

**Stage Status**: `needs-input`

---

## 4. Requirements Quality Gate (`requirements-quality-gate` v0.2.0-candidate)

### 4.1 Audit Procedure
Read-only evaluation of artifacts produced across Problem Framing, Requirements Rules, and Acceptance Criteria against declared gates.

### 4.2 Gate Evaluation Matrix

| Gate | Status | Evidence & Audit Notes |
| :--- | :---: | :--- |
| **artifact-availability** | PASSED | Problem framing, requirement registers, open items, and gate assessments are present and structured. |
| **end-to-end-traceability** | PASSED | Upstream input statements are traced through items ITEM-001..007 to REQ-001, RULE-001, and OPEN-001..006. |
| **critical-rule-retention** | PASSED | The task directive to "not invent metrics or personas" and fail-closed rules are strictly maintained. |
| **scope-and-authority** | NEEDS-INPUT | Leadership authority is cited, but governance authority (Data Owner) is unassigned. |
| **unknown-preservation** | PASSED | All 6 missing inputs (users, events, baseline, target, data owner, decision deadline) are preserved as open unknowns without loss. |
| **ac-testability** | NEEDS-INPUT | Testable AC cannot be generated because prerequisites are absent; unknown-precondition-stop gate triggered correctly. |
| **applicable-path-coverage** | NEEDS-INPUT | Coverage classes cannot be verified until behavioral triggers, actors, and metrics are defined. |
| **evidence-backed-verdict** | PASSED | Status is derived strictly from supplied prompt facts and contract constraints. |
| **read-only-review** | PASSED | No upstream content has been repaired, assumed, or rewritten. |

### 4.3 Findings Register
- **FINDING-001 (Severity: High, Gate: `ac-testability` / `requirements-readiness`)**:
  - *Location*: Acceptance Criteria Stage.
  - *Evidence*: Task explicitly states that no users, events, baseline, target, data owner, or decision deadline are provided.
  - *Consequence*: Testable Given/When/Then acceptance criteria cannot be drafted without inventing actors, triggers, and thresholds.
- **FINDING-002 (Severity: Medium, Gate: `scope-and-authority`)**:
  - *Location*: Requirements Stage (DEP-001, OPEN-005).
  - *Evidence*: Data owner is not designated.
  - *Consequence*: Metric and schema authority cannot be validated.

**Stage Status**: `needs-input`

---

## Minimum Missing Inputs Request

To proceed with drafting valid, testable requirements and Given/When/Then acceptance criteria without inventing personas or metrics, please provide the following minimum missing inputs:

1. **Target Users**: Who are the specific users or leadership roles who will access and use the dashboard?
2. **Events & Metrics**: What specific business events, metrics, or key performance indicators (KPIs) must be displayed?
3. **Baseline**: What is the current baseline visibility, data source, or reporting mechanism?
4. **Target**: What is the target performance level, success metric, or decision-support outcome expected from this dashboard?
5. **Data Owner**: Who is the designated authoritative owner responsible for the underlying data and metric definitions?
6. **Decision Deadline**: What is the decision deadline and target delivery timeline for this initiative?

Status: needs-input
