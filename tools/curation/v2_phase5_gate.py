#!/usr/bin/env python3
"""Fail-closed gate for Phase 5 architecture, data, authorization, and security candidates."""
from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

try:
    from tools.curation.v2_phase4_gate import verify as verify_phase4
except ModuleNotFoundError:
    from v2_phase4_gate import verify as verify_phase4

VERSION = "0.1.0-v2-candidate"
PRIOR_TREES = {"phase2": "57ff1aec49b2b7b370d74d36e52659d7338adf2f16260fe62be7ada870472601", "phase3": "de60929ce7eb1877ffb64a9e8cd671beec389b433f843e10320701c890de8965", "phase4": "968fd1e2175bdc35d77a4d9025a88ab35e5f096fba353137dbf9770e030d4695"}
REQUIRED_FILES = {"SKILL.md", "contract.json", "provenance.json", "trigger-cases.json", "evaluation-plan.json"}
AUTHORIZED_WORKSPACE = {"ci-pipeline-security-hardening", "frontend-runtime-boundaries-and-dependency-safety"}
NO_MUTATION = {"ai-safety-and-action-governance", "engineering-plan-review"}
ARTIFACT_ONLY = {"security-audit-and-threat-modeling"}
RUN_OUTPUT = {
    "ai-agent-autonomy-and-human-control", "ai-capability-architecture-and-autonomy", "ai-model-and-data-architecture",
    "architecture-candidate-reporting", "architecture-deep-module-design", "architecture-deepening-discovery",
    "architecture-interface-alternative-evaluation", "authorization-and-permission-contracts", "data-and-api-contract-design",
    "diagram-and-architecture-artifact-generation", "secrets-and-environment-governance",
}
REQUIRED_COVERAGE = {
    "action-classes", "graduated-autonomy", "human-checkpoint", "interruption", "rollback", "revocation", "fallback",
    "specialist-routing", "model-routing", "data-rights", "lineage", "freshness", "evaluation", "prompt-injection",
    "data-exfiltration", "tool-abuse", "default-deny", "information-hiding", "dependency-direction", "migration-rollback",
    "independent-alternatives", "subject-resource-action-context", "tenant-isolation", "server-enforcement", "negative-cases",
    "least-privilege", "immutable-pinning", "untrusted-input", "secret-isolation", "artifact-provenance", "schema-invariants",
    "compatibility", "validation-errors", "pagination", "idempotency", "concurrency", "authorization-hooks", "node-edge-provenance",
    "trust-boundary", "data-migration", "failure-modes", "operability", "client-server-boundary", "no-client-secret",
    "dependency-safety", "no-secret-values", "environment-separation", "rotation", "revocation", "authorized-local-check",
    "reproducible-finding", "severity-rationale", "no-remediation",
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

    prior = verify_phase4(workspace); add("phase-4-and-earlier-compatibility", [] if prior["ok"] else prior["errors"])
    identity_errors = []
    for phase, identity in PRIOR_TREES.items():
        actual = load(workspace / f".specs/capability-compiler-v2/{phase.replace('phase','phase-')}/artifact-manifest.json")["tree_sha256"]
        if actual != identity: identity_errors.append(f"{phase} artifact identity changed")
    add("prior-phase-artifact-identities", identity_errors)

    candidate_root = workspace / "evals/candidates/capability-compiler-v2/phase-5"; schema_root = workspace / "curation/v2/phase-5"
    expected = {item.removeprefix("capability:") for item in load(workspace / "curation/v2/lifecycle/phase-ownership.json")["phases"]["5"]}
    catalog = load(candidate_root / "catalog.json"); catalog_ids = [item["id"] for item in catalog["skills"]]; dirs = {path.name for path in (candidate_root / "skills").iterdir() if path.is_dir()}
    inventory_errors = []
    if len(expected) != 16: inventory_errors.append(f"expected 16 Phase 5 IDs, got {len(expected)}")
    if set(catalog_ids) != expected or duplicates(catalog_ids): inventory_errors.append("catalog IDs do not exactly equal ownership")
    if dirs != expected: inventory_errors.append(f"candidate directories mismatch missing={sorted(expected-dirs)} extra={sorted(dirs-expected)}")
    if catalog.get("skill_count") != 16 or catalog.get("version") != VERSION or catalog.get("status") != "evaluating": inventory_errors.append("catalog count/version/status mismatch")
    add("phase-5-candidate-inventory", inventory_errors)

    validators = {name: Draft202012Validator(load(schema_root / name)) for name in ["candidate-skill.schema.json", "provenance.schema.json", "trigger-cases.schema.json", "evaluation-plan.schema.json"]}
    designs = {item["skill_id"]: item for item in load(schema_root / "designs.json")["designs"]}; documents: dict[str, dict[str, Any]] = {}; all_cases = []; schema_errors = []
    for skill_id in sorted(expected):
        directory = candidate_root / "skills" / skill_id
        if not directory.is_dir(): schema_errors.append(f"{skill_id}: missing directory"); continue
        present = {path.name for path in directory.iterdir() if path.is_file()}
        if present != REQUIRED_FILES: schema_errors.append(f"{skill_id}: file set mismatch {sorted(present)}"); continue
        docs = {}
        for filename, schema_name in {"contract.json": "candidate-skill.schema.json", "provenance.json": "provenance.schema.json", "trigger-cases.json": "trigger-cases.schema.json", "evaluation-plan.json": "evaluation-plan.schema.json"}.items():
            doc = load(directory / filename); docs[filename] = doc
            for error in validators[schema_name].iter_errors(doc): schema_errors.append(f"{skill_id}/{filename}:{'.'.join(map(str,error.absolute_path)) or '<root>'}: {error.message}")
        documents[skill_id] = docs; contract = docs["contract.json"]; provenance = docs["provenance.json"]; evaluation = docs["evaluation-plan.json"]
        if any(doc.get("id", doc.get("skill_id")) != skill_id for doc in docs.values()): schema_errors.append(f"{skill_id}: internal IDs disagree")
        if contract["responsibility"] != designs[skill_id]["trigger"] or contract["hard_gates"][0] != designs[skill_id]["distinctive_gate"]: schema_errors.append(f"{skill_id}: semantic design not preserved")
        if contract["policy"]["coverage"] != designs[skill_id]["coverage"]: schema_errors.append(f"{skill_id}: semantic coverage markers changed")
        text = (directory / "SKILL.md").read_text(encoding="utf-8")
        if text.count(designs[skill_id]["distinctive_gate"]) != 1: schema_errors.append(f"{skill_id}: distinctive marker count mismatch")
        for filename, expected_hash in provenance["candidate_files"].items():
            if sha(directory / filename) != expected_hash: schema_errors.append(f"{skill_id}: stale hash {filename}")
        if evaluation["candidate"]["skill_sha256"] != sha(directory / "SKILL.md") or evaluation["candidate"]["contract_sha256"] != sha(directory / "contract.json"): schema_errors.append(f"{skill_id}: stale evaluation hashes")
        all_cases.extend(docs["trigger-cases.json"]["cases"])
    add("candidate-schemas-semantic-design-and-hashes", schema_errors)

    provenance_errors = []
    for skill_id, docs in documents.items():
        provenance = docs["provenance.json"]; capability = load(workspace / f"curation/v2/capabilities/{skill_id}.json")
        if provenance["prior_artifact_trees"] != PRIOR_TREES: provenance_errors.append(f"{skill_id}: prior artifact identities mismatch")
        for field in ["source_cluster_ids", "canonical_unit_ids", "retained_auxiliary_unit_ids", "root_derived_atom_ids", "source_fragment_ids", "fusion_decision_ids", "decision_references", "source_evidence", "source_defect_refs"]:
            if provenance[field] != capability[field]: provenance_errors.append(f"{skill_id}: provenance mismatch {field}")
        baseline = docs["evaluation-plan.json"]["baseline"]
        roots = {evidence.split("/", 1)[0] for evidence in capability["source_evidence"] if "/" in evidence}
        if baseline["kind"] == "source-skill" and (baseline["identity"] not in roots or not (workspace / "skills" / baseline["identity"] / "SKILL.md").is_file()): provenance_errors.append(f"{skill_id}: baseline is not a real provenance root")
        if baseline["kind"] == "no-capability-baseline" and roots: provenance_errors.append(f"{skill_id}: no-baseline claim ignores source roots")
    add("provenance-and-baseline-integrity", provenance_errors)

    permission_errors = []; identities = {item["id"]: item for item in load(workspace / "curation/v2/lifecycle/permission-identities.json")["identities"]}
    if AUTHORIZED_WORKSPACE | NO_MUTATION | ARTIFACT_ONLY | RUN_OUTPUT != expected: permission_errors.append("mutation allowlists do not cover ownership exactly")
    for skill_id, docs in documents.items():
        contract = docs["contract.json"]; execution = contract["execution"]; identity = identities[contract["permission_identity"]]
        if execution["model_tools"] != identity["model_tools"] or execution["host_actions"] != identity["host_actions"] or execution["external"] != identity["external"] or execution["remote_write"] is not False: permission_errors.append(f"{skill_id}: permission identity mismatch")
        expected_scope = "authorized-workspace" if skill_id in AUTHORIZED_WORKSPACE else ("none" if skill_id in NO_MUTATION else ("artifact-output" if skill_id in ARTIFACT_ONLY else "run-output"))
        if execution["mutation_scope"] != expected_scope: permission_errors.append(f"{skill_id}: mutation scope must be {expected_scope}")
        if skill_id in NO_MUTATION | ARTIFACT_ONLY and any(tool in execution["model_tools"] for tool in ["edit", "write"]): permission_errors.append(f"{skill_id}: review/audit has write tools")
        if skill_id == "security-audit-and-threat-modeling" and execution["host_actions"] != ["approved-local-commands"]: permission_errors.append("security audit local-exec scope mismatch")
    add("permission-source-audit-separation", permission_errors)

    case_errors = []; authored_ids = [case["id"] for case in all_cases]
    if duplicates(authored_ids): case_errors.append(f"duplicate authored IDs {sorted(duplicates(authored_ids))}")
    for skill_id, docs in documents.items():
        cases = docs["trigger-cases.json"]["cases"]; counts = Counter(case["kind"] for case in cases)
        if counts != {"should-trigger": 2, "should-not-trigger": 2, "boundary": 1, "authority-stop": 1}: case_errors.append(f"{skill_id}: case shape mismatch {dict(counts)}")
        for case in cases:
            if case["kind"] == "should-trigger" and case["expected_skill_id"] != skill_id: case_errors.append(f"{case['id']}: positive misroute")
            if case["kind"] == "should-not-trigger" and (case["expected_skill_id"] == skill_id or skill_id not in case["forbidden_skill_ids"]): case_errors.append(f"{case['id']}: anti-route invalid")
            target = case["expected_skill_id"]
            if target and target not in expected and not (workspace / f"curation/v2/capabilities/{target}.json").is_file(): case_errors.append(f"{case['id']}: unknown route {target}")
    holdout = load(candidate_root / "holdout-cases.json"); holdout_ids = [case["id"] for case in holdout["cases"]]
    if holdout.get("case_count") != 32 or len(holdout_ids) != 32 or holdout.get("execution_state") != "not-run-phase-9": case_errors.append("holdout count/state mismatch")
    if duplicates(holdout_ids) or set(holdout_ids) & set(authored_ids): case_errors.append("holdout IDs duplicate or overlap authored cases")
    for skill_id, docs in documents.items():
        planned = set(docs["evaluation-plan.json"]["holdout_case_ids"]); owned = {item for item in holdout_ids if item.startswith(f"V2-P5-{skill_id}-holdout-")}
        if planned != owned or len(owned) != 2: case_errors.append(f"{skill_id}: holdout mismatch")
    add("trigger-and-holdout-boundaries", case_errors)

    security_errors = []; aggregate = {marker for docs in documents.values() for marker in docs["contract.json"]["policy"]["coverage"]}; missing = REQUIRED_COVERAGE - aggregate
    if missing: security_errors.append(f"missing required coverage {sorted(missing)}")
    critical_by_skill = {
        "ai-agent-autonomy-and-human-control": {"graduated-autonomy", "human-checkpoint", "interruption", "rollback", "revocation"},
        "ai-safety-and-action-governance": {"prompt-injection", "data-exfiltration", "tool-abuse", "default-deny"},
        "authorization-and-permission-contracts": {"subject-resource-action-context", "default-deny", "tenant-isolation", "server-enforcement", "negative-cases"},
        "ci-pipeline-security-hardening": {"least-privilege", "immutable-pinning", "untrusted-input", "secret-isolation", "artifact-provenance"},
        "data-and-api-contract-design": {"schema-invariants", "compatibility", "idempotency", "concurrency", "authorization-hooks", "rollback"},
        "frontend-runtime-boundaries-and-dependency-safety": {"client-server-boundary", "no-client-secret", "server-enforcement", "dependency-safety"},
        "secrets-and-environment-governance": {"no-secret-values", "environment-separation", "rotation", "revocation", "leak-response"},
        "security-audit-and-threat-modeling": {"trust-boundary", "authorized-local-check", "reproducible-finding", "severity-rationale", "no-remediation", "no-secret-values"},
    }
    for skill_id, docs in documents.items():
        contract = docs["contract.json"]; text = (candidate_root / "skills" / skill_id / "SKILL.md").read_text(encoding="utf-8")
        absent = critical_by_skill.get(skill_id, set()) - set(contract["policy"]["coverage"])
        if absent: security_errors.append(f"{skill_id}: missing critical coverage {sorted(absent)}")
        if "Never access or emit secret values" not in text: security_errors.append(f"{skill_id}: secret-value prohibition missing")
        if contract["policy"]["data_governance"] and "## Data and Secret Governance" not in text: security_errors.append(f"{skill_id}: data-governance section missing")
        if contract["policy"]["human_decision"] and "## Human Architecture and Risk Authority" not in text: security_errors.append(f"{skill_id}: human authority section missing")
        if "Review, reporting, and audit candidates never repair source" not in text: security_errors.append(f"{skill_id}: audit/remediation separation missing")
    add("architecture-security-and-secret-invariants", security_errors)

    evaluation_errors = []
    for skill_id, docs in documents.items():
        evaluation = docs["evaluation-plan.json"]; text = (candidate_root / "skills" / skill_id / "SKILL.md").read_text(encoding="utf-8")
        if evaluation["status"] != "planned" or evaluation["execution_state"] != "not-run-phase-9": evaluation_errors.append(f"{skill_id}: false evaluation claim")
        for mutation in evaluation["mutations"]:
            marker = mutation["remove_exact_text"]
            if text.count(marker) != 1 or marker != designs[skill_id]["distinctive_gate"]: evaluation_errors.append(f"{mutation['id']}: invalid mutation marker")
    add("evaluation-plans-and-semantic-mutations", evaluation_errors)

    semantic_errors = []; semantic_path = schema_root / "semantic-review.json"
    if not semantic_path.is_file(): semantic_errors.append("semantic-review.json missing")
    else:
        semantic = load(semantic_path)
        if semantic.get("status") != "passed" or semantic.get("reviewed_candidate_count") != 16 or semantic.get("open_findings") != []: semantic_errors.append("semantic review status/count/open findings mismatch")
        if len(semantic.get("boundary_samples", [])) < 8 or any(item.get("verdict") != "passed" for item in semantic.get("boundary_samples", [])): semantic_errors.append("semantic boundary samples incomplete")
    add("semantic-boundary-review", semantic_errors)

    errors = [f"{check['name']}: {error}" for check in checks for error in check["errors"]]
    return {"gate": "capability-compiler-v2-phase-5", "ok": not errors, "checks": checks, "counts": {"skills": len(expected), "authored_trigger_cases": len(all_cases), "holdout_cases": len(holdout_ids), "planned_mutations": sum(len(docs["evaluation-plan.json"]["mutations"]) for docs in documents.values())}, "errors": errors}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__); parser.add_argument("--workspace-root", type=Path, default=Path(".")); parser.add_argument("--output", type=Path); args = parser.parse_args(); result = verify(args.workspace_root)
    if args.output:
        path = args.output if args.output.is_absolute() else args.workspace_root / args.output; path.parent.mkdir(parents=True, exist_ok=True); path.write_text(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps(result, ensure_ascii=False, sort_keys=True)); return 0 if result["ok"] else 1


if __name__ == "__main__": raise SystemExit(main())
