import json
from pathlib import Path

from tools.curation.v2_cluster_comparison_gate import verify
from tools.curation.v2_compile_cluster_comparisons import compile_all

ROOT = Path(__file__).resolve().parents[2]


def compile_candidate(tmp_path: Path) -> tuple[Path, Path, dict]:
    comparisons = tmp_path / "comparisons"
    relationships = tmp_path / "relationships.json"
    result = compile_all(ROOT, comparisons, relationships)
    return comparisons, relationships, result


def test_compiler_covers_88_clusters_and_all_assigned_units(tmp_path: Path) -> None:
    comparisons, relationships, result = compile_candidate(tmp_path)

    assert result["ok"] is True, result["errors"]
    assert result["cluster_count"] == 88
    assert result["canonical_unit_count"] == 965
    assert result["retained_auxiliary_count"] == 104
    assert result["source_pair_audit_count"] == 232
    assert result["explicit_relationship_count"] == 17
    assert verify(ROOT, comparisons, relationships)["ok"] is True


def test_policy_sensitive_clusters_bind_owner_decisions(tmp_path: Path) -> None:
    comparisons, _, _ = compile_candidate(tmp_path)
    visual = json.loads((comparisons / "visual-language-and-anti-template-controls.json").read_text(encoding="utf-8"))
    priority = json.loads((comparisons / "opportunity-prioritization-and-frameworks.json").read_text(encoding="utf-8"))
    interviews = json.loads((comparisons / "customer-interview-execution.json").read_text(encoding="utf-8"))

    assert "V2-DEC-002" in visual["decision_references"]
    assert any("context-selected variants" in rule["rule"] for rule in visual["fusion_rules"])
    assert {"V2-DEC-003", "V2-DEC-005"} <= set(priority["decision_references"])
    assert any("exact formula" in rule["rule"] for rule in priority["fusion_rules"])
    assert "V2-DEC-004" in interviews["decision_references"]
    assert any("redaction" in rule["rule"] and "deletion policy" in rule["rule"] for rule in interviews["fusion_rules"])


def test_matrix_columns_are_semantically_distinct(tmp_path: Path) -> None:
    comparisons, _, _ = compile_candidate(tmp_path)

    for path in comparisons.glob("*.json"):
        data = json.loads(path.read_text(encoding="utf-8"))
        for cell in data["source_dimension_matrix"]:
            assert cell["approach"] != cell["strengths"]
            assert cell["approach"] != cell["limitations"]


def test_exact_duplicates_and_qa_permission_conflict_are_resolved(tmp_path: Path) -> None:
    _, relationships, _ = compile_candidate(tmp_path)
    audits = {item["cluster_id"]: item for item in json.loads(relationships.read_text(encoding="utf-8"))["cluster_audits"]}
    facilitation = audits["cluster:facilitation-and-collaboration-protocols"]
    qa = audits["cluster:developer-self-check-and-fix"]

    duplicates = [item for item in facilitation["relationships"] if item["type"] == "duplicate"]
    assert len(duplicates) == 2
    assert all(next(decision for decision in facilitation["decisions"] if decision["id"] == relation["decision_id"])["disposition"] == "merge" for relation in duplicates)
    conflict = next(item for item in qa["relationships"] if item["type"] == "conflict")
    decision = next(item for item in qa["decisions"] if item["id"] == conflict["decision_id"])
    assert decision["disposition"] == "branch"
    assert "independent-qa is report-only" in decision["rationale"]
