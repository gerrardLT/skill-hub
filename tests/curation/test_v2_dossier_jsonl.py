import json
from pathlib import Path

from tools.curation.v2_compile_root_dossiers import compile_all
from tools.curation.v2_dossier_jsonl import import_jsonl

ROOT = Path(__file__).resolve().parents[2]


def test_dossier_import_rejects_partial_jsonl_before_updating_coverage(tmp_path: Path) -> None:
    jsonl = tmp_path / "jsonl"
    jsonl.mkdir()
    jsonl.joinpath("partial.jsonl").write_text(json.dumps({"root_id": "skill-root:x"}) + "\n", encoding="utf-8")
    coverage = tmp_path / "coverage.json"
    original = (ROOT / "curation/v2/coverage.json").read_bytes()
    coverage.write_bytes(original)

    result = import_jsonl(ROOT, jsonl, tmp_path / "dossiers", coverage)

    assert result["ok"] is False
    assert result["count"] == 1
    assert any("dossier schema" in error or "unknown dossier root" in error for error in result["errors"])
    assert coverage.read_bytes() == original


def test_import_recomputes_support_matches_after_reloading_dossiers(tmp_path: Path) -> None:
    jsonl = tmp_path / "jsonl"
    compile_all(ROOT, jsonl, None)
    coverage = tmp_path / "coverage.json"
    coverage.write_bytes((ROOT / "curation/v2/coverage.json").read_bytes())

    result = import_jsonl(ROOT, jsonl, tmp_path / "dossiers", coverage)

    assert result["ok"] is True
    assert result["count"] == 139
    assert result["reviewed_files"] == 2337
    stored = json.loads(coverage.read_text(encoding="utf-8"))
    assert stored["ok"] is True
    assert stored["counts"]["semantic-read"] + stored["counts"]["behavior-reviewed"] + stored["counts"]["excluded"] == 2337
    assert {item["v2_status"] for item in stored["roots"]} == {"semantic-read"}
