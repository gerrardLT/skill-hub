#!/usr/bin/env python3
"""Fail-closed gate for Phase 8 lifecycle Recipes and minimal-sufficient router."""
from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

try:
    from tools.curation.v2_phase7_gate import verify as verify_phase7
except ModuleNotFoundError:
    from v2_phase7_gate import verify as verify_phase7

VERSION = "0.1.0-v2-candidate"
PRIOR_TREES = {
    "phase2": "57ff1aec49b2b7b370d74d36e52659d7338adf2f16260fe62be7ada870472601",
    "phase3": "de60929ce7eb1877ffb64a9e8cd671beec389b433f843e10320701c890de8965",
    "phase4": "968fd1e2175bdc35d77a4d9025a88ab35e5f096fba353137dbf9770e030d4695",
    "phase5": "7b39fb29c0a25a4a97243e9a857840d14541a9f839e550970c29cc014122e1ee",
    "phase6": "7e8ff8c23ede16d189a9c89d141e2fee87df63251d5d27ec40aa40eef1d24561",
    "phase7": "c76902fd5df781db653e214268b044cb4a8cc389a4fce0a188f72a5fba829926",
}
HANDOFF_ARTIFACTS = ["artifact identities and hashes", "decision and authority record", "completion evidence", "known gaps and residual risk"]
INVALIDATION = ["source artifact hash changes", "source decision or authority changes", "source capability re-runs", "source evidence becomes stale or fails verification"]
EXPECTED_COMPOSITES = {
    "product-discovery-and-planning": list(range(1, 5)),
    "feature-build-and-verify": list(range(4, 11)),
    "verified-change-delivery-and-observation": list(range(10, 13)),
    "incident-recovery-and-learning": list(range(12, 15)),
    "full-software-lifecycle": list(range(1, 15)),
}
PROTECTED_SCOPES = {"local-system-write", "external-session-write", "authorized-local-git"}


def load(path: Path) -> Any: return json.loads(path.read_text(encoding="utf-8"))
def sha(path: Path) -> str: return hashlib.sha256(path.read_bytes().replace(b"\r\n", b"\n")).hexdigest()
def duplicates(values: list[str]) -> set[str]: return {value for value, count in Counter(values).items() if count > 1}
def stage_recipe_id(stage_id: str) -> str: return "stage-" + stage_id.removeprefix("stage:")
def protected(step: dict[str, Any]) -> bool: return bool(step["remote_write"] or step["mutation_scope"] in PROTECTED_SCOPES or step["mutation_scope"].startswith("remote-"))


def discover_candidates(workspace: Path) -> dict[str, dict[str, Any]]:
    records = {}
    for phase in range(3, 8):
        for contract_path in sorted((workspace / f"evals/candidates/capability-compiler-v2/phase-{phase}/skills").glob("*/contract.json")):
            skill_id = contract_path.parent.name; contract = load(contract_path); capability = load(workspace / f"curation/v2/capabilities/{skill_id}.json")
            records[skill_id] = {"id": skill_id, "phase": phase, "stage_id": capability["lifecycle_stage_id"], "candidate_path": contract_path.parent.relative_to(workspace).as_posix(), "contract_path": contract_path.relative_to(workspace).as_posix(), "contract_sha256": sha(contract_path), "skill_sha256": sha(contract_path.parent / "SKILL.md"), "trigger_cases_sha256": sha(contract_path.parent / "trigger-cases.json"), "responsibility": contract["responsibility"], "inputs": contract["inputs"], "outputs": contract["outputs"], "hard_gates": contract["hard_gates"], "permission_identity": contract["permission_identity"], "mutation_scope": contract["execution"]["mutation_scope"], "remote_write": contract["execution"]["remote_write"], "version": contract["version"], "status": contract["status"]}
    return records


def verify(workspace: Path) -> dict[str, Any]:
    workspace = workspace.resolve(); checks: list[dict[str, Any]] = []
    def add(name: str, errors: list[str]) -> None: checks.append({"name": name, "ok": not errors, "errors": errors})

    prior = verify_phase7(workspace); add("phase-7-and-earlier-compatibility", [] if prior["ok"] else prior["errors"])
    identity_errors = []
    for phase, identity in PRIOR_TREES.items():
        path = workspace / f".specs/capability-compiler-v2/{phase.replace('phase','phase-')}/artifact-manifest.json"
        if not path.is_file() or load(path).get("tree_sha256") != identity: identity_errors.append(f"{phase} artifact identity changed or missing")
    add("prior-phase-artifact-identities", identity_errors)

    root = workspace / "evals/candidates/capability-compiler-v2/phase-8"; schema_root = workspace / "curation/v2/phase-8"
    required_root = {"catalog.json", "evaluation-plan.json", "recipe-cases.json", "recipe-holdout-cases.json", "router-cases.json", "router-holdout-cases.json", "router.json", "skill-index.json"}
    inventory_errors = []
    if not root.is_dir(): inventory_errors.append("Phase 8 candidate root missing")
    else:
        files = {path.name for path in root.iterdir() if path.is_file()}
        if files != required_root: inventory_errors.append(f"candidate root file set mismatch {sorted(files)}")
    stage_paths = sorted((root / "recipes/stages").glob("*.json")) if root.is_dir() else []
    composite_paths = sorted((root / "recipes/composites").glob("*.json")) if root.is_dir() else []
    if len(stage_paths) != 15: inventory_errors.append(f"expected 15 stage Recipes, got {len(stage_paths)}")
    if {path.stem for path in composite_paths} != set(EXPECTED_COMPOSITES): inventory_errors.append("composite Recipe set mismatch")
    required_schemas = {"stage-recipe.schema.json", "composite-recipe.schema.json", "router.schema.json", "semantic-review.json"}
    if not schema_root.is_dir() or {path.name for path in schema_root.iterdir() if path.is_file()} != required_schemas: inventory_errors.append("Phase 8 schema/review file set mismatch")
    add("phase-8-artifact-inventory", inventory_errors)

    candidates = discover_candidates(workspace); index_errors = []
    index = load(root / "skill-index.json") if (root / "skill-index.json").is_file() else {"skills": []}
    indexed = {item["id"]: item for item in index.get("skills", [])}; indexed_ids = [item.get("id") for item in index.get("skills", [])]
    if len(candidates) != 157 or index.get("skill_count") != 157 or set(indexed) != set(candidates) or duplicates(indexed_ids): index_errors.append("candidate discovery and Skill index do not cover exactly 157 unique candidates")
    if index.get("version") != VERSION or index.get("status") != "evaluating" or index.get("prior_artifact_trees") != PRIOR_TREES: index_errors.append("Skill index version, status, or prior identities mismatch")
    for skill_id, expected in candidates.items():
        actual = indexed.get(skill_id)
        if actual != expected: index_errors.append(f"{skill_id}: indexed candidate identity or contract changed")
    ownership = load(workspace / "curation/v2/lifecycle/phase-ownership.json")["phases"]
    owned = {item.removeprefix("capability:") for phase in ["3", "4", "5", "6", "7"] for item in ownership[phase]}
    if owned != set(candidates): index_errors.append("Phase 3–7 ownership does not match indexed candidates")
    add("candidate-index-hashes-and-ownership", index_errors)

    schema_errors = []
    validators = {}
    for name in ["stage-recipe.schema.json", "composite-recipe.schema.json", "router.schema.json"]:
        path = schema_root / name
        if path.is_file(): validators[name] = Draft202012Validator(load(path))
    stage_docs: dict[str, dict[str, Any]] = {}; composite_docs: dict[str, dict[str, Any]] = {}
    for path in stage_paths:
        doc = load(path); stage_docs[doc.get("id", path.stem)] = doc
        for error in validators.get("stage-recipe.schema.json", Draft202012Validator({})).iter_errors(doc): schema_errors.append(f"{path.name}:{'.'.join(map(str,error.absolute_path)) or '<root>'}: {error.message}")
    for path in composite_paths:
        doc = load(path); composite_docs[doc.get("id", path.stem)] = doc
        for error in validators.get("composite-recipe.schema.json", Draft202012Validator({})).iter_errors(doc): schema_errors.append(f"{path.name}:{'.'.join(map(str,error.absolute_path)) or '<root>'}: {error.message}")
    router = load(root / "router.json") if (root / "router.json").is_file() else {}
    for error in validators.get("router.schema.json", Draft202012Validator({})).iter_errors(router): schema_errors.append(f"router.json:{'.'.join(map(str,error.absolute_path)) or '<root>'}: {error.message}")
    add("recipe-and-router-schemas", schema_errors)

    stage_source = load(workspace / "curation/v2/lifecycle/stages.json"); source_stages = {stage["id"]: stage for stage in stage_source["stages"]}; recipe_by_stage = {doc.get("stage_id"): doc for doc in stage_docs.values()}
    stage_errors = []
    if set(recipe_by_stage) != set(source_stages): stage_errors.append("one stage Recipe per lifecycle stage is not preserved")
    all_steps = []; seen_ids = []
    dependencies = load(workspace / "curation/v2/lifecycle/dependencies.json"); dep_by_target: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for record in dependencies["records"]: dep_by_target[record["target_capability_id"].removeprefix("capability:")].append(record)
    seen_dependency_records = []
    for stage_id, source in source_stages.items():
        doc = recipe_by_stage.get(stage_id)
        if not doc: continue
        if doc.get("id") != stage_recipe_id(stage_id) or doc.get("stage_order") != source["order"] or doc.get("mandatory_stage") != source["mandatory"] or doc.get("description") != source["responsibility"]: stage_errors.append(f"{stage_id}: stage identity changed")
        if not doc.get("condition") or not doc.get("human_checkpoint") or not doc.get("exit_contract"): stage_errors.append(f"{stage_id}: hand-designed policy incomplete")
        expected_records = sorted((record for skill_id in candidates if candidates[skill_id]["stage_id"] == stage_id for record in dep_by_target[skill_id]), key=lambda item: item["id"])
        if sorted(doc.get("dependency_records", []), key=lambda item: item["id"]) != expected_records: stage_errors.append(f"{stage_id}: dependency record projection mismatch")
        seen_dependency_records.extend(record["id"] for record in doc.get("dependency_records", []))
        for step in doc.get("steps", []):
            all_steps.append(step); seen_ids.append(step.get("id")); skill_id = step.get("id"); candidate = candidates.get(skill_id)
            if not candidate: stage_errors.append(f"{stage_id}: unknown Skill step {skill_id}"); continue
            exact = {"skill_ref": f"{skill_id}@{VERSION}", "candidate_path": candidate["candidate_path"], "contract_sha256": candidate["contract_sha256"], "permission_identity": candidate["permission_identity"], "mutation_scope": candidate["mutation_scope"], "remote_write": candidate["remote_write"], "inputs": candidate["inputs"], "outputs": candidate["outputs"], "hard_gates": candidate["hard_gates"]}
            if any(step.get(key) != value for key, value in exact.items()): stage_errors.append(f"{skill_id}: step widens or changes atomic contract")
            if candidate["stage_id"] != stage_id: stage_errors.append(f"{skill_id}: wrong primary stage")
            if step.get("default_state") != "skipped" or len(step.get("condition", "")) < 20: stage_errors.append(f"{skill_id}: missing explicit conditional activation")
            expected_activation = "disabled-pending-current-authorization" if protected(step) else "conditional"
            if step.get("activation") != expected_activation: stage_errors.append(f"{skill_id}: protected action activation mismatch")
            expected_refs = sorted(record["id"] for record in dep_by_target[skill_id])
            if step.get("dependency_refs") != expected_refs: stage_errors.append(f"{skill_id}: dependency references mismatch")
            if step.get("evidence_contract") != HANDOFF_ARTIFACTS or step.get("failure_routes") != {"needs-input": "stop-and-request-owner-input", "blocked": "stop-and-preserve-evidence", "failed": "stop-invalidate-dependents-and-record", "passed": "emit-artifact-contract"}: stage_errors.append(f"{skill_id}: evidence or failure contract mismatch")
        if doc.get("execution_state") != "not-run-phase-9" or doc.get("status") != "evaluating" or doc.get("version") != VERSION: stage_errors.append(f"{stage_id}: false execution, release, or version state")
    if set(seen_ids) != set(candidates) or len(seen_ids) != 157 or duplicates(seen_ids): stage_errors.append("157 candidates are not covered exactly once by primary stage Recipes")
    if len(seen_dependency_records) != 249 or set(seen_dependency_records) != {record["id"] for record in dependencies["records"]} or duplicates(seen_dependency_records): stage_errors.append("249 dependencies are not projected exactly once by target stage")
    add("stage-skill-coverage-permission-and-dependencies", stage_errors)

    handoffs = load(workspace / "curation/v2/lifecycle/handoffs.json"); handoff_errors = []
    if handoffs.get("count") != 13 or any(record.get("artifact_contract") != HANDOFF_ARTIFACTS or record.get("invalidation") != INVALIDATION for record in handoffs["records"]): handoff_errors.append("Phase 2 mandatory handoff contract changed")
    stages_by_order = {stage["order"]: stage for stage in source_stages.values()}
    for recipe_id, orders in EXPECTED_COMPOSITES.items():
        doc = composite_docs.get(recipe_id)
        if not doc: handoff_errors.append(f"{recipe_id}: missing"); continue
        expected_stages = [stages_by_order[order]["id"] for order in orders]; actual_stages = [item.get("stage_id") for item in doc.get("stage_steps", [])]
        if actual_stages != expected_stages: handoff_errors.append(f"{recipe_id}: stage sequence mismatch")
        for index, item in enumerate(doc.get("stage_steps", [])):
            expected_depends = [] if index == 0 else [stage_recipe_id(expected_stages[index - 1])]
            if item.get("recipe_ref") != f"{stage_recipe_id(item['stage_id'])}@{VERSION}" or item.get("depends_on") != expected_depends or item.get("mandatory_in_recipe") is not True: handoff_errors.append(f"{recipe_id}: invalid stage reference or dependency")
            if set(item) != {"stage_id", "recipe_ref", "condition", "depends_on", "mandatory_in_recipe"}: handoff_errors.append(f"{recipe_id}: atomic Skill logic leaked into composite")
        selected = set(expected_stages); expected_handoffs = [record for record in handoffs["records"] if record["source_stage_id"] in selected and record["target_stage_id"] in selected]
        if doc.get("handoffs") != expected_handoffs: handoff_errors.append(f"{recipe_id}: handoff projection changed")
        if doc.get("failure_policy", {}).get("invalidate_downstream_on") != INVALIDATION or not doc.get("failure_policy", {}).get("resume_only_from_valid_checkpoint"): handoff_errors.append(f"{recipe_id}: invalidation or resume weakened")
        support = doc.get("support_stage", {})
        if support.get("stage_id") != "stage:15-tool-runtime-support" or support.get("mandatory_in_recipe") is not False or support.get("return_to_blocked_owner") is not True: handoff_errors.append(f"{recipe_id}: support-stage semantics changed")
        if len(doc.get("human_checkpoints", [])) != len(orders): handoff_errors.append(f"{recipe_id}: human checkpoint count mismatch")
        if doc.get("execution_state") != "not-run-phase-9" or doc.get("status") != "evaluating": handoff_errors.append(f"{recipe_id}: false execution or release state")
    full = composite_docs.get("full-software-lifecycle", {})
    if full.get("handoffs") != handoffs["records"] or len(full.get("handoffs", [])) != 13: handoff_errors.append("full lifecycle does not preserve all thirteen mandatory handoffs")
    add("composite-handoffs-human-checkpoints-and-invalidation", handoff_errors)

    router_errors = []
    expected_order = ["safety override", "one atomic candidate Skill", "one stage Recipe", "specialized complete UI Recipe", "smallest bounded composite Recipe", "explicit full-software-lifecycle only", "governance intake fallback"]
    if router.get("selection_order") != expected_order: router_errors.append("minimal-sufficient selection order changed")
    stage_targets = router.get("stage_targets", []); composite_targets = router.get("composite_targets", [])
    if [item.get("stage_id") for item in stage_targets] != [stages_by_order[order]["id"] for order in range(1, 16)]: router_errors.append("router stage targets are incomplete or reordered")
    composite_ids = [item.get("id") for item in composite_targets]
    if set(composite_ids) != set(EXPECTED_COMPOSITES) or len(composite_ids) != 5 or composite_ids[-1:] != ["full-software-lifecycle"]: router_errors.append("bounded composites must precede the complete explicit-only composite set and full lifecycle")
    specialized = router.get("specialized_targets", [])
    if len(specialized) != 1 or specialized[0].get("id") != "complete-ui-design-and-review" or not (workspace / specialized[0].get("path", "missing")).is_file(): router_errors.append("specialized UI route missing or invalid")
    if router.get("fallback") != {"target": "stage-01-governance-intake", "status": "needs-input", "reason": "ambiguous authority, scope, lifecycle stage, or multi-domain request"}: router_errors.append("ambiguous route does not fail closed to governance intake")
    safety_text = "\n".join(router.get("safety_overrides", []))
    for marker in ["governance", "review plus repair", "observation plus rollback", "fresh per-action authorization", "never propagates", "ambiguous multi-domain"]:
        if marker not in safety_text: router_errors.append(f"router safety override missing {marker}")
    if router.get("execution_state") != "not-run-phase-9" or router.get("status") != "evaluating": router_errors.append("router claims execution or release")
    add("minimal-router-specialized-route-and-safety-overrides", router_errors)

    separation_errors = []; by_id = {step["id"]: step for step in all_steps if step.get("id")}
    pairs = [
        ("independent-code-review", "defect-remediation"),
        ("rendered-ui-critique-and-release-disposition", "ui-remediation"),
        ("change-delivery-preflight", "remote-git-push"),
        ("merge-and-deploy-readiness", "remote-pull-request-merge"),
        ("deployment-observation", "release-rollback-execution"),
        ("incident-response-coordination", "release-rollback-execution"),
        ("feedback-and-continuous-learning-loop", "local-learning-persistence"),
    ]
    for left, right in pairs:
        if left not in by_id or right not in by_id: separation_errors.append(f"missing separation member {left}/{right}"); continue
        if by_id[left]["permission_identity"] == by_id[right]["permission_identity"] and by_id[left]["mutation_scope"] == by_id[right]["mutation_scope"]: separation_errors.append(f"{left}/{right}: identities collapsed")
    for skill_id, step in by_id.items():
        if protected(step) and step["activation"] != "disabled-pending-current-authorization": separation_errors.append(f"{skill_id}: protected action enabled")
    add("review-change-observation-recovery-and-learning-separation", separation_errors)

    fixture_errors = []
    router_cases = load(root / "router-cases.json") if (root / "router-cases.json").is_file() else {"cases": []}; router_holdouts = load(root / "router-holdout-cases.json") if (root / "router-holdout-cases.json").is_file() else {"cases": []}; recipe_cases = load(root / "recipe-cases.json") if (root / "recipe-cases.json").is_file() else {"cases": []}; recipe_holdouts = load(root / "recipe-holdout-cases.json") if (root / "recipe-holdout-cases.json").is_file() else {"cases": []}; evaluation = load(root / "evaluation-plan.json") if (root / "evaluation-plan.json").is_file() else {}
    collections = [router_cases, router_holdouts, recipe_cases, recipe_holdouts]; ids = [[case.get("id") for case in value.get("cases", [])] for value in collections]
    if [len(value) for value in ids] != [14, 8, 8, 6]: fixture_errors.append("authored/holdout case counts mismatch")
    if any(value.get("execution_state") != "not-run-phase-9" for value in collections): fixture_errors.append("case set claims execution")
    flat = [item for values in ids for item in values]
    if duplicates(flat): fixture_errors.append("fixture IDs overlap")
    if evaluation.get("status") != "planned" or evaluation.get("execution_state") != "not-run-phase-9" or len(evaluation.get("mutations", [])) != 6: fixture_errors.append("evaluation plan state or mutation count mismatch")
    if evaluation.get("router_case_ids") != ids[0] or evaluation.get("router_holdout_ids") != ids[1] or evaluation.get("recipe_case_ids") != ids[2] or evaluation.get("recipe_holdout_ids") != ids[3]: fixture_errors.append("evaluation plan case references mismatch")
    expected_targets = {"root-cause-investigation", "stage-08-verification-quality", "complete-ui-design-and-review", "product-discovery-and-planning", "feature-build-and-verify", "verified-change-delivery-and-observation", "incident-recovery-and-learning", "full-software-lifecycle", "stage-01-governance-intake", "blocked-data-governance", "split-independent-review-human-approval-remediation", "split-observation-human-authorization-rollback", "blocked-non-cascading-remote-authorization", "stage-15-tool-runtime-support"}
    if {case.get("expected_target") for case in router_cases.get("cases", [])} != expected_targets: fixture_errors.append("authored router boundaries incomplete")
    add("authored-holdout-and-mutation-fixtures", fixture_errors)

    review_errors = []; review_path = schema_root / "semantic-review.json"
    if not review_path.is_file(): review_errors.append("semantic review missing")
    else:
        review = load(review_path)
        if review.get("status") != "passed" or review.get("reviewed_stage_recipe_count") != 15 or review.get("reviewed_composite_recipe_count") != 5 or review.get("reviewed_router_count") != 1 or review.get("reviewed_candidate_step_count") != 157 or review.get("open_findings") != []: review_errors.append("semantic review status/count/open findings mismatch")
        if len(review.get("boundary_samples", [])) < 15 or any(item.get("verdict") != "passed" for item in review.get("boundary_samples", [])): review_errors.append("semantic boundary review incomplete")
        if any(item.get("status") != "resolved" for item in review.get("findings", [])): review_errors.append("semantic findings unresolved")
    add("semantic-boundary-review", review_errors)

    catalog_errors = []; catalog = load(root / "catalog.json") if (root / "catalog.json").is_file() else {}
    if catalog.get("stage_recipe_count") != 15 or catalog.get("composite_recipe_count") != 5 or catalog.get("specialized_recipe_count") != 1 or catalog.get("router_count") != 1 or catalog.get("candidate_skill_count") != 157: catalog_errors.append("catalog counts mismatch")
    if catalog.get("version") != VERSION or catalog.get("status") != "evaluating": catalog_errors.append("catalog version or status mismatch")
    for item in catalog.get("stage_recipes", []) + catalog.get("composite_recipes", []):
        path = workspace / item.get("path", "missing")
        if not path.is_file() or sha(path) != item.get("sha256"): catalog_errors.append(f"catalog hash mismatch {item.get('id')}")
    for item in catalog.get("specialized_recipes", []):
        path = workspace / item.get("path", "missing")
        if not path.is_file() or sha(path) != item.get("sha256"): catalog_errors.append("specialized Recipe hash mismatch")
    router_record = catalog.get("router", {}); router_path = workspace / router_record.get("path", "missing")
    if not router_path.is_file() or sha(router_path) != router_record.get("sha256"): catalog_errors.append("router hash mismatch")
    add("catalog-hashes-and-no-release-claim", catalog_errors)

    errors = [f"{check['name']}: {error}" for check in checks for error in check["errors"]]
    return {"gate": "capability-compiler-v2-phase-8", "ok": not errors, "checks": checks, "counts": {"candidate_skills": len(candidates), "stage_recipes": len(stage_docs), "composite_recipes": len(composite_docs), "specialized_recipes": len(router.get("specialized_targets", [])), "mandatory_handoffs": len(full.get("handoffs", [])), "dependencies": len(seen_dependency_records), "router_authored_cases": len(ids[0]), "router_holdout_cases": len(ids[1]), "recipe_authored_cases": len(ids[2]), "recipe_holdout_cases": len(ids[3]), "planned_mutations": len(evaluation.get("mutations", [])), "protected_action_steps": sum(protected(step) for step in all_steps)}, "errors": errors}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__); parser.add_argument("--workspace-root", type=Path, default=Path(".")); parser.add_argument("--output", type=Path); args = parser.parse_args(); result = verify(args.workspace_root)
    if args.output:
        path = args.output if args.output.is_absolute() else args.workspace_root / args.output; path.parent.mkdir(parents=True, exist_ok=True); path.write_text(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps(result, ensure_ascii=False, sort_keys=True)); return 0 if result["ok"] else 1


if __name__ == "__main__": raise SystemExit(main())
