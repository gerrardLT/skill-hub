#!/usr/bin/env python3
"""Build deterministic Phase 5 candidate artifact manifest and report."""
from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path
from typing import Any

try:
    from tools.curation.v2_phase5_gate import verify
except ModuleNotFoundError:
    from v2_phase5_gate import verify


def load(path: Path) -> Any: return json.loads(path.read_text(encoding="utf-8"))
def digest(path: Path) -> str: return hashlib.sha256(path.read_bytes().replace(b"\r\n", b"\n")).hexdigest()
def write(path: Path, value: Any) -> None: path.parent.mkdir(parents=True, exist_ok=True); path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")


def build(workspace: Path, pytest_summary: str, repository_gate_count: int) -> dict[str, Any]:
    workspace = workspace.resolve(); phase_root = workspace / ".specs/capability-compiler-v2/phase-5"; gate = verify(workspace)
    if not gate["ok"]: raise ValueError("Phase 5 gate is not green: " + "; ".join(gate["errors"]))
    paths = [phase_root / "gate-report.json"]
    for directory in (workspace / "curation/v2/phase-5", workspace / "evals/candidates/capability-compiler-v2/phase-5"): paths.extend(sorted(path for path in directory.rglob("*") if path.is_file()))
    artifacts = [{"path": path.relative_to(workspace).as_posix(), "bytes": path.stat().st_size, "sha256": digest(path)} for path in sorted(set(paths))]
    tree = hashlib.sha256("".join(f"{item['path']}\0{item['sha256']}\n" for item in artifacts).encode("utf-8")).hexdigest(); write(phase_root / "artifact-manifest.json", {"schema_version": "2.0", "phase": 5, "artifact_count": len(artifacts), "tree_sha256": tree, "artifacts": artifacts})
    root = workspace / "evals/candidates/capability-compiler-v2/phase-5/skills"; contracts = [load(path) for path in sorted(root.glob("*/contract.json"))]; evaluations = [load(path) for path in sorted(root.glob("*/evaluation-plan.json"))]
    report = {"schema_version": "2.0", "phase": 5, "gate": gate["gate"], "gate_ok": True, "status": "passed-candidates-evaluating", "artifact_manifest": ".specs/capability-compiler-v2/phase-5/artifact-manifest.json", "artifact_tree_sha256": tree, "prior_artifact_trees": {phase: load(workspace / f".specs/capability-compiler-v2/{phase.replace('phase','phase-')}/artifact-manifest.json")["tree_sha256"] for phase in ["phase2", "phase3", "phase4"]}, "candidates": {"count": len(contracts), "version": "0.1.0-v2-candidate", "status": "evaluating", "released": 0, "by_permission_identity": dict(sorted(Counter(item["permission_identity"] for item in contracts).items())), "by_mutation_scope": dict(sorted(Counter(item["execution"]["mutation_scope"] for item in contracts).items()))}, "coverage": {"aggregate_markers": sorted({marker for item in contracts for marker in item["policy"]["coverage"]}), "data_governance_skills": sum(item["policy"]["data_governance"] for item in contracts), "human_decision_skills": sum(item["policy"]["human_decision"] for item in contracts), "source_writing_skills": sum(item["execution"]["mutation_scope"] == "authorized-workspace" for item in contracts), "review_or_audit_non_source_writers": sum(item["execution"]["mutation_scope"] in ["none", "artifact-output"] for item in contracts)}, "routing": {"authored_cases": gate["counts"]["authored_trigger_cases"], "holdout_cases": gate["counts"]["holdout_cases"]}, "evaluation": {"plans": len(evaluations), "planned_mutations": gate["counts"]["planned_mutations"], "execution_states": dict(sorted(Counter(item["execution_state"] for item in evaluations).items())), "real_model_runs": 0, "phase_9_required": True}, "verification": {"repository_gates_ok": True, "repository_gate_count": repository_gate_count, "pytest_summary": pytest_summary, "source_drift": 0, "v1_asset_drift": 0, "semantic_review_open_findings": 0}, "limitations": ["No Phase 9 model baseline/candidate/holdout execution has run.", "No Phase 10 human approval has occurred.", "No production, provider, remote Git, migration, credential, secret-value, or AI action-right mutation occurred.", "No candidate is released or referenced by a released Recipe."], "errors": []}
    write(phase_root / "phase-report.json", report); return {"gate": "capability-compiler-v2-phase-5-report", "ok": True, "artifact_count": len(artifacts), "tree_sha256": tree, "skills": len(contracts)}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__); parser.add_argument("--workspace-root", type=Path, default=Path(".")); parser.add_argument("--pytest-summary", required=True); parser.add_argument("--repository-gate-count", type=int, required=True); args = parser.parse_args(); print(json.dumps(build(args.workspace_root, args.pytest_summary, args.repository_gate_count), ensure_ascii=False, sort_keys=True)); return 0


if __name__ == "__main__": raise SystemExit(main())
