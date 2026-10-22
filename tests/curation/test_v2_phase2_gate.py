import hashlib
import json
import shutil
from pathlib import Path

import pytest

import tools.curation.v2_phase2_gate as gate

ROOT = Path(__file__).resolve().parents[2]


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def write(path: Path, value) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")


@pytest.fixture()
def candidate(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    for relative in [
        "curation/clusters.json",
        "curation/v2/capability.schema.json",
        "curation/v2/lifecycle",
        "curation/v2/capabilities",
        "curation/v2/fusion",
        "curation/v2/units/auxiliary.json",
        "curation/v2/units/root-derived.json",
        "skills/gstack/review/greptile-triage.md",
        "skills/gstack/ship/sections/pr-body.md",
        "skills/gstack/land-and-deploy/sections/merge-and-deploy.md",
    ]:
        source = ROOT / relative; target = tmp_path / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copytree(source, target) if source.is_dir() else shutil.copy2(source, target)
    monkeypatch.setattr(gate, "verify_phase1", lambda _: {"ok": True, "errors": []})
    return tmp_path


def check(candidate: Path, name: str) -> bool:
    result = gate.verify(candidate)
    return next(item["ok"] for item in result["checks"] if item["name"] == name)


def test_phase2_artifact_manifest_recomputes_exactly() -> None:
    path = ROOT / ".specs/capability-compiler-v2/phase-2/artifact-manifest.json"; manifest = load(path)
    assert path.relative_to(ROOT).as_posix() not in {item["path"] for item in manifest["artifacts"]}
    assert ".specs/capability-compiler-v2/phase-2/phase-report.json" not in {item["path"] for item in manifest["artifacts"]}
    records = []
    for item in manifest["artifacts"]:
        artifact = ROOT / item["path"]; data = artifact.read_bytes().replace(b"\r\n", b"\n")
        assert artifact.stat().st_size == item["bytes"]
        assert hashlib.sha256(data).hexdigest() == item["sha256"]
        records.append(f"{item['path']}\0{item['sha256']}\n")
    assert len(records) == manifest["artifact_count"] == 169
    assert hashlib.sha256("".join(records).encode("utf-8")).hexdigest() == manifest["tree_sha256"]


def test_phase2_gate_accepts_complete_candidate(candidate: Path) -> None:
    result = gate.verify(candidate)
    assert result["ok"] is True, result["errors"]
    assert result["counts"] == {
        "domains": 11,
        "stages": 15,
        "capabilities": 157,
        "legacy_clusters": 88,
        "canonical_units": 965,
        "retained_auxiliary_units": 104,
        "root_atoms": 1138,
        "fusion_decisions": 1244,
    }


def test_phase2_gate_rejects_missing_atom_decision(candidate: Path) -> None:
    path = candidate / "curation/v2/lifecycle/root-atom-map.json"; value = load(path)
    value["records"].pop(); write(path, value)
    assert check(candidate, "root-derived-atom-decisions") is False


def test_phase2_gate_rejects_duplicate_unit_owner(candidate: Path) -> None:
    paths = sorted((candidate / "curation/v2/capabilities").glob("*.json")); paths = [path for path in paths if path.name != "catalog.json"]
    owner = next(path for path in paths if load(path)["canonical_unit_ids"])
    unit_id = load(owner)["canonical_unit_ids"][0]
    other = next(path for path in paths if path != owner)
    value = load(other); value["canonical_unit_ids"].append(unit_id); write(other, value)
    assert check(candidate, "cluster-canonical-auxiliary-ownership") is False


def test_phase2_gate_rejects_review_write_identity(candidate: Path) -> None:
    path = candidate / "curation/v2/capabilities/independent-blackbox-qa.json"; value = load(path)
    value["permission_identity"] = "workspace-write-local-exec"; write(path, value)
    assert check(candidate, "permission-separation") is False


def test_phase2_gate_rejects_mutation_atom_in_read_only_review(candidate: Path) -> None:
    atom_id = "v2-root:gstack/review:021:step-5b-auto-fix-all-auto-fix-items"
    repair_path = candidate / "curation/v2/capabilities/defect-remediation.json"; repair = load(repair_path)
    repair["root_derived_atom_ids"].remove(atom_id); write(repair_path, repair)
    review_path = candidate / "curation/v2/capabilities/independent-code-review.json"; review = load(review_path)
    review["root_derived_atom_ids"].append(atom_id); write(review_path, review)
    assert check(candidate, "permission-separation") is False


def test_phase2_gate_rejects_missing_provenance(candidate: Path) -> None:
    path = candidate / "curation/v2/capabilities/tdd-change-loop.json"; value = load(path)
    value["source_evidence"] = []; write(path, value)
    assert check(candidate, "capability-contracts-and-coverage") is False


def test_phase2_gate_rejects_invalid_source_fragment(candidate: Path) -> None:
    path = candidate / "curation/v2/capabilities/remote-pull-request-merge.json"; value = load(path)
    value["source_fragment_ids"] = ["gstack/land-and-deploy/sections/merge-and-deploy.md:1-99999"]
    value["source_evidence"] = value["source_fragment_ids"]
    write(path, value)
    assert check(candidate, "capability-contracts-and-coverage") is False


def test_phase2_gate_rejects_hard_dependency_cycle(candidate: Path) -> None:
    path = candidate / "curation/v2/lifecycle/dependencies.json"; value = load(path)
    edge = value["hard_dag_edges"][0]
    value["hard_dag_edges"].append({
        "source_capability_id": edge["target_capability_id"],
        "target_capability_id": edge["source_capability_id"],
        "decision_id": "mutation-cycle",
    }); write(path, value)
    assert check(candidate, "dependency-dag-handoffs-and-phase-ownership") is False


def test_phase2_gate_rejects_dependency_island(candidate: Path) -> None:
    path = candidate / "curation/v2/lifecycle/dependencies.json"; value = load(path)
    capability_id = "capability:website-audit-remediation"
    value["records"] = [edge for edge in value["records"] if capability_id not in {edge["source_capability_id"], edge["target_capability_id"]}]
    value["hard_dag_edges"] = [edge for edge in value["hard_dag_edges"] if capability_id not in {edge["source_capability_id"], edge["target_capability_id"]}]
    write(path, value)
    assert check(candidate, "dependency-dag-handoffs-and-phase-ownership") is False


def test_phase2_gate_rejects_missing_human_decision_policy(candidate: Path) -> None:
    path = candidate / "curation/v2/capabilities/problem-framing-and-customer-research.json"; value = load(path)
    value["decision_references"].remove("V2-DEC-003"); write(path, value)
    assert check(candidate, "fusion-policy-application") is False
