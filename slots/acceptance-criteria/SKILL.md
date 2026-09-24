---
name: acceptance-criteria
description: Convert ready, authoritative requirements into numbered observable Given/When/Then acceptance criteria. Use when requirements are ready for QA-facing behavior coverage, including applicable failure, boundary, permission, recovery, and non-regression paths.
---

# Acceptance Criteria

## Responsibility

Translate ready requirements into independently testable, numbered Given/When/Then acceptance criteria without changing product intent.

## Readiness

Accept requirements with sufficient trigger, actor or system context, expected observable behavior, applicable rules, authority, and dependencies. A criterion may refer to a supplied named rule, policy, source-of-truth field, runtime configuration, or behavior-state predicate without inventing its value when the observable direction and authority are supplied. Return `needs-input` when the input explicitly leaves a required value or outcome-changing decision unknown and it can be requested. Return `blocked` only when criteria cannot safely be produced because a required artifact or authority is unavailable, or supplied authority is irreconcilable. Never guess.

## Procedure

1. Preserve requirement IDs and source traceability.
2. Create stable IDs `AC-n` and map every AC to one or more requirements or rules.
3. Write explicit `Given`, `When`, and `Then` clauses using externally observable outcomes.
4. Cover each applicable class: success, error, boundary, permission, recovery, and non-regression.
5. When a validated brief supplies an actor, trigger, behavior class, and observable direction, use parameterized Given conditions such as permitted/not permitted, available/unavailable, and recoverable/restored. The criterion must assert the supplied observable outcome but need not invent or request a role matrix, exhaustive failure taxonomy, UI, or implementation value.
6. When a supplied requirement intentionally delegates a value or decision to a named authority, express the criterion against that authority without selecting a UI, implementation stack, threshold, role matrix, or fallback value.
7. Preserve an unresolved input when the source explicitly says a required value is not supplied, or different resolutions would change the expected observable outcome, scope, authority, or safety boundary.
8. Mark a class `not-applicable` only with evidence from the supplied contract.
9. Report uncovered requirements, ambiguity, conflicts, and unknown prerequisites.

## Output

Return status, numbered Given/When/Then criteria, requirement mappings, coverage by applicable class, and unresolved inputs.

## Boundaries

Do not invent defaults, actors, thresholds, permissions, error behavior, recovery behavior, data, or scope. Do not alter requirements, resolve authority conflicts, prescribe implementation, or declare product quality.

## Fail Closed

Fail closed because fabricated preconditions make criteria executable-looking but invalid. Unknown prerequisites therefore produce `needs-input` or `blocked`, not guessed scenarios. Hard-fail on `fabricated-fact`, `missing-critical-rule`, `untestable-acceptance-criteria`, `unknown-loss`, `scope-or-authority-overreach`, `incorrect-gate`, or `qa-repair-overreach` when applicable.
