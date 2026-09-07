# Architecture Decision Records

## Objective

Record the irreversible or high-consequence choices for pilot-0.1.0.

## Facts and evidence

ADR-001 chooses SQLite as a reproducible local transactional store. ADR-002 chooses BEGIN IMMEDIATE for serialization. ADR-003 chooses partial unique indexes for active-state invariants. ADR-004 stores complete idempotent responses. ADR-005 uses FIFO queue_seq generated inside the transaction.

## Decision and specification

These decisions optimize deterministic evidence and minimal dependencies. They are accepted only for single-node pilot execution. The API boundary and domain invariants are designed so the storage implementation can later be replaced.

## Risks and edge cases

Main tradeoff is limited horizontal write scaling. Storing response JSON increases data retention responsibility. FIFO by commit order is fair at the server boundary but not a guarantee of network arrival fairness.

## Verification and acceptance criteria

Each ADR is verified by a matching test and documented rollback. A production architecture review must supersede ADR-001 and ADR-002 before multi-node deployment.

## Traceability and ownership

Owner: Architecture reviewer. Inputs: TD-001 and RR-001. Downstream: IP-001 and SP-001.
