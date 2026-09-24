Status: passed

# Product Requirements Document (PRD): CSV Customer Record Import

## Document Information

### Authors
- Product Manager (PM Core Platform)

### Reviewers
- Engineering Lead
- Quality Assurance Lead
- Data Platform Architect

**Date:** 2026-03-30

### Change Log

| Version | Date | Author | Change Description |
|---|---|---|---|
| 0.1 | 2026-03-30 | PM Core Platform | Initial requirements draft specifying acceptance criteria for CSV import, error handling, partial persistence, retry deduplication, and file size guardrails. |

---

## Table of Contents
1. [Executive Summary](#1-executive-summary)
2. [Problem Statement](#2-problem-statement)
3. [Target Users & Personas](#3-target-users--personas)
4. [Strategic Context](#4-strategic-context)
5. [Solution Overview](#5-solution-overview)
6. [Success Metrics](#6-success-metrics)
7. [User Stories & Requirements](#7-user-stories--requirements)
8. [Out of Scope](#8-out-of-scope)
9. [Dependencies & Risks](#9-dependencies--risks)
10. [Open Questions](#10-open-questions)
11. [PRD Self-Assessment](#prd-self-assessment)

---

## 1. Executive Summary

We are building a **fault-tolerant CSV customer record import engine** for **operations specialists and CRM administrators** to solve the problem of **failed bulk uploads, lost valid data during batch failures, uninformative error reporting, duplicate records created during retries, and system instability caused by oversized files**, which will result in **100% preservation of valid customer records, zero duplicate records created upon retrying failed rows, clear row-level error diagnostics, and deterministic stoppage when file size exceeds the documented limit**.

---

## 2. Problem Statement

### Who Has This Problem?
CRM administrators, customer operations specialists, and onboarding managers responsible for migrating, uploading, and synchronizing customer datasets via CSV files.

### What Is the Problem?
When users import a CSV of customer records:
1. If a single row is malformed or invalid, naive systems fail the entire file ("all-or-nothing"), throwing away hundreds or thousands of valid customer records.
2. Error messages are generic (e.g., "Import failed on row 412" or "Invalid file format"), failing to provide row-level transparency that explains exactly what failed and how to remediate it.
3. When users attempt to fix errors and re-upload the file or a subset of rows, the system risks creating duplicate customer records for rows that were already imported in the prior run.
4. When users upload files that exceed the system capacity, processing crashes mid-stream or hangs indefinitely because the system does not enforce file size limits up front.

### Why Is It Painful?
- **User impact**: Users waste hours manually scanning large spreadsheets to find syntax or schema errors, manually deduplicating customer profiles, and waiting on failed imports.
- **Business impact**: Slow customer onboarding, degraded CRM data hygiene, duplicate billing/communications to end customers, and elevated support escalations.

### Evidence
- **Support signals**: 🔶 **Assumption**: Import failure and duplicate record remediation represent ~30% of data-onboarding support tickets.
- **User feedback**: "I had 5,000 customers in a CSV and one bad email address rejected the entire file. After fixing it and re-uploading, half my customer base was duplicated."

---

## 3. Target Users & Personas

### Primary Persona: Operations Specialist Olivia
- **Role**: Sales/Customer Operations Manager
- **Context**: Responsible for maintaining customer databases; works extensively with CSV exports from marketing tools, billing systems, and external CRMs. Non-engineer.
- **Goals**: Reliably bulk-import customer records in minutes; clearly see and fix any invalid records; re-import without corrupting the database with duplicate records.
- **Pain points**: All-or-nothing file rejections; opaque error logs; duplicate customer creation; browser freezes on large files.
- **Current behaviour**: Chunks large CSVs into 100-row batches in Excel to isolate syntax errors; manually deduplicates records after every re-import.

### Jobs-to-Be-Done
- **Functional job**: Import valid customer records into the system, receive an itemized error manifest for any malformed rows, and retry failed rows without creating duplicates.
- **Emotional job**: Feel confident that valid customer records are safe and the customer database remains clean and accurate.
- **Social job**: Be recognized by leadership and sales teams as a reliable steward of clean data.

---

## 4. Strategic Context

### Business Goals
- **Strategic alignment**: Accelerate time-to-value for new customers by streamlining data onboarding.
- **Quality & hygiene**: Eliminate duplicate customer records created by bulk data ingestion.

### Why Now?
Customer data import volume has increased significantly. Without pre-flight size limits and resilient row-level processing, unhandled file sizes and duplicate customer creation threaten core platform stability and data integrity.

---

## 5. Solution Overview

### Solution Description
We are introducing an asynchronous, resilient customer CSV import pipeline:
1. **Pre-flight & Size Validation**: Immediately validates file metadata against the documented size limit (🔵 **Open Question**: What is the exact documented file size limit threshold?). If the file exceeds the limit, processing halts immediately without parsing or writing records.
2. **Streamed Row Parsing & Validation**: Reads the file row by row. Each row is evaluated against format rules (delimiters, quoting, column counts) and customer schema rules (required fields, valid email/phone formats).
3. **Partial Persistence (Preserve Valid Rows)**: Valid rows are committed to the database. Malformed rows are isolated and rejected without aborting or rolling back the valid rows.
4. **Row-Level Error Reporting**: Generates a detailed error report displaying exact source row numbers, raw values, and specific reasons for failure.
5. **Idempotent Retry Engine**: Allows users to re-upload corrected files (or error-only files) using a unique customer record identifier (e.g., Customer ID or Email) to update or skip existing records, guaranteeing no duplicate records are created.

### Key Features
- **Deterministic File-Size Guardrail**: Fast pre-flight check halting files that exceed the documented threshold.
- **Fault-Tolerant Row Ingestion**: Preserves valid records regardless of how many malformed rows exist in the file.
- **Actionable Error Report**: Row-by-row failure log with line numbers and human-readable error descriptions.
- **Zero-Duplicate Retry**: Idempotent re-import logic that deduplicates incoming records against existing database entries.

---

## 6. Success Metrics

### Primary Metric
- **Valid Row Import Rate**: 100% of syntactically and semantically valid rows are preserved and committed to the database, even when malformed rows are present in the same file.

### Secondary Metrics
- **Duplicate Record Rate on Retry**: 0% duplicate records created when re-importing corrected files.
- **Error Remediation Time**: Reduction in time spent diagnosing failed rows (target: < 2 minutes to identify and remediate errors).

### Guardrail Metrics
- **System Stability**: 0 out-of-memory errors or unbounded background job worker timeouts caused by files exceeding the documented size limit.

---

## 7. User Stories & Requirements

### Epic Hypothesis
We believe that implementing a fault-tolerant CSV customer import pipeline with strict file size guardrails, partial record preservation, row-level error reporting, and idempotent retry deduplication will eliminate duplicate customer records and data ingestion failures. We will measure success by 100% preservation of valid rows, zero duplicate records created on retries, and zero worker crashes from oversized files.

---

### User Stories & Acceptance Criteria

#### Story 1: Enforce Documented File Size Limit (Immediate Stoppage)
**As a** system administrator,  
**I want** the import process to stop immediately when an uploaded CSV file exceeds the documented size limit,  
**So that** server resources are protected, memory exhaustion is prevented, and users receive immediate feedback.

> 🔵 **Open Question**: What is the documented file size limit? (The exact numeric threshold—e.g., 10 MB, 25 MB, 50 MB, or 100 MB—is not supplied and must be confirmed with Engineering/Infrastructure before final release).

##### Acceptance Criteria:
- [ ] **AC 1.1 — Pre-Upload / Header Check**: The system must check the file size (via `Content-Length` or client-side file inspection) before processing row data.
- [ ] **AC 1.2 — Immediate Halt on Oversized Files**: Given an uploaded CSV file whose size exceeds the documented size limit (🔵 **Open Question**), when the upload is initiated, then the system must immediately stop processing the file.
- [ ] **AC 1.3 — Zero Database State Changes**: When a file is stopped due to exceeding the documented size limit, no records from the file shall be parsed, validated, or written to the database.
- [ ] **AC 1.4 — Clear Error Messaging**: The system must display a clear, user-facing error message stating:
  - That the upload stopped because the file exceeded the maximum allowed size limit.
  - The actual size of the uploaded file.
  - The documented size limit threshold (🔵 **Open Question**).
- [ ] **AC 1.5 — Processing Within Limit**: Given an uploaded CSV file whose size is less than or equal to the documented size limit (🔵 **Open Question**), when the upload is initiated, then the system proceeds to row validation and processing.

##### Gherkin Scenarios:
```gherkin
Scenario: File exceeds documented size limit
  Given the documented file size limit is "[Documented Size Limit - 🔵 Open Question]"
  When a user uploads a CSV file of customer records whose size exceeds "[Documented Size Limit - 🔵 Open Question]"
  Then the system immediately stops the import process
  And no customer records from the file are written to the database
  And an error message is displayed stating "File size exceeds the maximum limit of [Documented Size Limit - 🔵 Open Question]. Processing stopped."

Scenario: File is within documented size limit
  Given the documented file size limit is "[Documented Size Limit - 🔵 Open Question]"
  When a user uploads a CSV file of customer records whose size is within "[Documented Size Limit - 🔵 Open Question]"
  Then the file is accepted and proceeds to row parsing and validation
```

---

#### Story 2: Reject Malformed Rows and Preserve Valid Rows (Fault-Tolerant Partial Import)
**As an** operations specialist,  
**I want** the system to reject malformed rows while preserving and committing all valid rows from the same CSV file,  
**So that** I do not lose valid customer data or have my entire import blocked by isolated row defects.

##### Acceptance Criteria:
- [ ] **AC 2.1 — Identification of Malformed Rows**: The system must evaluate each row and classify it as malformed if it violates any of the following:
  - CSV structural errors: mismatched column counts (too few or too many delimiters/commas), unclosed quotation marks, or illegal control characters.
  - Data schema errors: missing mandatory customer fields (e.g., `First Name`, `Last Name`, `Customer ID` or `Email`), invalid email format, invalid phone number format, or incompatible data types.
- [ ] **AC 2.2 — Rejection of Malformed Rows**: Any row identified as malformed must be rejected and must NOT be saved or committed to the customer database.
- [ ] **AC 2.3 — Preservation of Valid Rows**: Any row meeting all CSV structural and schema validation rules must be classified as valid and successfully saved/committed to the customer database.
- [ ] **AC 2.4 — Non-Blocking Execution**: The presence of one or more malformed rows in a CSV file must NOT cause the entire import to fail, abort, or roll back valid rows.
- [ ] **AC 2.5 — Transactional Integrity**: All valid rows must be committed cleanly to the database upon completion of the import job, regardless of the failure of other rows.
- [ ] **AC 2.6 — Pure Failure / Pure Success Handling**:
  - If 100% of rows are valid, all rows are preserved and the import status is marked as `Completed`.
  - If 100% of rows are malformed, no rows are persisted, and the import status is marked as `Failed - All rows malformed`.
  - If a file contains a mix of valid and malformed rows, the valid rows are preserved, and the import status is marked as `Completed with Errors`.

##### Gherkin Scenarios:
```gherkin
Scenario: CSV contains a mix of valid and malformed rows
  Given a customer CSV file containing 100 rows within the documented size limit
  And 85 rows are valid customer records
  And 15 rows are malformed (e.g., missing required email, column count mismatch)
  When the user imports the CSV file
  Then the 85 valid rows are preserved and saved into the customer database
  And the 15 malformed rows are rejected from the customer database
  And the import job completes with status "Completed with Errors"

Scenario: CSV contains only malformed rows
  Given a customer CSV file where all rows have unclosed quotation marks or missing required fields
  When the user imports the CSV file
  Then 0 records are written to the customer database
  And the import job completes with status "Failed - All rows malformed"
```

---

#### Story 3: Generate and Display Row-Level Error Report
**As an** operations specialist,  
**I want** to see a detailed, row-level error report after the import completes,  
**So that** I know exactly which rows were rejected, which line numbers they were on, and why they failed.

##### Acceptance Criteria:
- [ ] **AC 3.1 — Report Availability**: Upon completion of any import that contains one or more malformed rows, a row-level error report must be generated and presented in the UI, with an option to download it as a CSV.
- [ ] **AC 3.2 — Mandatory Error Report Fields**: For every rejected row, the report must include:
  1. `Row Number`: The exact 1-based physical line number from the original CSV file (e.g., `Row 14`).
  2. `Record Identifier`: The customer identifier or email from the row if parseable (or `[Unparseable]` if the row is structurally broken).
  3. `Field / Attribute`: The specific column or field that failed validation (e.g., `Email`, `Column Count`).
  4. `Error Reason`: A descriptive, human-readable error explanation (e.g., `"Column count mismatch: expected 6 columns, found 4"`, `"Missing required field: Email"`, `"Invalid email syntax: 'jane.doe@'"`).
  5. `Raw Row Content`: A snippet or full string of the raw rejected row to allow quick copy/correction.
- [ ] **AC 3.3 — Import Summary Header**: The top of the error report must display an aggregate summary:
  - Total rows processed in file.
  - Total valid rows successfully imported.
  - Total malformed rows rejected.
- [ ] **AC 3.4 — No Errors Case**: When an import contains zero malformed rows, no error report is generated, and a success confirmation displays the total count of imported records.

##### Gherkin Scenarios:
```gherkin
Scenario: User views row-level error report after partial import
  Given a CSV file with 10 rows was imported
  And Row 4 failed due to "Missing required field: Email"
  And Row 8 failed due to "Column count mismatch: expected 6 columns, found 5"
  When the import process finishes
  Then the user is shown an error report containing:
    | Row Number | Record Identifier | Field        | Error Reason                                           |
    | Row 4      | CUST-104          | Email        | Missing required field: Email                          |
    | Row 8      | [Unparseable]     | Column Count | Column count mismatch: expected 6 columns, found 5     |
  And the summary displays "8 rows successfully imported, 2 rows rejected"
  And a "Download Error Report (CSV)" button is available
```

---

#### Story 4: Support Retry Without Duplicate Records (Idempotent Deduplication)
**As an** operations specialist,  
**I want** to retry importing my customer records after fixing errors without creating duplicate records in the database,  
**So that** my customer database remains clean, unified, and free of duplicate accounts.

##### Acceptance Criteria:
- [ ] **AC 4.1 — Flexible Retry Input**: The user must be able to retry using either:
  - Option A: An updated version of the entire original CSV file (with malformed rows corrected).
  - Option B: A remediation CSV containing only the corrected rows that previously failed.
- [ ] **AC 4.2 — Unique Record Key Matching**: The system must evaluate each incoming record against existing customer records in the database using a unique natural/business key (e.g., `Customer ID` or normalized `Email`).
- [ ] **AC 4.3 — Zero Duplicate Records Created**:
  - If an incoming row matches a customer record that was already successfully imported during the initial run, the system must NOT insert a duplicate customer record.
  - The system must either skip the existing record or update it based on the deduplication policy (🔵 **Open Question**: Confirm whether retry defaults to "Skip existing" or "Update/Upsert existing fields").
- [ ] **AC 4.4 — Ingestion of Newly Corrected Rows**: Rows that were previously rejected and are now corrected must be successfully parsed, validated, and persisted as valid customer records.
- [ ] **AC 4.5 — Retry Execution Summary**: Following a retry import, the system must display:
  - Count of newly imported records (previously failed, now valid).
  - Count of skipped/unmodified records (already existed from previous run).
  - Count of remaining rejected records (if any errors persist).
- [ ] **AC 4.6 — Database-Level Uniqueness Enforcement**: The database schema must enforce unique constraints on the customer unique identifier to guarantee zero duplicate records even under concurrent retry attempts.

##### Gherkin Scenarios:
```gherkin
Scenario: Re-importing a corrected full file does not create duplicate records
  Given 80 customer records were previously imported successfully from "customers_batch1.csv"
  And 20 customer records failed on the initial run
  When the user corrects the 20 malformed rows in "customers_batch1.csv" and re-uploads the entire file of 100 rows
  Then the 20 newly corrected customer records are inserted into the database
  And 0 duplicate records are created for the 80 previously imported customers
  And the retry summary reports: "20 new records imported, 80 existing records skipped/preserved, 0 errors"

Scenario: Re-importing an error-only remediation file
  Given 20 rows failed during the initial import
  When the user uploads an error-fix CSV containing only the 20 corrected rows
  Then the 20 records are validated and inserted into the customer database
  And the total customer count in the database increases by exactly 20
```

---

### Constraints & Edge Cases

#### Technical Constraints
- **Encoding**: Must support UTF-8 and UTF-8 with BOM (Byte Order Mark) encoded CSV files.
- **Delimiter**: Standard comma (`,`) delimited; fields containing commas or quotes must be properly escaped in accordance with RFC 4180.
- **Idempotency**: All row persistence operations must be idempotent based on the customer unique key.
- **File Size**: Must enforce the documented file size limit before/during ingestion (🔵 **Open Question**).

#### Edge Cases
1. **Empty File (0 bytes)**:
   - System rejects the file with message: `"Uploaded file is empty. Please select a valid CSV file."` No records created.
2. **Header-Only CSV**:
   - System parses headers, finds 0 data rows, and returns message: `"File contains headers but no customer data rows."` No records created.
3. **File with No Header Row**:
   - System detects missing header mappings and rejects file before data insertion with message: `"Invalid CSV format: Missing required header row."`
4. **Duplicate Rows Within the Same Upload File**:
   - If the same customer ID/email appears multiple times within the *same* upload file, the first valid occurrence is imported; subsequent occurrences within the same file are flagged in the error report as `"Duplicate entry within file: Customer identifier already processed in row X"` and skipped to prevent intra-file duplication.
5. **Network Disruption Mid-Upload**:
   - If the connection drops during file upload or streaming, the transaction/batch must roll back uncommitted rows, or the retry must cleanly handle partially committed chunks idempotently.

---

## 8. Out of Scope

- **Non-CSV File Formats**: Ingestion of Excel (`.xlsx`, `.xls`), JSON, TSV, or XML files is excluded from this release.
- **Automated AI Data Cleansing**: Automatic guessing or inferring of missing email addresses or phone numbers.
- **Custom Schema Mapping UI**: Dynamic visual column-mapping interface (this release requires CSV headers to match documented customer attributes).
- **Automated SFTP / Cloud Storage Sync**: Scheduled automated polling of external folders.

---

## 9. Dependencies & Risks

### Dependencies
- **Storage / Upload Service**: Infrastructure support for streaming uploads and checking file size metadata.
- **Background Worker Queue**: Worker pipeline (e.g., Celery/BullMQ) to process large files asynchronously without blocking HTTP threads.
- **Database Unique Indexes**: Customer table must have unique index on customer identifier (e.g., `email` or `customer_id`) to ensure database-level deduplication integrity.

### Risks & Mitigations

| Risk | Severity | Mitigation Strategy |
|---|---|---|
| **Oversized files bypass client checks and crash workers** | High | Enforce size validation at two layers: 1) Gateway / HTTP Reverse Proxy header check, and 2) Server-side stream counter that immediately halts parsing if byte count exceeds the documented size limit (🔵 **Open Question**). |
| **Duplicate records created during concurrent retries** | High | Enforce a strict database unique constraint on customer identifier; acquire an upload lock per customer account while import is processing. |
| **Ambiguous size limit expectations for end users** | Medium | Clearly state the documented file size limit directly on the UI file upload dropzone before the user selects a file (once 🔵 **Open Question** is resolved). |
| **Memory spikes on large valid batches** | Medium | Use streaming CSV parser and batch database inserts (e.g., chunks of 500 rows) rather than reading the entire file into application memory. |

---

## 10. Open Questions

| # | Question | Owner | Target Resolution Deadline | Status |
|---|---|---|---|---|
| 1 | 🔵 **Open Question**: What is the exact documented file size limit for CSV imports? (e.g., 10 MB, 25 MB, 50 MB, or 100 MB?) | Infrastructure Lead / PM Core Platform | Sprint Planning (Prior to engineering handoff) | **Open** |
| 2 | 🔵 **Open Question**: On retry import, should matching existing customer records be strictly skipped without modification, or should their fields be updated (upserted) with the newly uploaded row data? | Product Manager / CRM Data Governance | Sprint Planning | **Open** |
| 3 | 🔵 **Open Question**: How long should the generated row-level error reports be retained for download (e.g., 7 days, 30 days, or indefinitely in object storage)? | Compliance & Security Lead | Sprint Backlog Grooming | **Open** |

---

## PRD Self-Assessment

### Strongest Section
- **Section 7 (User Stories & Requirements)**: Provides precise, unambiguous, testable acceptance criteria and Gherkin scenarios for all five core requirements: stopping on files exceeding the documented size limit, rejecting malformed rows, preserving valid rows, generating row-level error reports, and deduplicating retried records.

### Weakest Section
- **Section 4 (Strategic Context)**: Market sizing and precise telemetry on current import failure frequency are based on preliminary assumptions (🔶 **Assumption**) rather than deep instrumentation metrics.

### Top Assumptions & Open Questions to Validate

| # | Type | Item | Risk if Wrong | Validation Plan |
|---|---|---|---|---|
| 1 | 🔵 **Open Question** | What is the documented file size limit? | If set too high, backend workers may encounter memory pressure; if set too low, users with valid enterprise datasets will be blocked. | Review infrastructure bandwidth, memory allocation, and historical file distributions with Tech Lead to document exact limit. |
| 2 | 🔵 **Open Question** | Deduplication strategy: Skip vs. Upsert on retry. | If users expect an update but the system skips, corrected customer attributes won't persist; if users expect skip and it overwrites, data may be unintentionally clobbered. | Validate customer intent with Operations users; align on default behavior (e.g., skip existing vs. update). |
| 3 | 🔶 **Assumption** | ~30% of onboarding support tickets stem from bulk CSV errors and duplicate records. | If lower, prioritization of error reporting over other ingestion features may be slightly misaligned. | Run a two-week support ticket tagging audit on import-related tickets. |

### Recommended Next Step
Meet with the Infrastructure and Data Platform leads to answer **Open Question #1** by officially documenting the file size limit value in the platform technical specification, and confirm whether the deduplication policy defaults to "skip" or "upsert" for retry operations.

---

Status: passed
