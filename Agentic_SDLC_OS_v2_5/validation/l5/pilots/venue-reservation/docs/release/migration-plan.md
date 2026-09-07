# Migration Plan

## Objective

Define schema creation and compatibility for the isolated pilot database.

## Facts and evidence

The application creates tables and indexes with idempotent CREATE IF NOT EXISTS statements. The pilot starts with an empty database and contains no customer data.

## Decision and specification

Migration strategy is create-on-start for version 0.1.0. A future non-empty upgrade must replace this with explicit versioned migrations and backup verification.

## Risks and edge cases

Automatic create-on-start is unsafe for complex production schema changes. The current plan is valid only for an empty disposable database.

## Verification and acceptance criteria

Pass requires successful schema initialization, foreign keys enabled, WAL mode, unique indexes present and no destructive changes.

## Traceability and ownership

Owner: Release OS. Inputs: TD-001 and ADR-001. Downstream: DEP-001.
