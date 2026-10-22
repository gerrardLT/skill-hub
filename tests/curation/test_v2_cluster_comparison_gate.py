import json
from pathlib import Path

from tools.curation.v2_cluster_comparison_gate import verify

ROOT = Path(__file__).resolve().parents[2]


def test_comparison_gate_requires_every_cluster(tmp_path: Path) -> None:
    relationships = tmp_path / "relationships.json"
    relationships.write_text('{"cluster_audits": []}', encoding="utf-8")

    result = verify(ROOT, tmp_path, relationships)

    assert result["ok"] is False
    assert result["cluster_count"] == 88
    assert result["comparison_count"] == 0
    assert any("missing comparison" in error for error in result["errors"])
    assert any("relationship audit coverage mismatch" in error for error in result["errors"])


def test_checked_in_comparisons_cover_units_sources_dimensions_rules_and_decisions() -> None:
    result = verify(ROOT, ROOT / "curation/v2/comparisons", ROOT / "curation/v2/relationships.json")

    assert result["ok"] is True, result["errors"]
    assert result["comparison_count"] == 88
    assert result["relationship_audit_count"] == 88
    assert result["canonical_unit_count"] == 965
    assert result["retained_auxiliary_count"] == 104
