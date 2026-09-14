import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

from tools.curation import generate_clusters as cluster_generator


ROOT = Path(__file__).resolve().parents[2]
GENERATOR = ROOT / "tools" / "curation" / "generate_clusters.py"
INVENTORY = ROOT / "curation" / "inventory.json"
UNITS_ROOT = ROOT / "curation" / "units"


def run_generator(
    inventory: Path,
    units_root: Path,
    output: Path,
) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    return subprocess.run(
        [
            sys.executable,
            str(GENERATOR),
            "--inventory",
            str(inventory),
            "--units-root",
            str(units_root),
            "--output",
            str(output),
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        env=env,
    )


def included_unit_ids(inventory: Path, units_root: Path) -> set[str]:
    data = json.loads(inventory.read_text(encoding="utf-8"))
    skills = sorted(
        entry["skill"]
        for entry in data["catalog_entries"]
        if entry.get("scope") == "included"
        and entry.get("resolution") == "resolved"
    )
    return {
        record["id"]
        for skill in skills
        for line in (units_root / f"{skill}.jsonl")
        .read_text(encoding="utf-8")
        .splitlines()
        if line.strip()
        for record in [json.loads(line)]
    }


def test_generator_assigns_every_included_unit_once_and_is_deterministic(
    tmp_path: Path,
) -> None:
    first = tmp_path / "first.json"
    second = tmp_path / "second.json"

    first_result = run_generator(INVENTORY, UNITS_ROOT, first)
    second_result = run_generator(INVENTORY, UNITS_ROOT, second)

    assert first_result.returncode == 0, first_result.stderr
    assert second_result.returncode == 0, second_result.stderr
    assert first.read_bytes() == second.read_bytes()

    data = json.loads(first.read_text(encoding="utf-8"))
    assigned = [
        unit_id
        for cluster in data["clusters"]
        for unit_id in cluster["unit_ids"]
    ]
    expected = included_unit_ids(INVENTORY, UNITS_ROOT)
    assert len(expected) == 965
    assert len(assigned) == len(set(assigned))
    assert set(assigned) == expected
    assert all(cluster["unit_ids"] == sorted(cluster["unit_ids"]) for cluster in data["clusters"])
    assert [cluster["id"] for cluster in data["clusters"]] == sorted(
        cluster["id"] for cluster in data["clusters"]
    )
    assert [relationship["id"] for relationship in data["relationships"]] == sorted(
        relationship["id"] for relationship in data["relationships"]
    )
    assert {relationship["type"] for relationship in data["relationships"]} == {
        "duplicate",
        "complementary",
        "conditional-variant",
        "conflict",
        "strong-dependency",
    }

    included_skills = {unit_id.split(":", 1)[0] for unit_id in expected}
    assert all(
        cluster["id"].removeprefix("cluster:") not in included_skills
        and cluster["candidate_responsibility"].strip()
        and cluster["input_boundary"].strip()
        and cluster["output_boundary"].strip()
        for cluster in data["clusters"]
    )
    assert any(
        len({unit_id.split(":", 1)[0] for unit_id in cluster["unit_ids"]}) > 1
        for cluster in data["clusters"]
    )
    clusters_by_skill: dict[str, set[str]] = {}
    for cluster in data["clusters"]:
        for unit_id in cluster["unit_ids"]:
            clusters_by_skill.setdefault(unit_id.split(":", 1)[0], set()).add(
                cluster["id"]
            )
    assert any(len(cluster_ids) > 1 for cluster_ids in clusters_by_skill.values())

    expected_destinations = {
        "frontend-design:unit-016": "cluster:source-metadata-and-provenance",
        "extract-design-system:unit-001": "cluster:external-design-token-extraction-and-normalization",
        "extract-design-system:unit-010": "cluster:external-design-token-extraction-and-normalization",
        "prototype:unit-012": "cluster:divergent-prototyping-and-variant-selection",
        "prototype:unit-019": "cluster:divergent-prototyping-and-variant-selection",
        "writing-plans:unit-011": "cluster:independent-plan-review",
        "vitest:unit-019": "cluster:completion-evidence-gate",
        "qao-gate-interactive-evidence-chain": "cluster:completion-evidence-gate",
        "ai-product-strategy:unit-016": "cluster:ai-model-and-data-architecture",
        "ai-product-strategy:unit-040": "cluster:ai-interaction-and-probabilistic-ux",
        "ai-product-strategy:unit-058": "cluster:ai-organizational-adoption-and-leadership",
    }
    actual_destinations = {
        unit_id: cluster["id"]
        for cluster in data["clusters"]
        for unit_id in cluster["unit_ids"]
        if unit_id in expected_destinations
    }
    assert actual_destinations == expected_destinations
    assert len(cluster_generator.SEMANTIC_OVERRIDES) == len(
        set(cluster_generator.SEMANTIC_OVERRIDES)
    )
    assert all(cluster_generator.SEMANTIC_OVERRIDES.values())

    raw_excerpts = {
        record["id"]: record["raw_excerpt"]
        for path in UNITS_ROOT.glob("*.jsonl")
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
        for record in [json.loads(line)]
    }
    for relationship in data["relationships"]:
        if relationship["type"] == "conflict":
            assert relationship["source_excerpt"] == raw_excerpts[
                relationship["source_unit_id"]
            ]
            assert relationship["target_excerpt"] == raw_excerpts[
                relationship["target_unit_id"]
            ]


def test_generator_rejects_unknown_unit_without_overwriting_output(
    tmp_path: Path,
) -> None:
    inventory = tmp_path / "inventory.json"
    inventory.write_bytes(INVENTORY.read_bytes())
    units_root = tmp_path / "units"
    units_root.mkdir()
    for path in UNITS_ROOT.glob("*.jsonl"):
        (units_root / path.name).write_bytes(path.read_bytes())

    target = units_root / "retro.jsonl"
    unknown = {
        "id": "retro:unit-999",
        "raw_excerpt": "Unknown fixture.",
        "candidate_destination": "retro:unknown-fixture",
    }
    with target.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(unknown) + "\n")

    output = tmp_path / "clusters.json"
    output.write_text("preserve-me\n", encoding="utf-8")
    result = run_generator(inventory, units_root, output)

    assert result.returncode == 1
    assert "unit range coverage mismatch: retro:missing=[]:extra=[999]" in result.stderr
    assert output.read_text(encoding="utf-8") == "preserve-me\n"


def test_generator_rejects_stale_override(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setitem(
        cluster_generator.UNIT_OVERRIDES,
        "missing:unit-001",
        "cluster:context-intake-and-routing",
    )

    with pytest.raises(ValueError, match="stale unit override: missing:unit-001"):
        cluster_generator.build_capability_map(INVENTORY, UNITS_ROOT)


def test_generator_rejects_dangling_relationship_endpoint(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    relationship = dict(cluster_generator.RELATIONSHIPS[0])
    relationship["source_unit_id"] = "missing:unit-001"
    monkeypatch.setattr(cluster_generator, "RELATIONSHIPS", (relationship,))

    with pytest.raises(
        ValueError,
        match="relationship relationship:ai-leadership-duplicate uses unknown unit: missing:unit-001",
    ):
        cluster_generator.build_capability_map(INVENTORY, UNITS_ROOT)


def test_generator_rejects_unknown_inventory_state() -> None:
    inventory = {
        "catalog_entries": [
            {"skill": "retro", "scope": "include", "resolution": "resolved"}
        ]
    }

    with pytest.raises(ValueError, match="inventory: invalid scope at entry 1"):
        cluster_generator.included_skills(inventory)


def test_generator_rejects_unit_id_from_another_skill(tmp_path: Path) -> None:
    units_root = tmp_path / "units"
    units_root.mkdir()
    (units_root / "retro.jsonl").write_text(
        json.dumps({"id": "validate-data:unit-001"}) + "\n",
        encoding="utf-8",
    )

    with pytest.raises(
        ValueError,
        match="units:retro:1: id does not belong to skill: validate-data:unit-001",
    ):
        cluster_generator.load_units(units_root, ["retro"])


def test_generator_rejects_overlapping_static_ranges(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setitem(
        cluster_generator.UNIT_RANGES,
        "retro",
        (
            (1, 5, "cluster:engineering-retrospective-and-improvement"),
            (5, 10, "cluster:engineering-retrospective-and-improvement"),
        ),
    )

    with pytest.raises(ValueError, match="overlapping unit range: retro:5"):
        cluster_generator.build_capability_map(INVENTORY, UNITS_ROOT)


def test_generator_rejects_dangling_cluster_dependency(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    cluster_id = "cluster:context-intake-and-routing"
    metadata = dict(cluster_generator.CLUSTERS[cluster_id])
    metadata["downstream_dependencies"] = ["cluster:missing"]
    monkeypatch.setitem(cluster_generator.CLUSTERS, cluster_id, metadata)

    with pytest.raises(
        ValueError,
        match=(
            "cluster cluster:context-intake-and-routing uses unknown "
            "downstream dependency: cluster:missing"
        ),
    ):
        cluster_generator.build_capability_map(INVENTORY, UNITS_ROOT)
