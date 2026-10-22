#!/usr/bin/env python3
"""Build the V2 review ledger without treating legacy coverage claims as semantic review."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from collections import defaultdict
from pathlib import Path
from typing import Any

try:
    from tools.curation.inventory import build_skill_roots, iter_files, normalized_bytes
except ModuleNotFoundError:  # direct script execution
    from inventory import build_skill_roots, iter_files, normalized_bytes

BINARY_EXTENSIONS = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".bmp", ".icns", ".zip"}
BEHAVIOR_EXTENSIONS = {".py", ".js", ".mjs", ".cjs", ".ts", ".tsx", ".jsx", ".sh", ".rb", ".swift", ".m", ".h"}
TEXT_EXTENSIONS = {"", ".md", ".mdx", ".txt", ".json", ".yaml", ".yml", ".toml", ".html", ".css", ".sql", ".tmpl", ".template", ".example", ".dockerfile", ".dockerignore", ".lock", ".plist", ".patch", ".ci"}

def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))

def write(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")

def digest(path: Path) -> str:
    return hashlib.sha256(normalized_bytes(path)).hexdigest()

def owner_roots(relative: str, roots: list[dict[str, Any]]) -> list[str]:
    owners = []
    for root in roots:
        prefix = root["path"] + "/"
        if relative == root["skill_path"] or relative.startswith(prefix):
            owners.append(root["id"])
    return sorted(owners, key=lambda value: (value.count("/"), value))

def review_kind(path: Path) -> tuple[str, str | None]:
    suffix = path.suffix.lower()
    if path.name == "SKILL.md":
        return "semantic-review-required", None
    if suffix in BINARY_EXTENSIONS:
        return "excluded", "binary-asset-inventory-only"
    if suffix in BEHAVIOR_EXTENSIONS:
        return "behavior-review-required", None
    if suffix in TEXT_EXTENSIONS:
        return "semantic-review-required", None
    return "semantic-review-required", "unknown-extension-requires-manual-review"

def legacy_coverage(workspace: Path) -> dict[str, list[dict[str, Any]]]:
    coverage = load(workspace / "curation/coverage.json")
    by_path: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for source, record in coverage.get("sources", {}).items():
        for item in record.get("files", []):
            by_path[item["path"]].append({"source": source, "status": item.get("status"), "reason": item.get("reason")})
    return by_path

def build(workspace: Path) -> dict[str, Any]:
    skills = workspace / "skills"
    roots = build_skill_roots(skills)
    legacy = legacy_coverage(workspace)
    records: list[dict[str, Any]] = []
    ownerless: list[str] = []
    for path in sorted(iter_files(skills), key=lambda item: item.relative_to(skills).as_posix()):
        relative = path.relative_to(skills).as_posix()
        owners = owner_roots(relative, roots)
        if not owners:
            ownerless.append(relative)
        status, reason = review_kind(path)
        records.append({
            "path": relative,
            "sha256": digest(path),
            "bytes": len(normalized_bytes(path)),
            "extension": path.suffix.lower(),
            "owner_roots": owners,
            "primary_owner": max(owners, key=lambda value: value.count("/")) if owners else None,
            "legacy_coverage": legacy.get(relative, []),
            "v2_status": status,
            "reason": reason,
            "subkind": "binary" if status == "excluded" else None,
            "review_evidence": [],
        })
    bodies: dict[str, list[str]] = defaultdict(list)
    for root in roots:
        skill_path = skills / root["skill_path"]
        bodies[digest(skill_path)].append(root["id"])
    duplicate_groups = [values for values in bodies.values() if len(values) > 1]
    counts: dict[str, int] = defaultdict(int)
    for record in records:
        counts[record["v2_status"]] += 1
    root_records = [{
        "id": root["id"],
        "path": root["path"],
        "skill_path": root["skill_path"],
        "kind": root["kind"],
        "parent_top_level": root["parent_top_level"],
        "snapshot_sha256": root["snapshot_sha256"],
        "skill_body_sha256": digest(skills / root["skill_path"]),
        "v2_status": "semantic-review-required",
        "dossier": None,
        "review_evidence": [],
    } for root in roots]
    errors = []
    if ownerless:
        errors.append(f"source files without an owning skill root: {ownerless}")
    if len(root_records) != 139:
        errors.append(f"expected 139 skill roots, found {len(root_records)}")
    return {
        "schema_version": "2.0",
        "gate": "capability-compiler-v2-phase-1-ledger",
        "ok": not errors,
        "counts": {
            "roots": len(root_records),
            "unique_skill_bodies": len(bodies),
            "duplicate_body_groups": len(duplicate_groups),
            "files": len(records),
            **dict(sorted(counts.items())),
        },
        "duplicate_skill_body_groups": sorted(duplicate_groups),
        "roots": root_records,
        "files": records,
        "errors": errors,
    }

def verify_reviewed(ledger: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    allowed = {"semantic-read", "behavior-reviewed", "excluded"}
    for root in ledger.get("roots", []):
        if root.get("v2_status") != "semantic-read" or not root.get("dossier") or not root.get("review_evidence"):
            errors.append(f"root not semantically reviewed: {root.get('id')}")
    for file in ledger.get("files", []):
        if file.get("v2_status") not in allowed:
            errors.append(f"file not reviewed: {file.get('path')}")
        if file.get("v2_status") == "excluded" and (not file.get("reason") or not file.get("subkind")):
            errors.append(f"excluded file lacks reason or subkind: {file.get('path')}")
        if file.get("v2_status") != "excluded" and not file.get("review_evidence"):
            errors.append(f"reviewed file lacks evidence: {file.get('path')}")
    return errors

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workspace-root", type=Path, default=Path("."))
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--verify-reviewed", action="store_true")
    args = parser.parse_args()
    output = args.output.resolve()
    if args.verify_reviewed:
        ledger = load(output)
        errors = verify_reviewed(ledger)
        result = {"gate": "capability-compiler-v2-phase-1-reviewed", "ok": not errors, "errors": errors}
        print(json.dumps(result, ensure_ascii=False, sort_keys=True))
        return 0 if result["ok"] else 1
    result = build(args.workspace_root.resolve())
    write(output, result)
    print(json.dumps({key: result[key] for key in ("gate", "ok", "counts", "errors")}, ensure_ascii=False, sort_keys=True))
    return 0 if result["ok"] else 1

if __name__ == "__main__":
    raise SystemExit(main())
