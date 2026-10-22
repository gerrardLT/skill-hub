#!/usr/bin/env python3
"""Build a deterministic BenchShare local package, inventory, and baseline patch."""
from __future__ import annotations

import argparse
import datetime as dt
import difflib
import hashlib
import json
import shutil
import zipfile
from pathlib import Path

INCLUDE = [
    "README.md", "PRODUCT.md", "DISCOVERY.md", "STRATEGY.md", "REQUIREMENTS.md",
    "DESIGN-BRIEF.md", "DESIGN.md", "ARCHITECTURE.md", "IMPLEMENTATION-PLAN.md",
    "TEST-MAP.md", "OPERATIONS.md", "RELEASE-NOTES.md", "RETROSPECTIVE.md",
]


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def now() -> str:
    return dt.datetime.now(dt.UTC).isoformat().replace("+00:00", "Z")


def files(root: Path):
    selected = [root / name for name in INCLUDE]
    selected += sorted((root / "benchshare").rglob("*"))
    selected += sorted((root / "tests").glob("test_*.py"))
    return [path for path in selected if path.is_file() and "__pycache__" not in path.parts]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workspace", type=Path, required=True)
    parser.add_argument("--baseline", type=Path, required=True)
    parser.add_argument("--package-root", type=Path, required=True)
    parser.add_argument("--runtime-tree", required=True)
    args = parser.parse_args()
    workspace, baseline, package_root = args.workspace.resolve(), args.baseline.resolve(), args.package_root.resolve()
    package_root.mkdir(parents=True, exist_ok=True)
    staging = package_root / "benchshare-v1"
    if staging.exists():
        raise FileExistsError(staging)
    staging.mkdir()

    manifest_files = []
    for source in files(workspace):
        relative = source.relative_to(workspace)
        destination = staging / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, destination)
        manifest_files.append({"path": relative.as_posix(), "bytes": destination.stat().st_size, "sha256": sha(destination)})

    tree = hashlib.sha256("".join(f"{item['path']}\0{item['sha256']}\n" for item in manifest_files).encode()).hexdigest()
    manifest = {
        "schema_version": "2.0", "case_id": "benchshare-v1", "format": "deterministic-v1",
        "runtime_tree_sha256": args.runtime_tree, "file_count": len(manifest_files), "tree_sha256": tree,
        "runtime_dependencies": [{"name": "Python", "minimum_version": "3.12", "kind": "runtime"}],
        "third_party_runtime_dependencies": [], "bundled_secrets": [], "bundled_databases": [], "files": manifest_files,
    }
    (staging / "PACKAGE-MANIFEST.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    archive = package_root / "benchshare-v1.zip"
    timestamp = (2025, 1, 1, 0, 0, 0)
    with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as package:
        for path in sorted(staging.rglob("*")):
            if not path.is_file():
                continue
            info = zipfile.ZipInfo((Path("benchshare-v1") / path.relative_to(staging)).as_posix(), timestamp)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            package.writestr(info, path.read_bytes())

    patch_lines = []
    baseline_files = {path.relative_to(baseline).as_posix(): path for path in baseline.rglob("*") if path.is_file()}
    workspace_files = {path.relative_to(workspace).as_posix(): path for path in files(workspace)}
    for name in sorted(set(baseline_files) | set(workspace_files)):
        old_path, new_path = baseline_files.get(name), workspace_files.get(name)
        old = old_path.read_text(encoding="utf-8").splitlines(keepends=True) if old_path else []
        new = new_path.read_text(encoding="utf-8").splitlines(keepends=True) if new_path else []
        patch_lines.extend(difflib.unified_diff(old, new, f"a/{name}" if old_path else "/dev/null", f"b/{name}" if new_path else "/dev/null"))
    patch = package_root / "benchshare-v1.patch"
    patch.write_text("".join(patch_lines), encoding="utf-8", newline="\n")
    receipt = {
        "schema_version": "2.0", "package": archive.name, "package_bytes": archive.stat().st_size,
        "package_sha256": sha(archive), "manifest_sha256": sha(staging / "PACKAGE-MANIFEST.json"),
        "patch": patch.name, "patch_bytes": patch.stat().st_size, "patch_sha256": sha(patch),
        "tree_sha256": tree, "remote_actions": [], "released": False,
    }
    (package_root / "package-receipt.json").write_text(json.dumps(receipt, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps(receipt, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
