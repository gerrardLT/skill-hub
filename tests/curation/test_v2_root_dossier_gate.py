import json
from pathlib import Path

from tools.curation.v2_root_dossier_gate import verify

ROOT = Path(__file__).resolve().parents[2]


def test_dossier_gate_rejects_missing_roots(tmp_path: Path) -> None:
    result = verify(ROOT, tmp_path)

    assert result["ok"] is False
    assert result["expected"] == 139
    assert result["checked"] == 0
    assert any("missing root dossiers" in error for error in result["errors"])


def test_dossier_gate_validates_identity_and_evidence(tmp_path: Path) -> None:
    index = json.loads((ROOT / "curation/v2/source-index.json").read_text(encoding="utf-8"))
    ledger = json.loads((ROOT / "curation/v2/coverage.json").read_text(encoding="utf-8"))
    files = {item["path"]: item for item in ledger["files"]}
    for source in index["records"]:
        supports = [item for item in files.values() if item["primary_owner"] == source["root_id"]]
        data = {
            "root_id": source["root_id"], "skill_path": source["path"], "source_sha256": source["sha256"],
            "trigger": "trigger", "non_trigger": "non-trigger", "responsibility": "responsibility", "non_responsibility": "non-responsibility",
            "inputs": ["input"], "outputs": ["output"], "workflow": ["step"], "branches": [], "rules_gates": ["gate"], "stop_conditions": [],
            "tools_dependencies": [], "permissions_side_effects": [], "unique_methods": ["method"], "weaknesses_failure_modes": ["weakness"], "relationship_hypotheses": [],
            "source_citations": [{"path": source["path"], "line_start": 1, "line_end": min(2, source["line_count"])}],
            "support_file_reviews": [{"path": support["path"], "disposition": "semantic-read", "reason": None, "subkind": None, "evidence": ["review"]} for support in supports],
        }
        path = tmp_path / (source["root_id"].replace("skill-root:", "").replace("/", "__") + ".json")
        path.write_text(json.dumps(data), encoding="utf-8")

    result = verify(ROOT, tmp_path)

    assert result["ok"] is True, result["errors"]
    assert result["checked"] == 139


def test_dossier_gate_rejects_bounded_glob_outside_root(tmp_path: Path) -> None:
    index = json.loads((ROOT / "curation/v2/source-index.json").read_text(encoding="utf-8"))["records"][0]
    data = {
        "root_id": index["root_id"], "skill_path": index["path"], "source_sha256": index["sha256"],
        "trigger": "trigger", "non_trigger": "non-trigger", "responsibility": "responsibility", "non_responsibility": "non-responsibility",
        "inputs": ["input"], "outputs": ["output"], "workflow": ["step"], "branches": [], "rules_gates": ["gate"], "stop_conditions": [],
        "tools_dependencies": [], "permissions_side_effects": [], "unique_methods": ["method"], "weaknesses_failure_modes": ["weakness"], "relationship_hypotheses": [],
        "source_citations": [{"path": index["path"], "line_start": 1, "line_end": 2}],
        "support_file_reviews": [{"path": "other-root/**", "disposition": "excluded", "reason": "wrong root", "subkind": "irrelevant-to-capability", "evidence": ["review"]}],
    }
    (tmp_path / "one.json").write_text(json.dumps(data), encoding="utf-8")

    result = verify(ROOT, tmp_path)

    assert result["ok"] is False
    assert any("invalid support review" in error for error in result["errors"])
