---
name: requirements-rules
description: Convert an already framed problem and supplied constraints into traceable numbered requirements, rules, dependencies, scope, and open items. Use before acceptance criteria when product intent must be normalized without designing tests.
---

# Requirements Rules

## Responsibility

Translate an existing problem frame and supplied constraints into numbered `requirement`, `rule`, `dependency`, `scope`, and `open-item` records. Preserve conflicts and authority.

## Inputs

Require a problem frame plus supplied constraints, decisions, policies, dependencies, and authority metadata. Do not silently repair an unready frame.

## Procedure

1. Verify each input claim retains its evidence and uncertainty status.
2. Normalize statements into stable IDs: `REQ-n`, `RULE-n`, `DEP-n`, `SCOPE-n`, and `OPEN-n`.
3. For each record include statement, source links, authority, rationale when supplied, and relationships.
4. Keep conflicting records side by side and identify the decision authority needed.
5. Distinguish included scope, excluded scope, dependencies, and sequencing or hard gates.
6. When a validated brief supplies the actor, trigger, behavior class, and observable direction, retain runtime predicates such as permitted/not permitted, available/unavailable, and recoverable/restored as parameterized conditions. Do not manufacture an open policy decision solely because role matrices, failure enumerations, UI details, or implementation values are absent.
7. Preserve an open item when the input explicitly identifies a value or decision as unknown, or when resolving it one way rather than another would change the required outcome, scope, authority, or safety boundary.
8. Return `needs-input` when a missing rule, authority decision, dependency, or scope decision can be explicitly requested, whether or not it is critical to downstream readiness.
9. Return `blocked` only when normalization cannot safely begin or continue because a required artifact or authority is unavailable, or an authority conflict is irreconcilable without an obtainable decision.

## Output

Return status and numbered records with complete traceability. Preserve rejected decisions and fallback or non-regression rules when supplied.

## Boundaries

Do not write acceptance criteria, Given/When/Then scenarios, solutions, UI details, implementation plans, or invented policy. Do not let lower-authority material override a named authority.

## Fail Closed

Fail closed because dropping an unknown, conflict, or binding rule makes downstream AC falsely test the wrong contract. Use `needs-input` or `blocked` instead. Hard-fail on `fabricated-fact`, `missing-critical-rule`, `untestable-acceptance-criteria`, `unknown-loss`, `scope-or-authority-overreach`, `incorrect-gate`, or `qa-repair-overreach` when applicable.
