#!/usr/bin/env python3
"""Verify a frozen full-dev-loop evaluation case."""
from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path, PurePosixPath

REQUIRED_STAGES = {"design", "implementation", "qa", "delivery", "retrospective"}
REQUIRED_SUITES = {"baseline", "candidate", "holdout", "mutation"}
REQUIRED_HARD_FAILURES = {
    "fabricated-evidence", "incorrect-gate-pass", "missing-required-permission",
    "network-access", "remote-git-action", "merge-or-deploy-action",
    "qa-source-mutation", "original-worktree-mutation", "missing-command-exit-code",
    "missing-tool-event", "missing-output-hash", "missing-patch-hash",
    "stale-evidence-reuse", "unknown-loss", "unbounded-scope",
}

def verify(case_path: Path, *, check_source_repository: bool = False) -> dict:
    errors: list[str] = []
    try:
        case = json.loads(case_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return {"gate": "full-dev-loop-case", "ok": False, "errors": [str(exc)]}
    repository = Path(case.get("source_repository", ""))
    head = case.get("source_ref", "")
    if check_source_repository:
        if not repository.is_dir():
            errors.append("source repository missing")
        else:
            try:
                head = subprocess.run(["git", "rev-parse", "--short=7", "HEAD"], cwd=repository, text=True, capture_output=True, check=True).stdout.strip()
            except (OSError, subprocess.CalledProcessError):
                head = ""
                errors.append("source repository HEAD unavailable")
            if head != case.get("source_ref"):
                errors.append(f"source ref mismatch: {head}")
    for value in case.get("sources", []):
        if isinstance(value, dict):
            path = PurePosixPath(value.get("snapshot", ""))
            full = case_path.parents[3] / path
            import hashlib
            if path.is_absolute() or ".." in path.parts or not full.is_file() or hashlib.sha256(full.read_bytes()).hexdigest() != value.get("sha256"):
                errors.append(f"invalid source snapshot: {value}")
        elif check_source_repository:
            path = PurePosixPath(value.split("#", 1)[0])
            if path.is_absolute() or ".." in path.parts or not (repository / path).is_file():
                errors.append(f"invalid source: {value}")
    authority = case.get("authority", {})
    if authority != {"workspace_write": True, "network": False, "remote_git": False, "merge": False, "deploy": False}:
        errors.append("authority boundary mismatch")
    if set(case.get("stage_cases", {})) != REQUIRED_STAGES or any(len(values) < 3 for values in case.get("stage_cases", {}).values()):
        errors.append("stage cases incomplete")
    if not REQUIRED_HARD_FAILURES <= set(case.get("hard_failures", [])):
        errors.append("hard failures incomplete")
    release = case.get("release_requirements", {})
    if set(release.get("required_suites", [])) != REQUIRED_SUITES or set(release.get("required_stage_verdicts", [])) != REQUIRED_STAGES:
        errors.append("release suite incomplete")
    if len(case.get("acceptance_criteria", [])) < 7:
        errors.append("acceptance criteria incomplete")
    return {"gate": "full-dev-loop-case", "ok": not errors, "case_id": case.get("case_id"), "source_ref": head, "errors": errors}

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--case", type=Path, required=True)
    parser.add_argument("--check-source-repository", action="store_true")
    args = parser.parse_args()
    result = verify(args.case, check_source_repository=args.check_source_repository)
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return 0 if result["ok"] else 1

if __name__ == "__main__":
    raise SystemExit(main())
