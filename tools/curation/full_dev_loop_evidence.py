#!/usr/bin/env python3
"""Build and verify a hashed full-dev-loop evidence manifest."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath

REQUIRED_SUFFIXES = {".json", ".md", ".patch"}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def build(run_root: Path, output: Path) -> dict:
    workspace = run_root.parents[4]
    files = []
    commands = []
    for path in sorted(run_root.rglob("*")):
        if not path.is_file() or path.resolve() == output.resolve() or path.suffix not in REQUIRED_SUFFIXES:
            continue
        relative = path.relative_to(workspace).as_posix()
        files.append({"path": relative, "bytes": path.stat().st_size, "sha256": sha256(path)})
        if path.name == "execution.json":
            evidence = json.loads(path.read_text(encoding="utf-8"))
            for result in evidence.get("command_results", []):
                commands.append({
                    "evidence_path": relative,
                    "argv": result.get("argv"),
                    "returncode": result.get("returncode"),
                    "duration_ms": result.get("duration_ms"),
                    "stdout_sha256": hashlib.sha256(result.get("stdout", "").encode("utf-8")).hexdigest(),
                    "stderr_sha256": hashlib.sha256(result.get("stderr", "").encode("utf-8")).hexdigest(),
                })
    return {"schema_version": "1.0", "run_root": run_root.relative_to(workspace).as_posix(), "files": files, "commands": commands}


def verify(manifest_path: Path) -> dict:
    errors: list[str] = []
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return {"gate": "full-dev-loop-evidence", "ok": False, "errors": [str(exc)]}
    workspace = manifest_path.parents[4]
    for item in manifest.get("files", []):
        relative = PurePosixPath(item.get("path", ""))
        path = workspace / relative
        if relative.is_absolute() or ".." in relative.parts or not path.is_file():
            errors.append(f"missing or unsafe evidence: {relative}")
        elif path.stat().st_size != item.get("bytes") or sha256(path) != item.get("sha256"):
            errors.append(f"evidence hash mismatch: {relative}")
    for command in manifest.get("commands", []):
        if not isinstance(command.get("returncode"), int) or not isinstance(command.get("duration_ms"), (int, float)):
            errors.append(f"command evidence incomplete: {command.get('evidence_path')}")
    required = {"result.json", "write_prd.md", "design_web_flow.md", "build_feature_tdd.md", "qa_only.md", "ship_release.md", "retro_to_requirements.md"}
    names = {PurePosixPath(item["path"]).name for item in manifest.get("files", [])}
    missing = sorted(required - names)
    if missing:
        errors.append(f"required artifacts missing: {missing}")
    return {"gate": "full-dev-loop-evidence", "ok": not errors, "file_count": len(manifest.get("files", [])), "command_count": len(manifest.get("commands", [])), "errors": errors}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--verify-only", action="store_true")
    args = parser.parse_args()
    if not args.verify_only:
        manifest = build(args.run_root.resolve(), args.output.resolve())
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    result = verify(args.output.resolve())
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
