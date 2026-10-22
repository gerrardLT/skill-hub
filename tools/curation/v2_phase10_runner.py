#!/usr/bin/env python3
"""Plan and run the 60 targeted Phase 10 revision-3 Recipe/router evaluations."""
from __future__ import annotations

import argparse
import concurrent.futures
import json
import shutil
import time
from pathlib import Path
from typing import Any

try:
    from tools.curation.v2_phase9_runner import MODEL, add_task, load, run_one, sha_text, utc_now, write
except ModuleNotFoundError:
    from v2_phase9_runner import MODEL, add_task, load, run_one, sha_text, utc_now, write

PLAN_PATH = Path("curation/v2/phase-10/run-plan.json")
RUN_ROOT = Path("evals/runs/capability-compiler-v2/phase-10")
REVISION = Path("evals/candidates/capability-compiler-v2/phase-10/revision-4")
PHASE9_TREE = "7540c53426a5dff605c3f751fdaf105f52059ffbafce213d77c9c3db94214152"


def p8_sources(case_id: str) -> list[str]:
    r = "evals/candidates/capability-compiler-v2/phase-10/revision-4/phase-8/"
    old = "evals/candidates/capability-compiler-v2/phase-8/"
    if any(key in case_id for key in ["optional-ai", "skip-ui"]): return [r + "recipes/stages/stage-05-experience-design.json", old + "recipes/stages/stage-06-architecture-risk-security.json"]
    if any(key in case_id for key in ["support-insert", "stage15"]): return [r + "recipes/composites/full-software-lifecycle.json", r + "recipes/stages/stage-15-tool-runtime-support.json"]
    if any(key in case_id for key in ["invalidation", "stale", "resume", "handoff"]): return [r + "recipes/composites/full-software-lifecycle.json"]
    if "review-repair" in case_id: return [r + "recipes/composites/feature-build-and-verify.json", old + "recipes/stages/stage-07-implementation-integration.json", old + "recipes/stages/stage-08-verification-quality.json"]
    if any(key in case_id for key in ["observe-rollback", "canary"]): return [old + "recipes/composites/verified-change-delivery-and-observation.json", old + "recipes/stages/stage-12-observation-canary.json", old + "recipes/stages/stage-13-incident-recovery.json"]
    if any(key in case_id for key in ["remote-stop", "merge-deploy"]): return [r + "recipes/composites/verified-change-delivery-and-observation.json", old + "recipes/stages/stage-10-release-readiness.json", old + "recipes/stages/stage-11-deployment-change.json"]
    if "learning" in case_id: return [old + "recipes/composites/incident-recovery-and-learning.json", old + "recipes/stages/stage-14-learning-feedback.json"]
    raise ValueError(case_id)


def build_plan(workspace: Path) -> dict[str, Any]:
    workspace = workspace.resolve()
    if load(workspace / ".specs/capability-compiler-v2/phase-9/artifact-manifest.json")["tree_sha256"] != PHASE9_TREE: raise ValueError("Phase 9 tree drift")
    tasks = []; revision = workspace / REVISION
    p4 = revision / "phase-4"
    for case in load(p4 / "recipe-holdout-cases.json")["cases"]:
        add_task(tasks, {"category": "p4-recipe-holdout", "phase": 10, "recipe_id": "complete-ui-design-and-review", "case_id": case["id"], "input": case["input"], "schema": "route", "variant": "candidate-revision-4", "expected": {"required_steps": case["required_steps"]}, "material": {"kind": "file", "path": (p4 / "complete-ui-design-and-review.json").relative_to(workspace).as_posix()}}, workspace)
    router_material = {"kind": "router", "router": (revision / "phase-8/router.json").relative_to(workspace).as_posix(), "index": "evals/candidates/capability-compiler-v2/phase-8/skill-index.json"}
    for filename, set_name in [("router-cases.json", "authored"), ("router-holdout-cases.json", "holdout")]:
        for case in load(revision / "phase-8" / filename)["cases"]:
            add_task(tasks, {"category": "p8-router", "phase": 10, "set": set_name, "case_id": case["id"], "input": case["input"], "schema": "router", "variant": "candidate-revision-4", "expected": {"target": case["expected_target"]}, "material": router_material}, workspace)
    for filename, set_name in [("recipe-cases.json", "authored"), ("recipe-holdout-cases.json", "holdout")]:
        for case in load(revision / "phase-8" / filename)["cases"]:
            add_task(tasks, {"category": "p8-recipe", "phase": 10, "set": set_name, "case_id": case["id"], "input": case["assertion"], "schema": "recipe", "variant": "candidate-revision-4", "expected": {"decision": "satisfied"}, "material": {"kind": "json-files", "paths": p8_sources(case["id"])}}, workspace)
    mutation_specs = [
        ("P10-P4-review-evidence", "A release route must include current review-evidence before rendered critique and release disposition.", "evals/candidates/capability-compiler-v2/phase-10/revision-4/phase-4/complete-ui-design-and-review.json"),
        ("P10-P4-human-control-points", "Independent review findings require explicit-human-approval and a separate-remediation-capability before source repair, then stale evidence invalidation and recapture.", "evals/candidates/capability-compiler-v2/phase-10/revision-4/phase-4/complete-ui-design-and-review.json"),
        ("P10-P4-complete-route-planning", "Complete UI route planning includes the post-decision release-gate while actual execution remains stopped at explicit-human-approval until the named decision exists.", "evals/candidates/capability-compiler-v2/phase-10/revision-4/phase-4/complete-ui-design-and-review.json"),
        ("P10-P8-handoff", "The full lifecycle preserves V2-HANDOFF-006 between architecture/security and implementation/integration with all evidence and invalidation fields.", "evals/candidates/capability-compiler-v2/phase-10/revision-4/phase-8/recipes/composites/full-software-lifecycle.json"),
        ("P10-P8-always-on", "Independent code review defaults to skipped and activates only when its explicit condition matches.", "evals/candidates/capability-compiler-v2/phase-8/recipes/stages/stage-08-verification-quality.json"),
        ("P10-P8-review-write", "Independent code review uses permission_identity read-only and mutation_scope none, never edits source, never remediates its own findings, and never approves its own repair.", "evals/candidates/capability-compiler-v2/phase-8/recipes/stages/stage-08-verification-quality.json"),
        ("P10-P8-remote-activation", "Remote Git push remains disabled pending fresh exact current authorization.", "evals/candidates/capability-compiler-v2/phase-8/recipes/stages/stage-11-deployment-change.json"),
        ("P10-P8-lifecycle-approval", "Release readiness requires a named human to accept release scope and residual risk before any separately authorized remote action; per-action authorization alone is insufficient.", "evals/candidates/capability-compiler-v2/phase-10/revision-4/phase-8/recipes/composites/verified-change-delivery-and-observation.json"),
        ("P10-P8-invalidation", "A source capability rerun invalidates the affected handoff and all dependent downstream evidence.", "evals/candidates/capability-compiler-v2/phase-10/revision-4/phase-8/recipes/composites/full-software-lifecycle.json"),
        ("P10-P8-resume-validation", "Resume occurs only after current revalidation of checkpoint input identities and hashes, output identities and hashes, all gates, exact authority, invalidation state, and dependent evidence.", "evals/candidates/capability-compiler-v2/phase-10/revision-4/phase-8/recipes/composites/full-software-lifecycle.json"),
    ]
    for mutation_id, assertion, control_relative in mutation_specs:
        control_path = (workspace / control_relative).resolve()
        if not control_path.is_file(): raise FileNotFoundError(control_path)
        common = {"category": "causal-mutation", "phase": 10, "case_id": mutation_id + "-challenge", "mutation_id": mutation_id, "input": assertion, "schema": "recipe"}
        add_task(tasks, {**common, "variant": "control", "expected": {"decision": "satisfied"}, "material": {"kind": "file", "path": control_path.relative_to(workspace).as_posix()}}, workspace)
        add_task(tasks, {**common, "variant": "mutated", "expected": {"decision": "violated"}, "material": {"kind": "file", "path": (revision / "mutations" / f"{mutation_id}.json").relative_to(workspace).as_posix()}}, workspace)
    if len(tasks) != 60: raise ValueError(f"expected 60 tasks, got {len(tasks)}")
    digest = sha_text(json.dumps(tasks, ensure_ascii=False, sort_keys=True, separators=(",", ":")))
    plan = {"schema_version": "2.0", "phase": 10, "revision": 4, "version": "0.1.4-v2-candidate", "status": "planned", "model_request": MODEL, "thinking": "low", "tools": [], "network_tools": False, "candidate_action_execution": False, "source_phase9_tree": PHASE9_TREE, "task_count": len(tasks), "counts": dict(sorted(__import__("collections").Counter(task["category"] for task in tasks).items())), "task_sha256": digest, "tasks": tasks}
    write(workspace / PLAN_PATH, plan); return plan


def run_plan(workspace: Path, concurrency: int, timeout: int) -> dict[str, Any]:
    workspace = workspace.resolve(); plan = load(workspace / PLAN_PATH); digest = sha_text(json.dumps(plan["tasks"], ensure_ascii=False, sort_keys=True, separators=(",", ":")))
    if plan.get("task_count") != 60 or plan.get("task_sha256") != digest: raise ValueError("Phase 10 plan count/hash mismatch")
    executable = shutil.which("pi.cmd") or shutil.which("pi")
    if not executable: raise RuntimeError("pi executable unavailable")
    output_root = workspace / RUN_ROOT; output_root.mkdir(parents=True, exist_ok=True); batch_id = f"batch-{int(time.time())}"; results = []; started = utc_now()
    with concurrent.futures.ThreadPoolExecutor(max_workers=concurrency) as pool:
        futures = {pool.submit(run_one, task, workspace, output_root, executable, timeout): task["id"] for task in plan["tasks"]}
        for future in concurrent.futures.as_completed(futures):
            try: results.append(future.result())
            except Exception as exc: results.append({"id": futures[future], "state": "runner-error", "exit_status": "failed", "parse_ok": False, "error": f"{type(exc).__name__}:{exc}"})
    summary = {"schema_version": "2.0", "batch_id": batch_id, "started_at": started, "ended_at": utc_now(), "model_request": MODEL, "concurrency": concurrency, "timeout_seconds": timeout, "selected_tasks": len(plan["tasks"]), "states": dict(sorted(__import__("collections").Counter(item["state"] for item in results).items())), "exit_statuses": dict(sorted(__import__("collections").Counter(item["exit_status"] for item in results).items())), "parse_ok": sum(bool(item["parse_ok"]) for item in results), "results": sorted(results, key=lambda item: item["id"])}
    write(output_root / "batches" / f"{batch_id}.json", summary); print(json.dumps({key: value for key, value in summary.items() if key != "results"}, ensure_ascii=False, sort_keys=True)); return summary


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__); sub = parser.add_subparsers(dest="command", required=True)
    plan = sub.add_parser("plan"); plan.add_argument("--workspace-root", type=Path, default=Path("."))
    run = sub.add_parser("run"); run.add_argument("--workspace-root", type=Path, default=Path(".")); run.add_argument("--concurrency", type=int, default=8); run.add_argument("--timeout", type=int, default=180)
    args = parser.parse_args()
    if args.command == "plan":
        value = build_plan(args.workspace_root); print(json.dumps({"ok": True, "task_count": value["task_count"], "counts": value["counts"], "task_sha256": value["task_sha256"]}, sort_keys=True)); return 0
    if not 1 <= args.concurrency <= 8: raise ValueError("concurrency must be 1..8")
    result = run_plan(args.workspace_root, args.concurrency, args.timeout); return 0 if result["states"].get("runner-error", 0) == 0 else 1


if __name__ == "__main__": raise SystemExit(main())
