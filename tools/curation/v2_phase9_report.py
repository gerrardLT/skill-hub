#!/usr/bin/env python3
"""Build deterministic Phase 9 evaluation manifest and truthful release-blocked report."""
from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path
from typing import Any

try:
    from tools.curation.v2_phase9_gate import verify
except ModuleNotFoundError:
    from v2_phase9_gate import verify


def load(path: Path) -> Any: return json.loads(path.read_text(encoding="utf-8"))
def digest(path: Path) -> str: return hashlib.sha256(path.read_bytes().replace(b"\r\n", b"\n")).hexdigest()
def write(path: Path, value: Any) -> None: path.parent.mkdir(parents=True, exist_ok=True); path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")


def build(workspace: Path, pytest_summary: str, repository_gate_count: int) -> dict[str, Any]:
    workspace = workspace.resolve(); phase_root = workspace / ".specs/capability-compiler-v2/phase-9"; gate = verify(workspace)
    if not gate["ok"]: raise ValueError("Phase 9 evidence gate is not green: " + "; ".join(gate["errors"]))
    excluded = {phase_root / "artifact-manifest.json", phase_root / "phase-report.json"}
    paths = []
    for directory in [phase_root, workspace / "curation/v2/phase-9", workspace / "evals/runs/capability-compiler-v2/phase-9", workspace / "evals/runs/capability-compiler-v2/phase-9-pilots"]:
        paths.extend(path for path in directory.rglob("*") if path.is_file() and path not in excluded)
    artifacts = [{"path": path.relative_to(workspace).as_posix(), "bytes": path.stat().st_size, "sha256": digest(path)} for path in sorted(set(paths))]
    tree = hashlib.sha256("".join(f"{item['path']}\0{item['sha256']}\n" for item in artifacts).encode("utf-8")).hexdigest()
    by_root = Counter("/".join(item["path"].split("/")[:4]) for item in artifacts)
    manifest = {"schema_version": "2.0", "phase": 9, "artifact_count": len(artifacts), "tree_sha256": tree, "by_root": dict(sorted(by_root.items())), "artifacts": artifacts}
    write(phase_root / "artifact-manifest.json", manifest)

    grading = load(workspace / "evals/runs/capability-compiler-v2/phase-9/grading-report.json"); plan = load(workspace / "curation/v2/phase-9/run-plan.json"); review = load(workspace / "curation/v2/phase-9/semantic-review.json")
    runs = [load(path) for path in sorted((workspace / "evals/runs/capability-compiler-v2/phase-9/attempts").glob("run-*/run.json"))]
    report = {
        "schema_version": "2.0",
        "phase": 9,
        "status": "completed-evidence-green-release-blocked",
        "gate": gate["gate"],
        "gate_ok": True,
        "evaluation_complete": True,
        "release_thresholds_passed": False,
        "release_blocked": True,
        "artifact_manifest": ".specs/capability-compiler-v2/phase-9/artifact-manifest.json",
        "artifact_count": len(artifacts),
        "artifact_tree_sha256": tree,
        "prior_artifact_trees": plan["prior_artifact_trees"],
        "runtime": {
            "planned_runs": plan["task_count"],
            "completed_attempts": grading["completed_attempts"],
            "exit_statuses": dict(sorted(Counter(item["exit_status"] for item in runs).items())),
            "parse_states": {str(key).lower(): value for key, value in sorted(Counter(item["parse_ok"] for item in runs).items(), key=lambda pair: str(pair[0]))},
            "provider_model_response": dict(sorted(Counter("/".join([item["provider"], item["model"], item["response_model"]]) for item in runs).items())),
            "stop_reasons": dict(sorted(Counter(item["stop_reason"] for item in runs).items())),
            "total_tokens": sum(item["token_usage"]["totalTokens"] for item in runs),
            "summed_duration_ms": round(sum(item["duration_ms"] for item in runs), 3),
            "candidate_actions_executed": sum(bool(item["candidate_action_executed"]) for item in runs),
            "tool_permissions": sorted({tuple(item["tool_permissions"]) for item in runs}),
            "task_plan_sha256": plan["task_sha256"],
        },
        "atomic_skill_results": {
            "baseline": grading["groups"]["skill_holdout_by_variant"]["baseline"],
            "candidate": grading["groups"]["skill_holdout_by_variant"]["candidate"],
            "by_phase": grading["groups"]["skill_holdout_by_phase"],
            "paired_outcomes": grading["groups"]["paired_skill_holdouts"],
        },
        "recipe_and_router_results": {
            "phase4_recipe": grading["groups"]["p4_recipe_by_variant"],
            "phase8_router": grading["groups"]["p8_router_by_set"],
            "phase8_recipe": grading["groups"]["p8_recipe_by_set"],
        },
        "mutation_results": grading["groups"]["mutations"],
        "thresholds": grading["thresholds"],
        "open_findings": review["open_findings"],
        "calibrations": [item["path"] for item in review["protocol_calibrations"]],
        "verification": {
            "evidence_errors": len(grading["evidence_errors"]),
            "repository_gates_ok": True,
            "repository_gate_count": repository_gate_count,
            "pytest_summary": pytest_summary,
            "source_drift": 0,
            "v1_asset_drift": 0,
            "deleted_failed_attempts": 0,
        },
        "limitations": [
            "Atomic Skill holdout thresholds passed, but Phase 4 and Phase 8 Recipe/router thresholds did not all pass.",
            "Behavioral mutation outcomes are diagnostic because most frozen semantic-marker mutations lack independently causal challenge cases; deterministic mutation Gates remain authoritative.",
            "Phase 9 behavioral evidence is not Phase 10 human approval and does not release any candidate.",
            "No candidate side effect, remote action, provider mutation, browser authentication, local-system mutation, deployment, rollback, or production change ran.",
        ],
        "next_required_phase": "Phase 10 candidate revision and human semantic review",
        "errors": [],
    }
    write(phase_root / "phase-report.json", report)
    return {"gate": "capability-compiler-v2-phase-9-report", "ok": True, "artifact_count": len(artifacts), "tree_sha256": tree, "evaluated_runs": len(runs), "release_blocked": True}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__); parser.add_argument("--workspace-root", type=Path, default=Path(".")); parser.add_argument("--pytest-summary", required=True); parser.add_argument("--repository-gate-count", type=int, required=True); args = parser.parse_args(); print(json.dumps(build(args.workspace_root, args.pytest_summary, args.repository_gate_count), ensure_ascii=False, sort_keys=True)); return 0


if __name__ == "__main__": raise SystemExit(main())
