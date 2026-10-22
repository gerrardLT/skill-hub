import hashlib
import json
import shutil
from pathlib import Path

import pytest

import tools.curation.v2_phase3_gate as gate

ROOT = Path(__file__).resolve().parents[2]


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def write(path: Path, value) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")


@pytest.fixture()
def candidate(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    relative_paths = [
        ".specs/capability-compiler-v2/phase-2/artifact-manifest.json",
        "curation/v2/lifecycle/phase-ownership.json",
        "curation/v2/capabilities",
        "curation/v2/fusion/decisions.jsonl",
        "curation/v2/phase-3",
        "evals/candidates/capability-compiler-v2/phase-3",
        "slots/problem-framing/contract.json",
        "slots/requirements-quality-gate/contract.json",
    ]
    source_baselines = {
        load(path)["baseline"]["identity"]
        for path in (ROOT / "evals/candidates/capability-compiler-v2/phase-3/skills").glob("*/evaluation-plan.json")
        if load(path)["baseline"]["kind"] == "source-skill"
    }
    relative_paths.extend(f"skills/{baseline}/SKILL.md" for baseline in source_baselines)
    for relative in relative_paths:
        source = ROOT / relative; target = tmp_path / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copytree(source, target) if source.is_dir() else shutil.copy2(source, target)
    monkeypatch.setattr(gate, "verify_phase2", lambda _: {"ok": True, "errors": []})
    return tmp_path


def check(candidate: Path, name: str) -> bool:
    result = gate.verify(candidate)
    return next(item["ok"] for item in result["checks"] if item["name"] == name)


def test_phase3_artifact_manifest_recomputes_exactly() -> None:
    path = ROOT / ".specs/capability-compiler-v2/phase-3/artifact-manifest.json"; manifest = load(path)
    artifact_paths = {item["path"] for item in manifest["artifacts"]}
    assert path.relative_to(ROOT).as_posix() not in artifact_paths
    assert ".specs/capability-compiler-v2/phase-3/phase-report.json" not in artifact_paths
    records = []
    for item in manifest["artifacts"]:
        artifact = ROOT / item["path"]; data = artifact.read_bytes().replace(b"\r\n", b"\n")
        assert artifact.stat().st_size == item["bytes"]
        assert hashlib.sha256(data).hexdigest() == item["sha256"]
        records.append(f"{item['path']}\0{item['sha256']}\n")
    assert len(records) == manifest["artifact_count"] == 164
    assert hashlib.sha256("".join(records).encode("utf-8")).hexdigest() == manifest["tree_sha256"]


def test_phase3_gate_accepts_complete_candidate(candidate: Path) -> None:
    result = gate.verify(candidate)
    assert result["ok"] is True, result["errors"]
    assert result["counts"] == {"skills": 31, "authored_trigger_cases": 186, "holdout_cases": 62, "planned_mutations": 31}


def test_phase3_gate_rejects_missing_skill(candidate: Path) -> None:
    shutil.rmtree(candidate / "evals/candidates/capability-compiler-v2/phase-3/skills/problem-framing-and-customer-research")
    assert check(candidate, "phase-3-candidate-inventory") is False


def test_phase3_gate_rejects_provenance_drift(candidate: Path) -> None:
    path = candidate / "evals/candidates/capability-compiler-v2/phase-3/skills/customer-interview-execution/provenance.json"
    value = load(path); value["source_evidence"].pop(); write(path, value)
    assert check(candidate, "provenance-set-equality") is False


def test_phase3_gate_rejects_generic_boundary_case(candidate: Path) -> None:
    path = candidate / "evals/candidates/capability-compiler-v2/phase-3/skills/data-analysis-validation/trigger-cases.json"
    value = load(path); boundary = next(case for case in value["cases"] if case["kind"] == "boundary")
    boundary["input"] = "The request lacks a source, scope, or decision owner needed to preserve traceability."
    write(path, value)
    assert check(candidate, "trigger-and-holdout-boundaries") is False


def test_phase3_gate_rejects_authored_holdout_overlap(candidate: Path) -> None:
    path = candidate / "evals/candidates/capability-compiler-v2/phase-3/holdout-cases.json"
    value = load(path); value["cases"][0]["id"] = "V2-P3-ai-product-opportunity-and-wedge-trigger-01"; write(path, value)
    assert check(candidate, "trigger-and-holdout-boundaries") is False


def test_phase3_gate_rejects_read_only_review_mutation(candidate: Path) -> None:
    path = candidate / "evals/candidates/capability-compiler-v2/phase-3/skills/executive-plan-review/contract.json"
    value = load(path); value["execution"]["model_tools"] = ["read", "write"]; value["execution"]["mutation_scope"] = "run-output"; write(path, value)
    assert check(candidate, "candidate-schemas-contracts-and-hashes") is False


def test_phase3_gate_rejects_missing_named_formula_policy(candidate: Path) -> None:
    path = candidate / "evals/candidates/capability-compiler-v2/phase-3/skills/opportunity-prioritization-and-frameworks/SKILL.md"
    path.write_text(path.read_text(encoding="utf-8").replace("## Named Formula Variants", "## Formula Notes"), encoding="utf-8", newline="\n")
    provenance = candidate / "evals/candidates/capability-compiler-v2/phase-3/skills/opportunity-prioritization-and-frameworks/provenance.json"
    value = load(provenance); value["candidate_files"]["SKILL.md"] = gate.sha(path); write(provenance, value)
    evaluation = candidate / "evals/candidates/capability-compiler-v2/phase-3/skills/opportunity-prioritization-and-frameworks/evaluation-plan.json"
    value = load(evaluation); value["candidate"]["skill_sha256"] = gate.sha(path); write(evaluation, value)
    assert check(candidate, "product-formula-data-and-authority-policy") is False


def test_phase3_gate_rejects_false_evaluation_claim(candidate: Path) -> None:
    path = candidate / "evals/candidates/capability-compiler-v2/phase-3/skills/qualitative-evidence-synthesis/evaluation-plan.json"
    value = load(path); value["execution_state"] = "passed"; write(path, value)
    assert check(candidate, "evaluation-plans-and-mutation-detection") is False


def test_phase3_gate_rejects_open_semantic_finding(candidate: Path) -> None:
    path = candidate / "curation/v2/phase-3/semantic-review.json"; value = load(path)
    value["open_findings"] = [{"id": "unresolved"}]; write(path, value)
    assert check(candidate, "semantic-boundary-review") is False


def test_phase3_gate_rejects_missing_semantic_marker(candidate: Path) -> None:
    directory = candidate / "evals/candidates/capability-compiler-v2/phase-3/skills/problem-framing-and-customer-research"
    evaluation = load(directory / "evaluation-plan.json"); marker = evaluation["mutations"][0]["remove_exact_text"]
    skill = directory / "SKILL.md"; skill.write_text(skill.read_text(encoding="utf-8").replace(marker, ""), encoding="utf-8", newline="\n")
    provenance = load(directory / "provenance.json"); provenance["candidate_files"]["SKILL.md"] = gate.sha(skill); write(directory / "provenance.json", provenance)
    evaluation["candidate"]["skill_sha256"] = gate.sha(skill); write(directory / "evaluation-plan.json", evaluation)
    assert check(candidate, "candidate-schemas-contracts-and-hashes") is False
    assert check(candidate, "evaluation-plans-and-mutation-detection") is False
