from __future__ import annotations

from venue_pilot.errors import DomainError


def create_session(service, capacity: int = 2, tenant: str = "tenant-a", session: str = "session-1"):
    return service.create_session(tenant, session, "2026-09-05T19:30:00Z", capacity)


def test_capacity_waitlist_and_fifo_promotion(service):
    create_session(service, capacity=2)
    status_1, first = service.reserve("tenant-a", "session-1", "member-1", "reserve-1")
    status_2, second = service.reserve("tenant-a", "session-1", "member-2", "reserve-2")
    status_3, third = service.reserve("tenant-a", "session-1", "member-3", "reserve-3")
    status_4, fourth = service.reserve("tenant-a", "session-1", "member-4", "reserve-4")

    assert (status_1, status_2, status_3, status_4) == (201, 201, 202, 202)
    assert first["outcome"] == "RESERVED"
    assert second["outcome"] == "RESERVED"
    assert third["queue_position"] == 1
    assert fourth["queue_position"] == 2

    cancel_status, canceled = service.cancel("tenant-a", first["reservation_id"], "cancel-1")
    assert cancel_status == 200
    assert canceled["promoted_member_id"] == "member-3"

    state = service.get_session("tenant-a", "session-1")
    metrics = service.session_metrics("tenant-a", "session-1")
    assert state["reserved"] == 2
    assert state["waitlisted"] == 1
    assert metrics["waitlist_promotions_total"] == 1
    assert metrics["oversold"] is False


def test_idempotency_replays_same_result(service):
    create_session(service, capacity=1)
    first_status, first = service.reserve("tenant-a", "session-1", "member-1", "same-key")
    second_status, second = service.reserve("tenant-a", "session-1", "member-1", "same-key")
    assert first_status == second_status == 201
    assert first == second


def test_idempotency_key_cannot_be_reused_for_different_payload(service):
    create_session(service, capacity=2)
    service.reserve("tenant-a", "session-1", "member-1", "same-key")
    try:
        service.reserve("tenant-a", "session-1", "member-2", "same-key")
    except DomainError as exc:
        assert exc.code == "IDEMPOTENCY_CONFLICT"
        assert exc.status_code == 409
    else:
        raise AssertionError("Expected idempotency conflict")


def test_member_cannot_hold_reservation_and_waitlist_duplicate(service):
    create_session(service, capacity=1)
    service.reserve("tenant-a", "session-1", "member-1", "key-1")
    try:
        service.reserve("tenant-a", "session-1", "member-1", "key-2")
    except DomainError as exc:
        assert exc.code == "ALREADY_RESERVED"
    else:
        raise AssertionError("Expected duplicate reservation rejection")


def test_tenant_isolation(service):
    create_session(service, capacity=1, tenant="tenant-a", session="shared-name")
    try:
        service.get_session("tenant-b", "shared-name")
    except DomainError as exc:
        assert exc.code == "SESSION_NOT_FOUND"
        assert exc.status_code == 404
    else:
        raise AssertionError("Expected tenant isolation")
