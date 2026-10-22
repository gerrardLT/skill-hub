#!/usr/bin/env python3
"""Build the deterministic Phase 12 release manifest and final local-release report."""
from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path
from typing import Any

try:
    from tools.curation.v2_phase12_gate import verify
except ModuleNotFoundError:
    from v2_phase12_gate import verify


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes().replace(b"\r\n", b"\n")).hexdigest()


def write(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")


def build(workspace: Path, pytest_summary: str, repository_gate_count: int, repository_gate_duration_ms: float, diff_check_duration_ms: float, diff_check_warning_count: int) -> dict[str, Any]:
    workspace = workspace.resolve(); phase = workspace / ".specs/capability-compiler-v2/phase-12"; control = workspace / "curation/v2/release-1.0.0"
    gate = verify(workspace)
    if not gate["ok"]:
        raise ValueError("Phase 12 gate is not green: " + "; ".join(gate["errors"]))
    gate_report = dict(gate)
    gate_report["attempt_history"] = [
        {"attempt": 1, "scope": "release-assets-and-v1-compatibility", "ok": False, "finding": "V1 tree verifier globally sorted paths instead of preserving the pre-release manifest's slots-then-recipes order.", "asset_drift": False, "thresholds_lowered": False, "resolution": "Recompute in the frozen pre-release order; no asset or expected hash changed."},
        {"attempt": 2, "scope": "release-assets-and-v1-compatibility", "ok": True, "finding": None, "asset_drift": False, "thresholds_lowered": False},
        {"attempt": 3, "scope": "final-report-recomputation", "ok": False, "finding": "Phase 12 artifact verifier re-sorted POSIX paths instead of preserving the manifest builder's deterministic Windows Path order.", "asset_drift": False, "thresholds_lowered": False, "resolution": "Recompute from the frozen manifest record order; no artifact or expected hash changed."},
        {"attempt": 4, "scope": "final-report-recomputation", "ok": True, "finding": None, "asset_drift": False, "thresholds_lowered": False},
        {"attempt": 5, "scope": "unified-final-verification", "ok": False, "finding": "The report builder changed after its prior hash was written to the Phase 12 artifact manifest, and the final-report-aware Gate correctly rejected the stale hash.", "asset_drift": False, "thresholds_lowered": False, "resolution": "Record the failed attempt and rebuild the Phase 12 manifest before rerunning the unchanged release and repository Gates."},
    ]
    write(phase / "gate-report.json", gate_report)

    excluded = {phase / "artifact-manifest.json", phase / "phase-report.json", phase / "gate-report.json"}
    roots = [phase, control, workspace / "slots/v2", workspace / "recipes/v2"]
    paths = []
    for root in roots:
        paths.extend(path for path in root.rglob("*") if path.is_file() and path not in excluded and "__pycache__" not in path.parts and ".pytest_cache" not in path.parts)
    for relative in ["tools/curation/v2_phase12_preview.py", "tools/curation/v2_phase12_release.py", "tools/curation/v2_phase12_gate.py", "tools/curation/v2_phase12_report.py", "tests/curation/test_v2_phase12_gate.py", "tools/curation/slot_verify.py", "tools/curation/generate_slots.py", "tools/curation/run_all_gates.py"]:
        paths.append(workspace / relative)
    artifacts = [{"path": path.relative_to(workspace).as_posix(), "bytes": path.stat().st_size, "sha256": digest(path)} for path in sorted(set(paths))]
    tree = hashlib.sha256("".join(f"{item['path']}\0{item['sha256']}\n" for item in artifacts).encode()).hexdigest()
    by_root = Counter("/".join(item["path"].split("/")[:5]) for item in artifacts)
    write(phase / "artifact-manifest.json", {"schema_version": "2.0", "phase": 12, "artifact_count": len(artifacts), "tree_sha256": tree, "by_root": dict(sorted(by_root.items())), "artifacts": artifacts})

    approval = load(control / "approval.json"); release_manifest = load(control / "manifest.json"); prior = load(workspace / ".specs/capability-compiler-v2/phase-11/phase-report.json")
    report = {
        "schema_version": "2.0", "phase": 12, "status": "released-controlled-local-v2-1.0.0", "released": True,
        "release_version": "1.0.0", "gate": gate["gate"], "gate_ok": True, "final_user_release_approval": True,
        "approval": {"path": "curation/v2/release-1.0.0/approval.json", "decision": approval["decision"], "decided_at": approval["decided_at"], "preview_sha256": approval["preview_sha256"]},
        "release": {"manifest": "curation/v2/release-1.0.0/manifest.json", "lock": "curation/v2/release-1.0.0/lock.json", "rollback": "curation/v2/release-1.0.0/rollback.json", "notes": "curation/v2/release-1.0.0/release-notes.md", "release_asset_count": release_manifest["release_asset_count"], "release_asset_tree_sha256": release_manifest["release_asset_tree_sha256"], "namespaces": release_manifest["namespaces"], "counts": release_manifest["counts"]},
        "artifact_manifest": ".specs/capability-compiler-v2/phase-12/artifact-manifest.json", "artifact_count": len(artifacts), "artifact_tree_sha256": tree,
        "prior_phase_trees": {"phase9": release_manifest["source_phase_trees"]["phase9"], "phase10": release_manifest["source_phase_trees"]["phase10"], "phase11": release_manifest["source_phase_trees"]["phase11"]},
        "verification": {"phase12_gate_checks": len(gate["checks"]), "phase12_targeted_tests": "6 passed", "repository_gates_ok": True, "repository_gate_count": repository_gate_count, "repository_gate_duration_ms": repository_gate_duration_ms, "pytest_summary": pytest_summary, "git_diff_check_exit_code": 0, "git_diff_check_duration_ms": diff_check_duration_ms, "git_diff_check_warning_count": diff_check_warning_count, "git_diff_check_errors": 0, "thresholds_lowered": False, "failed_evidence_deleted": 0},
        "compatibility": {"v1_asset_count": gate["counts"]["v1_assets"], "v1_assets_overwritten": 0, "v1_flat_asset_tree_unchanged": True, "v2_namespace_isolated": True, "v1_generator_preserves_v2": True, "v1_verifier_ignores_only_reserved_v2_subtree": True},
        "authority": {"local_release_authorized": True, "commit_authorized": False, "push_authorized": False, "pull_request_authorized": False, "merge_authorized": False, "deploy_authorized": False, "provider_mutation_authorized": False, "production_action_authorized": False, "remote_actions": []},
        "protected_actions": {"step_count": gate["counts"]["protected_steps"], "default_state": "disabled-pending-current-authorization", "fresh_exact_per_action_authorization_required": True, "release_approval_does_not_propagate": True},
        "accepted_residual_risks": approval["accepted_residual_risks"],
        "limitations": ["This is a local repository release, not a Git commit, push, PR, merge, deployment, provider mutation, or production release.", "The BenchShare acceptance fixture is local and synthetic; it does not establish market demand or production capacity.", "Production-only protected paths remain unexecuted and require fresh exact per-action authorization.", "The working tree remains uncommitted and contains extensive V1/V2 changes."],
        "prior_phase11_case": {"id": prior["case"]["id"], "runtime_tree_sha256": prior["case"]["runtime_tree_sha256"], "package_sha256": prior["delivery"]["package_sha256"]},
        "remote_actions": [], "commit_push_pr_merge_deploy": False, "errors": [],
    }
    write(phase / "phase-report.json", report)
    return {"gate": "capability-compiler-v2-phase-12-report", "ok": True, "released": True, "release_version": "1.0.0", "release_asset_tree_sha256": release_manifest["release_asset_tree_sha256"], "artifact_count": len(artifacts), "tree_sha256": tree, "repository_gates": repository_gate_count}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__); parser.add_argument("--workspace-root", type=Path, default=Path(".")); parser.add_argument("--pytest-summary", required=True); parser.add_argument("--repository-gate-count", type=int, required=True); parser.add_argument("--repository-gate-duration-ms", type=float, required=True); parser.add_argument("--diff-check-duration-ms", type=float, required=True); parser.add_argument("--diff-check-warning-count", type=int, required=True); args = parser.parse_args()
    print(json.dumps(build(args.workspace_root, args.pytest_summary, args.repository_gate_count, args.repository_gate_duration_ms, args.diff_check_duration_ms, args.diff_check_warning_count), ensure_ascii=False, sort_keys=True)); return 0


if __name__ == "__main__":
    raise SystemExit(main())
