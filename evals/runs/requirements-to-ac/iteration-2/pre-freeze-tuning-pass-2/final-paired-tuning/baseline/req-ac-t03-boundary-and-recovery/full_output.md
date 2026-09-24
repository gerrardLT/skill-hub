# Product Requirements & Acceptance Criteria: Customer CSV Import

## Document Overview
This document specifies the engineering-ready user stories, acceptance criteria, constraints, and edge cases for the **Customer CSV Import** capability. It defines fault-tolerant ingestion behavior, including early size enforcement, malformed row isolation, valid record persistence, row-level error reporting, and duplicate-safe retry processing.

---

### Inline Gap Tagging Key
* 🔶 **Assumption**: Inferred baseline rule or industry standard behavior requiring engineering/product confirmation.
* 🔵 **Open Question**: Unknown dependency or parameter not supplied in source requirements that requires stakeholder/architecture definition.

---

## 1. Epic Overview & Hypothesis

### Epic Hypothesis
> We believe that providing an asynchronous, fault-tolerant CSV import engine for customer records will allow operations and administrative users to bulk-onboard customer records efficiently without data corruption. We will know we have succeeded when:
> 1. Valid customer records within mixed-validity files are 100% preserved without requiring total rollback.
> 2. Files exceeding the documented size limit are halted before resource saturation.
> 3. Users can resolve row-level issues and re-import data without introducing duplicate customer records.

---

## 2. User Stories & Acceptance Criteria

---

### Story 1: File Size Validation & Early Termination

**User Story:**  
*As a* System Administrator,  
*I want* the import process to immediately stop and reject any file exceeding the documented size limit,  
*So that* system memory, network bandwidth, and background processing workers are protected from resource exhaustion.

#### Acceptance Criteria (Checklist Format)
- [ ] **AC 1.1 — Pre-Processing Validation:** The system must validate file size immediately upon upload (via HTTP header/content-length inspection and initial stream reading) prior to parsing CSV rows or writing to the database.
- [ ] **AC 1.2 — Enforcement of Size Limit:** If the uploaded file size strictly exceeds the documented size limit `[Documented File Size Limit]`, the system must terminate processing immediately.
  - 🔵 **Open Question:** What is the documented maximum file size limit (e.g., 10 MB, 25 MB, 50 MB, or 100 MB)?
  - 🔶 **Assumption:** File size validation occurs client-side (pre-upload warning) and is authoritatively enforced server-side upon initial stream inspection.
- [ ] **AC 1.3 — Clean Rejection:** When stopped due to size violation:
  - No customer records from the file shall be staged, committed, or persisted to the database.
  - Any temporary staging files or byte streams must be purged immediately.
- [ ] **AC 1.4 — Clear Error Feedback:** The system must return an explicit, human-readable error message: `"File size ([Actual Size]) exceeds the maximum documented limit of [Documented File Size Limit]. The import was stopped."`

#### Acceptance Criteria (Gherkin Scenarios)

```gherkin
Scenario: File size strictly exceeds documented limit
  Given the documented file size limit is "[Documented File Size Limit]"
  When a user uploads a customer CSV file with a size greater than "[Documented File Size Limit]"
  Then the system must halt ingestion immediately prior to parsing customer records
  And no customer records shall be saved to the database
  And the system shall display an error stating that the file exceeds "[Documented File Size Limit]"
  And all temporary upload storage associated with the file must be purged

Scenario: File size is within documented limit
  Given the documented file size limit is "[Documented File Size Limit]"
  When a user uploads a customer CSV file with a size less than or equal to "[Documented File Size Limit]"
  Then the system shall accept the file and proceed to schema and row validation
```

---

### Story 2: Malformed Row Rejection with Valid Row Preservation (Partial Import)

**User Story:**  
*As a* Customer Data Operations Specialist,  
*I want* the system to reject individual malformed rows while preserving and persisting all valid rows in the batch,  
*So that* bad data does not block valid customer records from being imported.

#### Acceptance Criteria (Checklist Format)
- [ ] **AC 2.1 — Schema & Syntax Validation:** The system must evaluate each row against documented syntax and schema rules. A row must be classified as **malformed** if:
  - It contains fewer or more columns than defined in the CSV header.
  - It contains unclosed quotes, invalid delimiters, or corrupted byte encoding (non-UTF-8).
  - It lacks mandatory fields (e.g., Customer Name, Email/Identifier).
    - 🔶 **Assumption:** Mandatory customer fields are `first_name`, `last_name`, and `email`.
  - Field values violate data types or structural formats (e.g., invalid email syntax, non-numeric phone values where numbers are expected, malformed dates).
- [ ] **AC 2.2 — Fault-Tolerant Partial Import (Preservation of Valid Rows):**
  - If a file contains a mix of valid rows and malformed rows, all valid rows must be parsed, imported, and committed to the customer database.
  - Malformed rows must be isolated and skipped without aborting the entire batch.
  - Failure of row $N$ must not invalidate or roll back valid row $N-1$ or valid row $N+1$.
- [ ] **AC 2.3 — Isolation of Malformed Data:**
  - Malformed rows must not be inserted into the production customer table.
  - Malformed rows must be captured in an in-memory or staging error buffer for reporting.
- [ ] **AC 2.4 — Transaction Integrity:**
  - Database persistence for valid rows must be executed using chunked/batched commits or row-level transactions so that a database failure on a malformed record does not leave valid records in an indeterminate state.

#### Acceptance Criteria (Gherkin Scenarios)

```gherkin
Scenario: CSV file contains both valid and malformed rows
  Given a customer CSV file containing 100 total rows within the documented size limit
  And 85 rows meet all customer schema and format requirements
  And 15 rows are malformed (e.g., invalid email format, column count mismatch)
  When the user executes the import
  Then exactly 85 valid customer records must be committed to the customer database
  And the 15 malformed rows must be rejected from the customer database
  And the import status must complete with a status of "Completed with Errors"

Scenario: CSV file contains 100% valid rows
  Given a customer CSV file where all rows conform to schema and format requirements
  When the user executes the import
  Then all rows must be committed to the customer database
  And the import status must complete with "Success"
  And the error report must indicate 0 errors

Scenario: CSV file contains 100% malformed rows
  Given a customer CSV file where every data row violates schema or data validation
  When the user executes the import
  Then zero records must be committed to the customer database
  And the import status must complete with "Failed - All Rows Rejected"
  And all rows must be itemized in the row-level error report
```

---

### Story 3: Row-Level Error Reporting

**User Story:**  
*As a* Customer Data Operations Specialist,  
*I want* a clear, row-level error report detailing every rejected record and the exact reason for failure,  
*So that* I can correct invalid data quickly without guessing which rows failed.

#### Acceptance Criteria (Checklist Format)
- [ ] **AC 3.1 — High-Level Batch Summary:** Upon completion of an import containing errors, the system must display an executive summary including:
  - Total rows processed (excluding header).
  - Total records successfully imported/preserved.
  - Total records rejected.
  - Timestamp of import completion.
- [ ] **AC 3.2 — Row-Level Error Itemization:** The error report must specify for every rejected row:
  - **Source Row Number:** The exact 1-based line number from the uploaded CSV file (accounting for header at line 1).
  - **Record Identifier:** The primary identifier present in the row (e.g., `Customer ID` or `Email`), or `[Missing Identifier]` if empty.
  - **Field Name:** The specific column/attribute that caused the rejection (e.g., `email`, `postal_code`, `column_count`).
  - **Rejection Reason:** A human-readable diagnostic message (e.g., `"Column count mismatch: expected 8 columns, found 6"`, `"Invalid email format: 'john.doe-at-example.com'"`).
  - **Raw Row Content Snippet:** The raw row string or field values as submitted for auditability.
- [ ] **AC 3.3 — Exportable Error Artifact:**
  - Users must have an option to download the error report as a CSV file (`import_errors_[timestamp].csv`).
  - 🔶 **Assumption:** The downloadable error report contains the original rejected data columns plus two appended columns: `_error_row_number` and `_rejection_reason`.

#### Acceptance Criteria (Gherkin Scenarios)

```gherkin
Scenario: Viewing and downloading row-level error report
  Given an import has completed with 3 rejected rows at lines 4, 12, and 27
  When the user reviews the import results
  Then the system displays an error summary showing 3 failed rows
  And a row-level table displays:
    | Row Number | Identifier          | Error Field | Error Message                                |
    | 4          | cust_104@test.com   | birth_date  | Invalid date format. Expected YYYY-MM-DD     |
    | 12         | [Missing]           | email       | Mandatory field 'email' is blank             |
    | 27         | cust_127@test.com   | N/A         | Column count mismatch: expected 8, found 10  |
  And the user can download a CSV containing these rows with their corresponding error reasons
```

---

### Story 4: Duplicate-Safe Retry & Idempotent Ingestion

**User Story:**  
*As a* Customer Data Operations Specialist,  
*I want* to fix errors and re-upload the file (or a subset of corrected rows) without creating duplicate customer records,  
*So that* I can safely achieve 100% data completion while maintaining database integrity.

#### Acceptance Criteria (Checklist Format)
- [ ] **AC 4.1 — Unique Record Identification:** Ingestion deduplication must be evaluated against a designated natural/unique business key:
  - 🔵 **Open Question:** What is the authoritative unique business key for a customer record (e.g., `email`, `customer_id`, or `external_system_id`)?
  - 🔶 **Assumption:** `email` acts as the unique customer identifier for deduplication if `customer_id` is not supplied.
- [ ] **AC 4.2 — Re-Importing Previously Imported Rows (Idempotency):**
  - If a user fixes the rejected rows and re-uploads the **entire** original CSV (containing both previously imported rows and newly fixed rows):
    - Records matching an existing unique identifier must **not** create duplicate customer records.
    - 🔵 **Open Question:** For records that already exist in the database, should the retry operation **skip** them (no-op) or **upsert/update** them with the incoming row's values?
    - 🔶 **Assumption:** The system default is an **Upsert / Update-if-changed** or **Idempotent Skip** where no duplicate record is created.
- [ ] **AC 4.3 — Corrected Rows Insertion:**
  - Rows that were previously rejected, once corrected to comply with schema and format rules, must be successfully imported into the customer database.
- [ ] **AC 4.4 — Intra-File Deduplication:**
  - If the uploaded file itself contains duplicate occurrences of the same unique customer identifier within the same file:
    - The first occurrence is imported as valid.
    - Subsequent occurrences within the same file must be flagged in the error report as `"Duplicate entry within uploaded file for identifier: [Key]"` to prevent race-condition duplicates.

#### Acceptance Criteria (Gherkin Scenarios)

```gherkin
Scenario: Full file re-import after correcting malformed rows
  Given a previous import run successfully imported 80 customer records and rejected 20 rows
  And the user corrects the 20 malformed rows in the original file
  When the user re-uploads the complete 100-row file
  Then the 20 previously rejected records must be newly created in the database
  And the 80 previously imported records must not produce duplicate entries
  And the total count of customer records in the database for this dataset must equal exactly 100
  And the import report shows 20 new records imported, 80 records deduplicated/updated, and 0 errors

Scenario: Partial retry file containing only corrected rows
  Given a user downloads the error report containing 20 rejected rows
  When the user corrects all 20 rows and uploads only the 20-row file
  Then all 20 records must be successfully imported
  And no duplicate records or errors are created in the customer database
```

---

## 3. Technical Constraints & Boundary Edge Cases

### Technical Constraints
1. **Memory Bounds:** CSV processing must stream rows sequentially or in micro-batches (e.g., 500 rows per chunk) rather than loading the entire file into application heap memory.
2. **Character Encoding:** Files must be decoded using UTF-8 (handling BOM gracefully). Unreadable byte sequences must mark the affected row as malformed.
3. **Delimiter Standards:** Default delimiter is comma (`,`), text qualified with standard double quotes (`"`). Embedded delimiters within quotes must be handled without splitting.

### Edge Cases
| ID | Edge Case Description | Expected System Behavior |
|---|---|---|
| **EC-01** | File size is exactly equal to `[Documented File Size Limit]`. | **Accept:** Process file normally; boundary threshold is inclusive ($Size \le Limit$). |
| **EC-02** | File size is 1 byte over `[Documented File Size Limit]`. | **Reject:** Immediate termination; do not process. |
| **EC-03** | 0-byte file (empty file) uploaded. | **Reject:** Stop processing immediately with error `"Uploaded file is empty"`. |
| **EC-04** | File contains only header row, no data rows. | **Complete with warning:** Zero records processed, no errors, system notifies user that no records were found. |
| **EC-05** | Malformed header (missing mandatory column headers). | **Reject entire file:** If header row cannot be mapped, no data rows can be reliably validated; abort batch before database writes. |
| **EC-06** | Row contains multi-line text (e.g., address with newline enclosed in valid quotes). | **Accept:** CSV parser must support multi-line quoted fields without counting newlines as distinct rows. |
| **EC-07** | Trailing whitespace or blank lines at end of CSV. | **Handle Gracefully:** Ignore empty trailing lines without flagging them as malformed rows. |

---

## 4. Open Questions & Assumptions Log

### Open Questions (Preserved Unknowns)
| # | Question | Impacted Requirement | Owner | Resolution Target | Status |
|---|---|---|---|---|---|
| 1 | **What is the exact documented file size limit (in MB)?** *(Value was not supplied in prompt)* | Story 1 (AC 1.1, AC 1.2, EC-01, EC-02) | Infrastructure / Lead Architect | Pre-Sprint Technical Refinement | 🔵 **Open Question** |
| 2 | **What is the primary business key for customer uniqueness (e.g., `email`, `customer_id`, or `external_uuid`)?** | Story 4 (AC 4.1, AC 4.2) | Product Manager / Data Architect | Pre-Sprint Technical Refinement | 🔵 **Open Question** |
| 3 | **What is the desired retry collision policy for existing records: Skip (no-op) or Upsert (overwrite existing fields)?** | Story 4 (AC 4.2) | Product Manager | Sprint Planning | 🔵 **Open Question** |

### Tagged Assumptions
| # | Assumption Description | Impacted Story | Risk if Invalidated |
|---|---|---|---|
| 1 | **Mandatory fields:** Assumed mandatory customer fields are `first_name`, `last_name`, and `email`. | Story 2 (AC 2.1) | Additional or fewer required fields change schema validation logic. |
| 2 | **Downloadable error format:** Assumed error report export is a CSV with original row data plus appended error columns. | Story 3 (AC 3.3) | UI/UX team may require a standalone JSON or separate audit dashboard. |
| 3 | **Streaming architecture:** Assumed server-side ingestion streams rows in batches to satisfy memory limits regardless of file size. | Technical Constraints | Large files within size limit could cause out-of-memory errors if loaded at once. |

Status: passed
