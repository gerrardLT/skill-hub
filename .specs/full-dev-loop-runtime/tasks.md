# Full Dev Loop Runtime Tasks

Status: approved-by-execution-request

| Task | Implements | Requirements | Acceptance criteria | Depends on |
|---|---|---|---|---|
| TASK-001 Extend Slot/Recipe schemas | DES-001 | REQ-003, REQ-004, REQ-006 | AC-011–AC-020, AC-026–AC-029 | none |
| TASK-002 Upgrade recursive verifier/catalog checks | DES-002 | REQ-001, REQ-005, REQ-006 | AC-003–AC-005, AC-021–AC-029 | TASK-001 |
| TASK-003 Add schema migration and recursion tests | DES-001, DES-002 | REQ-006 | AC-026–AC-029 | TASK-001, TASK-002 |
| TASK-004 Implement workflow state store and renderer | DES-003 | REQ-002 | AC-006–AC-010 | TASK-001 |
| TASK-005 Add state initialization/recovery/migration tests | DES-003 | REQ-002 | AC-006–AC-010 | TASK-004 |
| TASK-006 Implement released-only router | DES-004 | REQ-001 | AC-001–AC-005 | TASK-002, TASK-004 |
| TASK-007 Add adversarial routing cases | DES-004 | REQ-001 | AC-001–AC-005 | TASK-006 |
| TASK-008 Refactor stateful executor | DES-005 | REQ-002, REQ-003, REQ-005 | AC-006–AC-015, AC-021–AC-025 | TASK-002, TASK-004 |
| TASK-009 Implement artifact and workspace adapters | DES-006 | REQ-004 | AC-016–AC-020 | TASK-008 |
| TASK-010 Add failure route, retry, invalidation, and authorization tests | DES-005, DES-006 | REQ-003, REQ-004 | AC-011–AC-020 | TASK-008, TASK-009 |
| TASK-011 Freeze stage matrix and minimum Slot closure | DES-007 | REQ-005, REQ-007 | AC-021–AC-025, AC-030 | TASK-002 |
| TASK-012 Produce evaluation/review evidence and release selected Slots | DES-007, DES-009 | REQ-007 | AC-030 | TASK-011 |
| TASK-013 Create six stage Recipes | DES-008 | REQ-005, REQ-007 | AC-021–AC-032 | TASK-012 |
| TASK-014 Create full-dev-loop composition | DES-008 | REQ-005 | AC-021–AC-025 | TASK-013 |
| TASK-015 Run stage and full composition evidence | DES-008, DES-009 | REQ-007 | AC-031–AC-032 | TASK-013, TASK-014 |
| TASK-016 Update dev-loop docs and runtime integration | DES-004, DES-005, DES-008 | REQ-001–REQ-005 | AC-001–AC-025 | TASK-015 |
| TASK-017 Add unified Gates, CI, and dynamic status rendering | DES-010 | REQ-008 | AC-033–AC-035 | TASK-016 |
| TASK-018 Run final regression, source baseline, sync, and audit | DES-010 | REQ-008 | AC-033–AC-035 | TASK-017 |
