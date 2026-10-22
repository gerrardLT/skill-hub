#!/usr/bin/env python3
"""Fail-closed gate for the Capability Compiler V2 lifecycle taxonomy."""
from __future__ import annotations

import argparse
import json
import re
from collections import Counter, defaultdict, deque
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

try:
    from tools.curation.v2_phase1_gate import verify as verify_phase1
except ModuleNotFoundError:
    from v2_phase1_gate import verify as verify_phase1

MANDATORY_STAGES = {f"stage:{number:02d}-{slug}" for number, slug in [
    (1, "governance-intake"), (2, "discovery-research"), (3, "strategy-prioritization"),
    (4, "requirements-planning"), (5, "experience-design"), (6, "architecture-risk-security"),
    (7, "implementation-integration"), (8, "verification-quality"), (9, "performance-reliability"),
    (10, "release-readiness"), (11, "deployment-change"), (12, "observation-canary"),
    (13, "incident-recovery"), (14, "learning-feedback"),
]}
PERMISSION_CONTRACTS = {
    "read-only": ({"read"}, set(), "none", False),
    "workspace-write": ({"read", "edit", "write"}, set(), "none", False),
    "workspace-write-local-exec": ({"read", "edit", "write"}, {"approved-local-commands"}, "none", False),
    "workspace-write-external-read": ({"read", "edit", "write"}, {"approved-provider-read"}, "read-only", False),
    "workspace-write-local-exec-external-read": ({"read", "edit", "write"}, {"approved-local-commands", "approved-provider-read"}, "read-only", False),
    "artifact-write-local-exec": ({"read"}, {"approved-local-commands", "approved-artifact-write"}, "none", False),
    "artifact-write-local-exec-external-read": ({"read"}, {"approved-local-commands", "approved-artifact-write", "approved-provider-read"}, "read-only", False),
    "local-exec-external-read": ({"read"}, {"approved-local-commands", "approved-provider-read"}, "read-only", False),
    "local-system-write-external-session-authorized-only": ({"read"}, {"approved-local-system-write", "approved-network-exposure", "approved-credential-mint"}, "scoped-session-write-with-per-action-authorization", True),
    "local-system-write-authorized-only": ({"read"}, {"approved-local-system-write"}, "none", False),
    "local-exec": ({"read"}, {"approved-local-commands"}, "none", False),
    "external-read": ({"read"}, {"approved-provider-read"}, "read-only", False),
    "remote-write-authorized-only": ({"read"}, {"approved-provider-write"}, "write-with-per-action-authorization", True),
}
REVIEW_ONLY = {
    "capability:independent-blackbox-qa", "capability:independent-code-review",
    "capability:independent-plan-review", "capability:rendered-ui-critique-and-release-disposition",
    "capability:ui-review-scope-and-evidence-acquisition", "capability:qa-finding-triage",
    "capability:website-audit-assessment", "capability:developer-experience-plan-review",
    "capability:design-plan-review", "capability:executive-plan-review", "capability:engineering-plan-review",
    "capability:implementation-spec-compliance-review", "capability:browser-agent-pairing-verification",
}
POLICY_REQUIREMENTS = {
    "domain:product-discovery-and-strategy": {"V2-DEC-003", "V2-DEC-005"},
    "domain:ux-ui-and-accessibility": {"V2-DEC-002"},
}
MUTATION_ATOM_TARGETS = {
    "v2-root:gstack/review:021:step-5b-auto-fix-all-auto-fix-items": "capability:defect-remediation",
    "v2-root:gstack/review:023:step-5d-apply-user-approved-fixes": "capability:defect-remediation",
    "v2-root:gstack/design-review:009:b4-install-and-configure": "capability:test-runtime-bootstrap",
    "v2-root:gstack/design-review:024:phase-8-fix-loop": "capability:ui-remediation",
    "v2-root:gstack/ship:012:step-3-merge-the-base-branch-before-tests": "capability:local-branch-integration",
    "v2-root:gstack/ship:020:step-17-push": "capability:remote-git-push",
    "v2-root:gstack/land-and-deploy:015:strategy-a-github-actions-workflow": "capability:deployment-trigger-execution",
    "v2-root:gstack/land-and-deploy:016:strategy-c-auto-deploy-platforms-vercel-netlify": "capability:deployment-trigger-execution",
    "v2-root:gstack/land-and-deploy:017:strategy-d-custom-deploy-hooks": "capability:deployment-trigger-execution",
    "v2-root:gstack/land-and-deploy:019:step-8-revert-if-needed": "capability:release-rollback-execution",
    "v2-root:sentry-debug-issue:006:step-4-verify-against-the-code-then-fix": "capability:defect-remediation",
    "v2-root:dd-apm/k8s-ssi/troubleshoot-ssi:010:step-5-fix": "capability:apm-instrumentation-enablement",
    "v2-root:dd-apm/linux-ssi/troubleshoot-ssi:013:step-6-fix": "capability:apm-instrumentation-enablement",
    "v2-root:dd-apm/linux-ssi/troubleshoot-ssi:014:re-run-install-now-it-will-actually-download-and-extract": "capability:observability-agent-installation",
    "v2-root:gstack/canary:009:phase-2-baseline-capture-baseline-mode": "capability:canary-baseline-management",
    "v2-root:gstack/canary:011:phase-4-pre-deploy-snapshot-if-no-baseline-exists": "capability:canary-baseline-management",
    "v2-root:gstack/canary:014:phase-7-baseline-update": "capability:canary-baseline-management",
    "v2-root:gstack/codex:016:write-to-the-plan-file": "capability:artifact-persistence-and-tool-actions",
    "v2-root:gstack/health:013:step-5-persist-to-health-history": "capability:local-learning-persistence",
    "v2-root:gstack/plan-ceo-review:015:0d-post-persist-ceo-plan-expansion-and-selective-expansion-only": "capability:local-learning-persistence",
}
FORBIDDEN_ATOMIC_CAPABILITIES = {
    "capability:agent-observability-evaluation-lifecycle",
    "capability:plan-review-orchestration",
    "capability:qa-repair-loop",
    "capability:subagent-task-pipeline",
}

def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def duplicate_values(values: list[str]) -> set[str]:
    return {value for value, count in Counter(values).items() if count > 1}


def cycle_nodes(edges: list[dict[str, str]], known: set[str]) -> set[str]:
    outgoing: dict[str, set[str]] = defaultdict(set)
    indegree = {node: 0 for node in known}
    for edge in edges:
        source, target = edge["source_capability_id"], edge["target_capability_id"]
        if source in known and target in known and target not in outgoing[source]:
            outgoing[source].add(target)
            indegree[target] += 1
    queue = deque(node for node, degree in indegree.items() if degree == 0)
    visited = 0
    while queue:
        node = queue.popleft(); visited += 1
        for target in outgoing[node]:
            indegree[target] -= 1
            if indegree[target] == 0:
                queue.append(target)
    return {node for node, degree in indegree.items() if degree > 0} if visited != len(known) else set()


def verify(workspace: Path) -> dict[str, Any]:
    workspace = workspace.resolve(); checks: list[dict[str, Any]] = []
    def add(name: str, errors: list[str]) -> None:
        checks.append({"name": name, "ok": not errors, "errors": errors})

    phase1 = verify_phase1(workspace)
    add("phase-1-and-source-v1-compatibility", [] if phase1["ok"] else phase1["errors"])

    domains = load(workspace / "curation/v2/lifecycle/domains.json")["domains"]
    stages_doc = load(workspace / "curation/v2/lifecycle/stages.json")
    stages = stages_doc["stages"]
    domain_ids = {item["id"] for item in domains}; stage_ids = {item["id"] for item in stages}
    lifecycle_errors: list[str] = []
    if len(domains) != 11 or len(domain_ids) != 11: lifecycle_errors.append(f"expected 11 unique domains, got {len(domain_ids)}")
    if len(stages) != 15 or len(stage_ids) != 15: lifecycle_errors.append(f"expected 15 unique stages, got {len(stage_ids)}")
    if not MANDATORY_STAGES <= stage_ids: lifecycle_errors.append(f"missing mandatory stages: {sorted(MANDATORY_STAGES-stage_ids)}")
    if len(stages_doc.get("hard_stage_edges", [])) != 13: lifecycle_errors.append("lifecycle must have 13 ordered mandatory-stage edges")
    add("lifecycle-schema", lifecycle_errors)

    schema = load(workspace / "curation/v2/capability.schema.json")
    validator = Draft202012Validator(schema)
    capability_paths = sorted((workspace / "curation/v2/capabilities").glob("*.json"))
    capability_paths = [path for path in capability_paths if path.name != "catalog.json"]
    capabilities: dict[str, dict[str, Any]] = {}; contract_errors: list[str] = []
    for path in capability_paths:
        capability = load(path); capability_id = capability.get("capability_id", path.stem)
        for error in validator.iter_errors(capability):
            location = ".".join(str(part) for part in error.absolute_path)
            contract_errors.append(f"{path.name}:{location or '<root>'}: {error.message}")
        if capability_id in capabilities: contract_errors.append(f"duplicate capability_id: {capability_id}")
        capabilities[capability_id] = capability
        if path.stem != capability_id.removeprefix("capability:"): contract_errors.append(f"filename/id mismatch: {path.name} != {capability_id}")
        if capability.get("primary_domain_id") not in domain_ids: contract_errors.append(f"{capability_id}: unknown domain")
        if capability.get("lifecycle_stage_id") not in stage_ids: contract_errors.append(f"{capability_id}: unknown stage")
        if not (capability.get("source_cluster_ids") or capability.get("canonical_unit_ids") or capability.get("root_derived_atom_ids") or capability.get("source_fragment_ids")): contract_errors.append(f"{capability_id}: orphan capability")
        if not capability.get("fusion_decision_ids"): contract_errors.append(f"{capability_id}: missing fusion decisions")
        for fragment in capability.get("source_fragment_ids", []):
            match = re.fullmatch(r"(.+):(\d+)-(\d+)", fragment)
            if not match:
                contract_errors.append(f"{capability_id}: invalid source fragment identity {fragment}"); continue
            relative, start_text, end_text = match.groups(); source_path = workspace / "skills" / relative
            if not source_path.is_file():
                contract_errors.append(f"{capability_id}: missing source fragment file {relative}"); continue
            start, end = int(start_text), int(end_text); line_count = len(source_path.read_text(encoding="utf-8").splitlines())
            if start < 1 or end < start or end > line_count: contract_errors.append(f"{capability_id}: invalid source fragment range {fragment}, file has {line_count} lines")
            if fragment not in capability.get("source_evidence", []): contract_errors.append(f"{capability_id}: source fragment absent from source_evidence: {fragment}")
    catalog = load(workspace / "curation/v2/capabilities/catalog.json")
    catalog_ids = [item["capability_id"] for item in catalog["capabilities"]]
    if catalog.get("capability_count") != len(capabilities) or set(catalog_ids) != set(capabilities) or duplicate_values(catalog_ids): contract_errors.append("capability catalog does not exactly match capability files")
    empty_domains = domain_ids - {item.get("primary_domain_id") for item in capabilities.values()}
    empty_stages = MANDATORY_STAGES - {item.get("lifecycle_stage_id") for item in capabilities.values()}
    if empty_domains: contract_errors.append(f"empty domains: {sorted(empty_domains)}")
    if empty_stages: contract_errors.append(f"empty mandatory stages: {sorted(empty_stages)}")
    add("capability-contracts-and-coverage", contract_errors)

    clusters = load(workspace / "curation/clusters.json")["clusters"]
    cluster_map = load(workspace / "curation/v2/lifecycle/cluster-map.json")["records"]
    mapping_errors: list[str] = []
    expected_clusters = {item["id"] for item in clusters}; mapped_clusters = [item["cluster_id"] for item in cluster_map]
    if set(mapped_clusters) != expected_clusters or duplicate_values(mapped_clusters): mapping_errors.append("88 legacy clusters are not mapped exactly once")
    expected_canonical = {unit_id for cluster in clusters for unit_id in cluster["unit_ids"]}
    canonical_owners: dict[str, list[str]] = defaultdict(list)
    auxiliary_owners: dict[str, list[str]] = defaultdict(list)
    for capability in capabilities.values():
        for unit_id in capability.get("canonical_unit_ids", []): canonical_owners[unit_id].append(capability["capability_id"])
        for unit_id in capability.get("retained_auxiliary_unit_ids", []): auxiliary_owners[unit_id].append(capability["capability_id"])
    if set(canonical_owners) != expected_canonical: mapping_errors.append(f"canonical unit coverage mismatch missing={len(expected_canonical-set(canonical_owners))} extra={len(set(canonical_owners)-expected_canonical)}")
    duplicate_canonical = {key: value for key, value in canonical_owners.items() if len(value) != 1}
    if duplicate_canonical: mapping_errors.append(f"canonical units with non-unique ownership: {sorted(duplicate_canonical)[:10]}")
    auxiliary = load(workspace / "curation/v2/units/auxiliary.json")["units"]
    expected_auxiliary = {item["id"] for item in auxiliary if item["v2_disposition"] == "retain"}
    if set(auxiliary_owners) != expected_auxiliary: mapping_errors.append(f"retained auxiliary coverage mismatch missing={len(expected_auxiliary-set(auxiliary_owners))} extra={len(set(auxiliary_owners)-expected_auxiliary)}")
    duplicate_auxiliary = {key: value for key, value in auxiliary_owners.items() if len(value) != 1}
    if duplicate_auxiliary: mapping_errors.append(f"auxiliary units with non-unique ownership: {sorted(duplicate_auxiliary)[:10]}")
    unsupported = [item for item in auxiliary if item.get("source_validation") == "unsupported-summary"]
    if len(unsupported) != 8 or any(item["v2_disposition"] != "defer" for item in unsupported): mapping_errors.append("8 unsupported auxiliary summaries must remain deferred")
    add("cluster-canonical-auxiliary-ownership", mapping_errors)

    root_source = load(workspace / "curation/v2/units/root-derived.json")["units"]
    root_map = load(workspace / "curation/v2/lifecycle/root-atom-map.json")["records"]
    root_errors: list[str] = []
    source_ids = [item["id"] for item in root_source]; mapped_ids = [item["atom_id"] for item in root_map]
    if set(mapped_ids) != set(source_ids) or duplicate_values(mapped_ids): root_errors.append("1,138 root-derived records are not decided exactly once")
    source_by_id = {item["id"]: item for item in root_source}; map_by_id = {item["atom_id"]: item for item in root_map}
    representatives = {item["id"] for item in root_source if item["v2_disposition"] != "merge"}
    if len(representatives) != 930: root_errors.append(f"expected 930 distinct representative atoms, got {len(representatives)}")
    for atom_id in representatives:
        record = map_by_id.get(atom_id, {})
        if record.get("disposition") not in {"assign", "defer", "exclude"}: root_errors.append(f"{atom_id}: representative lacks assign/defer/exclude decision")
        if record.get("disposition") == "assign" and record.get("capability_id") not in capabilities: root_errors.append(f"{atom_id}: unknown assigned capability")
        if record.get("disposition") in {"defer", "exclude"} and not record.get("rationale"): root_errors.append(f"{atom_id}: {record.get('disposition')} lacks rationale")
    merges = [item for item in root_source if item["v2_disposition"] == "merge"]
    if len(merges) != 208: root_errors.append(f"expected 208 exact merges, got {len(merges)}")
    for atom in merges:
        record = map_by_id.get(atom["id"], {}); target = map_by_id.get(atom.get("target_unit_id"), {})
        if record.get("disposition") != "merge" or record.get("target_atom_id") != atom.get("target_unit_id"): root_errors.append(f"{atom['id']}: merge target mismatch")
        if not target or record.get("capability_id") != target.get("capability_id"): root_errors.append(f"{atom['id']}: merge does not inherit target classification")
    add("root-derived-atom-decisions", root_errors)

    fusion_path = workspace / "curation/v2/fusion/decisions.jsonl"
    fusion = [json.loads(line) for line in fusion_path.read_text(encoding="utf-8").splitlines() if line.strip()]
    fusion_errors: list[str] = []
    fusion_ids = [item["id"] for item in fusion]
    fusion_by_kind: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for item in fusion: fusion_by_kind[item["kind"]].append(item)
    if duplicate_values(fusion_ids): fusion_errors.append("fusion decision IDs are not unique")
    if {item["subject"] for item in fusion_by_kind["legacy-cluster-mapping"]} != set(mapped_clusters): fusion_errors.append("fusion ledger does not cover every legacy cluster exactly once")
    if {item["subject"] for item in fusion_by_kind["root-derived-atom"]} != set(mapped_ids): fusion_errors.append("fusion ledger does not cover every root-derived atom exactly once")
    expected_splits = {"audit-website:unit-005", "subagent-driven-development:unit-001", "subagent-driven-development:unit-002", "subagent-driven-development:unit-003", "subagent-driven-development:unit-004", "subagent-driven-development:unit-005", "subagent-driven-development:unit-006", "subagent-driven-development:unit-007", "subagent-driven-development:unit-008", "subagent-driven-development:unit-009", "subagent-driven-development:unit-010", "subagent-driven-development:unit-017", "subagent-driven-development:unit-018"}
    if {item["subject"] for item in fusion_by_kind["canonical-unit-split"]} != expected_splits: fusion_errors.append("canonical split ledger does not preserve all atomic responsibility decisions")
    if {item["subject"] for item in fusion_by_kind["auxiliary-unit-split"]} != {"skills/subagent-driven-development/SKILL.md:summary:parallel-tasks"}: fusion_errors.append("auxiliary split ledger does not preserve the orchestration responsibility decision")
    expected_fragments = {"gstack/review/greptile-triage.md:97-111", "gstack/ship/sections/pr-body.md:59-67", "gstack/ship/sections/pr-body.md:180-225", "gstack/land-and-deploy/sections/merge-and-deploy.md:1-145"}
    if {item["subject"] for item in fusion_by_kind["source-fragment-split"]} != expected_fragments: fusion_errors.append("support-file fragment split ledger does not preserve all remote-write responsibilities")
    fusion_id_set = set(fusion_ids)
    for capability in capabilities.values():
        missing = set(capability["fusion_decision_ids"]) - fusion_id_set
        if missing: fusion_errors.append(f"{capability['capability_id']}: unknown fusion decisions {sorted(missing)}")
        if not set(capability["fusion_decision_ids"]) & fusion_id_set: fusion_errors.append(f"{capability['capability_id']}: no linked fusion decision")
    add("fusion-provenance", fusion_errors)

    permission_doc = load(workspace / "curation/v2/lifecycle/permission-identities.json")
    permission_errors: list[str] = []
    identities = {item["id"]: item for item in permission_doc["identities"]}
    if set(identities) != set(PERMISSION_CONTRACTS): permission_errors.append("permission identity set mismatch")
    for identity, expected in PERMISSION_CONTRACTS.items():
        actual = identities.get(identity, {})
        if (set(actual.get("model_tools", [])), set(actual.get("host_actions", [])), actual.get("external"), actual.get("remote_write")) != expected: permission_errors.append(f"permission contract mismatch: {identity}")
    for capability_id, capability in capabilities.items():
        identity = capability["permission_identity"]
        if identity not in identities: permission_errors.append(f"{capability_id}: unknown permission identity {identity}")
        if capability_id in REVIEW_ONLY:
            permission = identities.get(identity, {})
            if {"edit", "write"} & set(permission.get("model_tools", [])) or permission.get("remote_write"):
                permission_errors.append(f"{capability_id}: review-only capability has mutation authority")
        if identities.get(identity, {}).get("remote_write"):
            text = " ".join(capability["inputs"] + capability["hard_gates"] + capability["stop_conditions"]).casefold()
            if "authoriz" not in text: permission_errors.append(f"{capability_id}: external write lacks explicit authorization contract")
    atom_owners = {atom_id: capability_id for capability_id, capability in capabilities.items() for atom_id in capability.get("root_derived_atom_ids", [])}
    for atom_id, expected_capability_id in MUTATION_ATOM_TARGETS.items():
        if atom_owners.get(atom_id) != expected_capability_id:
            permission_errors.append(f"mutation atom identity mismatch: {atom_id} -> {atom_owners.get(atom_id)}, expected {expected_capability_id}")
    forbidden = FORBIDDEN_ATOMIC_CAPABILITIES & set(capabilities)
    if forbidden: permission_errors.append(f"multi-stage workflow shells emitted as atomic capabilities: {sorted(forbidden)}")
    add("permission-separation", permission_errors)

    policy_errors: list[str] = []
    for capability_id, capability in capabilities.items():
        refs = set(capability["decision_references"])
        required = {"V2-DEC-001", "V2-DEC-006"} | POLICY_REQUIREMENTS.get(capability["primary_domain_id"], set())
        missing = required - refs
        if missing: policy_errors.append(f"{capability_id}: missing policy references {sorted(missing)}")
        if any(term in capability_id for term in ("interview", "feedback", "data-analysis", "llm-quality", "ai-observability", "trace-root", "production-trace", "evaluator", "evaluation-dataset", "llm-experiment")) and "V2-DEC-004" not in refs:
            policy_errors.append(f"{capability_id}: data-bearing capability missing V2-DEC-004")
        for variant in capability["provider_or_framework_variants"]:
            if not variant.get("applies_when") or not variant.get("provider") or not variant.get("environment"): policy_errors.append(f"{capability_id}: incomplete provider/framework variant")
    add("fusion-policy-application", policy_errors)

    dependencies = load(workspace / "curation/v2/lifecycle/dependencies.json")
    dependency_errors: list[str] = []
    stage_order = {item["id"]: item["order"] for item in stages}
    for edge in dependencies["hard_dag_edges"]:
        if edge["source_capability_id"] not in capabilities or edge["target_capability_id"] not in capabilities: dependency_errors.append(f"unknown hard dependency endpoint: {edge}")
        elif stage_order[capabilities[edge["source_capability_id"]]["lifecycle_stage_id"]] >= stage_order[capabilities[edge["target_capability_id"]]["lifecycle_stage_id"]]: dependency_errors.append(f"hard dependency is not forward-stage: {edge}")
    cycles = cycle_nodes(dependencies["hard_dag_edges"], set(capabilities))
    if cycles: dependency_errors.append(f"hard dependency cycle: {sorted(cycles)}")
    touched = {edge["source_capability_id"] for edge in dependencies["records"]} | {edge["target_capability_id"] for edge in dependencies["records"]}
    isolated = set(capabilities) - touched
    if isolated: dependency_errors.append(f"dependency graph isolated capabilities: {sorted(isolated)}")
    handoffs = load(workspace / "curation/v2/lifecycle/handoffs.json")
    if handoffs.get("count") != 13 or len(handoffs.get("records", [])) != 13: dependency_errors.append("expected 13 mandatory-stage handoff contracts")
    for item in handoffs.get("records", []):
        if not item.get("artifact_contract") or not item.get("invalidation"): dependency_errors.append(f"incomplete handoff contract: {item.get('id')}")
    ownership = load(workspace / "curation/v2/lifecycle/phase-ownership.json")
    owned_ids = [capability_id for phase, ids in ownership["phases"].items() for capability_id in ids]
    if set(owned_ids) != set(capabilities) or duplicate_values(owned_ids): dependency_errors.append("Phase 3-7 ownership does not assign every capability exactly once")
    for phase, ids in ownership["phases"].items():
        if any(capabilities[capability_id]["owning_phase"] != int(phase) for capability_id in ids): dependency_errors.append(f"owning phase mismatch in Phase {phase}")
    add("dependency-dag-handoffs-and-phase-ownership", dependency_errors)

    errors = [f"{check['name']}: {error}" for check in checks for error in check["errors"]]
    return {"gate": "capability-compiler-v2-phase-2", "ok": not errors, "checks": checks, "counts": {"domains": len(domain_ids), "stages": len(stage_ids), "capabilities": len(capabilities), "legacy_clusters": len(cluster_map), "canonical_units": len(expected_canonical), "retained_auxiliary_units": len(expected_auxiliary), "root_atoms": len(root_map), "fusion_decisions": len(fusion)}, "errors": errors}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workspace-root", type=Path, default=Path("."))
    parser.add_argument("--output", type=Path)
    args = parser.parse_args(); result = verify(args.workspace_root)
    if args.output:
        output = args.output if args.output.is_absolute() else args.workspace_root / args.output
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
