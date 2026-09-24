import json
import shutil
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools" / "curation"))
from tools.curation import verify


PILOT_SLOTS = (
    "problem-framing",
    "requirements-rules",
    "acceptance-criteria",
    "requirements-quality-gate",
)


def run_verify(root: Path) -> dict[str, object]:
    return verify.verify_phase5(
        root / "curation" / "clusters.json",
        root / "curation" / "units",
        root / "curation" / "decisions.jsonl",
        root / "curation" / "coverage.json",
        root / "slots",
    )


def copy_fixture(tmp_path: Path) -> Path:
    root = tmp_path / "workspace"
    curation = root / "curation"
    slots = root / "slots"
    curation.mkdir(parents=True)
    slots.mkdir()
    shutil.copy(ROOT / "curation" / "clusters.json", curation / "clusters.json")
    shutil.copy(ROOT / "curation" / "decisions.jsonl", curation / "decisions.jsonl")
    shutil.copy(ROOT / "curation" / "coverage.json", curation / "coverage.json")
    shutil.copytree(ROOT / "curation" / "units", curation / "units")
    for slot_id in PILOT_SLOTS:
        shutil.copytree(ROOT / "slots" / slot_id, slots / slot_id)
    return root


def test_phase5_pilot_provenance_is_complete_and_symmetric() -> None:
    result = run_verify(ROOT)

    assert result == {
        "gate": "phase-5-pilot-provenance",
        "ok": True,
        "pilot_slot_count": 4,
        "mapped_unit_count": 54,
        "errors": [],
        "input_errors": [],
        "jsonl_errors": [],
    }


def test_phase5_rejects_unknown_provenance_cluster(tmp_path: Path) -> None:
    root = copy_fixture(tmp_path)
    path = root / "slots" / "problem-framing" / "provenance.json"
    provenance = json.loads(path.read_text(encoding="utf-8"))
    provenance["source_clusters"][0] = "cluster:missing"
    path.write_text(json.dumps(provenance), encoding="utf-8")

    result = run_verify(root)

    assert result["ok"] is False
    assert any("source cluster mismatch" in error for error in result["errors"])


def test_phase5_rejects_dangling_decision_reference(tmp_path: Path) -> None:
    root = copy_fixture(tmp_path)
    path = root / "slots" / "acceptance-criteria" / "provenance.json"
    provenance = json.loads(path.read_text(encoding="utf-8"))
    provenance["unit_mappings"][0]["decision_ids"] = ["decision:missing"]
    path.write_text(json.dumps(provenance), encoding="utf-8")

    result = run_verify(root)

    assert result["ok"] is False
    assert any("unknown decision" in error for error in result["errors"])


def test_phase5_rejects_asymmetric_source_slot_coverage(tmp_path: Path) -> None:
    root = copy_fixture(tmp_path)
    path = root / "curation" / "coverage.json"
    coverage = json.loads(path.read_text(encoding="utf-8"))
    del coverage["slot_mappings"]["source_to_slots"]["prd-development"]["problem-framing"]
    path.write_text(json.dumps(coverage), encoding="utf-8")

    result = run_verify(root)

    assert result["ok"] is False
    assert any("coverage indexes are not symmetric" in error for error in result["errors"])


def test_phase5_rejects_coordinate_drift(tmp_path: Path) -> None:
    root = copy_fixture(tmp_path)
    path = root / "slots" / "requirements-rules" / "provenance.json"
    provenance = json.loads(path.read_text(encoding="utf-8"))
    provenance["unit_mappings"][0]["line_start"] += 1
    path.write_text(json.dumps(provenance), encoding="utf-8")

    result = run_verify(root)

    assert result["ok"] is False
    assert any("coordinate mismatch" in error for error in result["errors"])
