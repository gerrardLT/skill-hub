from __future__ import annotations

import uuid
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Any

from sqlalchemy import and_, or_, select, update
from sqlalchemy.orm import Session

from .models import Job, utcnow


def _aware(value: datetime | None) -> datetime | None:
    if value is None:
        return None
    return value if value.tzinfo is not None else value.replace(tzinfo=timezone.utc)


@dataclass(frozen=True)
class JobLease:
    id: str
    project_id: str | None
    job_type: str
    payload: dict[str, Any]
    attempt: int
    fencing_token: int
    lease_expires_at: datetime


class JobQueue:
    def enqueue(
        self,
        session: Session,
        *,
        job_type: str,
        payload: dict[str, Any],
        idempotency_key: str,
        project_id: str | None = None,
        priority: int = 100,
        max_attempts: int = 3,
    ) -> Job:
        existing = session.scalar(select(Job).where(Job.idempotency_key == idempotency_key))
        if existing is not None:
            return existing
        row = Job(
            id=f"job-{uuid.uuid4().hex}",
            project_id=project_id,
            job_type=job_type,
            payload_json=payload,
            idempotency_key=idempotency_key,
            priority=priority,
            max_attempts=max_attempts,
        )
        session.add(row)
        session.flush()
        return row

    def lease_next(
        self,
        session: Session,
        *,
        worker_id: str,
        lease_seconds: int = 60,
        job_types: list[str] | None = None,
    ) -> JobLease | None:
        current = utcnow()
        criteria = [
            Job.status.in_(["queued", "retry"]),
            Job.available_at <= current,
            or_(Job.lease_expires_at.is_(None), Job.lease_expires_at <= current),
        ]
        if job_types:
            criteria.append(Job.job_type.in_(job_types))
        lease_expires_at = current + timedelta(seconds=lease_seconds)
        dialect = session.get_bind().dialect.name

        if dialect == "sqlite":
            # SQLite ignores SELECT ... FOR UPDATE. Claim the job with a single
            # conditional UPDATE so concurrent workers cannot lease the same row.
            candidate_id = (
                select(Job.id)
                .where(and_(*criteria))
                .order_by(Job.priority.asc(), Job.created_at.asc())
                .limit(1)
                .scalar_subquery()
            )
            statement = (
                update(Job)
                .where(Job.id == candidate_id, and_(*criteria))
                .values(
                    status="leased",
                    attempt=Job.attempt + 1,
                    lease_owner=worker_id,
                    heartbeat_at=current,
                    lease_expires_at=lease_expires_at,
                    updated_at=current,
                )
                .returning(Job)
            )
            row = session.scalar(statement.execution_options(synchronize_session=False))
            if row is None:
                return None
        else:
            statement = (
                select(Job)
                .where(and_(*criteria))
                .order_by(Job.priority.asc(), Job.created_at.asc())
                .limit(1)
                .with_for_update(skip_locked=True)
            )
            row = session.scalar(statement)
            if row is None:
                return None
            row.status = "leased"
            row.attempt += 1
            row.lease_owner = worker_id
            row.heartbeat_at = current
            row.lease_expires_at = lease_expires_at
            row.updated_at = current
            session.flush()
        return JobLease(
            id=row.id,
            project_id=row.project_id,
            job_type=row.job_type,
            payload=dict(row.payload_json or {}),
            attempt=row.attempt,
            fencing_token=row.attempt,
            lease_expires_at=row.lease_expires_at,
        )

    def heartbeat(self, session: Session, *, job_id: str, worker_id: str, fencing_token: int, lease_seconds: int = 60) -> datetime:
        row = session.scalar(select(Job).where(Job.id == job_id).with_for_update())
        self._require_lease(row, worker_id, fencing_token)
        current = utcnow()
        row.heartbeat_at = current
        row.lease_expires_at = current + timedelta(seconds=lease_seconds)
        row.updated_at = current
        session.flush()
        return row.lease_expires_at

    def complete(self, session: Session, *, job_id: str, worker_id: str, fencing_token: int, result: dict[str, Any]) -> Job:
        row = session.scalar(select(Job).where(Job.id == job_id).with_for_update())
        self._require_lease(row, worker_id, fencing_token)
        row.status = "succeeded"
        row.result_json = result
        row.error = None
        row.lease_owner = None
        row.lease_expires_at = None
        row.updated_at = utcnow()
        session.flush()
        return row

    def fail(self, session: Session, *, job_id: str, worker_id: str, fencing_token: int, error: str) -> Job:
        row = session.scalar(select(Job).where(Job.id == job_id).with_for_update())
        self._require_lease(row, worker_id, fencing_token)
        row.error = error[:8000]
        row.lease_owner = None
        row.lease_expires_at = None
        row.updated_at = utcnow()
        if row.attempt >= row.max_attempts:
            row.status = "dead"
        else:
            row.status = "retry"
            delay = min(3600, 2 ** max(0, row.attempt - 1) * 15)
            row.available_at = utcnow() + timedelta(seconds=delay)
        session.flush()
        return row

    def reap_expired(self, session: Session) -> dict[str, int]:
        current = utcnow()
        rows = session.scalars(select(Job).where(
            Job.status == "leased",
            Job.lease_expires_at.is_not(None),
            Job.lease_expires_at <= current,
        ).with_for_update()).all()
        retried = 0
        dead = 0
        for row in rows:
            row.lease_owner = None
            row.lease_expires_at = None
            row.error = "Lease expired before completion"
            row.updated_at = current
            if row.attempt >= row.max_attempts:
                row.status = "dead"
                dead += 1
            else:
                row.status = "retry"
                row.available_at = current
                retried += 1
        session.flush()
        return {"requeued": retried, "dead": dead}

    @staticmethod
    def _require_lease(row: Job | None, worker_id: str, fencing_token: int) -> None:
        if row is None:
            raise KeyError("Job not found")
        if row.status != "leased" or row.lease_owner != worker_id or row.attempt != fencing_token:
            raise RuntimeError("Stale or foreign job lease")
        expires = _aware(row.lease_expires_at)
        if expires is None or expires <= utcnow():
            raise RuntimeError("Job lease has expired")
