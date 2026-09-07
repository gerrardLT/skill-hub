# Security Plan

## Objective

Protect tenant boundaries, request integrity and auditability for the pilot API.

## Facts and evidence

Controls include required tenant header, tenant predicates on resources, parameterized SQL, Pydantic identifier validation, bounded capacity, idempotency request hashes and no secret fields in audit payloads.

## Decision and specification

Reject missing or mismatched tenant resources with 404 to avoid disclosure. Reject reused idempotency keys with different payload using 409. Limit identifier length and character set. Do not accept arbitrary database paths from API input.

## Risks and edge cases

Authentication and authorization are not implemented; the tenant header is a test boundary only. Rate limiting, encryption at rest, secret management and production logging policy are outside the pilot and mandatory before external exposure.

## Verification and acceptance criteria

Pass requires tenant isolation tests, unsafe identifier rejection, parameterized queries and documented non-production scope. Any cross-tenant access is critical.

## Traceability and ownership

Owner: Security reviewer. Inputs: RR-001 and TD-001. Downstream: SEC-REV-001 and NFR-001.
