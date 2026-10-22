#!/usr/bin/env python3
"""Build deterministic Phase 8 Recipe/router artifact manifest and report."""
from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path
from typing import Any

try:
    from tools.curation.v2_phase8_gate import verify
except ModuleNotFoundError:
    from v2_phase8_gate import verify


def load(path: Path) -> Any: return json.loads(path.read_text(encoding="utf-8"))
def digest(path: Path) -> str: return hashlib.sha256(path.read_bytes().replace(b"\r\n", b"\n")).hexdigest()
def write(path: Path, value: Any) -> None: path.parent.mkdir(parents=True, exist_ok=True); path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")


def build(workspace: Path, pytest_summary: str, repository_gate_count: int) -> dict[str, Any]:
    workspace = workspace.resolve(); phase_root = workspace / ".specs/capability-compiler-v2/phase-8"; gate = verify(workspace)
    if not gate["ok"]: raise ValueError("Phase 8 gate is not green: " + "; ".join(gate["errors"]))
    paths = [phase_root / "gate-report.json"]
    for directory in (workspace / "curation/v2/phase-8", workspace / "evals/candidates/capability-compiler-v2/phase-8"):
        paths.extend(sorted(path for path in directory.rglob("*") if path.is_file()))
    artifacts = [{"path": path.relative_to(workspace).as_posix(), "bytes": path.stat().st_size, "sha256": digest(path)} for path in sorted(set(paths))]
    tree = hashlib.sha256("".join(f"{item['path']}\0{item['sha256']}\n" for item in artifacts).encode("utf-8")).hexdigest()
    write(phase_root / "artifact-manifest.json", {"schema_version": "2.0", "phase": 8, "artifact_count": len(artifacts), "tree_sha256": tree, "artifacts": artifacts})
    root = workspace / "evals/candidates/capability-compiler-v2/phase-8"; stages = [load(path) for path in sorted((root / "recipes/stages").glob("*.json"))]; composites = [load(path) for path in sorted((root / "recipes/composites").glob("*.json"))]; evaluation = load(root / "evaluation-plan.json")
    report = {
        "schema_version": "2.0",
        "phase": 8,
        "gate": gate["gate"],
        "gate_ok": True,
        "status": "passed-candidates-evaluating",
        "artifact_manifest": ".specs/capability-compiler-v2/phase-8/artifact-manifest.json",
        "artifact_tree_sha256": tree,
        "prior_artifact_trees": {f"phase{phase}": load(workspace / f".specs/capability-compiler-v2/phase-{phase}/artifact-manifest.json")["tree_sha256"] for phase in range(2, 8)},
        "composition": {
            "candidate_skills_covered": gate["counts"]["candidate_skills"],
            "stage_recipes": len(stages),
            "composite_recipes": len(composites),
            "specialized_recipes_referenced": gate["counts"]["specialized_recipes"],
            "router_count": 1,
            "mandatory_handoffs": gate["counts"]["mandatory_handoffs"],
            "dependencies_projected": gate["counts"]["dependencies"],
            "protected_action_steps": gate["counts"]["protected_action_steps"],
            "version": "0.1.0-v2-candidate",
            "status": "evaluating",
            "released": 0,
            "execution_states": dict(sorted(Counter(item["execution_state"] for item in stages + composites + [load(root / "router.json")]).items())),
        },
        "routing": {
            "selection_policy": "smallest-sufficient-fail-closed",
            "router_authored_cases": gate["counts"]["router_authored_cases"],
            "router_holdout_cases": gate["counts"]["router_holdout_cases"],
            "recipe_authored_cases": gate["counts"]["recipe_authored_cases"],
            "recipe_holdout_cases": gate["counts"]["recipe_holdout_cases"],
            "ambiguous_fallback": "stage-01-governance-intake",
            "full_lifecycle_explicit_only": True,
        },
        "evaluation": {
            "status": evaluation["status"],
            "execution_state": evaluation["execution_state"],
            "planned_mutations": gate["counts"]["planned_mutations"],
            "real_model_runs": 0,
            "phase_9_required": True,
        },
        "actions": {
            "remote_actions_executed": 0,
            "provider_actions_executed": 0,
            "browser_auth_or_pairing_actions_executed": 0,
            "local_system_actions_executed": 0,
            "production_actions_executed": 0,
        },
        "verification": {
            "repository_gates_ok": True,
            "repository_gate_count": repository_gate_count,
            "pytest_summary": pytest_summary,
            "source_drift": 0,
            "v1_asset_drift": 0,
            "semantic_review_open_findings": 0,
        },
        "limitations": [
            "Phase 8 compiles declarative candidate Recipes and a router; it does not execute them.",
            "No Phase 9 model baseline, candidate, holdout, or mutation evaluation has run.",
            "No Phase 10 human approval has occurred.",
            "No push, pull-request action, merge, deploy, provider configuration, publication, rollback, browser authentication, external-session mutation, local-system mutation, or production change ran.",
            "No Phase 8 candidate Recipe or router is released or referenced by the released catalog.",
        ],
        "errors": [],
    }
    write(phase_root / "phase-report.json", report)
    return {"gate": "capability-compiler-v2-phase-8-report", "ok": True, "artifact_count": len(artifacts), "tree_sha256": tree, "stage_recipes": len(stages), "composite_recipes": len(composites)}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__); parser.add_argument("--workspace-root", type=Path, default=Path(".")); parser.add_argument("--pytest-summary", required=True); parser.add_argument("--repository-gate-count", type=int, required=True); args = parser.parse_args(); print(json.dumps(build(args.workspace_root, args.pytest_summary, args.repository_gate_count), ensure_ascii=False, sort_keys=True)); return 0


if __name__ == "__main__": raise SystemExit(main())
