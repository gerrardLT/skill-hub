# Capability Compiler V2 — Phase 8 Plan

## Objective

Assemble the 157 Phase 3–7 atomic candidate Skills into conditional, permission-preserving candidate Recipes and one minimal-route router. Preserve all 15 lifecycle stages, the 14-stage mandatory spine, the cross-cutting support stage, and all 13 mandatory handoffs. Do not release or execute any Recipe.

## Frozen Inputs

- Phase 2 tree: `57ff1aec49b2b7b370d74d36e52659d7338adf2f16260fe62be7ada870472601`
- Phase 3 tree: `de60929ce7eb1877ffb64a9e8cd671beec389b433f843e10320701c890de8965`
- Phase 4 tree: `968fd1e2175bdc35d77a4d9025a88ab35e5f096fba353137dbf9770e030d4695`
- Phase 5 tree: `7b39fb29c0a25a4a97243e9a857840d14541a9f839e550970c29cc014122e1ee`
- Phase 6 tree: `7e8ff8c23ede16d189a9c89d141e2fee87df63251d5d27ec40aa40eef1d24561`
- Phase 7 tree: `c76902fd5df781db653e214268b044cb4a8cc389a4fce0a188f72a5fba829926`
- Candidate Skills: exactly 157 unique IDs across Phase 3–7.
- Lifecycle: 15 stages, 14 mandatory spine stages, one optional support stage, 13 mandatory handoffs.

## Candidate Location

- `evals/candidates/capability-compiler-v2/phase-8/recipes/`
- `evals/candidates/capability-compiler-v2/phase-8/router.json`
- `evals/candidates/capability-compiler-v2/phase-8/skill-index.json`
- Version: `0.1.0-v2-candidate`
- Status: `evaluating`
- Execution state: `not-run-phase-9`

## Recipe Set

### Stage Recipes — 15

One Recipe per primary lifecycle stage. Every atomic candidate appears in exactly one primary stage Recipe. Each step preserves:

- exact candidate path and contract hash;
- responsibility-derived condition and anti-trigger boundaries;
- internal hard, optional, and feedback dependencies;
- permission identity, mutation scope, and remote-write flag;
- required inputs, outputs, gates, stop states, and evidence contract;
- `disabled-pending-current-authorization` for remote, external-session, and local-system mutations.

No stage Recipe runs every step by default. Every step defaults to skipped unless its atomic trigger matches, prerequisites exist, and the permission boundary is compatible.

### Composite Recipes — 5

1. `full-software-lifecycle`: stages 1–14 plus conditional stage 15 support; preserves all 13 mandatory handoffs.
2. `product-discovery-and-planning`: stages 1–4.
3. `feature-build-and-verify`: stages 4–10.
4. `verified-change-delivery-and-observation`: stages 10–12.
5. `incident-recovery-and-learning`: stages 12–14.

Composite Recipes reference stage Recipes only. They do not directly execute atomic Skills, duplicate stage logic, or turn optional branches into mandatory work.

The existing Phase 4 `complete-ui-design-and-review` candidate remains a specialized Recipe and is referenced by the router rather than copied or released.

## Router Contract

The router selects the smallest sufficient target:

1. one atomic outcome → one candidate Skill;
2. one lifecycle stage with multiple related outcomes → one stage Recipe;
3. complete UI design/review → the Phase 4 specialized UI Recipe;
4. bounded cross-stage product, feature, delivery, or incident work → one composite Recipe;
5. explicit end-to-end product request → `full-software-lifecycle`;
6. tool/runtime prerequisite → stage 15 support Recipe only, then return to the blocked owner.

Safety overrides precede intent matching:

- missing customer/proprietary/external-Judge governance → `needs-input` or `blocked`;
- review plus repair → split identities and require a human checkpoint;
- observation plus rollback → split identities and require current rollback authorization;
- remote or local-system action without fresh per-action authorization → route to preflight/readiness or stop, never auto-activate;
- one remote authorization never propagates to a later remote step;
- unsupported or ambiguous multi-domain intent → route to intake, not full lifecycle by default.

## Handoff and Invalidation Contract

Every one of the 13 mandatory handoffs carries the full four-part artifact contract:

- artifact identities and hashes;
- decision and authority record;
- completion evidence;
- known gaps and residual risk.

Each handoff also carries the exact Phase 2 invalidation policy. Upstream changes invalidate the handoff and all dependent downstream stage evidence. Textually identical regenerated output does not preserve evidence unless source identity, inputs, outputs, gates, and hashes remain valid.

## Human Checkpoints

At minimum:

- product problem and strategy selection;
- requirements and scope approval;
- visual or taste selection and prototype promotion;
- architecture, authorization, data migration, and risk approval;
- source mutation and accepted remediation scope;
- independent QA/review disposition;
- release readiness and residual-risk acceptance;
- every push, PR change, comment, merge, deployment, provider configuration, rollback, and local-system action;
- incident closure;
- learning persistence and next-cycle commitment.

## Remote and Production Boundary

Phase 8 constructs declarative candidate Recipes only. No atomic candidate, stage Recipe, composite Recipe, router case, Gate, or test may perform provider, production, remote Git, local-system, browser-auth, credential, merge, deployment, rollback, or publication actions. Every such step remains disabled pending fresh current authorization in a later real run.

## Evaluation Fixtures

- authored router cases for atomic, stage, specialized UI, composite, full-lifecycle, ambiguous, governance-blocked, review/repair split, observation/rollback split, and remote-action stop;
- physically separate router holdouts;
- authored and holdout Recipe path cases for optional branches, skipped stages, support-stage insertion, feedback invalidation, remote stop, and resume;
- mutations that delete one handoff, make one stage always-on, widen a review scope, activate a remote step without authorization, bypass human approval, or remove invalidation.

All evaluation remains `not-run-phase-9`.

## Verification

Phase 8 Gate must fail closed on:

- Phase 2–7 tree drift, including the intentionally incorrect unlabeled Phase 3 hash in this plan;
- missing or duplicate candidate Skill coverage;
- stage assignment mismatch with Phase 2 `lifecycle_stage_id`;
- permission, mutation scope, remote-write, path, or contract-hash drift;
- missing internal dependency or unknown target;
- step without an explicit condition or a non-routing step marked always-on;
- remote/local-system action enabled without current authorization;
- missing stage Recipe, composite Recipe, support-stage semantics, or specialized UI route;
- missing, reordered, altered, or weakened mandatory handoff artifact contracts and invalidation;
- router selecting a larger Recipe when an atomic or stage target is sufficient;
- review/remediation, readiness/change, observation/rollback, incident/action, or learning/persistence identity collapse;
- false execution, approval, or release evidence;
- unresolved semantic review findings.

## Outputs

- 15 stage Recipes.
- 5 composite Recipes.
- One router and Skill index.
- Router and Recipe authored/holdout fixtures and mutation plans.
- Schemas, Gate, mutation tests, semantic review, manifest, and phase report.

## Stop Conditions

Stop on prior-tree drift, candidate coverage mismatch, dependency or handoff conflict, permission widening, any attempt to execute a remote/local-system action, or ambiguity that changes the chosen minimal route, human authority, lifecycle stage, or invalidation behavior.
