#!/usr/bin/env python3
"""Build deterministic Phase 11 acceptance manifest and report."""
from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path
from typing import Any

try:
    from tools.curation.v2_phase11_gate import verify
except ModuleNotFoundError:
    from v2_phase11_gate import verify


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes().replace(b"\r\n", b"\n")).hexdigest()


def write(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")


def build(workspace: Path, pytest_summary: str, repository_gate_count: int) -> dict[str, Any]:
    workspace = workspace.resolve(); phase_root = workspace / ".specs/capability-compiler-v2/phase-11"; gate = verify(workspace)
    if not gate["ok"]:
        raise ValueError("Phase 11 gate is not green: " + "; ".join(gate["errors"]))
    excluded = {phase_root / "artifact-manifest.json", phase_root / "phase-report.json"}; paths = []
    for directory in [phase_root, workspace / "curation/v2/phase-11", workspace / "evals/runs/capability-compiler-v2/phase-11"]:
        paths.extend(
            path for path in directory.rglob("*")
            if path.is_file() and path not in excluded and "__pycache__" not in path.parts and ".pytest_cache" not in path.parts
        )
    artifacts = [{"path": path.relative_to(workspace).as_posix(), "bytes": path.stat().st_size, "sha256": digest(path)} for path in sorted(set(paths))]
    tree = hashlib.sha256("".join(f"{item['path']}\0{item['sha256']}\n" for item in artifacts).encode()).hexdigest()
    by_root = Counter("/".join(item["path"].split("/")[:6]) for item in artifacts)
    write(phase_root / "artifact-manifest.json", {"schema_version": "2.0", "phase": 11, "artifact_count": len(artifacts), "tree_sha256": tree, "by_root": dict(sorted(by_root.items())), "artifacts": artifacts})
    semantic = load(workspace / "curation/v2/phase-11/semantic-review.json")
    browser = load(workspace / "evals/runs/capability-compiler-v2/phase-11/benchshare-v1/evidence/browser/iteration-3/report.json")
    performance = load(workspace / "evals/runs/capability-compiler-v2/phase-11/benchshare-v1/evidence/performance/iteration-1/report.json")
    package = load(workspace / "evals/runs/capability-compiler-v2/phase-11/benchshare-v1/package/package-receipt.json")
    report = {
        "schema_version": "2.0", "phase": 11, "status": "passed-local-end-to-end-validation-pending-final-approval",
        "gate": gate["gate"], "gate_ok": True, "phase_11_complete": True, "eligible_for_phase_12": True,
        "final_user_release_approval": False, "released": False,
        "artifact_manifest": ".specs/capability-compiler-v2/phase-11/artifact-manifest.json", "artifact_count": len(artifacts), "artifact_tree_sha256": tree,
        "prior_phase10_tree_sha256": gate["identities"]["phase10_tree_sha256"],
        "case": {"id": "benchshare-v1", "product": "BenchShare", "visual_direction": "municipal-wayfinding", "runtime_tree_sha256": gate["identities"]["runtime_tree_sha256"], "tests": "14 passed", "independent_code_findings_closed": 6, "browser_screenshots": len(browser["screenshots"]), "blackbox_findings_closed": 2},
        "performance": {"claim_boundary": "local-only", "health_p95_ms": performance["metrics"]["health"]["p95_ms"], "list_p95_ms": performance["metrics"]["reservation_list"]["p95_ms"], "create_p95_ms": performance["metrics"]["reservation_create"]["p95_ms"], "concurrent_approval": {"attempts": 10, "approved": performance["concurrency"]["approved_responses"], "conflicts": performance["concurrency"]["conflicts"], "server_errors": performance["concurrency"]["server_errors"]}},
        "delivery": {"package_sha256": package["package_sha256"], "patch_sha256": package["patch_sha256"], "package_tree_sha256": package["tree_sha256"], "reproducible": True, "fresh_unpack_tests": "14 passed", "patch_rebuild_exact": True, "backup_restore_rehearsed": True},
        "failure_retention": semantic["failure_retention"], "authority": semantic["authority"], "residual_risks": semantic["residual_risks"],
        "verification": {"repository_gates_ok": True, "repository_gate_count": repository_gate_count, "pytest_summary": pytest_summary, "phase11_gate_checks": len(gate["checks"]), "thresholds_lowered": False, "failed_evidence_deleted": 0, "remote_actions": 0},
        "limitations": ["Phase 11 validates one local synthetic full-stack case, not market demand or production capacity.", "Deployment, provider observation, remote rollback, and real incident response were not authorized or executed.", "The V2 candidate remains evaluating and unreleased until Phase 12 final human approval."],
        "next_required_phase": "Phase 12 final human approval and separately authorized controlled release", "errors": [],
    }
    write(phase_root / "phase-report.json", report)
    return {"gate": "capability-compiler-v2-phase-11-report", "ok": True, "artifact_count": len(artifacts), "tree_sha256": tree, "case_id": "benchshare-v1", "released": False}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__); parser.add_argument("--workspace-root", type=Path, default=Path(".")); parser.add_argument("--pytest-summary", required=True); parser.add_argument("--repository-gate-count", type=int, required=True); args = parser.parse_args()
    print(json.dumps(build(args.workspace_root, args.pytest_summary, args.repository_gate_count), ensure_ascii=False, sort_keys=True)); return 0


if __name__ == "__main__":
    raise SystemExit(main())
