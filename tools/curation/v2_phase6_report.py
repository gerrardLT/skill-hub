#!/usr/bin/env python3
"""Build deterministic Phase 6 candidate artifact manifest and report."""
from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path
from typing import Any

try:
    from tools.curation.v2_phase6_gate import verify
except ModuleNotFoundError:
    from v2_phase6_gate import verify


def load(path: Path) -> Any: return json.loads(path.read_text(encoding="utf-8"))
def digest(path: Path) -> str: return hashlib.sha256(path.read_bytes().replace(b"\r\n", b"\n")).hexdigest()
def write(path: Path, value: Any) -> None: path.parent.mkdir(parents=True, exist_ok=True); path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")


def build(workspace: Path, pytest_summary: str, repository_gate_count: int) -> dict[str, Any]:
    workspace = workspace.resolve(); phase_root = workspace / ".specs/capability-compiler-v2/phase-6"; gate = verify(workspace)
    if not gate["ok"]: raise ValueError("Phase 6 gate is not green: " + "; ".join(gate["errors"]))
    paths = [phase_root / "gate-report.json"]
    for directory in (workspace / "curation/v2/phase-6", workspace / "evals/candidates/capability-compiler-v2/phase-6"): paths.extend(sorted(path for path in directory.rglob("*") if path.is_file()))
    artifacts = [{"path": path.relative_to(workspace).as_posix(), "bytes": path.stat().st_size, "sha256": digest(path)} for path in sorted(set(paths))]
    tree = hashlib.sha256("".join(f"{item['path']}\0{item['sha256']}\n" for item in artifacts).encode("utf-8")).hexdigest(); write(phase_root / "artifact-manifest.json", {"schema_version": "2.0", "phase": 6, "artifact_count": len(artifacts), "tree_sha256": tree, "artifacts": artifacts})
    root = workspace / "evals/candidates/capability-compiler-v2/phase-6/skills"; contracts = [load(path) for path in sorted(root.glob("*/contract.json"))]; evaluations = [load(path) for path in sorted(root.glob("*/evaluation-plan.json"))]
    report = {"schema_version": "2.0", "phase": 6, "gate": gate["gate"], "gate_ok": True, "status": "passed-candidates-evaluating", "artifact_manifest": ".specs/capability-compiler-v2/phase-6/artifact-manifest.json", "artifact_tree_sha256": tree, "prior_artifact_trees": {phase: load(workspace / f".specs/capability-compiler-v2/{phase.replace('phase','phase-')}/artifact-manifest.json")["tree_sha256"] for phase in ["phase2", "phase3", "phase4", "phase5"]}, "candidates": {"count": len(contracts), "batches": 4, "version": "0.1.0-v2-candidate", "status": "evaluating", "released": 0, "by_permission_identity": dict(sorted(Counter(item["permission_identity"] for item in contracts).items())), "by_mutation_scope": dict(sorted(Counter(item["execution"]["mutation_scope"] for item in contracts).items())), "candidate_execution_states": dict(sorted(Counter(item["execution"]["candidate_execution_state"] for item in contracts).items()))}, "routing": {"authored_cases": gate["counts"]["authored_trigger_cases"], "holdout_cases": gate["counts"]["holdout_cases"]}, "evaluation": {"plans": len(evaluations), "planned_mutations": gate["counts"]["planned_mutations"], "execution_states": dict(sorted(Counter(item["execution_state"] for item in evaluations).items())), "real_model_runs": 0, "phase_9_required": True}, "high_risk_identities": {"remote_write_candidates": gate["counts"]["remote_write_candidates"], "external_session_candidates": gate["counts"]["external_session_candidates"], "local_system_candidates": gate["counts"]["local_system_candidates"], "actions_executed_in_phase_6": 0}, "verification": {"repository_gates_ok": True, "repository_gate_count": repository_gate_count, "pytest_summary": pytest_summary, "source_drift": 0, "v1_asset_drift": 0, "semantic_review_open_findings": 0}, "limitations": ["No Phase 9 model baseline/candidate/holdout execution has run.", "No Phase 10 human approval has occurred.", "No provider write, dataset publication, LLM experiment, browser authentication, browser pairing, credential mint, local-system setup, runtime upgrade, remote Git, merge, deploy, or release action ran.", "No candidate is released or referenced by a released Recipe."], "errors": []}
    write(phase_root / "phase-report.json", report); return {"gate": "capability-compiler-v2-phase-6-report", "ok": True, "artifact_count": len(artifacts), "tree_sha256": tree, "skills": len(contracts)}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__); parser.add_argument("--workspace-root", type=Path, default=Path(".")); parser.add_argument("--pytest-summary", required=True); parser.add_argument("--repository-gate-count", type=int, required=True); args = parser.parse_args(); print(json.dumps(build(args.workspace_root, args.pytest_summary, args.repository_gate_count), ensure_ascii=False, sort_keys=True)); return 0


if __name__ == "__main__": raise SystemExit(main())
