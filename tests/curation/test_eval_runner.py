import hashlib
import json
import subprocess
import sys
from pathlib import Path

import pytest

from tools.curation import eval_runner


CASE = {
    "id": "case-1",
    "prompt": "Produce a bounded requirements contract.",
    "required_behaviors": [
        {
            "criterion": "preserve supplied constraint",
            "assertion": "contains",
            "value": "preserve supplied constraint",
        }
    ],
    "must_preserve_unknowns": [
        {"criterion": "decision owner", "assertion": "contains", "value": "decision owner"}
    ],
    "must_not_claim": [
        {
            "criterion": "implementation complete",
            "assertion": "absent",
            "value": "implementation complete",
        }
    ],
    "expected_status": "needs-input",
}
REQUIRED_RUN_FIELDS = [
    "case_id",
    "source_skill",
    "full_output",
    "tool_evidence",
    "model",
    "input_hash",
    "tool_permissions",
    "budget",
    "duration_ms",
    "token_usage",
    "exit_status",
    "failure_reason",
]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value), encoding="utf-8")


def make_fixture(tmp_path: Path, output: str | None = None) -> tuple[Path, Path, Path, Path]:
    cases = tmp_path / "cases.json"
    rubric = tmp_path / "rubric.json"
    runs = tmp_path / "runs"
    run_dir = runs / CASE["id"]
    run_dir.mkdir(parents=True)
    output_path = run_dir / "full_output.md"
    output_path.write_text(
        output
        or "Status: needs-input\n\npreserve supplied constraint\n\nOpen question: decision owner\n",
        encoding="utf-8",
    )
    evidence_path = run_dir / "tool_evidence.json"
    write_json(
        evidence_path,
        {
            "case_id": CASE["id"],
            "offline": True,
            "network_accessed": False,
            "artifacts": {
                "full_output": {"path": "full_output.md", "sha256": sha256(output_path)}
            },
        },
    )
    write_json(
        run_dir / "run.json",
        {
            "case_id": CASE["id"],
            "source_skill": "example-skill",
            "full_output": "full_output.md",
            "full_output_sha256": sha256(output_path),
            "tool_evidence": "tool_evidence.json",
            "tool_evidence_sha256": sha256(evidence_path),
            "model": "local-test-model",
            "input_hash": hashlib.sha256(CASE["prompt"].encode()).hexdigest(),
            "tool_permissions": ["read-local-files", "write-run-output"],
            "budget": {"network": False},
            "offline": True,
            "duration_ms": 1,
            "token_usage": {"input": 1, "output": 1},
            "exit_status": "success",
            "failure_reason": None,
        },
    )
    write_json(cases, {"version": 1, "cases": [CASE]})
    write_json(
        rubric,
        {
            "version": 1,
            "hard_failures": [{"id": "unknown-loss"}],
            "minimums": {"hard_failures": 0},
        },
    )
    return cases, rubric, runs, run_dir


def test_complete_run_passes_structural_verification(tmp_path: Path) -> None:
    cases, _, runs, _ = make_fixture(tmp_path)

    report = eval_runner.verify_runs(cases, runs)

    assert report["passed"] is True
    assert report["cases"][0]["valid"] is True
    assert report["cases"][0]["errors"] == []


def test_candidate_freeze_matches_recorded_artifact(tmp_path: Path) -> None:
    artifact = tmp_path / "slots" / "example" / "SKILL.md"
    artifact.parent.mkdir(parents=True)
    artifact.write_text("frozen candidate\n", encoding="utf-8")
    freeze = tmp_path / "candidate-freeze.json"
    write_json(
        freeze,
        {
            "files": [
                {
                    "path": "slots/example/SKILL.md",
                    "sha256": sha256(artifact),
                    "bytes": artifact.stat().st_size,
                }
            ]
        },
    )

    report = eval_runner.verify_candidate_freeze(freeze, tmp_path)

    assert report == {
        "passed": True,
        "file_count": 1,
        "errors": [],
    }


def test_candidate_freeze_detects_artifact_drift(tmp_path: Path) -> None:
    artifact = tmp_path / "slots" / "example" / "SKILL.md"
    artifact.parent.mkdir(parents=True)
    artifact.write_text("frozen candidate\n", encoding="utf-8")
    freeze = tmp_path / "candidate-freeze.json"
    write_json(
        freeze,
        {
            "files": [
                {
                    "path": "slots/example/SKILL.md",
                    "sha256": sha256(artifact),
                    "bytes": artifact.stat().st_size,
                }
            ]
        },
    )
    artifact.write_text("changed candidate\n", encoding="utf-8")

    report = eval_runner.verify_candidate_freeze(freeze, tmp_path)

    assert report["passed"] is False
    assert "slots/example/SKILL.md: SHA-256 mismatch" in report["errors"]
    assert "slots/example/SKILL.md: byte count mismatch" in report["errors"]


def test_tampered_output_hash_fails(tmp_path: Path) -> None:
    cases, _, runs, run_dir = make_fixture(tmp_path)
    (run_dir / "full_output.md").write_text("tampered", encoding="utf-8")

    report = eval_runner.verify_runs(cases, runs)

    assert report["passed"] is False
    assert any("hash" in error for error in report["cases"][0]["errors"])


def test_missing_unknown_and_forbidden_claim_fail(tmp_path: Path) -> None:
    cases, rubric, runs, _ = make_fixture(
        tmp_path,
        "Status: needs-input\n\npreserve supplied constraint\nimplementation complete\n",
    )

    result = eval_runner.grade(cases, rubric, runs)
    case_result = result["cases"][0]

    assert result["passed"] is False
    assert case_result["objective_checks"]["must_preserve_unknowns"][0]["passed"] is False
    assert case_result["objective_checks"]["must_not_claim"][0]["passed"] is False
    assert "unknown-loss" in case_result["hard_failures"]
    assert "forbidden-claim" in case_result["hard_failures"]


def test_handwritten_pass_is_not_accepted_as_evidence(tmp_path: Path) -> None:
    cases, rubric, runs, _ = make_fixture(tmp_path, "PASS\nStatus: needs-input\n")

    case_result = eval_runner.grade(cases, rubric, runs)["cases"][0]

    assert case_result["passed"] is False
    assert case_result["objective_checks"]["required_behaviors"][0]["passed"] is False
    assert not any(item.get("text") == "PASS" for item in case_result["evidence"])


def test_missing_run_file_fails(tmp_path: Path) -> None:
    cases, _, runs, run_dir = make_fixture(tmp_path)
    (run_dir / "run.json").unlink()

    report = eval_runner.verify_runs(cases, runs)

    assert report["passed"] is False
    assert "missing run.json" in report["cases"][0]["errors"]


def test_grade_cli_writes_json_report(tmp_path: Path) -> None:
    cases, rubric, runs, _ = make_fixture(tmp_path)
    output = tmp_path / "grade.json"

    completed = subprocess.run(
        [
            sys.executable,
            "tools/curation/eval_runner.py",
            "grade",
            "--cases",
            str(cases),
            "--rubric",
            str(rubric),
            "--runs-root",
            str(runs),
            "--output",
            str(output),
        ],
        cwd=Path(__file__).parents[2],
        check=False,
        capture_output=True,
        text=True,
    )

    assert completed.returncode == 0, completed.stderr
    assert json.loads(output.read_text(encoding="utf-8"))["passed"] is True


def test_baseline_required_fields_are_enforced(tmp_path: Path) -> None:
    cases, _, runs, run_dir = make_fixture(tmp_path)
    manifest = tmp_path / "evals.json"
    write_json(
        manifest,
        {
            "baseline": {"required": True, "must_record": REQUIRED_RUN_FIELDS},
        },
    )
    run = json.loads((run_dir / "run.json").read_text(encoding="utf-8"))
    del run["model"]
    write_json(run_dir / "run.json", run)

    report = eval_runner.verify_runs(cases, runs, manifest)

    assert report["passed"] is False
    assert any("model" in error for error in report["cases"][0]["errors"])


def test_placeholder_timing_and_token_usage_fail_verification(tmp_path: Path) -> None:
    cases, _, runs, run_dir = make_fixture(tmp_path)
    run_path = run_dir / "run.json"
    run = json.loads(run_path.read_text(encoding="utf-8"))
    run["duration_ms"] = None
    run["token_usage"] = None
    write_json(run_path, run)

    report = eval_runner.verify_runs(cases, runs)

    assert report["passed"] is False
    assert "duration_ms must be a non-negative number" in report["cases"][0]["errors"]
    assert "token_usage must contain non-negative numeric usage" in report["cases"][0]["errors"]


def test_failed_execution_is_auditable_but_cannot_pass_grading(tmp_path: Path) -> None:
    cases, rubric, runs, run_dir = make_fixture(tmp_path)
    run_path = run_dir / "run.json"
    run = json.loads(run_path.read_text(encoding="utf-8"))
    run["exit_status"] = "failed"
    run["failure_reason"] = "agent harness failure"
    write_json(run_path, run)

    verification = eval_runner.verify_runs(cases, runs)
    grading = eval_runner.grade(cases, rubric, runs)

    assert verification["passed"] is True
    assert "run-execution-failed" in grading["cases"][0]["hard_failures"]
    assert grading["cases"][0]["passed"] is False


def test_failed_execution_requires_failure_reason(tmp_path: Path) -> None:
    cases, _, runs, run_dir = make_fixture(tmp_path)
    run_path = run_dir / "run.json"
    run = json.loads(run_path.read_text(encoding="utf-8"))
    run["exit_status"] = "failed"
    run["failure_reason"] = None
    write_json(run_path, run)

    report = eval_runner.verify_runs(cases, runs)

    assert report["passed"] is False
    assert "failed run requires failure_reason" in report["cases"][0]["errors"]


@pytest.mark.parametrize(
    ("line", "expected"),
    [
        ("# Status: Needs Input", "needs-input"),
        ("## Status\n\n**Blocked** - unresolved authority", "blocked"),
        ("**Status:** passed", "passed"),
        ("**Status:** Ready for a bounded handoff", "passed"),
        ("Overall status: `needs-input`", "needs-input"),
        ("## Overall status\n\n`blocked`", "blocked"),
    ],
)
def test_markdown_status_variants_are_parsed(line: str, expected: str) -> None:
    assert eval_runner._extract_status(line) == expected


def test_negated_forbidden_phrase_is_not_an_affirmative_claim(tmp_path: Path) -> None:
    cases, rubric, runs, _ = make_fixture(
        tmp_path,
        "Status: needs-input\n\npreserve supplied constraint\nOpen question: decision owner\n"
        "No implementation complete claim is made.\n",
    )

    result = eval_runner.grade(cases, rubric, runs)["cases"][0]

    assert result["objective_checks"]["must_not_claim"][0]["passed"] is True
    assert "forbidden-claim" not in result["hard_failures"]


def test_natural_language_behavior_requires_human_review(tmp_path: Path) -> None:
    cases, rubric, runs, _ = make_fixture(tmp_path)
    document = json.loads(cases.read_text(encoding="utf-8"))
    document["cases"][0]["required_behaviors"] = ["semantically preserve the supplied constraint"]
    write_json(cases, document)

    result = eval_runner.grade(cases, rubric, runs)["cases"][0]
    check = result["objective_checks"]["required_behaviors"][0]

    assert check["review_status"] == "pending-human-review"
    assert "pending-human-review" in result["hard_failures"]
    assert "missing-required-behavior" not in result["hard_failures"]
