#!/usr/bin/env python3
"""Fail-closed gate for 39 Phase 7 delivery, observability, incident, and learning candidates."""
from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

try:
    from tools.curation.v2_phase6_gate import verify as verify_phase6
except ModuleNotFoundError:
    from v2_phase6_gate import verify as verify_phase6

VERSION = "0.1.0-v2-candidate"
PRIOR_TREES = {
    "phase2": "57ff1aec49b2b7b370d74d36e52659d7338adf2f16260fe62be7ada870472601",
    "phase3": "de60929ce7eb1877ffb64a9e8cd671beec389b433f843e10320701c890de8965",
    "phase4": "968fd1e2175bdc35d77a4d9025a88ab35e5f096fba353137dbf9770e030d4695",
    "phase5": "7b39fb29c0a25a4a97243e9a857840d14541a9f839e550970c29cc014122e1ee",
    "phase6": "7e8ff8c23ede16d189a9c89d141e2fee87df63251d5d27ec40aa40eef1d24561",
}
REQUIRED_FILES = {"SKILL.md", "contract.json", "provenance.json", "trigger-cases.json", "evaluation-plan.json"}
REMOTE_WRITERS = {
    "ai-observability-configuration", "apm-instrumentation-enablement", "deployment-trigger-execution", "edge-worker-deployment",
    "kubernetes-application-deployment", "log-observability-configuration", "monitoring-and-alert-configuration",
    "observability-agent-installation", "pull-request-comment-response", "release-observability-configuration",
    "release-rollback-execution", "remote-git-push", "remote-pull-request-change", "remote-pull-request-merge",
    "service-identity-remapping", "web-hosting-deployment",
}
OBSERVERS = {
    "apm-instrumentation-troubleshooting", "apm-instrumentation-verification", "canary-baseline-management",
    "cloud-reliability-assessment", "deployment-observation", "error-monitoring-issue-investigation",
    "incident-response-coordination", "kubernetes-deployment-readiness", "metrics-system-and-observability",
    "production-canary-monitoring", "production-llm-trace-root-cause-analysis", "production-trace-classification",
}
PREFLIGHTS = {"change-delivery-preflight", "merge-and-deploy-readiness"}
NO_MUTATION = {"apm-onboarding-summary", "engineering-retrospective-and-improvement", "feedback-and-continuous-learning-loop", "source-metadata-and-provenance"}
SOURCE_WRITERS = {"change-packaging-and-versioning", "deployment-environment-setup", "release-documentation-maintenance"}
LOCAL_SYSTEM_WRITERS = {"local-learning-persistence"}
CRITICAL_COVERAGE = {
    "change-delivery-preflight": {"branch-ref-identity", "merge-base", "automation-stops", "no-remote-mutation"},
    "change-packaging-and-versioning": {"local-only", "bisectable-commits", "version", "changelog", "no-push"},
    "merge-and-deploy-readiness": {"fresh-readiness", "exact-PR", "separate-merge-deploy", "no-mutation"},
    "remote-git-push": {"exact-refspec", "non-force", "expected-remote-SHA", "push-receipt", "no-PR-action"},
    "remote-pull-request-change": {"verified-pushed-ref", "exact-base-head", "redaction", "PR-receipt", "no-merge"},
    "remote-pull-request-merge": {"exact-PR-head", "fresh-readiness", "allowed-merge-method", "merge-receipt", "no-deploy"},
    "deployment-trigger-execution": {"exact-target", "artifact-digest", "frozen-parameters", "idempotency", "trigger-receipt", "cancellation"},
    "deployment-observation": {"deployment-identity", "observation-window", "current-signals", "read-only", "rollback-recommendation-not-action"},
    "release-rollback-execution": {"exact-recovery-target", "rollback-condition", "current-evidence", "migration-compatibility", "blast-radius", "rollback-receipt"},
    "kubernetes-deployment-readiness": {"read-only", "cluster-namespace", "rollback-readiness", "no-apply"},
    "kubernetes-application-deployment": {"cluster-namespace", "manifest-hash", "image-digest", "server-dry-run", "rollback-revision"},
    "web-hosting-deployment": {"provider-project", "environment", "artifact-digest", "health-gate", "rollback-target"},
    "edge-worker-deployment": {"immutable-worker", "bindings", "routes", "limits", "rollback-target"},
    "ai-observability-configuration": {"telemetry-schema", "minimization", "redaction", "sampling", "retention", "deletion"},
    "log-observability-configuration": {"exact-log-sources", "parsing", "routing", "redaction", "retention", "volume-cost", "deletion"},
    "monitoring-and-alert-configuration": {"SLO-threshold", "window", "missing-data", "actionable-owner", "deduplication", "rollback"},
    "observability-agent-installation": {"pinned-agent", "exact-targets", "least-privilege", "health", "uninstall", "rollback"},
    "production-canary-monitoring": {"immutable-baseline", "allowlisted-production", "noise-control", "no-auto-rollback"},
    "incident-response-coordination": {"severity", "roles", "fact-hypothesis", "mitigation-first", "separate-action-owner", "no-provider-mutation"},
    "engineering-retrospective-and-improvement": {"blameless", "evidence-timeline", "fact-interpretation", "owner-deadline", "measurable-improvement"},
    "local-learning-persistence": {"one-validated-record", "local-only", "evidence-status", "retention", "deletion", "read-back", "rollback"},
}


def load(path: Path) -> Any: return json.loads(path.read_text(encoding="utf-8"))
def sha(path: Path) -> str: return hashlib.sha256(path.read_bytes().replace(b"\r\n", b"\n")).hexdigest()
def duplicates(values: list[str]) -> set[str]: return {value for value, count in Counter(values).items() if count > 1}


def verify(workspace: Path) -> dict[str, Any]:
    workspace = workspace.resolve(); checks: list[dict[str, Any]] = []
    def add(name: str, errors: list[str]) -> None: checks.append({"name": name, "ok": not errors, "errors": errors})

    prior = verify_phase6(workspace); add("phase-6-and-earlier-compatibility", [] if prior["ok"] else prior["errors"])
    identity_errors = []
    for phase, identity in PRIOR_TREES.items():
        if load(workspace / f".specs/capability-compiler-v2/{phase.replace('phase','phase-')}/artifact-manifest.json")["tree_sha256"] != identity: identity_errors.append(f"{phase} artifact identity changed")
    add("prior-phase-artifact-identities", identity_errors)

    root = workspace / "evals/candidates/capability-compiler-v2/phase-7"; schema_root = workspace / "curation/v2/phase-7"
    expected = {item.removeprefix("capability:") for item in load(workspace / "curation/v2/lifecycle/phase-ownership.json")["phases"]["7"]}
    catalog = load(root / "catalog.json"); catalog_ids = [item["id"] for item in catalog["skills"]]; dirs = {path.name for path in (root / "skills").iterdir() if path.is_dir()}; batches = load(schema_root / "batches.json")
    inventory_errors = []
    if len(expected) != 39 or catalog.get("skill_count") != 39: inventory_errors.append("Phase 7 ownership or catalog count is not 39")
    if set(catalog_ids) != expected or duplicates(catalog_ids) or dirs != expected: inventory_errors.append("catalog, directories, and ownership do not match exactly")
    batch_ids = [skill for values in batches["batches"].values() for skill in values]
    if batches.get("count") != 3 or batches.get("skill_count") != 39 or set(batch_ids) != expected or duplicates(batch_ids): inventory_errors.append("three-batch review ledger is incomplete or overlapping")
    if catalog.get("version") != VERSION or catalog.get("status") != "evaluating" or any(item.get("status") != "evaluating" or item.get("version") != VERSION for item in catalog["skills"]): inventory_errors.append("catalog version/status mismatch")
    add("phase-7-inventory-and-review-batches", inventory_errors)

    validators = {name: Draft202012Validator(load(schema_root / name)) for name in ["candidate-skill.schema.json", "provenance.schema.json", "trigger-cases.schema.json", "evaluation-plan.schema.json"]}
    designs = {item["skill_id"]: item for item in load(schema_root / "designs.json")["designs"]}; documents: dict[str, dict[str, Any]] = {}; all_cases = []; schema_errors = []
    for skill_id in sorted(expected):
        directory = root / "skills" / skill_id
        if not directory.is_dir(): schema_errors.append(f"{skill_id}: missing directory"); continue
        present = {path.name for path in directory.iterdir() if path.is_file()}
        if present != REQUIRED_FILES: schema_errors.append(f"{skill_id}: file set mismatch {sorted(present)}"); continue
        docs = {}
        for filename, schema_name in {"contract.json": "candidate-skill.schema.json", "provenance.json": "provenance.schema.json", "trigger-cases.json": "trigger-cases.schema.json", "evaluation-plan.json": "evaluation-plan.schema.json"}.items():
            doc = load(directory / filename); docs[filename] = doc
            for error in validators[schema_name].iter_errors(doc): schema_errors.append(f"{skill_id}/{filename}:{'.'.join(map(str,error.absolute_path)) or '<root>'}: {error.message}")
        documents[skill_id] = docs; contract = docs["contract.json"]; provenance = docs["provenance.json"]; evaluation = docs["evaluation-plan.json"]; design = designs[skill_id]; text = (directory / "SKILL.md").read_text(encoding="utf-8")
        if any(doc.get("id", doc.get("skill_id")) != skill_id for doc in docs.values()): schema_errors.append(f"{skill_id}: internal IDs disagree")
        if contract["responsibility"] != design["trigger"] or contract["hard_gates"][0] != design["distinctive_gate"] or contract["policy"]["coverage"] != design["coverage"] or contract["execution"]["mutation_scope"] != design["mutation_scope"]: schema_errors.append(f"{skill_id}: hand-designed semantics changed")
        if text.count(design["distinctive_gate"]) != 1: schema_errors.append(f"{skill_id}: distinctive marker count mismatch")
        for filename, expected_hash in provenance["candidate_files"].items():
            if sha(directory / filename) != expected_hash: schema_errors.append(f"{skill_id}: stale hash {filename}")
        if evaluation["candidate"]["skill_sha256"] != sha(directory / "SKILL.md") or evaluation["candidate"]["contract_sha256"] != sha(directory / "contract.json"): schema_errors.append(f"{skill_id}: stale evaluation hashes")
        all_cases.extend(docs["trigger-cases.json"]["cases"])
    add("candidate-schemas-hand-design-and-hashes", schema_errors)

    provenance_errors = []
    for skill_id, docs in documents.items():
        provenance = docs["provenance.json"]; capability = load(workspace / f"curation/v2/capabilities/{skill_id}.json")
        if provenance["prior_artifact_trees"] != PRIOR_TREES: provenance_errors.append(f"{skill_id}: prior artifact identities mismatch")
        for field in ["source_cluster_ids", "canonical_unit_ids", "retained_auxiliary_unit_ids", "root_derived_atom_ids", "source_fragment_ids", "fusion_decision_ids", "decision_references", "source_evidence", "source_defect_refs"]:
            if provenance[field] != capability[field]: provenance_errors.append(f"{skill_id}: provenance mismatch {field}")
        baseline = docs["evaluation-plan.json"]["baseline"]; roots = {item.split("/", 1)[0] for item in capability["source_evidence"] if "/" in item}
        if baseline["kind"] == "source-skill" and (baseline["identity"] not in roots or not (workspace / "skills" / baseline["identity"] / "SKILL.md").is_file()): provenance_errors.append(f"{skill_id}: baseline is not a real provenance root")
        if baseline["kind"] == "no-capability-baseline" and any((workspace / "skills" / item / "SKILL.md").is_file() for item in roots): provenance_errors.append(f"{skill_id}: no-baseline claim ignores executable source root")
    add("provenance-and-baseline-integrity", provenance_errors)

    permission_errors = []; identities = {item["id"]: item for item in load(workspace / "curation/v2/lifecycle/permission-identities.json")["identities"]}
    for skill_id, docs in documents.items():
        contract = docs["contract.json"]; execution = contract["execution"]; identity = identities[contract["permission_identity"]]; text = (root / "skills" / skill_id / "SKILL.md").read_text(encoding="utf-8")
        if execution["model_tools"] != identity["model_tools"] or execution["host_actions"] != identity["host_actions"] or execution["external"] != identity["external"] or execution["remote_write"] != identity["remote_write"]: permission_errors.append(f"{skill_id}: execution does not preserve Phase 2 identity")
        if execution["candidate_execution_state"] != "not-executed-phase-7": permission_errors.append(f"{skill_id}: candidate claims action execution")
        scope = execution["mutation_scope"]
        if skill_id in REMOTE_WRITERS and (contract["permission_identity"] != "remote-write-authorized-only" or not execution["remote_write"] or not scope.startswith("remote-")): permission_errors.append(f"{skill_id}: remote-write contract mismatch")
        if skill_id in OBSERVERS and (scope != "artifact-output" or execution["remote_write"] or any(tool in execution["model_tools"] for tool in ["edit", "write"])): permission_errors.append(f"{skill_id}: observer can mutate")
        if skill_id in PREFLIGHTS and (scope != "artifact-output" or execution["remote_write"]): permission_errors.append(f"{skill_id}: preflight can mutate")
        if skill_id in NO_MUTATION and (scope != "none" or any(tool in execution["model_tools"] for tool in ["edit", "write"])): permission_errors.append(f"{skill_id}: read-only candidate can mutate")
        if skill_id in SOURCE_WRITERS and scope != "authorized-workspace": permission_errors.append(f"{skill_id}: source writer lacks authorized-workspace scope")
        if skill_id in LOCAL_SYSTEM_WRITERS and (contract["permission_identity"] != "local-system-write-authorized-only" or scope != "local-system-write"): permission_errors.append(f"{skill_id}: local-system scope mismatch")
        if contract["policy"]["remote_or_system_action"] and "## Remote or Local-System Action Boundary" not in text: permission_errors.append(f"{skill_id}: action boundary section missing")
    if (REMOTE_WRITERS | OBSERVERS | PREFLIGHTS | NO_MUTATION | SOURCE_WRITERS | LOCAL_SYSTEM_WRITERS) - expected: permission_errors.append("permission allowlist references non-Phase-7 candidate")
    remote_scopes = [documents[skill]["contract.json"]["execution"]["mutation_scope"] for skill in REMOTE_WRITERS if skill in documents]
    if len(remote_scopes) != 16 or duplicates(remote_scopes): permission_errors.append("remote actions must have 16 distinct scopes")
    add("permission-readiness-observation-and-action-separation", permission_errors)

    case_errors = []; authored_ids = [case["id"] for case in all_cases]
    if duplicates(authored_ids): case_errors.append(f"duplicate authored case IDs {sorted(duplicates(authored_ids))}")
    for skill_id, docs in documents.items():
        cases = docs["trigger-cases.json"]["cases"]; counts = Counter(case["kind"] for case in cases)
        if counts != {"should-trigger": 2, "should-not-trigger": 2, "boundary": 1, "authority-stop": 1}: case_errors.append(f"{skill_id}: case shape mismatch {dict(counts)}")
        for case in cases:
            if case["kind"] == "should-trigger" and case["expected_skill_id"] != skill_id: case_errors.append(f"{case['id']}: positive misroute")
            if case["kind"] == "should-not-trigger" and (case["expected_skill_id"] == skill_id or skill_id not in case["forbidden_skill_ids"]): case_errors.append(f"{case['id']}: anti-route invalid")
            target = case["expected_skill_id"]
            if target and target not in expected and not (workspace / f"curation/v2/capabilities/{target}.json").is_file(): case_errors.append(f"{case['id']}: unknown route {target}")
    holdout = load(root / "holdout-cases.json"); holdout_ids = [case["id"] for case in holdout["cases"]]
    if holdout.get("case_count") != 78 or len(holdout_ids) != 78 or holdout.get("execution_state") != "not-run-phase-9": case_errors.append("holdout count/state mismatch")
    if duplicates(holdout_ids) or set(holdout_ids) & set(authored_ids): case_errors.append("holdout IDs duplicate or overlap authored cases")
    for skill_id, docs in documents.items():
        planned = set(docs["evaluation-plan.json"]["holdout_case_ids"]); owned = {item for item in holdout_ids if item.startswith(f"V2-P7-{skill_id}-holdout-")}
        if planned != owned or len(owned) != 2: case_errors.append(f"{skill_id}: holdout mismatch")
    add("trigger-and-holdout-boundaries", case_errors)

    semantic_errors = []
    for skill_id, required in CRITICAL_COVERAGE.items():
        if skill_id not in documents:
            semantic_errors.append(f"{skill_id}: candidate contract missing"); continue
        missing = required - set(documents[skill_id]["contract.json"]["policy"]["coverage"])
        if missing: semantic_errors.append(f"{skill_id}: missing critical markers {sorted(missing)}")
    for skill_id, docs in documents.items():
        contract = docs["contract.json"]; text = (root / "skills" / skill_id / "SKILL.md").read_text(encoding="utf-8")
        if "Preflight never changes; observation never recovers; coordination never performs specialist actions" not in text: semantic_errors.append(f"{skill_id}: lifecycle separation marker missing")
        if contract["policy"]["data_governance"] and "## Data and Credential Governance" not in text: semantic_errors.append(f"{skill_id}: data governance section missing")
        if contract["policy"]["human_decision"] and "## Human Decision Authority" not in text: semantic_errors.append(f"{skill_id}: human authority section missing")
        if skill_id in REMOTE_WRITERS | LOCAL_SYSTEM_WRITERS and not contract["policy"]["remote_or_system_action"]: semantic_errors.append(f"{skill_id}: action policy flag missing")
    add("delivery-observability-incident-and-learning-invariants", semantic_errors)

    evaluation_errors = []
    for skill_id, docs in documents.items():
        evaluation = docs["evaluation-plan.json"]; text = (root / "skills" / skill_id / "SKILL.md").read_text(encoding="utf-8")
        if evaluation["status"] != "planned" or evaluation["execution_state"] != "not-run-phase-9": evaluation_errors.append(f"{skill_id}: false evaluation claim")
        for mutation in evaluation["mutations"]:
            if mutation["remove_exact_text"] != designs[skill_id]["distinctive_gate"] or text.count(mutation["remove_exact_text"]) != 1: evaluation_errors.append(f"{mutation['id']}: invalid semantic mutation marker")
    add("evaluation-plans-and-semantic-mutations", evaluation_errors)

    review_errors = []; review_path = schema_root / "semantic-review.json"
    if not review_path.is_file(): review_errors.append("semantic-review.json missing")
    else:
        review = load(review_path)
        if review.get("status") != "passed" or review.get("reviewed_candidate_count") != 39 or review.get("open_findings") != []: review_errors.append("semantic review status/count/open findings mismatch")
        if len(review.get("boundary_samples", [])) < 12 or any(item.get("verdict") != "passed" for item in review.get("boundary_samples", [])): review_errors.append("semantic boundary samples incomplete")
    add("semantic-boundary-review", review_errors)

    errors = [f"{check['name']}: {error}" for check in checks for error in check["errors"]]
    return {"gate": "capability-compiler-v2-phase-7", "ok": not errors, "checks": checks, "counts": {"skills": 39, "batches": 3, "authored_trigger_cases": len(all_cases), "holdout_cases": len(holdout_ids), "planned_mutations": sum(len(docs["evaluation-plan.json"]["mutations"]) for docs in documents.values()), "remote_write_candidates": len(REMOTE_WRITERS), "observer_candidates": len(OBSERVERS), "preflight_candidates": len(PREFLIGHTS), "local_system_candidates": len(LOCAL_SYSTEM_WRITERS)}, "errors": errors}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__); parser.add_argument("--workspace-root", type=Path, default=Path(".")); parser.add_argument("--output", type=Path); args = parser.parse_args(); result = verify(args.workspace_root)
    if args.output:
        path = args.output if args.output.is_absolute() else args.workspace_root / args.output; path.parent.mkdir(parents=True, exist_ok=True); path.write_text(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps(result, ensure_ascii=False, sort_keys=True)); return 0 if result["ok"] else 1


if __name__ == "__main__": raise SystemExit(main())
