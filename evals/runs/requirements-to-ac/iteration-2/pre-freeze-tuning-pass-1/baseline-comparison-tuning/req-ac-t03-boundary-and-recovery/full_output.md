# CSV Customer Import Acceptance Criteria

Status: needs-input

## Scope

Import customer records from a CSV file while preserving valid data, reporting row-level failures, preventing duplicates during retry, and enforcing the documented file-size boundary.

## Acceptance Criteria

### AC1 — Import valid rows and reject malformed rows

```gherkin
Given a CSV file is within the documented size limit
And the file contains valid customer rows and malformed customer rows
When the user imports the file
Then each valid row is imported successfully
And each malformed row is rejected
And one malformed row does not prevent other valid rows from being imported
And the import result reports the counts of imported and rejected rows
```

A row is malformed when it cannot be parsed according to the supported CSV format or fails the required customer-field validation rules. The supported encoding, delimiter, quoting rules, required columns, field formats, and treatment of blank rows must be documented before implementation or QA sign-off.

### AC2 — Produce a row-level error report

```gherkin
Given an import contains one or more rejected rows
When processing completes
Then the user can access an error report containing one entry for every rejected row
And each entry identifies the source row number
And each entry includes a specific, actionable reason for rejection
And no successfully imported row is listed as rejected
And the report does not expose customer data beyond the product's approved data-handling policy
```

Where a row has multiple validation failures, the report must either list all detected failures or consistently report the first failure; this policy must be documented and testable.

### AC3 — Retry without duplicate records

```gherkin
Given a prior import imported valid rows and rejected malformed rows
And the user corrects the rejected rows and retries the import
When the retry is processed
Then previously imported records are not created again
And newly corrected valid rows are imported exactly once
And rows that remain malformed are rejected and included in the new error report
And the result reports counts for newly imported, rejected, and skipped-as-already-imported rows
```

```gherkin
Given the same file is submitted again after a completed import
When the retry is processed
Then no customer record created by the first import is duplicated
And the outcome clearly identifies rows that were already imported
```

The product must define the idempotency key or matching rule used to recognize a previously imported record (for example, an immutable customer identifier, an import-job-plus-row identity, or another documented unique key). Email alone must not be assumed to be unique unless the product's customer identity rules explicitly guarantee it.

### AC4 — Stop at the file-size boundary

```gherkin
Given the documented maximum CSV file size is LIMIT
And a CSV file has a size less than or equal to LIMIT
When the user starts the import
Then the file is eligible for processing
```

```gherkin
Given the documented maximum CSV file size is LIMIT
And a CSV file has a size greater than LIMIT
When the user attempts the import
Then the import is rejected before any customer row is committed
And processing stops
And the user is shown the allowed limit and the submitted file size
And no partial customer records or retry state are created from that attempt
```

The comparison must use the file's byte size and a documented unit convention (for example, decimal MB or binary MiB). An exact test for `LIMIT + 1 byte` is required.

## Recovery and Atomicity Rules

- Row-level validation failures use partial success: valid rows are committed and malformed rows are rejected.
- File-level size failure uses all-or-nothing behavior: zero rows are committed.
- A retry after partial success must be idempotent for records already committed.
- If processing fails for a reason other than row validation, the import must expose a recoverable outcome and must not create duplicates when the same input is retried.
- Import summaries and error reports must refer to stable source row numbers, including a documented convention for whether the header is row 1.

## Required Decision Before Final Approval

🔵 **Open Question:** What is the documented maximum CSV file size, including its unit convention? Replace `LIMIT` with that value before these criteria can be marked ready for implementation and QA. The missing value does not justify inventing a threshold; it prevents final boundary-test approval.

## Additional Clarifications Needed

- 🔵 **Open Question:** What columns are required, and what validation rules make a customer row valid?
- 🔵 **Open Question:** What stable identity or idempotency rule prevents duplicates across retries?
- 🔵 **Open Question:** Which CSV encodings, delimiters, quote/escape rules, and header conventions are supported?
- 🔵 **Open Question:** How should an infrastructure interruption be surfaced, and may users resume the same import job or only retry it?
