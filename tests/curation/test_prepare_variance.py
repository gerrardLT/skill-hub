import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from tools.curation.prepare_variance import prepare


def test_prepare_maps_candidate_and_baseline_runs(tmp_path: Path) -> None:
    paired = tmp_path / "paired"
    for config in ("candidate", "baseline"):
        run = paired / config / "case-1"
        run.mkdir(parents=True)
        for name in ("full_output.md", "tool_evidence.raw.json", "timing.json"):
            (run / name).write_text(config, encoding="utf-8")
    cases = tmp_path / "cases.json"
    cases.write_text(json.dumps({"cases": [{"id": "case-1"}]}), encoding="utf-8")

    result = prepare([paired], cases, tmp_path / "variance", ["case-1"])

    assert result["passed"] is True
    assert (tmp_path / "variance/case-1/with_skill/run-1/full_output.md").read_text() == "candidate"
    assert (tmp_path / "variance/case-1/without_skill/run-1/full_output.md").read_text() == "baseline"
