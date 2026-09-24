from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def safe_relative(value: object) -> str | None:
    if not isinstance(value, str) or not value:
        return None
    path = PurePosixPath(value.replace("\\", "/"))
    if path.is_absolute() or ".." in path.parts:
        return None
    return path.as_posix()


def add_error(
    errors: list[dict[str, str]], code: str, path: object, message: str
) -> None:
    errors.append({"code": code, "path": str(path), "message": message})


def verify_sync(audit_path: Path, workspace_root: Path, *, source_only: bool = False) -> dict[str, object]:
    errors: list[dict[str, str]] = []
    checked = 0
    try:
        audit = json.loads(audit_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        add_error(errors, "invalid-audit", audit_path, f"cannot read audit: {exc}")
        audit = {}

    source_relative = safe_relative(audit.get("source_root"))
    targets = audit.get("targets")
    if source_relative is None:
        add_error(errors, "invalid-audit", audit_path, "source_root must be relative")
    if not isinstance(targets, list) or not targets:
        add_error(errors, "invalid-audit", audit_path, "targets must be non-empty")
        targets = []

    source_root = workspace_root / source_relative if source_relative else workspace_root
    target_ids: set[str] = set()
    for target in targets:
        if not isinstance(target, dict):
            add_error(errors, "invalid-audit", audit_path, "target must be an object")
            continue
        target_id = target.get("id")
        target_root_value = target.get("root")
        files = target.get("files")
        if not isinstance(target_id, str) or not target_id or target_id in target_ids:
            add_error(errors, "invalid-audit", audit_path, "target id must be unique")
            continue
        target_ids.add(target_id)
        if not isinstance(target_root_value, str) or not target_root_value:
            add_error(errors, "invalid-audit", target_id, "target root is required")
            continue
        target_root = Path(target_root_value)
        if not isinstance(files, list) or not files:
            add_error(errors, "invalid-audit", target_id, "files must be non-empty")
            continue

        declared_targets: set[str] = set()
        for entry in files:
            if not isinstance(entry, dict):
                add_error(errors, "invalid-audit", target_id, "file must be an object")
                continue
            source_path = safe_relative(entry.get("source_path"))
            target_path = safe_relative(entry.get("target_path"))
            expected_hash = entry.get("sha256")
            expected_bytes = entry.get("bytes")
            if source_path is None or target_path is None:
                add_error(errors, "invalid-audit", target_id, "file paths must be relative")
                continue
            if target_path in declared_targets:
                add_error(errors, "invalid-audit", target_path, "duplicate target path")
                continue
            declared_targets.add(target_path)
            if (
                not isinstance(expected_hash, str)
                or len(expected_hash) != 64
                or not isinstance(expected_bytes, int)
                or expected_bytes < 0
            ):
                add_error(errors, "invalid-audit", target_path, "invalid hash or byte count")
                continue

            source_file = source_root / source_path
            target_file = target_root / target_path
            if not source_file.is_file():
                add_error(errors, "missing-source-file", source_path, "source file is missing")
                continue
            actual_source_hash = sha256(source_file)
            if actual_source_hash != expected_hash:
                add_error(
                    errors,
                    "source-hash-mismatch",
                    source_path,
                    "source does not match the recorded hash",
                )
            if source_file.stat().st_size != expected_bytes:
                add_error(
                    errors,
                    "source-byte-mismatch",
                    source_path,
                    "source does not match the recorded byte count",
                )
            if source_only:
                checked += 1
                continue
            if not target_file.is_file():
                add_error(errors, "missing-target-file", target_path, "target file is missing")
                continue
            checked += 1
            if sha256(target_file) != expected_hash:
                add_error(
                    errors,
                    "target-hash-mismatch",
                    target_path,
                    "target does not match the recorded source hash",
                )
            if target_file.stat().st_size != expected_bytes:
                add_error(
                    errors,
                    "target-byte-mismatch",
                    target_path,
                    "target does not match the recorded source byte count",
                )

        if not source_only:
            actual_targets = {
                path.relative_to(target_root).as_posix()
                for path in target_root.rglob("*")
                if path.is_file()
            } if target_root.is_dir() else set()
            for extra in sorted(actual_targets - declared_targets):
                add_error(errors, "extra-target-file", extra, f"undeclared file in {target_id}")

    return {
        "checked_file_count": checked,
        "errors": errors,
        "gate": "phase-8-dev-loop-source" if source_only else "phase-8-dev-loop-sync",
        "ok": not errors,
        "target_count": len(targets),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify installed dev-loop copies")
    parser.add_argument("--audit", type=Path, required=True)
    parser.add_argument("--workspace-root", type=Path, required=True)
    parser.add_argument("--source-only", action="store_true")
    args = parser.parse_args()
    report = verify_sync(args.audit, args.workspace_root, source_only=args.source_only)
    print(json.dumps(report, ensure_ascii=False, sort_keys=True))
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
