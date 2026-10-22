from pathlib import Path

from tools.curation.v2_auxiliary_units import normalize, verify_disposed

ROOT = Path(__file__).resolve().parents[2]


def test_all_114_auxiliary_units_are_normalized_without_premature_decisions() -> None:
    result = normalize(ROOT)

    assert result["ok"] is True, result["errors"]
    assert result["count"] == 114
    assert all(unit["source_path"] and unit["v2_disposition"] == "pending-semantic-review" for unit in result["units"])
    assert len({unit["id"] for unit in result["units"]}) == 114


def test_disposition_gate_requires_decision_and_destination() -> None:
    data = {"units": [
        {"id": "a", "v2_disposition": "pending-semantic-review", "decision_id": None},
        {"id": "b", "v2_disposition": "merge", "decision_id": "D-1", "target_unit_id": None},
        {"id": "c", "v2_disposition": "retain", "decision_id": "D-2", "target_cluster_id": None},
    ]}

    errors = verify_disposed(data)

    assert any("lacks disposition" in error for error in errors)
    assert any("merge lacks target" in error for error in errors)
    assert any("lacks cluster" in error for error in errors)
