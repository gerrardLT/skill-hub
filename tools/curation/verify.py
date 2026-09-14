from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath, PureWindowsPath

from inventory import build_baseline


def verify_source(root: Path, baseline_path: Path) -> dict[str, object]:
    expected = json.loads(baseline_path.read_text(encoding="utf-8"))
    current = build_baseline(root.resolve())
    expected_files = {entry["path"]: entry for entry in expected["files"]}
    current_files = {entry["path"]: entry for entry in current["files"]}

    expected_paths = set(expected_files)
    current_paths = set(current_files)
    added = sorted(current_paths - expected_paths)
    removed = sorted(expected_paths - current_paths)
    changed = sorted(
        path
        for path in expected_paths & current_paths
        if expected_files[path]["bytes"] != current_files[path]["bytes"]
        or expected_files[path]["sha256"] != current_files[path]["sha256"]
    )

    return {
        "added": added,
        "changed": changed,
        "ok": not (added or changed or removed),
        "removed": removed,
    }


def verify_inventory(
    inventory_path: Path,
    policy_path: Path,
    lock_path: Path,
) -> dict[str, object]:
    inventory = json.loads(inventory_path.read_text(encoding="utf-8"))
    policy = json.loads(policy_path.read_text(encoding="utf-8"))
    lock = json.loads(lock_path.read_text(encoding="utf-8"))

    top_level_roots = {
        root["path"]
        for root in inventory.get("skill_roots", [])
        if root.get("kind") == "top-level-skill"
    }
    locked_roots = set(lock.get("skills", {}))
    forbidden = [value.lower() for value in policy.get("forbidden_providers", [])]
    asset_identities = set()
    for root in inventory.get("skill_roots", []):
        asset_identities.update({str(root.get("path", "")), str(root.get("name", ""))})
    for entry in inventory.get("catalog_entries", []):
        asset_identities.add(str(entry.get("skill", "")))
    forbidden_identities = sorted(
        identity
        for identity in asset_identities
        if identity and any(provider in identity.lower() for provider in forbidden)
    )

    deferred = set(policy.get("deferred_skill_ids", []))
    scope_mismatches = []
    for entry in inventory.get("catalog_entries", []):
        skill = entry.get("skill")
        expected = "deferred-platform" if skill in deferred else "included"
        actual = entry.get("scope")
        if actual != expected:
            scope_mismatches.append(
                {"skill": skill, "expected": expected, "actual": actual}
            )

    missing_lock_entries = sorted(top_level_roots - locked_roots)
    extra_lock_entries = sorted(locked_roots - top_level_roots)
    return {
        "extra_lock_entries": extra_lock_entries,
        "forbidden_asset_identities": forbidden_identities,
        "missing_lock_entries": missing_lock_entries,
        "ok": not (
            extra_lock_entries
            or forbidden_identities
            or missing_lock_entries
            or scope_mismatches
        ),
        "scope_mismatches": scope_mismatches,
    }


def reference_key(record: dict[str, object]) -> str:
    return ":".join(
        [
            str(record.get("source_path", "")),
            str(record.get("line", "")),
            str(record.get("target", "")),
        ]
    )


def supplement_materials(supplements_root: Path) -> set[tuple[str, str]]:
    materials: set[tuple[str, str]] = set()
    if not supplements_root.exists():
        return materials

    for metadata_path in sorted(supplements_root.rglob("supplement.json")):
        try:
            metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            continue
        repository = metadata.get("source_repository")
        revision = metadata.get("source_revision")
        reason = metadata.get("reason")
        declared_files = metadata.get("files")
        if (
            not isinstance(repository, str)
            or not isinstance(revision, str)
            or len(revision) != 40
            or not isinstance(reason, str)
            or not reason.strip()
            or not isinstance(declared_files, dict)
        ):
            continue

        relative_metadata = metadata_path.relative_to(supplements_root)
        material_prefix = Path(*relative_metadata.parts[1:-1])
        for declared_path, expected_hash in declared_files.items():
            if not isinstance(declared_path, str) or not isinstance(expected_hash, str):
                continue
            normalized_declared = Path(declared_path.replace("\\", "/"))
            file_path = metadata_path.parent / normalized_declared
            if not file_path.is_file():
                continue
            actual_hash = hashlib.sha256(file_path.read_bytes()).hexdigest()
            if actual_hash != expected_hash:
                continue
            material_path = (material_prefix / normalized_declared).as_posix()
            materials.add((repository, material_path))
    return materials


def normalized_reference_target(target: str) -> str:
    parts = [part for part in target.replace("\\", "/").split("/") if part]
    while parts and parts[0] == "..":
        parts.pop(0)
    return "/".join(parts)


def normalized_skill_path(path: object) -> str:
    normalized = str(path or "").replace("\\", "/")
    if normalized.startswith("skills/"):
        return normalized[len("skills/") :]
    return normalized


def scan_forbidden_content(
    content_roots: list[Path], forbidden_providers: list[str]
) -> list[str]:
    matches = []
    forbidden = [provider.lower() for provider in forbidden_providers]
    for root in content_roots:
        if not root.exists():
            continue
        paths = [root] if root.is_file() else sorted(path for path in root.rglob("*") if path.is_file())
        for path in paths:
            try:
                text = path.read_text(encoding="utf-8", errors="ignore").lower()
            except OSError:
                continue
            if any(provider in text for provider in forbidden):
                matches.append(str(path))
    return sorted(set(matches))


def verify_phase2(
    inventory_path: Path,
    gaps_path: Path,
    reference_review_path: Path,
    dependency_scan_path: Path,
    supplements_root: Path,
    policy_path: Path,
    content_roots: list[Path],
) -> dict[str, object]:
    inventory = json.loads(inventory_path.read_text(encoding="utf-8"))
    gaps = json.loads(gaps_path.read_text(encoding="utf-8")).get("gaps", [])
    reference_review = json.loads(
        reference_review_path.read_text(encoding="utf-8")
    ).get("classifications", [])
    dependency_records = json.loads(
        dependency_scan_path.read_text(encoding="utf-8")
    ).get("records", [])
    policy = json.loads(policy_path.read_text(encoding="utf-8"))

    catalog_entries = inventory.get("catalog_entries", [])
    expected_catalog_count = inventory.get("counts", {}).get("catalog_entries")
    catalog_count_mismatch = (
        not isinstance(expected_catalog_count, int)
        or expected_catalog_count != len(catalog_entries)
    )
    allowed_resolutions = {"resolved", "duplicate-reference", "gap", "deferred"}
    incomplete_catalog_entries = sorted(
        str(entry.get("id", entry.get("skill", "<unknown>")))
        for entry in catalog_entries
        if entry.get("scope") not in {"included", "deferred-platform"}
        or entry.get("resolution") not in allowed_resolutions
    )

    revision_unknown_gaps = {
        str(gap.get("source"))
        for gap in gaps
        if gap.get("kind") == "source-revision-unknown"
    }
    license_unknown_gaps = {
        str(gap.get("source"))
        for gap in gaps
        if gap.get("kind") == "license-unverified-in-snapshot"
    }
    explicit_unknown_sources = []
    invalid_source_states = []
    for source, state in inventory.get("sources", {}).items():
        revision_status = state.get("revision_status")
        revision = state.get("revision")
        license_paths = state.get("license_paths")
        if revision_status == "unknown":
            explicit_unknown_sources.append(source)
            if source not in revision_unknown_gaps:
                invalid_source_states.append(f"{source}:missing-revision-gap")
        elif not (
            revision_status == "verified-from-download-cache"
            and isinstance(revision, str)
            and len(revision) == 40
        ):
            invalid_source_states.append(f"{source}:invalid-revision-state")
        if not isinstance(license_paths, list):
            invalid_source_states.append(f"{source}:invalid-license-state")
        elif not license_paths and source not in license_unknown_gaps:
            invalid_source_states.append(f"{source}:missing-license-gap")

    relative_gaps = [
        gap for gap in gaps if gap.get("kind") == "missing-relative-reference"
    ]
    reviewed_by_key = {reference_key(item): item for item in reference_review}
    unclassified_reference_gaps = sorted(
        reference_key(gap)
        for gap in relative_gaps
        if reference_key(gap) not in reviewed_by_key
    )
    orphan_reference_reviews = sorted(
        key
        for key in reviewed_by_key
        if key not in {reference_key(gap) for gap in relative_gaps}
    )

    top_level_skill_paths = {
        normalized_skill_path(root.get("skill_path"))
        for root in inventory.get("skill_roots", [])
        if root.get("kind") == "top-level-skill"
    }
    scanned_skill_paths = {
        normalized_skill_path(record.get("skill_path"))
        for record in dependency_records
    }
    missing_dependency_scans = sorted(top_level_skill_paths - scanned_skill_paths)
    extra_dependency_scans = sorted(scanned_skill_paths - top_level_skill_paths)

    catalog_by_skill = {
        str(entry.get("skill")): entry
        for entry in catalog_entries
        if entry.get("resolution") != "duplicate-reference"
    }
    materials = supplement_materials(supplements_root)
    unmitigated_included_blockers = []
    for gap in relative_gaps:
        key = reference_key(gap)
        review = reviewed_by_key.get(key)
        source_path = str(gap.get("source_path", ""))
        skill = source_path.split("/", 1)[0]
        catalog_entry = catalog_by_skill.get(skill)
        if not catalog_entry or catalog_entry.get("scope") != "included":
            continue
        if review is not None and not review.get("blocking_for_standalone"):
            continue
        source_repository = str(catalog_entry.get("source", ""))
        target = normalized_reference_target(str(gap.get("target", "")))
        if (source_repository, target) not in materials:
            unmitigated_included_blockers.append(key)

    forbidden_content_matches = scan_forbidden_content(
        content_roots, policy.get("forbidden_providers", [])
    )
    failures = (
        ["catalog-count-mismatch"] if catalog_count_mismatch else []
    ) + incomplete_catalog_entries + invalid_source_states + unclassified_reference_gaps + orphan_reference_reviews + missing_dependency_scans + extra_dependency_scans + unmitigated_included_blockers + forbidden_content_matches

    return {
        "catalog_count_mismatch": catalog_count_mismatch,
        "explicit_unknown_sources": sorted(explicit_unknown_sources),
        "extra_dependency_scans": extra_dependency_scans,
        "forbidden_content_matches": forbidden_content_matches,
        "incomplete_catalog_entries": incomplete_catalog_entries,
        "invalid_source_states": sorted(invalid_source_states),
        "missing_dependency_scans": missing_dependency_scans,
        "ok": not failures,
        "orphan_reference_reviews": orphan_reference_reviews,
        "unclassified_reference_gaps": unclassified_reference_gaps,
        "unmitigated_included_blockers": sorted(unmitigated_included_blockers),
    }


DOSSIER_SECTIONS = [
    "Problem",
    "When to Use",
    "When Not to Use",
    "Role",
    "Inputs",
    "Outputs",
    "Workflow",
    "Branches",
    "Rules",
    "Exceptions",
    "Dependencies",
    "Permissions and Side Effects",
    "Gates",
    "Open Questions",
    "Unique Value",
    "Reading Coverage",
]
UNIT_FIELDS = {
    "id",
    "source_path",
    "origin_line_start",
    "origin_line_end",
    "type",
    "raw_excerpt",
    "meaning",
    "boundary_condition",
    "dependency_skills",
    "candidate_destination",
    "validation_criteria",
    "status",
}
UNIT_TYPES = {
    "method",
    "rule",
    "exception",
    "template",
    "example",
    "tool-action",
    "gate",
}
UNIT_STATUSES = {
    "retain",
    "merge",
    "rewrite",
    "conditionalize",
    "exclude",
    "defer",
}


def markdown_targets(path: Path) -> list[str]:
    import re

    text = path.read_text(encoding="utf-8", errors="replace")
    visible_lines = []
    fence_marker = None
    fence_length = 0
    for line in text.splitlines(keepends=True):
        if fence_marker is None:
            opening = re.match(r"^ {0,3}(`{3,}|~{3,})", line)
            if opening and not (
                opening.group(1)[0] == "`" and "`" in line[opening.end() :]
            ):
                fence_marker = opening.group(1)[0]
                fence_length = len(opening.group(1))
                continue
            visible_lines.append(line)
            continue
        if re.match(
            rf"^ {{0,3}}{re.escape(fence_marker)}{{{fence_length},}}[ \t]*(?:\r?\n)?$",
            line,
        ):
            fence_marker = None
            fence_length = 0
    text = "".join(visible_lines)

    targets = []
    for target in re.findall(r"\[[^\]]*\]\(([^)]+)\)", text):
        clean = target.split("#", 1)[0].strip()
        if clean and not clean.startswith(("http://", "https://", "mailto:", "#")):
            targets.append(clean)

    for target in re.findall(r"(?<!`)`([^`\r\n]+)`(?!`)", text):
        clean = target.strip().replace("\\", "/")
        bare_url = re.match(
            r"^(?:[A-Za-z0-9-]+\.)+[A-Za-z]{2,63}/",
            clean,
            re.IGNORECASE,
        )
        if (
            not clean
            or any(character.isspace() for character in clean)
            or clean.startswith(("-", "#", "/", "//"))
            or re.match(r"^[A-Za-z][A-Za-z0-9+.-]*:", clean)
            or bare_url
            or any(character in clean for character in "$|;&<>*?{}[]()")
            or not Path(clean).suffix
        ):
            continue
        targets.append(clean)
    return targets


STANDARD_RESOURCE_DIRECTORIES = {
    "references",
    "reference",
    "templates",
    "examples",
    "sections",
    "scripts",
}


def reachable_skill_files(skills_root: Path, entry_path: str) -> set[str]:
    entry = skills_root / entry_path
    if not entry.is_file():
        return {entry_path}
    reachable = {entry_path}
    pending = [entry]
    visited = set()
    while pending:
        current = pending.pop()
        if current in visited or current.suffix.lower() != ".md":
            continue
        visited.add(current)
        for target in markdown_targets(current):
            resolved = (current.parent / target).resolve()
            try:
                relative = resolved.relative_to(skills_root.resolve()).as_posix()
            except ValueError:
                continue
            if resolved.is_file() and relative not in reachable:
                reachable.add(relative)
                pending.append(resolved)

    skill_root = entry.parent
    for directory_name in STANDARD_RESOURCE_DIRECTORIES:
        directory = skill_root / directory_name
        if not directory.is_dir():
            continue
        for resource in sorted(path for path in directory.rglob("*") if path.is_file()):
            relative = resource.relative_to(skills_root).as_posix()
            reachable.add(relative)
            if resource.suffix.lower() == ".md" and resource not in visited:
                pending.append(resource)

    while pending:
        current = pending.pop()
        if current in visited or current.suffix.lower() != ".md":
            continue
        visited.add(current)
        for target in markdown_targets(current):
            resolved = (current.parent / target).resolve()
            try:
                relative = resolved.relative_to(skills_root.resolve()).as_posix()
            except ValueError:
                continue
            if resolved.is_file() and relative not in reachable:
                reachable.add(relative)
                pending.append(resolved)
    return reachable


def read_jsonl(path: Path) -> tuple[list[dict[str, object]], list[str]]:
    records = []
    errors = []
    for line_number, line in enumerate(
        path.read_text(encoding="utf-8").splitlines(), 1
    ):
        if not line.strip():
            continue
        try:
            value = json.loads(line)
        except json.JSONDecodeError as error:
            errors.append(f"{path.name}:{line_number}:{error.msg}")
            continue
        if not isinstance(value, dict):
            errors.append(f"{path.name}:{line_number}:not-an-object")
            continue
        records.append(value)
    return records, errors


def verify_unit(
    unit: dict[str, object], skills_root: Path
) -> tuple[list[str], bool]:
    unit_id = str(unit.get("id", "<missing-id>"))
    errors = []
    missing = sorted(UNIT_FIELDS - set(unit))
    if missing:
        errors.append(f"{unit_id}:missing-fields:{','.join(missing)}")
    if unit.get("type") not in UNIT_TYPES:
        errors.append(f"{unit_id}:invalid-type")
    if unit.get("status") not in UNIT_STATUSES:
        errors.append(f"{unit_id}:invalid-status")
    if not isinstance(unit.get("dependency_skills"), list):
        errors.append(f"{unit_id}:invalid-dependency-skills")

    source_path = normalized_skill_path(unit.get("source_path"))
    source_file = skills_root / source_path
    start = unit.get("origin_line_start")
    end = unit.get("origin_line_end")
    excerpt_matches = True
    if not source_file.is_file():
        errors.append(f"{unit_id}:missing-source:{source_path}")
        excerpt_matches = False
    elif not isinstance(start, int) or not isinstance(end, int) or start < 1 or end < start:
        errors.append(f"{unit_id}:invalid-line-range")
        excerpt_matches = False
    else:
        source_lines = source_file.read_text(
            encoding="utf-8", errors="replace"
        ).splitlines()
        if end > len(source_lines):
            errors.append(f"{unit_id}:line-range-out-of-bounds")
            excerpt_matches = False
        else:
            expected = "\n".join(source_lines[start - 1 : end]).strip()
            actual = str(unit.get("raw_excerpt", "")).strip()
            if actual != expected:
                errors.append(f"{unit_id}:source-excerpt-mismatch")
                excerpt_matches = False
    return errors, excerpt_matches


def verify_phase3(
    inventory_path: Path,
    skills_root: Path,
    dossiers_root: Path,
    units_root: Path,
    coverage_path: Path,
    reference_review_path: Path,
    supplements_root: Path,
) -> dict[str, object]:
    inventory = json.loads(inventory_path.read_text(encoding="utf-8"))
    coverage = json.loads(coverage_path.read_text(encoding="utf-8"))
    reference_reviews = json.loads(
        reference_review_path.read_text(encoding="utf-8")
    ).get("classifications", [])
    coverage_sources = coverage.get("sources", {})
    if not isinstance(coverage_sources, dict):
        coverage_sources = {}
    included = {
        str(entry.get("skill")): entry
        for entry in inventory.get("catalog_entries", [])
        if entry.get("scope") == "included"
        and entry.get("resolution") == "resolved"
    }
    deferred = {
        str(entry.get("skill")): entry
        for entry in inventory.get("catalog_entries", [])
        if entry.get("scope") == "deferred-platform"
        and entry.get("resolution") == "resolved"
    }
    roots_by_path = {
        str(root.get("path")): root
        for root in inventory.get("skill_roots", [])
        if root.get("kind") == "top-level-skill"
    }
    missing_dossiers = []
    missing_unit_files = []
    missing_coverage_sources = []
    invalid_dossiers = []
    invalid_units = []
    jsonl_errors = []
    source_excerpt_mismatches = []
    unread_required_files = []
    validated_units = 0
    invalid_supplement_manifests = []
    missing_required_supplements = []
    missing_supplement_coverage = []
    unread_supplement_files = []

    blocking_supplements = []
    for review in reference_reviews:
        if (
            review.get("kind") != "missing-relative-reference"
            or review.get("blocking_for_standalone") is not True
        ):
            continue
        source_path = normalized_skill_path(review.get("source_path"))
        skill = source_path.split("/", 1)[0]
        catalog_entry = included.get(skill)
        if not catalog_entry:
            continue
        blocking_supplements.append(
            (
                skill,
                str(catalog_entry.get("source", "")),
                normalized_reference_target(str(review.get("target", ""))),
            )
        )
    required_repositories = {
        repository for _, repository, _ in blocking_supplements if repository
    }

    manifests = []
    if supplements_root.exists():
        for manifest_path in sorted(supplements_root.rglob("supplement.json")):
            relative_manifest = manifest_path.relative_to(supplements_root)
            try:
                manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            except (json.JSONDecodeError, OSError):
                continue
            if not isinstance(manifest, dict):
                continue
            repository = manifest.get("source_repository")
            if (
                not isinstance(repository, str)
                or repository not in required_repositories
            ):
                continue
            revision = manifest.get("source_revision")
            reason = manifest.get("reason")
            files = manifest.get("files")
            relative_manifest = manifest_path.relative_to(supplements_root)
            root = Path(*relative_manifest.parts[1:-1]).as_posix()
            identity = f"{repository}@{revision}:{root}"
            if (
                not isinstance(repository, str)
                or not isinstance(revision, str)
                or len(revision) != 40
                or any(character not in "0123456789abcdefABCDEF" for character in revision)
                or not isinstance(reason, str)
                or not reason.strip()
                or not isinstance(files, dict)
                or root == "."
            ):
                invalid_supplement_manifests.append(f"{identity}:invalid-metadata")
                continue
            declared_files = {}
            manifest_valid = True
            material_root = manifest_path.parent.resolve()
            for declared_path, expected_hash in files.items():
                if not isinstance(declared_path, str):
                    normalized = str(declared_path)
                    invalid_supplement_manifests.append(
                        f"{identity}:invalid-path:{normalized}"
                    )
                    manifest_valid = False
                    continue
                normalized = declared_path.replace("\\", "/")
                posix_path = PurePosixPath(normalized)
                windows_path = PureWindowsPath(declared_path)
                if (
                    not normalized
                    or posix_path.is_absolute()
                    or windows_path.is_absolute()
                    or windows_path.drive
                    or any(part in {".", ".."} for part in posix_path.parts)
                ):
                    invalid_supplement_manifests.append(
                        f"{identity}:invalid-path:{normalized}"
                    )
                    manifest_valid = False
                    continue
                file_path = (material_root / Path(*posix_path.parts)).resolve()
                try:
                    file_path.relative_to(material_root)
                except ValueError:
                    invalid_supplement_manifests.append(
                        f"{identity}:invalid-path:{normalized}"
                    )
                    manifest_valid = False
                    continue
                coverage_path_name = f"{root}/{posix_path.as_posix()}"
                declared_files[coverage_path_name] = expected_hash
                if not file_path.is_file():
                    invalid_supplement_manifests.append(
                        f"{identity}:missing-file:{coverage_path_name}"
                    )
                    manifest_valid = False
                elif not isinstance(expected_hash, str) or hashlib.sha256(
                    file_path.read_bytes()
                ).hexdigest() != expected_hash:
                    invalid_supplement_manifests.append(
                        f"{identity}:hash-mismatch:{coverage_path_name}"
                    )
                    manifest_valid = False
            manifests.append(
                {
                    "repository": repository,
                    "revision": revision,
                    "root": root,
                    "files": declared_files,
                    "valid": manifest_valid,
                }
            )

    for review in reference_reviews:
        if (
            review.get("kind") != "missing-relative-reference"
            or review.get("blocking_for_standalone") is not True
        ):
            continue
        source_path = normalized_skill_path(review.get("source_path"))
        skill = source_path.split("/", 1)[0]
        catalog_entry = included.get(skill)
        if not catalog_entry:
            continue
        repository = str(catalog_entry.get("source", ""))
        target = normalized_reference_target(str(review.get("target", "")))
        matches = [
            manifest
            for manifest in manifests
            if manifest["valid"]
            and manifest["repository"] == repository
            and target in manifest["files"]
        ]
        if not matches:
            missing_required_supplements.append(f"{skill}:{repository}:{target}")
            continue
        candidate_missing_coverage = []
        candidate_unread_files = []
        covered_match_found = False
        for manifest in matches:
            identity = (
                f"{skill}:{repository}@{manifest['revision']}:{manifest['root']}"
            )
            source_coverage = coverage_sources.get(skill)
            supplement_entries = (
                source_coverage.get("supplements", [])
                if isinstance(source_coverage, dict)
                else []
            )
            if not isinstance(supplement_entries, list):
                supplement_entries = []
            coverage_entry = next(
                (
                    item
                    for item in supplement_entries
                    if isinstance(item, dict)
                    and item.get("source_repository") == repository
                    and item.get("source_revision") == manifest["revision"]
                    and isinstance(item.get("root"), str)
                    and item["root"].replace("\\", "/") == manifest["root"]
                ),
                None,
            )
            if coverage_entry is None:
                candidate_missing_coverage.append(identity)
                continue
            coverage_files = coverage_entry.get("files", [])
            if not isinstance(coverage_files, list):
                coverage_files = []
            declared_coverage = {
                item["path"].replace("\\", "/"): item
                for item in coverage_files
                if isinstance(item, dict)
                and isinstance(item.get("path"), str)
            }
            manifest_unread_files = []
            for required_path in sorted(manifest["files"]):
                item = declared_coverage.get(required_path)
                if item is None or item.get("status") not in {"read", "excluded"}:
                    manifest_unread_files.append(f"{skill}:{required_path}")
                elif item.get("status") == "excluded" and not (
                    isinstance(item.get("reason"), str) and item["reason"].strip()
                ):
                    manifest_unread_files.append(f"{skill}:{required_path}")
            if manifest_unread_files:
                candidate_unread_files.extend(manifest_unread_files)
                continue
            covered_match_found = True
            break
        if not covered_match_found:
            missing_supplement_coverage.extend(candidate_missing_coverage)
            unread_supplement_files.extend(candidate_unread_files)

    for skill in sorted(included):
        dossier_path = dossiers_root / f"{skill}.md"
        unit_path = units_root / f"{skill}.jsonl"
        source_coverage = coverage_sources.get(skill)
        if not dossier_path.is_file():
            missing_dossiers.append(skill)
        else:
            headings = {
                line[3:].strip()
                for line in dossier_path.read_text(
                    encoding="utf-8", errors="replace"
                ).splitlines()
                if line.startswith("## ")
            }
            missing_sections = [
                section for section in DOSSIER_SECTIONS if section not in headings
            ]
            if missing_sections:
                invalid_dossiers.append(
                    {"source": skill, "missing_sections": missing_sections}
                )

        if not unit_path.is_file():
            missing_unit_files.append(skill)
        else:
            records, errors = read_jsonl(unit_path)
            jsonl_errors.extend(errors)
            if not records:
                invalid_units.append(f"{skill}:no-units")
            for unit in records:
                unit_errors, excerpt_matches = verify_unit(unit, skills_root)
                invalid_units.extend(unit_errors)
                if not excerpt_matches:
                    source_excerpt_mismatches.append(
                        str(unit.get("id", "<missing-id>"))
                    )
                if not unit_errors:
                    validated_units += 1

        if not isinstance(source_coverage, dict):
            missing_coverage_sources.append(skill)
            continue
        source_files = source_coverage.get("files", [])
        if not isinstance(source_files, list):
            source_files = []
        declared_files = {
            normalized_skill_path(item.get("path")): item
            for item in source_files
            if isinstance(item, dict)
        }
        root = roots_by_path.get(skill, {})
        entry_path = normalized_skill_path(
            root.get("skill_path", f"{skill}/SKILL.md")
        )
        for required_path in sorted(
            reachable_skill_files(skills_root, entry_path)
        ):
            item = declared_files.get(required_path)
            if item is None:
                unread_required_files.append(required_path)
                continue
            status = item.get("status")
            if status == "read":
                continue
            if (
                status == "excluded"
                and isinstance(item.get("reason"), str)
                and item["reason"].strip()
            ):
                continue
            unread_required_files.append(required_path)

    missing_deferred_dossiers = []
    missing_deferred_coverage = []
    for skill in sorted(deferred):
        dossier_path = dossiers_root / f"{skill}.md"
        source_coverage = coverage_sources.get(skill)
        if not dossier_path.is_file():
            missing_deferred_dossiers.append(skill)
        else:
            headings = {
                line[3:].strip()
                for line in dossier_path.read_text(
                    encoding="utf-8", errors="replace"
                ).splitlines()
                if line.startswith("## ")
            }
            missing_sections = [
                section for section in DOSSIER_SECTIONS if section not in headings
            ]
            if missing_sections:
                invalid_dossiers.append(
                    {"source": skill, "missing_sections": missing_sections}
                )
        if not isinstance(source_coverage, dict):
            missing_deferred_coverage.append(skill)
            continue
        source_files = source_coverage.get("files", [])
        if not isinstance(source_files, list):
            source_files = []
        declared_files = {
            normalized_skill_path(item.get("path")): item
            for item in source_files
            if isinstance(item, dict)
        }
        root = roots_by_path.get(skill, {})
        entry_path = normalized_skill_path(
            root.get("skill_path", f"{skill}/SKILL.md")
        )
        for required_path in sorted(
            reachable_skill_files(skills_root, entry_path)
        ):
            item = declared_files.get(required_path)
            if item is None:
                unread_required_files.append(required_path)
                continue
            status = item.get("status")
            if status == "read":
                continue
            if (
                status == "excluded"
                and isinstance(item.get("reason"), str)
                and item["reason"].strip()
            ):
                continue
            unread_required_files.append(required_path)

    failures = (
        missing_dossiers
        + missing_unit_files
        + missing_coverage_sources
        + missing_deferred_dossiers
        + missing_deferred_coverage
        + invalid_dossiers
        + invalid_units
        + jsonl_errors
        + source_excerpt_mismatches
        + unread_required_files
        + invalid_supplement_manifests
        + missing_required_supplements
        + missing_supplement_coverage
        + unread_supplement_files
    )
    return {
        "deferred_sources": len(deferred),
        "included_sources": len(included),
        "invalid_dossiers": invalid_dossiers,
        "invalid_supplement_manifests": sorted(set(invalid_supplement_manifests)),
        "invalid_units": sorted(set(invalid_units)),
        "jsonl_errors": sorted(jsonl_errors),
        "missing_coverage_sources": missing_coverage_sources,
        "missing_deferred_coverage": missing_deferred_coverage,
        "missing_deferred_dossiers": missing_deferred_dossiers,
        "missing_dossiers": missing_dossiers,
        "missing_required_supplements": sorted(set(missing_required_supplements)),
        "missing_supplement_coverage": sorted(set(missing_supplement_coverage)),
        "missing_unit_files": missing_unit_files,
        "ok": not failures,
        "source_excerpt_mismatches": sorted(set(source_excerpt_mismatches)),
        "unread_required_files": sorted(set(unread_required_files)),
        "unread_supplement_files": sorted(set(unread_supplement_files)),
        "validated_units": validated_units,
    }


PHASE4_RELATIONSHIP_TYPES = {
    "duplicate",
    "complementary",
    "conditional-variant",
    "conflict",
    "strong-dependency",
}
PHASE4_LOSSY_ACTIONS = {"merge", "rewrite", "exclude"}


def nonempty_text(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _verify_phase4_legacy(
    inventory_path: Path,
    units_root: Path,
    clusters_path: Path,
    decisions_path: Path,
) -> dict[str, object]:
    inventory = json.loads(inventory_path.read_text(encoding="utf-8"))
    cluster_data = json.loads(clusters_path.read_text(encoding="utf-8"))
    decisions, decision_jsonl_errors = read_jsonl(decisions_path)

    included_skills = sorted(
        str(entry.get("skill"))
        for entry in inventory.get("catalog_entries", [])
        if entry.get("scope") == "included" and entry.get("resolution") == "resolved"
    )
    unit_ids = set()
    jsonl_errors = list(decision_jsonl_errors)
    for skill in included_skills:
        records, errors = read_jsonl(units_root / f"{skill}.jsonl")
        jsonl_errors.extend(errors)
        unit_ids.update(
            str(record["id"])
            for record in records
            if nonempty_text(record.get("id"))
        )

    clusters = cluster_data.get("clusters", [])
    relationships = cluster_data.get("relationships", [])
    if not isinstance(clusters, list):
        clusters = []
    if not isinstance(relationships, list):
        relationships = []
    cluster_ids = {
        str(cluster.get("id"))
        for cluster in clusters
        if isinstance(cluster, dict) and nonempty_text(cluster.get("id"))
    }

    invalid_clusters = []
    assignments: dict[str, int] = {}
    for index, cluster in enumerate(clusters, 1):
        if not isinstance(cluster, dict):
            invalid_clusters.append(f"cluster:{index}:not-an-object")
            continue
        cluster_id = str(cluster.get("id", f"cluster:{index}"))
        for field in (
            "candidate_responsibility",
            "input_boundary",
            "output_boundary",
        ):
            if not nonempty_text(cluster.get(field)):
                invalid_clusters.append(
                    f"{cluster_id}:invalid-{field.replace('_', '-')}"
                )
        for field in ("upstream_dependencies", "downstream_dependencies"):
            if not isinstance(cluster.get(field), list):
                invalid_clusters.append(
                    f"{cluster_id}:invalid-{field.replace('_', '-')}"
                )
        member_ids = cluster.get("unit_ids", [])
        if not isinstance(member_ids, list):
            invalid_clusters.append(f"{cluster_id}:invalid-unit-ids")
            continue
        for unit_id in member_ids:
            if isinstance(unit_id, str):
                assignments[unit_id] = assignments.get(unit_id, 0) + 1

    invalid_relationships = []
    invalid_conflicts = []
    dangling_unit_references = []
    dangling_cluster_references = []
    for index, relationship in enumerate(relationships, 1):
        if not isinstance(relationship, dict):
            invalid_relationships.append(f"relationship:{index}:not-an-object")
            continue
        relationship_id = str(relationship.get("id", f"relationship:{index}"))
        relationship_type = relationship.get("type")
        if relationship_type not in PHASE4_RELATIONSHIP_TYPES:
            invalid_relationships.append(
                f"{relationship_id}:invalid-type:{relationship_type}"
            )
        for field in ("source_unit_id", "target_unit_id"):
            reference = relationship.get(field)
            if isinstance(reference, str) and reference not in unit_ids:
                dangling_unit_references.append(f"{relationship_id}:{reference}")
        cluster_reference = relationship.get("cluster_id")
        if isinstance(cluster_reference, str) and cluster_reference not in cluster_ids:
            dangling_cluster_references.append(
                f"{relationship_id}:{cluster_reference}"
            )
        if relationship_type == "conditional-variant" and not nonempty_text(
            relationship.get("condition")
        ):
            invalid_relationships.append(f"{relationship_id}:missing-condition")
        if relationship_type == "conflict":
            if relationship.get("resolution_status") not in {"unresolved", "resolved"}:
                invalid_conflicts.append(
                    f"{relationship_id}:missing-resolution-status"
                )
            if not nonempty_text(relationship.get("evidence")):
                invalid_conflicts.append(f"{relationship_id}:missing-evidence")

    invalid_decisions = []
    disposition_counts: dict[str, int] = {}
    for index, decision in enumerate(decisions, 1):
        decision_id = str(decision.get("id", f"decision:{index}"))
        action = decision.get("action")
        decision_units = decision.get("unit_ids", [])
        if not isinstance(decision_units, list):
            invalid_decisions.append(f"{decision_id}:invalid-unit-ids")
            decision_units = []
        for unit_id in decision_units:
            if not isinstance(unit_id, str):
                continue
            if unit_id not in unit_ids:
                dangling_unit_references.append(f"{decision_id}:{unit_id}")
            elif action in {"defer", "exclude"}:
                disposition_counts[unit_id] = disposition_counts.get(unit_id, 0) + 1
        cluster_reference = decision.get("cluster_id")
        if isinstance(cluster_reference, str) and cluster_reference not in cluster_ids:
            dangling_cluster_references.append(f"{decision_id}:{cluster_reference}")
        required_fields = []
        if action in {"defer", "exclude"}:
            required_fields.append("rationale")
        if action in PHASE4_LOSSY_ACTIONS or action == "defer":
            required_fields.extend(("potential_loss", "verification_method"))
        for field in required_fields:
            if not nonempty_text(decision.get(field)):
                invalid_decisions.append(
                    f"{decision_id}:missing-{field.replace('_', '-')}"
                )

    unassigned_units = sorted(
        unit_id
        for unit_id in unit_ids
        if assignments.get(unit_id, 0) + disposition_counts.get(unit_id, 0) == 0
    )
    duplicate_unit_assignments = sorted(
        unit_id for unit_id in unit_ids if assignments.get(unit_id, 0) > 1
    )
    conflicting_unit_dispositions = sorted(
        unit_id
        for unit_id in unit_ids
        if assignments.get(unit_id, 0) + disposition_counts.get(unit_id, 0) > 1
    )
    dangling_unit_references.extend(
        f"cluster-assignment:{unit_id}"
        for unit_id in assignments
        if unit_id not in unit_ids
    )
    failures = (
        invalid_clusters
        + invalid_relationships
        + invalid_conflicts
        + invalid_decisions
        + jsonl_errors
        + unassigned_units
        + duplicate_unit_assignments
        + conflicting_unit_dispositions
        + dangling_unit_references
        + dangling_cluster_references
    )
    return {
        "conflicting_unit_dispositions": conflicting_unit_dispositions,
        "dangling_cluster_references": sorted(set(dangling_cluster_references)),
        "dangling_unit_references": sorted(set(dangling_unit_references)),
        "duplicate_unit_assignments": duplicate_unit_assignments,
        "included_units": len(unit_ids),
        "invalid_clusters": sorted(set(invalid_clusters)),
        "invalid_conflicts": sorted(set(invalid_conflicts)),
        "invalid_decisions": sorted(set(invalid_decisions)),
        "invalid_relationships": sorted(set(invalid_relationships)),
        "jsonl_errors": sorted(jsonl_errors),
        "ok": not failures,
        "unassigned_units": unassigned_units,
        "validated_clusters": len(clusters) - len(
            {error.split(":invalid-", 1)[0] for error in invalid_clusters}
        ),
    }


PHASE4_ACTIONS = {
    "defer",
    "exclude",
    "merge",
    "rewrite",
    "conflict-resolution",
    "conflict-tracking",
    "dependency-boundary",
}


def _phase4_report() -> dict[str, object]:
    return {
        "conflicting_unit_dispositions": [],
        "dangling_cluster_references": [],
        "dangling_unit_references": [],
        "duplicate_cluster_ids": [],
        "duplicate_decision_ids": [],
        "duplicate_relationship_edges": [],
        "duplicate_relationship_ids": [],
        "duplicate_unit_assignments": [],
        "duplicate_unit_ids": [],
        "included_units": 0,
        "input_errors": [],
        "invalid_clusters": [],
        "invalid_conflicts": [],
        "invalid_decisions": [],
        "invalid_relationships": [],
        "jsonl_errors": [],
        "ok": False,
        "unassigned_units": [],
        "unhandled_responsibility_overlaps": [],
        "validated_clusters": 0,
    }


def _load_phase4_json(path: Path, label: str, report: dict[str, object]) -> object | None:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        report["input_errors"].append(f"{label}:{type(error).__name__}")
        return None
    if not isinstance(value, dict):
        report["input_errors"].append(f"{label}:top-level-not-an-object")
        return None
    return value


def _load_phase4_jsonl(path: Path, label: str, report: dict[str, object]) -> list[dict[str, object]]:
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as error:
        report["input_errors"].append(f"{label}:{type(error).__name__}")
        return []
    records = []
    for number, line in enumerate(text.splitlines(), 1):
        if not line.strip():
            continue
        try:
            value = json.loads(line)
        except json.JSONDecodeError as error:
            report["jsonl_errors"].append(f"{path.name}:{number}:{error.msg}")
            continue
        if not isinstance(value, dict):
            report["jsonl_errors"].append(f"{path.name}:{number}:not-an-object")
            continue
        records.append(value)
    return records


def _duplicates(values: list[str]) -> list[str]:
    return sorted({value for value in values if values.count(value) > 1})


def _safe_path_component(value: object) -> bool:
    if not nonempty_text(value):
        return False
    posix_path = PurePosixPath(value)
    windows_path = PureWindowsPath(value)
    return (
        not posix_path.is_absolute()
        and not windows_path.is_absolute()
        and not windows_path.drive
        and len(posix_path.parts) == 1
        and len(windows_path.parts) == 1
        and value not in {".", ".."}
    )


def verify_phase4(
    inventory_path: Path,
    units_root: Path,
    clusters_path: Path,
    decisions_path: Path,
) -> dict[str, object]:
    report = _phase4_report()
    inventory = _load_phase4_json(inventory_path, "inventory", report)
    cluster_data = _load_phase4_json(clusters_path, "clusters", report)
    decisions = _load_phase4_jsonl(decisions_path, "decisions", report)

    included_skills = []
    if inventory is not None:
        entries = inventory.get("catalog_entries")
        if not isinstance(entries, list):
            report["input_errors"].append("inventory:invalid-catalog-entries")
        else:
            for index, entry in enumerate(entries, 1):
                if not isinstance(entry, dict):
                    report["input_errors"].append(f"inventory:catalog-entry:{index}:not-an-object")
                elif entry.get("scope") == "included" and entry.get("resolution") == "resolved":
                    if _safe_path_component(entry.get("skill")):
                        included_skills.append(entry["skill"])
                    else:
                        report["input_errors"].append(f"inventory:catalog-entry:{index}:invalid-skill")

    units = []
    for skill in sorted(included_skills):
        units.extend(_load_phase4_jsonl(units_root / f"{skill}.jsonl", f"units:{skill}", report))
    unit_ids_list = []
    responsibility_by_unit = {}
    raw_excerpt_by_unit = {}
    for index, unit in enumerate(units, 1):
        unit_id = unit.get("id")
        if not nonempty_text(unit_id):
            report["input_errors"].append(f"units:record:{index}:invalid-id")
            continue
        unit_ids_list.append(unit_id)
        if "responsibility_key" in unit:
            if nonempty_text(unit["responsibility_key"]):
                responsibility_by_unit[unit_id] = unit["responsibility_key"].strip()
            else:
                report["input_errors"].append(f"{unit_id}:invalid-responsibility-key")
        elif "candidate_destination" not in unit:
            report["input_errors"].append(f"{unit_id}:missing-responsibility-key")
        elif nonempty_text(unit["candidate_destination"]):
            responsibility_by_unit[unit_id] = unit["candidate_destination"].strip()
        else:
            report["input_errors"].append(f"{unit_id}:invalid-candidate-destination")
        if nonempty_text(unit.get("raw_excerpt")):
            raw_excerpt_by_unit[unit_id] = unit["raw_excerpt"]
        else:
            report["input_errors"].append(f"{unit_id}:invalid-raw-excerpt")
    report["duplicate_unit_ids"] = _duplicates(unit_ids_list)
    unit_ids = set(unit_ids_list)
    report["included_units"] = len(unit_ids_list)

    clusters = []
    relationships = []
    if cluster_data is not None:
        raw_clusters = cluster_data.get("clusters")
        raw_relationships = cluster_data.get("relationships")
        if not isinstance(raw_clusters, list):
            report["input_errors"].append("clusters:invalid-clusters")
        else:
            clusters = raw_clusters
        if not isinstance(raw_relationships, list):
            report["input_errors"].append("clusters:invalid-relationships")
        else:
            relationships = raw_relationships

    cluster_id_list = [item["id"] for item in clusters if isinstance(item, dict) and nonempty_text(item.get("id"))]
    report["duplicate_cluster_ids"] = _duplicates(cluster_id_list)
    cluster_ids = set(cluster_id_list)
    assignments = {}
    memberships = {}
    valid_cluster_rows = 0
    cluster_dependencies = {}
    for index, cluster in enumerate(clusters, 1):
        row_errors = []
        if not isinstance(cluster, dict):
            report["invalid_clusters"].append(f"cluster:{index}:not-an-object")
            continue
        cluster_id = cluster.get("id") if nonempty_text(cluster.get("id")) else f"cluster:{index}"
        if not nonempty_text(cluster.get("id")):
            row_errors.append(f"{cluster_id}:invalid-id")
        if cluster.get("id") in report["duplicate_cluster_ids"]:
            row_errors.append(f"{cluster_id}:duplicate-id")
        for field in ("candidate_responsibility", "input_boundary", "output_boundary"):
            if not nonempty_text(cluster.get(field)):
                row_errors.append(f"{cluster_id}:invalid-{field.replace('_', '-')}")
        for field in ("upstream_dependencies", "downstream_dependencies"):
            values = cluster.get(field)
            if not isinstance(values, list):
                row_errors.append(f"{cluster_id}:invalid-{field.replace('_', '-')}")
                values = []
            valid_dependencies = set()
            seen = set()
            for value in values:
                if not nonempty_text(value):
                    row_errors.append(f"{cluster_id}:invalid-{field.replace('_', '-')}-member")
                    continue
                if value == cluster_id:
                    row_errors.append(f"{cluster_id}:self-{field.replace('_', '-')}")
                elif value in seen:
                    row_errors.append(f"{cluster_id}:duplicate-{field.replace('_', '-')}:{value}")
                elif value not in cluster_ids:
                    report["dangling_cluster_references"].append(f"{cluster_id}:{value}")
                else:
                    valid_dependencies.add(value)
                seen.add(value)
            cluster_dependencies[(cluster_id, field)] = valid_dependencies
        members = cluster.get("unit_ids")
        if not isinstance(members, list) or not members:
            row_errors.append(f"{cluster_id}:invalid-unit-ids")
            members = []
        seen = set()
        for unit_id in members:
            if not nonempty_text(unit_id):
                row_errors.append(f"{cluster_id}:invalid-unit-id")
                continue
            if unit_id in seen:
                row_errors.append(f"{cluster_id}:duplicate-unit-id:{unit_id}")
            elif unit_id not in unit_ids:
                report["dangling_unit_references"].append(f"cluster-assignment:{unit_id}")
            else:
                assignments[unit_id] = assignments.get(unit_id, 0) + 1
                memberships.setdefault(unit_id, set()).add(cluster_id)
            seen.add(unit_id)
        report["invalid_clusters"].extend(row_errors)
        if not row_errors:
            valid_cluster_rows += 1
    report["validated_clusters"] = valid_cluster_rows

    relationship_id_list = [
        item["id"]
        for item in relationships
        if isinstance(item, dict) and nonempty_text(item.get("id"))
    ]
    report["duplicate_relationship_ids"] = _duplicates(relationship_id_list)
    relationship_edges = {}
    edge_records = {}
    for index, relationship in enumerate(relationships, 1):
        if not isinstance(relationship, dict):
            continue
        raw_kind = relationship.get("type")
        kind = raw_kind if nonempty_text(raw_kind) else None
        raw_source = relationship.get("source_unit_id")
        raw_target = relationship.get("target_unit_id")
        source = raw_source if nonempty_text(raw_source) else None
        target = raw_target if nonempty_text(raw_target) else None
        if kind not in PHASE4_RELATIONSHIP_TYPES or source is None or target is None:
            continue
        endpoints = (source, target) if kind == "strong-dependency" else tuple(sorted((source, target)))
        edge = (kind,) + endpoints
        relationship_edges[index] = edge
        label = relationship.get("id") if nonempty_text(relationship.get("id")) else f"relationship:{index}"
        edge_records.setdefault(edge, []).append(label)
    duplicate_edge_keys = {
        edge for edge, labels in edge_records.items() if len(labels) > 1
    }
    for edge in sorted(duplicate_edge_keys):
        labels = edge_records[edge]
        report["duplicate_relationship_edges"].extend(
            f"{labels[0]},{label}" for label in labels[1:]
        )

    strong_dependency_boundaries = set()
    for index, relationship in enumerate(relationships, 1):
        if not isinstance(relationship, dict) or relationship.get("type") != "strong-dependency":
            continue
        relationship_id = relationship.get("id")
        raw_source = relationship.get("source_unit_id")
        raw_target = relationship.get("target_unit_id")
        raw_cluster_id = relationship.get("cluster_id")
        source = raw_source if nonempty_text(raw_source) else None
        target = raw_target if nonempty_text(raw_target) else None
        cluster_id = raw_cluster_id if nonempty_text(raw_cluster_id) else None
        if (
            not nonempty_text(relationship_id)
            or relationship_id in report["duplicate_relationship_ids"]
            or relationship_edges.get(index) in duplicate_edge_keys
            or source not in unit_ids
            or target not in unit_ids
            or source == target
            or cluster_id not in cluster_ids
            or cluster_id not in memberships.get(source, set()) | memberships.get(target, set())
        ):
            continue
        for source_cluster in memberships.get(source, set()):
            for target_cluster in memberships.get(target, set()):
                if source_cluster != target_cluster:
                    strong_dependency_boundaries.add(
                        (source, target, source_cluster, target_cluster)
                    )

    known_overlap_pairs = set()
    responsibility_groups = {}
    for unit_id, key in responsibility_by_unit.items():
        for cluster_id in memberships.get(unit_id, set()):
            responsibility_groups.setdefault(key, {}).setdefault(cluster_id, set()).add(unit_id)
    for cluster_units in responsibility_groups.values():
        clusters_for_key = sorted(cluster_units)
        for left_index, left in enumerate(clusters_for_key):
            for right in clusters_for_key[left_index + 1:]:
                known_overlap_pairs.update(
                    frozenset((a, b))
                    for a in cluster_units[left]
                    for b in cluster_units[right]
                )

    decision_id_list = [item["id"] for item in decisions if nonempty_text(item.get("id"))]
    report["duplicate_decision_ids"] = _duplicates(decision_id_list)
    conflict_decisions = {}
    boundary_decisions = set()
    overlap_decision_pairs = set()
    dispositions = {}
    for index, decision in enumerate(decisions, 1):
        decision_id = decision.get("id") if nonempty_text(decision.get("id")) else f"decision:{index}"
        raw_action = decision.get("action")
        action = raw_action if nonempty_text(raw_action) else None
        decision_valid = True
        if not nonempty_text(decision.get("id")):
            decision_valid = False
            report["invalid_decisions"].append(f"{decision_id}:invalid-id")
        elif decision_id in report["duplicate_decision_ids"]:
            decision_valid = False
            report["invalid_decisions"].append(f"{decision_id}:duplicate-id")
        if action not in PHASE4_ACTIONS:
            decision_valid = False
            report["invalid_decisions"].append(f"{decision_id}:invalid-action:{raw_action}")

        values = decision.get("unit_ids")
        if not isinstance(values, list) or not values:
            decision_valid = False
            report["invalid_decisions"].append(f"{decision_id}:invalid-unit-ids")
            values = []
        seen = set()
        for unit_id in values:
            if not nonempty_text(unit_id):
                decision_valid = False
                report["invalid_decisions"].append(f"{decision_id}:invalid-unit-id")
                continue
            if unit_id in seen:
                decision_valid = False
                report["invalid_decisions"].append(f"{decision_id}:duplicate-unit-id:{unit_id}")
            elif unit_id not in unit_ids:
                decision_valid = False
                report["dangling_unit_references"].append(f"{decision_id}:{unit_id}")
            seen.add(unit_id)

        legacy_cluster = decision.get("cluster_id")
        if nonempty_text(legacy_cluster) and legacy_cluster not in cluster_ids:
            decision_valid = False
            report["dangling_cluster_references"].append(f"{decision_id}:{legacy_cluster}")

        if action in {"defer", "exclude", "merge", "rewrite", "dependency-boundary"}:
            for field in ("rationale", "potential_loss", "verification_method"):
                if not nonempty_text(decision.get(field)):
                    decision_valid = False
                    report["invalid_decisions"].append(f"{decision_id}:missing-{field.replace('_', '-')}")

        overlap_pair = None
        if action in {"merge", "rewrite"}:
            target = decision.get("target_cluster_id")
            if not nonempty_text(target) or target not in cluster_ids:
                decision_valid = False
                report["invalid_decisions"].append(f"{decision_id}:invalid-target-cluster-id")
                if nonempty_text(target):
                    report["dangling_cluster_references"].append(f"{decision_id}:{target}")
            valid_values = [
                value for value in values if nonempty_text(value) and value in unit_ids
            ]
            pair = frozenset(valid_values)
            if len(values) != 2 or len(valid_values) != 2 or len(pair) != 2:
                decision_valid = False
                report["invalid_decisions"].append(f"{decision_id}:invalid-overlap-endpoints")
            elif pair not in known_overlap_pairs:
                decision_valid = False
                report["invalid_decisions"].append(f"{decision_id}:orphan-overlap-decision")
            elif target not in memberships.get(valid_values[0], set()) | memberships.get(valid_values[1], set()):
                decision_valid = False
                report["invalid_decisions"].append(f"{decision_id}:target-not-endpoint-cluster")
            else:
                overlap_pair = pair

        conflict_id = None
        if action in {"conflict-resolution", "conflict-tracking"}:
            conflict_id = decision.get("conflict_id")
            if not nonempty_text(conflict_id):
                decision_valid = False
                report["invalid_decisions"].append(f"{decision_id}:invalid-conflict-id")
            if not nonempty_text(decision.get("rationale")):
                decision_valid = False
                report["invalid_decisions"].append(f"{decision_id}:missing-rationale")

        boundary = None
        if action == "dependency-boundary":
            source_cluster = decision.get("source_cluster_id")
            target_cluster = decision.get("target_cluster_id")
            if not nonempty_text(source_cluster) or source_cluster not in cluster_ids:
                decision_valid = False
                report["invalid_decisions"].append(f"{decision_id}:invalid-source-cluster-id")
            if not nonempty_text(target_cluster) or target_cluster not in cluster_ids:
                decision_valid = False
                report["invalid_decisions"].append(f"{decision_id}:invalid-target-cluster-id")
            valid_values = [
                value for value in values if nonempty_text(value) and value in unit_ids
            ]
            source_units = [value for value in valid_values if source_cluster in memberships.get(value, set())]
            target_units = [value for value in valid_values if target_cluster in memberships.get(value, set())]
            if len(valid_values) != 2 or len(set(valid_values)) != 2 or len(source_units) != 1 or len(target_units) != 1:
                decision_valid = False
                report["invalid_decisions"].append(f"{decision_id}:invalid-boundary-endpoints")
            else:
                boundary = (
                    source_units[0],
                    target_units[0],
                    source_cluster,
                    target_cluster,
                )
                if source_cluster == target_cluster or boundary not in strong_dependency_boundaries:
                    decision_valid = False
                    report["invalid_decisions"].append(
                        f"{decision_id}:orphan-dependency-boundary"
                    )

        if not decision_valid:
            continue
        if action in {"defer", "exclude"}:
            for unit_id in values:
                dispositions[unit_id] = dispositions.get(unit_id, 0) + 1
        elif action in {"merge", "rewrite"}:
            overlap_decision_pairs.add(overlap_pair)
        elif action in {"conflict-resolution", "conflict-tracking"}:
            conflict_decisions.setdefault(conflict_id, []).append(
                (decision_id, action, set(values), decision)
            )
        elif action == "dependency-boundary":
            boundary_decisions.add(boundary)

    overlap_edges = set()
    conflict_ids = {
        item["id"]
        for item in relationships
        if isinstance(item, dict)
        and item.get("type") == "conflict"
        and nonempty_text(item.get("id"))
    }
    for conflict_id in sorted(set(conflict_decisions) - conflict_ids):
        for decision_id, _, _, _ in conflict_decisions[conflict_id]:
            report["invalid_decisions"].append(
                f"{decision_id}:invalid-conflict-id:{conflict_id}"
            )
    for index, relationship in enumerate(relationships, 1):
        if not isinstance(relationship, dict):
            report["invalid_relationships"].append(f"relationship:{index}:not-an-object")
            continue
        relationship_id = relationship.get("id") if nonempty_text(relationship.get("id")) else f"relationship:{index}"
        raw_kind = relationship.get("type")
        raw_source = relationship.get("source_unit_id")
        raw_target = relationship.get("target_unit_id")
        raw_cluster_id = relationship.get("cluster_id")
        kind = raw_kind if nonempty_text(raw_kind) else None
        source = raw_source if nonempty_text(raw_source) else None
        target = raw_target if nonempty_text(raw_target) else None
        cluster_id = raw_cluster_id if nonempty_text(raw_cluster_id) else None
        relationship_error_counts = {
            key: len(report[key])
            for key in (
                "invalid_relationships",
                "invalid_conflicts",
                "invalid_decisions",
                "dangling_unit_references",
                "dangling_cluster_references",
            )
        }
        if not nonempty_text(relationship.get("id")):
            report["invalid_relationships"].append(f"{relationship_id}:invalid-id")
        if relationship_edges.get(index) in duplicate_edge_keys:
            report["invalid_relationships"].append(f"{relationship_id}:duplicate-edge")
        if kind not in PHASE4_RELATIONSHIP_TYPES:
            report["invalid_relationships"].append(f"{relationship_id}:invalid-type:{raw_kind}")
        for raw_value, value in ((raw_source, source), (raw_target, target)):
            if value is None:
                report["invalid_relationships"].append(f"{relationship_id}:invalid-unit-reference")
            elif value not in unit_ids:
                report["dangling_unit_references"].append(f"{relationship_id}:{raw_value}")
        if source is not None and source == target:
            report["invalid_relationships"].append(f"{relationship_id}:self-reference")
        if cluster_id is None or cluster_id not in cluster_ids:
            report["invalid_relationships"].append(f"{relationship_id}:invalid-cluster-id")
            if cluster_id is not None:
                report["dangling_cluster_references"].append(f"{relationship_id}:{raw_cluster_id}")
        elif cluster_id not in memberships.get(source, set()) | memberships.get(target, set()):
            report["invalid_relationships"].append(f"{relationship_id}:cluster-not-associated")
        if kind == "conditional-variant":
            condition = relationship.get("condition")
            valid = isinstance(condition, dict) and set(condition) == {"source", "target"}
            sides = []
            if valid:
                values = [condition[side] for side in ("source", "target")]
                permission_fields = {"execution_mode", "may_modify", "report_only"}
                if all(
                    isinstance(value, dict) and set(value) == permission_fields
                    for value in values
                ):
                    for value in values:
                        raw_mode = value.get("execution_mode")
                        mode = raw_mode.strip() if nonempty_text(raw_mode) else None
                        may_modify = value.get("may_modify")
                        report_only = value.get("report_only")
                        if (
                            mode is None
                            or type(may_modify) is not bool
                            or type(report_only) is not bool
                        ):
                            valid = False
                            continue
                        sides.append((mode, may_modify, report_only))
                    required_roles = {
                        ("developer-self-check", True, False),
                        ("independent-qa", False, True),
                    }
                    if len(sides) != 2 or set(sides) != required_roles:
                        valid = False
                elif not all(
                    isinstance(value, dict)
                    and set(value) == {"applicability"}
                    and nonempty_text(value.get("applicability"))
                    for value in values
                ):
                    valid = False
            if not valid:
                report["invalid_relationships"].append(f"{relationship_id}:invalid-condition")
        if kind == "conflict":
            raw_status = relationship.get("resolution_status")
            status = raw_status if nonempty_text(raw_status) else None
            if status not in {"resolved", "unresolved"}:
                report["invalid_conflicts"].append(f"{relationship_id}:missing-resolution-status")
            for field in ("source_excerpt", "target_excerpt", "evidence", "design_case"):
                if not nonempty_text(relationship.get(field)):
                    report["invalid_conflicts"].append(f"{relationship_id}:missing-{field.replace('_', '-')}")
            if source in unit_ids and relationship.get("source_excerpt") != raw_excerpt_by_unit.get(source):
                report["invalid_conflicts"].append(f"{relationship_id}:source-excerpt-mismatch")
            if target in unit_ids and relationship.get("target_excerpt") != raw_excerpt_by_unit.get(target):
                report["invalid_conflicts"].append(f"{relationship_id}:target-excerpt-mismatch")
            applicability = relationship.get("applicability_conditions")
            applicability_valid = isinstance(applicability, dict)
            if applicability_valid:
                for side in ("source", "target"):
                    conditions = applicability.get(side)
                    if (
                        not isinstance(conditions, dict)
                        or not conditions
                        or not nonempty_text(conditions.get("execution_mode"))
                    ):
                        applicability_valid = False
            if not applicability_valid:
                report["invalid_conflicts"].append(f"{relationship_id}:invalid-applicability-conditions")
            if status == "resolved" and not nonempty_text(relationship.get("resolution")):
                report["invalid_conflicts"].append(f"{relationship_id}:missing-resolution")
            expected_units = {source, target}
            expected_action = (
                "conflict-resolution" if status == "resolved" else "conflict-tracking"
            )
            valid_conflict_decision = False
            for decision_id, action, decision_units, decision in conflict_decisions.get(relationship_id, []):
                valid = True
                if decision_units != expected_units:
                    valid = False
                    report["invalid_decisions"].append(f"{decision_id}:conflict-endpoints-mismatch")
                if action != expected_action:
                    valid = False
                    report["invalid_decisions"].append(f"{decision_id}:conflict-action-mismatch")
                if decision.get("resolution_status") != status:
                    valid = False
                    report["invalid_decisions"].append(f"{decision_id}:conflict-status-mismatch")
                if status == "resolved":
                    if not nonempty_text(decision.get("resolution")) or decision.get("resolution") != relationship.get("resolution"):
                        valid = False
                        report["invalid_decisions"].append(f"{decision_id}:conflict-resolution-mismatch")
                elif not nonempty_text(decision.get("next_design_case")):
                    valid = False
                    report["invalid_decisions"].append(f"{decision_id}:missing-next-design-case")
                if not nonempty_text(decision.get("rationale")):
                    valid = False
                valid_conflict_decision = valid_conflict_decision or valid
            if not valid_conflict_decision:
                report["invalid_conflicts"].append(f"{relationship_id}:missing-conflict-decision")
        if kind == "strong-dependency" and source in memberships and target in memberships:
            for source_cluster in memberships[source]:
                for target_cluster in memberships[target]:
                    if source_cluster == target_cluster:
                        continue
                    declared = (target_cluster in cluster_dependencies.get((source_cluster, "downstream_dependencies"), set()) and source_cluster in cluster_dependencies.get((target_cluster, "upstream_dependencies"), set()))
                    boundary = (source, target, source_cluster, target_cluster)
                    if not declared and boundary not in boundary_decisions:
                        report["invalid_relationships"].append(f"{relationship_id}:missing-dependency-boundary")
        relationship_valid = (
            nonempty_text(relationship.get("id"))
            and relationship_id not in report["duplicate_relationship_ids"]
            and all(
                len(report[key]) == count
                for key, count in relationship_error_counts.items()
            )
        )
        if relationship_valid:
            overlap_edges.add(frozenset((source, target)))

    responsibility_groups = {}
    for unit_id, key in responsibility_by_unit.items():
        for cluster_id in memberships.get(unit_id, set()):
            responsibility_groups.setdefault(key, {}).setdefault(cluster_id, set()).add(unit_id)
    for key, cluster_units in responsibility_groups.items():
        if len(cluster_units) < 2:
            continue
        covered = True
        clusters_for_key = sorted(cluster_units)
        for left_index, left in enumerate(clusters_for_key):
            for right in clusters_for_key[left_index + 1:]:
                pairs = (
                    frozenset((a, b))
                    for a in cluster_units[left]
                    for b in cluster_units[right]
                )
                if any(
                    pair not in overlap_edges and pair not in overlap_decision_pairs
                    for pair in pairs
                ):
                    covered = False
        if not covered:
            report["unhandled_responsibility_overlaps"].append(f"{key}:{','.join(clusters_for_key)}")

    report["unassigned_units"] = sorted(unit_id for unit_id in unit_ids if assignments.get(unit_id, 0) + dispositions.get(unit_id, 0) == 0)
    report["duplicate_unit_assignments"] = sorted(unit_id for unit_id in unit_ids if assignments.get(unit_id, 0) > 1)
    report["conflicting_unit_dispositions"] = sorted(unit_id for unit_id in unit_ids if assignments.get(unit_id, 0) + dispositions.get(unit_id, 0) > 1)
    for key, value in report.items():
        if isinstance(value, list):
            report[key] = sorted(set(value))
    failure_keys = [key for key, value in report.items() if isinstance(value, list) and value]
    report["ok"] = not failure_keys
    return report


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Verify curated skill assets")
    subparsers = parser.add_subparsers(dest="command", required=True)
    source = subparsers.add_parser("source")
    source.add_argument("--root", type=Path, required=True)
    source.add_argument("--baseline", type=Path, required=True)
    inventory = subparsers.add_parser("inventory")
    inventory.add_argument("--inventory", type=Path, required=True)
    inventory.add_argument("--policy", type=Path, required=True)
    inventory.add_argument("--lock", type=Path, required=True)
    phase2 = subparsers.add_parser("phase2")
    phase2.add_argument("--inventory", type=Path, required=True)
    phase2.add_argument("--gaps", type=Path, required=True)
    phase2.add_argument("--reference-review", type=Path, required=True)
    phase2.add_argument("--dependency-scan", type=Path, required=True)
    phase2.add_argument("--supplements-root", type=Path, required=True)
    phase2.add_argument("--policy", type=Path, required=True)
    phase2.add_argument("--content-root", type=Path, action="append", default=[])
    phase3 = subparsers.add_parser("phase3")
    phase3.add_argument("--inventory", type=Path, required=True)
    phase3.add_argument("--skills-root", type=Path, required=True)
    phase3.add_argument("--dossiers-root", type=Path, required=True)
    phase3.add_argument("--units-root", type=Path, required=True)
    phase3.add_argument("--coverage", type=Path, required=True)
    phase3.add_argument("--reference-review", type=Path, required=True)
    phase3.add_argument("--supplements-root", type=Path, required=True)
    phase4 = subparsers.add_parser("phase4")
    phase4.add_argument("--inventory", type=Path, required=True)
    phase4.add_argument("--units-root", type=Path, required=True)
    phase4.add_argument("--clusters", type=Path, required=True)
    phase4.add_argument("--decisions", type=Path, required=True)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.command == "source":
        report = verify_source(args.root, args.baseline)
        print(json.dumps(report, ensure_ascii=False, sort_keys=True))
        return 0 if report["ok"] else 1
    if args.command == "inventory":
        report = verify_inventory(args.inventory, args.policy, args.lock)
        print(json.dumps(report, ensure_ascii=False, sort_keys=True))
        return 0 if report["ok"] else 1
    if args.command == "phase2":
        report = verify_phase2(
            args.inventory,
            args.gaps,
            args.reference_review,
            args.dependency_scan,
            args.supplements_root,
            args.policy,
            args.content_root,
        )
        print(json.dumps(report, ensure_ascii=False, sort_keys=True))
        return 0 if report["ok"] else 1
    if args.command == "phase3":
        report = verify_phase3(
            args.inventory,
            args.skills_root,
            args.dossiers_root,
            args.units_root,
            args.coverage,
            args.reference_review,
            args.supplements_root,
        )
        print(json.dumps(report, ensure_ascii=False, sort_keys=True))
        return 0 if report["ok"] else 1
    if args.command == "phase4":
        report = verify_phase4(
            args.inventory,
            args.units_root,
            args.clusters,
            args.decisions,
        )
        print(json.dumps(report, ensure_ascii=False, sort_keys=True))
        return 0 if report["ok"] else 1
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
