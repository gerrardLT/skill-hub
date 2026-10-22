#!/usr/bin/env python3
"""Compile Phase 10 revision 2 from rejected revision 1 plus user taxonomy adjudication."""
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
from pathlib import Path
from typing import Any

VERSION = "0.1.2-v2-candidate"
PHASE9_TREE = "7540c53426a5dff605c3f751fdaf105f52059ffbafce213d77c9c3db94214152"


def load(path: Path) -> Any: return json.loads(path.read_text(encoding="utf-8"))
def write(path: Path, value: Any) -> None: path.parent.mkdir(parents=True, exist_ok=True); path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
def sha(path: Path) -> str: return hashlib.sha256(path.read_bytes().replace(b"\r\n", b"\n")).hexdigest()


def compile_revision(workspace: Path) -> dict[str, Any]:
    workspace = workspace.resolve()
    if load(workspace / ".specs/capability-compiler-v2/phase-9/artifact-manifest.json")["tree_sha256"] != PHASE9_TREE: raise ValueError("Phase 9 tree drift")
    decision = load(workspace / "curation/v2/phase-10/renderer-taxonomy-decision.json")
    if decision.get("selected_option") != "revise_fixture_fail_closed": raise ValueError("renderer taxonomy decision missing")
    source = workspace / "evals/candidates/capability-compiler-v2/phase-10/revision-1"; root = workspace / "evals/candidates/capability-compiler-v2/phase-10/revision-2"
    if root.exists(): shutil.rmtree(root)
    shutil.copytree(source, root)
    changes = []
    def update(relative: str, value: Any, rationale: str) -> None:
        path = root / relative; before = sha(path); write(path, value); changes.append({"path": path.relative_to(workspace).as_posix(), "revision1_sha256": before, "revision2_sha256": sha(path), "rationale": rationale})

    p4_path = root / "phase-4/complete-ui-design-and-review.json"; p4 = load(p4_path); p4["version"] = VERSION; p4["evaluation_state"] = "not-run-phase-10-revision-2"
    p4["feedback_routes"] = [
        {"artifact": "accepted visual findings", "authorization": "explicit-human-approval", "from": "rendered-critique", "to": "explicit-human-approval", "then": "separate-remediation-capability", "repair_target": "visual-language", "recapture_target": "review-evidence"},
        {"artifact": "accepted responsive findings", "authorization": "explicit-human-approval", "from": "rendered-critique", "to": "explicit-human-approval", "then": "separate-remediation-capability", "repair_target": "responsive-composition", "recapture_target": "review-evidence"},
        {"artifact": "accepted interaction findings", "authorization": "explicit-human-approval", "from": "rendered-critique", "to": "explicit-human-approval", "then": "separate-remediation-capability", "repair_target": "interaction-states", "recapture_target": "review-evidence"},
        {"artifact": "recapture requirements after authorized repair", "authorization": "explicit-human-approval", "from": "separate-remediation-capability", "to": "review-evidence", "then": "rendered-critique", "repair_target": "authorized-external-remediator", "recapture_target": "release-gate"},
    ]
    update("phase-4/complete-ui-design-and-review.json", p4, "Remove every direct review-to-writer feedback bypass and route repair through both non-executable control points.")
    p4_eval_path = root / "phase-4/evaluation-plan.json"; p4_eval = load(p4_eval_path); p4_eval["version"] = VERSION; p4_eval["candidate_sha256"] = sha(p4_path); p4_eval["execution_state"] = "not-run-phase-10-revision-2"; update("phase-4/evaluation-plan.json", p4_eval, "Retarget evaluation to revision 2 hash.")

    router_path = root / "phase-8/router.json"; router = load(router_path); router["version"] = VERSION; router["execution_state"] = "not-run-phase-10-revision-2"
    split = next(item for item in router["safety_dispositions"] if item["id"] == "split-independent-review-human-approval-remediation")
    split["match"] = "one request explicitly asks the same reviewer or QA identity to mutate source, accept its own fix, self-approve, or release; a governed composite with separate identities and human-owned disposition does not match"
    router["atomic_precedence"] = [
        {"condition": "one exact approved existing runtime needs readiness verification before a selected owner resumes", "target": "tool-runtime-readiness"},
        {"condition": "one exact approved project-local test runtime is missing and setup is authorized", "target": "test-runtime-bootstrap"},
        {"condition": "multiple runtime capabilities are needed or the support owner is unresolved", "target": "stage-15-tool-runtime-support"},
    ]
    router["gates"].append("evaluate atomic_precedence before stage targets; exact readiness or test-bootstrap ownership cannot be widened to stage 15")
    update("phase-8/router.json", router, "Narrow review/repair safety matching and encode runtime atomic precedence as structured routing data.")

    full_path = root / "phase-8/recipes/composites/full-software-lifecycle.json"; full = load(full_path); full["version"] = VERSION; full["execution_state"] = "not-run-phase-10-revision-2"
    full["failure_policy"]["resume_validation"] = ["current input identities and hashes match", "current output identities and hashes match", "all stage and handoff gates re-pass", "decision and action authority remains current and exact", "no invalidation trigger fired", "all dependent evidence remains current"]
    update("phase-8/recipes/composites/full-software-lifecycle.json", full, "Require current checkpoint revalidation before resume.")
    feature_path = root / "phase-8/recipes/composites/feature-build-and-verify.json"; feature = load(feature_path); feature["version"] = VERSION; feature["execution_state"] = "not-run-phase-10-revision-2"; feature["failure_policy"]["resume_validation"] = list(full["failure_policy"]["resume_validation"]); update("phase-8/recipes/composites/feature-build-and-verify.json", feature, "Require current checkpoint revalidation before resume.")

    holdout_path = root / "phase-8/recipe-holdout-cases.json"; holdouts = load(holdout_path); holdouts["execution_state"] = "not-run-phase-10-revision-2"; renderer = next(item for item in holdouts["cases"] if item["id"] == "V2-P8-RECIPE-HOLDOUT-stage15"); renderer["assertion"] = "When an approved renderer is missing and no existing atomic setup owner is authorized, stage 15 returns blocked-no-authorized-runtime-owner and does not install, widen another capability, or grant lifecycle approval."; update("phase-8/recipe-holdout-cases.json", holdouts, "Apply user adjudication: fail closed instead of inventing renderer bootstrap authority.")
    for relative in ["phase-8/router-cases.json", "phase-8/router-holdout-cases.json", "phase-8/recipe-cases.json", "phase-8/evaluation-plan.json"]:
        path = root / relative; doc = load(path); doc["execution_state"] = "not-run-phase-10-revision-2"; update(relative, doc, "Advance revision execution state without changing frozen expected behavior.")

    stage15_path = root / "phase-8/recipes/stages/stage-15-tool-runtime-support.json"; stage15 = load(stage15_path); stage15["version"] = VERSION; stage15["execution_state"] = "not-run-phase-10-revision-2"; update("phase-8/recipes/stages/stage-15-tool-runtime-support.json", stage15, "Advance user-approved fail-closed support contract to revision 2.")
    stage5_path = root / "phase-8/recipes/stages/stage-05-experience-design.json"; stage5 = load(stage5_path); stage5["version"] = VERSION; stage5["execution_state"] = "not-run-phase-10-revision-2"; update("phase-8/recipes/stages/stage-05-experience-design.json", stage5, "Advance explicit UI skip gate to revision 2.")

    mutation_root = root / "mutations"
    p4_control = load(p4_path); p4_mutant = json.loads(json.dumps(p4_control)); p4_mutant["control_points"] = []; p4_mutant["edges"] = [item for item in p4_mutant["edges"] if item["from"] not in {"explicit-human-approval", "separate-remediation-capability"} and item["to"] not in {"explicit-human-approval", "separate-remediation-capability"}]; p4_mutant["feedback_routes"] = [{"artifact": item["artifact"], "authorization": "none", "from": "rendered-critique", "to": item.get("repair_target", "visual-language")} for item in p4_control["feedback_routes"][:3]]; write(mutation_root / "P10-P4-human-control-points.json", p4_mutant)
    full_control = load(full_path); no_invalidation = json.loads(json.dumps(full_control)); no_invalidation["failure_policy"]["invalidate_downstream_on"] = [item for item in no_invalidation["failure_policy"]["invalidate_downstream_on"] if item != "source capability re-runs"]; [handoff.update({"invalidation": [item for item in handoff["invalidation"] if item != "source capability re-runs"]}) for handoff in no_invalidation["handoffs"]]; write(mutation_root / "P10-P8-invalidation.json", no_invalidation)
    no_resume = json.loads(json.dumps(full_control)); no_resume["failure_policy"].pop("resume_validation", None); write(mutation_root / "P10-P8-resume-validation.json", no_resume)
    stage11 = load(workspace / "evals/candidates/capability-compiler-v2/phase-8/recipes/stages/stage-11-deployment-change.json"); remote = json.loads(json.dumps(stage11)); push = next(item for item in remote["steps"] if item["id"] == "remote-git-push"); push["activation"] = "conditional"; push["condition"] = "Select whenever pushing would help."; push["inputs"] = ["A local branch and remote name."]; push["hard_gates"] = ["Do not force push."]; remote["gates"] = [item for item in remote["gates"] if "fresh current authorization" not in item and "preserve candidate permission identity" not in item]; write(mutation_root / "P10-P8-remote-activation.json", remote)

    policy_path = root / "mutation-policy.json"; policy = load(policy_path); policy["version"] = VERSION; policy["phase10_behavioral_challenges"] = [item for item in policy["phase10_behavioral_challenges"] if item["id"] != "P10-P8-remote-activation"] + [{"id": "P10-P8-remote-activation", "target": "Phase 8 complete fresh/exact remote authorization stop", "causal": True, "mutant_path": "mutations/P10-P8-remote-activation.json"}, {"id": "P10-P8-resume-validation", "target": "Phase 8 current checkpoint revalidation before resume", "causal": True, "mutant_path": "mutations/P10-P8-resume-validation.json"}]; update("mutation-policy.json", policy, "Use a causally discriminating remote-authorization mutation and add resume-validation mutation.")

    patch = load(root / "patch-ledger.json"); patch["version"] = VERSION; patch["base_revision"] = "0.1.1-v2-candidate"; patch["revision2_change_count"] = len(changes); patch["revision2_records"] = changes; patch["user_decision"] = "curation/v2/phase-10/renderer-taxonomy-decision.json"; write(root / "patch-ledger.json", patch)
    return {"ok": True, "version": VERSION, "changes": len(changes), "atomic_skill_revisions": 0, "user_decision": decision["id"]}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__); parser.add_argument("--workspace-root", type=Path, default=Path(".")); args = parser.parse_args(); print(json.dumps(compile_revision(args.workspace_root), ensure_ascii=False, sort_keys=True)); return 0


if __name__ == "__main__": raise SystemExit(main())
