# change-delivery-preflight

Status: released 1.0.0

## Responsibility

Prepare a verified change for delivery by checking branch state, merge base, credentials, automation stops, and documentation invariants.

## Inputs

A reviewed change, repository state, delivery policy, and intended publication boundary.

## Method

1. Classify every supplied statement as evidence, constraint, unknown, conflict, or authorized decision before acting.
2. Preserve stable IDs, source references, authority boundaries, and unresolved unknowns in every output.
3. Execute only the declared `delivery` responsibility; do not absorb upstream or downstream work.
4. Produce numbered findings or records with direct evidence citations and an explicit per-Gate result.
5. Return `needs-input` for missing required facts, `blocked` for missing authority or tooling, and `failed` for observed execution or verification failure.
6. Return `passed` only when all declared Gates have current evidence.

## Output

A delivery-ready package or explicit preflight blockers; no merge or deployment action.

## Safety

- Respect the execution adapter and explicit authorization boundary.
- Never fabricate evidence, silently resolve conflicts, erase unknowns, or treat a stale result as current.
- Never use remote Git, network, merge, or deployment authority unless the host supplied that exact authorization scope.

## Required Format

First line: `Status: passed|needs-input|blocked|failed`.
Then include `Evidence:`, numbered records, `Gate Results:`, and `Unknowns:` sections.
