#!/usr/bin/env python3
"""Run one approved local Phase 11 host command and persist its receipt."""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import subprocess
import time
from pathlib import Path


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def now() -> str:
    return dt.datetime.now(dt.UTC).isoformat().replace("+00:00", "Z")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cwd", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--timeout", type=int, default=300)
    parser.add_argument("command", nargs=argparse.REMAINDER)
    args = parser.parse_args()
    command = args.command[1:] if args.command[:1] == ["--"] else args.command
    if not command:
        parser.error("command is required after --")

    cwd = args.cwd.resolve()
    out = args.out.resolve()
    out.mkdir(parents=True, exist_ok=False)
    started_at = now()
    started = time.perf_counter()
    timed_out = False
    try:
        result = subprocess.run(command, cwd=cwd, capture_output=True, timeout=args.timeout, check=False)
        stdout, stderr, returncode = result.stdout, result.stderr, result.returncode
    except subprocess.TimeoutExpired as exc:
        stdout, stderr, returncode, timed_out = exc.stdout or b"", exc.stderr or b"", None, True
    duration_ms = round((time.perf_counter() - started) * 1000, 3)
    (out / "stdout.txt").write_bytes(stdout)
    (out / "stderr.txt").write_bytes(stderr)
    receipt = {
        "schema_version": "2.0",
        "argv": command,
        "cwd": cwd.as_posix(),
        "started_at": started_at,
        "ended_at": now(),
        "duration_ms": duration_ms,
        "timeout_seconds": args.timeout,
        "timed_out": timed_out,
        "exit_code": returncode,
        "stdout_sha256": sha(out / "stdout.txt"),
        "stderr_sha256": sha(out / "stderr.txt"),
    }
    (out / "receipt.json").write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps(receipt, sort_keys=True))
    return 124 if timed_out else int(returncode or 0)


if __name__ == "__main__":
    raise SystemExit(main())
