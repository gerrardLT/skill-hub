Status: needs-input

# CSV Customer Import Acceptance Contract

## Known Requirement

The CSV import must process valid customer rows while rejecting malformed rows, provide a row-level error report, allow corrected rows to be retried without creating duplicate customer records, and reject the entire file when it exceeds the documented file-size limit.

The acceptance contract is not ready for final approval because the documented file-size limit value was not supplied. The criteria below preserve that value as an explicit placeholder rather than inventing a number.

## Acceptance Criteria

### 1. File Within the Documented Size Limit

Given a CSV file whose size is less than or equal to the documented file-size limit,
when the user starts an import,
then the system evaluates the rows for import.

### 2. Hard Stop Above the Size Limit

Given a CSV file whose size exceeds the documented file-size limit,
when the user attempts to import it,
then the system rejects the file before importing any customer rows,
and reports that the file exceeds the documented limit,
and reports the applicable limit once that value is confirmed,
and creates no customer records from that import attempt.

### 3. Valid Rows

Given an accepted-size CSV containing well-formed customer rows,
when the import is processed,
then each valid row is imported as a customer record unless it matches a record already created by the same logical import or a retry of it,
and the import result reports the number of valid rows imported.

### 4. Malformed Rows and Partial Success

Given an accepted-size CSV containing both valid and malformed rows,
when the import is processed,
then malformed rows are rejected,
and valid rows are preserved and imported,
and one malformed row does not cause otherwise valid rows to be discarded,
and the result distinguishes imported rows from rejected rows.

### 5. Row-Level Error Report

Given one or more rejected rows,
when processing completes,
then the user can access an error report containing one entry for every rejected row,
and each entry identifies the source row unambiguously,
and each entry states the validation error that caused rejection,
and no rejected row is reported as imported.

### 6. Retry Without Duplicates

Given a prior import that created records from valid rows and rejected malformed rows,
when the user corrects the rejected rows and retries the import,
then records already created by the prior attempt are not created again,
and newly valid corrected rows can be imported,
and the retry result distinguishes records skipped as already imported from records newly created and rows still rejected.

Given the same file or same logical import is retried without corrections,
when the retry completes,
then the retry creates no duplicate customer records.

### 7. Recovery After an Oversized File Is Rejected

Given a file was rejected for exceeding the documented size limit,
when the user supplies a different file whose size is within the limit,
then the new file can proceed to row validation,
and no state or customer records from the rejected oversized attempt affect the new attempt.

## Constraint and Open Question

- Constraint: The size check is a hard, whole-file stop; partial row processing must not begin for an oversized file.
- Open question: What is the documented file-size limit, including its unit and whether the boundary is inclusive?
- Owner: Unknown; the product or platform owner responsible for the documented import constraint must resolve it.
- Decision required before final approval: Supply and approve the documented limit so the boundary examples and user-facing error can be made concrete and tested.

## Approval Boundary

All row-processing, partial-success, reporting, idempotent-retry, and recovery behaviors above are specified from supplied facts. Final acceptance remains needs-input until the documented file-size limit is provided; no numeric limit or successful end-to-end import at an unresolved boundary is asserted.
