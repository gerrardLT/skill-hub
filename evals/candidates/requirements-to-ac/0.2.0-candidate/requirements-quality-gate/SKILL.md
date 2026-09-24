---
name: requirements-quality-gate
description: Perform a read-only evidence-based review of problem frames, requirements, rules, and acceptance criteria. Use at requirements handoff to return passed, failed, needs-input, or blocked without repairing upstream artifacts.
---

# Requirements Quality Gate

## Responsibility

Review supplied requirements-chain artifacts without modifying them. Judge only against declared contracts and supplied evidence.

## Procedure

1. Read the artifacts and preserve their versions, IDs, source links, authority, conflicts, and unknowns.
2. Check traceability from problem frame through requirements and rules to acceptance criteria.
3. Check critical-rule retention, scope and authority, unknown preservation, AC observability, Given/When/Then structure, and applicable success, error, boundary, permission, recovery, and non-regression coverage.
4. Treat a criterion that references a supplied named rule, policy, source-of-truth field, runtime configuration, or behavior-state predicate as parameterized rather than incomplete when its trigger and externally observable outcome remain testable. A validated brief that names the actor, trigger, behavior class, and observable direction does not need an exhaustive role matrix, failure taxonomy, UI, implementation stack, threshold, or fallback value unless the source explicitly marks it unknown or different values would change the required outcome.
5. Do not expand applicable-path coverage beyond the supplied requirement classes merely because the general coverage taxonomy lists other classes.
6. Emit findings with stable IDs, severity, violated gate, artifact location, evidence, and consequence.
7. Return exactly one status:
   - `passed`: every applicable gate has affirmative evidence and no unresolved blocking finding.
   - `failed`: supplied evidence proves a gate violation.
   - `needs-input`: evidence or a decision is absent but can be explicitly requested from an identifiable source or authority, including when it is critical to downstream readiness.
   - `blocked`: review cannot safely begin or continue because a required artifact or authority is unavailable, or supplied authority is irreconcilable without an obtainable decision.

## Output

Return status, findings, evidence citations, gate results, and unresolved inputs. A passing result must cite positive evidence; absence of findings alone is insufficient.

## Boundaries

This is read-only QA. Never edit product source, upstream artifacts, requirements, rules, or AC. Never silently repair, rewrite, fill gaps, choose authority, or expand scope. Suggested remediation may describe the violated contract but must not supply missing product decisions.

## Fail Closed

Fail closed because an incorrect pass authorizes downstream work on an unproven contract. Missing evidence cannot count as success. Hard-fail on `fabricated-fact`, `missing-critical-rule`, `untestable-acceptance-criteria`, `unknown-loss`, `scope-or-authority-overreach`, `incorrect-gate`, or `qa-repair-overreach` when applicable.
