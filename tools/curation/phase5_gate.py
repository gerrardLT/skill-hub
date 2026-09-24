#!/usr/bin/env python3
"""Verify the complete requirements-to-AC pilot release evidence."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

PILOT_SLOTS = (
    "problem-framing",
    "requirements-rules",
    "acceptance-criteria",
    "requirements-quality-gate",
)
CANDIDATE_GRADES = (
    "final-paired-tuning/candidate/grading.json",
    "formal-holdout/candidate/grading.json",
    "formal-holdout-fresh/candidate/grading.json",
)
REQUIRED_REPORTS = (
    "repeated-formal-holdout/variance-report.json",
    "downstream-handoff/req-ac-h04-approved-copy-correction/verification.json",
    "mutations/report.json",
)


def _load(path: Path, errors: list[str]) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"cannot read {path.as_posix()}: {exc}")
        return {}
    if not isinstance(value, dict):
        errors.append(f"not an object: {path.as_posix()}")
        return {}
    return value


def verify_phase5_release(workspace: Path) -> dict[str, Any]:
    errors: list[str] = []
    run_root = workspace / "evals/runs/requirements-to-ac/iteration-2"
    freeze = _load(run_root / "candidate-freeze.json", errors)
    frozen_paths: set[str] = set()
    for entry in freeze.get("files", []):
        if not isinstance(entry, dict) or not isinstance(entry.get("path"), str):
            errors.append("invalid candidate freeze entry")
            continue
        path = workspace / entry["path"]
        frozen_paths.add(entry["path"])
        if not path.is_file():
            errors.append(f"missing frozen file: {entry['path']}")
        elif path.stat().st_size != entry.get("bytes") or hashlib.sha256(path.read_bytes()).hexdigest() != entry.get("sha256"):
            errors.append(f"candidate freeze mismatch: {entry['path']}")

    for relative in CANDIDATE_GRADES:
        grade = _load(run_root / relative, errors)
        cases = grade.get("cases")
        if not isinstance(cases, list) or not cases:
            errors.append(f"missing grade cases: {relative}")
            continue
        for case in cases:
            status = case.get("status_match", {}) if isinstance(case, dict) else {}
            hard = case.get("hard_failures", []) if isinstance(case, dict) else []
            non_review_failures = [value for value in hard if value != "pending-human-review"] if isinstance(hard, list) else ["invalid-hard-failures"]
            if status.get("passed") is not True or case.get("run_validation_errors") not in ([], None) or non_review_failures:
                errors.append(f"candidate grade failed: {relative}:{case.get('case_id')}")

    for relative in REQUIRED_REPORTS:
        report = _load(run_root / relative, errors)
        if report.get("passed") is not True:
            errors.append(f"report not passing: {relative}")

    review = run_root / "review.html"
    if not review.is_file() or review.stat().st_size < 1000:
        errors.append("official review viewer missing or empty")
    feedback = _load(run_root / "feedback.json", errors)
    if feedback.get("verdict") != "approved-for-release" or not feedback.get("reviewer") or not feedback.get("cases_reviewed"):
        errors.append("human feedback is not approved")

    for slot_id in PILOT_SLOTS:
        contract = _load(workspace / "slots" / slot_id / "contract.json", errors)
        provenance = _load(workspace / "slots" / slot_id / "provenance.json", errors)
        if contract.get("id") != slot_id or contract.get("version") != "0.2.0" or contract.get("status") != "released":
            errors.append(f"slot is not released 0.2.0: {slot_id}")
        if provenance.get("id") != slot_id or provenance.get("version") != "0.2.0" or provenance.get("status") != "released":
            errors.append(f"provenance is not released 0.2.0: {slot_id}")
        if provenance.get("evaluation", {}).get("status") != "passed" or not provenance.get("release_evidence"):
            errors.append(f"slot release evidence missing: {slot_id}")

    return {
        "gate": "phase-5-requirements-to-ac-release",
        "ok": not errors,
        "candidate_freeze_files": len(frozen_paths),
        "pilot_slot_count": len(PILOT_SLOTS),
        "errors": sorted(set(errors)),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workspace-root", type=Path, default=Path("."))
    args = parser.parse_args()
    report = verify_phase5_release(args.workspace_root.resolve())
    print(json.dumps(report, ensure_ascii=False, sort_keys=True))
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
