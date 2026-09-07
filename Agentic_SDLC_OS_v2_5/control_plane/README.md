# Production control plane

The local `.sdlc/state.json` kernel remains available for single-user work. The production control plane adds PostgreSQL persistence, revision compare-and-swap, leases/fencing, idempotent jobs, RBAC/approval separation, hash-chained audit, recovery, encrypted secrets, budgets and a minimal API/dashboard.

## Important database boundary

SQLite is a **local safety/test mode**, not a production topology. v2.3 makes its job claim and revision updates atomic so accidental multi-thread use does not silently double-lease jobs or lose successful state updates, but Production Candidate evidence still requires live PostgreSQL stress and recovery testing.

## Start

```bash
export SDLC_MASTER_KEY_B64="$(python scripts/control_plane.py generate-master-key)"
export SDLC_BOOTSTRAP_TOKEN="replace-me"
docker compose up --build
```

## Stress / recovery

```bash
python scripts/control_plane_stress.py --output sqlite-stress.json
python scripts/control_plane_stress.py --database-url 'postgresql+psycopg://...' --output postgres-stress.json
```

The PostgreSQL run must show zero duplicate job claims, exact revision convergence, a valid audit chain, expired job requeue and expired lease reaping before it can be used as production-maturity evidence.
