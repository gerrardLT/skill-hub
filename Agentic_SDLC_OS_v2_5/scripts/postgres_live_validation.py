#!/usr/bin/env python3
"""Live PostgreSQL production-control validation.

Refuses SQLite. Exercises concurrent claiming/state CAS, recovery/dead-letter,
PostgreSQL advisory-lock exclusivity, and an optional real connection-loss drill.
Production Candidate policy requires the connection-loss drill to be executed.
"""
from __future__ import annotations

import argparse
import json
import sys
import time
import uuid
from pathlib import Path
from typing import Any

from sqlalchemy import text, select

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "control_plane"))

from scripts.control_plane_stress import run_stress
from agentic_sdlc_cp.db import create_database, init_database
from agentic_sdlc_cp.jobs import JobQueue
from agentic_sdlc_cp.models import Job
from agentic_sdlc_cp.recovery import RecoveryService


def advisory_lock_drill(database) -> dict[str, Any]:
    key = 4242424242
    c1 = database.engine.connect(); c2 = database.engine.connect()
    try:
        first = bool(c1.scalar(text("SELECT pg_try_advisory_lock(:k)"), {"k": key}))
        second_while_held = bool(c2.scalar(text("SELECT pg_try_advisory_lock(:k)"), {"k": key}))
        c1.execute(text("SELECT pg_advisory_unlock(:k)"), {"k": key})
        second_after_release = bool(c2.scalar(text("SELECT pg_try_advisory_lock(:k)"), {"k": key}))
        if second_after_release:
            c2.execute(text("SELECT pg_advisory_unlock(:k)"), {"k": key})
        return {"passed": first and not second_while_held and second_after_release, "first": first, "second_while_held": second_while_held, "second_after_release": second_after_release}
    finally:
        c1.close(); c2.close()


def dead_letter_drill(database) -> dict[str, Any]:
    queue = JobQueue(); token = uuid.uuid4().hex
    with database.session() as session:
        job = queue.enqueue(session, job_type="dead-letter-drill", payload={}, idempotency_key=f"dead-{token}", max_attempts=1)
    with database.session() as session:
        lease = queue.lease_next(session, worker_id="crash-worker", lease_seconds=1, job_types=["dead-letter-drill"])
        if lease is None or lease.id != job.id:
            return {"passed": False, "reason": "could not lease dead-letter canary"}
    time.sleep(1.2)
    recovery = RecoveryService(database).payload()
    with database.session() as session:
        row = session.scalar(select(Job).where(Job.id == job.id))
        status = row.status if row else None
    return {"passed": status == "dead" and int(recovery.get("jobs_dead", 0)) >= 1, "status": status, "recovery": recovery}


def connection_fault_drill(database) -> dict[str, Any]:
    """Terminate one checked-out backend and prove pool_pre_ping recovers."""
    victim = database.engine.connect(); killer = database.engine.connect()
    pid = None
    try:
        pid = int(victim.scalar(text("SELECT pg_backend_pid()")))
        terminated = bool(killer.scalar(text("SELECT pg_terminate_backend(:pid)"), {"pid": pid}))
        victim_failed = False
        try:
            victim.execute(text("SELECT 1"))
        except Exception:
            victim_failed = True
        try:
            victim.close()
        except Exception:
            pass
        recovered = False
        try:
            with database.engine.connect() as fresh:
                recovered = int(fresh.scalar(text("SELECT 1"))) == 1
        except Exception:
            recovered = False
        return {"passed": terminated and victim_failed and recovered, "terminated": terminated, "victim_failed": victim_failed, "pool_recovered": recovered, "pid": pid}
    except Exception as exc:
        return {"passed": False, "pid": pid, "error": str(exc), "note": "pg_terminate_backend may require pg_signal_backend or equivalent permission"}
    finally:
        try: victim.close()
        except Exception: pass
        try: killer.close()
        except Exception: pass


def validate(database_url: str, *, jobs: int, workers: int, updates: int, connection_fault: bool) -> dict[str, Any]:
    database = create_database(database_url); init_database(database)
    dialect = database.engine.dialect.name
    if dialect != "postgresql":
        database.engine.dispose()
        return {"passed": False, "live_postgresql": False, "database": dialect, "failures": ["database URL is not PostgreSQL"]}
    with database.engine.connect() as conn:
        version = str(conn.scalar(text("SELECT version()")))
    stress = run_stress(database_url, jobs=jobs, workers=workers, updates_per_worker=updates)
    advisory = advisory_lock_drill(database)
    dead = dead_letter_drill(database)
    fault = connection_fault_drill(database) if connection_fault else {"passed": False, "skipped": True, "reason": "--connection-fault not requested"}
    passed = bool(stress.get("passed") and advisory.get("passed") and dead.get("passed") and fault.get("passed"))
    result = {
        "schema_version": "2.5.0", "passed": passed, "database": dialect, "live_postgresql": True,
        "postgres_version": version, "concurrency_stress": bool(stress.get("passed")),
        "recovery_drill": bool(stress.get("recovery_drill")), "dead_letter_drill": bool(dead.get("passed")),
        "advisory_lock_drill": bool(advisory.get("passed")), "connection_fault_drill": bool(fault.get("passed")),
        "details": {"stress": stress, "advisory_lock": advisory, "dead_letter": dead, "connection_fault": fault},
    }
    database.engine.dispose(); return result


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Live PostgreSQL validation for Agentic SDLC OS")
    p.add_argument("--database-url", required=True); p.add_argument("--jobs", type=int, default=100); p.add_argument("--workers", type=int, default=16); p.add_argument("--updates-per-worker", type=int, default=20); p.add_argument("--connection-fault", action="store_true"); p.add_argument("--output")
    args = p.parse_args(argv)
    try:
        result = validate(args.database_url, jobs=args.jobs, workers=args.workers, updates=args.updates_per_worker, connection_fault=args.connection_fault)
        payload = json.dumps(result, indent=2, ensure_ascii=False)
        if args.output:
            path=Path(args.output).resolve(); path.parent.mkdir(parents=True, exist_ok=True); path.write_text(payload+"\n", encoding="utf-8")
        print(payload); return 0 if result.get("passed") else 2
    except Exception as exc:
        print(json.dumps({"passed": False, "live_postgresql": False, "error": str(exc)}, indent=2)); return 2


if __name__ == "__main__":
    raise SystemExit(main())
