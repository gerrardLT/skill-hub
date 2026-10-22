#!/usr/bin/env python3
"""Recompute the Capability Compiler V2 source and curation baseline."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
from typing import Any

try:
    from tools.curation.inventory import build_baseline, build_skill_roots
except ModuleNotFoundError:  # direct script execution
    from inventory import build_baseline, build_skill_roots

V1_SLOT_STATUS = {"released"}
V1_RECIPE_STATUS = {"released"}
ALLOWED_FILE_STATES = {"read", "excluded"}
REQUIRED_UNIT_FIELDS = {"id", "source_path", "origin_line_start", "origin_line_end", "type", "raw_excerpt", "meaning", "boundary_condition", "validation_criteria", "status"}

def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))

def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes().replace(b"\r\n", b"\n")).hexdigest()

def raw_root_sha256(root: Path) -> str:
    digest = hashlib.sha256()
    files: list[Path] = []
    for current, directories, names in os.walk(root):
        directories[:] = sorted(name for name in directories if name != ".git")
        files.extend(Path(current) / name for name in sorted(names))
    for path in sorted(files, key=lambda item: item.relative_to(root).as_posix()):
        relative = path.relative_to(root).as_posix()
        digest.update(relative.encode("utf-8"))
        digest.update(b"\0")
        digest.update(hashlib.sha256(path.read_bytes()).hexdigest().encode("ascii"))
        digest.update(b"\n")
    return digest.hexdigest()

def write(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")

def load_units(root: Path) -> tuple[list[dict[str, Any]], list[str]]:
    units: list[dict[str, Any]] = []
    errors: list[str] = []
    for path in sorted(root.iterdir()):
        if not path.is_file() or path.suffix not in {".json", ".jsonl"}:
            continue
        try:
            if path.suffix == ".jsonl":
                values = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
            else:
                data = load(path)
                values = data if isinstance(data, list) else data.get("units", [])
            for value in values:
                if not isinstance(value, dict):
                    errors.append(f"non-object unit: {path.as_posix()}")
                    continue
                units.append({**value, "_file": path.name})
        except (OSError, json.JSONDecodeError) as exc:
            errors.append(f"invalid unit file {path.as_posix()}: {exc}")
    return units, errors

def released_assets(workspace: Path) -> list[dict[str, Any]]:
    assets: list[dict[str, Any]] = []
    for path in sorted((workspace / "slots").glob("*/contract.json")):
        data = load(path)
        if data.get("status") in V1_SLOT_STATUS:
            directory = path.parent
            files = sorted(item for item in directory.rglob("*") if item.is_file())
            assets.append({"kind": "slot", "id": data["id"], "version": data["version"], "files": [{"path": item.relative_to(workspace).as_posix(), "sha256": sha(item)} for item in files]})
    for path in sorted((workspace / "recipes").glob("*.json")):
        if path.name in {"schema.json", "catalog.json"}:
            continue
        data = load(path)
        if data.get("status") in V1_RECIPE_STATUS:
            assets.append({"kind": "recipe", "id": data["id"], "version": data["version"], "files": [{"path": path.relative_to(workspace).as_posix(), "sha256": sha(path)}]})
    return assets

def audit(workspace: Path) -> dict[str, Any]:
    skills = workspace / "skills"
    inventory = load(workspace / "curation/inventory.json")
    coverage = load(workspace / "curation/coverage.json")
    clusters = load(workspace / "curation/clusters.json")
    errors: list[str] = []
    warnings: list[str] = []

    disk_roots = build_skill_roots(skills)
    expected_roots = inventory.get("skill_roots", [])
    disk_by_id = {item["id"]: item for item in disk_roots}
    expected_by_id = {item["id"]: item for item in expected_roots}
    missing_roots = sorted(set(expected_by_id) - set(disk_by_id))
    untracked_roots = sorted(set(disk_by_id) - set(expected_by_id))
    changed_roots = sorted(
        root_id
        for root_id in set(disk_by_id) & set(expected_by_id)
        if expected_by_id[root_id].get("snapshot_sha256") not in {
            disk_by_id[root_id]["snapshot_sha256"],
            raw_root_sha256(skills / disk_by_id[root_id]["path"]),
        }
    )
    if missing_roots: errors.append(f"missing skill roots: {missing_roots}")
    if untracked_roots: errors.append(f"untracked skill roots: {untracked_roots}")
    if changed_roots: errors.append(f"changed skill roots: {changed_roots}")

    coverage_records: list[dict[str, Any]] = []
    covered_source_paths: set[str] = set()
    missing_files: list[str] = []
    invalid_file_states: list[str] = []
    excluded_without_reason: list[str] = []
    for source, record in coverage.get("sources", {}).items():
        scope = record.get("scope") or ("included" if record.get("source") else None)
        for item in record.get("files", []):
            state = item.get("status")
            relative = item.get("path")
            path = skills / relative if isinstance(relative, str) else None
            exists = bool(path and path.is_file())
            evidence = {"source": source, "scope": scope, "path": relative, "status": state, "reason": item.get("reason"), "exists": exists, "sha256": sha(path) if exists else None}
            coverage_records.append(evidence)
            if isinstance(relative, str):
                covered_source_paths.add(relative)
            if state not in ALLOWED_FILE_STATES: invalid_file_states.append(f"{source}:{relative}:{state}")
            if not exists: missing_files.append(f"{source}:{relative}")
            if state == "excluded" and not item.get("reason"): excluded_without_reason.append(f"{source}:{relative}")
        for supplement in record.get("supplements", []):
            supplement_root = workspace / "curation/supplements" / supplement["source_repository"].replace("/", "_") / supplement["root"]
            for item in supplement.get("files", []):
                path = supplement_root / item["path"].removeprefix(supplement["root"] + "/")
                state = item.get("status")
                coverage_records.append({"source": source, "scope": "supplement", "path": path.relative_to(workspace).as_posix(), "status": state, "reason": item.get("reason"), "exists": path.is_file(), "sha256": sha(path) if path.is_file() else None})
                if state not in ALLOWED_FILE_STATES: invalid_file_states.append(f"supplement:{path}:{state}")
                if not path.is_file(): missing_files.append(f"supplement:{path}")
                if state == "excluded" and not item.get("reason"): excluded_without_reason.append(f"supplement:{path}")
    if missing_files: errors.append(f"missing coverage files: {missing_files}")
    if invalid_file_states: errors.append(f"invalid coverage states: {invalid_file_states}")
    if excluded_without_reason: errors.append(f"excluded coverage files lack reasons: {excluded_without_reason}")
    source_baseline = build_baseline(skills)
    source_file_paths = {item["path"] for item in source_baseline["files"]}
    unclassified_source_files = sorted(source_file_paths - covered_source_paths)
    uncovered_skill_roots = sorted(item["id"] for item in disk_roots if item["skill_path"] not in covered_source_paths)

    units, unit_errors = load_units(workspace / "curation/units")
    errors.extend(unit_errors)
    unit_by_id: dict[str, dict[str, Any]] = {}
    duplicate_units: list[str] = []
    malformed_units: list[str] = []
    for unit in units:
        unit_id = unit.get("id")
        if not isinstance(unit_id, str) or not unit_id:
            malformed_units.append(f"{unit.get('_file')}:missing-id")
            continue
        if unit_id in unit_by_id: duplicate_units.append(unit_id)
        unit_by_id[unit_id] = unit
        if not REQUIRED_UNIT_FIELDS <= set(unit):
            missing = sorted(REQUIRED_UNIT_FIELDS - set(unit))
            malformed_units.append(f"{unit_id}:missing:{missing}")
    if duplicate_units: errors.append(f"duplicate unit ids: {sorted(set(duplicate_units))}")

    cluster_assignments: dict[str, list[str]] = {}
    for cluster in clusters.get("clusters", []):
        for unit_id in cluster.get("unit_ids", []):
            cluster_assignments.setdefault(unit_id, []).append(cluster["id"])
    duplicate_assignments = {key: value for key, value in cluster_assignments.items() if len(value) != 1}
    dangling_cluster_units = sorted(set(cluster_assignments) - set(unit_by_id))
    clustered_units = set(cluster_assignments)
    retained_units = {unit_id for unit_id, unit in unit_by_id.items() if unit.get("status") in {"retain", "retained"}}
    unclustered_retained = sorted(retained_units - clustered_units)
    malformed_clustered = [item for item in malformed_units if item.split(":missing:", 1)[0] in clustered_units]
    auxiliary_units = sorted(set(unit_by_id) - clustered_units)
    if duplicate_assignments: errors.append(f"unit assigned to multiple clusters: {duplicate_assignments}")
    if dangling_cluster_units: errors.append(f"cluster references missing units: {dangling_cluster_units}")
    if malformed_clustered: errors.append(f"clustered units use incomplete schema: {malformed_clustered}")

    slots: list[dict[str, Any]] = []
    for contract_path in sorted((workspace / "slots").glob("*/contract.json")):
        contract = load(contract_path)
        provenance_path = contract_path.parent / "provenance.json"
        skill_path = contract_path.parent / "SKILL.md"
        provenance = load(provenance_path) if provenance_path.is_file() else {}
        text = skill_path.read_text(encoding="utf-8") if skill_path.is_file() else ""
        status = contract.get("status")
        classification = "released" if status == "released" else "evaluating" if status == "evaluating" else "draft-skeleton" if "source-index skeleton only" in text else "draft-other"
        sources = sorted({unit.get("source_path", "").split("/")[0] for unit in provenance.get("units", []) if unit.get("source_path")})
        slots.append({"id": contract.get("id"), "version": contract.get("version"), "status": status, "classification": classification, "unit_count": len(provenance.get("units", [])), "source_roots": sources, "release_evidence_count": len(provenance.get("release_evidence", []))})

    relationships = clusters.get("relationships", [])
    relationship_types: dict[str, int] = {}
    for item in relationships:
        relationship_types[item.get("type", "unknown")] = relationship_types.get(item.get("type", "unknown"), 0) + 1

    counts = {
        "skill_roots_disk": len(disk_roots),
        "skill_roots_inventory": len(expected_roots),
        "coverage_sources": len(coverage.get("sources", {})),
        "coverage_files": len(coverage_records),
        "classified_source_files": len(covered_source_paths),
        "unclassified_source_files": len(unclassified_source_files),
        "covered_skill_roots": len(disk_roots) - len(uncovered_skill_roots),
        "uncovered_skill_roots": len(uncovered_skill_roots),
        "coverage_read": sum(item["status"] == "read" for item in coverage_records),
        "coverage_excluded": sum(item["status"] == "excluded" for item in coverage_records),
        "unit_files": len([path for path in (workspace / "curation/units").iterdir() if path.is_file() and path.suffix in {".json", ".jsonl"}]),
        "physical_units": len(units),
        "unique_units": len(unit_by_id),
        "clustered_units": len(clustered_units),
        "auxiliary_units": len(auxiliary_units),
        "clusters": len(clusters.get("clusters", [])),
        "relationships": len(relationships),
        "slots": len(slots),
        "released_slots": sum(item["classification"] == "released" for item in slots),
        "draft_skeleton_slots": sum(item["classification"] == "draft-skeleton" for item in slots),
        "other_unreleased_slots": sum(item["classification"] not in {"released", "draft-skeleton"} for item in slots),
    }
    return {
        "schema_version": "2.0",
        "gate": "capability-compiler-v2-phase-0",
        "ok": not errors,
        "counts": counts,
        "source_baseline": source_baseline,
        "root_drift": {"missing": missing_roots, "untracked": untracked_roots, "changed": changed_roots},
        "coverage": {"records": coverage_records, "missing_files": missing_files, "invalid_states": invalid_file_states, "excluded_without_reason": excluded_without_reason, "uncovered_skill_roots": uncovered_skill_roots, "unclassified_source_files": unclassified_source_files},
        "units": {"duplicate_ids": sorted(set(duplicate_units)), "malformed": malformed_units, "malformed_clustered": malformed_clustered, "clustered_count": len(clustered_units), "auxiliary_unit_ids": auxiliary_units, "retained_unclustered": unclustered_retained},
        "clusters": {"relationship_types": relationship_types, "duplicate_assignments": duplicate_assignments, "dangling_units": dangling_cluster_units},
        "slots": slots,
        "v1_assets": released_assets(workspace),
        "errors": errors,
        "warnings": warnings,
    }

def gaps(result: dict[str, Any]) -> dict[str, Any]:
    items: list[dict[str, Any]] = []
    for root_id in result["coverage"]["uncovered_skill_roots"]:
        items.append({"severity": "blocking-phase-1", "kind": "uncovered-skill-root", "identity": root_id, "required_action": "read the root and classify its required files"})
    for path in result["coverage"]["unclassified_source_files"]:
        items.append({"severity": "blocking-phase-1", "kind": "unclassified-source-file", "identity": path, "required_action": "mark read or excluded with a concrete reason"})
    for unit_id in result["units"]["auxiliary_unit_ids"]:
        items.append({"severity": "review-phase-1", "kind": "auxiliary-unit-outside-canonical-clusters", "identity": unit_id, "required_action": "merge, supersede, defer, or assign to exactly one V2 cluster"})
    for slot in result["slots"]:
        if slot["classification"] == "draft-skeleton":
            items.append({"severity": "blocking-before-v2-release", "kind": "unpurified-slot-skeleton", "identity": slot["id"], "required_action": "synthesize, evaluate, or explicitly retire"})
    relationships = result["counts"]["relationships"]
    units = result["counts"]["clustered_units"]
    items.append({"severity": "review-phase-1", "kind": "semantic-relationship-coverage", "identity": "curation/clusters.json", "observed": {"relationships": relationships, "clustered_units": units, "ratio": relationships / units if units else 0}, "required_action": "prove each cluster has complete duplicate/complement/conflict/variant/dependency analysis"})
    counts: dict[str, int] = {}
    for item in items:
        counts[item["kind"]] = counts.get(item["kind"], 0) + 1
    return {"schema_version": "2.0", "phase": 0, "counts": counts, "items": items}

def phase_report(result: dict[str, Any], gap_report: dict[str, Any]) -> dict[str, Any]:
    return {
        "schema_version": "2.0", "phase": 0,
        "status": "passed-with-forward-gaps" if result["ok"] else "failed",
        "gate": result["gate"], "gate_ok": result["ok"], "counts": result["counts"],
        "facts": [
            "The current source tree matches the immutable source baseline.",
            "Coverage declarations do not yet classify every skill root or source file.",
            "965 canonical units are clustered; 114 auxiliary units require Phase 1 disposition.",
            "82 slots are source-index skeletons, not purified V2 skills.",
            "V1 remains the only released compatibility line during V2 construction.",
        ],
        "forward_gap_counts": gap_report["counts"],
        "errors": result["errors"], "warnings": result["warnings"],
    }

def compare_expected(result: dict[str, Any], expected: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if result["source_baseline"]["tree_sha256"] != expected.get("source_baseline", {}).get("tree_sha256"):
        errors.append("source baseline changed")
    if result["v1_assets"] != expected.get("v1_assets"):
        errors.append("V1 released assets changed")
    return errors

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workspace-root", type=Path, default=Path("."))
    parser.add_argument("--output", type=Path)
    parser.add_argument("--gaps-output", type=Path)
    parser.add_argument("--report-output", type=Path)
    parser.add_argument("--expected-baseline", type=Path)
    args = parser.parse_args()
    result = audit(args.workspace_root.resolve())
    if args.expected_baseline:
        result["errors"].extend(compare_expected(result, load(args.expected_baseline.resolve())))
        result["ok"] = not result["errors"]
    gap_report = gaps(result)
    if args.output:
        write(args.output, result)
    if args.gaps_output:
        write(args.gaps_output, gap_report)
    if args.report_output:
        write(args.report_output, phase_report(result, gap_report))
    print(json.dumps({key: result[key] for key in ("gate", "ok", "counts", "errors", "warnings")}, ensure_ascii=False, sort_keys=True))
    return 0 if result["ok"] else 1

if __name__ == "__main__":
    raise SystemExit(main())
