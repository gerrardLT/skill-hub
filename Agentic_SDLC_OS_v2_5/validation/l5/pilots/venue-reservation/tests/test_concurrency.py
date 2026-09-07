from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor


def test_one_hundred_concurrent_requests_never_oversell(service):
    capacity = 10
    total = 100
    service.create_session("tenant-a", "rush-hour", "2026-09-05T19:30:00Z", capacity)

    def reserve(index: int):
        return service.reserve("tenant-a", "rush-hour", f"member-{index}", f"idem-{index}")[1]

    with ThreadPoolExecutor(max_workers=24) as pool:
        results = list(pool.map(reserve, range(total)))

    reserved = [item for item in results if item["outcome"] == "RESERVED"]
    waitlisted = [item for item in results if item["outcome"] == "WAITLISTED"]
    positions = sorted(item["queue_position"] for item in waitlisted)
    state = service.get_session("tenant-a", "rush-hour")

    assert len(reserved) == capacity
    assert len(waitlisted) == total - capacity
    assert positions == list(range(1, total - capacity + 1))
    assert state["reserved"] == capacity
    assert state["available"] == 0
    assert service.session_metrics("tenant-a", "rush-hour")["oversold"] is False


def test_concurrent_cancellations_promote_exact_fifo_count(service):
    capacity = 5
    service.create_session("tenant-a", "promotion", "2026-09-05T20:00:00Z", capacity)
    reservations = []
    for index in range(15):
        result = service.reserve("tenant-a", "promotion", f"member-{index}", f"r-{index}")[1]
        if result["outcome"] == "RESERVED":
            reservations.append(result["reservation_id"])

    def cancel(pair):
        index, reservation_id = pair
        return service.cancel("tenant-a", reservation_id, f"c-{index}")[1]

    with ThreadPoolExecutor(max_workers=5) as pool:
        results = list(pool.map(cancel, enumerate(reservations)))

    promoted = {item["promoted_member_id"] for item in results}
    assert promoted == {f"member-{index}" for index in range(5, 10)}
    state = service.get_session("tenant-a", "promotion")
    assert state["reserved"] == capacity
    assert state["waitlisted"] == 5
