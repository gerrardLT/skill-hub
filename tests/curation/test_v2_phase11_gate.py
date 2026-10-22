import hashlib
import json
import shutil
from pathlib import Path

import tools.curation.v2_phase11_gate as gate

ROOT = Path(__file__).resolve().parents[2]
CASE = ROOT / "evals/runs/capability-compiler-v2/phase-11/benchshare-v1"


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def test_phase11_artifact_manifest_recomputes_exactly() -> None:
    path = ROOT / ".specs/capability-compiler-v2/phase-11/artifact-manifest.json"
    manifest = load(path); records = []; excluded = {path.relative_to(ROOT).as_posix(), ".specs/capability-compiler-v2/phase-11/phase-report.json"}
    for item in manifest["artifacts"]:
        assert item["path"] not in excluded
        artifact = ROOT / item["path"]; data = artifact.read_bytes().replace(b"\r\n", b"\n")
        assert artifact.stat().st_size == item["bytes"]
        assert hashlib.sha256(data).hexdigest() == item["sha256"]
        records.append(f"{item['path']}\0{item['sha256']}\n")
    assert len(records) == manifest["artifact_count"]
    assert hashlib.sha256("".join(records).encode()).hexdigest() == manifest["tree_sha256"]


def test_phase11_gate_accepts_local_case_without_release_claim() -> None:
    result = gate.verify(ROOT)
    assert result["ok"] is True, result["errors"]
    assert result["eligible_for_phase_12"] is True
    assert result["final_user_release_approval"] is False
    assert result["released"] is False
    assert result["counts"] == {"application_tests": 14, "independent_code_findings_closed": 6, "browser_screenshots": 12, "blackbox_findings_closed": 2, "performance_runs": 130, "concurrent_approvals": 10, "package_files": 24, "remote_actions": 0}


def test_phase11_runtime_and_delivery_identities_recompute() -> None:
    result = gate.verify(ROOT)
    assert result["identities"] == {
        "phase10_tree_sha256": "7fd6640a563789257da77e1015be3f37033a3baf40ecaf9a4b9fa1fde7828d56",
        "runtime_tree_sha256": "708ea6b7ec0b169bcb7d2a36e77f5d6df9a3ff9a9df2446fee978419e7af7266",
        "package_sha256": "8fb653c637294f2a10edd3f9d540d6dabf74a9d1d1dded71e6ab3c0445cf3309",
        "patch_sha256": "15bf934015d39cdb2f0bb04185216474ba7641ceeec8293727c9c47907040a7f",
        "package_tree_sha256": "f2944d37e772da78b818a3210fe84fdea536a3be04b6c2f099f4c132840a1566",
    }


def test_phase11_browser_evidence_is_current_and_complete() -> None:
    report = load(CASE / "evidence/browser/iteration-3/report.json")
    assert report["passed"] is True and report["failures"] == []
    assert report["unexpected_console_errors"] == [] and report["page_errors"] == []
    assert len(report["screenshots"]) == 12
    assert {item["state"] for item in report["screenshots"]} == {
        "boot-loading", "no-session-mobile", "no-session-populated-equipment-empty-schedule",
        "member-empty-reservation-list", "member-field-validation", "member-submitting-disabled",
        "member-request-success-pending-ledger", "member-pending-mobile", "member-cancel-success",
        "coordinator-two-pending", "coordinator-approval-conflict-refreshed", "coordinator-empty-queue-after-decision",
    }
    assert all(hashlib.sha256((CASE / "evidence/browser/iteration-3" / item["path"]).read_bytes()).hexdigest() == item["sha256"] for item in report["screenshots"])


def test_phase11_failed_and_rejected_evidence_is_preserved() -> None:
    assert load(CASE / "evidence/browser/iteration-1/report.json")["passed"] is False
    assert load(CASE / "evidence/blackbox-qa/qa-output-iteration-2.json")["verdict"] == "findings"
    assert (CASE / "evidence/implementation-writer/attempt-1-command/launch-failure.json").is_file()
    assert (CASE / "package/iteration-1/package-receipt.json").is_file()
    semantic = load(ROOT / "curation/v2/phase-11/semantic-review.json")
    assert semantic["failure_retention"]["deleted_failures"] == 0
    assert semantic["failure_retention"]["thresholds_lowered"] is False


def test_phase11_gate_rejects_tampered_screenshot(tmp_path: Path, monkeypatch) -> None:
    source = ROOT / "evals/runs/capability-compiler-v2/phase-11"
    target = tmp_path / "evals/runs/capability-compiler-v2/phase-11"
    shutil.copytree(source, target)
    screenshot = target / "benchshare-v1/evidence/browser/iteration-3/screenshots/00-boot-loading.png"
    screenshot.write_bytes(b"tampered")
    real_case = gate.CASE
    monkeypatch.setattr(gate, "CASE", target / "benchshare-v1")
    try:
        result = gate.verify(ROOT)
    finally:
        monkeypatch.setattr(gate, "CASE", real_case)
    assert result["ok"] is False
    assert any("screenshot evidence invalid" in error for error in result["errors"])


def test_phase11_never_claims_final_approval_or_remote_action() -> None:
    review = load(ROOT / "curation/v2/phase-11/semantic-review.json")
    assert review["authority"]["final_user_release_approval"] is False
    assert review["authority"]["remote_actions"] == []
    assert review["authority"]["provider_actions"] == []
    assert review["authority"]["production_actions"] == []
    assert review["release_disposition"] == "eligible-for-phase-12-final-human-approval-not-released"
