import json
from pathlib import Path

from tools.curation.v2_compile_root_dossiers import compile_all

ROOT = Path(__file__).resolve().parents[2]


def dossiers(path: Path) -> dict[str, dict]:
    return {
        item["root_id"]: item
        for file in path.glob("*.jsonl")
        for line in file.read_text(encoding="utf-8").splitlines()
        if line.strip()
        for item in [json.loads(line)]
    }


def test_compiler_covers_every_root_and_primary_owned_file(tmp_path: Path) -> None:
    result = compile_all(ROOT, tmp_path / "jsonl", tmp_path / "reports")

    assert result == {
        "gate": "capability-compiler-v2-dossier-compile",
        "ok": True,
        "dossier_count": 139,
        "reviewed_file_count": 2337,
        "fallback_reports": 3,
    }


def test_gstack_preamble_is_not_misclassified_as_capability_contract(tmp_path: Path) -> None:
    compile_all(ROOT, tmp_path / "jsonl", None)
    compiled = dossiers(tmp_path / "jsonl")
    autoplan = compiled["skill-root:gstack/autoplan"]

    assert "AUTO-GENERATED" not in autoplan["non_trigger"]
    assert "Source does not declare an explicit non-trigger" in autoplan["non_trigger"]
    assert all("RECENT ARTIFACTS" not in value for value in autoplan["inputs"])
    assert all("ARTIFACTS_SYNC" not in value for value in autoplan["outputs"])
    assert all("Preamble" not in value for value in autoplan["unique_methods"])
    assert all("AskUserQuestion" not in value for value in autoplan["unique_methods"])


def test_explicit_boundaries_and_dangerous_side_effects_are_preserved(tmp_path: Path) -> None:
    compile_all(ROOT, tmp_path / "jsonl", None)
    compiled = dossiers(tmp_path / "jsonl")
    deploy = compiled["skill-root:azure-kubernetes/azure-kubernetes-app-deploy"]
    land = compiled["skill-root:gstack/land-and-deploy"]

    assert deploy["non_trigger"].startswith("Not for:")
    assert "Source has no explicit output section" in deploy["outputs"][0]
    assert any("merge" in value.lower() or "deploy" in value.lower() for value in land["permissions_side_effects"])
    assert any(item["type"] == "duplicate" and item["target"] == "skill-root:land-and-deploy" for item in land["relationship_hypotheses"])
