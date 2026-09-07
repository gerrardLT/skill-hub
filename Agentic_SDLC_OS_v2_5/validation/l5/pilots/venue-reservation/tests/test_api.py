from __future__ import annotations

TENANT_HEADERS = {"X-Tenant-ID": "tenant-a"}


def test_api_end_to_end(client):
    response = client.post(
        "/v1/sessions",
        headers=TENANT_HEADERS,
        json={"session_id": "evening-1", "starts_at": "2026-09-05T19:30:00Z", "capacity": 1},
    )
    assert response.status_code == 201
    assert response.json()["available"] == 1

    reserved = client.post(
        "/v1/sessions/evening-1/reservations",
        headers={**TENANT_HEADERS, "Idempotency-Key": "r-1"},
        json={"member_id": "member-1"},
    )
    waitlisted = client.post(
        "/v1/sessions/evening-1/reservations",
        headers={**TENANT_HEADERS, "Idempotency-Key": "r-2"},
        json={"member_id": "member-2"},
    )
    assert reserved.status_code == 201
    assert waitlisted.status_code == 202
    assert waitlisted.json()["queue_position"] == 1

    canceled = client.delete(
        f"/v1/reservations/{reserved.json()['reservation_id']}",
        headers={**TENANT_HEADERS, "Idempotency-Key": "c-1"},
    )
    assert canceled.status_code == 200
    assert canceled.json()["promoted_member_id"] == "member-2"

    metrics = client.get("/v1/sessions/evening-1/metrics", headers=TENANT_HEADERS)
    assert metrics.status_code == 200
    payload = metrics.json()
    assert payload["oversold"] is False
    assert payload["reserved"] == 1
    assert payload["waitlist_promotions_total"] == 1


def test_error_contract_contains_next_action(client):
    response = client.post(
        "/v1/sessions/missing/reservations",
        headers={**TENANT_HEADERS, "Idempotency-Key": "missing-1"},
        json={"member_id": "member-1"},
    )
    assert response.status_code == 404
    assert response.json()["error"]["code"] == "SESSION_NOT_FOUND"
    assert response.json()["error"]["next_action"]


def test_validation_rejects_unsafe_identifier(client):
    response = client.post(
        "/v1/sessions",
        headers=TENANT_HEADERS,
        json={"session_id": "../escape", "starts_at": "2026-09-05T19:30:00Z", "capacity": 1},
    )
    assert response.status_code == 422
