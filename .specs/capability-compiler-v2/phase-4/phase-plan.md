# Capability Compiler V2 — Phase 4 Plan

## Objective

Rewrite the 17 Phase 4 UX/UI taxonomy capabilities into atomic, provenance-complete candidate Skills and define one candidate end-to-end UI design/review Recipe without releasing either. The set must cover product-to-interface translation, information and interaction structure, visual system, authentic content, responsive composition, states, accessibility, motion, AI uncertainty, preservation-aware redesign, and real rendered review.

## Frozen Inputs

- Phase 2 artifact tree SHA-256: `57ff1aec49b2b7b370d74d36e52659d7338adf2f16260fe62be7ada870472601`
- Phase 3 artifact tree SHA-256: `de60929ce7eb1877ffb64a9e8cd671beec389b433f843e10320701c890de8965`
- Phase ownership: exactly 17 IDs in `curation/v2/lifecycle/phase-ownership.json` phase `4`.
- Source Skills remain immutable.
- V1 released Slots and Recipes remain immutable.

## Candidate Location

- Skills: `evals/candidates/capability-compiler-v2/phase-4/skills/<capability-id>/`
- Candidate UI Recipe: `evals/candidates/capability-compiler-v2/phase-4/recipes/complete-ui-design-and-review.json`
- Version: `0.1.0-v2-candidate`
- Status: `evaluating`
- Evaluation state: `not-run-phase-9`

## Atomic Skill Boundary

Each candidate Skill must define:

1. one trigger and at least two anti-triggers;
2. explicit inputs, procedure, artifacts, status mapping, failure modes, and non-responsibilities;
3. exact Phase 2 provenance sets and source evidence;
4. permission behavior derived from side effects, not capability name;
5. at least two authored positive cases, two anti-cases, one boundary case, one authority-stop case, and two physically separate holdouts;
6. one mutation targeting its distinctive semantic gate;
7. no pipeline execution, remote writes, release claim, or downstream impersonation.

## Required UI Coverage Gates

The 17-Skill set and candidate Recipe must explicitly cover:

- user flow and information hierarchy before visual polish;
- design context, audience, goals, brand evidence, and success criteria;
- design-system foundations, token extraction/normalization, component/state coverage, and provenance;
- authentic content, copy, and asset provenance rather than placeholder UI;
- mobile, tablet, desktop, intermediate widths, zoom, overflow, density, and touch-target checks;
- loading, empty, error, disabled, validation, permission, success, interruption, and recovery states;
- semantic structure, keyboard, focus, assistive technology, contrast, visual input, reduced motion, and error recovery;
- purposeful, interruptible, reduced-motion-safe, deterministic motion;
- AI confidence, uncertainty, explainability, correction, escalation, and safe failure;
- preservation-aware redesign with explicit invariants;
- real rendered evidence acquisition, multi-viewport review, severity, blocking findings, and release disposition.

Static source inspection alone cannot satisfy rendered-review or release-disposition capabilities. Browser/runtime capture must use artifact-only identities; source repair remains a different capability and Recipe branch.

## Candidate Recipe Boundary

The Phase 4 Recipe is declarative and conditional. It may order and route the 17 candidates, define checkpoints and feedback edges, and aggregate evidence. It must not:

- execute a candidate itself;
- merge reviewer and remediation identities;
- treat source inspection as rendered evidence;
- trigger remote deployment or release;
- claim any candidate passed Phase 9 or Phase 10.

Expected high-level flow:

1. task route and governance;
2. context/direction contract;
3. optional external token extraction or preservation baseline;
4. divergent prototype exploration and human variant selection;
5. information/interaction, visual language, design system, authentic content, responsive, accessibility, motion, and AI-UX branches as applicable;
6. cross-domain preflight;
7. independent review scope and rendered evidence acquisition;
8. evidence-based review and critique;
9. human release disposition or bounded repair feedback, never automatic source mutation by a reviewer.

## Verification

Phase 4 Gate must fail closed on:

- Phase 2 or Phase 3 artifact identity drift;
- missing/extra candidates or wrong ownership;
- incomplete provenance, stale file hashes, trigger collisions, or authored/holdout leakage;
- a review capability holding source-write permission;
- a source-editing capability posing as a read-only reviewer;
- omission of any required UI coverage marker;
- a rendered-review candidate accepting static inspection as sufficient evidence;
- a Recipe step with incompatible permission identity, missing conditionality, illegal reviewer-to-repair transition, or remote write;
- any evaluation plan claiming execution before Phase 9;
- unresolved semantic review findings.

## Outputs

- 17 candidate Skill packages.
- Candidate UI Recipe and Recipe-specific routing/checkpoint fixtures.
- Phase 4 schemas, design ledger, semantic review, Gate, mutation tests, artifact manifest, and phase report.
- Unified runner updated only after Phase 4 directed tests are green.

## Stop Conditions

Stop on source or Phase 2/3 identity drift, unresolved semantic conflict, insufficient rendered-evidence permission separation, missing human design decision authority, or any need for remote/browser/provider mutation not already represented by an authorized artifact-only identity.
