#!/usr/bin/env python3
"""Compile the bounded Phase 10 Recipe/router revision without touching frozen candidates."""
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
from pathlib import Path
from typing import Any

VERSION = "0.1.1-v2-candidate"
PHASE4_TREE = "968fd1e2175bdc35d77a4d9025a88ab35e5f096fba353137dbf9770e030d4695"
PHASE8_TREE = "501d9cddfdc44fec4af8f17470c99b57b48ffced977e0fa7086cce568fa92f66"
PHASE9_TREE = "7540c53426a5dff605c3f751fdaf105f52059ffbafce213d77c9c3db94214152"


def load(path: Path) -> Any: return json.loads(path.read_text(encoding="utf-8"))
def write(path: Path, value: Any) -> None: path.parent.mkdir(parents=True, exist_ok=True); path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
def sha(path: Path) -> str: return hashlib.sha256(path.read_bytes().replace(b"\r\n", b"\n")).hexdigest()


def compile_revision(workspace: Path) -> dict[str, Any]:
    workspace = workspace.resolve()
    for phase, expected in [(4, PHASE4_TREE), (8, PHASE8_TREE), (9, PHASE9_TREE)]:
        if load(workspace / f".specs/capability-compiler-v2/phase-{phase}/artifact-manifest.json")["tree_sha256"] != expected: raise ValueError(f"Phase {phase} tree drift")
    root = workspace / "evals/candidates/capability-compiler-v2/phase-10/revision-1"
    if root.exists(): shutil.rmtree(root)
    root.mkdir(parents=True)
    patch_records = []

    def save(relative: str, value: Any, source: Path, rationale: str) -> None:
        target = root / relative; write(target, value); patch_records.append({"path": target.relative_to(workspace).as_posix(), "source_path": source.relative_to(workspace).as_posix(), "source_sha256": sha(source), "revised_sha256": sha(target), "rationale": rationale})

    p4_source = workspace / "evals/candidates/capability-compiler-v2/phase-4/recipes/complete-ui-design-and-review.json"; p4 = load(p4_source); p4["version"] = VERSION; p4["status"] = "evaluating"; p4["evaluation_state"] = "not-run-phase-10-targeted"
    p4["control_points"] = [
        {"id": "explicit-human-approval", "executable": False, "permission_identity": "human-decision-only", "mutation_scope": "none", "condition": "a reviewer finding, prototype choice, residual risk, remediation scope, or release disposition requires a named human owner decision", "outputs": ["decision owner", "accepted or rejected finding", "bounded remediation authorization or disposition", "decision evidence"]},
        {"id": "separate-remediation-capability", "executable": False, "permission_identity": "route-only", "mutation_scope": "none", "condition": "a human accepted a finding and separately authorized an exact source repair scope", "outputs": ["exact remediator capability identity", "bounded source scope", "stale evidence invalidation", "required recapture handoff"]},
    ]
    p4["edges"].extend([
        {"from": "rendered-critique", "to": "explicit-human-approval", "condition": "a finding, taste choice, risk acceptance, remediation scope, or release disposition needs a human decision"},
        {"from": "explicit-human-approval", "to": "separate-remediation-capability", "condition": "the named human owner accepts a finding and authorizes exact source remediation"},
        {"from": "separate-remediation-capability", "to": "review-evidence", "condition": "authorized repair completed, stale evidence was invalidated, and current captures must be reacquired"},
        {"from": "explicit-human-approval", "to": "release-gate", "condition": "no source repair is required and the named owner requests final evidence-based disposition"},
    ])
    p4["gates"].extend(["human approval is a non-executable control point and never grants the reviewer source-write authority", "accepted findings route to a separate remediator identity; repaired UI invalidates stale evidence and must be recaptured"])
    save("phase-4/complete-ui-design-and-review.json", p4, p4_source, "Make human approval and separate remediation first-class non-executable route control points.")
    for name in ["recipe-cases.json", "recipe-holdout-cases.json"]:
        source = p4_source.parent / name; save(f"phase-4/{name}", load(source), source, "Preserve frozen Phase 4 route fixtures for targeted rerun.")
    p4_eval = load(p4_source.parent / "evaluation-plan.json"); p4_eval["version"] = VERSION; p4_eval["status"] = "planned"; p4_eval["execution_state"] = "not-run-phase-10-targeted"; p4_eval["base_candidate_sha256"] = p4_eval.pop("candidate_sha256"); p4_eval["candidate_sha256"] = sha(root / "phase-4/complete-ui-design-and-review.json")
    save("phase-4/evaluation-plan.json", p4_eval, p4_source.parent / "evaluation-plan.json", "Retarget frozen checks to revision 1.")

    p8 = workspace / "evals/candidates/capability-compiler-v2/phase-8"; stage5_source = p8 / "recipes/stages/stage-05-experience-design.json"; stage5 = load(stage5_source); stage5["version"] = VERSION; stage5["execution_state"] = "not-run-phase-10-targeted"; stage5["gates"].append("experience-design steps may be skipped as not applicable only when approved requirements explicitly state that the bounded change has no user-facing surface, user-visible state, content, accessibility, or interaction effect")
    stage5["skip_contract"] = {"required_evidence": "approved requirements explicitly state no user-facing surface or effect", "default_without_evidence": "needs-input", "never_infer_from": ["backend-only label", "file paths", "absence of UI files in the proposed diff"]}
    save("phase-8/recipes/stages/stage-05-experience-design.json", stage5, stage5_source, "Require explicit approved no-user-facing-surface evidence before skipping experience design.")

    stage15_source = p8 / "recipes/stages/stage-15-tool-runtime-support.json"; stage15 = load(stage15_source); stage15["version"] = VERSION; stage15["execution_state"] = "not-run-phase-10-targeted"
    stage15["support_routes"] = [
        {"condition": "one approved project-local test runtime is missing", "target": "test-runtime-bootstrap", "authorization": "fresh authorized-workspace and local-exec authorization", "return_to_blocked_owner": True, "lifecycle_approval": False},
        {"condition": "one existing required tool or renderer needs version, invocation, capability, or safe-failure verification", "target": "tool-runtime-readiness", "authorization": "local-exec only", "return_to_blocked_owner": True, "lifecycle_approval": False},
        {"condition": "one installed workflow runtime needs a pinned upgrade", "target": "workflow-runtime-upgrade", "authorization": "fresh local-system authorization with backup and rollback", "return_to_blocked_owner": True, "lifecycle_approval": False},
        {"condition": "an approved document renderer is ready and one source must be rendered and validated", "target": "document-rendering-and-validation", "authorization": "declared workspace-write-local-exec artifact scope", "return_to_blocked_owner": True, "lifecycle_approval": False},
        {"condition": "no existing atomic support owner safely covers the missing runtime setup", "target": "blocked-no-authorized-runtime-owner", "authorization": "none", "return_to_blocked_owner": False, "lifecycle_approval": False},
    ]
    stage15["gates"].extend(["a missing runtime never authorizes stage 15 itself to install or upgrade it; select the narrow existing atomic owner and require that owner's exact fresh authorization", "after readiness, setup, upgrade, or rendering evidence is verified, return to the original blocked owner; support evidence never grants lifecycle approval"])
    save("phase-8/recipes/stages/stage-15-tool-runtime-support.json", stage15, stage15_source, "Make missing-runtime owner selection, authorization, and return semantics explicit.")

    revised_stage_refs = {"stage:05-experience-design": f"stage-05-experience-design@{VERSION}"}
    for recipe_name in ["feature-build-and-verify", "full-software-lifecycle"]:
        source = p8 / f"recipes/composites/{recipe_name}.json"; doc = load(source); doc["version"] = VERSION; doc["execution_state"] = "not-run-phase-10-targeted"
        for item in doc["stage_steps"]:
            if item["stage_id"] in revised_stage_refs: item["recipe_ref"] = revised_stage_refs[item["stage_id"]]
        doc["support_stage"]["recipe_ref"] = f"stage-15-tool-runtime-support@{VERSION}"
        save(f"phase-8/recipes/composites/{recipe_name}.json", doc, source, "Reference revised experience-design and tool-support stage contracts.")

    router_source = p8 / "router.json"; router = load(router_source); router["version"] = VERSION; router["execution_state"] = "not-run-phase-10-targeted"
    router["safety_dispositions"] = [
        {"id": "blocked-data-governance", "match": "customer, proprietary, recorded, or external-Judge data lacks consent, minimization, redaction, retention, transfer, access, deletion, or incident terms", "status": "blocked", "executable": False, "next_route": "stage-01-governance-intake", "authorization_propagates": False},
        {"id": "split-independent-review-human-approval-remediation", "match": "one request combines independent review, source repair, self-approval, or release", "status": "needs-input", "executable": False, "next_route": "independent review then explicit human approval then a separate remediator", "authorization_propagates": False},
        {"id": "split-observation-human-authorization-rollback", "match": "one request combines production observation with automatic rollback or recovery", "status": "needs-input", "executable": False, "next_route": "deployment-observation then explicit human rollback authorization then release-rollback-execution", "authorization_propagates": False},
        {"id": "blocked-non-cascading-remote-authorization", "match": "one approval is offered for multiple remote actions such as push, PR change, comment, merge, deploy, provider configuration, or rollback", "status": "blocked", "executable": False, "next_route": "stage-10-release-readiness then one separately authorized remote action", "authorization_propagates": False},
    ]
    router["gates"].extend(["when a safety disposition matches, return its exact disposition ID before any normal target; its next_route is explanatory and is not executed", "atomic runtime support beats stage 15 when one exact owner is known; stage 15 owns multi-capability support or unresolved support-owner selection"])
    for target in router["stage_targets"]:
        if target["stage_id"] in {"stage:05-experience-design", "stage:15-tool-runtime-support"}: target["path"] = f"evals/candidates/capability-compiler-v2/phase-10/revision-1/phase-8/recipes/stages/{target['id']}.json"
    for target in router["composite_targets"]:
        if target["id"] in {"feature-build-and-verify", "full-software-lifecycle"}: target["path"] = f"evals/candidates/capability-compiler-v2/phase-10/revision-1/phase-8/recipes/composites/{target['id']}.json"
    router["specialized_targets"][0]["path"] = "evals/candidates/capability-compiler-v2/phase-10/revision-1/phase-4/complete-ui-design-and-review.json"
    save("phase-8/router.json", router, router_source, "Encode exact non-executable safety dispositions and revised target paths.")

    router_cases = load(p8 / "router-cases.json"); next(item for item in router_cases["cases"] if item["id"] == "V2-P8-ROUTER-support")["expected_target"] = "test-runtime-bootstrap"; router_cases["execution_state"] = "not-run-phase-10-targeted"
    save("phase-8/router-cases.json", router_cases, p8 / "router-cases.json", "Resolve exact missing test runtime to the atomic bootstrap owner.")
    router_holdouts = load(p8 / "router-holdout-cases.json"); next(item for item in router_holdouts["cases"] if item["id"] == "V2-P8-HOLDOUT-tool")["expected_target"] = "tool-runtime-readiness"; router_holdouts["execution_state"] = "not-run-phase-10-targeted"
    save("phase-8/router-holdout-cases.json", router_holdouts, p8 / "router-holdout-cases.json", "Resolve exact browser runtime readiness to the atomic readiness owner.")
    for name in ["recipe-cases.json", "recipe-holdout-cases.json"]:
        source = p8 / name; doc = load(source); doc["execution_state"] = "not-run-phase-10-targeted"; save(f"phase-8/{name}", doc, source, "Preserve frozen Recipe assertions against revised contracts.")

    p8_eval = load(p8 / "evaluation-plan.json"); p8_eval["version"] = VERSION; p8_eval["status"] = "planned"; p8_eval["execution_state"] = "not-run-phase-10-targeted"
    save("phase-8/evaluation-plan.json", p8_eval, p8 / "evaluation-plan.json", "Retarget structural challenges to revision 1.")

    mutation_root = root / "mutations"
    p4_control = load(root / "phase-4/complete-ui-design-and-review.json")
    p4_no_evidence = json.loads(json.dumps(p4_control)); p4_no_evidence["steps"] = [item for item in p4_no_evidence["steps"] if item["id"] != "review-evidence"]; p4_no_evidence["edges"] = [item for item in p4_no_evidence["edges"] if item["from"] != "review-evidence" and item["to"] != "review-evidence"]
    write(mutation_root / "P10-P4-review-evidence.json", p4_no_evidence)
    p4_no_controls = json.loads(json.dumps(p4_control)); p4_no_controls["control_points"] = []; p4_no_controls["edges"] = [item for item in p4_no_controls["edges"] if item["from"] not in {"explicit-human-approval", "separate-remediation-capability"} and item["to"] not in {"explicit-human-approval", "separate-remediation-capability"}]; p4_no_controls["gates"] = [item for item in p4_no_controls["gates"] if "human approval is a non-executable control point" not in item and "separate remediator identity" not in item]
    write(mutation_root / "P10-P4-human-control-points.json", p4_no_controls)

    full_control = load(root / "phase-8/recipes/composites/full-software-lifecycle.json")
    no_handoff = json.loads(json.dumps(full_control)); no_handoff["handoffs"] = [item for item in no_handoff["handoffs"] if item["id"] != "V2-HANDOFF-006"]; write(mutation_root / "P10-P8-handoff.json", no_handoff)
    stage8_source = p8 / "recipes/stages/stage-08-verification-quality.json"; stage8_control = load(stage8_source)
    always_on = json.loads(json.dumps(stage8_control)); next(item for item in always_on["steps"] if item["id"] == "independent-code-review")["default_state"] = "active"; write(mutation_root / "P10-P8-always-on.json", always_on)
    review_write = json.loads(json.dumps(stage8_control)); review_step = next(item for item in review_write["steps"] if item["id"] == "independent-code-review"); review_step["permission_identity"] = "workspace-write"; review_step["mutation_scope"] = "authorized-workspace"; write(mutation_root / "P10-P8-review-write.json", review_write)
    stage11_source = p8 / "recipes/stages/stage-11-deployment-change.json"; stage11_control = load(stage11_source)
    remote_active = json.loads(json.dumps(stage11_control)); next(item for item in remote_active["steps"] if item["id"] == "remote-git-push")["activation"] = "conditional"; write(mutation_root / "P10-P8-remote-activation.json", remote_active)
    delivery_source = p8 / "recipes/composites/verified-change-delivery-and-observation.json"; delivery_control = load(delivery_source)
    no_lifecycle_approval = json.loads(json.dumps(delivery_control)); no_lifecycle_approval["human_checkpoints"] = [item for item in no_lifecycle_approval["human_checkpoints"] if "release scope" not in item]; write(mutation_root / "P10-P8-lifecycle-approval.json", no_lifecycle_approval)
    no_invalidation = json.loads(json.dumps(full_control)); no_invalidation["failure_policy"]["invalidate_downstream_on"] = [item for item in no_invalidation["failure_policy"]["invalidate_downstream_on"] if item != "source capability re-runs"]
    for handoff in no_invalidation["handoffs"]: handoff["invalidation"] = [item for item in handoff["invalidation"] if item != "source capability re-runs"]
    write(mutation_root / "P10-P8-invalidation.json", no_invalidation)

    mutation_policy = {
        "schema_version": "2.0", "version": VERSION, "status": "planned", "source_phase9_tree": PHASE9_TREE,
        "rules": [
            "A deterministic semantic-marker deletion remains killed only by exact marker/hash Gate unless an independently authored causal behavioral challenge exists.",
            "A behavior result is deterministic-only, killed, survived, invalid-control, or behavioral-challenge-needed; do not infer Skill quality from a non-causal survived mutation.",
            "Lifecycle approval and per-action authorization are separate mutation targets and require separate challenges.",
        ],
        "phase9_reclassification": {"deterministic_only": 157, "behavioral_killed_claims_carried_forward": 0},
        "phase10_behavioral_challenges": [
            {"id": "P10-P4-review-evidence", "target": "Phase 4 review-evidence step", "causal": True, "mutant_path": "mutations/P10-P4-review-evidence.json"},
            {"id": "P10-P4-human-control-points", "target": "Phase 4 explicit human approval and separate remediation", "causal": True, "mutant_path": "mutations/P10-P4-human-control-points.json"},
            {"id": "P10-P8-handoff", "target": "Phase 8 mandatory handoff", "causal": True, "mutant_path": "mutations/P10-P8-handoff.json"},
            {"id": "P10-P8-always-on", "target": "Phase 8 conditional atomic step", "causal": True, "mutant_path": "mutations/P10-P8-always-on.json"},
            {"id": "P10-P8-review-write", "target": "Phase 8 review/source-write separation", "causal": True, "mutant_path": "mutations/P10-P8-review-write.json"},
            {"id": "P10-P8-remote-activation", "target": "Phase 8 protected remote activation", "causal": True, "mutant_path": "mutations/P10-P8-remote-activation.json"},
            {"id": "P10-P8-lifecycle-approval", "target": "Phase 8 release-readiness lifecycle approval, not per-action authorization", "causal": True, "mutant_path": "mutations/P10-P8-lifecycle-approval.json"},
            {"id": "P10-P8-invalidation", "target": "Phase 8 source-rerun invalidation", "causal": True, "mutant_path": "mutations/P10-P8-invalidation.json"},
        ],
    }
    write(root / "mutation-policy.json", mutation_policy)

    unaffected = []
    revised_sources = {item["source_path"] for item in patch_records}
    for path in sorted((p8 / "recipes").rglob("*.json")):
        relative = path.relative_to(workspace).as_posix()
        if relative not in revised_sources: unaffected.append({"path": relative, "sha256": sha(path)})
    write(root / "unchanged-reference-manifest.json", {"schema_version": "2.0", "count": len(unaffected), "references": unaffected})
    write(root / "patch-ledger.json", {"schema_version": "2.0", "version": VERSION, "status": "evaluating", "base_trees": {"phase4": PHASE4_TREE, "phase8": PHASE8_TREE, "phase9": PHASE9_TREE}, "patch_count": len(patch_records), "records": patch_records, "atomic_skill_revisions": 0, "released": 0})
    return {"ok": True, "version": VERSION, "patches": len(patch_records), "atomic_skill_revisions": 0, "unaffected_references": len(unaffected)}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__); parser.add_argument("--workspace-root", type=Path, default=Path(".")); args = parser.parse_args(); print(json.dumps(compile_revision(args.workspace_root), ensure_ascii=False, sort_keys=True)); return 0


if __name__ == "__main__": raise SystemExit(main())
