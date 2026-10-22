import json
from pathlib import Path

from tools.curation.v2_phase1_review_gate import verify

ROOT = Path(__file__).resolve().parents[2]


def test_review_batches_cover_all_139_roots_exactly_once() -> None:
    result = verify(ROOT)

    assert result["ok"] is True, result["errors"]
    assert result["root_count"] == 139
    assert result["assignment_count"] == 139


def test_review_gate_rejects_missing_report_roots_and_citations(tmp_path: Path) -> None:
    batches = json.loads((ROOT / "curation/v2/root-batches.json").read_text(encoding="utf-8"))["batches"]
    for name in batches:
        (tmp_path / f"{name}.md").write_text("Trigger Responsibility Inputs Outputs Workflow Permissions Unique Weakness Support\n", encoding="utf-8")

    result = verify(ROOT, tmp_path)

    assert result["ok"] is False
    assert any("lacks roots" in error for error in result["errors"])
    assert any("lacks per-root line citations" in error for error in result["errors"])
