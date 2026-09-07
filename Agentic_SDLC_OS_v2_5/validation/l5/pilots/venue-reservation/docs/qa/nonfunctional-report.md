# Nonfunctional Report

## Objective

Evaluate performance, security boundary, accessibility handoff, auditability and recoverability for pilot scope.

## Facts and evidence

Performance passed with p95 107.185 ms and zero oversell. Security review permits local non-production use only. Audit events cover five material event types. Accessibility review confirms semantic prototype structure with known screen-reader test gaps.

## Decision and specification

Accept nonfunctional evidence for the controlled pilot. Do not authorize public exposure or distributed deployment.

## Risks and edge cases

Missing production controls include authentication, rate limiting, TLS, secret management, retention, backup, disaster recovery and multi-node coordination. These are release conditions for any later environment.

## Verification and acceptance criteria

Pass is limited to the local pilot environment described in DEP-001. The report is invalid if deployment topology changes.

## Traceability and ownership

Owner: QA OS. Inputs: PERF-001, SEC-REV-001 and AR-001. Downstream: RELREC-001.
