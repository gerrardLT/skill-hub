# Output and Handoff Contracts

## Standard work envelope

Every material OS output should include:

1. Decision or objective.
2. Inputs and accepted upstream artifacts.
3. Facts and evidence.
4. Inferences.
5. Assumptions and unknowns.
6. Result or specification.
7. Risks, edge cases and non-goals.
8. Acceptance criteria or verification evidence.
9. Traceability links.
10. Next owner, stage and blocking Gate.

## Completion status

- `DONE`: work and fresh verification are complete; evidence is cited.
- `DONE_WITH_CONCERNS`: deliverable is usable but residual concerns are explicit.
- `BLOCKED`: an external dependency, failed Gate or critical risk prevents progress.
- `NEEDS_CONTEXT`: a specific indispensable input is unavailable and cannot be inferred safely.

Do not report `DONE` merely because a document or code diff exists.

## Content acceptance

For text artifacts, require more than headings and word count:

- non-empty sections matching the artifact contract;
- concrete evidence/source anchors;
- an explicit decision or commitment;
- measurable or falsifiable conditions;
- ownership, identity or version linkage;
- sufficiently distinct section content rather than copied boilerplate.

Reject excessive `TBD`, “as needed”, “later”, or similar vague language. High-Assurance and high-criticality artifacts require an independent verifier; owner and verifier must differ.

## Handoff acceptance

The receiving OS must validate:

- artifact versions and scope;
- unresolved questions and risks;
- acceptance criteria;
- environment and dependency assumptions;
- traceability to upstream intent;
- whether evidence is current enough for the decision.

The receiver may reject or partially accept a handoff and route it back.

When an accepted upstream artifact changes, treat all downstream derivatives as stale until they are re-reviewed and reaccepted. Run `impact` before changing a material artifact and `reconcile --apply` after detecting out-of-band file changes.
