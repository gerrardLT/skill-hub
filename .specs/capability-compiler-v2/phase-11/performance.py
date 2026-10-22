#!/usr/bin/env python3
"""Measure BenchShare local latency and ten-way approval integrity."""
from __future__ import annotations

import argparse
import concurrent.futures
import hashlib
import http.cookiejar
import json
import socket
import sqlite3
import statistics
import subprocess
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any


def now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def free_port() -> int:
    with socket.socket() as sock:
        sock.bind(("127.0.0.1", 0))
        return int(sock.getsockname()[1])


def percentile(values: list[float], fraction: float) -> float:
    ordered = sorted(values)
    rank = max(0, min(len(ordered) - 1, int((len(ordered) * fraction + 0.999999) - 1)))
    return ordered[rank]


def summarize(values: list[float]) -> dict[str, float]:
    return {
        "runs": len(values),
        "min_ms": round(min(values), 3),
        "median_ms": round(statistics.median(values), 3),
        "p95_ms": round(percentile(values, 0.95), 3),
        "max_ms": round(max(values), 3),
        "spread_ms": round(max(values) - min(values), 3),
    }


def session(base: str, actor_id: int):
    jar = http.cookiejar.CookieJar()
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(jar))
    request = urllib.request.Request(
        base + "/api/session",
        data=json.dumps({"actor_id": actor_id}).encode(),
        method="POST",
        headers={"Content-Type": "application/json", "Origin": base},
    )
    response = opener.open(request, timeout=5)
    return opener, json.loads(response.read())["csrf"]


def call(opener, base: str, method: str, path: str, body=None, headers=None):
    data = None if body is None else json.dumps(body).encode()
    values = headers or {}
    if body is not None:
        values = {"Content-Type": "application/json", **values}
    request = urllib.request.Request(base + path, data=data, method=method, headers=values)
    start = time.perf_counter()
    try:
        response = opener.open(request, timeout=10)
    except urllib.error.HTTPError as error:
        response = error
    raw = response.read()
    return response.status, json.loads(raw) if raw else None, (time.perf_counter() - start) * 1000


def future(hours: int) -> str:
    return (datetime.now(timezone.utc) + timedelta(hours=hours)).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workspace", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--runtime-tree", required=True)
    args = parser.parse_args()
    workspace, out = args.workspace.resolve(), args.out.resolve()
    out.mkdir(parents=True, exist_ok=False)
    port = free_port()
    base = f"http://127.0.0.1:{port}"
    db, ready = out / "performance.db", out / "ready.json"
    stdout = (out / "server-stdout.txt").open("w", encoding="utf-8")
    stderr = (out / "server-stderr.txt").open("w", encoding="utf-8")
    server = subprocess.Popen(
        [sys.executable, "-m", "benchshare", "--host", "127.0.0.1", "--port", str(port), "--db", str(db), "--ready-file", str(ready)],
        cwd=workspace, stdout=stdout, stderr=stderr, text=True,
    )
    deadline = time.monotonic() + 10
    while time.monotonic() < deadline and not ready.exists() and server.poll() is None:
        time.sleep(0.05)
    if not ready.exists():
        raise RuntimeError("server readiness failed")

    thresholds = {"health_p95_ms": 100.0, "list_p95_ms": 100.0, "create_p95_ms": 250.0, "concurrent_attempts": 10, "approved": 1, "conflicts": 9, "server_errors": 0}
    started = now()
    try:
        plain = urllib.request.build_opener()
        member, member_csrf = session(base, 1)
        coordinator, coordinator_csrf = session(base, 3)
        # Warm up paths before timed matched runs.
        for _ in range(5):
            call(plain, base, "GET", "/health")
            call(member, base, "GET", "/api/reservations")

        health_ms, list_ms, create_ms = [], [], []
        for _ in range(50):
            status, _, elapsed = call(plain, base, "GET", "/health")
            assert status == 200
            health_ms.append(elapsed)
        for _ in range(50):
            status, _, elapsed = call(member, base, "GET", "/api/reservations")
            assert status == 200
            list_ms.append(elapsed)
        for index in range(20):
            payload = {"equipment_id": 4, "start_at": future(24 + index * 2), "end_at": future(25 + index * 2), "purpose": f"Performance write {index}", "training_ack": True}
            status, created, elapsed = call(member, base, "POST", "/api/reservations", payload, {"Origin": base, "X-CSRF-Token": member_csrf, "Idempotency-Key": f"perf-{index}"})
            assert status == 201, created
            create_ms.append(elapsed)

        overlap = {"equipment_id": 1, "start_at": future(72), "end_at": future(73), "purpose": "Ten-way approval integrity", "training_ack": True}
        pending_ids = []
        for index in range(10):
            actor = 1 if index % 2 == 0 else 2
            opener, csrf = session(base, actor)
            status, created, _ = call(opener, base, "POST", "/api/reservations", overlap, {"Origin": base, "X-CSRF-Token": csrf, "Idempotency-Key": f"concurrency-{index}"})
            assert status == 201, created
            pending_ids.append(created["reservation"]["id"])

        def approve(reservation_id: int):
            opener, csrf = session(base, 3)
            status, body, elapsed = call(opener, base, "POST", f"/api/reservations/{reservation_id}/approve", {}, {"Origin": base, "X-CSRF-Token": csrf})
            return {"reservation_id": reservation_id, "status": status, "code": "ok" if status == 200 else body["error"]["code"], "duration_ms": round(elapsed, 3)}

        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as pool:
            outcomes = list(pool.map(approve, pending_ids))
        approved = sum(item["status"] == 200 for item in outcomes)
        conflicts = sum(item["status"] == 409 and item["code"] == "booking_conflict" for item in outcomes)
        server_errors = sum(item["status"] >= 500 for item in outcomes)
        with sqlite3.connect(db) as connection:
            approved_rows = connection.execute("SELECT COUNT(*) FROM reservations WHERE equipment_id=1 AND status='approved' AND start_at=? AND end_at=?", (overlap["start_at"], overlap["end_at"])).fetchone()[0]
            integrity = connection.execute("PRAGMA integrity_check").fetchone()[0]
            audit_count = connection.execute("SELECT COUNT(*) FROM audit_events WHERE action='reservation.approve'").fetchone()[0]

        metrics = {"health": summarize(health_ms), "reservation_list": summarize(list_ms), "reservation_create": summarize(create_ms)}
        checks = {
            "health_p95": metrics["health"]["p95_ms"] <= thresholds["health_p95_ms"],
            "list_p95": metrics["reservation_list"]["p95_ms"] <= thresholds["list_p95_ms"],
            "create_p95": metrics["reservation_create"]["p95_ms"] <= thresholds["create_p95_ms"],
            "ten_attempts": len(outcomes) == thresholds["concurrent_attempts"],
            "one_approved_response": approved == thresholds["approved"],
            "nine_conflicts": conflicts == thresholds["conflicts"],
            "zero_500": server_errors == thresholds["server_errors"],
            "one_approved_row": approved_rows == 1,
            "one_approval_audit": audit_count == 1,
            "integrity_ok": integrity == "ok",
        }
        report = {
            "schema_version": "2.0", "case_id": "benchshare-v1", "started_at": started, "ended_at": now(),
            "runtime_tree_sha256": args.runtime_tree, "environment": {"python": sys.version, "host": "local-loopback", "processes": 1, "database": "SQLite"},
            "method": {"warmups_per_read_path": 5, "health_runs": 50, "list_runs": 50, "isolated_create_runs": 20, "concurrent_approval_attempts": 10, "percentile": "nearest-rank", "claim_boundary": "local validation only"},
            "thresholds": thresholds, "metrics": metrics, "concurrency": {"outcomes": outcomes, "approved_responses": approved, "conflicts": conflicts, "server_errors": server_errors, "approved_rows": approved_rows, "approval_audit_events": audit_count, "integrity_check": integrity},
            "checks": checks, "passed": all(checks.values()), "failed_runs_deleted": 0, "remote_actions": [],
        }
        (out / "report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
        print(json.dumps({"passed": report["passed"], "metrics": metrics, "concurrency": {key: report["concurrency"][key] for key in ["approved_responses", "conflicts", "server_errors", "approved_rows"]}}, sort_keys=True))
        return 0 if report["passed"] else 1
    finally:
        server.terminate()
        try:
            server.wait(timeout=5)
        except subprocess.TimeoutExpired:
            server.kill()
        stdout.close(); stderr.close()


if __name__ == "__main__":
    raise SystemExit(main())
