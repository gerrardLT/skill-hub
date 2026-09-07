#!/usr/bin/env python3
"""Verify the embedded skills/agentic-sdlc-os/ copy has not drifted from the root source.

The repository keeps an authoritative runtime under the root (``scripts/``,
``manifest/``, ``domain-packs/``, ``control_plane/``) and mirrors part of it into
the shipped skill (``skills/agentic-sdlc-os/``). This checker "freezes" that
mirror by comparing SHA-256 digests, so any silent divergence is caught
deterministically in CI without depending on platform-specific tooling.

Domains checked:
  1. scripts/ intersection  - every *.py present in BOTH trees must be identical.
  2. manifest/ tree         - exact file-set + content parity.
  3. domain-packs/ tree     - exact file-set + content parity.
  4. control_plane/ tree    - exact file-set + content parity.
  5. references/manifests/  - flattened mirror of manifest/ (+ manifest/schemas/).

Files that intentionally live on only one side (root-only dev tooling such as
run_validation.py, or the embedded-only entry point sdlc.py) are reported as
informational, not as drift.

Exit codes: 0 = parity OK, 1 = drift detected.
"""
from __future__ import annotations

import argparse
import hashlib
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MASTER = ROOT / "skills" / "agentic-sdlc-os"

EXCLUDED_PARTS = {"__pycache__"}
EXCLUDED_SUFFIXES = {".pyc"}
EXCLUDED_NAMES = {".DS_Store"}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def tree_files(base: Path) -> set[Path]:
    """Relative paths of all comparable files under ``base`` (caches excluded)."""
    if not base.is_dir():
        return set()
    return {
        item.relative_to(base)
        for item in base.rglob("*")
        if item.is_file()
        and not (set(item.parts) & EXCLUDED_PARTS)
        and item.suffix not in EXCLUDED_SUFFIXES
        and item.name not in EXCLUDED_NAMES
    }


class Report:
    def __init__(self) -> None:
        self.compared = 0
        self.drifts: list[str] = []
        self.info: list[str] = []

    def compare(self, label: str, left: Path, right: Path) -> None:
        self.compared += 1
        left_hash, right_hash = sha256(left), sha256(right)
        if left_hash != right_hash:
            self.drifts.append(f"{label}: root {left_hash[:12]} != embedded {right_hash[:12]}")


def check_scripts(report: Report) -> None:
    """Hash-compare every *.py present in both scripts/ trees (intersection)."""
    root_scripts, master_scripts = ROOT / "scripts", MASTER / "scripts"
    root_py = {p.name for p in root_scripts.glob("*.py")}
    master_py = {p.name for p in master_scripts.glob("*.py")}
    for name in sorted(root_py & master_py):
        report.compare(f"scripts/{name}", root_scripts / name, master_scripts / name)
    for name in sorted(root_py - master_py):
        report.info.append(f"root-only script (dev/CI, not shipped): scripts/{name}")
    for name in sorted(master_py - root_py):
        report.info.append(f"embedded-only script: skills/agentic-sdlc-os/scripts/{name}")


def check_tree(report: Report, rel: str) -> None:
    """Require exact file-set + content parity for a fully mirrored tree."""
    source, target = ROOT / rel, MASTER / rel
    if not source.is_dir():
        report.drifts.append(f"{rel}/: root source tree missing")
        return
    if not target.is_dir():
        report.drifts.append(f"{rel}/: embedded tree missing")
        return
    source_files, target_files = tree_files(source), tree_files(target)
    for rel_path in sorted(source_files - target_files):
        report.drifts.append(f"{rel}/{rel_path.as_posix()}: missing in embedded copy")
    for rel_path in sorted(target_files - source_files):
        report.drifts.append(f"{rel}/{rel_path.as_posix()}: unexpected in embedded copy")
    for rel_path in sorted(source_files & target_files):
        report.compare(f"{rel}/{rel_path.as_posix()}", source / rel_path, target / rel_path)


def check_references(report: Report) -> None:
    """references/manifests/ flattens manifest/ + manifest/schemas/ into one dir."""
    ref = MASTER / "references" / "manifests"
    if not ref.is_dir():
        report.drifts.append("references/manifests/: embedded mirror missing")
        return
    for item in sorted(tree_files(ref)):
        candidates = [ROOT / "manifest" / item.name, ROOT / "manifest" / "schemas" / item.name]
        source = next((c for c in candidates if c.is_file()), None)
        if source is None:
            report.drifts.append(f"references/manifests/{item.name}: no root source found")
            continue
        report.compare(f"references/manifests/{item.name}", source, ref / item)


def main() -> int:
    parser = argparse.ArgumentParser(description="Check root vs embedded skill-copy parity.")
    parser.add_argument("--verbose", action="store_true", help="list one-sided (informational) files")
    parser.add_argument("--quiet", action="store_true", help="print only when drift is found")
    args = parser.parse_args()

    if not MASTER.is_dir():
        print(f"embedded skill copy not found: {MASTER}", file=sys.stderr)
        return 1

    report = Report()
    check_scripts(report)
    for rel in ("manifest", "domain-packs", "control_plane"):
        check_tree(report, rel)
    check_references(report)

    if report.drifts:
        print("EMBEDDED PARITY DRIFT")
        for line in report.drifts:
            print("-", line)
        print(f"\n{report.compared} mirrored files compared, {len(report.drifts)} drifted")
        return 1

    if not args.quiet:
        print(f"EMBEDDED PARITY OK - {report.compared} mirrored files identical (sha256)")
    if args.verbose:
        for line in report.info:
            print("  i", line)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
