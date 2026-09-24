import json
import shutil
from pathlib import Path

from tools.curation.phase5_gate import verify_phase5_release

ROOT = Path(__file__).resolve().parents[2]


def test_phase5_release_gate_passes_current_evidence() -> None:
    report = verify_phase5_release(ROOT)
    assert report["ok"] is True, report
    assert report["candidate_freeze_files"] == 12
    assert report["pilot_slot_count"] == 4


def test_phase5_release_gate_rejects_unapproved_feedback(tmp_path: Path) -> None:
    workspace = tmp_path / "workspace"
    shutil.copytree(ROOT / "evals", workspace / "evals")
    shutil.copytree(ROOT / "slots", workspace / "slots")
    feedback_path = workspace / "evals/runs/requirements-to-ac/iteration-2/feedback.json"
    feedback = json.loads(feedback_path.read_text(encoding="utf-8"))
    feedback["verdict"] = "changes-requested"
    feedback_path.write_text(json.dumps(feedback), encoding="utf-8")

    report = verify_phase5_release(workspace)

    assert report["ok"] is False
    assert "human feedback is not approved" in report["errors"]
