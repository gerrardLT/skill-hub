#!/usr/bin/env python3
"""Build a read-only, byte-level preview of the proposed V2 local release."""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import re
from pathlib import Path
from typing import Any

VERSION = "1.0.0"
PHASE_TREES = {
    "phase9": "7540c53426a5dff605c3f751fdaf105f52059ffbafce213d77c9c3db94214152",
    "phase10": "7fd6640a563789257da77e1015be3f37033a3baf40ecaf9a4b9fa1fde7828d56",
    "phase11": "275a2139cf207ac50105d3e65fd2138b371a3e2dbe0dce4b05ab043cb1cd5fbc",
}
SKILL_ROOT = Path("slots/v2/1.0.0/skills")
RECIPE_ROOT = Path("recipes/v2/1.0.0")


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def rendered(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode()


def sha_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha(path: Path) -> str:
    return sha_bytes(path.read_bytes())


def target_record(path: Path, data: bytes, source: str, transformation: str) -> dict[str, Any]:
    return {"target": path.as_posix(), "bytes": len(data), "sha256": sha_bytes(data), "source": source, "transformation": transformation}


def recipe_sources(workspace: Path) -> dict[str, tuple[str, Path]]:
    phase8 = workspace / "evals/candidates/capability-compiler-v2/phase-8/recipes"
    revision4 = workspace / "evals/candidates/capability-compiler-v2/phase-10/revision-4/phase-8/recipes"
    result: dict[str, tuple[str, Path]] = {}
    for kind in ["stages", "composites"]:
        for path in sorted((phase8 / kind).glob("*.json")):
            overlay = revision4 / kind / path.name
            selected = overlay if overlay.is_file() else path
            result[load(selected)["id"]] = (kind, selected)
    result["complete-ui-design-and-review"] = ("specialized", workspace / "evals/candidates/capability-compiler-v2/phase-10/revision-4/phase-4/complete-ui-design-and-review.json")
    return result


def rewrite_string(value: str, skill_paths: dict[str, str], recipe_paths: dict[str, str]) -> str:
    for skill_id, path in skill_paths.items():
        if value.endswith(f"/skills/{skill_id}") and value.startswith("evals/candidates/capability-compiler-v2/"):
            return path
    for recipe_id, path in recipe_paths.items():
        if value.endswith(f"/{recipe_id}.json") and value.startswith("evals/candidates/capability-compiler-v2/"):
            return path
    value = re.sub(r"@(0\.1\.[0-9]+-v2-candidate)", f"@{VERSION}", value)
    return value


def rewrite(value: Any, skill_paths: dict[str, str], recipe_paths: dict[str, str]) -> Any:
    if isinstance(value, str):
        return rewrite_string(value, skill_paths, recipe_paths)
    if isinstance(value, list):
        return [rewrite(item, skill_paths, recipe_paths) for item in value]
    if isinstance(value, dict):
        return {key: rewrite(item, skill_paths, recipe_paths) for key, item in value.items()}
    return value


def build(workspace: Path, *, include_assets: bool = False) -> dict[str, Any] | tuple[dict[str, Any], dict[str, bytes]]:
    workspace = workspace.resolve()
    if load(workspace / ".specs/capability-compiler-v2/phase-10/artifact-manifest.json")["tree_sha256"] != PHASE_TREES["phase10"]:
        raise ValueError("Phase 10 tree drift")
    if load(workspace / ".specs/capability-compiler-v2/phase-11/artifact-manifest.json")["tree_sha256"] != PHASE_TREES["phase11"]:
        raise ValueError("Phase 11 tree drift")

    candidate_index = load(workspace / "evals/candidates/capability-compiler-v2/phase-8/skill-index.json")
    if candidate_index.get("skill_count") != 157:
        raise ValueError("candidate index is not exactly 157")
    existing_v1 = {path.name for path in (workspace / "slots").iterdir() if path.is_dir()}
    collisions = sorted(item["id"] for item in candidate_index["skills"] if item["id"] in existing_v1)
    if (workspace / "slots/v2").exists() or (workspace / "recipes/v2").exists():
        raise ValueError("proposed V2 release namespace already exists")

    targets: list[dict[str, Any]] = []
    asset_bytes: dict[str, bytes] = {}
    def add_target(path: Path, data: bytes, source: str, transformation: str) -> None:
        key = path.as_posix()
        if key in asset_bytes:
            raise ValueError(f"duplicate release target {key}")
        asset_bytes[key] = data
        targets.append(target_record(path, data, source, transformation))

    skill_paths = {item["id"]: (SKILL_ROOT / item["id"]).as_posix() for item in candidate_index["skills"]}
    released_contract_hashes: dict[str, str] = {}
    skill_catalog_records = []
    for item in sorted(candidate_index["skills"], key=lambda record: record["id"]):
        skill_id = item["id"]; source_dir = workspace / item["candidate_path"]; target_dir = SKILL_ROOT / skill_id
        skill_bytes = (source_dir / "SKILL.md").read_bytes()
        contract = load(source_dir / "contract.json"); candidate_version = contract["version"]
        contract["version"] = VERSION; contract["status"] = "released"
        contract_bytes = rendered(contract); released_contract_hashes[skill_id] = sha_bytes(contract_bytes)
        original_provenance = load(source_dir / "provenance.json")
        provenance = {
            "schema_version": "2.0", "id": skill_id, "version": VERSION, "status": "released",
            "capability_id": contract["capability_id"], "candidate_phase": item["phase"],
            "candidate_identity": {"path": item["candidate_path"], "version": candidate_version, "status": item["status"], "skill_sha256": item["skill_sha256"], "contract_sha256": item["contract_sha256"], "trigger_cases_sha256": item["trigger_cases_sha256"]},
            "candidate_provenance": original_provenance,
            "release_evidence": PHASE_TREES,
            "release_files": {"SKILL.md": sha_bytes(skill_bytes), "contract.json": sha_bytes(contract_bytes)},
        }
        provenance_bytes = rendered(provenance)
        add_target(target_dir / "SKILL.md", skill_bytes, (source_dir / "SKILL.md").relative_to(workspace).as_posix(), "exact-copy")
        add_target(target_dir / "contract.json", contract_bytes, (source_dir / "contract.json").relative_to(workspace).as_posix(), "version=1.0.0,status=released")
        add_target(target_dir / "provenance.json", provenance_bytes, (source_dir / "provenance.json").relative_to(workspace).as_posix(), "wrap-candidate-provenance-and-bind-phase9-11-evidence")
        skill_catalog_records.append({"id": skill_id, "path": target_dir.as_posix(), "contract_sha256": sha_bytes(contract_bytes), "skill_sha256": sha_bytes(skill_bytes), "provenance_sha256": sha_bytes(provenance_bytes), "permission_identity": contract["permission_identity"], "mutation_scope": contract["execution"]["mutation_scope"], "remote_write": contract["execution"]["remote_write"]})

    recipe_source_map = recipe_sources(workspace)
    recipe_paths = {}
    for recipe_id, (kind, _) in recipe_source_map.items():
        directory = {"stages": "stages", "composites": "composites", "specialized": "specialized"}[kind]
        recipe_paths[recipe_id] = (RECIPE_ROOT / directory / f"{recipe_id}.json").as_posix()

    transformed_recipes: dict[str, bytes] = {}
    recipe_records = []
    for recipe_id, (kind, source) in sorted(recipe_source_map.items()):
        document = rewrite(copy.deepcopy(load(source)), skill_paths, recipe_paths)
        document["version"] = VERSION; document["status"] = "released"
        if "execution_state" in document: document["execution_state"] = "release-definition-not-executed"
        if "evaluation_state" in document: document["evaluation_state"] = "phase-10-accepted"
        def update_contract_hashes(value: Any) -> None:
            if isinstance(value, dict):
                if isinstance(value.get("id"), str) and value["id"] in released_contract_hashes and "contract_sha256" in value:
                    value["contract_sha256"] = released_contract_hashes[value["id"]]
                for child in value.values(): update_contract_hashes(child)
            elif isinstance(value, list):
                for child in value: update_contract_hashes(child)
        update_contract_hashes(document)
        data = rendered(document); transformed_recipes[recipe_id] = data
        target = Path(recipe_paths[recipe_id])
        add_target(target, data, source.relative_to(workspace).as_posix(), "accepted-revision-overlay; rewrite-skill-and-recipe-paths; version=1.0.0,status=released")
        recipe_records.append({"id": recipe_id, "kind": kind, "path": target.as_posix(), "sha256": sha_bytes(data), "source": source.relative_to(workspace).as_posix()})

    router_source = workspace / "evals/candidates/capability-compiler-v2/phase-10/revision-4/phase-8/router.json"
    router = rewrite(copy.deepcopy(load(router_source)), skill_paths, recipe_paths)
    router["version"] = VERSION; router["status"] = "released"; router["execution_state"] = "release-definition-not-executed"
    router["atomic_index_ref"] = "slots/v2/catalog.json"
    router_bytes = rendered(router)
    add_target(RECIPE_ROOT / "router.json", router_bytes, router_source.relative_to(workspace).as_posix(), "accepted-revision-4; rewrite-target-paths; version=1.0.0,status=released")

    skill_catalog = {"schema_version": "2.0", "version": VERSION, "status": "released", "skill_count": 157, "skills": skill_catalog_records, "release_evidence": PHASE_TREES}
    recipe_catalog = {"schema_version": "2.0", "version": VERSION, "status": "released", "stage_recipe_count": 15, "composite_recipe_count": 5, "specialized_recipe_count": 1, "router_count": 1, "recipes": recipe_records, "router": {"path": (RECIPE_ROOT / "router.json").as_posix(), "sha256": sha_bytes(router_bytes)}, "release_evidence": PHASE_TREES}
    add_target(Path("slots/v2/catalog.json"), rendered(skill_catalog), "evals/candidates/capability-compiler-v2/phase-8/skill-index.json", "released-skill-catalog")
    add_target(Path("recipes/v2/catalog.json"), rendered(recipe_catalog), "accepted-phase8-revision4-recipes", "released-recipe-and-router-catalog")

    release_assets = sorted(targets, key=lambda item: item["target"])
    digest = hashlib.sha256("".join(f"{item['target']}\0{item['sha256']}\n" for item in release_assets).encode()).hexdigest()
    existing_targets = [item["target"] for item in release_assets if (workspace / item["target"]).exists()]
    preview = {
        "schema_version": "2.0", "release_version": VERSION, "status": "awaiting-final-user-approval",
        "release_namespace": {"skills": SKILL_ROOT.as_posix(), "recipes": RECIPE_ROOT.as_posix()},
        "source_candidate": "0.1.4-v2-candidate", "source_phase_trees": PHASE_TREES,
        "counts": {"skills": 157, "skill_files": 471, "stage_recipes": 15, "composite_recipes": 5, "specialized_recipes": 1, "routers": 1, "catalogs": 2, "release_assets": len(release_assets), "v1_id_collisions_avoided": len(collisions)},
        "v1_collisions": collisions, "existing_release_targets": existing_targets,
        "release_asset_tree_sha256": digest, "release_assets": release_assets,
        "compatibility_mutations": [
            {"path": "tools/curation/slot_verify.py", "change": "ignore only reserved top-level slots/v2 subtree when validating V1 flat Slots"},
            {"path": "tools/curation/generate_slots.py", "change": "preserve existing slots/v2 subtree across V1 flat-slot regeneration"},
            {"path": "tools/curation/run_all_gates.py", "change": "append v2-phase12 release Gate"}
        ],
        "release_control_targets": [
            "curation/v2/release-1.0.0/approval.json", "curation/v2/release-1.0.0/manifest.json", "curation/v2/release-1.0.0/lock.json", "curation/v2/release-1.0.0/rollback.json", "curation/v2/release-1.0.0/release-notes.md",
            "tools/curation/v2_phase12_release.py", "tools/curation/v2_phase12_gate.py", "tools/curation/v2_phase12_report.py", "tests/curation/test_v2_phase12_gate.py",
            ".specs/capability-compiler-v2/phase-12/gate-report.json", ".specs/capability-compiler-v2/phase-12/artifact-manifest.json", ".specs/capability-compiler-v2/phase-12/phase-report.json"
        ],
        "source_paths_modified": [], "phase0_11_evidence_modified": [], "v1_assets_overwritten": [],
        "remote_actions": [], "commit_push_pr_merge_deploy": False,
        "approval_required": True,
    }
    return (preview, asset_bytes) if include_assets else preview


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__); parser.add_argument("--workspace-root", type=Path, default=Path(".")); parser.add_argument("--output", type=Path, required=True); args = parser.parse_args()
    result = build(args.workspace_root); output = args.output if args.output.is_absolute() else args.workspace_root / args.output; output.parent.mkdir(parents=True, exist_ok=True); output.write_text(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"ok": True, "counts": result["counts"], "release_asset_tree_sha256": result["release_asset_tree_sha256"], "existing_release_targets": result["existing_release_targets"]}, ensure_ascii=False, sort_keys=True)); return 0


if __name__ == "__main__":
    raise SystemExit(main())
