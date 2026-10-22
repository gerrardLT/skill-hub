import json
import shutil
from pathlib import Path

from tools.curation.full_dev_loop_release_gate import _review_approved, verify

ROOT = Path(__file__).resolve().parents[2]


def test_review_requires_exactly_all_six_stage_approvals() -> None:
    review = {
        "verdict": "approved-for-release",
        "stage_verdicts": {
            "requirements": "approved",
            "design": "approved",
            "implementation": "approved",
            "qa": "approved",
            "delivery": "approved",
            "retrospective": "approved",
        },
    }
    assert _review_approved(review)
    review["stage_verdicts"].pop("qa")
    assert not _review_approved(review)


def test_release_gate_recomputes_case_output_hashes(tmp_path: Path) -> None:
    shutil.copytree(ROOT / "evals/runs/full-dev-loop/ip-rate-limiting-v1", tmp_path / "evals/runs/full-dev-loop/ip-rate-limiting-v1")
    shutil.copytree(ROOT / "evals/candidates/full-dev-loop/recipes", tmp_path / "evals/candidates/full-dev-loop/recipes")
    suite = tmp_path / "evals/runs/full-dev-loop/ip-rate-limiting-v1/slot-evaluations/tdd-change-loop/candidate.json"
    data = json.loads(suite.read_text(encoding="utf-8"))
    data["cases"][0]["output_sha256"] = "0" * 64
    suite.write_text(json.dumps(data), encoding="utf-8")

    result = verify(tmp_path, check_gate_report=False)

    assert result["ok"] is False
    assert any("output hash mismatch" in error for error in result["errors"])
