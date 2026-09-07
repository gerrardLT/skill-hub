from __future__ import annotations

import json


def test_audit_events_are_immutable_and_specific(service):
    service.create_session("tenant-a", "audit-session", "2026-09-05T18:00:00Z", 1)
    _, reservation = service.reserve("tenant-a", "audit-session", "member-1", "audit-r1")
    service.reserve("tenant-a", "audit-session", "member-2", "audit-r2")
    service.cancel("tenant-a", reservation["reservation_id"], "audit-c1")

    with service.store.connect() as connection:
        rows = connection.execute(
            "SELECT event_type, payload_json FROM audit_events ORDER BY id"
        ).fetchall()
    types = [row["event_type"] for row in rows]
    assert types == [
        "SESSION_OPENED",
        "RESERVATION_CONFIRMED",
        "WAITLIST_JOINED",
        "WAITLIST_AUTO_PROMOTED",
        "RESERVATION_CANCELED",
    ]
    for row in rows:
        payload = json.loads(row["payload_json"])
        assert isinstance(payload, dict)
        assert payload
