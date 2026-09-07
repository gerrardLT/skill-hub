from __future__ import annotations

import collections
import tempfile
import threading
import time
import unittest
from pathlib import Path

from sqlalchemy.exc import OperationalError

from control_plane.agentic_sdlc_cp.db import create_database, init_database
from control_plane.agentic_sdlc_cp.jobs import JobQueue
from control_plane.agentic_sdlc_cp.repository import ProjectRepository, RevisionConflict


class V23ConcurrencyCase(unittest.TestCase):
    def test_sqlite_job_claim_is_atomic_across_workers(self) -> None:
        with tempfile.TemporaryDirectory(prefix="sdlc-v23-jobs-") as temp:
            database = create_database(f"sqlite+pysqlite:///{Path(temp) / 'jobs.db'}")
            init_database(database)
            queue = JobQueue()
            with database.session() as session:
                for index in range(30):
                    queue.enqueue(
                        session,
                        job_type="stress",
                        payload={"index": index},
                        idempotency_key=f"job-{index}",
                    )

            claims: list[str] = []
            errors: list[str] = []
            guard = threading.Lock()
            barrier = threading.Barrier(8)

            def worker(index: int) -> None:
                try:
                    barrier.wait()
                except threading.BrokenBarrierError:
                    return
                while True:
                    try:
                        with database.session() as session:
                            lease = queue.lease_next(session, worker_id=f"worker-{index}", lease_seconds=30)
                        if lease is None:
                            return
                        with guard:
                            claims.append(lease.id)
                    except OperationalError as exc:
                        with guard:
                            errors.append(str(exc))
                        time.sleep(0.001)

            threads = [threading.Thread(target=worker, args=(index,)) for index in range(8)]
            for thread in threads:
                thread.start()
            for thread in threads:
                thread.join()

            counts = collections.Counter(claims)
            self.assertFalse(errors, errors[:3])
            self.assertEqual(len(claims), 30)
            self.assertEqual(len(counts), 30)
            self.assertTrue(all(value == 1 for value in counts.values()))

    def test_sqlite_revision_cas_preserves_all_retried_updates(self) -> None:
        with tempfile.TemporaryDirectory(prefix="sdlc-v23-state-") as temp:
            database = create_database(f"sqlite+pysqlite:///{Path(temp) / 'state.db'}")
            init_database(database)
            repository = ProjectRepository()
            with database.session() as session:
                repository.create_project(
                    session,
                    name="concurrency-stress",
                    actor="bootstrap",
                    project_id="project-stress",
                    state={"counter": 0},
                )

            errors: list[str] = []
            guard = threading.Lock()
            barrier = threading.Barrier(8)

            def worker(index: int) -> None:
                try:
                    barrier.wait()
                except threading.BrokenBarrierError:
                    return
                for iteration in range(5):
                    for _attempt in range(100):
                        try:
                            with database.session() as session:
                                revision = repository.get_project(session, "project-stress").revision
                            with database.session() as session:
                                repository.update_state(
                                    session,
                                    project_id="project-stress",
                                    expected_revision=revision,
                                    actor=f"worker-{index}",
                                    event_type="stress-increment",
                                    mutate=lambda state: state | {"counter": int(state.get("counter", 0)) + 1},
                                )
                            break
                        except (RevisionConflict, OperationalError):
                            time.sleep(0.001)
                    else:
                        with guard:
                            errors.append(f"worker={index} iteration={iteration} retries exhausted")

            threads = [threading.Thread(target=worker, args=(index,)) for index in range(8)]
            for thread in threads:
                thread.start()
            for thread in threads:
                thread.join()

            with database.session() as session:
                project = repository.get_project(session, "project-stress")
                audit = repository.verify_audit_chain(session, "project-stress")
            self.assertFalse(errors, errors)
            self.assertEqual(project.revision, 40)
            self.assertEqual(project.state_json["counter"], 40)
            self.assertTrue(audit["valid"], audit)
            self.assertEqual(audit["events"], 41)


if __name__ == "__main__":
    unittest.main()
