from pathlib import Path

from tools.curation.v2_skill_source_index import build

ROOT = Path(__file__).resolve().parents[2]


def test_source_index_covers_every_skill_body_with_line_evidence() -> None:
    index = build(ROOT)

    assert index["ok"] is True, index["errors"]
    assert index["root_count"] == 139
    assert index["line_count"] == 61361
    assert all(item["sha256"] and item["line_count"] > 0 and item["headings"] for item in index["records"])


def test_nested_roots_keep_distinct_source_identity() -> None:
    index = build(ROOT)
    paths = {item["path"] for item in index["records"]}

    assert "dd-apm/SKILL.md" in paths
    assert "dd-apm/k8s-ssi/agent-install/SKILL.md" in paths
    assert "gstack/SKILL.md" in paths
    assert "gstack/design-review/SKILL.md" in paths
