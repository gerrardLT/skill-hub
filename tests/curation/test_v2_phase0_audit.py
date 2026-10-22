import json
import shutil
from pathlib import Path

from tools.curation.v2_phase0_audit import audit, compare_expected, gaps, phase_report, raw_root_sha256

ROOT = Path(__file__).resolve().parents[2]


def test_phase0_recomputes_current_repository_facts() -> None:
    result = audit(ROOT)

    assert result["ok"] is True, result["errors"]
    assert result["counts"] == {
        "skill_roots_disk": 139,
        "skill_roots_inventory": 139,
        "coverage_sources": 64,
        "coverage_files": 603,
        "classified_source_files": 597,
        "unclassified_source_files": 1740,
        "covered_skill_roots": 64,
        "uncovered_skill_roots": 75,
        "coverage_read": 311,
        "coverage_excluded": 292,
        "unit_files": 57,
        "physical_units": 1079,
        "unique_units": 1079,
        "clustered_units": 965,
        "auxiliary_units": 114,
        "clusters": 88,
        "relationships": 15,
        "slots": 92,
        "released_slots": 10,
        "draft_skeleton_slots": 82,
        "other_unreleased_slots": 0,
    }
    assert result["root_drift"] == {"missing": [], "untracked": [], "changed": []}


def test_phase0_exposes_forward_work_without_faking_failure() -> None:
    result = audit(ROOT)
    gap_report = gaps(result)
    report = phase_report(result, gap_report)

    assert report["status"] == "passed-with-forward-gaps"
    assert gap_report["counts"]["uncovered-skill-root"] == 75
    assert gap_report["counts"]["unclassified-source-file"] == 1740
    assert gap_report["counts"]["auxiliary-unit-outside-canonical-clusters"] == 114
    assert gap_report["counts"]["unpurified-slot-skeleton"] == 82


def test_phase0_accepts_legacy_raw_root_hashes() -> None:
    inventory = json.loads((ROOT / "curation/inventory.json").read_text(encoding="utf-8"))
    expected = next(item for item in inventory["skill_roots"] if item["path"] == "agent-observability-eval-pipeline")

    assert raw_root_sha256(ROOT / "skills/agent-observability-eval-pipeline") == expected["snapshot_sha256"]


def test_phase0_fails_when_a_skill_root_changes(tmp_path: Path) -> None:
    shutil.copytree(ROOT / "skills", tmp_path / "skills")
    shutil.copytree(ROOT / "curation", tmp_path / "curation")
    shutil.copytree(ROOT / "slots", tmp_path / "slots")
    shutil.copytree(ROOT / "recipes", tmp_path / "recipes")
    target = tmp_path / "skills/test-driven-development/SKILL.md"
    target.write_text(target.read_text(encoding="utf-8") + "\nmutation\n", encoding="utf-8")

    result = audit(tmp_path)

    assert result["ok"] is False
    assert any("changed skill roots" in error for error in result["errors"])


def test_phase0_fails_when_v1_asset_changes_against_frozen_baseline(tmp_path: Path) -> None:
    expected = audit(ROOT)
    actual = json.loads(json.dumps(expected))
    actual["v1_assets"][0]["files"][0]["sha256"] = "0" * 64

    assert compare_expected(actual, expected) == ["V1 released assets changed"]
