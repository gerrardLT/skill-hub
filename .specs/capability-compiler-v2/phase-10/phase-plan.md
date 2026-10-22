# Capability Compiler V2 — Phase 10 Plan

## Objective

Manually review the frozen candidate behavior evidence, adjudicate all six Phase 9 open findings, revise only the affected Recipe/router layer in a new immutable revision path, and rerun targeted behavioral checks without changing Phase 9 evidence or thresholds. This is parent-direct semantic review, not final user release approval.

## Frozen Inputs

- Phase 3 tree: `de60929ce7eb1877ffb64a9e8cd671beec389b433f843e10320701c890de8965`
- Phase 4 tree: `968fd1e2175bdc35d77a4d9025a88ab35e5f096fba353137dbf9770e030d4695`
- Phase 5 tree: `7b39fb29c0a25a4a97243e9a857840d14541a9f839e550970c29cc014122e1ee`
- Phase 6 tree: `7e8ff8c23ede16d189a9c89d141e2fee87df63251d5d27ec40aa40eef1d24561`
- Phase 7 tree: `c76902fd5df781db653e214268b044cb4a8cc389a4fce0a188f72a5fba829926`
- Phase 8 tree: `501d9cddfdc44fec4af8f17470c99b57b48ffced977e0fa7086cce568fa92f66`
- Phase 9 tree: `7540c53426a5dff605c3f751fdaf105f52059ffbafce213d77c9c3db94214152`
- Phase 9 production plan: 1,002 runs, hash `97b7f493a54cb6d6419479ecd6f7ffee3dfd9260818659697d35a109724f995b`.
- Phase 9 candidate Skill holdouts: 314/314 passed; no candidate Skill routing regression.
- Phase 9 release thresholds failed only in Phase 4/8 Recipe/router behavior.

## Review Scope

### Atomic Skills — 157

For every Skill:

1. review both candidate holdout requests, decisions, matched boundaries, and reasons;
2. confirm no authority widening, side-effect execution, adjacent-capability collapse, or unsupported claim;
3. record `accepted`, `revision-required`, or `blocked` with evidence paths;
4. do not revise an atomic Skill merely because a deterministic-marker mutation survived a non-causal behavioral challenge;
5. preserve all prior trigger, holdout, provenance, permission, and deterministic mutation evidence.

No blanket acceptance from aggregate accuracy alone is allowed. The review ledger must contain exactly 157 Skill records and 314 reviewed candidate outputs.

### Open Finding Adjudication — 6

1. **Phase 8 Recipe skip gate**: require approved requirements to explicitly state no user-facing surface before experience-design atomic steps may be skipped.
2. **Stage 15 missing renderer support**: distinguish readiness verification from authorized preparation. Route missing approved renderer setup to the narrow existing runtime/bootstrap capability, require its exact authorization, then return to the blocked owner. Stage 15 itself still grants no lifecycle approval.
3. **Explicit safety route targets**: encode first-class safety dispositions for blocked data governance, review/repair split, observation/rollback split, and non-cascading remote authorization. Generic intake/readiness/incident routes may be next steps but cannot replace the safety disposition.
4. **Atomic versus stage support fixture**: uphold smallest-sufficient routing. The two tool-support fixtures are revised to the exact atomic targets `test-runtime-bootstrap` and `tool-runtime-readiness`; stage 15 remains for multi-capability support or unresolved runtime-owner selection.
5. **Phase 4 control points**: promote `explicit-human-approval` and `separate-remediation-capability` to first-class non-executable route control points so complete-route evidence can represent review/remediation separation structurally.
6. **Mutation validity**: retain deterministic semantic-marker mutation Gates as authoritative. Create behavioral mutation challenges only where an independently authored prompt is causally discriminating; otherwise record `deterministic-only` rather than `survived`. Distinguish lifecycle approval from per-action authorization in the Phase 8 human-checkpoint mutation.

## Revision Location

- `evals/candidates/capability-compiler-v2/phase-10/revision-1/`
- Version: `0.1.1-v2-candidate`
- Status: `evaluating`
- Base identities: exact Phase 4 and Phase 8 artifact hashes.

Revision 1 contains only:

- a complete revised Phase 4 specialized UI Recipe and its revised route fixtures;
- a complete revised Phase 8 router, revised router fixtures, and explicit safety dispositions;
- revised Phase 8 stage/composite Recipes required by findings 1, 2, and 6;
- an unchanged-reference manifest for unaffected Phase 8 stage/composite Recipes;
- mutation-policy and targeted evaluation plans;
- provenance and exact patch ledger.

No Phase 3–7 Skill content is copied or rewritten unless the 157-record review ledger identifies a real semantic defect. A lack of such defects means zero atomic Skill revisions.

## Targeted Re-evaluation

Use the frozen Phase 9 runner protocol and model identity, but a new Phase 10 plan and output root.

Required checks:

- all four Phase 4 Recipe holdouts;
- all 22 Phase 8 router authored/holdout cases with revised exact expectations;
- all 14 Phase 8 Recipe authored/holdout assertions;
- matched controls and mutations for the two Phase 4 control-point changes and six Phase 8 structural changes;
- explicit negative cases proving safety disposition does not execute an action;
- explicit cases proving atomic runtime targets return to the blocked owner and do not grant lifecycle approval.

All targeted release thresholds are 100%. Failed cases remain preserved. No threshold changes after results.

## Review Evidence

- per-Phase review packets containing case input, expected outcome, candidate output, and evidence path;
- one 157-record Skill review ledger;
- one open-finding adjudication matrix;
- one revision patch ledger with old/new hashes and semantic rationale;
- targeted run artifacts with the same prompt/material/case/command/events/output/parse/run/grade/manifest chain as Phase 9;
- a review report that clearly distinguishes parent-direct semantic review from final user approval.

## Gates

Phase 10 fails closed on:

- Phase 3–9 tree drift;
- any modification beneath frozen Phase 3–9 candidate or run roots;
- fewer than 157 Skill review records or 314 reviewed outputs;
- a Skill accepted without both holdout evidence paths;
- an unadjudicated Phase 9 open finding;
- safety disposition that performs or implicitly authorizes the forbidden action;
- revised Recipe/router permission widening;
- changed unaffected Recipe hashes;
- rerun prompt containing expected answers;
- incomplete targeted evidence;
- any targeted threshold below 100%;
- claim of final human approval, release, remote action, provider mutation, local-system mutation, or production execution.

## Outputs

- `tools/curation/v2_compile_phase10_revision.py`
- `tools/curation/v2_phase10_review.py`
- `tools/curation/v2_phase10_runner.py`
- `tools/curation/v2_phase10_gate.py`
- `tools/curation/v2_phase10_report.py`
- `tests/curation/test_v2_phase10_gate.py`
- `curation/v2/phase-10/review-packets/`
- `curation/v2/phase-10/skill-review-ledger.json`
- `curation/v2/phase-10/finding-adjudications.json`
- `evals/candidates/capability-compiler-v2/phase-10/revision-1/`
- `evals/runs/capability-compiler-v2/phase-10/`
- `.specs/capability-compiler-v2/phase-10/{gate-report,artifact-manifest,phase-report}.json`

## Stop Conditions

Stop on frozen evidence drift, a genuine atomic Skill defect requiring broader re-evaluation, ambiguous product/safety authority, targeted model-runtime failure, threshold miss, evidence loss, or any attempt to convert this review into final user approval or release.
