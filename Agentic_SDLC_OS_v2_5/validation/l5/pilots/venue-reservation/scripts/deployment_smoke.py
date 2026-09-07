#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import socket
import subprocess
import sys
import tempfile
import time
import urllib.error
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any


def free_port() -> int:
    with socket.socket() as sock:
        sock.bind(("127.0.0.1", 0))
        return int(sock.getsockname()[1])


def request(base: str, method: str, path: str, *, tenant: str | None = None, key: str | None = None, body: dict[str, Any] | None = None) -> tuple[int, dict[str, Any]]:
    headers = {"Accept": "application/json"}
    if tenant:
        headers["X-Tenant-Id"] = tenant
    if key:
        headers["Idempotency-Key"] = key
    data = None
    if body is not None:
        headers["Content-Type"] = "application/json"
        data = json.dumps(body).encode("utf-8")
    req = urllib.request.Request(base + path, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=5) as response:
            return response.status, json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        payload = json.loads(exc.read().decode("utf-8"))
        return exc.code, payload


def wait_for_health(base: str, timeout: float = 12.0) -> dict[str, Any]:
    deadline = time.monotonic() + timeout
    last_error = "not started"
    while time.monotonic() < deadline:
        try:
            status, payload = request(base, "GET", "/health")
            if status == 200 and payload.get("status") == "ok":
                return payload
        except Exception as exc:  # noqa: BLE001
            last_error = str(exc)
        time.sleep(0.15)
    raise RuntimeError(f"server did not become healthy: {last_error}")


def run(output: Path) -> dict[str, Any]:
    pilot = Path(__file__).resolve().parents[1]
    port = free_port()
    base = f"http://127.0.0.1:{port}"
    with tempfile.TemporaryDirectory(prefix="venue-deploy-") as tmp:
        database = Path(tmp) / "smoke.db"
        log_path = Path(tmp) / "uvicorn.log"
        env = os.environ.copy()
        env["PYTHONPATH"] = str(pilot / "src")
        env["VENUE_DATABASE"] = str(database)
        cmd = [
            sys.executable,
            "-m",
            "uvicorn",
            "venue_pilot.api:app",
            "--host",
            "127.0.0.1",
            "--port",
            str(port),
            "--log-level",
            "warning",
        ]
        started = time.perf_counter()
        with log_path.open("w", encoding="utf-8") as log:
            process = subprocess.Popen(cmd, cwd=pilot, env=env, stdout=log, stderr=subprocess.STDOUT)
        checks: list[dict[str, Any]] = []
        try:
            health = wait_for_health(base)
            checks.append({"name": "health", "passed": health == {"status": "ok"}, "observed": health})

            starts_at = (datetime.now(timezone.utc) + timedelta(days=1)).replace(microsecond=0).isoformat()
            status, session = request(
                base,
                "POST",
                "/v1/sessions",
                tenant="tenant-smoke",
                body={"session_id": "session-smoke", "starts_at": starts_at, "capacity": 1},
            )
            checks.append({"name": "create_session", "passed": status == 201 and session.get("capacity") == 1, "status": status, "observed": session})

            status, first = request(
                base,
                "POST",
                "/v1/sessions/session-smoke/reservations",
                tenant="tenant-smoke",
                key="smoke-reserve-1",
                body={"member_id": "member-1"},
            )
            checks.append({"name": "reserve_capacity", "passed": status == 201 and first.get("outcome") == "RESERVED", "status": status, "observed": first})

            replay_status, replay = request(
                base,
                "POST",
                "/v1/sessions/session-smoke/reservations",
                tenant="tenant-smoke",
                key="smoke-reserve-1",
                body={"member_id": "member-1"},
            )
            checks.append({"name": "idempotent_replay", "passed": replay_status == 201 and replay == first, "status": replay_status, "observed": replay})

            status, second = request(
                base,
                "POST",
                "/v1/sessions/session-smoke/reservations",
                tenant="tenant-smoke",
                key="smoke-reserve-2",
                body={"member_id": "member-2"},
            )
            checks.append({"name": "waitlist_on_full", "passed": status == 202 and second.get("outcome") == "WAITLISTED" and second.get("queue_position") == 1, "status": status, "observed": second})

            status, cancelled = request(
                base,
                "DELETE",
                f"/v1/reservations/{first['reservation_id']}",
                tenant="tenant-smoke",
                key="smoke-cancel-1",
            )
            checks.append({"name": "fifo_promotion", "passed": status == 200 and cancelled.get("outcome") == "CANCELED" and cancelled.get("promoted_member_id") == "member-2", "status": status, "observed": cancelled})

            status, metrics = request(base, "GET", "/v1/sessions/session-smoke/metrics", tenant="tenant-smoke")
            checks.append({"name": "no_oversell", "passed": status == 200 and metrics.get("reserved") == 1 and metrics.get("oversold") is False, "status": status, "observed": metrics})

            isolated_status, isolated = request(base, "GET", "/v1/sessions/session-smoke", tenant="other-tenant")
            checks.append({"name": "tenant_isolation", "passed": isolated_status == 404, "status": isolated_status, "observed": isolated})

            result = {
                "schema_version": "1.0",
                "pilot": "venue-reservation",
                "observed_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
                "server": {"command": cmd, "base_url": base, "startup_ms": round((time.perf_counter() - started) * 1000, 3)},
                "checks": checks,
                "passed": all(item["passed"] for item in checks),
                "evidence_boundary": "Local loopback deployment smoke only; this is not external production traffic or a causal A/B result.",
            }
        finally:
            process.terminate()
            try:
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait(timeout=5)
            if process.returncode not in {0, -15}:
                raise RuntimeError(f"server exited unexpectedly with {process.returncode}: {log_path.read_text(encoding='utf-8')}")

    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description="Run a real localhost deployment smoke for the venue pilot")
    parser.add_argument("--output", type=Path, default=Path("reports/deployment-smoke.json"))
    args = parser.parse_args()
    result = run(args.output)
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
