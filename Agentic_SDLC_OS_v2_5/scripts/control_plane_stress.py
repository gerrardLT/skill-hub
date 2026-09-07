#!/usr/bin/env python3
"""Concurrent control-plane stress and recovery drill.

Without --database-url this runs a local SQLite safety regression. A production
maturity claim requires a PostgreSQL URL and a passing report from that dialect.
"""
from __future__ import annotations

import argparse
import collections
import json
import tempfile
import threading
import time
import uuid
from pathlib import Path
from typing import Any

from sqlalchemy.exc import OperationalError

ROOT = Path(__file__).resolve().parents[1]
import sys
sys.path.insert(0, str(ROOT / "control_plane"))

from agentic_sdlc_cp.db import create_database, init_database
from agentic_sdlc_cp.jobs import JobQueue
from agentic_sdlc_cp.locks import LeaseLockManager
from agentic_sdlc_cp.recovery import RecoveryService
from agentic_sdlc_cp.repository import ProjectRepository, RevisionConflict


def run_stress(database_url: str, *, jobs: int, workers: int, updates_per_worker: int) -> dict[str, Any]:
    database = create_database(database_url)
    init_database(database)
    queue = JobQueue()
    repository = ProjectRepository()
    suffix = uuid.uuid4().hex[:12]
    project_id = f"stress-{suffix}"
    with database.session() as session:
        repository.create_project(session, name="control-plane-stress", actor="stress", project_id=project_id, state={"counter": 0})
        for index in range(jobs):
            queue.enqueue(session, project_id=project_id, job_type="stress", payload={"index": index}, idempotency_key=f"{suffix}-job-{index}")

    claims: list[str] = []
    errors: list[str] = []
    guard = threading.Lock()
    barrier = threading.Barrier(workers)

    def job_worker(index: int) -> None:
        try:
            barrier.wait()
        except threading.BrokenBarrierError:
            return
        while True:
            try:
                with database.session() as session:
                    lease = queue.lease_next(session, worker_id=f"job-worker-{index}", lease_seconds=30, job_types=["stress"])
                if lease is None:
                    return
                with guard:
                    claims.append(lease.id)
            except OperationalError as exc:
                with guard:
                    errors.append(f"job:{exc}")
                time.sleep(0.002)

    threads = [threading.Thread(target=job_worker, args=(index,)) for index in range(workers)]
    for thread in threads: thread.start()
    for thread in threads: thread.join()
    claim_counts = collections.Counter(claims)

    state_barrier = threading.Barrier(workers)
    state_errors: list[str] = []

    def state_worker(index: int) -> None:
        try:
            state_barrier.wait()
        except threading.BrokenBarrierError:
            return
        for iteration in range(updates_per_worker):
            for _attempt in range(200):
                try:
                    with database.session() as session:
                        revision = repository.get_project(session, project_id).revision
                    with database.session() as session:
                        repository.update_state(
                            session,
                            project_id=project_id,
                            expected_revision=revision,
                            actor=f"state-worker-{index}",
                            event_type="stress-increment",
                            mutate=lambda state: state | {"counter": int(state.get("counter", 0)) + 1},
                        )
                    break
                except (RevisionConflict, OperationalError):
                    time.sleep(0.001)
            else:
                with guard:
                    state_errors.append(f"worker={index} iteration={iteration}")

    threads = [threading.Thread(target=state_worker, args=(index,)) for index in range(workers)]
    for thread in threads: thread.start()
    for thread in threads: thread.join()

    with database.session() as session:
        project = repository.get_project(session, project_id)
        audit = repository.verify_audit_chain(session, project_id)
        recovery_job = queue.enqueue(session, project_id=project_id, job_type="recovery", payload={}, idempotency_key=f"{suffix}-recovery", max_attempts=3)
    with database.session() as session:
        recovery_lease = queue.lease_next(session, worker_id="recovery-worker", lease_seconds=1, job_types=["recovery"])
        if recovery_lease is None or recovery_lease.id != recovery_job.id:
            raise RuntimeError("Could not create recovery lease")

    lock_manager = LeaseLockManager(database)
    lock_manager.acquire(f"stress-lock-{suffix}", "recovery-worker", ttl_seconds=1, wait_seconds=2)
    time.sleep(1.2)
    recovery = RecoveryService(database).payload()

    expected_updates = workers * updates_per_worker
    passed = (
        not errors
        and not state_errors
        and len(claims) == jobs
        and len(claim_counts) == jobs
        and all(count == 1 for count in claim_counts.values())
        and project.revision == expected_updates
        and int(project.state_json.get("counter", -1)) == expected_updates
        and audit.get("valid") is True
        and int(recovery.get("jobs_requeued", 0)) >= 1
        and int(recovery.get("leases_reaped", 0)) >= 1
        and int(recovery.get("audit_failed", 1)) == 0
    )
    result = {
        "passed": passed,
        "database": database.engine.dialect.name,
        "live_postgresql": database.engine.dialect.name == "postgresql",
        "concurrency_stress": passed,
        "recovery_drill": int(recovery.get("jobs_requeued", 0)) >= 1 and int(recovery.get("leases_reaped", 0)) >= 1 and int(recovery.get("audit_failed", 1)) == 0,
        "jobs": {"expected": jobs, "claims": len(claims), "unique": len(claim_counts), "duplicate_claims": sum(max(0, count - 1) for count in claim_counts.values()), "errors": errors[:10]},
        "state": {"expected_updates": expected_updates, "revision": project.revision, "counter": project.state_json.get("counter"), "errors": state_errors[:10], "audit": audit},
        "recovery": recovery,
    }
    database.engine.dispose()
    return result


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Agentic SDLC control-plane stress and recovery drill")
    parser.add_argument("--database-url")
    parser.add_argument("--jobs", type=int, default=50)
    parser.add_argument("--workers", type=int, default=10)
    parser.add_argument("--updates-per-worker", type=int, default=10)
    parser.add_argument("--output")
    args = parser.parse_args(argv)
    temp = None
    try:
        if args.database_url:
            url = args.database_url
        else:
            temp = tempfile.TemporaryDirectory(prefix="sdlc-control-stress-")
            url = f"sqlite+pysqlite:///{Path(temp.name) / 'stress.db'}"
        result = run_stress(url, jobs=args.jobs, workers=args.workers, updates_per_worker=args.updates_per_worker)
        payload = json.dumps(result, indent=2)
        if args.output:
            Path(args.output).write_text(payload + "\n", encoding="utf-8")
        print(payload)
        return 0 if result["passed"] else 2
    finally:
        if temp is not None:
            temp.cleanup()


if __name__ == "__main__":
    raise SystemExit(main())
