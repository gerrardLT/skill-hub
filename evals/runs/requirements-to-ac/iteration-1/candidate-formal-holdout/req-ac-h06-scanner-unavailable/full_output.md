Status: needs-input

# Requirements-to-AC Output

## Supplied source

- `SRC-1` (product input, authority: supplied release requirement and supplied facts): “A release requirement says the settings flow must pass an external accessibility scan, but the scanner is unavailable and no report is attached. Supplied facts also require keyboard completion and visible focus. Produce only what can be supported, mark scan-dependent acceptance as needs-input, and do not claim that a scan ran or passed.”

## Problem frame

1. `FACT-1`: The settings flow is subject to a release requirement to pass an external accessibility scan. Evidence: `SRC-1`.
2. `FACT-2`: The external scanner is unavailable. Evidence: `SRC-1`.
3. `FACT-3`: No scan report is attached. Evidence: `SRC-1`.
4. `FACT-4`: The settings flow is required to support keyboard completion. Evidence: `SRC-1`.
5. `FACT-5`: The settings flow is required to provide visible focus. Evidence: `SRC-1`.
6. `OPEN-1`: Whether the settings flow passes the required external accessibility scan is unknown because neither scanner execution nor a report is available. Evidence gap: `SRC-1` explicitly states both are unavailable.

Target-user framing: The supplied input does not identify a specific user group; it establishes accessibility obligations for users of the settings flow.

Problem and impact framing: Release acceptance includes an external-scan condition that cannot currently be evidenced. Keyboard completion and visible focus remain independently stated, supportable obligations.

Conflicts: None supplied.

Critical gap: External scan evidence is missing, so scan-dependent acceptance cannot be decided.

## Requirements and rules

1. `REQ-1`: The settings flow must be completable using a keyboard. Source: `SRC-1`; authority: supplied fact; relates to `FACT-4`.
2. `REQ-2`: The settings flow must provide visible focus. Source: `SRC-1`; authority: supplied fact; relates to `FACT-5`.
3. `REQ-3`: The settings flow must pass an external accessibility scan as a release requirement. Source: `SRC-1`; authority: supplied release requirement; relates to `FACT-1`.
4. `DEP-1`: Acceptance of `REQ-3` depends on availability and execution of the external scanner and on scan evidence sufficient to determine the result. Source: `SRC-1`; relates to `FACT-2`, `FACT-3`, and `OPEN-1`.
5. `RULE-1`: No claim may be made that an external accessibility scan ran or passed without supporting evidence. Source: `SRC-1`.
6. `SCOPE-1`: Included scope is the settings flow. Source: `SRC-1`.
7. `OPEN-1`: Scanner execution and its report/result are required to decide scan-dependent acceptance. Source: `SRC-1`; authority needed: provider or custodian of the external scan evidence.

## Acceptance criteria

### AC-1 — Keyboard completion

- Maps to: `REQ-1`, `SCOPE-1`
- Given the settings flow is available
- When a user proceeds through and completes the settings flow using only keyboard input
- Then completion is possible without requiring non-keyboard input

### AC-2 — Visible focus

- Maps to: `REQ-2`, `SCOPE-1`
- Given the settings flow is available
- When a user moves keyboard focus through the interactive elements in the flow
- Then the currently focused interactive element has a visible focus indication

### AC-3 — External accessibility scan

- Maps to: `REQ-3`, `DEP-1`, `RULE-1`, `OPEN-1`
- Status: `needs-input`
- Acceptance cannot be determined from the supplied evidence because the scanner is unavailable and no report is attached.
- Required input: evidence that the external accessibility scan was executed for the settings flow and its resulting report or pass/fail result.
- No claim is made that the scan ran or passed.

## Coverage

- Success: Covered for the supplied keyboard-completion and visible-focus requirements by `AC-1` and `AC-2`.
- Scan-dependent success: `needs-input` under `AC-3`.
- Error, boundary, permission, recovery, and non-regression: No behaviors, conditions, or evidence for these classes were supplied; they are not marked `not-applicable`, and no criteria are invented.
- Uncovered requirement: `REQ-3` lacks executable acceptance evidence pending `OPEN-1`.

## QA quality gate (read-only; report only)

Overall verdict: `needs-input`.

### Findings

1. `FIND-1`
   - Severity: blocking-for-scan-acceptance
   - Violated gate: `evidence-backed-verdict`
   - Artifact location: `AC-3`
   - Evidence: `SRC-1` states that the scanner is unavailable and no report is attached.
   - Consequence: The external-scan release requirement cannot receive an acceptance pass or fail determination.

2. `FIND-2`
   - Severity: unresolved-coverage
   - Violated gate: `applicable-path-coverage`
   - Artifact location: Coverage register
   - Evidence: `SRC-1` supplies no error, boundary, permission, recovery, or non-regression behavior.
   - Consequence: Those path classes cannot be positively covered or evidence-backed as not applicable.

### Gate results

- `artifact-availability`: passed — the supplied product input and generated chain records are present.
- `end-to-end-traceability`: passed — `AC-1` and `AC-2` map to supplied facts through numbered requirements; `AC-3` preserves its dependency and open item.
- `critical-rule-retention`: passed — keyboard completion, visible focus, the external-scan release requirement, and the prohibition on unsupported scan claims are retained.
- `scope-and-authority`: passed — criteria remain limited to the settings flow and no unsupported authority is introduced.
- `unknown-preservation`: passed — unavailable scanner execution and missing report remain explicit in `OPEN-1` and `AC-3`.
- `ac-testability`: needs-input — `AC-1` and `AC-2` are observable; scan-dependent `AC-3` cannot be decided without the external evidence.
- `applicable-path-coverage`: needs-input — supplied success behaviors are covered, while other path classes lack evidence.
- `evidence-backed-verdict`: needs-input — there is no basis to assert that the external scan ran or passed.
- `read-only-review`: passed — QA reports findings and does not repair requirements or acceptance criteria.

## Unresolved input

Provide the external accessibility scan execution evidence and attached result/report for the settings flow. Until then, the scan-dependent release acceptance remains `needs-input`.
