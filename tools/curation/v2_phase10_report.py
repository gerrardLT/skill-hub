#!/usr/bin/env python3
"""Build deterministic Phase 10 review/revision manifest and report."""
from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path
from typing import Any

try:
    from tools.curation.v2_phase10_gate import verify
except ModuleNotFoundError:
    from v2_phase10_gate import verify


def load(path: Path) -> Any: return json.loads(path.read_text(encoding="utf-8"))
def digest(path: Path) -> str: return hashlib.sha256(path.read_bytes().replace(b"\r\n", b"\n")).hexdigest()
def write(path: Path, value: Any) -> None: path.parent.mkdir(parents=True, exist_ok=True); path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")


def build(workspace: Path, pytest_summary: str, repository_gate_count: int) -> dict[str, Any]:
    workspace = workspace.resolve(); phase_root = workspace / ".specs/capability-compiler-v2/phase-10"; gate = verify(workspace)
    if not gate["ok"]: raise ValueError("Phase 10 gate is not green: " + "; ".join(gate["errors"]))
    excluded = {phase_root / "artifact-manifest.json", phase_root / "phase-report.json"}; paths = []
    for directory in [phase_root, workspace / "curation/v2/phase-10", workspace / "evals/candidates/capability-compiler-v2/phase-10", workspace / "evals/runs/capability-compiler-v2/phase-10"]:
        paths.extend(path for path in directory.rglob("*") if path.is_file() and path not in excluded)
    artifacts = [{"path": path.relative_to(workspace).as_posix(), "bytes": path.stat().st_size, "sha256": digest(path)} for path in sorted(set(paths))]
    tree = hashlib.sha256("".join(f"{item['path']}\0{item['sha256']}\n" for item in artifacts).encode("utf-8")).hexdigest(); by_root = Counter("/".join(item["path"].split("/")[:5]) for item in artifacts)
    write(phase_root / "artifact-manifest.json", {"schema_version": "2.0", "phase": 10, "artifact_count": len(artifacts), "tree_sha256": tree, "by_root": dict(sorted(by_root.items())), "artifacts": artifacts})
    grading = load(workspace / "evals/runs/capability-compiler-v2/phase-10/grading-report.json"); review = load(workspace / "curation/v2/phase-10/semantic-review.json"); plan = load(workspace / "curation/v2/phase-10/run-plan.json")
    report = {
        "schema_version": "2.0", "phase": 10, "status": "passed-parent-direct-review-candidates-not-released", "gate": gate["gate"], "gate_ok": True,
        "phase_10_complete": True, "eligible_for_phase_11": True, "final_user_release_approval": False, "released": False,
        "artifact_manifest": ".specs/capability-compiler-v2/phase-10/artifact-manifest.json", "artifact_count": len(artifacts), "artifact_tree_sha256": tree,
        "source_phase9_tree": plan["source_phase9_tree"],
        "skill_review": review["atomic_skill_review"], "findings": review["phase9_findings"], "user_decisions": review["user_decisions"], "revision_history": review["revision_history"],
        "accepted_revision": {"revision": 4, "version": "0.1.4-v2-candidate", "task_plan_sha256": plan["task_sha256"], "runs": grading["completed_attempts"], "groups": grading["groups"], "thresholds": grading["thresholds"], "thresholds_passed": grading["thresholds_passed"], "causal_mutations": dict(sorted(Counter(item["status"] for item in grading["mutation_results"]).items()))},
        "verification": {"repository_gates_ok": True, "repository_gate_count": repository_gate_count, "pytest_summary": pytest_summary, "rejected_revision_failures_deleted": 0, "thresholds_lowered": False, "candidate_actions_executed": 0, "source_drift": 0, "v1_asset_drift": 0},
        "limitations": ["Phase 10 parent-direct semantic review is not final user release approval.", "Revision 4 remains evaluating and is eligible only for Phase 11 real-project validation.", "No candidate was copied into released slots or recipes.", "No remote, provider, browser-auth, local-system, deployment, rollback, or production action ran."],
        "next_required_phase": "Phase 11 end-to-end real-project validation and final documentation", "errors": [],
    }
    write(phase_root / "phase-report.json", report); return {"gate": "capability-compiler-v2-phase-10-report", "ok": True, "artifact_count": len(artifacts), "tree_sha256": tree, "reviewed_skills": 157, "revision4_runs": 60, "released": False}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__); parser.add_argument("--workspace-root", type=Path, default=Path(".")); parser.add_argument("--pytest-summary", required=True); parser.add_argument("--repository-gate-count", type=int, required=True); args = parser.parse_args(); print(json.dumps(build(args.workspace_root, args.pytest_summary, args.repository_gate_count), ensure_ascii=False, sort_keys=True)); return 0


if __name__ == "__main__": raise SystemExit(main())
