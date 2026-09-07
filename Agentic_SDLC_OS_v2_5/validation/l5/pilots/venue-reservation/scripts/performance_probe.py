#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import math
import tempfile
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from venue_pilot.service import ReservationService


def percentile(values: list[float], fraction: float) -> float:
    ordered = sorted(values)
    index = min(len(ordered) - 1, max(0, math.ceil(len(ordered) * fraction) - 1))
    return ordered[index]


def run(total: int, capacity: int, workers: int) -> dict:
    with tempfile.TemporaryDirectory() as tmp:
        service = ReservationService(Path(tmp) / "probe.db")
        service.create_session("tenant-a", "probe", "2026-09-05T19:30:00Z", capacity)

        def reserve(index: int):
            started = time.perf_counter()
            status, payload = service.reserve("tenant-a", "probe", f"member-{index}", f"probe-{index}")
            return (time.perf_counter() - started) * 1000.0, status, payload["outcome"]

        wall_started = time.perf_counter()
        with ThreadPoolExecutor(max_workers=workers) as pool:
            rows = list(pool.map(reserve, range(total)))
        wall_seconds = time.perf_counter() - wall_started
        latencies = [row[0] for row in rows]
        outcomes = [row[2] for row in rows]
        metrics = service.session_metrics("tenant-a", "probe")
        return {
            "requests": total,
            "capacity": capacity,
            "workers": workers,
            "wall_seconds": round(wall_seconds, 6),
            "throughput_rps": round(total / wall_seconds, 3),
            "latency_ms": {
                "min": round(min(latencies), 3),
                "p50": round(percentile(latencies, 0.50), 3),
                "p95": round(percentile(latencies, 0.95), 3),
                "p99": round(percentile(latencies, 0.99), 3),
                "max": round(max(latencies), 3),
            },
            "reserved": outcomes.count("RESERVED"),
            "waitlisted": outcomes.count("WAITLISTED"),
            "oversold": metrics["oversold"],
            "audit_events": metrics["audit_events"],
        }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--requests", type=int, default=200)
    parser.add_argument("--capacity", type=int, default=20)
    parser.add_argument("--workers", type=int, default=32)
    parser.add_argument("--output")
    args = parser.parse_args()
    result = run(args.requests, args.capacity, args.workers)
    encoded = json.dumps(result, indent=2, sort_keys=True)
    if args.output:
        path = Path(args.output)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(encoded + "\n", encoding="utf-8")
    print(encoded)
    return 0 if not result["oversold"] and result["reserved"] == args.capacity else 1


if __name__ == "__main__":
    raise SystemExit(main())
