#!/usr/bin/env python3
"""Fail-closed Phase 11 real-project acceptance evidence gate."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

PHASE10_TREE = "7fd6640a563789257da77e1015be3f37033a3baf40ecaf9a4b9fa1fde7828d56"
RUNTIME_TREE = "708ea6b7ec0b169bcb7d2a36e77f5d6df9a3ff9a9df2446fee978419e7af7266"
PACKAGE_SHA = "8fb653c637294f2a10edd3f9d540d6dabf74a9d1d1dded71e6ab3c0445cf3309"
PATCH_SHA = "15bf934015d39cdb2f0bb04185216474ba7641ceeec8293727c9c47907040a7f"
PACKAGE_TREE = "f2944d37e772da78b818a3210fe84fdea536a3be04b6c2f099f4c132840a1566"
CASE = Path("evals/runs/capability-compiler-v2/phase-11/benchshare-v1")


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def parse_events(path: Path) -> dict[str, Any]:
    events = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    calls = []
    for event in events:
        for part in event.get("message", {}).get("content", []):
            if part.get("type") in {"toolCall", "tool_call"}:
                calls.append({"name": part.get("name") or part.get("toolName"), "args": part.get("arguments") or part.get("input") or {}})
    ends = [event["message"] for event in events if event.get("type") == "message_end" and event.get("message", {}).get("role") == "assistant"]
    if not ends:
        raise ValueError(f"no assistant message_end: {path}")
    message = ends[-1]
    text = "".join(part.get("text", "") for part in message.get("content", []) if part.get("type") == "text")
    return {"calls": calls, "message": message, "text": text}


def runtime_tree(workspace: Path) -> str:
    root = workspace / CASE / "workspace/benchshare"
    artifacts = []
    for path in sorted(root.rglob("*")):
        if path.is_file() and "__pycache__" not in path.parts:
            artifacts.append((path.relative_to(root.parent).as_posix(), sha(path)))
    return hashlib.sha256("".join(f"{name}\0{digest}\n" for name, digest in artifacts).encode()).hexdigest()


def verify(workspace: Path) -> dict[str, Any]:
    workspace = workspace.resolve(); case = workspace / CASE; checks = []
    def add(name: str, errors: list[str]) -> None: checks.append({"name": name, "ok": not errors, "errors": errors})

    identity_errors = []
    if load(workspace / ".specs/capability-compiler-v2/phase-10/artifact-manifest.json").get("tree_sha256") != PHASE10_TREE: identity_errors.append("Phase 10 tree drift")
    if runtime_tree(workspace) != RUNTIME_TREE: identity_errors.append("BenchShare runtime tree drift")
    review = load(workspace / "curation/v2/phase-10/semantic-review.json")
    if review.get("release_disposition") != "eligible-for-phase-11-real-project-validation-not-released" or review.get("final_user_release_approval") is not False: identity_errors.append("Phase 10 candidate boundary changed")
    add("frozen-phase-10-and-runtime-identities", identity_errors)

    decision_errors = []; decision = load(workspace / "curation/v2/phase-11/product-decision.json")
    if decision.get("case_id") != "benchshare-v1" or decision.get("product", {}).get("selected_by") != "user" or decision.get("visual_direction", {}).get("id") != "municipal-wayfinding" or decision.get("visual_direction", {}).get("selected_by") != "user": decision_errors.append("product or visual human checkpoint mismatch")
    if decision.get("authority", {}).get("remote_actions_authorized") is not False or decision.get("authority", {}).get("final_release_approval") is not False: decision_errors.append("decision authority widened")
    required_contracts = ["PRODUCT.md", "DISCOVERY.md", "STRATEGY.md", "REQUIREMENTS.md", "DESIGN-BRIEF.md", "ARCHITECTURE.md", "IMPLEMENTATION-PLAN.md", "DESIGN.md", "TEST-MAP.md", "OPERATIONS.md", "RELEASE-NOTES.md", "RETROSPECTIVE.md"]
    if any(not (case / "workspace" / name).is_file() for name in required_contracts): decision_errors.append("lifecycle contract missing")
    add("human-checkpoints-and-lifecycle-contracts", decision_errors)

    lifecycle_errors = []; lifecycle = load(case / "evidence/lifecycle-execution.json"); stages = lifecycle.get("stages", [])
    if [item.get("stage") for item in stages] != list(range(1, 16)): lifecycle_errors.append("lifecycle stages not exactly 1..15")
    if any(not item.get("condition") for item in stages): lifecycle_errors.append("stage condition missing")
    stage11 = next((item for item in stages if item.get("stage") == 11), {})
    if stage11.get("selected") != [] or stage11.get("activation") != "disabled-pending-current-authorization" or not stage11.get("skipped"): lifecycle_errors.append("remote stage not fail-closed")
    if lifecycle.get("remote_actions") != [] or lifecycle.get("provider_actions") != [] or lifecycle.get("production_actions") != [] or lifecycle.get("final_human_release_decision") != "pending-phase-12": lifecycle_errors.append("lifecycle claims action or approval")
    add("conditional-lifecycle-and-authority-boundaries", lifecycle_errors)

    model_errors = []
    model_specs = [
        ("implementation-writer/attempt-2-command/stdout.txt", {"read", "edit", "write"}, "completed", False),
        ("remediation/attempt-1-command/stdout.txt", {"read", "edit"}, "completed", False),
        ("independent-review/attempt-1-command/stdout.txt", {"read"}, "findings", True),
        ("independent-review/confirmation-attempt-1-command/stdout.txt", {"read"}, "pass", True),
    ]
    for relative, expected_tools, expected_verdict, json_output in model_specs:
        path = case / "evidence" / relative
        try:
            evidence = parse_events(path); message = evidence["message"]; tools = {call["name"] for call in evidence["calls"]}
            if message.get("provider") != "router9-qoder" or message.get("model") != "cx/gpt-5.6-sol" or message.get("stopReason") != "stop": model_errors.append(f"{relative}: model identity/stop mismatch")
            if tools != expected_tools: model_errors.append(f"{relative}: tools {sorted(tools)} != {sorted(expected_tools)}")
            for call in evidence["calls"]:
                target = call["args"].get("path") if isinstance(call["args"], dict) else None
                if target and (Path(target).is_absolute() or ".." in Path(target).parts): model_errors.append(f"{relative}: out-of-workspace path {target}")
            if json_output:
                value = json.loads(evidence["text"])
                if value.get("verdict") != expected_verdict or value.get("would_modify_source") is not False: model_errors.append(f"{relative}: review output mismatch")
            elif "Host verification remains pending" not in evidence["text"] and relative.startswith("implementation"):
                model_errors.append("implementation writer claimed completion without host boundary")
        except Exception as exc: model_errors.append(f"{relative}: {type(exc).__name__}:{exc}")
    # No-tools black-box sessions must contain no tool calls and exact JSON.
    for attempt, verdict in [("attempt-1-command", "findings"), ("attempt-2-command", "pass")]:
        relative = f"blackbox-qa/{attempt}/stdout.txt"
        try:
            evidence = parse_events(case / "evidence" / relative); value = json.loads(evidence["text"])
            if evidence["calls"] or value.get("verdict") != verdict or value.get("would_modify_source") is not False or value.get("would_approve_release") is not False: model_errors.append(f"{relative}: no-tools/verdict boundary mismatch")
        except Exception as exc: model_errors.append(f"{relative}: {type(exc).__name__}:{exc}")
    add("model-identities-tools-and-role-separation", model_errors)

    test_errors = []
    green = load(case / "evidence/commands/remediation-tests-green/receipt.json")
    green_stdout = (case / "evidence/commands/remediation-tests-green/stdout.txt").read_text(encoding="utf-8")
    if green.get("exit_code") != 0 or "14 passed" not in green_stdout: test_errors.append("current host tests not 14/14")
    if load(case / "evidence/commands/compileall-2/receipt.json").get("exit_code") != 0: test_errors.append("current compileall failed")
    red = load(case / "evidence/commands/review-regressions-red/receipt.json")
    if red.get("exit_code") != 1 or "5 failed, 9 passed" not in (case / "evidence/commands/review-regressions-red/stdout.txt").read_text(encoding="utf-8"): test_errors.append("regression RED evidence missing")
    confirmation = load(case / "evidence/independent-review/confirmation-output.json")
    if confirmation.get("verdict") != "pass" or set(confirmation.get("confirmations", {}).values()) != {"closed"} or confirmation.get("findings") != []: test_errors.append("independent review findings not closed")
    add("tests-red-green-and-independent-code-confirmation", test_errors)

    browser_errors = []; browser = load(case / "evidence/browser/iteration-3/report.json")
    if browser.get("runtime_tree_sha256") != RUNTIME_TREE or browser.get("passed") is not True or browser.get("failures") != [] or browser.get("unexpected_console_errors") != [] or browser.get("page_errors") != [] or len(browser.get("screenshots", [])) != 12: browser_errors.append("browser iteration 3 status/count mismatch")
    required_checks = ["keyboard_coordinator_approve_and_conflict", "keyboard_coordinator_reject", "keyboard_member_cancel", "keyboard_member_request", "member_approval_controls_absent", "member_approve_denied", "mobile_no_session_no_overflow", "submitting_disabled", "reduced_motion_media"]
    for name in required_checks:
        value = browser.get("checks", {}).get(name)
        if name == "member_approve_denied":
            if value != {"status": 403, "code": "forbidden"}: browser_errors.append(f"browser check failed: {name}")
        elif value is not True: browser_errors.append(f"browser check failed: {name}")
    for item in browser.get("screenshots", []):
        path = case / "evidence/browser/iteration-3" / item.get("path", "missing")
        if not path.is_file() or sha(path) != item.get("sha256") or path.stat().st_size != item.get("bytes") or item.get("runtime_tree_sha256") != RUNTIME_TREE: browser_errors.append(f"screenshot evidence invalid: {item.get('name')}")
    rendered = load(case / "evidence/browser/rendered-review.json"); qa = load(case / "evidence/blackbox-qa/qa-output-iteration-3.json")
    if rendered.get("iteration") != 3 or len(rendered.get("opened_screenshots", [])) != 12 or rendered.get("visual_verdict") != "accepted-for-phase-11-local-validation" or rendered.get("final_release_approval") is not False: browser_errors.append("rendered review mismatch")
    if qa.get("verdict") != "pass" or qa.get("findings") != [] or not all(qa.get("evidence_checks", {}).values()) or qa.get("would_approve_release") is not False: browser_errors.append("black-box QA confirmation mismatch")
    add("real-browser-rendering-accessibility-and-blackbox-qa", browser_errors)

    performance_errors = []; performance = load(case / "evidence/performance/iteration-1/report.json")
    if performance.get("runtime_tree_sha256") != RUNTIME_TREE or performance.get("passed") is not True or not all(performance.get("checks", {}).values()) or performance.get("failed_runs_deleted") != 0: performance_errors.append("performance aggregate failed")
    metrics = performance.get("metrics", {})
    if metrics.get("health", {}).get("p95_ms", 999) > 100 or metrics.get("reservation_list", {}).get("p95_ms", 999) > 100 or metrics.get("reservation_create", {}).get("p95_ms", 999) > 250: performance_errors.append("predeclared p95 threshold missed")
    concurrency = performance.get("concurrency", {})
    if (concurrency.get("approved_responses"), concurrency.get("conflicts"), concurrency.get("server_errors"), concurrency.get("approved_rows"), concurrency.get("approval_audit_events"), concurrency.get("integrity_check")) != (1, 9, 0, 1, 1, "ok"): performance_errors.append("ten-way concurrency invariant failed")
    add("performance-reliability-and-concurrency", performance_errors)

    package_errors = []; package = case / "package"; receipt = load(package / "package-receipt.json"); manifest = load(package / "benchshare-v1/PACKAGE-MANIFEST.json")
    if receipt.get("package_sha256") != PACKAGE_SHA or sha(package / "benchshare-v1.zip") != PACKAGE_SHA or receipt.get("patch_sha256") != PATCH_SHA or sha(package / "benchshare-v1.patch") != PATCH_SHA or receipt.get("tree_sha256") != PACKAGE_TREE or manifest.get("tree_sha256") != PACKAGE_TREE: package_errors.append("package/patch identity mismatch")
    recomputed = []
    for item in manifest.get("files", []):
        path = package / "benchshare-v1" / item.get("path", "missing")
        if not path.is_file() or sha(path) != item.get("sha256") or path.stat().st_size != item.get("bytes"): package_errors.append(f"package file mismatch: {item.get('path')}")
        else: recomputed.append(f"{item['path']}\0{item['sha256']}\n")
    if hashlib.sha256("".join(recomputed).encode()).hexdigest() != PACKAGE_TREE: package_errors.append("package tree recompute mismatch")
    compare = load(case / "evidence/commands/package-repro-compare/receipt.json")
    if compare.get("exit_code") != 0 or '"ok": true' not in (case / "evidence/commands/package-repro-compare/stdout.txt").read_text(encoding="utf-8").lower(): package_errors.append("reproducible build evidence failed")
    verification = load(case / "evidence/package-verification/iteration-1/report.json")
    if verification.get("passed") is not True or not all(verification.get("checks", {}).values()) or verification.get("remote_actions") != []: package_errors.append("fresh package/patch/restore verification failed")
    if manifest.get("third_party_runtime_dependencies") != [] or manifest.get("bundled_secrets") != [] or manifest.get("bundled_databases") != []: package_errors.append("package dependency/secret/database boundary failed")
    add("reproducible-package-patch-and-restore", package_errors)

    failure_errors = []
    expected = [
        case / "evidence/implementation-writer/attempt-1-command/launch-failure.json",
        case / "evidence/commands/verify-approved-inputs-after-writer/finding.json",
        case / "evidence/commands/review-regressions-red/receipt.json",
        case / "evidence/browser/iteration-1/report.json",
        case / "evidence/blackbox-qa/qa-output-iteration-2.json",
        case / "package/iteration-1-finding.json",
        case / "package/iteration-1/package-receipt.json",
    ]
    if any(not path.is_file() for path in expected): failure_errors.append("failed/calibration evidence missing")
    if load(case / "evidence/browser/iteration-1/report.json").get("passed") is not False: failure_errors.append("browser failure overwritten")
    if load(case / "evidence/blackbox-qa/qa-output-iteration-2.json").get("verdict") != "findings": failure_errors.append("blackbox failure overwritten")
    add("failed-attempts-and-rejected-evidence-preserved", failure_errors)

    semantic_errors = []; semantic = load(workspace / "curation/v2/phase-11/semantic-review.json")
    if semantic.get("status") != "passed-local-end-to-end-validation-pending-final-approval" or semantic.get("release_disposition") != "eligible-for-phase-12-final-human-approval-not-released": semantic_errors.append("Phase 11 semantic status mismatch")
    authority = semantic.get("authority", {})
    if any(authority.get(name) for name in ["remote_actions", "provider_actions", "production_actions"]) or authority.get("final_user_release_approval") is not False or authority.get("deployment_performed") is not False: semantic_errors.append("semantic review claims unauthorized action/approval")
    if semantic.get("delivery", {}).get("released") is not False or semantic.get("accepted_candidate", {}).get("released") is not False: semantic_errors.append("semantic review claims release")
    add("phase-11-parent-review-not-final-approval", semantic_errors)

    errors = [f"{check['name']}: {error}" for check in checks for error in check["errors"]]
    return {
        "gate": "capability-compiler-v2-phase-11", "ok": not errors,
        "phase_11_complete": not errors, "eligible_for_phase_12": not errors,
        "final_user_release_approval": False, "released": False,
        "checks": checks,
        "counts": {"application_tests": 14, "independent_code_findings_closed": 6, "browser_screenshots": 12, "blackbox_findings_closed": 2, "performance_runs": 130, "concurrent_approvals": 10, "package_files": len(manifest.get("files", [])), "remote_actions": 0},
        "identities": {"phase10_tree_sha256": PHASE10_TREE, "runtime_tree_sha256": RUNTIME_TREE, "package_sha256": PACKAGE_SHA, "patch_sha256": PATCH_SHA, "package_tree_sha256": PACKAGE_TREE},
        "errors": errors,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__); parser.add_argument("--workspace-root", type=Path, default=Path(".")); parser.add_argument("--output", type=Path); args = parser.parse_args(); result = verify(args.workspace_root)
    if args.output:
        path = args.output if args.output.is_absolute() else args.workspace_root / args.output; path.parent.mkdir(parents=True, exist_ok=True); path.write_text(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps(result, ensure_ascii=False, sort_keys=True)); return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
