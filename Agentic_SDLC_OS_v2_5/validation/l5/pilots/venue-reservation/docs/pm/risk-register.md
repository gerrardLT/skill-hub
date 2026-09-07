# Risk Register

## Scope and objective

Control the non-compensable risks for pilot-0.1.0 before design, implementation and release decisions.

## Risks and failure modes

RISK-001 oversell during concurrent allocation. RISK-002 duplicate active reservation or waitlist entry. RISK-003 unfair promotion order. RISK-004 idempotency key replay with a different payload. RISK-005 cross-tenant read or write. RISK-006 SQLite assumptions copied into distributed production.

## Severity, likelihood and impact

RISK-001, RISK-002 and RISK-005 are critical impact and possible likelihood. RISK-003 and RISK-004 are high impact and possible. RISK-006 is high impact if the pilot is misclassified as production architecture.

## Mitigation and controls

Use BEGIN IMMEDIATE transactions, partial unique indexes, queue sequence uniqueness, request hashes, tenant predicates, parameterized SQL, immutable audit events, concurrency tests and explicit architecture scope labels.

## Owners, triggers and review

Engineering owns transaction integrity; QA owns adversarial verification; Release owns scope labeling. Any oversold=true, duplicate active state, non-contiguous queue, mismatched replay acceptance or tenant access fails the gate and stops release.

## Traceability, source and evidence

Sources: D26, D33 and state invariants in `source/requirements-selection.md`. Evidence: `tests/test_concurrency.py`, `tests/test_service.py`, `tests/test_api.py`, `reports/coverage.json` and `reports/performance.json`.
