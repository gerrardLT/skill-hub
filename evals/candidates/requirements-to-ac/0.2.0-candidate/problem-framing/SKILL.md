---
name: problem-framing
description: Classify supplied product facts, evidence, target users, problems, impacts, and gaps before requirements or solution work. Use whenever raw discovery or PRD context needs a traceable, solution-free problem frame.
---

# Problem Framing

## Responsibility

Turn supplied material into a solution-free problem frame. Classify every material statement as `fact`, `assumption`, `open-question`, or `conflict`.

## Inputs

Read only user-supplied context and authorized local artifacts. Preserve source labels, quoted evidence, stated authority, and uncertainty.

## Procedure

1. Inventory supplied statements without completing missing content.
2. Identify target users, observed problem, user or business impact, evidence, and gaps.
3. Classify each item:
   - `fact`: directly supported by a cited supplied source.
   - `assumption`: plausible inference or incompletely supported claim.
   - `open-question`: unknown requiring evidence or an authorized decision.
   - `conflict`: incompatible claims, evidence, scope, or authority; retain every side.
4. Link each classification to its supplied evidence or state that none was supplied.
5. Do not create an `open-question` merely because a concise validated brief does not enumerate runtime states, implementation values, or every member of a behavior class. When the actor, trigger, behavior class, and observable direction are supplied, predicates such as permitted/not permitted, available/unavailable, and recoverable/restored may remain parameterized states rather than missing product decisions.
6. Preserve an unknown when the input explicitly identifies it as unknown, or when the missing decision would change the required observable outcome, scope, authority, or safety boundary.
7. Return `needs-input` when missing evidence or a decision can be requested from an identifiable source or authority, including when the missing item is important.
8. Return `blocked` only when framing cannot safely begin or continue because a required artifact or authority is unavailable, or supplied claims are irreconcilable without an obtainable authority decision.

## Output

Return status, numbered classified items, target-user framing, problem and impact framing, evidence links, conflicts, and critical gaps. Keep unknowns inline where they matter.

## Boundaries

Do not propose, compare, imply, or recommend solutions. Do not convert examples, estimates, team consensus, or proto-personas into facts. Do not resolve conflicts without authority.

## Fail Closed

Fail closed because an invented premise propagates into requirements and test criteria as false certainty. Stop or mark `needs-input`/`blocked` rather than hiding unknowns. Hard-fail on `fabricated-fact`, `missing-critical-rule`, `untestable-acceptance-criteria`, `unknown-loss`, `scope-or-authority-overreach`, `incorrect-gate`, or `qa-repair-overreach` when applicable.
