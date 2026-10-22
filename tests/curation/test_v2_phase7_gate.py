import hashlib
import json
import shutil
from pathlib import Path

import pytest

import tools.curation.v2_phase7_gate as gate

ROOT = Path(__file__).resolve().parents[2]


def load(path: Path): return json.loads(path.read_text(encoding="utf-8"))
def write(path: Path, value) -> None: path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")


@pytest.fixture()
def candidate(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    paths = [
        ".specs/capability-compiler-v2/phase-2/artifact-manifest.json", ".specs/capability-compiler-v2/phase-3/artifact-manifest.json",
        ".specs/capability-compiler-v2/phase-4/artifact-manifest.json", ".specs/capability-compiler-v2/phase-5/artifact-manifest.json",
        ".specs/capability-compiler-v2/phase-6/artifact-manifest.json", "curation/v2/lifecycle/phase-ownership.json",
        "curation/v2/lifecycle/permission-identities.json", "curation/v2/capabilities", "curation/v2/phase-7",
        "evals/candidates/capability-compiler-v2/phase-7",
    ]
    baselines = {load(path)["baseline"]["identity"] for path in (ROOT / "evals/candidates/capability-compiler-v2/phase-7/skills").glob("*/evaluation-plan.json") if load(path)["baseline"]["kind"] == "source-skill"}
    paths.extend(f"skills/{name}/SKILL.md" for name in baselines)
    for relative in paths:
        source = ROOT / relative; target = tmp_path / relative; target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copytree(source, target) if source.is_dir() else shutil.copy2(source, target)
    monkeypatch.setattr(gate, "verify_phase6", lambda _: {"ok": True, "errors": []})
    return tmp_path


def check(candidate: Path, name: str) -> bool: return next(item["ok"] for item in gate.verify(candidate)["checks"] if item["name"] == name)


def refresh(candidate: Path, skill_id: str) -> None:
    directory = candidate / f"evals/candidates/capability-compiler-v2/phase-7/skills/{skill_id}"; provenance = load(directory / "provenance.json")
    for filename in ["SKILL.md", "contract.json", "trigger-cases.json"]: provenance["candidate_files"][filename] = gate.sha(directory / filename)
    write(directory / "provenance.json", provenance); evaluation = load(directory / "evaluation-plan.json"); evaluation["candidate"]["skill_sha256"] = gate.sha(directory / "SKILL.md"); evaluation["candidate"]["contract_sha256"] = gate.sha(directory / "contract.json"); write(directory / "evaluation-plan.json", evaluation)


def test_phase7_artifact_manifest_recomputes_exactly() -> None:
    path = ROOT / ".specs/capability-compiler-v2/phase-7/artifact-manifest.json"; manifest = load(path)
    excluded = {path.relative_to(ROOT).as_posix(), ".specs/capability-compiler-v2/phase-7/phase-report.json"}; records = []
    for item in manifest["artifacts"]:
        assert item["path"] not in excluded
        artifact = ROOT / item["path"]; data = artifact.read_bytes().replace(b"\r\n", b"\n")
        assert artifact.stat().st_size == item["bytes"]
        assert hashlib.sha256(data).hexdigest() == item["sha256"]
        records.append(f"{item['path']}\0{item['sha256']}\n")
    assert len(records) == manifest["artifact_count"] == 205
    assert hashlib.sha256("".join(records).encode("utf-8")).hexdigest() == manifest["tree_sha256"]


def test_phase7_gate_accepts_complete_candidates(candidate: Path) -> None:
    result = gate.verify(candidate)
    assert result["ok"] is True, result["errors"]
    assert result["counts"] == {"skills": 39, "batches": 3, "authored_trigger_cases": 234, "holdout_cases": 78, "planned_mutations": 39, "remote_write_candidates": 16, "observer_candidates": 12, "preflight_candidates": 2, "local_system_candidates": 1}


def test_phase7_gate_rejects_missing_candidate_without_crash(candidate: Path) -> None:
    shutil.rmtree(candidate / "evals/candidates/capability-compiler-v2/phase-7/skills/deployment-observation")
    result = gate.verify(candidate)
    assert result["ok"] is False
    assert check(candidate, "phase-7-inventory-and-review-batches") is False


def test_phase7_gate_rejects_observer_remote_write(candidate: Path) -> None:
    skill_id = "deployment-observation"; path = candidate / f"evals/candidates/capability-compiler-v2/phase-7/skills/{skill_id}/contract.json"; value = load(path)
    value["execution"]["remote_write"] = True; value["execution"]["mutation_scope"] = "remote-release-rollback"; write(path, value); refresh(candidate, skill_id)
    assert check(candidate, "permission-readiness-observation-and-action-separation") is False


def test_phase7_gate_rejects_preflight_remote_scope(candidate: Path) -> None:
    skill_id = "merge-and-deploy-readiness"; path = candidate / f"evals/candidates/capability-compiler-v2/phase-7/skills/{skill_id}/contract.json"; value = load(path)
    value["execution"]["remote_write"] = True; value["execution"]["mutation_scope"] = "remote-pr-merge"; write(path, value); refresh(candidate, skill_id)
    assert check(candidate, "permission-readiness-observation-and-action-separation") is False


def test_phase7_gate_rejects_remote_action_scope_collision(candidate: Path) -> None:
    skill_id = "remote-pull-request-merge"; path = candidate / f"evals/candidates/capability-compiler-v2/phase-7/skills/{skill_id}/contract.json"; value = load(path)
    value["execution"]["mutation_scope"] = "remote-git-push"; write(path, value); refresh(candidate, skill_id)
    assert check(candidate, "permission-readiness-observation-and-action-separation") is False


def test_phase7_gate_rejects_remote_execution_claim(candidate: Path) -> None:
    skill_id = "web-hosting-deployment"; path = candidate / f"evals/candidates/capability-compiler-v2/phase-7/skills/{skill_id}/contract.json"; value = load(path)
    value["execution"]["candidate_execution_state"] = "deployed"; write(path, value); refresh(candidate, skill_id)
    assert check(candidate, "candidate-schemas-hand-design-and-hashes") is False
    assert check(candidate, "permission-readiness-observation-and-action-separation") is False


def test_phase7_gate_rejects_remote_action_without_boundary(candidate: Path) -> None:
    skill_id = "remote-git-push"; path = candidate / f"evals/candidates/capability-compiler-v2/phase-7/skills/{skill_id}/SKILL.md"; text = path.read_text(encoding="utf-8")
    start = text.index("## Remote or Local-System Action Boundary"); end = text.index("## Status Mapping", start); path.write_text(text[:start] + text[end:], encoding="utf-8", newline="\n"); refresh(candidate, skill_id)
    assert check(candidate, "permission-readiness-observation-and-action-separation") is False


def test_phase7_gate_rejects_rollback_target_marker_removal(candidate: Path) -> None:
    skill_id = "release-rollback-execution"; path = candidate / f"evals/candidates/capability-compiler-v2/phase-7/skills/{skill_id}/contract.json"; value = load(path)
    value["policy"]["coverage"].remove("exact-recovery-target"); write(path, value); refresh(candidate, skill_id)
    assert check(candidate, "candidate-schemas-hand-design-and-hashes") is False
    assert check(candidate, "delivery-observability-incident-and-learning-invariants") is False


def test_phase7_gate_rejects_incident_provider_mutation_marker_removal(candidate: Path) -> None:
    skill_id = "incident-response-coordination"; path = candidate / f"evals/candidates/capability-compiler-v2/phase-7/skills/{skill_id}/contract.json"; value = load(path)
    value["policy"]["coverage"].remove("no-provider-mutation"); write(path, value); refresh(candidate, skill_id)
    assert check(candidate, "delivery-observability-incident-and-learning-invariants") is False


def test_phase7_gate_rejects_canary_auto_rollback_marker_removal(candidate: Path) -> None:
    skill_id = "production-canary-monitoring"; path = candidate / f"evals/candidates/capability-compiler-v2/phase-7/skills/{skill_id}/contract.json"; value = load(path)
    value["policy"]["coverage"].remove("no-auto-rollback"); write(path, value); refresh(candidate, skill_id)
    assert check(candidate, "delivery-observability-incident-and-learning-invariants") is False


def test_phase7_gate_rejects_local_learning_remote_write(candidate: Path) -> None:
    skill_id = "local-learning-persistence"; path = candidate / f"evals/candidates/capability-compiler-v2/phase-7/skills/{skill_id}/contract.json"; value = load(path)
    value["execution"]["remote_write"] = True; value["execution"]["mutation_scope"] = "remote-pr-change"; write(path, value); refresh(candidate, skill_id)
    assert check(candidate, "permission-readiness-observation-and-action-separation") is False


def test_phase7_gate_rejects_baseline_forgery(candidate: Path) -> None:
    path = candidate / "evals/candidates/capability-compiler-v2/phase-7/skills/deployment-observation/evaluation-plan.json"; value = load(path); value["baseline"]["identity"] = "ai-product-strategy"; write(path, value)
    assert check(candidate, "provenance-and-baseline-integrity") is False


def test_phase7_gate_rejects_holdout_leakage(candidate: Path) -> None:
    authored = load(candidate / "evals/candidates/capability-compiler-v2/phase-7/skills/remote-git-push/trigger-cases.json")["cases"][0]["id"]
    path = candidate / "evals/candidates/capability-compiler-v2/phase-7/holdout-cases.json"; value = load(path); value["cases"][0]["id"] = authored; write(path, value)
    assert check(candidate, "trigger-and-holdout-boundaries") is False


def test_phase7_gate_rejects_false_evaluation_claim(candidate: Path) -> None:
    path = candidate / "evals/candidates/capability-compiler-v2/phase-7/skills/production-canary-monitoring/evaluation-plan.json"; value = load(path); value["execution_state"] = "passed"; write(path, value)
    assert check(candidate, "evaluation-plans-and-semantic-mutations") is False


def test_phase7_gate_rejects_missing_semantic_marker(candidate: Path) -> None:
    skill_id = "remote-pull-request-merge"; directory = candidate / f"evals/candidates/capability-compiler-v2/phase-7/skills/{skill_id}"; evaluation = load(directory / "evaluation-plan.json"); marker = evaluation["mutations"][0]["remove_exact_text"]
    skill = directory / "SKILL.md"; skill.write_text(skill.read_text(encoding="utf-8").replace(marker, ""), encoding="utf-8", newline="\n"); refresh(candidate, skill_id)
    assert check(candidate, "candidate-schemas-hand-design-and-hashes") is False
    assert check(candidate, "evaluation-plans-and-semantic-mutations") is False


def test_phase7_gate_rejects_open_semantic_finding(candidate: Path) -> None:
    path = candidate / "curation/v2/phase-7/semantic-review.json"; value = load(path); value["open_findings"] = [{"id": "open"}]; write(path, value)
    assert check(candidate, "semantic-boundary-review") is False
