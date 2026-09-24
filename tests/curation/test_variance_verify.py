import json
from pathlib import Path

from tools.curation import variance_verify


def write_run(root: Path, case_id: str, config: str, run_number: int, status: str) -> None:
    run = root / case_id / config / f"run-{run_number}"
    run.mkdir(parents=True)
    (run / "full_output.md").write_text(f"Status: {status}\n", encoding="utf-8")
    (run / "tool_evidence.raw.json").write_text(
        json.dumps(
            {
                "offline": True,
                "network_accessed": False,
                "skills_modified": False,
                "case_file_read": False,
                "rubric_read": False,
                "slots_read": config == "with_skill",
                "paths_read": ["slots/example/SKILL.md"] if config == "with_skill" else [],
                "errors": [],
            }
        ),
        encoding="utf-8",
    )
    (run / "timing.json").write_text(
        json.dumps(
            {
                "total_tokens": 100 + run_number,
                "duration_ms": 1000 + run_number,
                "total_duration_seconds": (1000 + run_number) / 1000,
            }
        ),
        encoding="utf-8",
    )


def test_paired_variance_report_computes_status_and_metric_stats(tmp_path: Path) -> None:
    cases = tmp_path / "cases.json"
    cases.write_text(
        json.dumps(
            {
                "cases": [
                    {"id": "case-1", "expected_status": "needs-input"},
                ]
            }
        ),
        encoding="utf-8",
    )
    for run_number in (1, 2):
        write_run(tmp_path / "runs", "case-1", "with_skill", run_number, "needs-input")
        write_run(tmp_path / "runs", "case-1", "without_skill", run_number, "passed")

    report = variance_verify.verify_variance(cases, tmp_path / "runs", ["case-1"], 2)

    assert report["passed"] is True
    case = report["cases"][0]
    assert case["paired_run_count"] == 2
    assert case["with_skill"]["status_match"]["mean"] == 1.0
    assert case["without_skill"]["status_match"]["mean"] == 0.0
    assert case["with_skill"]["tokens"]["stddev"] > 0


def test_incomplete_pair_is_excluded_but_preserved(tmp_path: Path) -> None:
    cases = tmp_path / "cases.json"
    cases.write_text(
        json.dumps({"cases": [{"id": "case-1", "expected_status": "passed"}]}),
        encoding="utf-8",
    )
    for run_number in (1, 2, 3):
        write_run(tmp_path / "runs", "case-1", "with_skill", run_number, "passed")
        write_run(tmp_path / "runs", "case-1", "without_skill", run_number, "passed")
    (tmp_path / "runs/case-1/without_skill/run-2/tool_evidence.raw.json").unlink()

    report = variance_verify.verify_variance(cases, tmp_path / "runs", ["case-1"], 2)

    assert report["passed"] is True
    assert report["cases"][0]["paired_run_count"] == 2
    assert report["cases"][0]["excluded_pairs"] == [
        {
            "run_number": 2,
            "reason": "without_skill: missing tool_evidence.raw.json",
        }
    ]


def test_fails_when_too_few_valid_pairs_remain(tmp_path: Path) -> None:
    cases = tmp_path / "cases.json"
    cases.write_text(
        json.dumps({"cases": [{"id": "case-1", "expected_status": "passed"}]}),
        encoding="utf-8",
    )
    write_run(tmp_path / "runs", "case-1", "with_skill", 1, "passed")
    write_run(tmp_path / "runs", "case-1", "without_skill", 1, "passed")

    report = variance_verify.verify_variance(cases, tmp_path / "runs", ["case-1"], 2)

    assert report["passed"] is False
    assert "case-1: only 1 valid paired runs; require 2" in report["errors"]


def test_expected_read_configuration_is_enforced(tmp_path: Path) -> None:
    cases = tmp_path / "cases.json"
    cases.write_text(
        json.dumps({"cases": [{"id": "case-1", "expected_status": "passed"}]}),
        encoding="utf-8",
    )
    for config in ("with_skill", "without_skill"):
        write_run(tmp_path / "runs", "case-1", config, 1, "passed")
    configuration = {
        "case-1": {
            "with_skill": ["slots/example/SKILL.md", "slots/example/contract.json"],
            "without_skill": [],
        }
    }

    report = variance_verify.verify_variance(
        cases,
        tmp_path / "runs",
        ["case-1"],
        1,
        configuration,
    )

    assert report["passed"] is False
    assert report["cases"][0]["excluded_pairs"] == [
        {
            "run_number": 1,
            "reason": "with_skill: paths_read does not match expected configuration",
        }
    ]
