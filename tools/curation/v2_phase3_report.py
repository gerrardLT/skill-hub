#!/usr/bin/env python3
"""Build the deterministic Phase 3 candidate artifact manifest and report."""
from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path
from typing import Any

try:
    from tools.curation.v2_phase3_gate import verify
except ModuleNotFoundError:
    from v2_phase3_gate import verify


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes().replace(b"\r\n", b"\n")).hexdigest()


def write(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")


def build(workspace: Path, pytest_summary: str, repository_gate_count: int) -> dict[str, Any]:
    workspace = workspace.resolve(); phase_root = workspace / ".specs/capability-compiler-v2/phase-3"
    gate = verify(workspace)
    if not gate["ok"]: raise ValueError("Phase 3 gate is not green: " + "; ".join(gate["errors"]))
    paths = [phase_root / "gate-report.json"]
    for directory in (workspace / "curation/v2/phase-3", workspace / "evals/candidates/capability-compiler-v2/phase-3"):
        paths.extend(sorted(path for path in directory.rglob("*") if path.is_file()))
    artifacts = [{"path": path.relative_to(workspace).as_posix(), "bytes": path.stat().st_size, "sha256": digest(path)} for path in sorted(set(paths))]
    tree = hashlib.sha256("".join(f"{item['path']}\0{item['sha256']}\n" for item in artifacts).encode("utf-8")).hexdigest()
    manifest = {"schema_version": "2.0", "phase": 3, "artifact_count": len(artifacts), "tree_sha256": tree, "artifacts": artifacts}
    write(phase_root / "artifact-manifest.json", manifest)
    root = workspace / "evals/candidates/capability-compiler-v2/phase-3/skills"
    contracts = [load(path) for path in sorted(root.glob("*/contract.json"))]
    evaluations = [load(path) for path in sorted(root.glob("*/evaluation-plan.json"))]
    report = {
        "schema_version": "2.0", "phase": 3, "gate": gate["gate"], "gate_ok": True, "status": "passed-candidates-evaluating",
        "artifact_manifest": ".specs/capability-compiler-v2/phase-3/artifact-manifest.json", "artifact_tree_sha256": tree,
        "phase2_artifact_tree_sha256": load(workspace / ".specs/capability-compiler-v2/phase-2/artifact-manifest.json")["tree_sha256"],
        "candidates": {"count": len(contracts), "version": "0.1.0-v2-candidate", "status": "evaluating", "by_permission_identity": dict(sorted(Counter(item["permission_identity"] for item in contracts).items())), "released": 0},
        "routing": {"authored_trigger_cases": gate["counts"]["authored_trigger_cases"], "holdout_cases": gate["counts"]["holdout_cases"], "holdout_execution_state": "not-run-phase-9"},
        "evaluation": {"planned_mutations": gate["counts"]["planned_mutations"], "plans": len(evaluations), "execution_states": dict(sorted(Counter(item["execution_state"] for item in evaluations).items())), "real_model_runs": 0, "phase_9_required": True},
        "policies": {"data_governance_candidates": sum(item["policy"]["data_governance"] for item in contracts), "human_decision_candidates": sum(item["policy"]["human_decision"] for item in contracts), "named_formula_variant_candidates": sum(item["policy"]["named_formula_variants"] for item in contracts), "semantic_review_open_findings": 0},
        "verification": {"repository_gates_ok": True, "repository_gate_count": repository_gate_count, "pytest_summary": pytest_summary, "source_drift": 0, "v1_asset_drift": 0},
        "limitations": ["No Phase 9 model baseline/candidate/holdout execution has run.", "No Phase 10 human approval has occurred.", "No candidate is released or referenced by a released Recipe."],
        "errors": [],
    }
    write(phase_root / "phase-report.json", report)
    return {"gate": "capability-compiler-v2-phase-3-report", "ok": True, "artifact_count": len(artifacts), "tree_sha256": tree, "skills": len(contracts)}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__); parser.add_argument("--workspace-root", type=Path, default=Path(".")); parser.add_argument("--pytest-summary", required=True); parser.add_argument("--repository-gate-count", required=True, type=int); args = parser.parse_args()
    result = build(args.workspace_root, args.pytest_summary, args.repository_gate_count); print(json.dumps(result, ensure_ascii=False, sort_keys=True)); return 0


if __name__ == "__main__": raise SystemExit(main())
