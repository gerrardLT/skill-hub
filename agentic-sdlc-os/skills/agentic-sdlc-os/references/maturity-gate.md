# Maturity claim gate

Treat release maturity as an evidence claim, not a self-assigned label.

`production-candidate` requires all of:

- at least 3 independent real project inputs and 3 independently verified executable project validations;
- real, non-synthetic L5-B with >=5 complete pairs, sealed, `decision=positive`, and `formal_evidence_eligible=true`;
- live PostgreSQL control-plane report with concurrency stress and recovery drill passing;
- >=30 production soak days with zero P0 and zero P1 control-plane incidents;
- RBAC, secret rotation, backup/restore and audit-export drills.

Every evidence artifact must have a SHA-256 binding. Missing evidence fails closed.

Use:

```bash
python scripts/maturity_gate.py template --output maturity-evidence.json
python scripts/maturity_gate.py assess maturity-evidence.json --target production-candidate --json
```

Synthetic L5-B, SQLite-only stress, static PostgreSQL DDL checks, planning-only projects and self-reported claims cannot satisfy Production Candidate.
