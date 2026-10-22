#!/usr/bin/env python3
"""Fail-closed gate for Phase 4 UX/UI candidate Skills and candidate Recipe."""
from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter, defaultdict, deque
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

try:
    from tools.curation.v2_phase3_gate import verify as verify_phase3
except ModuleNotFoundError:
    from v2_phase3_gate import verify as verify_phase3

VERSION = "0.1.0-v2-candidate"
PHASE2_TREE = "57ff1aec49b2b7b370d74d36e52659d7338adf2f16260fe62be7ada870472601"
PHASE3_TREE = "de60929ce7eb1877ffb64a9e8cd671beec389b433f843e10320701c890de8965"
REQUIRED_FILES = {"SKILL.md", "contract.json", "provenance.json", "trigger-cases.json", "evaluation-plan.json"}
AUTHORIZED_WORKSPACE = {
    "ai-interaction-and-probabilistic-ux", "content-copy-and-authentic-assets", "design-system-foundation-and-token-extraction",
    "divergent-prototyping-and-variant-selection", "interaction-states-forms-and-navigation", "purposeful-motion-and-animation-engineering",
    "responsive-layout-and-spatial-composition", "visual-language-and-anti-template-controls",
}
ARTIFACT_ONLY = {"rendered-ui-critique-and-release-disposition", "ui-review-scope-and-evidence-acquisition"}
RUN_OUTPUT = {
    "accessibility-contracts-and-assistive-validation", "cross-domain-ui-preflight-checklists", "design-context-and-direction-contract",
    "evidence-based-ui-review-and-release-gates", "existing-interface-redesign-and-preservation",
    "external-design-token-extraction-and-normalization", "ui-task-routing-and-governance",
}
REQUIRED_COVERAGE = {
    "user-flow", "information-hierarchy", "semantic-tokens", "component-contracts", "truthful-copy", "asset-provenance",
    "mobile", "tablet", "desktop", "intermediate-widths", "zoom", "overflow", "touch-targets", "loading", "empty", "error",
    "permission", "disabled", "success", "interruption", "recovery", "semantics", "keyboard", "focus", "assistive-technology",
    "contrast", "visual-input", "reduced-motion", "determinism", "uncertainty", "provenance", "correction", "escalation",
    "safe-failure", "preservation", "SEO", "analytics", "real-renders", "multi-viewport", "interaction-traces",
}


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes().replace(b"\r\n", b"\n")).hexdigest()


def duplicates(values: list[str]) -> set[str]:
    return {value for value, count in Counter(values).items() if count > 1}


def verify(workspace: Path) -> dict[str, Any]:
    workspace = workspace.resolve(); checks: list[dict[str, Any]] = []
    def add(name: str, errors: list[str]) -> None: checks.append({"name": name, "ok": not errors, "errors": errors})

    phase3 = verify_phase3(workspace)
    add("phase-3-and-earlier-compatibility", [] if phase3["ok"] else phase3["errors"])
    identity_errors = []
    if load(workspace / ".specs/capability-compiler-v2/phase-2/artifact-manifest.json")["tree_sha256"] != PHASE2_TREE: identity_errors.append("Phase 2 artifact identity changed")
    if load(workspace / ".specs/capability-compiler-v2/phase-3/artifact-manifest.json")["tree_sha256"] != PHASE3_TREE: identity_errors.append("Phase 3 artifact identity changed")
    add("prior-phase-artifact-identities", identity_errors)

    candidate_root = workspace / "evals/candidates/capability-compiler-v2/phase-4"; schema_root = workspace / "curation/v2/phase-4"
    expected = {item.removeprefix("capability:") for item in load(workspace / "curation/v2/lifecycle/phase-ownership.json")["phases"]["4"]}
    catalog = load(candidate_root / "catalog.json"); catalog_ids = [item["id"] for item in catalog["skills"]]
    candidate_dirs = {path.name for path in (candidate_root / "skills").iterdir() if path.is_dir()}
    inventory_errors = []
    if len(expected) != 17: inventory_errors.append(f"expected 17 Phase 4 IDs, got {len(expected)}")
    if set(catalog_ids) != expected or duplicates(catalog_ids): inventory_errors.append("catalog IDs do not exactly equal Phase 4 ownership")
    if candidate_dirs != expected: inventory_errors.append(f"candidate directories mismatch missing={sorted(expected-candidate_dirs)} extra={sorted(candidate_dirs-expected)}")
    if catalog.get("skill_count") != 17 or catalog.get("recipe_count") != 1 or catalog.get("version") != VERSION or catalog.get("status") != "evaluating": inventory_errors.append("catalog count/version/status mismatch")
    if any(item.get("version") != VERSION or item.get("status") != "evaluating" for item in catalog["skills"] + catalog["recipes"]): inventory_errors.append("catalog entry version/status mismatch")
    add("phase-4-candidate-inventory", inventory_errors)

    schema_names = ["candidate-skill.schema.json", "provenance.schema.json", "trigger-cases.schema.json", "evaluation-plan.schema.json", "candidate-recipe.schema.json"]
    validators = {name: Draft202012Validator(load(schema_root / name)) for name in schema_names}
    designs = {item["skill_id"]: item for item in load(schema_root / "designs.json")["designs"]}
    documents: dict[str, dict[str, Any]] = {}; all_cases: list[dict[str, Any]] = []; schema_errors = []
    for skill_id in sorted(expected):
        directory = candidate_root / "skills" / skill_id
        if not directory.is_dir(): schema_errors.append(f"{skill_id}: missing candidate directory"); continue
        present = {path.name for path in directory.iterdir() if path.is_file()}
        if present != REQUIRED_FILES: schema_errors.append(f"{skill_id}: file set mismatch {sorted(present)}"); continue
        docs = {}
        for filename, schema_name in {"contract.json": "candidate-skill.schema.json", "provenance.json": "provenance.schema.json", "trigger-cases.json": "trigger-cases.schema.json", "evaluation-plan.json": "evaluation-plan.schema.json"}.items():
            doc = load(directory / filename); docs[filename] = doc
            for error in validators[schema_name].iter_errors(doc):
                schema_errors.append(f"{skill_id}/{filename}:{'.'.join(map(str,error.absolute_path)) or '<root>'}: {error.message}")
        documents[skill_id] = docs; contract = docs["contract.json"]; provenance = docs["provenance.json"]; evaluation = docs["evaluation-plan.json"]
        if any(doc.get("id", doc.get("skill_id")) != skill_id for doc in docs.values()): schema_errors.append(f"{skill_id}: internal IDs disagree")
        if contract["responsibility"] != designs[skill_id]["trigger"] or contract["hard_gates"][0] != designs[skill_id]["distinctive_gate"]: schema_errors.append(f"{skill_id}: semantic design not preserved")
        text = (directory / "SKILL.md").read_text(encoding="utf-8")
        if designs[skill_id]["distinctive_gate"] not in text: schema_errors.append(f"{skill_id}: distinctive marker absent")
        for filename, expected_hash in provenance["candidate_files"].items():
            if sha(directory / filename) != expected_hash: schema_errors.append(f"{skill_id}: stale candidate hash {filename}")
        if evaluation["candidate"]["skill_sha256"] != sha(directory / "SKILL.md") or evaluation["candidate"]["contract_sha256"] != sha(directory / "contract.json"): schema_errors.append(f"{skill_id}: stale evaluation hashes")
        all_cases.extend(docs["trigger-cases.json"]["cases"])
    recipe_path = candidate_root / "recipes/complete-ui-design-and-review.json"; recipe = load(recipe_path)
    for error in validators["candidate-recipe.schema.json"].iter_errors(recipe): schema_errors.append(f"recipe:{'.'.join(map(str,error.absolute_path)) or '<root>'}: {error.message}")
    add("candidate-schemas-semantic-design-and-hashes", schema_errors)

    provenance_errors = []
    for skill_id, docs in documents.items():
        provenance = docs["provenance.json"]; capability = load(workspace / f"curation/v2/capabilities/{skill_id}.json")
        if provenance["phase2_artifact_tree_sha256"] != PHASE2_TREE or provenance["phase3_artifact_tree_sha256"] != PHASE3_TREE: provenance_errors.append(f"{skill_id}: prior identity mismatch")
        for field in ["source_cluster_ids", "canonical_unit_ids", "retained_auxiliary_unit_ids", "root_derived_atom_ids", "source_fragment_ids", "fusion_decision_ids", "decision_references", "source_evidence", "source_defect_refs"]:
            if provenance[field] != capability[field]: provenance_errors.append(f"{skill_id}: provenance mismatch {field}")
    add("provenance-set-equality", provenance_errors)

    permission_errors = []
    identities = {item["id"]: item for item in load(workspace / "curation/v2/lifecycle/permission-identities.json")["identities"]}
    if AUTHORIZED_WORKSPACE | ARTIFACT_ONLY | RUN_OUTPUT != expected: permission_errors.append("mutation allowlists do not cover Phase 4 ownership exactly")
    for skill_id, docs in documents.items():
        contract = docs["contract.json"]; identity = identities[contract["permission_identity"]]; execution = contract["execution"]
        if execution["model_tools"] != identity["model_tools"] or execution["host_actions"] != identity["host_actions"] or execution["external"] != identity["external"] or execution["remote_write"] is not False: permission_errors.append(f"{skill_id}: execution does not match permission identity")
        expected_scope = "authorized-workspace" if skill_id in AUTHORIZED_WORKSPACE else ("artifact-output" if skill_id in ARTIFACT_ONLY else "run-output")
        if execution["mutation_scope"] != expected_scope: permission_errors.append(f"{skill_id}: mutation scope must be {expected_scope}")
        if skill_id in ARTIFACT_ONLY and ("edit" in execution["model_tools"] or "write" in execution["model_tools"]): permission_errors.append(f"{skill_id}: reviewer has source-write tools")
        if skill_id == "external-design-token-extraction-and-normalization" and (execution["external"] != "none" or "approved-provider-read" in execution["host_actions"]): permission_errors.append("external-token candidate exceeds supplied-artifact-only authority")
    add("permission-and-review-repair-separation", permission_errors)

    case_errors = []; authored_ids = [case["id"] for case in all_cases]
    if duplicates(authored_ids): case_errors.append(f"duplicate authored IDs: {sorted(duplicates(authored_ids))}")
    for skill_id, docs in documents.items():
        cases = docs["trigger-cases.json"]["cases"]; counts = Counter(case["kind"] for case in cases)
        if counts != {"should-trigger": 2, "should-not-trigger": 2, "boundary": 1, "authority-stop": 1}: case_errors.append(f"{skill_id}: case shape mismatch {dict(counts)}")
        for case in cases:
            if case["kind"] == "should-trigger" and case["expected_skill_id"] != skill_id: case_errors.append(f"{case['id']}: positive misroute")
            if case["kind"] == "should-not-trigger" and (case["expected_skill_id"] == skill_id or skill_id not in case["forbidden_skill_ids"]): case_errors.append(f"{case['id']}: anti-route invalid")
            target = case["expected_skill_id"]
            if target and target not in expected and not (workspace / f"curation/v2/capabilities/{target}.json").is_file(): case_errors.append(f"{case['id']}: unknown route {target}")
    holdout = load(candidate_root / "holdout-cases.json"); holdout_ids = [case["id"] for case in holdout["cases"]]
    if holdout.get("case_count") != 34 or len(holdout_ids) != 34 or holdout.get("execution_state") != "not-run-phase-9": case_errors.append("holdout count/state mismatch")
    if duplicates(holdout_ids) or set(holdout_ids) & set(authored_ids): case_errors.append("holdout IDs duplicate or overlap authored cases")
    for skill_id, docs in documents.items():
        planned = set(docs["evaluation-plan.json"]["holdout_case_ids"]); owned = {item for item in holdout_ids if item.startswith(f"V2-P4-{skill_id}-holdout-")}
        if planned != owned or len(owned) != 2: case_errors.append(f"{skill_id}: holdout plan mismatch")
    add("trigger-and-holdout-boundaries", case_errors)

    ui_errors = []; aggregate = {marker for docs in documents.values() for marker in docs["contract.json"]["policy"]["coverage"]}
    missing = REQUIRED_COVERAGE - aggregate
    if missing: ui_errors.append(f"missing required UI coverage {sorted(missing)}")
    for skill_id, docs in documents.items():
        contract = docs["contract.json"]; text = (candidate_root / "skills" / skill_id / "SKILL.md").read_text(encoding="utf-8")
        if contract["policy"]["rendered_evidence"] and ("## Rendered Evidence" not in text or "static source inspection" not in text): ui_errors.append(f"{skill_id}: rendered-evidence gate missing")
        if contract["policy"]["human_decision"] and "## Human Design Authority" not in text: ui_errors.append(f"{skill_id}: human design authority missing")
        if "Review and preflight capabilities never repair product source" not in text: ui_errors.append(f"{skill_id}: review/repair separation marker missing")
    add("complete-ui-coverage-and-rendered-evidence", ui_errors)

    evaluation_errors = []
    for skill_id, docs in documents.items():
        evaluation = docs["evaluation-plan.json"]; directory = candidate_root / "skills" / skill_id; text = (directory / "SKILL.md").read_text(encoding="utf-8")
        if evaluation["status"] != "planned" or evaluation["execution_state"] != "not-run-phase-9": evaluation_errors.append(f"{skill_id}: false evaluation claim")
        baseline = evaluation["baseline"]
        if baseline["kind"] == "released-v1-slot":
            baseline_id, version = baseline["identity"].rsplit("@", 1); path = workspace / f"slots/{baseline_id}/contract.json"
            if not path.is_file() or load(path).get("status") != "released" or load(path).get("version") != version: evaluation_errors.append(f"{skill_id}: invalid released baseline")
        elif baseline["kind"] == "source-skill" and not (workspace / "skills" / baseline["identity"] / "SKILL.md").is_file(): evaluation_errors.append(f"{skill_id}: missing source baseline")
        for mutation in evaluation["mutations"]:
            marker = mutation["remove_exact_text"]
            if text.count(marker) != 1 or marker not in designs[skill_id]["distinctive_gate"]: evaluation_errors.append(f"{mutation['id']}: mutation marker invalid")
    add("evaluation-plans-and-semantic-mutations", evaluation_errors)

    recipe_errors = []; steps = recipe["steps"]; step_ids = [step["id"] for step in steps]; refs = [step["skill_ref"].removesuffix(f"@{VERSION}") for step in steps]
    if len(steps) != 17 or set(refs) != expected or duplicates(refs) or duplicates(step_ids): recipe_errors.append("Recipe must reference all 17 Skills exactly once")
    if recipe.get("status") != "evaluating" or recipe.get("evaluation_state") != "not-run-phase-9": recipe_errors.append("Recipe status/evaluation state unsafe")
    by_step = {step["id"]: step for step in steps}
    for step in steps:
        skill_id = step["skill_ref"].removesuffix(f"@{VERSION}")
        if skill_id not in documents:
            recipe_errors.append(f"{step['id']}: referenced candidate contract is missing"); continue
        if step["permission_identity"] != documents[skill_id]["contract.json"]["permission_identity"]: recipe_errors.append(f"{step['id']}: incompatible permission identity")
        if step["mutation_scope"] != documents[skill_id]["contract.json"]["execution"]["mutation_scope"]: recipe_errors.append(f"{step['id']}: incompatible mutation scope")
        if step["id"] != "route" and step["when"] == "always": recipe_errors.append(f"{step['id']}: non-routing step is unconditional")
        if any(dependency not in by_step for dependency in step["depends_on"]): recipe_errors.append(f"{step['id']}: unknown dependency")
    graph = defaultdict(list); indegree = {step_id: 0 for step_id in step_ids}
    for edge in recipe["edges"]:
        if edge["from"] not in by_step or edge["to"] not in by_step: recipe_errors.append(f"unknown Recipe edge {edge}"); continue
        graph[edge["from"]].append(edge["to"]); indegree[edge["to"]] += 1
    queue = deque(node for node, degree in indegree.items() if degree == 0); visited = []
    while queue:
        node = queue.popleft(); visited.append(node)
        for target in graph[node]:
            indegree[target] -= 1
            if indegree[target] == 0: queue.append(target)
    if len(visited) != len(step_ids): recipe_errors.append("Recipe edge graph has a cycle")
    reachable = {"route"}; queue = deque(["route"])
    while queue:
        for target in graph[queue.popleft()]:
            if target not in reachable: reachable.add(target); queue.append(target)
    if reachable != set(step_ids): recipe_errors.append(f"Recipe has unreachable steps {sorted(set(step_ids)-reachable)}")
    if any(route["authorization"] != "explicit-human-approval" for route in recipe["feedback_routes"]): recipe_errors.append("feedback route lacks human repair authorization")
    if "authorize source remediation separately from every review finding" not in recipe["human_checkpoints"]: recipe_errors.append("Recipe lacks reviewer/remediator checkpoint")
    if not any("static source inspection" in gate for gate in recipe["gates"]): recipe_errors.append("Recipe lacks rendered-evidence gate")
    if any(term in json.dumps(recipe).lower() for term in ["remote-write-authorized-only", "deployment-trigger-execution", "pull-request-creation"]): recipe_errors.append("Recipe exposes remote mutation")
    recipe_cases = load(candidate_root / "recipes/recipe-cases.json"); recipe_holdouts = load(candidate_root / "recipes/recipe-holdout-cases.json"); recipe_eval = load(candidate_root / "recipes/evaluation-plan.json")
    recipe_case_ids = [case["id"] for case in recipe_cases["cases"]]; recipe_holdout_ids = [case["id"] for case in recipe_holdouts["cases"]]
    if len(recipe_case_ids) != 8 or duplicates(recipe_case_ids) or len(recipe_holdout_ids) != 4 or duplicates(recipe_holdout_ids) or set(recipe_case_ids) & set(recipe_holdout_ids): recipe_errors.append("Recipe authored/holdout corpus invalid")
    if recipe_holdouts.get("execution_state") != "not-run-phase-9" or recipe_eval.get("execution_state") != "not-run-phase-9" or recipe_eval.get("status") != "planned": recipe_errors.append("Recipe evidence falsely claims execution")
    if set(recipe_eval["authored_case_ids"]) != set(recipe_case_ids) or set(recipe_eval["holdout_case_ids"]) != set(recipe_holdout_ids) or recipe_eval["candidate_sha256"] != sha(recipe_path): recipe_errors.append("Recipe evaluation plan stale")
    if len(recipe_eval["mutations"]) != 2: recipe_errors.append("Recipe mutations missing")
    if recipe_eval.get("baseline") != {"identity": "design-web-flow@1.0.0", "kind": "released-v1-recipe"}: recipe_errors.append("Recipe baseline identity mismatch")
    baseline_recipe = workspace / "recipes/design-web-flow.json"
    if not baseline_recipe.is_file() or load(baseline_recipe).get("status") != "released" or load(baseline_recipe).get("version") != "1.0.0": recipe_errors.append("Recipe baseline is not released at exact version")
    if {item.get("remove_step") for item in recipe_eval["mutations"] if "remove_step" in item} != {"review-evidence"}: recipe_errors.append("Recipe rendered-evidence mutation target mismatch")
    if {item.get("remove_checkpoint") for item in recipe_eval["mutations"] if "remove_checkpoint" in item} != {"authorize source remediation separately from every review finding"}: recipe_errors.append("Recipe human-authority mutation target mismatch")
    add("conditional-ui-recipe", recipe_errors)

    semantic_errors = []
    semantic_path = schema_root / "semantic-review.json"
    if semantic_path.is_file():
        semantic = load(semantic_path)
        if semantic.get("status") != "passed" or semantic.get("reviewed_candidate_count") != 17 or semantic.get("open_findings") != []: semantic_errors.append("semantic review status/count/open findings mismatch")
        if len(semantic.get("boundary_samples", [])) < 8 or any(item.get("verdict") != "passed" for item in semantic.get("boundary_samples", [])): semantic_errors.append("semantic review boundary samples incomplete")
    else: semantic_errors.append("semantic-review.json missing")
    add("semantic-boundary-review", semantic_errors)

    errors = [f"{check['name']}: {error}" for check in checks for error in check["errors"]]
    return {"gate": "capability-compiler-v2-phase-4", "ok": not errors, "checks": checks, "counts": {"skills": len(expected), "authored_trigger_cases": len(all_cases), "holdout_cases": len(holdout_ids), "planned_skill_mutations": sum(len(docs["evaluation-plan.json"]["mutations"]) for docs in documents.values()), "recipes": 1, "recipe_authored_cases": len(recipe_case_ids), "recipe_holdout_cases": len(recipe_holdout_ids), "recipe_mutations": len(recipe_eval["mutations"])}, "errors": errors}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__); parser.add_argument("--workspace-root", type=Path, default=Path(".")); parser.add_argument("--output", type=Path); args = parser.parse_args()
    result = verify(args.workspace_root)
    if args.output:
        path = args.output if args.output.is_absolute() else args.workspace_root / args.output; path.parent.mkdir(parents=True, exist_ok=True); path.write_text(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps(result, ensure_ascii=False, sort_keys=True)); return 0 if result["ok"] else 1


if __name__ == "__main__": raise SystemExit(main())
