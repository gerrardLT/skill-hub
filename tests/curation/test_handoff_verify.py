import json
from pathlib import Path

from tools.curation import handoff_verify


UPSTREAM = """Status: passed
`SRC-1` source
`AUTH-1` authority
`FACT-1` fact
`OPEN-1` unknown
`REQ-1` requirement
`RULE-1` rule
`DEP-1` dependency
`SCOPE-1` scope
`AC-1` criterion
"""

DOWNSTREAM = """# QA handoff
QA is read-only: report findings; do not repair implementation or make product decisions.
Missing evidence must be reported as `BLOCKED`; do not infer unknown values.
Preserved: `SRC-1` `AUTH-1` `FACT-1` `OPEN-1` `REQ-1` `RULE-1` `DEP-1` `SCOPE-1` `AC-1`.
"""


def write_fixture(tmp_path: Path, downstream: str = DOWNSTREAM) -> tuple[Path, Path, Path]:
    upstream = tmp_path / "upstream.md"
    output = tmp_path / "outputs" / "test-handoff.md"
    evidence = tmp_path / "tool_evidence.raw.json"
    output.parent.mkdir()
    upstream.write_text(UPSTREAM, encoding="utf-8")
    output.write_text(downstream, encoding="utf-8")
    evidence.write_text(
        json.dumps(
            {
                "offline": True,
                "network_accessed": False,
                "skills_modified": False,
                "case_file_read": False,
                "rubric_read": False,
                "paths_read": [str(upstream)],
                "paths_written": [str(output), str(evidence)],
                "errors": [],
            }
        ),
        encoding="utf-8",
    )
    return upstream, output, evidence


def test_valid_handoff_preserves_contract_and_isolation(tmp_path: Path) -> None:
    upstream, output, evidence = write_fixture(tmp_path)

    report = handoff_verify.verify_handoff(upstream, output, evidence)

    assert report["passed"] is True
    assert report["missing_ids"] == []
    assert report["errors"] == []


def test_missing_upstream_id_fails_closed(tmp_path: Path) -> None:
    upstream, output, evidence = write_fixture(
        tmp_path,
        DOWNSTREAM.replace(" `OPEN-1`", ""),
    )

    report = handoff_verify.verify_handoff(upstream, output, evidence)

    assert report["passed"] is False
    assert report["missing_ids"] == ["OPEN-1"]


def test_non_isolated_or_repairing_handoff_fails(tmp_path: Path) -> None:
    upstream, output, evidence = write_fixture(
        tmp_path,
        DOWNSTREAM.replace("do not repair implementation", "repair implementation"),
    )
    data = json.loads(evidence.read_text(encoding="utf-8"))
    data["case_file_read"] = True
    evidence.write_text(json.dumps(data), encoding="utf-8")

    report = handoff_verify.verify_handoff(upstream, output, evidence)

    assert report["passed"] is False
    assert "handoff-read-case-file" in report["errors"]
    assert "qa-read-only-rule-missing" in report["errors"]
