#!/usr/bin/env python3
"""Publish the explicitly approved V2 1.0.0 assets into isolated local namespaces."""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
import shutil
import tempfile
from pathlib import Path
from typing import Any

try:
    from tools.curation.v2_phase12_preview import build as build_preview
except ModuleNotFoundError:
    from v2_phase12_preview import build as build_preview

VERSION = "1.0.0"
PREVIEW_TREE = "116651adca2b907b3629e7e1954cddcd15cf0388e3401facaf2e8cb5c210d852"


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")


def sha_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha(path: Path) -> str:
    return sha_bytes(path.read_bytes())


def now() -> str:
    return dt.datetime.now(dt.UTC).isoformat().replace("+00:00", "Z")


def restore_compatibility(workspace: Path, rollback: dict[str, Any]) -> None:
    for item in rollback["compatibility_preimages"]:
        path = workspace / item["path"]
        path.write_text(item["content_utf8"], encoding="utf-8", newline="")


def release(workspace: Path) -> dict[str, Any]:
    workspace = workspace.resolve(); phase = workspace / ".specs/capability-compiler-v2/phase-12"; control = workspace / "curation/v2/release-1.0.0"
    preview_path = phase / "release-preview.json"; approval_path = control / "approval.json"; rollback_path = control / "rollback.json"
    stored_preview = load(preview_path); approval = load(approval_path); rollback = load(rollback_path)
    if approval.get("decision") != "approved-controlled-local-release" or approval.get("release_asset_tree_sha256") != PREVIEW_TREE:
        raise ValueError("final user approval is absent or mismatched")
    if approval.get("preview_sha256") != sha(preview_path):
        raise ValueError("approved preview bytes changed")
    if stored_preview.get("release_asset_tree_sha256") != PREVIEW_TREE or stored_preview.get("existing_release_targets") != []:
        raise ValueError("approved preview identity or collision state changed")
    if rollback.get("released_roots_before") != {"slots/v2": False, "recipes/v2": False}:
        raise ValueError("rollback pre-state does not prove absent release roots")
    for item in rollback.get("compatibility_preimages", []):
        if sha_bytes(item["content_utf8"].encode()) != item["sha256"]:
            raise ValueError(f"rollback preimage corrupt: {item['path']}")
    if (workspace / "slots/v2").exists() or (workspace / "recipes/v2").exists():
        raise FileExistsError("V2 release target already exists")

    generated, assets = build_preview(workspace, include_assets=True)
    if generated != stored_preview or len(assets) != 495:
        raise ValueError("release bytes no longer match approved preview")
    for record in stored_preview["release_assets"]:
        data = assets.get(record["target"])
        if data is None or len(data) != record["bytes"] or sha_bytes(data) != record["sha256"]:
            raise ValueError(f"approved release asset mismatch: {record['target']}")

    with tempfile.TemporaryDirectory(prefix="v2-release-", dir=workspace) as temporary:
        staging = Path(temporary)
        for relative, data in assets.items():
            target = staging / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(data)
        for record in stored_preview["release_assets"]:
            staged = staging / record["target"]
            if not staged.is_file() or staged.stat().st_size != record["bytes"] or sha(staged) != record["sha256"]:
                raise ValueError(f"staging verification failed: {record['target']}")
        try:
            os.replace(staging / "slots/v2", workspace / "slots/v2")
            os.replace(staging / "recipes/v2", workspace / "recipes/v2")
        except Exception:
            shutil.rmtree(workspace / "slots/v2", ignore_errors=True)
            shutil.rmtree(workspace / "recipes/v2", ignore_errors=True)
            restore_compatibility(workspace, rollback)
            raise

    actual = []
    for record in stored_preview["release_assets"]:
        path = workspace / record["target"]
        if not path.is_file() or path.stat().st_size != record["bytes"] or sha(path) != record["sha256"]:
            shutil.rmtree(workspace / "slots/v2", ignore_errors=True)
            shutil.rmtree(workspace / "recipes/v2", ignore_errors=True)
            restore_compatibility(workspace, rollback)
            raise ValueError(f"post-release verification failed: {record['target']}")
        actual.append({"path": record["target"], "bytes": path.stat().st_size, "sha256": sha(path), "source": record["source"], "transformation": record["transformation"]})
    tree = hashlib.sha256("".join(f"{item['path']}\0{item['sha256']}\n" for item in actual).encode()).hexdigest()
    if tree != PREVIEW_TREE:
        shutil.rmtree(workspace / "slots/v2", ignore_errors=True)
        shutil.rmtree(workspace / "recipes/v2", ignore_errors=True)
        restore_compatibility(workspace, rollback)
        raise ValueError("post-release tree mismatch")

    skill_catalog = load(workspace / "slots/v2/catalog.json"); recipe_catalog = load(workspace / "recipes/v2/catalog.json")
    manifest = {
        "schema_version": "2.0", "release_version": VERSION, "status": "released",
        "released_at": now(), "approval_path": approval_path.relative_to(workspace).as_posix(), "approval_sha256": sha(approval_path),
        "preview_path": preview_path.relative_to(workspace).as_posix(), "preview_sha256": sha(preview_path),
        "release_asset_count": len(actual), "release_asset_tree_sha256": tree, "release_assets": actual,
        "counts": stored_preview["counts"], "namespaces": stored_preview["release_namespace"],
        "source_phase_trees": stored_preview["source_phase_trees"], "v1_collision_count_avoided": len(stored_preview["v1_collisions"]),
        "source_paths_modified": [], "phase0_11_evidence_modified": [], "v1_assets_overwritten": [],
        "remote_actions": [], "commit_push_pr_merge_deploy": False,
    }
    lock = {
        "schema_version": "2.0", "release_version": VERSION, "status": "released",
        "skill_count": skill_catalog["skill_count"],
        "skills": {item["id"]: {"ref": f"{item['id']}@{VERSION}", "path": item["path"], "skill_sha256": item["skill_sha256"], "contract_sha256": item["contract_sha256"], "provenance_sha256": item["provenance_sha256"]} for item in skill_catalog["skills"]},
        "recipe_count": len(recipe_catalog["recipes"]),
        "recipes": {item["id"]: {"ref": f"{item['id']}@{VERSION}", "kind": item["kind"], "path": item["path"], "sha256": item["sha256"]} for item in recipe_catalog["recipes"]},
        "router": {"id": "capability-compiler-v2-router", "ref": f"capability-compiler-v2-router@{VERSION}", **recipe_catalog["router"]},
        "release_asset_tree_sha256": tree,
    }
    write(control / "manifest.json", manifest); write(control / "lock.json", lock)
    rollback["state"] = "released-rollback-ready"
    rollback["release_asset_tree_sha256"] = tree
    rollback["released_roots_after"] = {"slots/v2": True, "recipes/v2": True}
    rollback["compatibility_postimages"] = [{"path": item["path"], "bytes": (workspace / item["path"]).stat().st_size, "sha256": sha(workspace / item["path"])} for item in rollback["compatibility_preimages"]]
    rollback["rollback_procedure"] = ["delete slots/v2", "delete recipes/v2", "restore every compatibility_preimage content_utf8", "run all repository gates"]
    write(rollback_path, rollback)
    notes = f"""# Capability Compiler V2 1.0.0 Local Release\n\nReleased 157 atomic Skills, 15 stage Recipes, 5 composite Recipes, one specialized UI Recipe, and one fail-closed router into isolated V2 namespaces.\n\n- Release asset tree: `{tree}`\n- Phase 9 tree: `{stored_preview['source_phase_trees']['phase9']}`\n- Phase 10 tree: `{stored_preview['source_phase_trees']['phase10']}`\n- Phase 11 tree: `{stored_preview['source_phase_trees']['phase11']}`\n- V1 collisions avoided: {len(stored_preview['v1_collisions'])}\n- V1 assets overwritten: 0\n- Remote/provider/production actions: 0\n\nProtected capabilities remain disabled pending fresh exact per-action authorization. This local release does not constitute a Git commit, push, PR, merge, deployment, or production release.\n"""
    (control / "release-notes.md").write_text(notes, encoding="utf-8", newline="\n")
    result = {"gate": "capability-compiler-v2-phase-12-release", "ok": True, "release_version": VERSION, "skills": 157, "recipes": 21, "routers": 1, "release_assets": len(actual), "release_asset_tree_sha256": tree, "v1_assets_overwritten": 0, "remote_actions": [], "released": True}
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__); parser.add_argument("--workspace-root", type=Path, default=Path(".")); args = parser.parse_args()
    result = release(args.workspace_root); print(json.dumps(result, ensure_ascii=False, sort_keys=True)); return 0


if __name__ == "__main__":
    raise SystemExit(main())
