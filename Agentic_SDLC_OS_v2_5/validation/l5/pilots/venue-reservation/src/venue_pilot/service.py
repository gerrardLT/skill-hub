from __future__ import annotations

import hashlib
import json
import sqlite3
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .errors import DomainError
from .store import SQLiteStore


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def stable_hash(payload: dict[str, Any]) -> str:
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def new_id(prefix: str) -> str:
    return f"{prefix}_{uuid.uuid4().hex}"


class ReservationService:
    def __init__(self, database: str | Path) -> None:
        self.store = SQLiteStore(database)

    @staticmethod
    def _require_tenant(tenant_id: str) -> str:
        tenant_id = tenant_id.strip()
        if not tenant_id or len(tenant_id) > 80:
            raise DomainError("INVALID_TENANT", "A valid tenant identifier is required.", 400)
        return tenant_id

    @staticmethod
    def _load_idempotent(
        connection: sqlite3.Connection,
        tenant_id: str,
        key: str,
        request_hash: str,
    ) -> tuple[int, dict[str, Any]] | None:
        row = connection.execute(
            "SELECT request_hash, status_code, response_json FROM idempotency_records WHERE tenant_id = ? AND idempotency_key = ?",
            (tenant_id, key),
        ).fetchone()
        if row is None:
            return None
        if row["request_hash"] != request_hash:
            raise DomainError(
                "IDEMPOTENCY_CONFLICT",
                "The idempotency key was already used for a different request.",
                409,
                next_action="Use the original payload or provide a new idempotency key.",
            )
        return int(row["status_code"]), json.loads(row["response_json"])

    @staticmethod
    def _save_idempotent(
        connection: sqlite3.Connection,
        tenant_id: str,
        key: str,
        request_hash: str,
        status_code: int,
        response: dict[str, Any],
        created_at: str,
    ) -> None:
        connection.execute(
            """
            INSERT INTO idempotency_records(
                tenant_id, idempotency_key, request_hash, status_code, response_json, created_at
            ) VALUES (?, ?, ?, ?, ?, ?)
            """,
            (tenant_id, key, request_hash, status_code, json.dumps(response, sort_keys=True), created_at),
        )

    def create_session(self, tenant_id: str, session_id: str, starts_at: str, capacity: int) -> dict[str, Any]:
        tenant_id = self._require_tenant(tenant_id)
        created_at = utc_now()
        try:
            with self.store.transaction() as connection:
                connection.execute(
                    "INSERT INTO sessions(id, tenant_id, starts_at, capacity, status, created_at) VALUES (?, ?, ?, ?, 'OPEN', ?)",
                    (session_id, tenant_id, starts_at, int(capacity), created_at),
                )
                self.store.append_event(
                    connection,
                    tenant_id=tenant_id,
                    event_type="SESSION_OPENED",
                    aggregate_type="session",
                    aggregate_id=session_id,
                    payload={"capacity": int(capacity), "starts_at": starts_at},
                    created_at=created_at,
                )
        except sqlite3.IntegrityError as exc:
            raise DomainError("SESSION_CONFLICT", "The session already exists or is invalid.", 409) from exc
        return self.get_session(tenant_id, session_id)

    def get_session(self, tenant_id: str, session_id: str) -> dict[str, Any]:
        tenant_id = self._require_tenant(tenant_id)
        with self.store.connect() as connection:
            row = connection.execute(
                "SELECT id, tenant_id, starts_at, capacity, status FROM sessions WHERE id = ? AND tenant_id = ?",
                (session_id, tenant_id),
            ).fetchone()
            if row is None:
                raise DomainError("SESSION_NOT_FOUND", "The session does not exist for this tenant.", 404)
            reserved = int(connection.execute(
                "SELECT COUNT(*) FROM reservations WHERE session_id = ? AND status = 'RESERVED'",
                (session_id,),
            ).fetchone()[0])
            waitlisted = int(connection.execute(
                "SELECT COUNT(*) FROM waitlist_entries WHERE session_id = ? AND status = 'WAITLISTED'",
                (session_id,),
            ).fetchone()[0])
        return {
            "session_id": row["id"],
            "tenant_id": row["tenant_id"],
            "status": row["status"],
            "capacity": int(row["capacity"]),
            "reserved": reserved,
            "available": max(int(row["capacity"]) - reserved, 0),
            "waitlisted": waitlisted,
            "starts_at": row["starts_at"],
        }

    def reserve(self, tenant_id: str, session_id: str, member_id: str, idempotency_key: str) -> tuple[int, dict[str, Any]]:
        tenant_id = self._require_tenant(tenant_id)
        if not idempotency_key.strip() or len(idempotency_key) > 120:
            raise DomainError("INVALID_IDEMPOTENCY_KEY", "A non-empty idempotency key is required.", 400)
        payload = {"operation": "reserve", "session_id": session_id, "member_id": member_id}
        request_hash = stable_hash(payload)
        created_at = utc_now()
        try:
            with self.store.transaction() as connection:
                cached = self._load_idempotent(connection, tenant_id, idempotency_key, request_hash)
                if cached is not None:
                    return cached
                session = connection.execute(
                    "SELECT id, tenant_id, capacity, status FROM sessions WHERE id = ? AND tenant_id = ?",
                    (session_id, tenant_id),
                ).fetchone()
                if session is None:
                    raise DomainError("SESSION_NOT_FOUND", "The session does not exist for this tenant.", 404)
                if session["status"] != "OPEN":
                    raise DomainError("SESSION_NOT_OPEN", "The session is not open for reservations.", 409)
                if connection.execute(
                    "SELECT 1 FROM reservations WHERE session_id = ? AND member_id = ? AND status = 'RESERVED'",
                    (session_id, member_id),
                ).fetchone():
                    raise DomainError(
                        "ALREADY_RESERVED",
                        "The member already has an active reservation for this session.",
                        409,
                        next_action="Open the existing reservation instead of submitting again.",
                    )
                if connection.execute(
                    "SELECT 1 FROM waitlist_entries WHERE session_id = ? AND member_id = ? AND status = 'WAITLISTED'",
                    (session_id, member_id),
                ).fetchone():
                    raise DomainError(
                        "ALREADY_WAITLISTED",
                        "The member is already on the waitlist for this session.",
                        409,
                        next_action="Open the existing waitlist entry to view the current position.",
                    )
                reserved = int(connection.execute(
                    "SELECT COUNT(*) FROM reservations WHERE session_id = ? AND status = 'RESERVED'",
                    (session_id,),
                ).fetchone()[0])
                if reserved < int(session["capacity"]):
                    reservation_id = new_id("res")
                    connection.execute(
                        """
                        INSERT INTO reservations(id, tenant_id, session_id, member_id, status, created_at)
                        VALUES (?, ?, ?, ?, 'RESERVED', ?)
                        """,
                        (reservation_id, tenant_id, session_id, member_id, created_at),
                    )
                    response = {
                        "outcome": "RESERVED",
                        "session_id": session_id,
                        "member_id": member_id,
                        "reservation_id": reservation_id,
                        "waitlist_id": None,
                        "queue_position": None,
                        "promoted_member_id": None,
                        "promoted_reservation_id": None,
                        "message": "Reservation confirmed. The capacity was atomically allocated.",
                    }
                    status_code = 201
                    event_type = "RESERVATION_CONFIRMED"
                    aggregate_id = reservation_id
                else:
                    next_seq = int(connection.execute(
                        "SELECT COALESCE(MAX(queue_seq), 0) + 1 FROM waitlist_entries WHERE session_id = ?",
                        (session_id,),
                    ).fetchone()[0])
                    waitlist_id = new_id("wait")
                    connection.execute(
                        """
                        INSERT INTO waitlist_entries(
                            id, tenant_id, session_id, member_id, status, queue_seq, created_at
                        ) VALUES (?, ?, ?, ?, 'WAITLISTED', ?, ?)
                        """,
                        (waitlist_id, tenant_id, session_id, member_id, next_seq, created_at),
                    )
                    active_ahead = int(connection.execute(
                        """
                        SELECT COUNT(*) FROM waitlist_entries
                        WHERE session_id = ? AND status = 'WAITLISTED' AND queue_seq <= ?
                        """,
                        (session_id, next_seq),
                    ).fetchone()[0])
                    response = {
                        "outcome": "WAITLISTED",
                        "session_id": session_id,
                        "member_id": member_id,
                        "reservation_id": None,
                        "waitlist_id": waitlist_id,
                        "queue_position": active_ahead,
                        "promoted_member_id": None,
                        "promoted_reservation_id": None,
                        "message": f"Session is full. Added to the FIFO waitlist at position {active_ahead}.",
                    }
                    status_code = 202
                    event_type = "WAITLIST_JOINED"
                    aggregate_id = waitlist_id
                self.store.append_event(
                    connection,
                    tenant_id=tenant_id,
                    event_type=event_type,
                    aggregate_type="reservation",
                    aggregate_id=aggregate_id,
                    payload=response,
                    created_at=created_at,
                )
                self._save_idempotent(
                    connection, tenant_id, idempotency_key, request_hash, status_code, response, created_at
                )
                return status_code, response
        except sqlite3.IntegrityError as exc:
            raise DomainError(
                "CONCURRENT_CONFLICT",
                "A concurrent request changed the reservation state.",
                409,
                next_action="Refresh the session state and retry with a new idempotency key.",
            ) from exc

    def cancel(self, tenant_id: str, reservation_id: str, idempotency_key: str) -> tuple[int, dict[str, Any]]:
        tenant_id = self._require_tenant(tenant_id)
        if not idempotency_key.strip() or len(idempotency_key) > 120:
            raise DomainError("INVALID_IDEMPOTENCY_KEY", "A non-empty idempotency key is required.", 400)
        payload = {"operation": "cancel", "reservation_id": reservation_id}
        request_hash = stable_hash(payload)
        timestamp = utc_now()
        with self.store.transaction() as connection:
            cached = self._load_idempotent(connection, tenant_id, idempotency_key, request_hash)
            if cached is not None:
                return cached
            reservation = connection.execute(
                """
                SELECT id, tenant_id, session_id, member_id, status
                FROM reservations WHERE id = ? AND tenant_id = ?
                """,
                (reservation_id, tenant_id),
            ).fetchone()
            if reservation is None:
                raise DomainError("RESERVATION_NOT_FOUND", "The reservation does not exist for this tenant.", 404)
            if reservation["status"] == "CANCELED":
                response = {
                    "outcome": "CANCELED",
                    "session_id": reservation["session_id"],
                    "member_id": reservation["member_id"],
                    "reservation_id": reservation_id,
                    "waitlist_id": None,
                    "queue_position": None,
                    "promoted_member_id": None,
                    "promoted_reservation_id": None,
                    "message": "Reservation was already canceled. No additional state change was made.",
                }
                self._save_idempotent(connection, tenant_id, idempotency_key, request_hash, 200, response, timestamp)
                return 200, response
            connection.execute(
                "UPDATE reservations SET status = 'CANCELED', canceled_at = ? WHERE id = ?",
                (timestamp, reservation_id),
            )
            waitlist = connection.execute(
                """
                SELECT id, member_id, queue_seq FROM waitlist_entries
                WHERE session_id = ? AND tenant_id = ? AND status = 'WAITLISTED'
                ORDER BY queue_seq ASC LIMIT 1
                """,
                (reservation["session_id"], tenant_id),
            ).fetchone()
            promoted_member_id = None
            promoted_reservation_id = None
            if waitlist is not None:
                promoted_member_id = waitlist["member_id"]
                promoted_reservation_id = new_id("res")
                connection.execute(
                    "UPDATE waitlist_entries SET status = 'AUTO_PROMOTED', promoted_at = ? WHERE id = ?",
                    (timestamp, waitlist["id"]),
                )
                connection.execute(
                    """
                    INSERT INTO reservations(
                        id, tenant_id, session_id, member_id, status, created_at, promoted_from_waitlist_id
                    ) VALUES (?, ?, ?, ?, 'RESERVED', ?, ?)
                    """,
                    (
                        promoted_reservation_id,
                        tenant_id,
                        reservation["session_id"],
                        promoted_member_id,
                        timestamp,
                        waitlist["id"],
                    ),
                )
                self.store.append_event(
                    connection,
                    tenant_id=tenant_id,
                    event_type="WAITLIST_AUTO_PROMOTED",
                    aggregate_type="waitlist",
                    aggregate_id=waitlist["id"],
                    payload={
                        "session_id": reservation["session_id"],
                        "member_id": promoted_member_id,
                        "reservation_id": promoted_reservation_id,
                        "queue_seq": int(waitlist["queue_seq"]),
                    },
                    created_at=timestamp,
                )
            response = {
                "outcome": "CANCELED",
                "session_id": reservation["session_id"],
                "member_id": reservation["member_id"],
                "reservation_id": reservation_id,
                "waitlist_id": None,
                "queue_position": None,
                "promoted_member_id": promoted_member_id,
                "promoted_reservation_id": promoted_reservation_id,
                "message": "Reservation canceled and the earliest eligible waitlist entry was promoted." if waitlist else "Reservation canceled; no active waitlist entry required promotion.",
            }
            self.store.append_event(
                connection,
                tenant_id=tenant_id,
                event_type="RESERVATION_CANCELED",
                aggregate_type="reservation",
                aggregate_id=reservation_id,
                payload=response,
                created_at=timestamp,
            )
            self._save_idempotent(connection, tenant_id, idempotency_key, request_hash, 200, response, timestamp)
            return 200, response

    def session_metrics(self, tenant_id: str, session_id: str) -> dict[str, Any]:
        state = self.get_session(tenant_id, session_id)
        with self.store.connect() as connection:
            joined = int(connection.execute(
                "SELECT COUNT(*) FROM waitlist_entries WHERE session_id = ?",
                (session_id,),
            ).fetchone()[0])
            promotions = int(connection.execute(
                "SELECT COUNT(*) FROM waitlist_entries WHERE session_id = ? AND status = 'AUTO_PROMOTED'",
                (session_id,),
            ).fetchone()[0])
            cancellations = int(connection.execute(
                "SELECT COUNT(*) FROM reservations WHERE session_id = ? AND status = 'CANCELED'",
                (session_id,),
            ).fetchone()[0])
            event_count = int(connection.execute(
                "SELECT COUNT(*) FROM audit_events WHERE aggregate_id = ? OR json_extract(payload_json, '$.session_id') = ?",
                (session_id, session_id),
            ).fetchone()[0])
        return {
            **state,
            "waitlist_joined_total": joined,
            "waitlist_promotions_total": promotions,
            "waitlist_conversion_rate": round(promotions / joined, 6) if joined else 0.0,
            "cancellations_total": cancellations,
            "oversold": state["reserved"] > state["capacity"],
            "audit_events": event_count,
        }
