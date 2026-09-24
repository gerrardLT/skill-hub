Status: passed

# Acceptance Criteria Artifact

## 1. Acceptance criteria

### AC-1 — Preserve acknowledgement context at successful handover

**Given** a known alarm acknowledgement context exists before handover for an alarm identified by its existing alarm ID  
**And** acknowledgement history is available under the applicable runtime predicate  
**And** the evening coordinator is permitted to access the context under the applicable permission state  
**When** the daytime-to-evening coordinator handover occurs and the evening coordinator accesses the acknowledgement context for that existing alarm ID  
**Then** the known acknowledgement context remains available to the evening coordinator after takeover  
**And** it remains associated with the same existing alarm ID.

**Maps to:** REQ-1, REQ-2, REQ-4, RULE-1, RULE-2, RULE-3, DEP-1, DEP-2, SCOPE-1, SCOPE-2, SCOPE-3  
**Source trace:** SRC-1 `Problem`, `Primary user`, `Goal`, `Constraint`, `Include`, `Do not`; SRC-3

---

### AC-2 — Preserve acknowledgement context when the acknowledgement is stale

**Given** a known acknowledgement context exists for an alarm identified by its existing alarm ID  
**And** the acknowledgement is classified as stale by the applicable runtime predicate  
**And** acknowledgement history is available  
**And** the evening coordinator is permitted to access the context  
**When** the daytime-to-evening coordinator handover occurs and the evening coordinator accesses the context for that existing alarm ID  
**Then** the known acknowledgement context remains available to the evening coordinator while the acknowledgement is classified as stale  
**And** it remains associated with the existing alarm ID.

**Maps to:** REQ-1, REQ-3, REQ-4, RULE-1, RULE-2, RULE-3, DEP-1, DEP-2, SCOPE-2, SCOPE-3  
**Source trace:** SRC-1 `Goal`, `Include`, `Constraint`, `Do not`; SRC-3

---

### AC-3 — Enforce a not-permitted permission state

**Given** acknowledgement context is available for an alarm identified by its existing alarm ID  
**And** the applicable permission state classifies the evening coordinator as not permitted to access that context  
**When** the daytime-to-evening coordinator handover occurs and the evening coordinator attempts to access the acknowledgement context  
**Then** the acknowledgement context is not made available to that evening coordinator.

**Maps to:** REQ-2, REQ-4, RULE-2, RULE-3, DEP-2, SCOPE-3, SCOPE-5  
**Source trace:** SRC-1 `Goal`, `Include`, `Do not`; SRC-3

---

### AC-4 — Do not report unavailable acknowledgement history as available

**Given** the applicable runtime predicate classifies acknowledgement history for an existing alarm ID as unavailable  
**And** the evening coordinator is permitted to access acknowledgement context when that history is available  
**When** the evening coordinator attempts to access the acknowledgement context during takeover  
**Then** the unavailable acknowledgement history is not represented as available to the evening coordinator  
**And** acknowledgement context belonging to a different identifier is not substituted as the context for the existing alarm ID.

**Maps to:** REQ-1, REQ-5, RULE-1, RULE-2, RULE-6, DEP-1, DEP-2, SCOPE-3, SCOPE-7  
**Source trace:** SRC-1 `Problem`, `Goal`, `Include`, `Constraint`

---

### AC-5 — Retain the unavailable outcome while history is recoverable but not restored

**Given** acknowledgement history for an existing alarm ID was unavailable  
**And** the applicable recovery predicate now classifies that history as recoverable  
**And** the applicable history-availability predicate still classifies it as unavailable rather than restored and available  
**And** the evening coordinator is permitted to access the context when it is available  
**When** the evening coordinator accesses the acknowledgement context during or after handover  
**Then** the acknowledgement context remains unavailable while the history-availability predicate remains unavailable  
**And** the recoverable state is not treated as a restored and available state  
**And** the existing alarm ID remains the authoritative identifier for the recovery state.

**Maps to:** REQ-5, REQ-6, RULE-1, RULE-2, DEP-1, DEP-2, SCOPE-3  
**Source trace:** SRC-1 `Goal`, `Include`, `Constraint`

---

### AC-6 — Make acknowledgement context available after history is restored

**Given** acknowledgement history for an existing alarm ID was previously unavailable  
**And** the applicable runtime predicates now classify the history as restored and available  
**And** a known acknowledgement context remains associated with that existing alarm ID  
**And** the evening coordinator is permitted to access the context  
**When** the evening coordinator accesses the acknowledgement context after restoration  
**Then** the known acknowledgement context is available to the evening coordinator  
**And** it is available under the same existing alarm ID.

**Maps to:** REQ-1, REQ-2, REQ-4, REQ-5, REQ-6, RULE-1, RULE-2, RULE-3, DEP-1, DEP-2, SCOPE-3  
**Source trace:** SRC-1 `Goal`, `Include`, `Constraint`, `Do not`; SRC-3

---

### AC-7 — Keep the existing alarm ID authoritative across all included states

**Given** an alarm has an existing alarm ID  
**And** the test independently establishes one of the following states: available at handover, stale acknowledgement, unavailable history, recoverable history, or restored history  
**When** acknowledgement context or its history or recovery state is handled during the daytime-to-evening coordinator handover  
**Then** every observable association of that context or state identifies the alarm by its existing alarm ID  
**And** no alternate identifier is represented as superseding the existing alarm ID as the authoritative identifier.

**Maps to:** REQ-1, REQ-2, REQ-3, REQ-5, REQ-6, RULE-1, RULE-2, DEP-1, DEP-2, SCOPE-3  
**Source trace:** SRC-1 `Goal`, `Constraint`, `Include`

**Execution note:** AC-7 is parameterized and must be exercised separately for each listed state.

## 2. Requirement coverage

| Requirement | Covered by | Coverage |
|---|---|---|
| REQ-1 — Preserve acknowledgement context across handover | AC-1, AC-2, AC-4, AC-6, AC-7 | Covered |
| REQ-2 — Include successful preservation | AC-1, AC-3, AC-6, AC-7 | Covered |
| REQ-3 — Include stale acknowledgement state | AC-2, AC-7 | Covered |
| REQ-4 — Condition behavior on permission state | AC-1, AC-2, AC-3, AC-4, AC-5, AC-6 | Covered |
| REQ-5 — Include unavailable-history state | AC-4, AC-5, AC-6, AC-7 | Covered |
| REQ-6 — Include recovery behavior | AC-5, AC-6, AC-7 | Covered |

**Uncovered requirements:** None.

## 3. Coverage by applicable class

| Applicable class | Acceptance criteria | Coverage result |
|---|---|---|
| Success | AC-1; restored success in AC-6 | Covered |
| Error / unavailable history | AC-4; continued unavailability in AC-5 | Covered to the supplied authority boundary; no error message, cause, or presentation behavior is invented |
| Boundary | AC-2 for stale acknowledgement; AC-5 for recoverable-but-not-restored history | Covered |
| Permission | Permitted paths in AC-1, AC-2, AC-4, AC-5, and AC-6; not-permitted path in AC-3 | Covered |
| Recovery | Recoverable state in AC-5; restored state in AC-6 | Covered |
| Non-regression | AC-7, with same-ID assertions in AC-1, AC-2, AC-4, AC-5, and AC-6 | Covered |

## 4. Rule and scope handling

- **RULE-1:** Directly verified by AC-1, AC-2, AC-4, AC-5, AC-6, and AC-7.
- **RULE-2:** Staleness, permission, history availability, and recovery remain parameterized runtime predicates. No threshold, role matrix, failure taxonomy, or recovery value is introduced.
- **RULE-3:** AC-3 tests the supplied not-permitted state without defining or changing the permission policy.
- **RULE-4:** No UI, presentation design, architecture, storage mechanism, vendor, framework, or implementation stack is prescribed.
- **RULE-5:** All product-behavior criteria retain shift coordinators as the primary users. Support agents are not recast as shift coordinators or assigned invented product behavior.
- **RULE-6:** AC-4 asserts only observable unavailability and does not attribute it to deletion, persistence, synchronization, filtering, permission denial, or another cause.
- **RULE-7:** The aggregate evidence inventory is not converted into a runtime acceptance criterion, incident rate, prevalence measure, trend, or record-level claim.
- **RULE-8:** No additional operational, service, financial, business, or safety impact is asserted.
- **RULE-9:** No criterion changes the supplied goal, source-of-truth constraint, included behavior classes, or exclusions.

## 5. Parameterized prerequisites and unresolved inputs

### Parameterized test prerequisites

QA execution must obtain the following from the applicable runtime or test authority rather than from these criteria:

1. A test alarm with an existing alarm ID and known acknowledgement context.
2. The applicable stale or not-stale classification.
3. The applicable permitted or not-permitted classification.
4. The applicable available or unavailable history classification.
5. The applicable recoverable or restored recovery classification.
6. An implementation-supported means to observe whether context is available and which alarm ID is authoritative, without requiring a particular UI or technical stack.

### Unresolved inputs

None requiring product input before these criteria can be used.

The following remain intentionally unspecified and are not acceptance assumptions:

- Staleness thresholds or classification algorithms.
- Permission roles, matrices, or authorization rules.
- Causes or technical categories of unavailable history.
- Recovery timing, retry count, retry behavior, or fallback behavior.
- Error wording or presentation.
- UI and interaction design.
- Architecture, storage mechanism, and implementation stack.
- A finer decomposition of “alarm acknowledgement context.”
- Record-level incident findings or interview contents.

## 6. Conflicts and unknown prerequisites

- **Authority conflicts:** None identified.
- **Requirement conflicts:** None identified.
- **Unknown product decisions blocking acceptance criteria:** None.
- **Unsupported fallback behavior:** None added.
- **Unsupported cause claims:** None added.
- **Unsupported evidence or impact claims:** None added.

## 7. Gate results

- **given-when-then-structure:** passed — Every acceptance criterion contains explicit Given, When, and Then clauses.
- **observability:** passed — Outcomes are expressed as context availability, non-availability, preservation across takeover, recovery availability, and observable authoritative-ID association.
- **applicable-success-coverage:** passed — Successful handover preservation is covered by AC-1, and successful availability after restoration is covered by AC-6.