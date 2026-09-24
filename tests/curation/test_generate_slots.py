import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

from tools.curation import generate_slots


ROOT = Path(__file__).resolve().parents[2]
GENERATOR = ROOT / "tools" / "curation" / "generate_slots.py"
CLUSTERS = ROOT / "curation" / "clusters.json"
UNITS = ROOT / "curation" / "units"
DECISIONS = ROOT / "curation" / "decisions.jsonl"


def tree_hash(root: Path) -> str:
    digest = hashlib.sha256()
    for path in sorted(item for item in root.rglob("*") if item.is_file()):
        digest.update(path.relative_to(root).as_posix().encode("utf-8"))
        digest.update(b"\0")
        digest.update(path.read_bytes())
        digest.update(b"\0")
    return digest.hexdigest()


def run_generator(slots: Path, queue: Path) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    return subprocess.run(
        [
            sys.executable,
            str(GENERATOR),
            "--clusters",
            str(CLUSTERS),
            "--units-root",
            str(UNITS),
            "--decisions",
            str(DECISIONS),
            "--slots-root",
            str(slots),
            "--review-queue",
            str(queue),
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        env=env,
    )


def snapshot(root: Path) -> dict[str, bytes]:
    return {
        path.relative_to(root).as_posix(): path.read_bytes()
        for path in sorted(item for item in root.rglob("*") if item.is_file())
    }


def source_units() -> dict[str, dict[str, object]]:
    return {
        record["id"]: record
        for path in sorted(UNITS.glob("*.jsonl"))
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
        for record in [json.loads(line)]
    }


def test_generator_is_deterministic_and_does_not_modify_skills(tmp_path: Path) -> None:
    skills_before = tree_hash(ROOT / "skills")
    first_slots, second_slots = tmp_path / "first", tmp_path / "second"
    first_queue, second_queue = tmp_path / "first.json", tmp_path / "second.json"

    first = run_generator(first_slots, first_queue)
    second = run_generator(second_slots, second_queue)

    assert first.returncode == 0, first.stderr
    assert second.returncode == 0, second.stderr
    assert snapshot(first_slots) == snapshot(second_slots)
    assert first_queue.read_bytes() == second_queue.read_bytes()
    assert tree_hash(ROOT / "skills") == skills_before


def test_generator_covers_all_clusters_and_units_once(tmp_path: Path) -> None:
    slots, queue_path = tmp_path / "slots", tmp_path / "queue.json"
    result = run_generator(slots, queue_path)
    assert result.returncode == 0, result.stderr

    clusters = json.loads(CLUSTERS.read_text(encoding="utf-8"))["clusters"]
    cluster_ids = {cluster["id"] for cluster in clusters}
    slot_ids = {cluster_id.removeprefix("cluster:") for cluster_id in cluster_ids}
    assert len(cluster_ids) == 88
    assert {path.name for path in slots.iterdir()} == slot_ids
    assert all(
        {path.name for path in slot.iterdir()} == {"SKILL.md", "contract.json", "provenance.json"}
        for slot in slots.iterdir()
    )

    mappings = [
        mapping
        for slot in sorted(slots.iterdir())
        for mapping in json.loads((slot / "provenance.json").read_text(encoding="utf-8"))["units"]
    ]
    assert len(mappings) == 965
    assert len({mapping["unit_id"] for mapping in mappings}) == 965
    assert {mapping["unit_id"] for mapping in mappings} == set(source_units())

    queue = json.loads(queue_path.read_text(encoding="utf-8"))
    assert len(queue["items"]) == 88
    assert {item["cluster_id"] for item in queue["items"]} == cluster_ids
    assert all(item["review_status"] == "pending" for item in queue["items"])
    assert all(item["platform"] is False for item in queue["items"])
    assert all(isinstance(item["topology_batch"], int) and item["topology_batch"] > 0 for item in queue["items"])
    assert sum(item["unit_count"] for item in queue["items"]) == 965


def test_contracts_and_provenance_remain_draft_and_source_faithful(tmp_path: Path) -> None:
    slots, queue_path = tmp_path / "slots", tmp_path / "queue.json"
    result = run_generator(slots, queue_path)
    assert result.returncode == 0, result.stderr

    clusters = {
        cluster["id"]: cluster
        for cluster in json.loads(CLUSTERS.read_text(encoding="utf-8"))["clusters"]
    }
    units = source_units()
    required_contract = {
        "schema_version", "id", "version", "status", "responsibility", "inputs",
        "outputs", "boundaries", "dependencies", "permissions", "statuses", "gates",
        "forbidden_actions", "hard_failures", "artifact_types",
    }
    all_text = queue_path.read_text(encoding="utf-8")
    for slot in sorted(slots.iterdir()):
        contract = json.loads((slot / "contract.json").read_text(encoding="utf-8"))
        provenance = json.loads((slot / "provenance.json").read_text(encoding="utf-8"))
        cluster = clusters[f"cluster:{slot.name}"]
        assert required_contract <= contract.keys()
        assert contract["status"] == "draft"
        assert contract["responsibility"] == cluster["candidate_responsibility"]
        assert set(contract["dependencies"]) <= set(clusters)
        assert provenance["status"] == "draft"
        assert provenance["source_clusters"] == [cluster["id"]]
        assert provenance["evaluation"] == {"semantic": "not-run"}
        assert provenance["release_evidence"] == []
        skill = (slot / "SKILL.md").read_text(encoding="utf-8")
        assert cluster["candidate_responsibility"] in skill
        assert cluster["input_boundary"] in skill
        assert cluster["output_boundary"] in skill
        all_text += json.dumps(contract) + json.dumps(provenance) + skill
        for mapping in provenance["units"]:
            unit = units[mapping["unit_id"]]
            assert mapping["source_path"] == unit["source_path"]
            assert mapping["line_start"] == unit["origin_line_start"]
            assert mapping["line_end"] == unit["origin_line_end"]
            assert mapping["disposition"] == unit["status"]
            assert isinstance(mapping["decision_ids"], list)
    assert '"status": "released"' not in all_text


def test_contract_dependencies_only_name_upstream_prerequisites(tmp_path: Path) -> None:
    slots, queue_path = tmp_path / "slots", tmp_path / "queue.json"
    result = run_generator(slots, queue_path)
    assert result.returncode == 0, result.stderr

    clusters = json.loads(CLUSTERS.read_text(encoding="utf-8"))["clusters"]
    for cluster in clusters:
        slot_id = cluster["id"].removeprefix("cluster:")
        contract = json.loads((slots / slot_id / "contract.json").read_text(encoding="utf-8"))
        assert contract["dependencies"] == sorted(cluster["upstream_dependencies"])


def test_topology_batches_condense_cycles_without_flattening_dependents() -> None:
    clusters = [
        {
            "id": "cluster:a",
            "upstream_dependencies": ["cluster:b"],
            "downstream_dependencies": [],
        },
        {
            "id": "cluster:b",
            "upstream_dependencies": ["cluster:a"],
            "downstream_dependencies": ["cluster:c"],
        },
        {
            "id": "cluster:c",
            "upstream_dependencies": ["cluster:b"],
            "downstream_dependencies": [],
        },
        {
            "id": "cluster:independent",
            "upstream_dependencies": [],
            "downstream_dependencies": [],
        },
    ]

    batch_by_id = generate_slots.batches(clusters)

    assert batch_by_id["cluster:a"] == batch_by_id["cluster:b"]
    assert batch_by_id["cluster:c"] > batch_by_id["cluster:b"]
    assert batch_by_id["cluster:independent"] < batch_by_id["cluster:c"]
