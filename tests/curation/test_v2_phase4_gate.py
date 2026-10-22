import hashlib
import json
import shutil
from pathlib import Path

import pytest

import tools.curation.v2_phase4_gate as gate

ROOT = Path(__file__).resolve().parents[2]


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def write(path: Path, value) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")


@pytest.fixture()
def candidate(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    paths = [
        ".specs/capability-compiler-v2/phase-2/artifact-manifest.json",
        ".specs/capability-compiler-v2/phase-3/artifact-manifest.json",
        "curation/v2/lifecycle/phase-ownership.json",
        "curation/v2/lifecycle/permission-identities.json",
        "curation/v2/capabilities",
        "curation/v2/phase-4",
        "evals/candidates/capability-compiler-v2/phase-4",
        "recipes/design-web-flow.json",
        "slots/design-context-and-direction-contract/contract.json",
    ]
    source_baselines = {
        load(path)["baseline"]["identity"]
        for path in (ROOT / "evals/candidates/capability-compiler-v2/phase-4/skills").glob("*/evaluation-plan.json")
        if load(path)["baseline"]["kind"] == "source-skill"
    }
    paths.extend(f"skills/{name}/SKILL.md" for name in source_baselines)
    for relative in paths:
        source = ROOT / relative; target = tmp_path / relative; target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copytree(source, target) if source.is_dir() else shutil.copy2(source, target)
    monkeypatch.setattr(gate, "verify_phase3", lambda _: {"ok": True, "errors": []})
    return tmp_path


def check(candidate: Path, name: str) -> bool:
    return next(item["ok"] for item in gate.verify(candidate)["checks"] if item["name"] == name)


def refresh_skill_hashes(candidate: Path, skill_id: str) -> None:
    directory = candidate / f"evals/candidates/capability-compiler-v2/phase-4/skills/{skill_id}"
    provenance = load(directory / "provenance.json")
    for filename in ["SKILL.md", "contract.json", "trigger-cases.json"]: provenance["candidate_files"][filename] = gate.sha(directory / filename)
    write(directory / "provenance.json", provenance)
    evaluation = load(directory / "evaluation-plan.json"); evaluation["candidate"]["skill_sha256"] = gate.sha(directory / "SKILL.md"); evaluation["candidate"]["contract_sha256"] = gate.sha(directory / "contract.json"); write(directory / "evaluation-plan.json", evaluation)


def refresh_recipe_hash(candidate: Path) -> None:
    recipe = candidate / "evals/candidates/capability-compiler-v2/phase-4/recipes/complete-ui-design-and-review.json"
    plan = recipe.parent / "evaluation-plan.json"; value = load(plan); value["candidate_sha256"] = gate.sha(recipe); write(plan, value)


def test_phase4_artifact_manifest_recomputes_exactly() -> None:
    path = ROOT / ".specs/capability-compiler-v2/phase-4/artifact-manifest.json"; manifest = load(path)
    excluded = {path.relative_to(ROOT).as_posix(), ".specs/capability-compiler-v2/phase-4/phase-report.json"}
    records = []
    for item in manifest["artifacts"]:
        assert item["path"] not in excluded
        artifact = ROOT / item["path"]; data = artifact.read_bytes().replace(b"\r\n", b"\n")
        assert artifact.stat().st_size == item["bytes"]
        assert hashlib.sha256(data).hexdigest() == item["sha256"]
        records.append(f"{item['path']}\0{item['sha256']}\n")
    assert len(records) == manifest["artifact_count"] == 99
    assert hashlib.sha256("".join(records).encode("utf-8")).hexdigest() == manifest["tree_sha256"]


def test_phase4_gate_accepts_complete_candidates_and_recipe(candidate: Path) -> None:
    result = gate.verify(candidate)
    assert result["ok"] is True, result["errors"]
    assert result["counts"] == {"skills": 17, "authored_trigger_cases": 102, "holdout_cases": 34, "planned_skill_mutations": 17, "recipes": 1, "recipe_authored_cases": 8, "recipe_holdout_cases": 4, "recipe_mutations": 2}


def test_phase4_gate_rejects_missing_skill(candidate: Path) -> None:
    shutil.rmtree(candidate / "evals/candidates/capability-compiler-v2/phase-4/skills/responsive-layout-and-spatial-composition")
    result = gate.verify(candidate)
    assert result["ok"] is False
    assert check(candidate, "phase-4-candidate-inventory") is False


def test_phase4_gate_rejects_review_source_write(candidate: Path) -> None:
    skill_id = "rendered-ui-critique-and-release-disposition"; path = candidate / f"evals/candidates/capability-compiler-v2/phase-4/skills/{skill_id}/contract.json"
    value = load(path); value["execution"]["model_tools"] = ["read", "edit", "write"]; value["execution"]["mutation_scope"] = "authorized-workspace"; write(path, value); refresh_skill_hashes(candidate, skill_id)
    assert check(candidate, "permission-and-review-repair-separation") is False


def test_phase4_gate_rejects_external_token_network_authority(candidate: Path) -> None:
    skill_id = "external-design-token-extraction-and-normalization"; path = candidate / f"evals/candidates/capability-compiler-v2/phase-4/skills/{skill_id}/contract.json"
    value = load(path); value["execution"]["external"] = "read-only"; value["execution"]["host_actions"] = ["approved-provider-read"]; write(path, value); refresh_skill_hashes(candidate, skill_id)
    assert check(candidate, "permission-and-review-repair-separation") is False


def test_phase4_gate_rejects_static_inspection_as_rendered_evidence(candidate: Path) -> None:
    skill_id = "rendered-ui-critique-and-release-disposition"; path = candidate / f"evals/candidates/capability-compiler-v2/phase-4/skills/{skill_id}/SKILL.md"
    path.write_text(path.read_text(encoding="utf-8").replace("static source inspection", "source inspection"), encoding="utf-8", newline="\n"); refresh_skill_hashes(candidate, skill_id)
    assert check(candidate, "complete-ui-coverage-and-rendered-evidence") is False


def test_phase4_gate_rejects_missing_state_coverage(candidate: Path) -> None:
    skill_id = "interaction-states-forms-and-navigation"; path = candidate / f"evals/candidates/capability-compiler-v2/phase-4/skills/{skill_id}/contract.json"
    value = load(path); value["policy"]["coverage"].remove("recovery"); write(path, value); refresh_skill_hashes(candidate, skill_id)
    assert check(candidate, "complete-ui-coverage-and-rendered-evidence") is False


def test_phase4_gate_rejects_authored_holdout_leakage(candidate: Path) -> None:
    authored = load(candidate / "evals/candidates/capability-compiler-v2/phase-4/skills/design-context-and-direction-contract/trigger-cases.json")["cases"][0]["id"]
    path = candidate / "evals/candidates/capability-compiler-v2/phase-4/holdout-cases.json"; value = load(path); value["cases"][0]["id"] = authored; write(path, value)
    assert check(candidate, "trigger-and-holdout-boundaries") is False


def test_phase4_gate_rejects_false_skill_evaluation_claim(candidate: Path) -> None:
    path = candidate / "evals/candidates/capability-compiler-v2/phase-4/skills/visual-language-and-anti-template-controls/evaluation-plan.json"
    value = load(path); value["execution_state"] = "passed"; write(path, value)
    assert check(candidate, "evaluation-plans-and-semantic-mutations") is False


def test_phase4_gate_rejects_missing_skill_semantic_marker(candidate: Path) -> None:
    skill_id = "accessibility-contracts-and-assistive-validation"; directory = candidate / f"evals/candidates/capability-compiler-v2/phase-4/skills/{skill_id}"
    evaluation = load(directory / "evaluation-plan.json"); marker = evaluation["mutations"][0]["remove_exact_text"]
    skill = directory / "SKILL.md"; skill.write_text(skill.read_text(encoding="utf-8").replace(marker, ""), encoding="utf-8", newline="\n"); refresh_skill_hashes(candidate, skill_id)
    assert check(candidate, "candidate-schemas-semantic-design-and-hashes") is False
    assert check(candidate, "evaluation-plans-and-semantic-mutations") is False


def test_phase4_gate_rejects_recipe_permission_widening(candidate: Path) -> None:
    path = candidate / "evals/candidates/capability-compiler-v2/phase-4/recipes/complete-ui-design-and-review.json"; value = load(path)
    next(step for step in value["steps"] if step["id"] == "release-gate")["mutation_scope"] = "authorized-workspace"; write(path, value); refresh_recipe_hash(candidate)
    assert check(candidate, "conditional-ui-recipe") is False


def test_phase4_gate_rejects_recipe_without_render_evidence_step(candidate: Path) -> None:
    path = candidate / "evals/candidates/capability-compiler-v2/phase-4/recipes/complete-ui-design-and-review.json"; value = load(path)
    value["steps"] = [step for step in value["steps"] if step["id"] != "review-evidence"]; value["edges"] = [edge for edge in value["edges"] if edge["from"] != "review-evidence" and edge["to"] != "review-evidence"]; write(path, value); refresh_recipe_hash(candidate)
    assert check(candidate, "conditional-ui-recipe") is False


def test_phase4_gate_rejects_recipe_without_human_repair_checkpoint(candidate: Path) -> None:
    path = candidate / "evals/candidates/capability-compiler-v2/phase-4/recipes/complete-ui-design-and-review.json"; value = load(path)
    value["human_checkpoints"].remove("authorize source remediation separately from every review finding"); write(path, value); refresh_recipe_hash(candidate)
    assert check(candidate, "conditional-ui-recipe") is False


def test_phase4_gate_rejects_open_semantic_finding(candidate: Path) -> None:
    path = candidate / "curation/v2/phase-4/semantic-review.json"; value = load(path); value["open_findings"] = [{"id": "open"}]; write(path, value)
    assert check(candidate, "semantic-boundary-review") is False
