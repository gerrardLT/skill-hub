#!/usr/bin/env python3
"""Authorize six-stage release only from machine and human evidence."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

try:
    from tools.curation.recipe_verify import _validate_slot_run
except ModuleNotFoundError:  # direct script execution
    from recipe_verify import _validate_slot_run

SLOTS = {
    "design-context-and-direction-contract",
    "tdd-change-loop",
    "completion-evidence-gate",
    "independent-blackbox-qa",
    "change-delivery-preflight",
    "feedback-and-continuous-learning-loop",
}
SUITES = {"baseline", "candidate", "holdout", "mutation"}
RECIPES = {"write-prd", "design-web-flow", "build-feature-tdd", "qa-only", "ship-release", "retro-to-requirements", "full-dev-loop"}
REQUIRED_STAGES = {"requirements", "design", "implementation", "qa", "delivery", "retrospective"}


def _review_approved(review: dict) -> bool:
    verdicts = review.get("stage_verdicts", {})
    return review.get("verdict") == "approved-for-release" and set(verdicts) == REQUIRED_STAGES and set(verdicts.values()) == {"approved"}


def verify(workspace: Path, *, check_gate_report: bool = True) -> dict:
    errors: list[str] = []
    root = workspace / "evals/runs/full-dev-loop/ip-rate-limiting-v1"
    review = json.loads((root / "human-review.json").read_text(encoding="utf-8"))
    if not _review_approved(review):
        errors.append("human semantic review is not approved")
    if check_gate_report:
        report = json.loads((workspace / "curation/gate-report.json").read_text(encoding="utf-8"))
        results = {item["name"]: item for item in report.get("results", [])}
        required_gates = {"tests", "source", "phase2", "phase3", "phase4", "phase5-provenance", "phase5-release", "phase6", "phase7", "phase8-source", "full-loop-case", "full-loop-security", "full-loop-evidence", "full-loop-lifecycle", "full-loop-feedback"}
        for name in sorted(required_gates):
            if results.get(name, {}).get("ok") is not True:
                errors.append(f"machine gate not passing: {name}")
    evidence_root = root / "slot-evaluations"
    for slot in sorted(SLOTS):
        for suite in sorted(SUITES):
            path = evidence_root / slot / f"{suite}.json"
            if not path.is_file():
                errors.append(f"missing slot evaluation: {slot}/{suite}")
                continue
            data = json.loads(path.read_text(encoding="utf-8"))
            if data.get("slot_id") != slot or data.get("suite") != suite or data.get("passed") is not True or not data.get("cases"):
                errors.append(f"invalid slot evaluation: {slot}/{suite}")
                continue
            problem = _validate_slot_run(path, slot, workspace)
            if problem:
                errors.append(problem)
    candidate_root = workspace / "evals/candidates/full-dev-loop/recipes"
    if {p.stem for p in candidate_root.glob("*.json")} != RECIPES:
        errors.append("candidate recipe closure mismatch")
    return {"gate": "full-dev-loop-release", "ok": not errors, "slot_count": len(SLOTS), "recipe_count": len(RECIPES), "errors": errors}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workspace-root", type=Path, default=Path("."))
    parser.add_argument("--skip-gate-report", action="store_true")
    args = parser.parse_args()
    result = verify(args.workspace_root.resolve(), check_gate_report=not args.skip_gate_report)
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
