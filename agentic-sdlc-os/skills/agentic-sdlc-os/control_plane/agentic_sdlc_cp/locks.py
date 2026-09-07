from __future__ import annotations

import hashlib
import time
from contextlib import contextmanager
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Generator

from sqlalchemy import delete, select, text
from sqlalchemy.exc import IntegrityError

from .db import Database
from .models import Lease, utcnow


@dataclass(frozen=True)
class LeaseToken:
    resource_key: str
    owner: str
    fencing_token: int
    expires_at: datetime


def _aware(value: datetime) -> datetime:
    return value if value.tzinfo is not None else value.replace(tzinfo=timezone.utc)


class LeaseLockManager:
    """Database-backed distributed leases with fencing tokens.

    PostgreSQL row locks serialize contenders. SQLite is supported for local tests.
    Fencing tokens must be checked by any external side effect that can outlive a lease.
    """

    def __init__(self, database: Database):
        self.database = database

    def acquire(
        self,
        resource_key: str,
        owner: str,
        *,
        ttl_seconds: float = 30.0,
        wait_seconds: float = 5.0,
    ) -> LeaseToken:
        deadline = time.monotonic() + wait_seconds
        while True:
            try:
                with self.database.session() as session:
                    row = session.scalar(
                        select(Lease).where(Lease.resource_key == resource_key).with_for_update()
                    )
                    current = utcnow()
                    expires = current + timedelta(seconds=ttl_seconds)
                    if row is None:
                        row = Lease(
                            resource_key=resource_key,
                            owner=owner,
                            fencing_token=1,
                            lease_expires_at=expires,
                        )
                        session.add(row)
                        session.flush()
                        return LeaseToken(resource_key, owner, 1, expires)
                    if row.owner == owner or _aware(row.lease_expires_at) <= current:
                        row.owner = owner
                        row.fencing_token += 1
                        row.lease_expires_at = expires
                        row.updated_at = current
                        session.flush()
                        return LeaseToken(resource_key, owner, row.fencing_token, expires)
            except IntegrityError:
                pass
            if time.monotonic() >= deadline:
                raise TimeoutError(f"Could not acquire lease: {resource_key}")
            time.sleep(0.05)

    def renew(self, token: LeaseToken, *, ttl_seconds: float = 30.0) -> LeaseToken:
        with self.database.session() as session:
            row = session.scalar(select(Lease).where(Lease.resource_key == token.resource_key).with_for_update())
            if row is None or row.owner != token.owner or row.fencing_token != token.fencing_token:
                raise RuntimeError("Lease is no longer owned by this token")
            expires = utcnow() + timedelta(seconds=ttl_seconds)
            row.lease_expires_at = expires
            row.updated_at = utcnow()
            session.flush()
            return LeaseToken(token.resource_key, token.owner, token.fencing_token, expires)

    def release(self, token: LeaseToken) -> bool:
        with self.database.session() as session:
            row = session.scalar(select(Lease).where(Lease.resource_key == token.resource_key).with_for_update())
            if row is None:
                return False
            if row.owner != token.owner or row.fencing_token != token.fencing_token:
                return False
            session.delete(row)
            return True

    def reap_expired(self) -> int:
        with self.database.session() as session:
            result = session.execute(delete(Lease).where(Lease.lease_expires_at <= utcnow()))
            return int(result.rowcount or 0)

    @contextmanager
    def lock(self, resource_key: str, owner: str, *, ttl_seconds: float = 30.0, wait_seconds: float = 5.0) -> Generator[LeaseToken, None, None]:
        token = self.acquire(resource_key, owner, ttl_seconds=ttl_seconds, wait_seconds=wait_seconds)
        try:
            yield token
        finally:
            self.release(token)


class PostgresAdvisoryLock:
    """Optional session-scoped PostgreSQL advisory lock for short critical sections."""

    def __init__(self, database: Database):
        self.database = database

    @staticmethod
    def _key(resource_key: str) -> int:
        raw = hashlib.sha256(resource_key.encode("utf-8")).digest()[:8]
        return int.from_bytes(raw, "big", signed=True)

    @contextmanager
    def lock(self, resource_key: str) -> Generator[None, None, None]:
        if self.database.engine.dialect.name != "postgresql":
            raise RuntimeError("PostgreSQL advisory locks require a PostgreSQL database")
        connection = self.database.engine.connect()
        transaction = connection.begin()
        key = self._key(resource_key)
        try:
            connection.execute(text("SELECT pg_advisory_xact_lock(:key)"), {"key": key})
            yield
            transaction.commit()
        except Exception:
            transaction.rollback()
            raise
        finally:
            connection.close()
