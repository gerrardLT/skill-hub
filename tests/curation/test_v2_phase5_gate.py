import hashlib
import json
import shutil
from pathlib import Path

import pytest

import tools.curation.v2_phase5_gate as gate

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
        ".specs/capability-compiler-v2/phase-4/artifact-manifest.json",
        "curation/v2/lifecycle/phase-ownership.json",
        "curation/v2/lifecycle/permission-identities.json",
        "curation/v2/capabilities",
        "curation/v2/phase-5",
        "evals/candidates/capability-compiler-v2/phase-5",
    ]
    baselines = {
        load(path)["baseline"]["identity"]
        for path in (ROOT / "evals/candidates/capability-compiler-v2/phase-5/skills").glob("*/evaluation-plan.json")
        if load(path)["baseline"]["kind"] == "source-skill"
    }
    paths.extend(f"skills/{name}/SKILL.md" for name in baselines)
    for relative in paths:
        source = ROOT / relative; target = tmp_path / relative; target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copytree(source, target) if source.is_dir() else shutil.copy2(source, target)
    monkeypatch.setattr(gate, "verify_phase4", lambda _: {"ok": True, "errors": []})
    return tmp_path


def check(candidate: Path, name: str) -> bool:
    return next(item["ok"] for item in gate.verify(candidate)["checks"] if item["name"] == name)


def refresh_hashes(candidate: Path, skill_id: str) -> None:
    directory = candidate / f"evals/candidates/capability-compiler-v2/phase-5/skills/{skill_id}"
    provenance = load(directory / "provenance.json")
    for filename in ["SKILL.md", "contract.json", "trigger-cases.json"]: provenance["candidate_files"][filename] = gate.sha(directory / filename)
    write(directory / "provenance.json", provenance)
    evaluation = load(directory / "evaluation-plan.json"); evaluation["candidate"]["skill_sha256"] = gate.sha(directory / "SKILL.md"); evaluation["candidate"]["contract_sha256"] = gate.sha(directory / "contract.json"); write(directory / "evaluation-plan.json", evaluation)


def test_phase5_artifact_manifest_recomputes_exactly() -> None:
    path = ROOT / ".specs/capability-compiler-v2/phase-5/artifact-manifest.json"; manifest = load(path)
    excluded = {path.relative_to(ROOT).as_posix(), ".specs/capability-compiler-v2/phase-5/phase-report.json"}; records = []
    for item in manifest["artifacts"]:
        assert item["path"] not in excluded
        artifact = ROOT / item["path"]; data = artifact.read_bytes().replace(b"\r\n", b"\n")
        assert artifact.stat().st_size == item["bytes"]
        assert hashlib.sha256(data).hexdigest() == item["sha256"]
        records.append(f"{item['path']}\0{item['sha256']}\n")
    assert len(records) == manifest["artifact_count"] == 89
    assert hashlib.sha256("".join(records).encode("utf-8")).hexdigest() == manifest["tree_sha256"]


def test_phase5_gate_accepts_complete_candidates(candidate: Path) -> None:
    result = gate.verify(candidate)
    assert result["ok"] is True, result["errors"]
    assert result["counts"] == {"skills": 16, "authored_trigger_cases": 96, "holdout_cases": 32, "planned_mutations": 16}


def test_phase5_gate_rejects_missing_skill(candidate: Path) -> None:
    shutil.rmtree(candidate / "evals/candidates/capability-compiler-v2/phase-5/skills/data-and-api-contract-design")
    assert gate.verify(candidate)["ok"] is False
    assert check(candidate, "phase-5-candidate-inventory") is False


def test_phase5_gate_rejects_provenance_baseline_forgery(candidate: Path) -> None:
    skill_id = "authorization-and-permission-contracts"; path = candidate / f"evals/candidates/capability-compiler-v2/phase-5/skills/{skill_id}/evaluation-plan.json"
    value = load(path); value["baseline"]["identity"] = "ai-product-strategy"; write(path, value)
    assert check(candidate, "provenance-and-baseline-integrity") is False


def test_phase5_gate_rejects_security_audit_source_write(candidate: Path) -> None:
    skill_id = "security-audit-and-threat-modeling"; path = candidate / f"evals/candidates/capability-compiler-v2/phase-5/skills/{skill_id}/contract.json"
    value = load(path); value["execution"]["model_tools"] = ["read", "edit", "write"]; value["execution"]["mutation_scope"] = "authorized-workspace"; write(path, value); refresh_hashes(candidate, skill_id)
    assert check(candidate, "permission-source-audit-separation") is False


def test_phase5_gate_rejects_security_audit_remote_or_provider_scope(candidate: Path) -> None:
    skill_id = "security-audit-and-threat-modeling"; path = candidate / f"evals/candidates/capability-compiler-v2/phase-5/skills/{skill_id}/contract.json"
    value = load(path); value["execution"]["host_actions"] = ["approved-local-commands", "approved-provider-read"]; value["execution"]["external"] = "read-only"; write(path, value); refresh_hashes(candidate, skill_id)
    assert check(candidate, "permission-source-audit-separation") is False


def test_phase5_gate_rejects_ci_hardening_without_source_scope(candidate: Path) -> None:
    skill_id = "ci-pipeline-security-hardening"; path = candidate / f"evals/candidates/capability-compiler-v2/phase-5/skills/{skill_id}/contract.json"
    value = load(path); value["execution"]["mutation_scope"] = "run-output"; write(path, value); refresh_hashes(candidate, skill_id)
    assert check(candidate, "permission-source-audit-separation") is False


def test_phase5_gate_rejects_secret_value_prohibition_removal(candidate: Path) -> None:
    skill_id = "secrets-and-environment-governance"; path = candidate / f"evals/candidates/capability-compiler-v2/phase-5/skills/{skill_id}/SKILL.md"
    path.write_text(path.read_text(encoding="utf-8").replace("Never access or emit secret values", "Do not normally expose secrets"), encoding="utf-8", newline="\n"); refresh_hashes(candidate, skill_id)
    assert check(candidate, "architecture-security-and-secret-invariants") is False


def test_phase5_gate_rejects_default_deny_coverage_removal(candidate: Path) -> None:
    skill_id = "authorization-and-permission-contracts"; path = candidate / f"evals/candidates/capability-compiler-v2/phase-5/skills/{skill_id}/contract.json"
    value = load(path); value["policy"]["coverage"].remove("default-deny"); write(path, value); refresh_hashes(candidate, skill_id)
    assert check(candidate, "architecture-security-and-secret-invariants") is False


def test_phase5_gate_rejects_holdout_leakage(candidate: Path) -> None:
    authored = load(candidate / "evals/candidates/capability-compiler-v2/phase-5/skills/ai-agent-autonomy-and-human-control/trigger-cases.json")["cases"][0]["id"]
    path = candidate / "evals/candidates/capability-compiler-v2/phase-5/holdout-cases.json"; value = load(path); value["cases"][0]["id"] = authored; write(path, value)
    assert check(candidate, "trigger-and-holdout-boundaries") is False


def test_phase5_gate_rejects_false_evaluation_claim(candidate: Path) -> None:
    path = candidate / "evals/candidates/capability-compiler-v2/phase-5/skills/ai-safety-and-action-governance/evaluation-plan.json"
    value = load(path); value["execution_state"] = "passed"; write(path, value)
    assert check(candidate, "evaluation-plans-and-semantic-mutations") is False


def test_phase5_gate_rejects_missing_semantic_marker(candidate: Path) -> None:
    skill_id = "data-and-api-contract-design"; directory = candidate / f"evals/candidates/capability-compiler-v2/phase-5/skills/{skill_id}"
    evaluation = load(directory / "evaluation-plan.json"); marker = evaluation["mutations"][0]["remove_exact_text"]
    skill = directory / "SKILL.md"; skill.write_text(skill.read_text(encoding="utf-8").replace(marker, ""), encoding="utf-8", newline="\n"); refresh_hashes(candidate, skill_id)
    assert check(candidate, "candidate-schemas-semantic-design-and-hashes") is False
    assert check(candidate, "evaluation-plans-and-semantic-mutations") is False


def test_phase5_gate_rejects_open_semantic_finding(candidate: Path) -> None:
    path = candidate / "curation/v2/phase-5/semantic-review.json"; value = load(path); value["open_findings"] = [{"id": "open"}]; write(path, value)
    assert check(candidate, "semantic-boundary-review") is False
