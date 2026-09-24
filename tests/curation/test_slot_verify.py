import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

from tools.curation import slot_verify


ROOT = Path(__file__).resolve().parents[2]
VERIFIER = ROOT / "tools" / "curation" / "slot_verify.py"


def copy_fixture(tmp_path: Path) -> dict[str, Path]:
    paths = {
        "clusters": tmp_path / "clusters.json",
        "units": tmp_path / "units",
        "slots": tmp_path / "slots",
        "queue": tmp_path / "queue.json",
        "status": tmp_path / "status.json",
        "inventory": tmp_path / "inventory.json",
    }
    shutil.copy(ROOT / "curation" / "clusters.json", paths["clusters"])
    shutil.copytree(ROOT / "curation" / "units", paths["units"])
    shutil.copytree(ROOT / "slots", paths["slots"])
    shutil.copy(ROOT / "curation" / "slot-review-queue.json", paths["queue"])
    shutil.copy(ROOT / "curation" / "slot-release-status.json", paths["status"])
    shutil.copy(ROOT / "curation" / "inventory.json", paths["inventory"])
    return paths


def run_verify(paths: dict[str, Path]) -> dict[str, object]:
    return slot_verify.verify(
        paths["clusters"], paths["units"], paths["slots"], paths["queue"],
        paths["status"], paths["inventory"],
    )


def first_slot(paths: dict[str, Path]) -> Path:
    cluster = json.loads(paths["clusters"].read_text(encoding="utf-8"))["clusters"][0]
    return paths["slots"] / cluster["id"].removeprefix("cluster:")


def test_duplicate_unit_fails(tmp_path: Path) -> None:
    paths = copy_fixture(tmp_path)
    provenance_path = first_slot(paths) / "provenance.json"
    provenance = json.loads(provenance_path.read_text(encoding="utf-8"))
    provenance["units"].append(provenance["units"][0])
    provenance_path.write_text(json.dumps(provenance), encoding="utf-8")

    result = run_verify(paths)

    assert result["ok"] is False
    assert any("exactly once" in error for error in result["errors"])


def test_missing_slot_fails(tmp_path: Path) -> None:
    paths = copy_fixture(tmp_path)
    shutil.rmtree(first_slot(paths))

    result = run_verify(paths)

    assert result["ok"] is False
    assert any("status-list slot ids do not match" in error for error in result["errors"])


def test_fake_release_without_evidence_fails(tmp_path: Path) -> None:
    paths = copy_fixture(tmp_path)
    status = json.loads(paths["status"].read_text(encoding="utf-8"))
    status["items"][0].update({"disposition": "released", "evaluation_references": [], "release_evidence": []})
    status["items"][0].pop("review", None)
    paths["status"].write_text(json.dumps(status), encoding="utf-8")

    result = run_verify(paths)

    assert result["ok"] is False
    assert any("released slot lacks evidence" in error for error in result["errors"])
    assert any("lacks valid review evidence" in error for error in result["errors"])


def test_pending_draft_disposition_fails_gate(tmp_path: Path) -> None:
    paths = copy_fixture(tmp_path)
    status = json.loads(paths["status"].read_text(encoding="utf-8"))
    status["items"][0]["disposition"] = "draft"
    paths["status"].write_text(json.dumps(status), encoding="utf-8")

    result = run_verify(paths)

    assert result["ok"] is False
    assert any("disposition is not final" in error for error in result["errors"])


def test_honest_unreleased_full_coverage_passes_and_cli_outputs_json(tmp_path: Path) -> None:
    paths = copy_fixture(tmp_path)

    result = run_verify(paths)

    assert result == {
        "gate": "phase-6-slot-coverage-release",
        "ok": True,
        "cluster_count": 88,
        "slot_count": 92,
        "unit_count": 965,
        "mapped_unit_count": 965,
        "errors": [],
    }
    env = os.environ.copy()
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    completed = subprocess.run(
        [
            sys.executable, str(VERIFIER), "--clusters", str(paths["clusters"]),
            "--units-root", str(paths["units"]), "--slots-root", str(paths["slots"]),
            "--review-queue", str(paths["queue"]), "--release-status", str(paths["status"]),
            "--inventory", str(paths["inventory"]),
        ],
        cwd=ROOT, capture_output=True, text=True, encoding="utf-8", env=env,
    )
    assert completed.returncode == 0, completed.stderr
    assert json.loads(completed.stdout)["ok"] is True
