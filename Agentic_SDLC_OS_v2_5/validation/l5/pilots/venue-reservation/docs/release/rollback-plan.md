# Rollback Plan

## Objective

Return the controlled pilot to a clean pre-deployment state within five minutes.

## Facts and evidence

The release creates one local Uvicorn process and one isolated SQLite database. No external schema, queue, secret or customer data is modified.

## Decision and specification

Rollback steps: stop the recorded process, verify port 8080 is closed, archive logs if needed, delete the temporary database, restore the prior source archive if source changed, then rerun baseline validation.

## Risks and edge cases

A process may survive if its PID is not captured; verification checks the health endpoint and local process list. Deleting a database is allowed only because the environment contains generated pilot data.

## Verification and acceptance criteria

Rollback passes when /health is unreachable, the temporary database is removed and the source test baseline remains green.

## Traceability and ownership

Owner: Release OS. Input: RLP-001. Downstream: DEP-001 and PV-001.
