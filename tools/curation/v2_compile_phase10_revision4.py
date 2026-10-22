#!/usr/bin/env python3
"""Compile authorized one-change Phase 10 revision 4 from rejected revision 3."""
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
from pathlib import Path
from typing import Any

VERSION = "0.1.4-v2-candidate"
PHASE9_TREE = "7540c53426a5dff605c3f751fdaf105f52059ffbafce213d77c9c3db94214152"


def load(path: Path) -> Any: return json.loads(path.read_text(encoding="utf-8"))
def write(path: Path, value: Any) -> None: path.parent.mkdir(parents=True, exist_ok=True); path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
def sha(path: Path) -> str: return hashlib.sha256(path.read_bytes().replace(b"\r\n", b"\n")).hexdigest()


def compile_revision(workspace: Path) -> dict[str, Any]:
    workspace = workspace.resolve()
    if load(workspace / ".specs/capability-compiler-v2/phase-9/artifact-manifest.json")["tree_sha256"] != PHASE9_TREE: raise ValueError("Phase 9 tree drift")
    rejection = load(workspace / ".specs/capability-compiler-v2/phase-10/revision-3-rejection.json")
    if rejection.get("next_state") != "awaiting-explicit-authorization-for-bounded-revision-4": raise ValueError("Revision 4 checkpoint missing")
    source = workspace / "evals/candidates/capability-compiler-v2/phase-10/revision-3"; root = workspace / "evals/candidates/capability-compiler-v2/phase-10/revision-4"
    if root.exists(): shutil.rmtree(root)
    shutil.copytree(source, root)
    recipe_path = root / "phase-4/complete-ui-design-and-review.json"; before = sha(recipe_path); recipe = load(recipe_path); recipe["version"] = VERSION; recipe["evaluation_state"] = "not-run-phase-10-revision-4"
    expected_tail = {
        "no source repair is required after critique": ["review-evidence", "rendered-critique", "explicit-human-approval", "release-gate"],
        "source repair is accepted": ["review-evidence", "rendered-critique", "explicit-human-approval", "separate-remediation-capability", "review-evidence", "rendered-critique", "explicit-human-approval", "release-gate"],
    }
    for sequence in recipe["complete_route_planning"]["sequences"]:
        sequence["planned_route"] = expected_tail[sequence["condition"]]
    write(recipe_path, recipe)
    eval_path = root / "phase-4/evaluation-plan.json"; evaluation = load(eval_path); evaluation["version"] = VERSION; evaluation["candidate_sha256"] = sha(recipe_path); evaluation["execution_state"] = "not-run-phase-10-revision-4"; write(eval_path, evaluation)
    mutant_path = root / "mutations/P10-P4-complete-route-planning.json"; mutant = load(mutant_path); mutant["version"] = VERSION; mutant.pop("complete_route_planning", None); mutant["gates"] = [item for item in mutant["gates"] if "complete route planning" not in item]; write(mutant_path, mutant)
    policy_path = root / "mutation-policy.json"; policy = load(policy_path); policy["version"] = VERSION; write(policy_path, policy)
    patch_path = root / "patch-ledger.json"; patch = load(patch_path); patch["version"] = VERSION; patch["base_revision"] = "0.1.3-v2-candidate"; patch["revision4_change_count"] = 1; patch["revision4_records"] = [{"path": recipe_path.relative_to(workspace).as_posix(), "revision3_sha256": before, "revision4_sha256": sha(recipe_path), "rationale": "Prepend current review-evidence to both complete route planning sequences before rendered critique."}]; patch["revision4_authorization"] = "user confirmed revision4_authorization: yes"; write(patch_path, patch)
    return {"ok": True, "version": VERSION, "changes": 1, "atomic_skill_revisions": 0, "recipe_sha256": sha(recipe_path)}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__); parser.add_argument("--workspace-root", type=Path, default=Path(".")); args = parser.parse_args(); print(json.dumps(compile_revision(args.workspace_root), ensure_ascii=False, sort_keys=True)); return 0


if __name__ == "__main__": raise SystemExit(main())
