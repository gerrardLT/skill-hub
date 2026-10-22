#!/usr/bin/env python3
"""Fail-closed gate for the approved local Capability Compiler V2 1.0.0 release."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path
from typing import Any

VERSION = "1.0.0"
RELEASE_TREE = "116651adca2b907b3629e7e1954cddcd15cf0388e3401facaf2e8cb5c210d852"
V1_TREE = "1337c1dcbfb180906b417a6917863127fa09137e9d7650f51d82a1a1cf95e1b6"
PHASE_TREES = {
    "phase9": "7540c53426a5dff605c3f751fdaf105f52059ffbafce213d77c9c3db94214152",
    "phase10": "7fd6640a563789257da77e1015be3f37033a3baf40ecaf9a4b9fa1fde7828d56",
    "phase11": "275a2139cf207ac50105d3e65fd2138b371a3e2dbe0dce4b05ab043cb1cd5fbc",
}
PROTECTED_IDENTITIES = {"remote-write-authorized-only", "local-system-write-authorized-only", "local-system-write-external-session-authorized-only"}


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def tree(records: list[dict[str, Any]], path_key: str = "path", *, preserve_order: bool = False) -> str:
    ordered = records if preserve_order else sorted(records, key=lambda item: item[path_key])
    return hashlib.sha256("".join(f"{item[path_key]}\0{item['sha256']}\n" for item in ordered).encode()).hexdigest()


def released_files(workspace: Path) -> list[str]:
    result = []
    for root in [workspace / "slots/v2", workspace / "recipes/v2"]:
        result.extend(path.relative_to(workspace).as_posix() for path in root.rglob("*") if path.is_file())
    return sorted(result)


def v1_records(workspace: Path) -> list[dict[str, Any]]:
    paths = []
    for base in [workspace / "slots", workspace / "recipes"]:
        for path in sorted(base.iterdir()):
            if path.name == "v2":
                continue
            paths.extend([path] if path.is_file() else [item for item in sorted(path.rglob("*")) if item.is_file()])
    return [{"path": path.relative_to(workspace).as_posix(), "sha256": sha(path)} for path in paths]


def verify_release_assets(workspace: Path, manifest: dict[str, Any] | None = None) -> list[str]:
    errors = []
    try:
        manifest = manifest or load(workspace / "curation/v2/release-1.0.0/manifest.json")
        records = manifest.get("release_assets", [])
        if len(records) != 495 or manifest.get("release_asset_count") != 495:
            errors.append("release manifest does not contain exactly 495 assets")
        declared = [item.get("path") for item in records if isinstance(item, dict)]
        if len(declared) != len(set(declared)):
            errors.append("release manifest contains duplicate targets")
        if any(not isinstance(path, str) or not path.startswith(("slots/v2/", "recipes/v2/")) for path in declared):
            errors.append("release manifest target escaped isolated V2 namespaces")
        if released_files(workspace) != sorted(declared):
            errors.append("released namespace files differ from manifest")
        for item in records:
            path = workspace / item.get("path", "missing")
            if not path.is_file() or path.stat().st_size != item.get("bytes") or sha(path) != item.get("sha256"):
                errors.append(f"released asset mismatch: {item.get('path')}")
        computed = tree(records)
        if computed != RELEASE_TREE or manifest.get("release_asset_tree_sha256") != RELEASE_TREE:
            errors.append("released asset tree differs from approved preview")
    except Exception as exc:
        errors.append(f"release asset verification failed: {type(exc).__name__}:{exc}")
    return errors


def verify_phase12_manifest(workspace: Path) -> list[str]:
    errors = []; manifest_path = workspace / ".specs/capability-compiler-v2/phase-12/artifact-manifest.json"
    try:
        manifest = load(manifest_path); records = manifest.get("artifacts", [])
        excluded = {".specs/capability-compiler-v2/phase-12/artifact-manifest.json", ".specs/capability-compiler-v2/phase-12/phase-report.json", ".specs/capability-compiler-v2/phase-12/gate-report.json"}
        if manifest.get("phase") != 12 or manifest.get("artifact_count") != len(records) or any(item.get("path") in excluded for item in records):
            errors.append("Phase 12 artifact manifest identity/count/exclusions mismatch")
        for item in records:
            path = workspace / item.get("path", "missing")
            normalized = path.read_bytes().replace(b"\r\n", b"\n") if path.is_file() else b""
            if not path.is_file() or path.stat().st_size != item.get("bytes") or hashlib.sha256(normalized).hexdigest() != item.get("sha256"):
                errors.append(f"Phase 12 artifact mismatch: {item.get('path')}")
        if tree(records, preserve_order=True) != manifest.get("tree_sha256"):
            errors.append("Phase 12 artifact tree mismatch")
    except Exception as exc:
        errors.append(f"Phase 12 artifact manifest verification failed: {type(exc).__name__}:{exc}")
    return errors


def verify(workspace: Path, *, require_final_report: bool = False) -> dict[str, Any]:
    workspace = workspace.resolve(); control = workspace / "curation/v2/release-1.0.0"; checks = []
    def add(name: str, errors: list[str]) -> None:
        checks.append({"name": name, "ok": not errors, "errors": errors})

    approval_errors = []
    try:
        preview_path = workspace / ".specs/capability-compiler-v2/phase-12/release-preview.json"
        preview = load(preview_path); approval = load(control / "approval.json")
        if approval.get("decision") != "approved-controlled-local-release" or approval.get("release_version") != VERSION:
            approval_errors.append("controlled local release approval missing")
        if approval.get("preview_sha256") != sha(preview_path) or approval.get("release_asset_tree_sha256") != RELEASE_TREE:
            approval_errors.append("approval is not bound to the exact preview")
        if preview.get("release_asset_tree_sha256") != RELEASE_TREE or preview.get("counts", {}).get("release_assets") != 495 or preview.get("existing_release_targets") != []:
            approval_errors.append("approved preview identity/count/collision record mismatch")
        if preview.get("approval_required") is not True or preview.get("remote_actions") != [] or preview.get("commit_push_pr_merge_deploy") is not False:
            approval_errors.append("preview authority boundary changed")
        if approval.get("remote_actions") != [] or approval.get("commit_push_pr_merge_deploy") is not False:
            approval_errors.append("approval widened to remote or Git delivery actions")
        forbidden = {"commit", "push", "pull request", "merge", "deploy", "provider mutation", "production action", "credential action", "browser login"}
        if not forbidden.issubset(set(approval.get("not_authorized", []))):
            approval_errors.append("approval omits a protected non-authorized action")
    except Exception as exc:
        approval_errors.append(f"approval verification failed: {type(exc).__name__}:{exc}")
    add("exact-human-approval-and-authority-boundary", approval_errors)

    manifest_errors = []
    try:
        manifest = load(control / "manifest.json")
        manifest_errors.extend(verify_release_assets(workspace, manifest))
        if manifest.get("status") != "released" or manifest.get("release_version") != VERSION:
            manifest_errors.append("release manifest identity/status mismatch")
        if manifest.get("counts") != preview.get("counts") or manifest.get("source_phase_trees") != PHASE_TREES:
            manifest_errors.append("release manifest counts or source evidence changed")
        if manifest.get("source_paths_modified") != [] or manifest.get("phase0_11_evidence_modified") != [] or manifest.get("v1_assets_overwritten") != []:
            manifest_errors.append("release manifest claims forbidden source, prior evidence, or V1 mutation")
        if manifest.get("remote_actions") != [] or manifest.get("commit_push_pr_merge_deploy") is not False:
            manifest_errors.append("release manifest claims unauthorized external action")
    except Exception as exc:
        manifest_errors.append(f"manifest verification failed: {type(exc).__name__}:{exc}")
    add("byte-exact-release-manifest", manifest_errors)

    skill_errors = []; skill_contracts = {}; skill_hashes = {}
    try:
        catalog = load(workspace / "slots/v2/catalog.json"); skills = catalog.get("skills", [])
        if catalog.get("schema_version") != "2.0" or catalog.get("version") != VERSION or catalog.get("status") != "released" or catalog.get("skill_count") != 157 or len(skills) != 157:
            skill_errors.append("released Skill catalog identity/count mismatch")
        ids = [item.get("id") for item in skills]
        if len(ids) != len(set(ids)):
            skill_errors.append("released Skill IDs are not unique")
        for item in skills:
            skill_id = item.get("id"); root = workspace / item.get("path", "missing")
            expected_path = f"slots/v2/{VERSION}/skills/{skill_id}"
            if item.get("path") != expected_path or sorted(path.name for path in root.iterdir()) != ["SKILL.md", "contract.json", "provenance.json"]:
                skill_errors.append(f"Skill layout mismatch: {skill_id}"); continue
            contract_path = root / "contract.json"; skill_path = root / "SKILL.md"; provenance_path = root / "provenance.json"
            contract = load(contract_path); provenance = load(provenance_path); text = skill_path.read_text(encoding="utf-8")
            skill_contracts[skill_id] = contract; skill_hashes[skill_id] = item.get("contract_sha256")
            if contract.get("id") != skill_id or contract.get("capability_id") != f"capability:{skill_id}" or contract.get("version") != VERSION or contract.get("status") != "released":
                skill_errors.append(f"Skill contract identity mismatch: {skill_id}")
            if contract.get("execution", {}).get("remote_write") is not item.get("remote_write") or contract.get("permission_identity") != item.get("permission_identity") or contract.get("execution", {}).get("mutation_scope") != item.get("mutation_scope"):
                skill_errors.append(f"Skill permission identity mismatch: {skill_id}")
            if sha(contract_path) != item.get("contract_sha256") or sha(skill_path) != item.get("skill_sha256") or sha(provenance_path) != item.get("provenance_sha256"):
                skill_errors.append(f"Skill catalog hash mismatch: {skill_id}")
            if provenance.get("id") != skill_id or provenance.get("version") != VERSION or provenance.get("status") != "released" or provenance.get("release_evidence") != PHASE_TREES:
                skill_errors.append(f"Skill provenance/release evidence mismatch: {skill_id}")
            if provenance.get("release_files") != {"SKILL.md": sha(skill_path), "contract.json": sha(contract_path)}:
                skill_errors.append(f"Skill release file binding mismatch: {skill_id}")
            match = re.match(r"---\s*\nname:\s*([^\n]+)", text)
            if not match or match.group(1).strip() != skill_id or "## Trigger" not in text or "Do not use when:" not in text or "## Output Contract" not in text:
                skill_errors.append(f"Skill semantic boundary sections missing: {skill_id}")
        if set(skill_contracts) != set(ids):
            skill_errors.append("not all catalog Skills loaded")
    except Exception as exc:
        skill_errors.append(f"Skill verification failed: {type(exc).__name__}:{exc}")
    add("released-atomic-skills-contracts-and-provenance", skill_errors)

    recipe_errors = []; protected = []; primary = []
    try:
        catalog = load(workspace / "recipes/v2/catalog.json"); records = catalog.get("recipes", [])
        if (catalog.get("stage_recipe_count"), catalog.get("composite_recipe_count"), catalog.get("specialized_recipe_count"), catalog.get("router_count"), len(records)) != (15, 5, 1, 1, 21):
            recipe_errors.append("released Recipe/router counts mismatch")
        recipe_ids = {item.get("id") for item in records}; documents = {}
        for item in records:
            path = workspace / item.get("path", "missing"); document = load(path); recipe_id = item.get("id"); documents[recipe_id] = document
            if sha(path) != item.get("sha256") or document.get("id") != recipe_id or document.get("version") != VERSION or document.get("status") != "released":
                recipe_errors.append(f"Recipe identity/hash mismatch: {recipe_id}")
            if item.get("kind") == "stages":
                for step in document.get("steps", []):
                    primary.append(step.get("id")); ref = step.get("skill_ref", ""); skill_id = ref.removesuffix(f"@{VERSION}")
                    if ref != f"{step.get('id')}@{VERSION}" or skill_id not in skill_contracts or step.get("candidate_path") != f"slots/v2/{VERSION}/skills/{skill_id}" or step.get("contract_sha256") != skill_hashes.get(skill_id):
                        recipe_errors.append(f"stage Skill reference mismatch: {recipe_id}:{step.get('id')}")
                    is_protected = step.get("remote_write") is True or step.get("permission_identity") in PROTECTED_IDENTITIES or step.get("mutation_scope") == "authorized-local-git"
                    if is_protected:
                        protected.append((recipe_id, step.get("id")))
                        if step.get("activation") != "disabled-pending-current-authorization":
                            recipe_errors.append(f"protected step not disabled: {recipe_id}:{step.get('id')}")
            if item.get("kind") == "composites":
                for stage in document.get("stage_steps", []):
                    ref = stage.get("recipe_ref", ""); target = ref.removesuffix(f"@{VERSION}")
                    if target not in recipe_ids or ref != f"{target}@{VERSION}":
                        recipe_errors.append(f"composite stage reference mismatch: {recipe_id}:{ref}")
            if item.get("kind") == "specialized":
                for step in document.get("steps", []):
                    ref = step.get("skill_ref", ""); skill_id = ref.removesuffix(f"@{VERSION}")
                    if skill_id not in skill_contracts or ref != f"{skill_id}@{VERSION}":
                        recipe_errors.append(f"specialized Skill reference mismatch: {recipe_id}:{ref}")
        if len(primary) != 157 or len(set(primary)) != 157 or set(primary) != set(skill_contracts):
            recipe_errors.append("157 atomic Skills are not assigned exactly once to primary stage Recipes")
        if len(protected) != 27:
            recipe_errors.append(f"protected step count is {len(protected)}, expected 27")
        router_path = workspace / "recipes/v2/1.0.0/router.json"; router = load(router_path)
        if sha(router_path) != catalog.get("router", {}).get("sha256") or router.get("id") != "capability-compiler-v2-router" or router.get("version") != VERSION or router.get("status") != "released":
            recipe_errors.append("router identity/hash mismatch")
        routed = [(item.get("id"), item.get("path")) for key in ["stage_targets", "specialized_targets", "composite_targets"] for item in router.get(key, [])]
        expected = {(item["id"], item["path"]) for item in records}
        if set(routed) != expected or len(routed) != 21:
            recipe_errors.append("router targets do not exactly cover released Recipes")
        if router.get("atomic_index_ref") != "slots/v2/catalog.json" or router.get("fallback", {}).get("status") != "needs-input" or len(router.get("safety_dispositions", [])) != 4 or any(item.get("executable") is not False or item.get("authorization_propagates") is not False for item in router.get("safety_dispositions", [])):
            recipe_errors.append("router fail-closed safety contract mismatch")
    except Exception as exc:
        recipe_errors.append(f"Recipe/router verification failed: {type(exc).__name__}:{exc}")
    add("recipes-router-and-protected-action-boundaries", recipe_errors)

    lock_errors = []
    try:
        lock = load(control / "lock.json")
        if lock.get("release_version") != VERSION or lock.get("status") != "released" or lock.get("release_asset_tree_sha256") != RELEASE_TREE or lock.get("skill_count") != 157 or lock.get("recipe_count") != 21:
            lock_errors.append("release lock identity/count mismatch")
        if set(lock.get("skills", {})) != set(skill_contracts) or set(lock.get("recipes", {})) != recipe_ids:
            lock_errors.append("release lock does not cover exact Skill/Recipe IDs")
        for skill_id, item in lock.get("skills", {}).items():
            if item.get("ref") != f"{skill_id}@{VERSION}" or item.get("contract_sha256") != skill_hashes.get(skill_id):
                lock_errors.append(f"release lock Skill mismatch: {skill_id}")
        if lock.get("router", {}).get("ref") != f"capability-compiler-v2-router@{VERSION}":
            lock_errors.append("release lock router mismatch")
    except Exception as exc:
        lock_errors.append(f"lock verification failed: {type(exc).__name__}:{exc}")
    add("version-lock-and-reference-integrity", lock_errors)

    compatibility_errors = []
    try:
        records = v1_records(workspace)
        if len(records) != 287 or tree(records, preserve_order=True) != V1_TREE:
            compatibility_errors.append("V1 flat Slot/Recipe assets changed from pre-release identity")
        rollback = load(control / "rollback.json")
        if rollback.get("state") != "released-rollback-ready" or rollback.get("released_roots_before") != {"slots/v2": False, "recipes/v2": False} or rollback.get("released_roots_after") != {"slots/v2": True, "recipes/v2": True}:
            compatibility_errors.append("rollback pre/post state mismatch")
        if rollback.get("release_asset_tree_sha256") != RELEASE_TREE or rollback.get("remote_actions") != [] or rollback.get("source_tree_mutation_authorized") is not False or rollback.get("phase0_11_evidence_mutation_authorized") is not False:
            compatibility_errors.append("rollback authority/evidence boundary mismatch")
        for item in rollback.get("compatibility_preimages", []):
            if hashlib.sha256(item.get("content_utf8", "").encode()).hexdigest() != item.get("sha256"):
                compatibility_errors.append(f"rollback preimage corrupt: {item.get('path')}")
        post = {item.get("path"): item for item in rollback.get("compatibility_postimages", [])}
        for path in ["tools/curation/slot_verify.py", "tools/curation/generate_slots.py", "tools/curation/run_all_gates.py"]:
            if path not in post or sha(workspace / path) != post[path].get("sha256"):
                compatibility_errors.append(f"compatibility postimage mismatch: {path}")
        if 'path.name != "v2"' not in (workspace / "tools/curation/slot_verify.py").read_text(encoding="utf-8"):
            compatibility_errors.append("V1 verifier does not ignore only reserved V2 subtree")
        generator = (workspace / "tools/curation/generate_slots.py").read_text(encoding="utf-8")
        if 'released_v2 = slots_root / "v2"' not in generator or "shutil.copytree(released_v2, temp_root / \"v2\")" not in generator:
            compatibility_errors.append("V1 generator does not preserve released V2 subtree")
        if 'command("v2-phase12", "tools/curation/v2_phase12_gate.py"' not in (workspace / "tools/curation/run_all_gates.py").read_text(encoding="utf-8"):
            compatibility_errors.append("unified Gate runner omits V2 Phase 12")
    except Exception as exc:
        compatibility_errors.append(f"compatibility/rollback verification failed: {type(exc).__name__}:{exc}")
    add("v1-compatibility-and-rollback-readiness", compatibility_errors)

    evidence_errors = []
    try:
        for phase, expected in PHASE_TREES.items():
            number = phase.removeprefix("phase")
            if load(workspace / f".specs/capability-compiler-v2/phase-{number}/artifact-manifest.json").get("tree_sha256") != expected:
                evidence_errors.append(f"{phase} evidence tree drift")
        notes = (control / "release-notes.md").read_text(encoding="utf-8")
        if RELEASE_TREE not in notes or "Remote/provider/production actions: 0" not in notes or "fresh exact per-action authorization" not in notes:
            evidence_errors.append("release notes omit identity or protected-action boundary")
        if any((control / name).exists() for name in ["release-receipt.json", "v1-pre-release-manifest.json"]):
            evidence_errors.append("unpreviewed release control artifact exists")
        if require_final_report:
            evidence_errors.extend(verify_phase12_manifest(workspace))
            report = load(workspace / ".specs/capability-compiler-v2/phase-12/phase-report.json")
            if report.get("status") != "released-controlled-local-v2-1.0.0" or report.get("released") is not True or report.get("final_user_release_approval") is not True or report.get("release", {}).get("release_asset_tree_sha256") != RELEASE_TREE:
                evidence_errors.append("Phase 12 final report identity/status mismatch")
            if report.get("authority", {}).get("remote_actions") != [] or report.get("commit_push_pr_merge_deploy") is not False:
                evidence_errors.append("Phase 12 final report widens authority")
    except Exception as exc:
        evidence_errors.append(f"evidence boundary verification failed: {type(exc).__name__}:{exc}")
    add("frozen-prior-evidence-and-release-claim-boundary", evidence_errors)

    errors = [f"{check['name']}: {error}" for check in checks for error in check["errors"]]
    return {
        "gate": "capability-compiler-v2-phase-12", "ok": not errors, "released": not errors,
        "release_version": VERSION, "release_asset_tree_sha256": RELEASE_TREE,
        "counts": {"skills": 157, "stage_recipes": 15, "composite_recipes": 5, "specialized_recipes": 1, "routers": 1, "release_assets": 495, "protected_steps": len(protected), "v1_assets": 287, "remote_actions": 0},
        "checks": checks, "errors": errors,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__); parser.add_argument("--workspace-root", type=Path, default=Path(".")); parser.add_argument("--output", type=Path); parser.add_argument("--require-final-report", action="store_true"); args = parser.parse_args(); result = verify(args.workspace_root, require_final_report=args.require_final_report)
    if args.output:
        path = args.output if args.output.is_absolute() else args.workspace_root / args.output; path.parent.mkdir(parents=True, exist_ok=True); path.write_text(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps(result, ensure_ascii=False, sort_keys=True)); return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
