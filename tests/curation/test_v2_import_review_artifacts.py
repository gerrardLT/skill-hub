import json
from pathlib import Path

from tools.curation.v2_import_review_artifacts import import_artifacts

ROOT = Path(__file__).resolve().parents[2]


def test_review_import_refuses_partial_fanout(tmp_path: Path) -> None:
    source = tmp_path / "source"
    source.mkdir()
    source.joinpath("product.md").write_text("partial", encoding="utf-8")

    result = import_artifacts(ROOT, source, tmp_path / "output", "run-1")

    assert result["ok"] is False
    assert result["batch_count"] == 1
    assert any("missing source review artifact" in error for error in result["errors"])
    manifest = json.loads((tmp_path / "output/manifest.json").read_text(encoding="utf-8"))
    assert manifest["workflow_run_id"] == "run-1"


def test_review_import_requires_origin_for_every_batch_when_manifest_is_supplied(tmp_path: Path) -> None:
    source = tmp_path / "source"
    source.mkdir()
    for path in (ROOT / "curation/v2/reviews").glob("*.md"):
        source.joinpath(path.name).write_bytes(path.read_bytes())
    origins = tmp_path / "origins.json"
    origins.write_text(json.dumps({"batches": {"product": {"mode": "test"}}}), encoding="utf-8")

    result = import_artifacts(ROOT, source, tmp_path / "output", "mixed", origins)

    assert result["ok"] is False
    assert any("missing review origin: platform" == error for error in result["errors"])
