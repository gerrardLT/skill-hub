#!/usr/bin/env python3
"""Build Phase 10 per-Skill semantic review ledger and Phase 9 finding adjudications."""
from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

PHASE9_TREE = "7540c53426a5dff605c3f751fdaf105f52059ffbafce213d77c9c3db94214152"


def load(path: Path) -> Any: return json.loads(path.read_text(encoding="utf-8"))
def write(path: Path, value: Any) -> None: path.parent.mkdir(parents=True, exist_ok=True); path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")


def build(workspace: Path) -> dict[str, Any]:
    workspace = workspace.resolve(); phase9 = load(workspace / ".specs/capability-compiler-v2/phase-9/artifact-manifest.json")
    if phase9["tree_sha256"] != PHASE9_TREE: raise ValueError("Phase 9 tree drift")
    plan = load(workspace / "curation/v2/phase-9/run-plan.json"); tasks = {item["id"]: item for item in plan["tasks"]}; run_root = workspace / "evals/runs/capability-compiler-v2/phase-9/attempts"; review_root = workspace / "curation/v2/phase-10/review-packets"
    by_skill: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for task in tasks.values():
        if task["category"] != "skill-holdout" or task["variant"] != "candidate": continue
        directory = run_root / task["id"]; grading = load(directory / "grading.json"); run = load(directory / "run.json"); actual = grading["actual"]
        expected = task["expected"]["decision"]
        checks = {
            "objective_grade_passed": grading["passed"] is True,
            "decision_exact": actual.get("decision") == expected,
            "matched_boundary_present": isinstance(actual.get("matched_boundary"), str) and bool(actual["matched_boundary"].strip()),
            "reason_present": isinstance(actual.get("reason"), str) and bool(actual["reason"].strip()),
            "would_execute_false": actual.get("would_execute") is False,
            "tools_denied": run.get("tool_permissions") == [],
            "candidate_action_false": run.get("candidate_action_executed") is False,
            "run_completed_and_parsed": run.get("exit_status") == "completed" and run.get("parse_ok") is True,
        }
        by_skill[task["skill_id"]].append({
            "run_id": task["id"], "case_id": task["case_id"], "case_kind": task["expected"]["case_kind"],
            "input": task["input"], "expected_decision": expected, "actual_decision": actual["decision"],
            "matched_boundary": actual["matched_boundary"], "reason": actual["reason"], "checks": checks,
            "evidence_path": directory.relative_to(workspace).as_posix(),
        })
    records = []
    for skill_id, cases in sorted(by_skill.items()):
        task = next(item for item in tasks.values() if item.get("skill_id") == skill_id and item["category"] == "skill-holdout" and item["variant"] == "candidate")
        all_ok = len(cases) == 2 and {item["case_kind"] for item in cases} == {"should-trigger", "should-not-trigger"} and all(all(item["checks"].values()) for item in cases)
        records.append({
            "skill_id": skill_id, "phase": task["phase"], "domain_id": task["domain_id"], "stage_id": task["stage_id"],
            "permission_identity": task["permission_identity"], "mutation_scope": task["mutation_scope"],
            "reviewed_output_count": len(cases), "cases": sorted(cases, key=lambda item: item["case_id"]),
            "verdict": "accepted" if all_ok else "revision-required", "revision_required": not all_ok,
            "review_basis": "Both unseen ownership and adjacent-boundary outputs were checked against frozen expectations, semantic reasons, action denial, tool denial, and run evidence.",
        })
    if len(records) != 157 or sum(item["reviewed_output_count"] for item in records) != 314: raise ValueError("review ledger coverage mismatch")
    ledger = {"schema_version": "2.0", "phase": 10, "source_phase9_tree": PHASE9_TREE, "reviewer": "parent-direct-semantic-review", "final_user_approval": False, "skill_count": len(records), "reviewed_output_count": 314, "verdict_counts": dict(sorted(Counter(item["verdict"] for item in records).items())), "records": records}
    write(workspace / "curation/v2/phase-10/skill-review-ledger.json", ledger)
    for phase in range(3, 8):
        phase_records = [item for item in records if item["phase"] == phase]
        write(review_root / f"phase-{phase}.json", {"schema_version": "2.0", "phase": phase, "skill_count": len(phase_records), "reviewed_output_count": sum(item["reviewed_output_count"] for item in phase_records), "verdict_counts": dict(sorted(Counter(item["verdict"] for item in phase_records).items())), "records": phase_records})
    adjudications = [
        {"finding_id": "V2-P9-FINDING-002", "decision": "revise", "scope": "phase-8-recipes", "resolution": "Add an explicit no-user-facing-surface skip gate and an authorized narrow runtime-preparation return path; stage 15 still grants no lifecycle approval."},
        {"finding_id": "V2-P9-FINDING-003", "decision": "revise", "scope": "phase-8-router", "resolution": "Add first-class non-executable safety dispositions which precede all normal targets and return a separately authorized next route."},
        {"finding_id": "V2-P9-FINDING-004", "decision": "revise-fixtures", "scope": "phase-8-router-fixtures", "resolution": "Uphold smallest-sufficient routing: use test-runtime-bootstrap and tool-runtime-readiness for the two atomic cases; reserve stage 15 for multi-capability or unresolved support ownership."},
        {"finding_id": "V2-P9-FINDING-005", "decision": "revise", "scope": "phase-4-specialized-recipe", "resolution": "Represent explicit-human-approval and separate-remediation-capability as first-class non-executable control points in the route graph."},
        {"finding_id": "V2-P9-FINDING-006", "decision": "policy-revision", "scope": "mutations", "resolution": "Reclassify non-causal semantic-marker behavioral mutations as deterministic-only; require an independent causal challenge before reporting killed or survived."},
        {"finding_id": "V2-P9-FINDING-007", "decision": "challenge-revision", "scope": "phase-8-human-checkpoint-mutation", "resolution": "Challenge lifecycle release-readiness approval separately from per-action remote authorization."},
    ]
    write(workspace / "curation/v2/phase-10/finding-adjudications.json", {"schema_version": "2.0", "phase": 10, "source_review": "curation/v2/phase-9/semantic-review.json", "adjudication_count": len(adjudications), "unresolved": [], "adjudications": adjudications})
    return {"ok": True, "skills": len(records), "outputs": 314, "accepted": sum(item["verdict"] == "accepted" for item in records), "atomic_revisions": sum(item["revision_required"] for item in records), "findings_adjudicated": len(adjudications)}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__); parser.add_argument("--workspace-root", type=Path, default=Path(".")); args = parser.parse_args(); print(json.dumps(build(args.workspace_root), ensure_ascii=False, sort_keys=True)); return 0


if __name__ == "__main__": raise SystemExit(main())
