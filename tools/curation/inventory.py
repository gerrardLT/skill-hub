from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
from pathlib import Path
from typing import Iterable


IGNORED_DIRECTORIES = {".git"}


def iter_files(root: Path) -> Iterable[Path]:
    for current_root, directories, files in os.walk(root):
        directories[:] = sorted(
            directory
            for directory in directories
            if directory not in IGNORED_DIRECTORIES
        )
        for filename in sorted(files):
            yield Path(current_root) / filename


def normalized_bytes(path: Path) -> bytes:
    data = path.read_bytes()
    if path.suffix.lower() not in {".zip", ".png", ".jpg", ".jpeg", ".gif", ".webp", ".bmp", ".icns"}:
        data = data.replace(b"\r\n", b"\n")
    return data


def sha256_file(path: Path) -> str:
    return hashlib.sha256(normalized_bytes(path)).hexdigest()


def build_baseline(root: Path) -> dict[str, object]:
    files = []
    total_bytes = 0
    tree_digest = hashlib.sha256()
    paths = sorted(iter_files(root), key=lambda path: path.relative_to(root).as_posix())

    for path in paths:
        relative_path = path.relative_to(root).as_posix()
        content = normalized_bytes(path)
        size = len(content)
        digest = hashlib.sha256(content).hexdigest()
        entry = {"path": relative_path, "bytes": size, "sha256": digest}
        files.append(entry)
        total_bytes += size
        tree_digest.update(relative_path.encode("utf-8"))
        tree_digest.update(b"\0")
        tree_digest.update(str(size).encode("ascii"))
        tree_digest.update(b"\0")
        tree_digest.update(digest.encode("ascii"))
        tree_digest.update(b"\n")

    return {
        "version": 1,
        "algorithm": "sha256",
        "root": root.name,
        "file_count": len(files),
        "total_bytes": total_bytes,
        "tree_sha256": tree_digest.hexdigest(),
        "files": files,
    }


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def parse_frontmatter(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8", errors="replace")
    if not text.startswith("---"):
        return {}
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}
    values = {}
    for line in parts[1].splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        values[key.strip()] = value.strip().strip('"').strip("'")
    return values


def parse_catalog(path: Path) -> tuple[list[dict[str, str]], list[dict[str, str]]]:
    entries = []
    supplemental = []
    domain = "unclassified"
    row_pattern = re.compile(
        r"^\|\s*(\d+)\s*\|\s*`([^`]+)`\s*\|\s*`([^`]+)`\s*\|\s*(.*?)\s*\|"
    )
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        if line.startswith("## "):
            domain = line[3:].strip()
            continue
        match = row_pattern.match(line)
        if not match:
            continue
        number, skill, source, role = match.groups()
        entry = {
            "domain": domain,
            "skill": skill,
            "source": source,
            "role": role,
        }
        if number == "0":
            supplemental.append(entry)
        else:
            entries.append(entry)
    return entries, supplemental


def build_skill_roots(root: Path) -> list[dict[str, object]]:
    roots = []
    for skill_path in sorted(root.rglob("SKILL.md"), key=lambda path: path.as_posix()):
        relative = skill_path.relative_to(root)
        top_level = relative.parts[0]
        is_top_level = len(relative.parts) == 2
        metadata = parse_frontmatter(skill_path)
        directory = skill_path.parent
        files = list(iter_files(directory))
        digest = hashlib.sha256()
        total_bytes = 0
        for file_path in sorted(files, key=lambda path: path.relative_to(directory).as_posix()):
            relative_file = file_path.relative_to(directory).as_posix()
            file_digest = sha256_file(file_path)
            total_bytes += file_path.stat().st_size
            digest.update(relative_file.encode("utf-8"))
            digest.update(b"\0")
            digest.update(file_digest.encode("ascii"))
            digest.update(b"\n")
        roots.append(
            {
                "id": "skill-root:" + skill_path.parent.relative_to(root).as_posix(),
                "name": metadata.get("name") or directory.name,
                "description": metadata.get("description"),
                "path": skill_path.parent.relative_to(root).as_posix(),
                "skill_path": skill_path.relative_to(root).as_posix(),
                "kind": "top-level-skill" if is_top_level else "embedded-skill",
                "parent_top_level": top_level,
                "file_count": len(files),
                "total_bytes": total_bytes,
                "snapshot_sha256": digest.hexdigest(),
            }
        )
    return roots


def find_missing_references(root: Path) -> list[dict[str, object]]:
    gaps = []
    link_pattern = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
    for markdown in sorted(root.rglob("*.md"), key=lambda path: path.as_posix()):
        text = markdown.read_text(encoding="utf-8", errors="replace")
        for line_number, line in enumerate(text.splitlines(), 1):
            for target in link_pattern.findall(line):
                clean_target = target.split("#", 1)[0].strip()
                if not clean_target or clean_target.startswith(("http://", "https://", "mailto:", "#")):
                    continue
                if not (markdown.parent / clean_target).exists():
                    gaps.append(
                        {
                            "severity": "review-required",
                            "kind": "missing-relative-reference",
                            "source_path": markdown.relative_to(root).as_posix(),
                            "line": line_number,
                            "target": clean_target,
                        }
                    )
    return gaps


def build_inventory(
    root: Path,
    catalog_path: Path,
    source_evidence_path: Path | None = None,
    policy_path: Path | None = None,
) -> tuple[dict[str, object], dict[str, object], dict[str, object]]:
    catalog_entries, supplemental_entries = parse_catalog(catalog_path)
    source_evidence = {}
    if source_evidence_path:
        source_evidence = json.loads(
            source_evidence_path.read_text(encoding="utf-8")
        ).get("records", {})
    policy = {}
    if policy_path:
        policy = json.loads(policy_path.read_text(encoding="utf-8"))
    deferred_skill_ids = set(policy.get("deferred_skill_ids", []))
    skill_roots = build_skill_roots(root)
    top_level_directories = sorted(path.name for path in root.iterdir() if path.is_dir())
    top_level_roots = [entry for entry in skill_roots if entry["kind"] == "top-level-skill"]
    embedded_roots = [entry for entry in skill_roots if entry["kind"] == "embedded-skill"]
    top_level_by_name = {entry["path"]: entry for entry in top_level_roots}
    seen = {}
    resolved_entries = []
    gaps = find_missing_references(root)

    for index, entry in enumerate(catalog_entries, 1):
        key = (entry["skill"], entry["source"])
        entry_id = f"catalog-entry:{index:03d}"
        resolved = {
            "id": entry_id,
            **entry,
            "scope": (
                "deferred-platform"
                if entry["skill"] in deferred_skill_ids
                else "included"
            ),
        }
        if key in seen:
            resolved["resolution"] = "duplicate-reference"
            resolved["duplicate_of"] = seen[key]
        elif entry["skill"] in top_level_by_name:
            resolved["resolution"] = "resolved"
            resolved["skill_root"] = top_level_by_name[entry["skill"]]["id"]
            seen[key] = entry_id
        else:
            resolved["resolution"] = "gap"
            gaps.append(
                {
                    "severity": "blocking",
                    "kind": "catalog-skill-root-missing",
                    "catalog_entry": entry_id,
                    "skill": entry["skill"],
                }
            )
        resolved_entries.append(resolved)

    supplemental = []
    for index, entry in enumerate(supplemental_entries, 1):
        supplemental.append(
            {
                "id": f"supplemental-entry:{index:03d}",
                **entry,
                "resolution": "resolved" if entry["skill"] in top_level_by_name else "gap",
            }
        )

    source_repositories = sorted({entry["source"] for entry in catalog_entries + supplemental_entries})
    sources = {}
    for source in source_repositories:
        cache_key = source.replace("/", "_")
        evidence = source_evidence.get(cache_key, {})
        revision = evidence.get("uniqueCommit")
        commit_objects = evidence.get("commitObjects", [])
        revision_verified = (
            isinstance(revision, str)
            and len(revision) == 40
            and commit_objects == [revision]
        )
        license_paths = evidence.get("licensePaths", []) if revision_verified else []
        sources[source] = {
            "revision": revision if revision_verified else None,
            "revision_status": (
                "verified-from-download-cache" if revision_verified else "unknown"
            ),
            "license_paths": license_paths,
            "evidence": evidence.get("evidence") if revision_verified else None,
        }
        if not revision_verified:
            gaps.append(
                {
                    "severity": "review-required",
                    "kind": "source-revision-unknown",
                    "source": source,
                }
            )
        if not license_paths:
            gaps.append(
                {
                    "severity": "review-required",
                    "kind": "license-unverified-in-snapshot",
                    "source": source,
                }
            )

    cataloged_skill_names = {
        entry["skill"] for entry in catalog_entries + supplemental_entries
    }
    unlisted_top_level_roots = sorted(
        entry["path"]
        for entry in top_level_roots
        if entry["path"] not in cataloged_skill_names
    )

    inventory = {
        "version": 1,
        "source_root": root.name,
        "counts": {
            "catalog_entries": len(catalog_entries),
            "unique_catalog_skill_names": len({entry["skill"] for entry in catalog_entries}),
            "supplemental_entries": len(supplemental_entries),
            "top_level_directories": len(top_level_directories),
            "top_level_skill_roots": len(top_level_roots),
            "embedded_skill_roots": len(embedded_roots),
            "all_skill_roots": len(skill_roots),
        },
        "catalog_entries": resolved_entries,
        "supplemental_entries": supplemental,
        "unlisted_top_level_roots": unlisted_top_level_roots,
        "skill_roots": skill_roots,
        "sources": sources,
    }
    gap_report = {"version": 1, "gaps": gaps}
    lock_entries = {}
    for entry in top_level_roots:
        source = next(
            (
                item["source"]
                for item in catalog_entries + supplemental_entries
                if item["skill"] == entry["path"]
            ),
            None,
        )
        lock_entries[entry["path"]] = {
            "skillPath": f"skills/{entry['skill_path']}",
            "snapshotHash": entry["snapshot_sha256"],
            "source": source,
            "sourceRevision": sources.get(source, {}).get("revision"),
        }
    lock = {"version": 2, "skills": lock_entries}
    return inventory, gap_report, lock


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build deterministic skill inventory facts")
    subparsers = parser.add_subparsers(dest="command", required=True)
    baseline = subparsers.add_parser("baseline")
    baseline.add_argument("--root", type=Path, required=True)
    baseline.add_argument("--output", type=Path, required=True)
    inventory = subparsers.add_parser("inventory")
    inventory.add_argument("--root", type=Path, required=True)
    inventory.add_argument("--catalog", type=Path, required=True)
    inventory.add_argument("--source-evidence", type=Path)
    inventory.add_argument("--policy", type=Path)
    inventory.add_argument("--output", type=Path, required=True)
    inventory.add_argument("--gaps-output", type=Path, required=True)
    inventory.add_argument("--lock-output", type=Path, required=True)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.command == "baseline":
        write_json(args.output, build_baseline(args.root.resolve()))
        return 0
    if args.command == "inventory":
        inventory, gaps, lock = build_inventory(
            args.root.resolve(),
            args.catalog.resolve(),
            args.source_evidence.resolve() if args.source_evidence else None,
            args.policy.resolve() if args.policy else None,
        )
        write_json(args.output, inventory)
        write_json(args.gaps_output, gaps)
        write_json(args.lock_output, lock)
        return 0
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
