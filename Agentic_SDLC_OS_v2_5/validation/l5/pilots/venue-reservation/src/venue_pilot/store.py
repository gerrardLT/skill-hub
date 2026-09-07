from __future__ import annotations

import json
import sqlite3
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Iterator

SCHEMA = """
PRAGMA foreign_keys = ON;
CREATE TABLE IF NOT EXISTS sessions (
    id TEXT PRIMARY KEY,
    tenant_id TEXT NOT NULL,
    starts_at TEXT NOT NULL,
    capacity INTEGER NOT NULL CHECK (capacity > 0),
    status TEXT NOT NULL CHECK (status IN ('OPEN', 'CLOSED', 'CANCELED')),
    created_at TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_sessions_tenant ON sessions(tenant_id, id);

CREATE TABLE IF NOT EXISTS reservations (
    id TEXT PRIMARY KEY,
    tenant_id TEXT NOT NULL,
    session_id TEXT NOT NULL REFERENCES sessions(id),
    member_id TEXT NOT NULL,
    status TEXT NOT NULL CHECK (status IN ('RESERVED', 'CANCELED')),
    created_at TEXT NOT NULL,
    canceled_at TEXT,
    promoted_from_waitlist_id TEXT
);
CREATE UNIQUE INDEX IF NOT EXISTS uniq_active_reservation
    ON reservations(session_id, member_id) WHERE status = 'RESERVED';
CREATE INDEX IF NOT EXISTS idx_reservation_session_status
    ON reservations(session_id, status);

CREATE TABLE IF NOT EXISTS waitlist_entries (
    id TEXT PRIMARY KEY,
    tenant_id TEXT NOT NULL,
    session_id TEXT NOT NULL REFERENCES sessions(id),
    member_id TEXT NOT NULL,
    status TEXT NOT NULL CHECK (status IN ('WAITLISTED', 'AUTO_PROMOTED', 'CANCELED', 'EXPIRED')),
    queue_seq INTEGER NOT NULL,
    created_at TEXT NOT NULL,
    promoted_at TEXT
);
CREATE UNIQUE INDEX IF NOT EXISTS uniq_active_waitlist
    ON waitlist_entries(session_id, member_id) WHERE status = 'WAITLISTED';
CREATE UNIQUE INDEX IF NOT EXISTS uniq_waitlist_sequence
    ON waitlist_entries(session_id, queue_seq);
CREATE INDEX IF NOT EXISTS idx_waitlist_fifo
    ON waitlist_entries(session_id, status, queue_seq);

CREATE TABLE IF NOT EXISTS idempotency_records (
    tenant_id TEXT NOT NULL,
    idempotency_key TEXT NOT NULL,
    request_hash TEXT NOT NULL,
    status_code INTEGER NOT NULL,
    response_json TEXT NOT NULL,
    created_at TEXT NOT NULL,
    PRIMARY KEY (tenant_id, idempotency_key)
);

CREATE TABLE IF NOT EXISTS audit_events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tenant_id TEXT NOT NULL,
    event_type TEXT NOT NULL,
    aggregate_type TEXT NOT NULL,
    aggregate_id TEXT NOT NULL,
    payload_json TEXT NOT NULL,
    created_at TEXT NOT NULL
);
"""


class SQLiteStore:
    def __init__(self, database: str | Path) -> None:
        self.database = str(database)
        Path(self.database).parent.mkdir(parents=True, exist_ok=True)
        self.initialize()

    def connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self.database, timeout=10.0, isolation_level=None, check_same_thread=False)
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys = ON")
        connection.execute("PRAGMA busy_timeout = 10000")
        connection.execute("PRAGMA journal_mode = WAL")
        return connection

    def initialize(self) -> None:
        with self.connect() as connection:
            connection.executescript(SCHEMA)

    @contextmanager
    def transaction(self) -> Iterator[sqlite3.Connection]:
        connection = self.connect()
        try:
            connection.execute("BEGIN IMMEDIATE")
            yield connection
            connection.execute("COMMIT")
        except Exception:
            connection.execute("ROLLBACK")
            raise
        finally:
            connection.close()

    @staticmethod
    def append_event(
        connection: sqlite3.Connection,
        *,
        tenant_id: str,
        event_type: str,
        aggregate_type: str,
        aggregate_id: str,
        payload: dict[str, Any],
        created_at: str,
    ) -> None:
        connection.execute(
            """
            INSERT INTO audit_events(
                tenant_id, event_type, aggregate_type, aggregate_id, payload_json, created_at
            ) VALUES (?, ?, ?, ?, ?, ?)
            """,
            (tenant_id, event_type, aggregate_type, aggregate_id, json.dumps(payload, sort_keys=True), created_at),
        )
