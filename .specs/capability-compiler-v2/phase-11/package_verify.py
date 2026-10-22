#!/usr/bin/env python3
"""Verify, unpack, smoke, patch-rebuild, backup, and restore the BenchShare package."""
from __future__ import annotations

import argparse
import hashlib
import http.cookiejar
import json
import shutil
import socket
import sqlite3
import subprocess
import sys
import time
import urllib.request
import zipfile
from pathlib import Path


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def free_port() -> int:
    with socket.socket() as sock:
        sock.bind(("127.0.0.1", 0))
        return int(sock.getsockname()[1])


def run(command, cwd: Path, timeout=120):
    started = time.perf_counter()
    process = subprocess.run(command, cwd=cwd, capture_output=True, text=True, timeout=timeout, check=False)
    return {"argv": command, "cwd": cwd.as_posix(), "exit_code": process.returncode, "duration_ms": round((time.perf_counter()-started)*1000, 3), "stdout": process.stdout, "stderr": process.stderr}


def health(base: str):
    response = urllib.request.urlopen(base + "/health", timeout=5)
    return response.status, json.loads(response.read())


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--package-root", type=Path, required=True)
    parser.add_argument("--baseline", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    package_root, baseline, out = args.package_root.resolve(), args.baseline.resolve(), args.out.resolve()
    out.mkdir(parents=True, exist_ok=False)
    receipt = json.loads((package_root / "package-receipt.json").read_text(encoding="utf-8"))
    checks, commands = {}, []
    checks["archive_receipt_hash"] = sha(package_root / receipt["package"]) == receipt["package_sha256"]
    checks["patch_receipt_hash"] = sha(package_root / receipt["patch"]) == receipt["patch_sha256"]

    unpack = out / "unpack"
    with zipfile.ZipFile(package_root / receipt["package"]) as package:
        package.extractall(unpack)
    app = unpack / "benchshare-v1"
    manifest = json.loads((app / "PACKAGE-MANIFEST.json").read_text(encoding="utf-8"))
    recomputed = []
    for item in manifest["files"]:
        path = app / item["path"]
        recomputed.append({"path": item["path"], "exists": path.is_file(), "bytes": path.stat().st_size if path.is_file() else None, "sha256": sha(path) if path.is_file() else None})
    tree = hashlib.sha256("".join(f"{item['path']}\0{item['sha256']}\n" for item in recomputed).encode()).hexdigest()
    checks["manifest_files"] = all(item["exists"] and item["bytes"] == expected["bytes"] and item["sha256"] == expected["sha256"] for item, expected in zip(recomputed, manifest["files"], strict=True))
    checks["manifest_tree"] = tree == manifest["tree_sha256"] == receipt["tree_sha256"]
    checks["no_bundled_db"] = not list(app.rglob("*.db"))
    checks["no_third_party_runtime_dependency"] = manifest["third_party_runtime_dependencies"] == []

    compile_result = run([sys.executable, "-m", "compileall", "-q", "benchshare"], app)
    test_result = run([sys.executable, "-m", "pytest", "-q"], app)
    commands.extend([compile_result, test_result])
    checks["fresh_compile"] = compile_result["exit_code"] == 0
    checks["fresh_tests"] = test_result["exit_code"] == 0 and "14 passed" in test_result["stdout"]

    port = free_port(); ready = out / "package-ready.json"; db = out / "package-smoke.db"
    server = subprocess.Popen([sys.executable, "-m", "benchshare", "--host", "127.0.0.1", "--port", str(port), "--db", str(db), "--ready-file", str(ready)], cwd=app, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    deadline = time.monotonic() + 10
    while time.monotonic() < deadline and not ready.exists() and server.poll() is None:
        time.sleep(0.05)
    try:
        status, body = health(f"http://127.0.0.1:{port}") if ready.exists() else (None, None)
        checks["fresh_server_health"] = status == 200 and body == {"status": "ok", "database": "ready"}
    finally:
        server.terminate()
        try: stdout, stderr = server.communicate(timeout=5)
        except subprocess.TimeoutExpired:
            server.kill(); stdout, stderr = server.communicate()
        (out / "package-server-stdout.txt").write_text(stdout, encoding="utf-8")
        (out / "package-server-stderr.txt").write_text(stderr, encoding="utf-8")

    backup = out / "package-smoke.backup.db"
    shutil.copyfile(db, backup)
    backup_hash = sha(backup)
    with sqlite3.connect(backup) as connection:
        backup_integrity = connection.execute("PRAGMA integrity_check").fetchone()[0]
    db.write_bytes(b"damaged")
    shutil.copyfile(backup, db)
    with sqlite3.connect(db) as connection:
        restore_integrity = connection.execute("PRAGMA integrity_check").fetchone()[0]
        actor_count = connection.execute("SELECT COUNT(*) FROM actors WHERE active=1").fetchone()[0]
    checks["backup_integrity"] = backup_integrity == "ok"
    checks["restore_hash"] = sha(db) == backup_hash
    checks["restore_integrity"] = restore_integrity == "ok" and actor_count == 3

    rebuilt = out / "patch-rebuild"
    shutil.copytree(baseline, rebuilt)
    patch_result = run(["patch", "-p1", "-i", str(package_root / receipt["patch"])], rebuilt)
    commands.append(patch_result)
    checks["patch_applies"] = patch_result["exit_code"] == 0
    rebuilt_files = {path.relative_to(rebuilt).as_posix(): sha(path) for path in rebuilt.rglob("*") if path.is_file() and path.name != "README.md.orig"}
    package_files = {item["path"]: item["sha256"] for item in manifest["files"]}
    # Baseline README is deleted/replaced by the complete patch; exact package files must result.
    checks["patch_rebuild_matches"] = all(rebuilt_files.get(name) == digest for name, digest in package_files.items()) and set(rebuilt_files) == set(package_files)

    report = {"schema_version": "2.0", "checks": checks, "commands": commands, "package_receipt": receipt, "manifest_tree_recomputed": tree, "backup_sha256": backup_hash, "passed": all(checks.values()), "remote_actions": []}
    (out / "report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"passed": report["passed"], "checks": checks}, sort_keys=True))
    return 0 if report["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
