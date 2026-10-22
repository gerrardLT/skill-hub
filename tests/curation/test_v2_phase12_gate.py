import hashlib
import json
import shutil
from pathlib import Path

from tools.curation import v2_phase12_gate as gate
from tools.curation.generate_slots import generate

ROOT = Path(__file__).resolve().parents[2]


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def test_phase12_gate_accepts_exact_local_release() -> None:
    result = gate.verify(ROOT, require_final_report=True)
    assert result["ok"] is True, result["errors"]
    assert result["released"] is True
    assert result["counts"] == {"skills": 157, "stage_recipes": 15, "composite_recipes": 5, "specialized_recipes": 1, "routers": 1, "release_assets": 495, "protected_steps": 27, "v1_assets": 287, "remote_actions": 0}


def test_phase12_manifest_recomputes_exactly() -> None:
    manifest = load(ROOT / "curation/v2/release-1.0.0/manifest.json")
    rows = []
    for item in manifest["release_assets"]:
        path = ROOT / item["path"]
        assert path.stat().st_size == item["bytes"]
        assert hashlib.sha256(path.read_bytes()).hexdigest() == item["sha256"]
        rows.append(f"{item['path']}\0{item['sha256']}\n")
    assert len(rows) == 495
    assert hashlib.sha256("".join(rows).encode()).hexdigest() == "116651adca2b907b3629e7e1954cddcd15cf0388e3401facaf2e8cb5c210d852"


def test_phase12_gate_rejects_tampered_release_asset(tmp_path: Path) -> None:
    workspace = tmp_path / "workspace"
    for relative in ["slots/v2", "recipes/v2", "curation/v2/release-1.0.0", ".specs/capability-compiler-v2/phase-12"]:
        shutil.copytree(ROOT / relative, workspace / relative)
    path = workspace / "slots/v2/1.0.0/skills/problem-framing-and-customer-research/SKILL.md"
    path.write_text("tampered\n", encoding="utf-8")
    errors = gate.verify_release_assets(workspace)
    assert any("released asset mismatch" in error for error in errors)


def test_v1_generator_preserves_released_v2_subtree(tmp_path: Path) -> None:
    slots = tmp_path / "slots"
    marker = slots / "v2/catalog.json"
    marker.parent.mkdir(parents=True)
    marker.write_text('{"sentinel": true}\n', encoding="utf-8")
    queue = tmp_path / "queue.json"
    generate(ROOT / "curation/clusters.json", ROOT / "curation/units", ROOT / "curation/decisions.jsonl", slots, queue)
    assert marker.read_text(encoding="utf-8") == '{"sentinel": true}\n'
    assert queue.is_file()


def test_v1_verifier_excludes_only_reserved_v2_subtree() -> None:
    source = (ROOT / "tools/curation/slot_verify.py").read_text(encoding="utf-8")
    assert 'path.is_dir() and path.name != "v2"' in source
    assert "slots_root.rglob" not in source


def test_release_writer_creates_only_previewed_control_artifacts() -> None:
    source = (ROOT / "tools/curation/v2_phase12_release.py").read_text(encoding="utf-8")
    assert 'write(control / "release-receipt.json"' not in source
    assert 'write(control / "v1-pre-release-manifest.json"' not in source
