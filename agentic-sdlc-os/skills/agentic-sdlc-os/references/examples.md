# Worked Scenarios

## New SaaS MVP

1. PM validates the target problem and defines outcome, scope and measurement.
2. Design creates complete flows/states and validates the prototype.
3. Engineering passes build-ready, implements in small verified increments and passes verification-ready.
4. QA independently validates risk and recommends release.
5. Release performs canary rollout with rollback and production verification.
6. Evolution compares activation/retention against the product hypothesis and routes learning back.

## Rescue a weak existing project

1. Initialize as `brownfield` and inventory current artifacts, architecture, tests, deployment and telemetry.
2. Record baseline evidence and critical risks.
3. Diagnose the highest-leverage constraint instead of rewriting by default.
4. Route to the owning OS, preserve behavior with tests, improve in reversible increments and re-run downstream Gates.

## Production incident

1. Evolution TRIAGE establishes impact and coordinates stabilization.
2. Release executes an authorized rollback or containment if appropriate.
3. Engineering identifies root cause and provides a verified fix.
4. QA runs impact-based regression.
5. Release rolls out progressively.
6. Evolution records incident review and learning-decision, including systemic prevention.

## Small isolated task

A copy change or bounded bug fix does not require every OS. Route directly, inspect upstream intent and downstream impact, produce the minimum sufficient evidence and update traceability.
