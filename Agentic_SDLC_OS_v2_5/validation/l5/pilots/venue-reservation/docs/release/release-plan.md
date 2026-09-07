# Release Plan

## Objective

Deploy the pilot to a reproducible localhost environment and capture evidence without claiming external production release.

## Facts and evidence

Preflight runs pytest, coverage and the performance probe. Build uses the current Python environment and package source. Rollout starts Uvicorn on 127.0.0.1:8080 with an isolated database. Verification calls /health and exercises a complete reserve-waitlist-cancel path.

## Decision and specification

Proceed only after QA recommendation GO for controlled scope. The deployment window is immediate and reversible because no external data or migration is used.

## Risks and edge cases

Stop conditions are failed preflight, bind beyond localhost, oversold=true, tenant test failure or missing rollback path. Public exposure is prohibited.

## Verification and acceptance criteria

Success requires health=ok, deterministic smoke path, metrics visibility and saved deployment evidence. Rollback must complete by terminating the process and deleting the temporary database.

## Traceability and ownership

Owner: Release OS. Inputs: RELREC-001 and SRC-001. Downstream: DEP-001 and PV-001.
