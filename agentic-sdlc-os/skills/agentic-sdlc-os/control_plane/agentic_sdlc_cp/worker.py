from __future__ import annotations

import time
from collections.abc import Callable
from typing import Any

from .db import Database
from .jobs import JobLease, JobQueue


Handler = Callable[[dict[str, Any]], dict[str, Any]]


class Worker:
    def __init__(self, database: Database, worker_id: str, handlers: dict[str, Handler]):
        self.database = database
        self.worker_id = worker_id
        self.handlers = handlers
        self.queue = JobQueue()

    def run_once(self, lease_seconds: int = 60) -> bool:
        with self.database.session() as session:
            lease = self.queue.lease_next(
                session,
                worker_id=self.worker_id,
                lease_seconds=lease_seconds,
                job_types=sorted(self.handlers),
            )
        if lease is None:
            return False
        handler = self.handlers.get(lease.job_type)
        if handler is None:
            with self.database.session() as session:
                self.queue.fail(
                    session,
                    job_id=lease.id,
                    worker_id=self.worker_id,
                    fencing_token=lease.fencing_token,
                    error=f"No handler registered for {lease.job_type}",
                )
            return True
        try:
            result = handler(lease.payload)
            with self.database.session() as session:
                self.queue.complete(
                    session,
                    job_id=lease.id,
                    worker_id=self.worker_id,
                    fencing_token=lease.fencing_token,
                    result=result,
                )
        except Exception as exc:
            with self.database.session() as session:
                self.queue.fail(
                    session,
                    job_id=lease.id,
                    worker_id=self.worker_id,
                    fencing_token=lease.fencing_token,
                    error=f"{type(exc).__name__}: {exc}",
                )
        return True

    def run_forever(self, *, poll_seconds: float = 1.0, lease_seconds: int = 60) -> None:
        while True:
            if not self.run_once(lease_seconds=lease_seconds):
                time.sleep(poll_seconds)
