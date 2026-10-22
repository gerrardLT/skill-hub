#!/usr/bin/env python3
"""Verify host-enforced boundaries in a full dev-loop evidence tree."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

FORBIDDEN_TOOLS = {"bash", "network", "remote-git", "merge", "deploy"}
MUTATING_TOOLS = {"edit", "write"}
ALLOWED_COMMAND_PREFIXES = {"python", "python.exe"}


def verify(run_root: Path) -> dict:
    errors: list[str] = []
    checked = 0
    for path in sorted(run_root.rglob("execution.json")):
        checked += 1
        try:
            evidence = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            errors.append(f"invalid execution evidence {path}: {exc}")
            continue
        tools = set(evidence.get("tools", []))
        if tools & FORBIDDEN_TOOLS:
            errors.append(f"forbidden tool enabled: {path}: {sorted(tools & FORBIDDEN_TOOLS)}")
        if tools - {"read", "edit", "write"}:
            errors.append(f"unknown host tool enabled: {path}: {sorted(tools)}")
        if tools == {"read"} and evidence.get("incremental_patch_sha256") != "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855":
            errors.append(f"read-only execution mutated source: {path}")
        for result in evidence.get("command_results", []):
            argv = result.get("argv")
            if not isinstance(argv, list) or not argv or Path(argv[0]).name.casefold() not in ALLOWED_COMMAND_PREFIXES:
                errors.append(f"unapproved host command: {path}: {argv}")
        if not isinstance(evidence.get("source_head"), str) or evidence.get("source_head") != evidence.get("isolated_head"):
            errors.append(f"snapshot identity mismatch: {path}")
    manifest = run_root.parent / "delivery-package/manifest.json"
    if not manifest.is_file():
        errors.append("delivery manifest missing")
    else:
        delivery = json.loads(manifest.read_text(encoding="utf-8"))
        if delivery.get("remote_actions") != [] or delivery.get("merge_performed") is not False or delivery.get("deployment_performed") is not False:
            errors.append("delivery manifest records forbidden side effects")
    return {"gate": "full-dev-loop-security", "ok": not errors, "checked_executions": checked, "errors": errors}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-root", type=Path, required=True)
    args = parser.parse_args()
    result = verify(args.run_root)
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
