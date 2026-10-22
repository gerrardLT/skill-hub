import copy
import hashlib
import json
import shutil
from pathlib import Path

import pytest

import tools.curation.v2_phase9_gate as gate
import tools.curation.v2_phase9_grade as grader

ROOT = Path(__file__).resolve().parents[2]
RUN_ROOT = ROOT / "evals/runs/capability-compiler-v2/phase-9"


def load(path: Path): return json.loads(path.read_text(encoding="utf-8"))
def write(path: Path, value) -> None: path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")


def copied_attempt(tmp_path: Path, run_id: str = "run-0001") -> tuple[dict, Path]:
    plan = load(ROOT / "curation/v2/phase-9/run-plan.json"); task = next(item for item in plan["tasks"] if item["id"] == run_id); directory = tmp_path / run_id; shutil.copytree(RUN_ROOT / "attempts" / run_id, directory); return task, directory


def test_phase9_artifact_manifest_recomputes_exactly() -> None:
    path = ROOT / ".specs/capability-compiler-v2/phase-9/artifact-manifest.json"; manifest = load(path); records = []
    excluded = {path.relative_to(ROOT).as_posix(), ".specs/capability-compiler-v2/phase-9/phase-report.json"}
    for item in manifest["artifacts"]:
        assert item["path"] not in excluded
        artifact = ROOT / item["path"]; data = artifact.read_bytes().replace(b"\r\n", b"\n")
        assert artifact.stat().st_size == item["bytes"]
        assert hashlib.sha256(data).hexdigest() == item["sha256"]
        records.append(f"{item['path']}\0{item['sha256']}\n")
    assert len(records) == manifest["artifact_count"] == 13254
    assert hashlib.sha256("".join(records).encode()).hexdigest() == manifest["tree_sha256"] == "7540c53426a5dff605c3f751fdaf105f52059ffbafce213d77c9c3db94214152"


def test_phase9_gate_accepts_complete_evidence_and_blocks_release() -> None:
    result = gate.verify(ROOT)
    assert result["ok"] is True, result["errors"]
    assert result["evaluation_complete"] is True
    assert result["release_thresholds_passed"] is False
    assert result["release_blocked"] is True
    assert result["counts"] == {"planned_runs": 1002, "verified_attempts": 1002, "candidate_skill_holdouts_passed": 314, "candidate_skill_holdouts_total": 314, "open_findings": 6, "preserved_calibration_attempts": 20}


def test_phase9_plan_recomputes_exactly() -> None:
    plan = load(ROOT / "curation/v2/phase-9/run-plan.json")
    assert plan["task_count"] == len(plan["tasks"]) == 1002
    assert plan["counts"] == gate.EXPECTED_COUNTS
    assert hashlib.sha256(json.dumps(plan["tasks"], ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()).hexdigest() == plan["task_sha256"] == "97b7f493a54cb6d6419479ecd6f7ffee3dfd9260818659697d35a109724f995b"


def test_phase9_attempt_verifier_accepts_current_attempt(tmp_path: Path) -> None:
    task, directory = copied_attempt(tmp_path)
    verified, errors = grader.verify_attempt(task, directory)
    assert errors == []
    assert verified["run"]["candidate_action_executed"] is False


def test_phase9_attempt_verifier_rejects_output_tamper(tmp_path: Path) -> None:
    task, directory = copied_attempt(tmp_path); (directory / "full_output.md").write_text("{}\n", encoding="utf-8")
    _, errors = grader.verify_attempt(task, directory)
    assert "full_output.md-hash-mismatch" in errors


def test_phase9_attempt_verifier_rejects_prompt_tamper(tmp_path: Path) -> None:
    task, directory = copied_attempt(tmp_path); (directory / "prompt.md").write_text("leaked expected answer\n", encoding="utf-8")
    _, errors = grader.verify_attempt(task, directory)
    assert "prompt.md-hash-mismatch" in errors


def test_phase9_attempt_verifier_rejects_missing_no_tools_flag(tmp_path: Path) -> None:
    task, directory = copied_attempt(tmp_path); command = load(directory / "command.json"); command["argv"].remove("--no-tools"); write(directory / "command.json", command)
    _, errors = grader.verify_attempt(task, directory)
    assert "command-no-tool-flags-missing" in errors


def test_phase9_attempt_verifier_rejects_action_claim(tmp_path: Path) -> None:
    task, directory = copied_attempt(tmp_path); run = load(directory / "run.json"); run["candidate_action_executed"] = True; write(directory / "run.json", run)
    _, errors = grader.verify_attempt(task, directory)
    assert "tool-or-action-boundary-mismatch" in errors


def test_phase9_grade_value_rejects_wrong_router_target() -> None:
    task = {"schema": "router", "expected": {"target": "blocked-data-governance"}}
    passed, failures = grader.grade_value(task, {"target": "stage-01-governance-intake", "reason": "x", "would_execute": False})
    assert passed is False
    assert failures == ["target-mismatch"]


def test_phase9_grade_value_rejects_missing_recipe_route_steps() -> None:
    task = {"schema": "route", "expected": {"required_steps": ["review-evidence", "rendered-critique"]}}
    passed, failures = grader.grade_value(task, {"selected_steps": ["rendered-critique"], "decision": "satisfied", "reason": "x", "would_execute": False})
    assert passed is False
    assert failures == ["missing-required-steps:review-evidence"]


def test_phase9_report_preserves_failed_thresholds() -> None:
    report = load(RUN_ROOT / "grading-report.json")
    assert report["thresholds"] == gate.EXPECTED_THRESHOLDS
    assert report["thresholds_passed"] is False
    assert len(report["failed_runs"]) == 174
    assert report["groups"]["paired_skill_holdouts"] == {"candidate-win": 155, "tie": 159}


def test_phase9_calibration_failures_are_preserved() -> None:
    first = ROOT / "evals/runs/capability-compiler-v2/phase-9-pilots/routing-readiness-calibration-v1/run-root/attempts"
    second = ROOT / "evals/runs/capability-compiler-v2/phase-9-pilots/recipe-route-completeness-calibration-v2/attempts"
    assert len(list(first.glob("run-*/run.json"))) == 8
    assert len(list(second.glob("run-*/run.json"))) == 12
    for path in [first.parents[1] / "finding.json", second.parent / "finding.json"]:
        value = load(path); assert value["deleted_failures"] == 0; assert value["production_evidence_eligible"] is False
