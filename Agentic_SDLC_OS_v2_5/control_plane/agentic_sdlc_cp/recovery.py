from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any

from sqlalchemy import select

from .db import Database
from .jobs import JobQueue
from .locks import LeaseLockManager
from .models import OutboxEvent, Project
from .repository import ProjectRepository


@dataclass(frozen=True)
class RecoveryReport:
    audit_checked: int
    audit_failed: int
    jobs_requeued: int
    jobs_dead: int
    leases_reaped: int
    unpublished_outbox: int


class RecoveryService:
    def __init__(self, database: Database):
        self.database = database
        self.jobs = JobQueue()
        self.locks = LeaseLockManager(database)
        self.projects = ProjectRepository()

    def recover(self) -> RecoveryReport:
        with self.database.session() as session:
            job_result = self.jobs.reap_expired(session)
            project_ids = list(session.scalars(select(Project.id)).all())
            audit_failed = 0
            for project_id in project_ids:
                result = self.projects.verify_audit_chain(session, project_id)
                if not result["valid"]:
                    audit_failed += 1
            unpublished = len(list(session.scalars(select(OutboxEvent.id).where(OutboxEvent.published.is_(False))).all()))
        leases_reaped = self.locks.reap_expired()
        return RecoveryReport(
            audit_checked=len(project_ids),
            audit_failed=audit_failed,
            jobs_requeued=job_result["requeued"],
            jobs_dead=job_result["dead"],
            leases_reaped=leases_reaped,
            unpublished_outbox=unpublished,
        )

    def payload(self) -> dict[str, Any]:
        return asdict(self.recover())
