#!/usr/bin/env python3
"""Compile bounded Phase 10 revision 3 from rejected revision 2."""
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
from pathlib import Path
from typing import Any

VERSION = "0.1.3-v2-candidate"
PHASE9_TREE = "7540c53426a5dff605c3f751fdaf105f52059ffbafce213d77c9c3db94214152"


def load(path: Path) -> Any: return json.loads(path.read_text(encoding="utf-8"))
def write(path: Path, value: Any) -> None: path.parent.mkdir(parents=True, exist_ok=True); path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
def sha(path: Path) -> str: return hashlib.sha256(path.read_bytes().replace(b"\r\n", b"\n")).hexdigest()


def compile_revision(workspace: Path) -> dict[str, Any]:
    workspace = workspace.resolve()
    if load(workspace / ".specs/capability-compiler-v2/phase-9/artifact-manifest.json")["tree_sha256"] != PHASE9_TREE: raise ValueError("Phase 9 tree drift")
    rejection = load(workspace / ".specs/capability-compiler-v2/phase-10/revision-2-rejection.json")
    if rejection.get("next_state") != "awaiting-explicit-authorization-for-bounded-revision-3": raise ValueError("Revision 3 authorization checkpoint missing")
    source = workspace / "evals/candidates/capability-compiler-v2/phase-10/revision-2"; root = workspace / "evals/candidates/capability-compiler-v2/phase-10/revision-3"
    if root.exists(): shutil.rmtree(root)
    shutil.copytree(source, root)
    changes = []
    def update(relative: str, value: Any, rationale: str) -> None:
        path = root / relative; before = sha(path); write(path, value); changes.append({"path": path.relative_to(workspace).as_posix(), "revision2_sha256": before, "revision3_sha256": sha(path), "rationale": rationale})

    p4_path = root / "phase-4/complete-ui-design-and-review.json"; p4 = load(p4_path); p4["version"] = VERSION; p4["evaluation_state"] = "not-run-phase-10-revision-3"
    p4["complete_route_planning"] = {
        "plan_all_required_steps": True,
        "execution_stops_at_control_points": True,
        "sequences": [
            {"condition": "no source repair is required after critique", "planned_route": ["rendered-critique", "explicit-human-approval", "release-gate"], "execution_stop": "explicit-human-approval"},
            {"condition": "source repair is accepted", "planned_route": ["rendered-critique", "explicit-human-approval", "separate-remediation-capability", "review-evidence", "rendered-critique", "explicit-human-approval", "release-gate"], "execution_stop": "explicit-human-approval"},
        ],
    }
    p4["gates"].append("complete route planning lists the required post-decision release-gate while actual execution stops at explicit-human-approval until the named human decision exists")
    update("phase-4/complete-ui-design-and-review.json", p4, "Separate complete route planning from execution stops so release-gate remains visible after human approval.")
    p4_eval_path = root / "phase-4/evaluation-plan.json"; p4_eval = load(p4_eval_path); p4_eval["version"] = VERSION; p4_eval["candidate_sha256"] = sha(p4_path); p4_eval["execution_state"] = "not-run-phase-10-revision-3"; update("phase-4/evaluation-plan.json", p4_eval, "Retarget Phase 4 checks to revision 3.")

    router_path = root / "phase-8/router.json"; router = load(router_path); router["version"] = VERSION; router["execution_state"] = "not-run-phase-10-revision-3"
    router["atomic_precedence"] = [
        {"condition": "one exact approved existing runtime needs readiness verification before a selected owner resumes", "target": "tool-runtime-readiness", "activation": "conditional-local-exec", "authorization_if_missing": "needs-input"},
        {"condition": "one exact approved project-local test runtime is missing", "target": "test-runtime-bootstrap", "activation": "disabled-pending-fresh-authorized-workspace-and-local-exec", "authorization_if_missing": "needs-input"},
        {"condition": "multiple runtime capabilities are needed or the support owner is unresolved", "target": "stage-15-tool-runtime-support", "activation": "conditional-routing-only", "authorization_if_missing": "needs-input"},
    ]
    router["gates"].append("route target ownership independently from activation authority: a missing project-local test runtime belongs to test-runtime-bootstrap even when activation remains disabled and needs-input")
    for target in router["composite_targets"]:
        if target["id"] == "verified-change-delivery-and-observation": target["path"] = "evals/candidates/capability-compiler-v2/phase-10/revision-3/phase-8/recipes/composites/verified-change-delivery-and-observation.json"
    update("phase-8/router.json", router, "Separate atomic target ownership from fresh activation authorization and reference the revised delivery composite.")

    delivery_source = workspace / "evals/candidates/capability-compiler-v2/phase-8/recipes/composites/verified-change-delivery-and-observation.json"
    delivery_target = root / "phase-8/recipes/composites/verified-change-delivery-and-observation.json"; delivery_target.parent.mkdir(parents=True, exist_ok=True); shutil.copy2(delivery_source, delivery_target)
    delivery = load(delivery_source); delivery["version"] = VERSION; delivery["status"] = "evaluating"; delivery["execution_state"] = "not-run-phase-10-revision-3"
    delivery["release_decision_control"] = {"executable": False, "permission_identity": "human-decision-only", "mutation_scope": "none", "required_before_remote_action": True, "required_fields": ["named human decision owner", "accepted release scope", "accepted redaction result", "accepted residual risk", "durable decision evidence identity and hash"], "does_not_authorize": ["push", "PR change", "comment", "merge", "deploy", "provider configuration", "rollback"]}
    delivery["human_checkpoints"][0] = "named human decision owner accepts release scope, redaction, residual risk, and records durable decision evidence; each upcoming remote action remains separately authorized"
    delivery["gates"].append("release readiness requires the named human decision owner and durable release-decision evidence before any separate per-action authorization can be considered")
    update("phase-8/recipes/composites/verified-change-delivery-and-observation.json", delivery, "Separate named lifecycle release decision from every remote action authorization.")

    mutation_root = root / "mutations"
    stage8 = load(workspace / "evals/candidates/capability-compiler-v2/phase-8/recipes/stages/stage-08-verification-quality.json"); review_mutant = json.loads(json.dumps(stage8)); review = next(item for item in review_mutant["steps"] if item["id"] == "independent-code-review"); review["permission_identity"] = "workspace-write"; review["mutation_scope"] = "authorized-workspace"; review["condition"] = "Independently review the change, edit source to fix every finding, and approve the repaired result."; review["hard_gates"] = ["Apply the smallest source patch for each accepted finding."]; review["outputs"].append("source remediation patch"); review_mutant["gates"] = [item for item in review_mutant["gates"] if "preserve candidate permission identity" not in item]; write(mutation_root / "P10-P8-review-write.json", review_mutant)
    delivery_mutant = json.loads(json.dumps(delivery)); delivery_mutant.pop("release_decision_control", None); delivery_mutant["human_checkpoints"] = [item for item in delivery_mutant["human_checkpoints"] if "named human decision owner" not in item]; delivery_mutant["gates"] = [item for item in delivery_mutant["gates"] if "named human decision owner" not in item]; write(mutation_root / "P10-P8-lifecycle-approval.json", delivery_mutant)
    p4_control = load(p4_path); p4_mutant = json.loads(json.dumps(p4_control)); p4_mutant.pop("complete_route_planning", None); p4_mutant["gates"] = [item for item in p4_mutant["gates"] if "complete route planning" not in item]; write(mutation_root / "P10-P4-complete-route-planning.json", p4_mutant)

    policy_path = root / "mutation-policy.json"; policy = load(policy_path); policy["version"] = VERSION; policy["phase10_behavioral_challenges"] = [item for item in policy["phase10_behavioral_challenges"] if item["id"] != "P10-P4-complete-route-planning"] + [{"id": "P10-P4-complete-route-planning", "target": "Phase 4 post-approval release-gate visibility in complete route planning", "causal": True, "mutant_path": "mutations/P10-P4-complete-route-planning.json"}]; update("mutation-policy.json", policy, "Add a causal complete-route-planning mutation and retain the revised review-write and lifecycle approval mutants.")

    for relative in ["phase-8/router-cases.json", "phase-8/router-holdout-cases.json", "phase-8/recipe-cases.json", "phase-8/recipe-holdout-cases.json", "phase-8/evaluation-plan.json"]:
        path = root / relative; doc = load(path); doc["execution_state"] = "not-run-phase-10-revision-3"; update(relative, doc, "Advance targeted fixture state to revision 3 without changing expected outcomes.")
    for relative in ["phase-8/recipes/composites/full-software-lifecycle.json", "phase-8/recipes/composites/feature-build-and-verify.json", "phase-8/recipes/stages/stage-05-experience-design.json", "phase-8/recipes/stages/stage-15-tool-runtime-support.json"]:
        path = root / relative; doc = load(path); doc["version"] = VERSION; doc["execution_state"] = "not-run-phase-10-revision-3"; update(relative, doc, "Advance unchanged accepted revision-2 semantics to revision 3.")

    patch = load(root / "patch-ledger.json"); patch["version"] = VERSION; patch["base_revision"] = "0.1.2-v2-candidate"; patch["revision3_change_count"] = len(changes); patch["revision3_records"] = changes; patch["revision3_authorization"] = "user message: 继续"; write(root / "patch-ledger.json", patch)
    return {"ok": True, "version": VERSION, "changes": len(changes), "atomic_skill_revisions": 0}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__); parser.add_argument("--workspace-root", type=Path, default=Path(".")); args = parser.parse_args(); print(json.dumps(compile_revision(args.workspace_root), ensure_ascii=False, sort_keys=True)); return 0


if __name__ == "__main__": raise SystemExit(main())
