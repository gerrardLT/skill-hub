# Production control plane

Use the local `.sdlc/` kernel for a single operator or repository. Use the database control plane when multiple Agents, humans or runners can write concurrently.

## Guarantees

- PostgreSQL-ready SQLAlchemy data model with SQLite local-safety mode.
- Project updates use revision compare-and-swap; stale writes fail instead of silently overwriting.
- SQLite job leasing uses a single conditional `UPDATE ... RETURNING` claim because SQLite ignores `FOR UPDATE`.
- Hash-chained audit events and revision snapshots.
- Database leases with monotonic fencing tokens.
- Idempotent job queue, heartbeat, retry, dead-letter and expired-lease recovery.
- Role-based access, bearer tokens and high-assurance separation of duties.
- AES-GCM encrypted secrets.
- Gate approvals bound to current artifact revision.
- Budget preflight and run accounting.
- Transactional outbox records.

## Concurrency and recovery verification

Local safety regression:

```bash
python scripts/control_plane_stress.py --output sqlite-stress.json
```

This must show zero duplicate job claims, exact revision/counter convergence, a valid audit chain, expired-job requeue and expired-lease reaping.

Production evidence requires the same stress tool against PostgreSQL:

```bash
python scripts/control_plane_stress.py \
  --database-url 'postgresql+psycopg://...' \
  --output postgres-stress.json
```

SQLite results **cannot** satisfy the Production Candidate PostgreSQL requirement.

## PostgreSQL verification

```bash
python scripts/postgres_conformance.py
SDLC_POSTGRES_TEST_URL='postgresql+psycopg://...' python scripts/postgres_conformance.py --require-live
```

Static conformance is not equivalent to a live PostgreSQL test.

## Maturity claim gate

Before using `Production Candidate` or stronger language:

```bash
python scripts/maturity_gate.py assess evidence.json --target production-candidate --json
```

The gate requires real sealed L5-B evidence, live PostgreSQL stress/recovery, three independently verified executable real projects, 30-day soak evidence and organization-level RBAC/secret/backup/audit drills.
