from pathlib import Path

from tools.curation.v2_auxiliary_match import propose

ROOT = Path(__file__).resolve().parents[2]


def test_auxiliary_matcher_proposes_without_deciding() -> None:
    result = propose(ROOT, ROOT / "curation/v2/units/auxiliary.json")

    assert result["ok"] is True, result["errors"]
    assert result["count"] == 114
    assert result["exact_match_suggestions"] == 1
    assert result["manual_review"] == 113
    assert all("recommendation" in item and "candidates" in item for item in result["matches"])
    assert all("v2_disposition" not in item for item in result["matches"])
