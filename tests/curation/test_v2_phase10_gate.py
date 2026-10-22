import hashlib
import json
import shutil
from pathlib import Path

import pytest

import tools.curation.v2_phase10_gate as gate
import tools.curation.v2_phase9_grade as grader

ROOT = Path(__file__).resolve().parents[2]


def load(path: Path): return json.loads(path.read_text(encoding="utf-8"))
def write(path: Path, value) -> None: path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")


def test_phase10_artifact_manifest_recomputes_exactly() -> None:
    path = ROOT / ".specs/capability-compiler-v2/phase-10/artifact-manifest.json"; manifest = load(path); records = []; excluded = {path.relative_to(ROOT).as_posix(), ".specs/capability-compiler-v2/phase-10/phase-report.json"}
    for item in manifest["artifacts"]:
        assert item["path"] not in excluded
        artifact = ROOT / item["path"]; data = artifact.read_bytes().replace(b"\r\n", b"\n")
        assert artifact.stat().st_size == item["bytes"]
        assert hashlib.sha256(data).hexdigest() == item["sha256"]
        records.append(f"{item['path']}\0{item['sha256']}\n")
    assert len(records) == manifest["artifact_count"] == 2707
    assert hashlib.sha256("".join(records).encode()).hexdigest() == manifest["tree_sha256"] == "7fd6640a563789257da77e1015be3f37033a3baf40ecaf9a4b9fa1fde7828d56"


def test_phase10_gate_accepts_complete_review_without_release_claim() -> None:
    result = gate.verify(ROOT)
    assert result["ok"] is True, result["errors"]
    assert result["eligible_for_phase_11"] is True
    assert result["final_user_release_approval"] is False
    assert result["released"] is False
    assert result["counts"] == {"reviewed_skills": 157, "reviewed_outputs": 314, "adjudicated_findings": 6, "rejected_revisions_preserved": 3, "revision4_runs": 60, "causal_mutations_killed": 10}


def test_phase10_plan_recomputes_exactly() -> None:
    plan = load(ROOT / "curation/v2/phase-10/run-plan.json")
    assert plan["revision"] == 4 and plan["task_count"] == len(plan["tasks"]) == 60
    assert hashlib.sha256(json.dumps(plan["tasks"], ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()).hexdigest() == plan["task_sha256"] == "b96a2b6172b9ee2760e3b9a40582a48e2516c70a5c9c42a0e4099ff6282ecd53"


def test_phase10_review_ledger_is_exactly_157_by_2() -> None:
    ledger = load(ROOT / "curation/v2/phase-10/skill-review-ledger.json")
    assert ledger["skill_count"] == 157
    assert ledger["reviewed_output_count"] == 314
    assert len({item["skill_id"] for item in ledger["records"]}) == 157
    assert all(item["verdict"] == "accepted" and item["revision_required"] is False and len(item["cases"]) == 2 for item in ledger["records"])


def test_phase10_rejected_revisions_preserve_all_attempts() -> None:
    for revision, expected in [(1, 56), (2, 58), (3, 60)]:
        root = ROOT / f"evals/runs/capability-compiler-v2/phase-10/revision-{revision}/attempts"
        assert len(list(root.glob("run-*/run.json"))) == expected
        checkpoint = load(ROOT / f".specs/capability-compiler-v2/phase-10/revision-{revision}-rejection.json")
        assert checkpoint["deleted_failures"] == 0
        assert checkpoint["thresholds_lowered"] is False


def test_phase10_attempt_verifier_rejects_output_tamper(tmp_path: Path) -> None:
    plan = load(ROOT / "curation/v2/phase-10/run-plan.json"); task = plan["tasks"][0]; source = ROOT / "evals/runs/capability-compiler-v2/phase-10/attempts" / task["id"]; target = tmp_path / task["id"]; shutil.copytree(source, target); (target / "full_output.md").write_text("{}\n", encoding="utf-8")
    _, errors = grader.verify_attempt(task, target)
    assert "full_output.md-hash-mismatch" in errors


def test_phase10_semantic_review_cannot_claim_final_approval() -> None:
    review = load(ROOT / "curation/v2/phase-10/semantic-review.json")
    assert review["final_user_release_approval"] is False
    assert review["release_disposition"] == "eligible-for-phase-11-real-project-validation-not-released"
    assert review["open_findings"] == []


def test_phase10_revision4_scope_is_one_authorized_recipe_change() -> None:
    patch = load(ROOT / "evals/candidates/capability-compiler-v2/phase-10/revision-4/patch-ledger.json")
    assert patch["atomic_skill_revisions"] == 0
    assert patch["released"] == 0
    assert patch["revision4_change_count"] == 1
    assert len(patch["revision4_records"]) == 1
    assert patch["revision4_records"][0]["path"].endswith("phase-4/complete-ui-design-and-review.json")


def test_phase10_all_targeted_thresholds_remain_100_percent() -> None:
    report = load(ROOT / "evals/runs/capability-compiler-v2/phase-10/grading-report.json")
    assert report["thresholds_passed"] is True
    assert all(report["thresholds"].values())
    assert report["failed_runs"] == []
    assert report["groups"]["overall"]["accuracy"] == 1.0
    assert len(report["mutation_results"]) == 10
    assert all(item["status"] == "killed" for item in report["mutation_results"])
