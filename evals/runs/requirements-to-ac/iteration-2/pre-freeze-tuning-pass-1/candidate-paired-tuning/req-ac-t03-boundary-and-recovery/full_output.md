# Offline Candidate Evaluation

Case: `req-ac-t03-boundary-and-recovery`

## 1. Problem Framing

1. `fact` — The product must import a CSV containing customer records. Evidence: supplied product input. Authority: product input.
2. `fact` — Malformed rows must be rejected. Evidence: supplied product input. Authority: product input.
3. `fact` — Valid rows must be preserved when other rows are malformed. Evidence: supplied product input. Authority: product input.
4. `fact` — The import must provide a row-level error report. Evidence: supplied product input. Authority: product input.
5. `fact` — A retry must not create duplicate customer records. Evidence: supplied product input. Authority: product input.
6. `fact` — Processing must stop when the file exceeds the documented size limit. Evidence: supplied product input. Authority: product input.
7. `open-question` — What value does the documented file-size limit specify, and which document is authoritative? Evidence: the product input explicitly says the value is not supplied.
8. `open-question` — Which supplied rules determine whether a row is malformed? Evidence: no CSV syntax or customer-record validation rules are supplied.

Target user: not supplied. The framed problem is that a customer-record CSV can contain invalid rows, can be retried, or can exceed an applicable limit; the required outcomes are partial preservation, attributable errors, duplicate-free recovery, and termination at the documented boundary. User and business impacts are not supplied. There are no supplied conflicts. Critical gaps are the authoritative size-limit reference/value and malformed-row rules.

## 2. Requirements And Rules

- `SCOPE-1` — CSV import of customer records is included. Source: product input. Authority: product input.
- `REQ-1` — The import shall reject each malformed row. Source: product input. Authority: product input. Related: `REQ-2`, `REQ-3`, `OPEN-2`.
- `REQ-2` — The import shall preserve valid rows when malformed rows occur in the same file. Source: product input. Authority: product input. Related: `REQ-1`, `REQ-3`.
- `REQ-3` — The import shall produce an error report attributable at row level for rejected rows. Source: product input. Authority: product input. Related: `REQ-1`.
- `REQ-4` — Retrying an import shall not create duplicate customer records. Source: product input. Authority: product input. Related: `RULE-1`.
- `RULE-1` — Duplicate customer records are prohibited on retry. Source: product input. Authority: product input. The customer-record identity rule is not supplied.
- `REQ-5` — The import shall stop when the input file exceeds the documented size limit. Source: product input. Authority: product input. Related: `RULE-2`, `OPEN-1`.
- `RULE-2` — The applicable threshold is the documented file-size limit; no numeric value or fallback may be invented. Source: product input. Authority for the value: the referenced documentation, which is not identified in the supplied input.
- `OPEN-1` — Obtain the applicable limit value and authoritative document from the product owner or owner of the documented import limit.
- `OPEN-2` — Obtain the authoritative CSV and customer-record validation rules from the product owner or data-contract owner.
- `OPEN-3` — Obtain the authoritative customer identity or duplicate-detection rule from the product owner or customer-data owner.

No exclusions, permissions, sequencing constraints, or additional dependencies were supplied.

## 3. Acceptance Criteria

`AC-1` — Mixed valid and malformed rows (`REQ-1`, `REQ-2`, `REQ-3`)

Given a CSV containing rows that satisfy the authoritative import validation rules and rows that fail those rules  
When the CSV import is performed  
Then every failing row is rejected, every satisfying row is preserved, and the resulting error report identifies each rejected row and its error.

`AC-2` — Retry after a partial import (`REQ-2`, `REQ-4`, `RULE-1`)

Given a CSV import has preserved valid customer records and reported rejected rows  
When the same file is retried  
Then no additional customer record is created for any customer record already preserved by the first attempt, according to the authoritative customer identity rule.

`AC-3` — Recovery after correcting rejected rows (`REQ-1`, `REQ-2`, `REQ-3`, `REQ-4`)

Given an import preserved valid rows and reported malformed rows, and a retry file contains corrected versions of the rejected rows together with previously preserved rows  
When the retry file is imported  
Then the corrected rows that satisfy the authoritative validation rules are preserved, previously preserved customer records are not duplicated according to the authoritative customer identity rule, and any rows still failing validation remain identified in the row-level error report.

`AC-4` — File above the documented limit (`REQ-5`, `RULE-2`)

Given the authoritative documented file-size limit is available and a CSV file has a size greater than that limit  
When import is attempted  
Then the import stops because the file exceeds that documented limit.

`AC-5` — File at the documented limit (`REQ-5`, `RULE-2`)

Given the authoritative documented file-size limit is available and a CSV file has a size exactly equal to that limit  
When import is attempted  
Then the import is not stopped for exceeding the file-size limit.

Coverage: success and error are covered by `AC-1`; recovery and non-regression are covered by `AC-2` and `AC-3`; boundary is covered by `AC-4` and `AC-5`. Permission behavior is unresolved because no permission requirement or evidence of non-applicability was supplied. The criteria deliberately parameterize the documented size limit rather than inventing its value. Execution of `AC-1` through `AC-3` requires the missing validation and customer-identity rules.

## 4. Requirements Quality Gate

Status: needs-input

### Findings

- `F-1` — Severity: blocking. Gate: `unknown-preservation`. Location: `OPEN-1` / `AC-4` / `AC-5`. Evidence: the product input says the size-limit value is not supplied. Consequence: the boundary criteria are structurally testable against the documented authority but cannot be executed until the authoritative document and value are provided.
- `F-2` — Severity: blocking. Gate: `ac-testability`. Location: `OPEN-2` / `AC-1` / `AC-3`. Evidence: “malformed” is required but no validation contract is supplied. Consequence: QA cannot determine the complete valid and malformed row sets without an authoritative rule.
- `F-3` — Severity: blocking. Gate: `ac-testability`. Location: `OPEN-3` / `AC-2` / `AC-3`. Evidence: retry must avoid duplicate records, but no customer identity rule is supplied. Consequence: QA cannot determine when two rows represent the same customer.
- `F-4` — Severity: non-blocking. Gate: `applicable-path-coverage`. Location: coverage register. Evidence: no permission behavior or evidence supporting `not-applicable` is supplied. Consequence: permission coverage cannot be positively closed.

### Gate Results

- `artifact-availability` — Pass: all four chain artifacts were produced in sequence from the supplied input.
- `end-to-end-traceability` — Pass: facts map to stable requirement/rule IDs, and each criterion names its mappings.
- `critical-rule-retention` — Pass: malformed-row rejection, valid-row preservation, row-level errors, duplicate-free retry, and the documented size boundary are retained.
- `scope-and-authority` — Pass: no threshold, validation rule, identity rule, UI, or implementation detail is invented.
- `unknown-preservation` — Needs input: `OPEN-1` through `OPEN-3` remain explicit.
- `ac-testability` — Needs input: criteria have observable Given/When/Then outcomes, but three authoritative test parameters are unavailable.
- `applicable-path-coverage` — Needs input: required success, error, boundary, recovery, and non-regression paths are represented; permission applicability is unproven.
- `evidence-backed-verdict` — Pass: the verdict follows the explicitly missing, requestable product decisions.
- `read-only-review` — Pass: the review does not repair upstream records or select missing values.

Required input: the authoritative size-limit document and value, malformed-row validation contract, customer identity rule used for duplicate detection, and an authority decision on whether permission behavior applies.