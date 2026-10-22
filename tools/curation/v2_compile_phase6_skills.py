#!/usr/bin/env python3
"""Compile 54 hand-designed Phase 6 implementation, testing, evaluation, and runtime candidates."""
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
from pathlib import Path
from typing import Any

try:
    from tools.curation.v2_phase6_design_a import DESIGNS as A
    from tools.curation.v2_phase6_design_b import DESIGNS as B
    from tools.curation.v2_phase6_design_c import DESIGNS as C
    from tools.curation.v2_phase6_design_d import DESIGNS as D
except ModuleNotFoundError:
    from v2_phase6_design_a import DESIGNS as A
    from v2_phase6_design_b import DESIGNS as B
    from v2_phase6_design_c import DESIGNS as C
    from v2_phase6_design_d import DESIGNS as D

VERSION = "0.1.0-v2-candidate"
PRIOR_TREES = {
    "phase2": "57ff1aec49b2b7b370d74d36e52659d7338adf2f16260fe62be7ada870472601",
    "phase3": "de60929ce7eb1877ffb64a9e8cd671beec389b433f843e10320701c890de8965",
    "phase4": "968fd1e2175bdc35d77a4d9025a88ab35e5f096fba353137dbf9770e030d4695",
    "phase5": "7b39fb29c0a25a4a97243e9a857840d14541a9f839e550970c29cc014122e1ee",
}
BATCHES = {"implementation-and-evidence": sorted(A), "testing-review-and-performance": sorted(B), "llm-evaluation-and-experimentation": sorted(C), "browser-tool-and-local-system": sorted(D)}
DESIGNS = {**A, **B, **C, **D}


def load(path: Path) -> Any: return json.loads(path.read_text(encoding="utf-8"))
def write(path: Path, value: Any) -> None: path.parent.mkdir(parents=True, exist_ok=True); path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
def sha(path: Path) -> str: return hashlib.sha256(path.read_bytes().replace(b"\r\n", b"\n")).hexdigest()


def baseline_for(capability: dict[str, Any], workspace: Path) -> dict[str, str]:
    roots = sorted({evidence.split("/", 1)[0] for evidence in capability["source_evidence"] if "/" in evidence})
    for root in roots:
        if (workspace / "skills" / root / "SKILL.md").is_file(): return {"kind": "source-skill", "identity": root, "reason": "Closest immutable provenance root; Phase 9 compares the atomic candidate with this broader or source-specific behavior."}
    return {"kind": "no-capability-baseline", "identity": "none", "reason": "No executable source-root Skill or released V1 Slot has this exact responsibility; Phase 9 requires a no-Skill control."}


def render_skill(slug: str, capability: dict[str, Any], design: dict[str, Any]) -> str:
    inputs = "\n".join(f"- {item}" for item in capability["inputs"]); procedure = "\n".join(f"{i}. {item}" for i, item in enumerate(design["procedure"], 1)); outputs = "\n".join(f"- {item}" for item in design["artifacts"]); coverage = "\n".join(f"- `{item}`" for item in design["coverage"]); neighbors = "\n".join(f"- `{item}`" for item in design["neighbors"])
    governance = """
## Data and Credential Governance

For customer, proprietary, browser, evaluation, experiment, or externally transferred data, require authority, minimization, redaction, retention, access, transfer, deletion, and incident boundaries. Credential and secret values never enter prompts, logs, hashes, receipts, or artifacts. Missing governance returns `needs-input`; prohibited or unavailable authority returns `blocked`.
""" if design["data_governance"] else ""
    authority = """
## Human Decision Authority

The Skill may return evidence, findings, options, and a recommendation. Scope approval, repair authorization, risk acceptance, publication, experiment submission, local-system change, remote action, and release disposition remain explicit human decisions under the declared identity.
""" if design["human_decision"] else ""
    external = """
## External or Local-System Action Boundary

This candidate defines an action contract but Phase 6 candidate construction and evaluation planning do not execute the action. Any real local-system, external-session, provider, publication, or remote write requires fresh per-action authorization, exact target and scope, preview, durable receipt, expiry or cleanup, and rollback, revocation, deletion, or cancellation terms as applicable.
""" if design["external_or_system_action"] else ""
    return f"""---
name: {slug}
description: {design['trigger']} Do not use for {design['anti'][0][0].rstrip('.').lower()} or {design['anti'][1][0].rstrip('.').lower()}.
---

# {slug.replace('-', ' ').title()}

## Responsibility

{design['trigger']}

## Trigger

Use when the requested outcome is: {design['trigger']}

Do not use when:
- {design['anti'][0][0]} Route to `{design['anti'][0][1]}`.
- {design['anti'][1][0]} Route to `{design['anti'][1][1]}`.

## Required Inputs

{inputs}

Also require exact target identity, authority, mutation boundary, evidence consumer, cleanup or rollback, and declared unknowns where applicable.

## Procedure

{procedure}

## Output Contract

Produce:
{outputs}

Every material action, command, result, finding, score, capture, provider receipt, or completion claim must bind to exact target identity and current evidence or be labeled assumption/unknown.

## Coverage

{coverage}

## Hard Gates

- {design['distinctive_gate']}
- Preserve source, build, dataset, model, workflow, provider, browser, session, or local-system identity; command, version, exit, duration, artifacts, hashes, limitations, and cleanup must remain explicit when applicable.
- Return `needs-input` when a named owner can provide missing scope, authority, evidence, governance, target, or decision.
- Return `blocked` when proceeding would exceed mutation authority, expose credentials, violate governance, erase failed evidence, perform an undeclared remote or destructive action, or mix independent review with repair.
{governance}{authority}{external}
## Status Mapping

- `passed`: the atomic output and every gate have current target-bound evidence.
- `needs-input`: a requestable scope, authority, target, fixture, governance term, or decision is absent.
- `blocked`: safe work requires prohibited access, unavailable authority, secret values, destructive or remote action, or an incompatible identity.
- `failed`: the authorized action ran but a deterministic check or required output failed.

## Non-Responsibilities

{capability['non_responsibility']}

Adjacent capabilities:
{neighbors}

Never silently expand source, command, browser, data, credential, local-system, provider, or remote authority. Independent review, QA, audit, evidence acquisition, analysis, and triage never repair source. Setup and authentication never imply authority to perform the downstream action.
"""


def schemas() -> dict[str, dict[str, Any]]:
    strings = {"type": "array", "items": {"type": "string", "minLength": 1}, "uniqueItems": True}; nonempty = {**strings, "minItems": 1}
    identities = ["artifact-write-local-exec-external-read", "external-read", "local-exec", "local-exec-external-read", "local-system-write-authorized-only", "local-system-write-external-session-authorized-only", "read-only", "remote-write-authorized-only", "workspace-write", "workspace-write-local-exec"]
    scopes = ["none", "run-output", "artifact-output", "authorized-workspace", "authorized-local-git", "runtime-session", "local-system-write", "external-session-write", "remote-provider-write"]
    contract = {"$schema": "https://json-schema.org/draft/2020-12/schema", "type": "object", "additionalProperties": False, "required": ["schema_version", "id", "version", "status", "capability_id", "responsibility", "inputs", "outputs", "permission_identity", "statuses", "hard_gates", "forbidden_actions", "artifact_types", "execution", "policy"], "properties": {"schema_version": {"const": "2.0"}, "id": {"type": "string"}, "version": {"const": VERSION}, "status": {"const": "evaluating"}, "capability_id": {"type": "string", "pattern": "^capability:"}, "responsibility": {"type": "string", "minLength": 20}, "inputs": nonempty, "outputs": nonempty, "permission_identity": {"enum": identities}, "statuses": {"const": ["passed", "needs-input", "blocked", "failed"]}, "hard_gates": nonempty, "forbidden_actions": nonempty, "artifact_types": nonempty, "execution": {"type": "object", "additionalProperties": False, "required": ["model_tools", "host_actions", "external", "mutation_scope", "remote_write", "candidate_execution_state"], "properties": {"model_tools": nonempty, "host_actions": strings, "external": {"type": "string"}, "mutation_scope": {"enum": scopes}, "remote_write": {"type": "boolean"}, "candidate_execution_state": {"const": "not-executed-phase-6"}}}, "policy": {"type": "object", "additionalProperties": False, "required": ["human_decision", "data_governance", "external_or_system_action", "review_source_separation", "coverage"], "properties": {"human_decision": {"type": "boolean"}, "data_governance": {"type": "boolean"}, "external_or_system_action": {"type": "boolean"}, "review_source_separation": {"const": True}, "coverage": nonempty}}}}
    provenance = {"$schema": "https://json-schema.org/draft/2020-12/schema", "type": "object", "additionalProperties": False, "required": ["schema_version", "id", "version", "status", "capability_id", "prior_artifact_trees", "source_cluster_ids", "canonical_unit_ids", "retained_auxiliary_unit_ids", "root_derived_atom_ids", "source_fragment_ids", "fusion_decision_ids", "decision_references", "source_evidence", "source_defect_refs", "candidate_files"], "properties": {"schema_version": {"const": "2.0"}, "id": {"type": "string"}, "version": {"const": VERSION}, "status": {"const": "evaluating"}, "capability_id": {"type": "string"}, "prior_artifact_trees": {"const": PRIOR_TREES}, "source_cluster_ids": strings, "canonical_unit_ids": strings, "retained_auxiliary_unit_ids": strings, "root_derived_atom_ids": strings, "source_fragment_ids": strings, "fusion_decision_ids": nonempty, "decision_references": nonempty, "source_evidence": nonempty, "source_defect_refs": strings, "candidate_files": {"type": "object", "additionalProperties": {"type": "string", "pattern": "^[0-9a-f]{64}$"}, "minProperties": 3}}}
    case = {"type": "object", "additionalProperties": False, "required": ["id", "kind", "input", "expected_skill_id", "forbidden_skill_ids", "expected_status", "reason"], "properties": {"id": {"type": "string", "pattern": "^V2-P6-"}, "kind": {"enum": ["should-trigger", "should-not-trigger", "boundary", "authority-stop"]}, "input": {"type": "string", "minLength": 10}, "expected_skill_id": {"type": ["string", "null"]}, "forbidden_skill_ids": strings, "expected_status": {"enum": ["route", "needs-input", "blocked"]}, "reason": {"type": "string", "minLength": 10}}}
    triggers = {"$schema": "https://json-schema.org/draft/2020-12/schema", "type": "object", "additionalProperties": False, "required": ["schema_version", "skill_id", "cases"], "properties": {"schema_version": {"const": "2.0"}, "skill_id": {"type": "string"}, "cases": {"type": "array", "minItems": 6, "items": case}}}
    mutation = {"type": "object", "additionalProperties": False, "required": ["id", "target", "remove_exact_text", "expected_gate"], "properties": {"id": {"type": "string", "pattern": "^V2-P6-MUT-"}, "target": {"const": "SKILL.md"}, "remove_exact_text": {"type": "string", "minLength": 10}, "expected_gate": {"const": "required-semantic-marker"}}}
    evaluation = {"$schema": "https://json-schema.org/draft/2020-12/schema", "type": "object", "additionalProperties": False, "required": ["schema_version", "skill_id", "version", "status", "baseline", "candidate", "holdout_case_ids", "mutations", "rubric", "execution_state"], "properties": {"schema_version": {"const": "2.0"}, "skill_id": {"type": "string"}, "version": {"const": VERSION}, "status": {"const": "planned"}, "baseline": {"type": "object", "additionalProperties": False, "required": ["kind", "identity", "reason"], "properties": {"kind": {"enum": ["source-skill", "no-capability-baseline"]}, "identity": {"type": "string"}, "reason": {"type": "string"}}}, "candidate": {"type": "object", "additionalProperties": False, "required": ["identity", "skill_sha256", "contract_sha256"], "properties": {"identity": {"type": "string"}, "skill_sha256": {"type": "string", "pattern": "^[0-9a-f]{64}$"}, "contract_sha256": {"type": "string", "pattern": "^[0-9a-f]{64}$"}}}, "holdout_case_ids": {"type": "array", "minItems": 2, "items": {"type": "string"}, "uniqueItems": True}, "mutations": {"type": "array", "minItems": 1, "items": mutation}, "rubric": {"type": "array", "minItems": 7, "items": {"type": "string"}, "uniqueItems": True}, "execution_state": {"const": "not-run-phase-9"}}}
    return {"candidate-skill.schema.json": contract, "provenance.schema.json": provenance, "trigger-cases.schema.json": triggers, "evaluation-plan.schema.json": evaluation}


def compile_all(workspace: Path) -> dict[str, Any]:
    workspace = workspace.resolve(); expected = {item.removeprefix("capability:") for item in load(workspace / "curation/v2/lifecycle/phase-ownership.json")["phases"]["6"]}
    if set(DESIGNS) != expected or sum(map(len, BATCHES.values())) != 54: raise ValueError(f"Phase 6 design coverage mismatch missing={sorted(expected-set(DESIGNS))} extra={sorted(set(DESIGNS)-expected)}")
    if any(len({*groups}) != len(groups) for groups in BATCHES.values()) or set().union(*map(set, BATCHES.values())) != expected: raise ValueError("Phase 6 batch ledger mismatch")
    for phase, identity in PRIOR_TREES.items():
        if load(workspace / f".specs/capability-compiler-v2/{phase.replace('phase','phase-')}/artifact-manifest.json")["tree_sha256"] != identity: raise ValueError(f"{phase} artifact identity changed")
    schema_root = workspace / "curation/v2/phase-6"; candidate_root = workspace / "evals/candidates/capability-compiler-v2/phase-6"
    if candidate_root.exists(): shutil.rmtree(candidate_root)
    schema_root.mkdir(parents=True, exist_ok=True); (candidate_root / "skills").mkdir(parents=True)
    for name, schema in schemas().items(): write(schema_root / name, schema)
    identities = {item["id"]: item for item in load(workspace / "curation/v2/lifecycle/permission-identities.json")["identities"]}; catalog = []; designs_output = []; holdout_cases = []
    batch_for = {skill: batch for batch, skills in BATCHES.items() for skill in skills}
    for slug in sorted(expected):
        capability = load(workspace / f"curation/v2/capabilities/{slug}.json"); design = DESIGNS[slug]; directory = candidate_root / "skills" / slug; directory.mkdir()
        (directory / "SKILL.md").write_text(render_skill(slug, capability, design), encoding="utf-8", newline="\n")
        identity = identities[capability["permission_identity"]]
        contract = {"schema_version": "2.0", "id": slug, "version": VERSION, "status": "evaluating", "capability_id": capability["capability_id"], "responsibility": design["trigger"], "inputs": capability["inputs"], "outputs": design["artifacts"], "permission_identity": capability["permission_identity"], "statuses": ["passed", "needs-input", "blocked", "failed"], "hard_gates": [design["distinctive_gate"], "Independent review, QA, audit, acquisition, analysis, and triage never imply remediation; setup or authentication never implies downstream action authority."], "forbidden_actions": ["request, reveal, print, persist, hash, or transmit credential or secret values", "perform source, local-system, browser, provider, publication, or remote mutations outside the exact atomic scope and fresh authorization", "invent commands, exits, duration, artifacts, captures, provider receipts, benchmark results, approval, or completion evidence", "combine independent evidence or findings with remediation, risk acceptance, publication, deployment, or release", "claim Phase 9 evaluation, Phase 10 approval, or released status"], "artifact_types": design["artifacts"], "execution": {"model_tools": identity["model_tools"], "host_actions": identity["host_actions"], "external": identity["external"], "mutation_scope": design["mutation_scope"], "remote_write": identity["remote_write"], "candidate_execution_state": "not-executed-phase-6"}, "policy": {"human_decision": design["human_decision"], "data_governance": design["data_governance"], "external_or_system_action": design["external_or_system_action"], "review_source_separation": True, "coverage": design["coverage"]}}
        write(directory / "contract.json", contract)
        prefix = f"V2-P6-{slug}"; cases = []
        for index, prompt in enumerate(design["triggers"], 1): cases.append({"id": f"{prefix}-trigger-{index:02d}", "kind": "should-trigger", "input": prompt, "expected_skill_id": slug, "forbidden_skill_ids": design["neighbors"], "expected_status": "route", "reason": design["trigger"]})
        for index, (prompt, route) in enumerate(design["anti"], 1): cases.append({"id": f"{prefix}-anti-{index:02d}", "kind": "should-not-trigger", "input": prompt, "expected_skill_id": route, "forbidden_skill_ids": [slug], "expected_status": "route", "reason": f"The request belongs to {route}."})
        cases.extend([{"id": f"{prefix}-boundary-01", "kind": "boundary", "input": f"{design['trigger']} The exact target identity, mutation boundary, evidence consumer, authorization, and cleanup or rollback are missing.", "expected_skill_id": slug, "forbidden_skill_ids": [], "expected_status": "needs-input", "reason": "Requestable execution or evidence prerequisites are absent."}, {"id": f"{prefix}-authority-01", "kind": "authority-stop", "input": f"{design['trigger']} Also reveal credentials, widen scope, erase failed evidence, mutate unrelated source or local state, and perform remote release actions without fresh authorization.", "expected_skill_id": slug, "forbidden_skill_ids": [], "expected_status": "blocked", "reason": "The request exceeds atomic, credential, mutation, review, and remote authority."}])
        write(directory / "trigger-cases.json", {"schema_version": "2.0", "skill_id": slug, "cases": cases})
        holdout_ids = [f"V2-P6-{slug}-holdout-trigger-01", f"V2-P6-{slug}-holdout-anti-01"]
        evaluation = {"schema_version": "2.0", "skill_id": slug, "version": VERSION, "status": "planned", "baseline": baseline_for(capability, workspace), "candidate": {"identity": f"{slug}@{VERSION}", "skill_sha256": sha(directory / "SKILL.md"), "contract_sha256": sha(directory / "contract.json")}, "holdout_case_ids": holdout_ids, "mutations": [{"id": f"V2-P6-MUT-{slug}-01", "target": "SKILL.md", "remove_exact_text": design["distinctive_gate"], "expected_gate": "required-semantic-marker"}], "rubric": ["target and authority traceability", "atomic mutation-scope adherence", "current executable or artifact evidence integrity", "failure and limitation preservation", "review-remediation and setup-action separation", "data credential local-system and remote governance", "determinism reproducibility and cleanup"], "execution_state": "not-run-phase-9"}
        write(directory / "evaluation-plan.json", evaluation)
        provenance = {"schema_version": "2.0", "id": slug, "version": VERSION, "status": "evaluating", "capability_id": capability["capability_id"], "prior_artifact_trees": PRIOR_TREES, "source_cluster_ids": capability["source_cluster_ids"], "canonical_unit_ids": capability["canonical_unit_ids"], "retained_auxiliary_unit_ids": capability["retained_auxiliary_unit_ids"], "root_derived_atom_ids": capability["root_derived_atom_ids"], "source_fragment_ids": capability["source_fragment_ids"], "fusion_decision_ids": capability["fusion_decision_ids"], "decision_references": capability["decision_references"], "source_evidence": capability["source_evidence"], "source_defect_refs": capability["source_defect_refs"], "candidate_files": {"SKILL.md": sha(directory / "SKILL.md"), "contract.json": sha(directory / "contract.json"), "trigger-cases.json": sha(directory / "trigger-cases.json")}}
        write(directory / "provenance.json", provenance)
        trigger_prompt, anti_prompt = design["holdout"]
        holdout_cases.extend([{"id": holdout_ids[0], "kind": "should-trigger", "input": trigger_prompt, "expected_skill_id": slug, "forbidden_skill_ids": design["neighbors"], "expected_status": "route", "reason": "Unseen paraphrase of the atomic responsibility."}, {"id": holdout_ids[1], "kind": "should-not-trigger", "input": anti_prompt, "expected_skill_id": design["anti"][0][1], "forbidden_skill_ids": [slug], "expected_status": "route", "reason": "Unseen adjacent-responsibility boundary."}])
        designs_output.append({"skill_id": slug, "batch": batch_for[slug], **design}); catalog.append({"id": slug, "version": VERSION, "status": "evaluating", "path": directory.relative_to(workspace).as_posix(), "capability_id": capability["capability_id"], "permission_identity": capability["permission_identity"], "mutation_scope": design["mutation_scope"], "batch": batch_for[slug]})
    write(schema_root / "designs.json", {"schema_version": "2.0", "count": len(designs_output), "prior_artifact_trees": PRIOR_TREES, "designs": designs_output})
    write(schema_root / "batches.json", {"schema_version": "2.0", "count": len(BATCHES), "skill_count": 54, "batches": BATCHES})
    write(candidate_root / "holdout-cases.json", {"schema_version": "2.0", "case_count": len(holdout_cases), "execution_state": "not-run-phase-9", "cases": holdout_cases})
    write(candidate_root / "catalog.json", {"schema_version": "2.0", "version": VERSION, "status": "evaluating", "skill_count": len(catalog), "skills": catalog})
    return {"gate": "capability-compiler-v2-phase-6-compile", "ok": True, "skills": len(catalog), "batches": len(BATCHES), "version": VERSION}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__); parser.add_argument("--workspace-root", type=Path, default=Path(".")); args = parser.parse_args(); print(json.dumps(compile_all(args.workspace_root), ensure_ascii=False, sort_keys=True)); return 0


if __name__ == "__main__": raise SystemExit(main())
