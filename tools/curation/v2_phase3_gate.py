#!/usr/bin/env python3
"""Fail-closed gate for Phase 3 product-discovery and requirements candidate Skills."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from collections import Counter
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

try:
    from tools.curation.v2_phase2_gate import verify as verify_phase2
except ModuleNotFoundError:
    from v2_phase2_gate import verify as verify_phase2

VERSION = "0.1.0-v2-candidate"
PHASE2_TREE = "57ff1aec49b2b7b370d74d36e52659d7338adf2f16260fe62be7ada870472601"
REQUIRED_FILES = {"SKILL.md", "contract.json", "provenance.json", "trigger-cases.json", "evaluation-plan.json"}
REQUIRED_SECTIONS = {"Responsibility", "Trigger", "Required Inputs", "Procedure", "Output Contract", "Hard Gates", "Status Mapping", "Non-Responsibilities"}
GENERIC_CASE_INPUTS = {
    "The request lacks a source, scope, or decision owner needed to preserve traceability.",
    "The request asks the Skill to make or execute a decision outside its authority.",
}


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes().replace(b"\r\n", b"\n")).hexdigest()


def duplicate_values(values: list[str]) -> set[str]:
    return {value for value, count in Counter(values).items() if count > 1}


def headings(markdown: str) -> set[str]:
    return {match.group(1).strip() for match in re.finditer(r"^## (.+)$", markdown, re.MULTILINE)}


def verify(workspace: Path) -> dict[str, Any]:
    workspace = workspace.resolve(); checks: list[dict[str, Any]] = []
    def add(name: str, errors: list[str]) -> None: checks.append({"name": name, "ok": not errors, "errors": errors})

    phase2 = verify_phase2(workspace)
    add("phase-2-and-source-v1-compatibility", [] if phase2["ok"] else phase2["errors"])
    phase2_manifest = load(workspace / ".specs/capability-compiler-v2/phase-2/artifact-manifest.json")
    identity_errors = [] if phase2_manifest["tree_sha256"] == PHASE2_TREE else ["Phase 2 artifact tree identity changed"]
    add("phase-2-artifact-identity", identity_errors)

    ownership = load(workspace / "curation/v2/lifecycle/phase-ownership.json")["phases"]["3"]
    expected_ids = {item.removeprefix("capability:") for item in ownership}
    candidate_root = workspace / "evals/candidates/capability-compiler-v2/phase-3"
    catalog = load(candidate_root / "catalog.json")
    catalog_ids = [item["id"] for item in catalog["skills"]]
    candidate_dirs = {path.name for path in (candidate_root / "skills").iterdir() if path.is_dir()}
    inventory_errors: list[str] = []
    if len(expected_ids) != 31: inventory_errors.append(f"expected 31 Phase 3 ownership IDs, got {len(expected_ids)}")
    if set(catalog_ids) != expected_ids or duplicate_values(catalog_ids): inventory_errors.append("catalog IDs do not exactly equal Phase 3 ownership")
    if candidate_dirs != expected_ids: inventory_errors.append(f"candidate directories mismatch missing={sorted(expected_ids-candidate_dirs)} extra={sorted(candidate_dirs-expected_ids)}")
    if catalog.get("skill_count") != 31 or catalog.get("version") != VERSION or catalog.get("status") != "evaluating": inventory_errors.append("catalog count/version/status mismatch")
    for item in catalog["skills"]:
        if item.get("status") != "evaluating" or item.get("version") != VERSION: inventory_errors.append(f"catalog item is not evaluating at frozen version: {item.get('id')}")
    add("phase-3-candidate-inventory", inventory_errors)

    schema_root = workspace / "curation/v2/phase-3"
    validators = {name: Draft202012Validator(load(schema_root / name)) for name in ["candidate-skill.schema.json", "provenance.schema.json", "trigger-cases.schema.json", "evaluation-plan.schema.json"]}
    designs_doc = load(schema_root / "designs.json"); designs = {item["skill_id"]: item for item in designs_doc["designs"]}
    schema_errors: list[str] = []
    all_cases: list[dict[str, Any]] = []; candidates: dict[str, dict[str, Any]] = {}
    for skill_id in sorted(expected_ids):
        directory = candidate_root / "skills" / skill_id
        if not directory.is_dir():
            schema_errors.append(f"{skill_id}: missing candidate directory"); continue
        present = {path.name for path in directory.iterdir() if path.is_file()}
        if present != REQUIRED_FILES: schema_errors.append(f"{skill_id}: candidate files mismatch {sorted(present)}"); continue
        files = {"contract.json": "candidate-skill.schema.json", "provenance.json": "provenance.schema.json", "trigger-cases.json": "trigger-cases.schema.json", "evaluation-plan.json": "evaluation-plan.schema.json"}
        documents = {}
        for filename, schema_name in files.items():
            document = load(directory / filename); documents[filename] = document
            for error in validators[schema_name].iter_errors(document):
                location = ".".join(str(part) for part in error.absolute_path)
                schema_errors.append(f"{skill_id}/{filename}:{location or '<root>'}: {error.message}")
        candidates[skill_id] = documents
        contract = documents["contract.json"]; provenance = documents["provenance.json"]; triggers = documents["trigger-cases.json"]; evaluation = documents["evaluation-plan.json"]
        if any(document.get("id", document.get("skill_id")) != skill_id for document in (contract, provenance, triggers, evaluation)): schema_errors.append(f"{skill_id}: internal candidate IDs disagree")
        skill_text = (directory / "SKILL.md").read_text(encoding="utf-8")
        missing_sections = REQUIRED_SECTIONS - headings(skill_text)
        if missing_sections: schema_errors.append(f"{skill_id}: missing SKILL sections {sorted(missing_sections)}")
        if contract["responsibility"] != designs[skill_id]["trigger"]: schema_errors.append(f"{skill_id}: contract responsibility is not the semantic design")
        if contract["hard_gates"][0] != designs[skill_id]["distinctive_gate"]: schema_errors.append(f"{skill_id}: distinctive gate not first in contract")
        if designs[skill_id]["distinctive_gate"] not in skill_text: schema_errors.append(f"{skill_id}: distinctive gate absent from SKILL.md")
        expected_tools = ["read"] if contract["permission_identity"] == "read-only" else ["read", "write"]
        expected_scope = "none" if contract["permission_identity"] == "read-only" else "run-output"
        if contract["execution"]["model_tools"] != expected_tools or contract["execution"]["mutation_scope"] != expected_scope: schema_errors.append(f"{skill_id}: execution identity mismatch")
        if contract["execution"]["remote_write"] is not False: schema_errors.append(f"{skill_id}: remote write must be false")
        if provenance["phase2_artifact_tree_sha256"] != PHASE2_TREE: schema_errors.append(f"{skill_id}: stale Phase 2 identity")
        file_hashes = provenance["candidate_files"]
        for filename, expected_hash in file_hashes.items():
            if sha(directory / filename) != expected_hash: schema_errors.append(f"{skill_id}: candidate hash mismatch {filename}")
        if evaluation["candidate"]["skill_sha256"] != sha(directory / "SKILL.md") or evaluation["candidate"]["contract_sha256"] != sha(directory / "contract.json"): schema_errors.append(f"{skill_id}: evaluation candidate hashes stale")
        all_cases.extend(triggers["cases"])
    add("candidate-schemas-contracts-and-hashes", schema_errors)

    provenance_errors: list[str] = []
    fusion_ids = {json.loads(line)["id"] for line in (workspace / "curation/v2/fusion/decisions.jsonl").read_text(encoding="utf-8").splitlines() if line.strip()}
    for skill_id, documents in candidates.items():
        provenance = documents["provenance.json"]; capability = load(workspace / f"curation/v2/capabilities/{skill_id}.json")
        for field in ["source_cluster_ids", "canonical_unit_ids", "retained_auxiliary_unit_ids", "root_derived_atom_ids", "source_fragment_ids", "fusion_decision_ids", "decision_references", "source_evidence", "source_defect_refs"]:
            if provenance[field] != capability[field]: provenance_errors.append(f"{skill_id}: provenance mismatch {field}")
        missing_fusion = set(provenance["fusion_decision_ids"]) - fusion_ids
        if missing_fusion: provenance_errors.append(f"{skill_id}: unknown fusion decisions {sorted(missing_fusion)}")
    add("provenance-set-equality", provenance_errors)

    trigger_errors: list[str] = []
    case_ids = [case["id"] for case in all_cases]
    if duplicate_values(case_ids): trigger_errors.append(f"duplicate authored case IDs: {sorted(duplicate_values(case_ids))}")
    for skill_id, documents in candidates.items():
        cases = documents["trigger-cases.json"]["cases"]; counts = Counter(case["kind"] for case in cases)
        if counts != {"should-trigger": 2, "should-not-trigger": 2, "boundary": 1, "authority-stop": 1}: trigger_errors.append(f"{skill_id}: authored case shape mismatch {dict(counts)}")
        for case in cases:
            if case["input"] in GENERIC_CASE_INPUTS: trigger_errors.append(f"{case['id']}: generic placeholder input")
            if case["kind"] == "should-trigger" and (case["expected_skill_id"] != skill_id or skill_id in case["forbidden_skill_ids"]): trigger_errors.append(f"{case['id']}: invalid positive routing")
            if case["kind"] == "should-not-trigger" and (case["expected_skill_id"] == skill_id or skill_id not in case["forbidden_skill_ids"]): trigger_errors.append(f"{case['id']}: invalid anti-routing")
            if case["expected_skill_id"] and case["expected_skill_id"] not in expected_ids and not (workspace / f"curation/v2/capabilities/{case['expected_skill_id']}.json").is_file(): trigger_errors.append(f"{case['id']}: unknown expected route {case['expected_skill_id']}")
    holdout = load(candidate_root / "holdout-cases.json"); holdout_cases = holdout["cases"]
    holdout_ids = [case["id"] for case in holdout_cases]
    if holdout.get("execution_state") != "not-run-phase-9" or holdout.get("case_count") != 62 or len(holdout_cases) != 62: trigger_errors.append("holdout corpus identity/count/state mismatch")
    if duplicate_values(holdout_ids) or set(holdout_ids) & set(case_ids): trigger_errors.append("holdout IDs duplicate or overlap authored cases")
    for skill_id, documents in candidates.items():
        planned = set(documents["evaluation-plan.json"]["holdout_case_ids"])
        owned = {case["id"] for case in holdout_cases if case["id"].startswith(f"V2-P3-{skill_id}-holdout-")}
        if planned != owned or len(owned) != 2: trigger_errors.append(f"{skill_id}: holdout plan/corpus mismatch")
    add("trigger-and-holdout-boundaries", trigger_errors)

    policy_errors: list[str] = []
    for skill_id, documents in candidates.items():
        contract = documents["contract.json"]; text = (candidate_root / "skills" / skill_id / "SKILL.md").read_text(encoding="utf-8")
        policy = contract["policy"]
        if policy["data_governance"] and "## Data Governance" not in text: policy_errors.append(f"{skill_id}: missing data-governance section")
        if policy["named_formula_variants"] and ("## Named Formula Variants" not in text or not all(term in text for term in ("RICE", "ICE", "Opportunity Score", "exact formula variant"))): policy_errors.append(f"{skill_id}: named formula variant policy incomplete")
        if policy["human_decision"] and ("## Human Decision Authority" not in text or "remain human decisions" not in text): policy_errors.append(f"{skill_id}: human authority policy incomplete")
        if contract["permission_identity"] == "read-only" and contract["execution"]["mutation_scope"] != "none": policy_errors.append(f"{skill_id}: read-only candidate can mutate")
        if any(term in text for term in ("we deployed", "deployment completed", "PR created", "merge completed")): policy_errors.append(f"{skill_id}: unsupported external action claim")
    add("product-formula-data-and-authority-policy", policy_errors)

    evaluation_errors: list[str] = []
    for skill_id, documents in candidates.items():
        evaluation = documents["evaluation-plan.json"]; directory = candidate_root / "skills" / skill_id; skill_text = (directory / "SKILL.md").read_text(encoding="utf-8")
        if evaluation["execution_state"] != "not-run-phase-9" or evaluation["status"] != "planned": evaluation_errors.append(f"{skill_id}: evaluation falsely claims execution")
        baseline = evaluation["baseline"]
        if baseline["kind"] == "released-v1-slot":
            baseline_id, baseline_version = baseline["identity"].rsplit("@", 1); baseline_path = workspace / f"slots/{baseline_id}/contract.json"
            if not baseline_path.is_file(): evaluation_errors.append(f"{skill_id}: missing released baseline")
            else:
                baseline_contract = load(baseline_path)
                if baseline_contract.get("status") != "released" or baseline_contract.get("version") != baseline_version: evaluation_errors.append(f"{skill_id}: baseline is not released at claimed version")
        elif baseline["kind"] == "source-skill" and not (workspace / "skills" / baseline["identity"] / "SKILL.md").is_file(): evaluation_errors.append(f"{skill_id}: missing source baseline {baseline['identity']}")
        for mutation in evaluation["mutations"]:
            marker = mutation["remove_exact_text"]
            if skill_text.count(marker) != 1: evaluation_errors.append(f"{mutation['id']}: semantic marker must occur exactly once")
            mutated = skill_text.replace(marker, "")
            if marker in mutated or marker not in designs[skill_id]["distinctive_gate"]: evaluation_errors.append(f"{mutation['id']}: mutation detector cannot attribute the removed gate")
    add("evaluation-plans-and-mutation-detection", evaluation_errors)

    semantic_errors: list[str] = []
    semantic = load(schema_root / "semantic-review.json")
    if semantic.get("status") != "passed" or semantic.get("reviewed_candidate_count") != 31: semantic_errors.append("semantic review status/count mismatch")
    if semantic.get("open_findings") != []: semantic_errors.append("semantic review has open findings")
    sample_ids = [item["id"] for item in semantic.get("boundary_samples", [])]
    if len(sample_ids) != 8 or duplicate_values(sample_ids) or any(item.get("verdict") != "passed" for item in semantic.get("boundary_samples", [])): semantic_errors.append("eight unique boundary samples must pass")
    if len(semantic.get("resolved_findings", [])) < 4: semantic_errors.append("semantic review must preserve resolved corrections")
    if semantic.get("release_claim") != "none; all 31 candidates remain evaluating and all evaluation plans remain not-run-phase-9": semantic_errors.append("semantic review release claim is unsafe")
    add("semantic-boundary-review", semantic_errors)

    errors = [f"{check['name']}: {error}" for check in checks for error in check["errors"]]
    return {"gate": "capability-compiler-v2-phase-3", "ok": not errors, "checks": checks, "counts": {"skills": len(expected_ids), "authored_trigger_cases": len(all_cases), "holdout_cases": len(holdout_cases), "planned_mutations": sum(len(documents["evaluation-plan.json"]["mutations"]) for documents in candidates.values())}, "errors": errors}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__); parser.add_argument("--workspace-root", type=Path, default=Path(".")); parser.add_argument("--output", type=Path); args = parser.parse_args()
    result = verify(args.workspace_root)
    if args.output:
        path = args.output if args.output.is_absolute() else args.workspace_root / args.output; path.parent.mkdir(parents=True, exist_ok=True); path.write_text(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps(result, ensure_ascii=False, sort_keys=True)); return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
