#!/usr/bin/env python3
"""Verify Phase 6 slot coverage and release dispositions by slot identity."""
from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

FINAL_DISPOSITIONS = {"released", "unreleased"}


def _load(path: Path, errors: list[str]) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"cannot parse {path}: {exc}")
        return None


def _load_units(root: Path, errors: list[str]) -> dict[str, dict[str, Any]]:
    units: dict[str, dict[str, Any]] = {}
    for path in sorted(root.glob("*.jsonl")):
        for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            if not line.strip():
                continue
            try:
                unit = json.loads(line)
                unit_id = unit["id"]
            except (json.JSONDecodeError, KeyError, TypeError) as exc:
                errors.append(f"cannot parse {path}:{line_number}: {exc}")
                continue
            if unit_id in units:
                errors.append(f"duplicate source unit id: {unit_id}")
            else:
                units[unit_id] = unit
    return units


def _nonempty(value: Any) -> bool:
    return isinstance(value, list) and bool(value) and all(item not in (None, "", [], {}) for item in value)


def verify(
    clusters_path: Path,
    units_root: Path,
    slots_root: Path,
    queue_path: Path,
    status_path: Path,
    inventory_path: Path | None = None,
) -> dict[str, Any]:
    errors: list[str] = []
    clusters_doc = _load(clusters_path, errors) or {}
    queue_doc = _load(queue_path, errors) or {}
    status_doc = _load(status_path, errors) or {}
    units = _load_units(units_root, errors)
    clusters = clusters_doc.get("clusters", [])
    cluster_ids = {item.get("id") for item in clusters if isinstance(item, dict) and item.get("id")}
    if len(cluster_ids) != len(clusters):
        errors.append("cluster ids must be present and unique")

    schema = _load(slots_root / "schema.json", errors) or {}
    validator = Draft202012Validator(schema)
    contracts: dict[str, dict[str, Any]] = {}
    provenances: dict[str, dict[str, Any]] = {}
    for slot_dir in sorted(path for path in slots_root.iterdir() if path.is_dir()):
        contract = _load(slot_dir / "contract.json", errors)
        provenance = _load(slot_dir / "provenance.json", errors)
        if not isinstance(contract, dict) or not isinstance(provenance, dict):
            continue
        schema_errors = sorted(validator.iter_errors(contract), key=lambda item: list(item.absolute_path))
        if schema_errors:
            errors.append(f"invalid contract for {slot_dir.name}: {schema_errors[0].message}")
        slot_id = contract.get("id")
        if slot_id != slot_dir.name or slot_id in contracts:
            errors.append(f"slot id mismatch or duplicate: {slot_dir.name}")
            continue
        contracts[slot_id] = contract
        provenances[slot_id] = provenance

    queue_items = queue_doc.get("items", []) if isinstance(queue_doc, dict) else []
    status_items = status_doc.get("items", []) if isinstance(status_doc, dict) else []
    queue_by_slot = {item.get("slot_id"): item for item in queue_items if isinstance(item, dict) and item.get("slot_id")}
    status_by_slot = {item.get("slot_id"): item for item in status_items if isinstance(item, dict) and item.get("slot_id")}
    if len(queue_by_slot) != len(queue_items):
        errors.append("queue slot ids must be present and unique")
    if len(status_by_slot) != len(status_items):
        errors.append("status-list slot ids must be present and unique")
    if set(status_by_slot) != set(contracts):
        errors.append("status-list slot ids do not match materialized slots")

    mappings: list[dict[str, Any]] = []
    for slot_id, contract in sorted(contracts.items()):
        provenance = provenances[slot_id]
        item = status_by_slot.get(slot_id, {})
        queue_item = queue_by_slot.get(slot_id)
        source_clusters = provenance.get("source_clusters", [])
        if not isinstance(source_clusters, list) or not source_clusters or any(value not in cluster_ids for value in source_clusters):
            errors.append(f"invalid source clusters for {slot_id}")
        if provenance.get("id", slot_id) != slot_id or provenance.get("version", contract.get("version")) != contract.get("version") or provenance.get("status") != contract.get("status"):
            errors.append(f"slot provenance identity mismatch for {slot_id}")
        if item.get("cluster_ids") != source_clusters:
            errors.append(f"release status cluster mapping mismatch for {slot_id}")
        if item.get("materialization_status") != contract.get("status"):
            errors.append(f"materialization status mismatch for {slot_id}")
        if queue_item and queue_item.get("review_status") == "pending" and contract.get("status") != "draft":
            errors.append(f"pending queue item must describe draft materialization for {slot_id}")

        disposition = item.get("disposition")
        if disposition not in FINAL_DISPOSITIONS:
            errors.append(f"Phase 6 disposition is not final for {slot_id}: {disposition}")
        elif disposition == "released":
            if not _nonempty(item.get("evaluation_references")) or not _nonempty(item.get("release_evidence")):
                errors.append(f"released slot lacks evidence: {slot_id}")
            review = item.get("review")
            if not isinstance(review, dict) or review.get("human_review") in (None, "", False):
                errors.append(f"released slot lacks valid review evidence: {slot_id}")
        else:
            if item.get("reason") in (None, "") or not _nonempty(item.get("retained_source_skills")) or not _nonempty(item.get("blocking_gaps")):
                errors.append(f"unreleased slot lacks retained source or blocking gaps: {slot_id}")

        source_mappings = provenance.get("units", provenance.get("unit_mappings", []))
        mappings.extend(value for value in source_mappings if isinstance(value, dict))

    counts = Counter(item.get("unit_id") for item in mappings)
    canonical_slot_ids = {cluster_id.removeprefix("cluster:") for cluster_id in cluster_ids}
    canonical_mappings = [
        item
        for slot_id in canonical_slot_ids
        for item in provenances.get(slot_id, {}).get("units", [])
        if isinstance(item, dict)
    ]
    canonical_counts = Counter(item.get("unit_id") for item in canonical_mappings)
    for unit_id in sorted(set(units) | set(canonical_counts)):
        if canonical_counts[unit_id] != 1:
            errors.append(f"unit must occur exactly once in canonical slot provenance: {unit_id} ({canonical_counts[unit_id]})")
    for mapping in mappings:
        unit = units.get(mapping.get("unit_id"))
        if unit is None:
            errors.append(f"unknown source unit: {mapping.get('unit_id')}")
            continue
        expected = (unit.get("source_path"), unit.get("origin_line_start"), unit.get("origin_line_end"))
        actual = (mapping.get("source_path"), mapping.get("line_start"), mapping.get("line_end"))
        if actual != expected:
            errors.append(f"unit coordinates differ from source record: {mapping.get('unit_id')}")

    return {
        "gate": "phase-6-slot-coverage-release",
        "ok": not errors,
        "cluster_count": len(cluster_ids),
        "slot_count": len(contracts),
        "unit_count": len(units),
        "mapped_unit_count": len(canonical_counts),
        "errors": errors,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--clusters", type=Path, default=Path("curation/clusters.json"))
    parser.add_argument("--units-root", type=Path, default=Path("curation/units"))
    parser.add_argument("--slots-root", type=Path, default=Path("slots"))
    parser.add_argument("--review-queue", type=Path, default=Path("curation/slot-review-queue.json"))
    parser.add_argument("--release-status", type=Path, default=Path("curation/slot-release-status.json"))
    parser.add_argument("--inventory", type=Path, default=Path("curation/inventory.json"))
    args = parser.parse_args()
    result = verify(args.clusters, args.units_root, args.slots_root, args.review_queue, args.release_status, args.inventory)
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
