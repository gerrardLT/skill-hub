Status: needs-input

# Requirements-to-AC Evaluation

## Problem frame

1. `FACT-1` — The requested capability imports customer records from a CSV file. Source: case prompt.
2. `FACT-2` — Malformed rows must be rejected while valid rows are preserved. Source: case prompt.
3. `FACT-3` — A row-level error report must be shown. Source: case prompt.
4. `FACT-4` — Retry must not create duplicate records. Source: case prompt.
5. `FACT-5` — Import must stop when the file exceeds the documented size limit. Source: case prompt.
6. `OPEN-1` — The numeric value and unit of the documented file size limit are not supplied. Source: case prompt explicitly identifies this omission. This unknown is material to executable boundary criteria and is not inferred.

Target user: not supplied.

Problem and impact: Customer-record CSV imports need defined behavior for mixed valid and malformed rows, diagnostic reporting, safe retry, and oversized files. User and business impacts beyond those behavioral constraints are not supplied.

Conflicts: none supplied.

## Requirements and rules

- `REQ-1` — The import shall accept a CSV containing customer records. Source: `FACT-1`; authority: case prompt.
- `REQ-2` — For a file within the documented size limit, the import shall reject each malformed row and preserve each valid row. Source: `FACT-2`; authority: case prompt; relationships: `RULE-1`, `OPEN-1`.
- `REQ-3` — The import shall provide a row-level error report for malformed rows. Source: `FACT-3`; authority: case prompt; relationship: `REQ-2`.
- `REQ-4` — Retrying an import shall not create duplicate customer records. Source: `FACT-4`; authority: case prompt.
- `REQ-5` — When a file exceeds the documented size limit, the import shall stop. Source: `FACT-5`; authority: case prompt; relationship: `OPEN-1`.
- `RULE-1` — Malformed rows do not prevent valid rows in the same eligible file from being preserved. Source: combined explicit wording of `FACT-2`; authority: case prompt.
- `RULE-2` — An oversized file is a hard-stop condition. Source: `FACT-5`; authority: case prompt; relationship: `OPEN-1`.
- `RULE-3` — Retry is non-duplicating. Source: `FACT-4`; authority: case prompt.
- `SCOPE-1` — Included: CSV customer-record import, malformed-row handling, valid-row preservation, row-level reporting, retry duplicate prevention, and file-size enforcement. Source: case prompt.
- `OPEN-1` — Supply the documented numeric file size limit and its unit through the authorized product contract. Until supplied, the exact at-limit and over-limit fixtures cannot be defined and successful acceptance of the complete import contract cannot be claimed.

Dependencies: no external dependency is supplied. Evaluation of `REQ-5` depends on resolving `OPEN-1`.

## Acceptance criteria

The following criteria preserve the unknown limit symbolically as `DOCUMENTED_SIZE_LIMIT`; they do not assign it a value. Criteria requiring exact boundary fixtures remain non-executable until `OPEN-1` is resolved.

### AC-1 — Mixed-row partial success

Mapping: `REQ-2`, `RULE-1`

Given a CSV whose file size is within `DOCUMENTED_SIZE_LIMIT` and that contains at least one valid customer row and at least one malformed row  
When the CSV import is performed  
Then every valid row is preserved as a customer record  
And every malformed row is rejected  
And rejection of malformed rows does not roll back or discard the valid rows.

### AC-2 — Row-level malformed-row report

Mapping: `REQ-2`, `REQ-3`

Given a CSV within `DOCUMENTED_SIZE_LIMIT` containing malformed rows at known row positions  
When the CSV import is performed  
Then the observable error report contains an entry for each malformed row  
And each entry identifies the corresponding CSV row  
And no report entry is required here to assert an error taxonomy or message text that the supplied contract does not define.

### AC-3 — Retry without duplicate records

Mapping: `REQ-4`, `RULE-3`; non-regression for valid records preserved by `REQ-2`

Given a CSV within `DOCUMENTED_SIZE_LIMIT` has been imported once and its valid rows have been preserved  
When the same import is retried  
Then the retry creates no additional customer record for any customer record already created by the first import.

The supplied contract does not define customer identity, duplicate matching keys, or behavior for corrected/replaced rows. Those details must be supplied before a test fixture can determine record equivalence beyond replaying the same import.

### AC-4 — File above the documented limit hard-stops

Mapping: `REQ-5`, `RULE-2`

Given the authorized value and unit of `DOCUMENTED_SIZE_LIMIT` have been supplied  
And a CSV has a measured size greater than `DOCUMENTED_SIZE_LIMIT`  
When the CSV import is attempted  
Then the import stops  
And no row from that file is imported.

`AC-4` is structurally specified but cannot be executed until `OPEN-1` supplies the numeric limit and unit. No error message, status code, or UI behavior is asserted because none was supplied.

### AC-5 — Exact size-limit boundary

Mapping: `REQ-5`, `RULE-2`

Given the authorized value and unit of `DOCUMENTED_SIZE_LIMIT` have been supplied  
And a CSV has a measured size exactly equal to `DOCUMENTED_SIZE_LIMIT`  
When the CSV import is attempted  
Then the import is not stopped for exceeding the size limit.

`AC-5` is structurally specified but cannot be executed until `OPEN-1` is resolved. Its outcome follows only from the supplied term “exceeds”; it does not claim that all other validation succeeds.

## Coverage

- Success / partial success: covered by `AC-1`, subject to the unresolved size-limit fixture.
- Error / malformed rows: covered by `AC-1` and `AC-2`.
- Boundary: structurally covered by `AC-4` and `AC-5`; not executable because `OPEN-1` is unresolved.
- Permission: not marked applicable or not-applicable because the supplied contract provides no permission evidence.
- Recovery: covered by retry behavior in `AC-3`; identity semantics remain unspecified.
- Non-regression: covered by valid-row preservation in `AC-1` and duplicate prevention in `AC-3`.
- Uncovered executable requirement: `REQ-5`, pending the documented numeric limit and unit.

## Read-only quality gate

Verdict: `needs-input`. This review does not modify or repair upstream product artifacts.

- `FINDING-1` — Severity: blocking for complete executable AC. Gate: `unknown-preservation` / `ac-testability`. Location: `OPEN-1`, `AC-4`, `AC-5`. Evidence: the case says the size-limit value is not supplied. Consequence: exact boundary fixtures cannot be executed and a complete pass cannot be issued.
- `FINDING-2` — Severity: non-blocking for symbolic retry coverage, blocking for broader identity cases. Gate: `ac-testability`. Location: `AC-3`. Evidence: duplicate prevention is required, but customer identity and duplicate matching rules are absent. Consequence: replay of the same import is testable only if record equivalence is observable; corrected-row and cross-file duplicate cases remain undefined.

Gate results:

- Artifact availability: passed for the supplied case and four frozen slot contracts.
- End-to-end traceability: passed; facts, requirements, rules, and AC mappings retain source links.
- Critical-rule retention: passed; malformed-row rejection, valid-row preservation, row-level reporting, non-duplicating retry, and oversized-file hard stop are retained.
- Scope and authority: passed; no numeric limit, UI, error text, identity key, or implementation detail is invented.
- Unknown preservation: needs-input due to `OPEN-1`.
- AC testability: needs-input for exact size boundary; available behavioral clauses remain externally observable.
- Applicable-path coverage: needs-input overall; partial success, malformed-row error, reporting, retry recovery, hard stop, and non-regression are represented, but boundary execution awaits `OPEN-1`.
- Evidence-backed verdict: passed; the `needs-input` result follows from explicit missing evidence.
- Read-only review: passed; no candidate skill, source skill, product artifact, or upstream requirements artifact was modified.

Required input: the authorized numeric value and unit of the documented CSV file size limit. After that input is supplied, substitute it into boundary fixtures and rerun the read-only gate; do not infer it from examples or conventions.
