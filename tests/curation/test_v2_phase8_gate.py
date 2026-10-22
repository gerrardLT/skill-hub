import hashlib
import json
import shutil
from pathlib import Path

import pytest

import tools.curation.v2_phase8_gate as gate

ROOT = Path(__file__).resolve().parents[2]


def load(path: Path): return json.loads(path.read_text(encoding="utf-8"))
def write(path: Path, value) -> None: path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")


@pytest.fixture()
def candidate(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    files = [f".specs/capability-compiler-v2/phase-{phase}/artifact-manifest.json" for phase in range(2, 8)]
    files += [
        "curation/v2/lifecycle/phase-ownership.json",
        "curation/v2/lifecycle/stages.json",
        "curation/v2/lifecycle/dependencies.json",
        "curation/v2/lifecycle/handoffs.json",
        "curation/v2/capabilities",
        "curation/v2/phase-8",
        "evals/candidates/capability-compiler-v2/phase-8",
        "evals/candidates/capability-compiler-v2/phase-4/recipes/complete-ui-design-and-review.json",
    ]
    files += [f"evals/candidates/capability-compiler-v2/phase-{phase}/skills" for phase in range(3, 8)]
    for relative in files:
        source = ROOT / relative; target = tmp_path / relative; target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copytree(source, target) if source.is_dir() else shutil.copy2(source, target)
    monkeypatch.setattr(gate, "verify_phase7", lambda _: {"ok": True, "errors": []})
    return tmp_path


def check(candidate: Path, name: str) -> bool:
    return next(item["ok"] for item in gate.verify(candidate)["checks"] if item["name"] == name)


def stage(candidate: Path, recipe_id: str) -> Path:
    return candidate / f"evals/candidates/capability-compiler-v2/phase-8/recipes/stages/{recipe_id}.json"


def composite(candidate: Path, recipe_id: str) -> Path:
    return candidate / f"evals/candidates/capability-compiler-v2/phase-8/recipes/composites/{recipe_id}.json"


def test_phase8_artifact_manifest_recomputes_exactly() -> None:
    path = ROOT / ".specs/capability-compiler-v2/phase-8/artifact-manifest.json"; manifest = load(path)
    excluded = {path.relative_to(ROOT).as_posix(), ".specs/capability-compiler-v2/phase-8/phase-report.json"}; records = []
    for item in manifest["artifacts"]:
        assert item["path"] not in excluded
        artifact = ROOT / item["path"]; data = artifact.read_bytes().replace(b"\r\n", b"\n")
        assert artifact.stat().st_size == item["bytes"]
        assert hashlib.sha256(data).hexdigest() == item["sha256"]
        records.append(f"{item['path']}\0{item['sha256']}\n")
    assert len(records) == manifest["artifact_count"] == 33
    assert hashlib.sha256("".join(records).encode("utf-8")).hexdigest() == manifest["tree_sha256"] == "501d9cddfdc44fec4af8f17470c99b57b48ffced977e0fa7086cce568fa92f66"


def test_phase8_gate_accepts_complete_recipe_graph(candidate: Path) -> None:
    result = gate.verify(candidate)
    assert result["ok"] is True, result["errors"]
    assert result["counts"] == {
        "candidate_skills": 157,
        "stage_recipes": 15,
        "composite_recipes": 5,
        "specialized_recipes": 1,
        "mandatory_handoffs": 13,
        "dependencies": 249,
        "router_authored_cases": 14,
        "router_holdout_cases": 8,
        "recipe_authored_cases": 8,
        "recipe_holdout_cases": 6,
        "planned_mutations": 6,
        "protected_action_steps": 27,
    }


def test_phase8_gate_rejects_prior_tree_drift(candidate: Path) -> None:
    path = candidate / ".specs/capability-compiler-v2/phase-7/artifact-manifest.json"; value = load(path); value["tree_sha256"] = "0" * 64; write(path, value)
    assert check(candidate, "prior-phase-artifact-identities") is False


def test_phase8_gate_rejects_missing_stage_recipe(candidate: Path) -> None:
    stage(candidate, "stage-09-performance-reliability").unlink()
    assert check(candidate, "phase-8-artifact-inventory") is False
    assert check(candidate, "stage-skill-coverage-permission-and-dependencies") is False


def test_phase8_gate_rejects_duplicate_skill_coverage(candidate: Path) -> None:
    path = stage(candidate, "stage-08-verification-quality"); value = load(path); value["steps"].append(value["steps"][0]); write(path, value)
    assert check(candidate, "stage-skill-coverage-permission-and-dependencies") is False


def test_phase8_gate_rejects_wrong_primary_stage(candidate: Path) -> None:
    source = stage(candidate, "stage-08-verification-quality"); target = stage(candidate, "stage-07-implementation-integration")
    source_value = load(source); target_value = load(target); moved = source_value["steps"].pop(0); target_value["steps"].append(moved); write(source, source_value); write(target, target_value)
    assert check(candidate, "stage-skill-coverage-permission-and-dependencies") is False


def test_phase8_gate_rejects_review_scope_widening(candidate: Path) -> None:
    path = stage(candidate, "stage-08-verification-quality"); value = load(path); item = next(step for step in value["steps"] if step["id"] == "independent-code-review"); item["permission_identity"] = "workspace-write"; item["mutation_scope"] = "authorized-workspace"; write(path, value)
    assert check(candidate, "stage-skill-coverage-permission-and-dependencies") is False


def test_phase8_gate_rejects_remote_action_activation(candidate: Path) -> None:
    path = stage(candidate, "stage-11-deployment-change"); value = load(path); item = next(step for step in value["steps"] if step["id"] == "remote-git-push"); item["activation"] = "conditional"; write(path, value)
    assert check(candidate, "stage-skill-coverage-permission-and-dependencies") is False
    assert check(candidate, "review-change-observation-recovery-and-learning-separation") is False


def test_phase8_gate_rejects_authorized_local_git_activation(candidate: Path) -> None:
    path = stage(candidate, "stage-07-implementation-integration"); value = load(path); item = next(step for step in value["steps"] if step["id"] == "local-branch-integration"); assert item["mutation_scope"] == "authorized-local-git"; item["activation"] = "conditional"; write(path, value)
    assert check(candidate, "stage-skill-coverage-permission-and-dependencies") is False


def test_phase8_gate_rejects_dependency_deletion(candidate: Path) -> None:
    path = stage(candidate, "stage-08-verification-quality"); value = load(path); value["dependency_records"].pop(); write(path, value)
    assert check(candidate, "stage-skill-coverage-permission-and-dependencies") is False


def test_phase8_gate_rejects_mandatory_handoff_deletion(candidate: Path) -> None:
    path = composite(candidate, "full-software-lifecycle"); value = load(path); value["handoffs"] = [item for item in value["handoffs"] if item["id"] != "V2-HANDOFF-006"]; write(path, value)
    assert check(candidate, "composite-handoffs-human-checkpoints-and-invalidation") is False


def test_phase8_gate_rejects_invalidation_deletion(candidate: Path) -> None:
    path = composite(candidate, "full-software-lifecycle"); value = load(path); value["failure_policy"]["invalidate_downstream_on"].remove("source capability re-runs"); write(path, value)
    assert check(candidate, "composite-handoffs-human-checkpoints-and-invalidation") is False


def test_phase8_gate_rejects_human_checkpoint_bypass(candidate: Path) -> None:
    path = composite(candidate, "verified-change-delivery-and-observation"); value = load(path); value["human_checkpoints"].pop(0); write(path, value)
    assert check(candidate, "composite-handoffs-human-checkpoints-and-invalidation") is False


def test_phase8_gate_rejects_full_lifecycle_precedence(candidate: Path) -> None:
    path = candidate / "evals/candidates/capability-compiler-v2/phase-8/router.json"; value = load(path); full = value["composite_targets"].pop(); value["composite_targets"].insert(0, full); write(path, value)
    assert check(candidate, "minimal-router-specialized-route-and-safety-overrides") is False


def test_phase8_gate_rejects_specialized_ui_route_removal(candidate: Path) -> None:
    path = candidate / "evals/candidates/capability-compiler-v2/phase-8/router.json"; value = load(path); value["specialized_targets"] = []; write(path, value)
    assert check(candidate, "recipe-and-router-schemas") is False
    assert check(candidate, "minimal-router-specialized-route-and-safety-overrides") is False


def test_phase8_gate_rejects_router_holdout_leakage(candidate: Path) -> None:
    authored = load(candidate / "evals/candidates/capability-compiler-v2/phase-8/router-cases.json")["cases"][0]["id"]
    path = candidate / "evals/candidates/capability-compiler-v2/phase-8/router-holdout-cases.json"; value = load(path); value["cases"][0]["id"] = authored; write(path, value)
    assert check(candidate, "authored-holdout-and-mutation-fixtures") is False


def test_phase8_gate_rejects_false_evaluation_claim(candidate: Path) -> None:
    path = candidate / "evals/candidates/capability-compiler-v2/phase-8/evaluation-plan.json"; value = load(path); value["execution_state"] = "passed"; write(path, value)
    assert check(candidate, "authored-holdout-and-mutation-fixtures") is False


def test_phase8_gate_rejects_open_semantic_finding(candidate: Path) -> None:
    path = candidate / "curation/v2/phase-8/semantic-review.json"; value = load(path); value["open_findings"] = [{"id": "open"}]; write(path, value)
    assert check(candidate, "semantic-boundary-review") is False


def test_phase8_gate_rejects_stale_catalog_hash(candidate: Path) -> None:
    path = candidate / "evals/candidates/capability-compiler-v2/phase-8/catalog.json"; value = load(path); value["router"]["sha256"] = "0" * 64; write(path, value)
    assert check(candidate, "catalog-hashes-and-no-release-claim") is False
