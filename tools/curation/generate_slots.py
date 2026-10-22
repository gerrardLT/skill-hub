#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import shutil
import tempfile
from pathlib import Path
from typing import Any

SCHEMA_VERSION = "1.0"


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def read_jsonl(root: Path) -> dict[str, dict[str, Any]]:
    records: dict[str, dict[str, Any]] = {}
    for path in sorted(root.glob("*.jsonl")):
        for line in path.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            record = json.loads(line)
            unit_id = record["id"]
            if unit_id in records:
                raise ValueError(f"duplicate unit id: {unit_id}")
            records[unit_id] = record
    return records


def decision_index(path: Path) -> dict[str, list[str]]:
    result: dict[str, list[str]] = {}
    if not path.exists():
        return result
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        decision = json.loads(line)
        for unit_id in decision.get("unit_ids", []):
            result.setdefault(unit_id, []).append(decision["id"])
    return {unit_id: sorted(ids) for unit_id, ids in result.items()}


def json_bytes(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8")


def write_bytes(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)


def batches(clusters: list[dict[str, Any]]) -> dict[str, int]:
    ids = {cluster["id"] for cluster in clusters}
    dependencies = {
        cluster["id"]: set(cluster["upstream_dependencies"]) & ids
        for cluster in clusters
    }

    index = 0
    indices: dict[str, int] = {}
    lowlinks: dict[str, int] = {}
    stack: list[str] = []
    on_stack: set[str] = set()
    components: list[tuple[str, ...]] = []

    def visit(node: str) -> None:
        nonlocal index
        indices[node] = index
        lowlinks[node] = index
        index += 1
        stack.append(node)
        on_stack.add(node)
        for dependency in sorted(dependencies[node]):
            if dependency not in indices:
                visit(dependency)
                lowlinks[node] = min(lowlinks[node], lowlinks[dependency])
            elif dependency in on_stack:
                lowlinks[node] = min(lowlinks[node], indices[dependency])
        if lowlinks[node] == indices[node]:
            component: list[str] = []
            while True:
                member = stack.pop()
                on_stack.remove(member)
                component.append(member)
                if member == node:
                    break
            components.append(tuple(sorted(component)))

    for node in sorted(ids):
        if node not in indices:
            visit(node)

    component_by_node = {
        node: component_index
        for component_index, component in enumerate(components)
        for node in component
    }
    component_dependencies = {
        component_index: {
            component_by_node[dependency]
            for node in component
            for dependency in dependencies[node]
            if component_by_node[dependency] != component_index
        }
        for component_index, component in enumerate(components)
    }
    component_batches: dict[int, int] = {}

    def assign_batch(component_index: int) -> int:
        if component_index not in component_batches:
            upstream_batches = [assign_batch(item) for item in component_dependencies[component_index]]
            component_batches[component_index] = 1 + max(upstream_batches, default=0)
        return component_batches[component_index]

    return {
        node: assign_batch(component_by_node[node])
        for node in sorted(ids)
    }


def skill_markdown(cluster: dict[str, Any]) -> str:
    dependencies = sorted(cluster["upstream_dependencies"])
    dependency_lines = "\n".join(f"- `{item}`" for item in dependencies) or "- None recorded."
    return f"""# {cluster['id'].removeprefix('cluster:')}

Status: draft candidate; source-index skeleton only. This file has not been purified, evaluated, or released.

## Candidate Responsibility

{cluster['candidate_responsibility']}

## Source Boundaries

- Input: {cluster['input_boundary']}
- Output: {cluster['output_boundary']}

## Required Upstream Dependencies

{dependency_lines}

## Source Units

See `provenance.json` for the complete unit-by-unit source index and recorded dispositions.

## Fail-Closed Protocol

Do not execute, publish, or claim completion from this skeleton. Stop when required inputs, permissions, dependency contracts, source evidence, evaluation evidence, or release evidence are missing or unresolved. Never fabricate evidence or treat `not-run`, `pending`, or `draft` as a passing gate.
"""


def contract(cluster: dict[str, Any]) -> dict[str, Any]:
    slot_id = cluster["id"].removeprefix("cluster:")
    dependencies = sorted(cluster["upstream_dependencies"])
    return {
        "artifact_types": ["SKILL.md", "contract.json", "provenance.json"],
        "boundaries": {
            "input": cluster["input_boundary"],
            "output": cluster["output_boundary"],
        },
        "dependencies": dependencies,
        "forbidden_actions": [
            "claim purification or release",
            "execute without required permissions and evidence",
            "fabricate or infer missing evidence",
        ],
        "gates": [
            "source-review",
            "semantic-evaluation",
            "dependency-validation",
            "release-evidence",
        ],
        "hard_failures": [
            "missing-source-evidence",
            "missing-required-permission",
            "unresolved-dependency",
            "fabricated-evidence",
            "incorrect-gate-pass",
        ],
        "id": slot_id,
        "inputs": [cluster["input_boundary"]],
        "outputs": [cluster["output_boundary"]],
        "permissions": {"default": "none", "requires_explicit_authorization": True},
        "responsibility": cluster["candidate_responsibility"],
        "schema_version": SCHEMA_VERSION,
        "status": "draft",
        "statuses": ["draft"],
        "version": "0.0.0-draft",
    }


def provenance(
    cluster: dict[str, Any],
    units: dict[str, dict[str, Any]],
    decisions: dict[str, list[str]],
) -> dict[str, Any]:
    mappings = []
    for unit_id in sorted(cluster["unit_ids"]):
        unit = units[unit_id]
        mappings.append(
            {
                "decision_ids": decisions.get(unit_id, []),
                "disposition": unit["status"],
                "line_end": unit["origin_line_end"],
                "line_start": unit["origin_line_start"],
                "source_path": unit["source_path"],
                "unit_id": unit_id,
            }
        )
    return {
        "evaluation": {"semantic": "not-run"},
        "release_evidence": [],
        "schema_version": SCHEMA_VERSION,
        "source_clusters": [cluster["id"]],
        "status": "draft",
        "units": mappings,
    }


def generate(
    clusters_path: Path,
    units_root: Path,
    decisions_path: Path,
    slots_root: Path,
    queue_path: Path,
) -> None:
    cluster_data = read_json(clusters_path)
    clusters = sorted(cluster_data["clusters"], key=lambda item: item["id"])
    units = read_jsonl(units_root)
    decisions = decision_index(decisions_path)

    assigned = [unit_id for cluster in clusters for unit_id in cluster["unit_ids"]]
    if len(assigned) != len(set(assigned)) or set(assigned) != set(units):
        raise ValueError("cluster unit assignments must cover every unit exactly once")
    cluster_ids = {cluster["id"] for cluster in clusters}
    for cluster in clusters:
        dependencies = set(cluster["upstream_dependencies"]) | set(cluster["downstream_dependencies"])
        missing = dependencies - cluster_ids
        if missing:
            raise ValueError(f"unknown dependencies for {cluster['id']}: {sorted(missing)}")

    batch_by_id = batches(clusters)
    queue = {
        "items": [
            {
                "cluster_id": cluster["id"],
                "platform": False,
                "review_status": "pending",
                "slot_id": cluster["id"].removeprefix("cluster:"),
                "topology_batch": batch_by_id[cluster["id"]],
                "unit_count": len(cluster["unit_ids"]),
            }
            for cluster in clusters
        ],
        "schema_version": SCHEMA_VERSION,
        "status": "draft",
    }

    slots_root.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="slots-", dir=slots_root.parent) as temp_name:
        temp_root = Path(temp_name)
        for cluster in clusters:
            slot = temp_root / cluster["id"].removeprefix("cluster:")
            write_bytes(slot / "SKILL.md", skill_markdown(cluster).encode("utf-8"))
            write_bytes(slot / "contract.json", json_bytes(contract(cluster)))
            write_bytes(slot / "provenance.json", json_bytes(provenance(cluster, units, decisions)))
        released_v2 = slots_root / "v2"
        if released_v2.exists():
            shutil.copytree(released_v2, temp_root / "v2")
        if slots_root.exists():
            shutil.rmtree(slots_root)
        os.replace(temp_root, slots_root)
    write_bytes(queue_path, json_bytes(queue))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate deterministic draft slot skeletons")
    parser.add_argument("--clusters", type=Path, default=Path("curation/clusters.json"))
    parser.add_argument("--units-root", type=Path, default=Path("curation/units"))
    parser.add_argument("--decisions", type=Path, default=Path("curation/decisions.jsonl"))
    parser.add_argument("--slots-root", type=Path, default=Path("slots"))
    parser.add_argument("--review-queue", type=Path, default=Path("curation/slot-review-queue.json"))
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    generate(args.clusters, args.units_root, args.decisions, args.slots_root, args.review_queue)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
