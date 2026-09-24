# CSV Customer Record Import — Acceptance Contract

**Status:** needs-input

## Requirement

The CSV import must process valid customer-record rows while isolating malformed rows, provide an actionable row-level error report, allow corrected data to be retried without creating duplicate customer records, and reject an entire file before row processing when its size exceeds the documented limit.

## Acceptance Criteria

### Valid and malformed rows

- Given a CSV file is within the documented size limit and contains both valid and malformed rows, when the import is processed, then every valid row is preserved as an imported customer record and every malformed row is rejected.
- Given a malformed row, when processing completes, then no customer record is created or updated from that row.
- Given one or more malformed rows, when processing completes, then failures in those rows do not roll back or discard successfully processed valid rows.
- Given all rows are valid and the file is within the documented size limit, when processing completes, then all rows are imported and the error report contains no row errors.

### Row-level error report

- Given one or more rows are rejected, when processing completes, then the importer produces an error report with a separate entry for each rejected row.
- Given an error-report entry, then it identifies the source row and describes why that row was rejected sufficiently for the source data to be corrected.
- Given a file contains multiple malformed rows, when processing completes, then the report includes every rejected row and does not report successfully imported rows as failures.

### Retry and duplicate prevention

- Given valid rows from a file were imported and malformed rows were rejected, when the same file or a corrected version is retried, then records corresponding to rows already imported are not created again.
- Given a previously rejected row is corrected and retried, when that row is now valid, then it is imported once.
- Given the same corrected input is retried more than once, when each retry completes, then the resulting customer-record set contains no duplicates caused by those retries.

### File-size boundary and hard stop

- Given a file exceeds the documented file size limit, when import is requested, then the entire import is stopped before any row is processed, no customer records from that attempt are created or updated, and the user is informed that the file exceeds the documented limit.
- Given a file is exactly at the documented file size limit, when import is requested, then it is eligible for row processing under the valid/malformed-row criteria above.
- Given a file is below the documented file size limit, when import is requested, then it is eligible for row processing under the valid/malformed-row criteria above.

## Open Question / Blocking Input

- 🔵 **Open Question:** What is the documented maximum CSV file size, including its unit? The numeric value is not supplied.
- The size-boundary criteria cannot be finalized or executed with a concrete test fixture until the authoritative limit is provided. No numeric limit is assumed here.
