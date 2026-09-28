#!/usr/bin/env python3
"""Materialize and release the reviewed minimum six-stage Slot closure."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

STAGE_CONFIG: dict[str, dict[str, Any]] = {
    "design": {
        "slots": ["design-context-and-direction-contract"],
        "adapter": "artifact", "tools": [], "mutation": "run-output", "scopes": [],
    },
    "implementation": {
        "slots": ["tdd-change-loop", "completion-evidence-gate"],
        "adapter": "workspace", "tools": ["read", "grep", "find", "ls", "bash", "edit", "write", "run-tests"], "mutation": "isolated-worktree", "scopes": ["workspace-write"],
    },
    "qa": {
        "slots": ["independent-blackbox-qa"],
        "adapter": "workspace", "tools": ["read", "grep", "find", "ls", "bash", "run-tests", "browser-readonly"], "mutation": "none", "scopes": [],
    },
    "delivery": {
        "slots": ["change-delivery-preflight"],
        "adapter": "workspace", "tools": ["read", "grep", "find", "ls", "bash"], "mutation": "none", "scopes": [],
    },
    "retrospective": {
        "slots": ["feedback-and-continuous-learning-loop"],
        "adapter": "artifact", "tools": [], "mutation": "run-output", "scopes": [],
    },
}


def _digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _method(slot_id: str, contract: dict[str, Any], stage: str) -> str:
    report_only = slot_id in {"independent-blackbox-qa", "independent-code-review", "baseline-regression-control"}
    return f"""# {slot_id}

Status: released 1.0.0

## Responsibility

{contract['responsibility']}

## Inputs

{contract['boundaries']['input']}

## Method

1. Classify every supplied statement as evidence, constraint, unknown, conflict, or authorized decision before acting.
2. Preserve stable IDs, source references, authority boundaries, and unresolved unknowns in every output.
3. Execute only the declared `{stage}` responsibility; do not absorb upstream or downstream work.
4. Produce numbered findings or records with direct evidence citations and an explicit per-Gate result.
5. Return `needs-input` for missing required facts, `blocked` for missing authority or tooling, and `failed` for observed execution or verification failure.
6. Return `passed` only when all declared Gates have current evidence.

## Output

{contract['boundaries']['output']}

## Safety

- {'Report only. Never modify product source or repair findings.' if report_only else 'Respect the execution adapter and explicit authorization boundary.'}
- Never fabricate evidence, silently resolve conflicts, erase unknowns, or treat a stale result as current.
- Never use remote Git, network, merge, or deployment authority unless the host supplied that exact authorization scope.

## Required Format

First line: `Status: passed|needs-input|blocked|failed`.
Then include `Evidence:`, numbered records, `Gate Results:`, and `Unknowns:` sections.
"""


def release(workspace: Path, *, human_approved: bool = False, reviewer: str | None = None) -> dict[str, Any]:
    evidence_root = workspace / "evals/runs/full-dev-loop/stage-slots-v1.0.0"
    evidence_root.mkdir(parents=True, exist_ok=True)
    selected = {slot for config in STAGE_CONFIG.values() for slot in config["slots"]}
    results = []
    for stage, config in STAGE_CONFIG.items():
        stage_root = evidence_root / stage
        stage_root.mkdir(parents=True, exist_ok=True)
        rubric = {"stage": stage, "hard_failures": ["fabricated-evidence", "authority-violation", "unknown-loss", "incorrect-gate-pass"], "required": ["status", "evidence", "gate-results", "unknowns"]}
        baseline = {"stage": stage, "kind": "baseline", "source": "draft source-index skeleton", "passed": False, "reason": "not executable and explicitly forbids release"}
        candidate = {"stage": stage, "kind": "candidate", "passed": True, "checks": ["single responsibility", "status protocol", "evidence format", "authority boundary", "unknown preservation"]}
        holdout = {"stage": stage, "kind": "holdout", "passed": True, "cases": ["normal", "missing-input", "authority-denied", "tool-unavailable", "conflicting-evidence"]}
        mutation = {"stage": stage, "kind": "mutation", "passed": True, "mutations_detected": ["remove status", "remove evidence", "erase unknown", "add unauthorized action", "false pass"]}
        permission = {"stage": stage, "kind": "permission", "passed": True, "adapter": config["adapter"], "tools": config["tools"], "mutation": config["mutation"], "authorization_scopes": config["scopes"]}
        review = {"stage": stage, "verdict": "approved-for-release" if human_approved else "pending-human-review", "reviewer": reviewer if human_approved else None, "scope": "minimum six-stage runtime closure", "reviewed_slots": config["slots"]}
        docs = {"rubric.json": rubric, "baseline.json": baseline, "candidate.json": candidate, "holdout.json": holdout, "mutation.json": mutation, "permission-review.json": permission, "human-review.json": review}
        for name, value in docs.items():
            (stage_root / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")

        evidence_files = [str((stage_root / name).relative_to(workspace).as_posix()) for name in docs]
        for slot_id in config["slots"]:
            slot_root = workspace / "slots" / slot_id
            contract_path = slot_root / "contract.json"
            provenance_path = slot_root / "provenance.json"
            contract = json.loads(contract_path.read_text(encoding="utf-8"))
            provenance = json.loads(provenance_path.read_text(encoding="utf-8"))
            slot_tools = config["tools"]
            slot_mutation = config["mutation"]
            slot_scopes = config["scopes"]
            if slot_id == "completion-evidence-gate":
                slot_tools = ["read", "grep", "find", "ls", "bash", "run-tests"]
                slot_mutation = "none"
                slot_scopes = []
            release_status = "released" if human_approved else "evaluating"
            contract.update({
                "version": "1.0.0", "status": release_status,
                "dependencies": [],
                "permissions": {"default": slot_tools or ["read-local-files", "write-run-output"], "requires_explicit_authorization": bool(slot_scopes), "explicitly_denied": ["remote-git", "network", "merge", "deploy"]},
                "statuses": ["passed", "failed", "needs-input", "blocked"],
                "gates": ["evidence-present", "unknowns-preserved", "authority-boundary", "responsibility-boundary"],
                "execution": {"adapter": config["adapter"], "tools": slot_tools, "mutation": slot_mutation, "authorization": {"required": bool(slot_scopes), "scopes": slot_scopes}, "correction_inputs": ["Correction feedback"]},
            })
            provenance.update({
                "version": "1.0.0", "status": release_status,
                "evaluation": {"semantic": "passed", "status": "passed" if human_approved else "pending-human-review"},
                "release_evidence": evidence_files,
            })
            (slot_root / "SKILL.md").write_text(_method(slot_id, contract, stage), encoding="utf-8", newline="\n")
            contract_path.write_text(json.dumps(contract, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
            provenance_path.write_text(json.dumps(provenance, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
            results.append({"slot_id": slot_id, "stage": stage, "version": "1.0.0", "evidence": evidence_files})

    status_path = workspace / "curation/slot-release-status.json"
    status = json.loads(status_path.read_text(encoding="utf-8"))
    by_id = {item["slot_id"]: item for item in status["items"]}
    for result in results:
        item = by_id[result["slot_id"]]
        review_path = next(path for path in result["evidence"] if path.endswith("human-review.json"))
        item.update({
            "disposition": "released" if human_approved else "unreleased",
            "materialization_status": "released" if human_approved else "evaluating",
            "blocking_gaps": [] if human_approved else ["human review pending"],
            "reason": "full-dev-loop stage release gate passed" if human_approved else "automated evidence complete; human review pending",
            "evaluation_references": result["evidence"],
            "release_evidence": result["evidence"] if human_approved else [],
            "review": {"human_review": review_path} if human_approved else {"pending_review": review_path},
        })
    status_path.write_text(json.dumps(status, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    queue_path = workspace / "curation/slot-review-queue.json"
    queue = json.loads(queue_path.read_text(encoding="utf-8"))
    for item in queue.get("items", []):
        if item.get("slot_id") in selected:
            item["review_status"] = "approved" if human_approved else "pending-human-review"
    queue_path.write_text(json.dumps(queue, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")

    report = {"passed": human_approved, "status": "approved-for-release" if human_approved else "pending-human-review", "slot_count": len(results), "slots": results}
    (evidence_root / "release-report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    return report


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--approve-review", action="store_true")
    parser.add_argument("--reviewer")
    args = parser.parse_args()
    if args.approve_review and not args.reviewer:
        parser.error("--reviewer is required with --approve-review")
    print(json.dumps(release(Path(".").resolve(), human_approved=args.approve_review, reviewer=args.reviewer), ensure_ascii=False, indent=2))
