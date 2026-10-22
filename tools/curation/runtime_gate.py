#!/usr/bin/env python3
"""Verify the released full-dev-loop runtime boundary."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

try:
    from tools.curation.recipe_route import build_catalog, route_request
    from tools.curation.recipe_verify import verify_recipes
except ModuleNotFoundError:  # direct script execution
    from recipe_route import build_catalog, route_request
    from recipe_verify import verify_recipes

REQUIRED = {"write-prd", "design-web-flow", "build-feature-tdd", "qa-only", "ship-release", "retro-to-requirements", "full-dev-loop", "requirements-to-acceptance-criteria"}
DANGEROUS = {"remote-git", "network", "merge", "deploy"}


def verify(workspace: Path) -> dict[str, Any]:
    errors: list[str] = []
    recipes_root, slots_root = workspace / "recipes", workspace / "slots"
    report = verify_recipes(recipes_root, slots_root, workspace)
    errors.extend(f"recipe:{item['code']}:{item['message']}" for item in report["errors"])
    try:
        catalog = build_catalog(recipes_root, slots_root, workspace)
    except ValueError as exc:
        catalog = {}
        errors.append(str(exc))
    missing = sorted(REQUIRED - catalog.keys())
    if missing:
        errors.append(f"missing released recipes: {missing}; six-stage runtime is not released")
    else:
        route = route_request("请运行完整研发闭环", catalog)
        if route.get("recipe_ref") != "full-dev-loop@1.0.0":
            errors.append(f"natural language route mismatch: {route}")
        ambiguous = route_request("write prd and qa only", catalog)
        if ambiguous.get("status") != "needs-input":
            errors.append("ambiguous route did not need input")
    ship = catalog.get("ship-release", {})
    if DANGEROUS.intersection(ship.get("permissions", [])):
        errors.append("ship-release requests dangerous default permission")
    qa = catalog.get("qa-only", {})
    if {"write", "edit", "write-worktree"}.intersection(qa.get("permissions", [])):
        errors.append("qa-only is not report-only")
    selection_path = workspace / "curation/full-dev-loop-slot-selection.json"
    status_path = workspace / "curation/slot-release-status.json"
    if selection_path.is_file() and status_path.is_file():
        selected = set(sum(json.loads(selection_path.read_text(encoding="utf-8"))["selected"].values(), []))
        released = {item["slot_id"] for item in json.loads(status_path.read_text(encoding="utf-8"))["items"] if item["disposition"] == "released"}
        original = {"problem-framing", "requirements-rules", "acceptance-criteria", "requirements-quality-gate"}
        unexpected = released - (selected | original)
        if unexpected:
            errors.append(f"unexpected released slots: {sorted(unexpected)}")
        if not missing and released != selected | original:
            errors.append(f"released slot boundary mismatch: {sorted(released ^ (selected | original))}")
    return {"gate": "full-dev-loop-runtime", "ok": not errors, "released_recipes": len(catalog), "errors": errors}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workspace-root", type=Path, default=Path("."))
    args = parser.parse_args()
    report = verify(args.workspace_root.resolve())
    print(json.dumps(report, ensure_ascii=False, sort_keys=True))
    return 0 if report["ok"] else 1

if __name__ == "__main__":
    raise SystemExit(main())
