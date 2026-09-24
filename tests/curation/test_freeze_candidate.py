import hashlib
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from tools.curation.freeze_candidate import freeze


def test_freeze_records_sorted_workspace_paths_hashes_and_bytes(tmp_path: Path) -> None:
    candidate = tmp_path / "candidate"
    candidate.mkdir()
    (candidate / "b.md").write_text("b", encoding="utf-8")
    (candidate / "a.md").write_text("alpha", encoding="utf-8")

    result = freeze(candidate, tmp_path)

    assert [item["path"] for item in result["files"]] == ["candidate/a.md", "candidate/b.md"]
    assert result["files"][0]["bytes"] == 5
    assert result["files"][0]["sha256"] == hashlib.sha256(b"alpha").hexdigest()
