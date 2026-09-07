# Dynamic process tailoring

Use two governance layers.

## 1. Project profile

At bootstrap, score nine 0–5 factors: blast radius, data sensitivity, regulatory exposure, irreversibility, technical novelty, problem uncertainty, user exposure, change size and operational complexity. The result is the project's default envelope: `lite`, `standard` or `high-assurance`. Hard escalations override the weighted score.

## 2. Work Item profile

For a bounded change or defect, create a Work Item with explicit affected paths and reassess the same risk factors. The active Work Item Profile controls Gate depth and stage compression.

```bash
python scripts/sdlc.py work-start . --id WORK-001 --title "fix lockfile registry" \
  --bounded --affected-path web/package-lock.json
python scripts/sdlc.py work-status . --json
```

Rules:

- A bounded low-risk Work Item may safely downshift below the project Profile.
- An unbounded Work Item may not downshift below the project Profile.
- Protected paths such as CI, deployment, auth, security, database/schema or Docker escalate to at least `standard`.
- Migration, secrets/credentials, payments/billing/ledger paths escalate to `high-assurance`.
- Installed Domain Packs apply only when the Work Item actually impacts that domain or it is explicitly declared.
- Reassess when scope or affected paths change; never downshift to meet a deadline or budget.

## Compact bounded-lite path

A reversible low-risk fix should not inherit the documentation burden of a high-assurance project. Default core artifacts are:

`Change Plan → Change Verification → Release Recommendation`

Engineering stages compress to `INTAKE → BUILD → HANDOFF`; QA compresses to `INTAKE → EXECUTION → RECOMMENDATION`. Tests, static analysis, diff review and rollback evidence still attach as evidence. Production verification remains mandatory before claiming production completion.

## Record governance

Artifacts are evaluated using the Profile/Criticality of the Work Item that created them. Work-scoped artifacts, evidence and traces from one change cannot satisfy another change's Gate. Project-global critical risks still block all work.
