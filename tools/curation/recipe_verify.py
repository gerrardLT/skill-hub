"""Verify released recipes, exact slot/sub-recipe references, and runtime safety."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
from typing import Any

from jsonschema import Draft202012Validator

FAILURE_STATUSES = {"needs-input", "failed", "blocked"}
DANGEROUS_PERMISSIONS = {
    "write-worktree": "workspace-write",
    "remote-git": "remote-git",
    "network": "network",
    "merge": "merge",
    "deploy": "deploy",
}


def load_slots(slots_root: Path) -> tuple[dict[str, dict[str, Any]], list[dict[str, str]]]:
    slots: dict[str, dict[str, Any]] = {}
    errors: list[dict[str, str]] = []
    validator = Draft202012Validator(json.loads((slots_root / "schema.json").read_text(encoding="utf-8")))
    for slot_dir in sorted(slots_root.iterdir()):
        contract_path = slot_dir / "contract.json"
        if not slot_dir.is_dir() or not contract_path.exists():
            continue
        try:
            contract = json.loads(contract_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            errors.append({"code": "invalid-slot-contract", "message": f"{slot_dir.name}: {exc}"})
            continue
        schema_errors = sorted(validator.iter_errors(contract), key=lambda item: list(item.absolute_path))
        if schema_errors:
            errors.append({"code": "invalid-slot-contract", "message": f"{slot_dir.name}: {schema_errors[0].message}"})
            continue
        slot_id = contract["id"]
        if slot_id != slot_dir.name:
            errors.append({"code": "slot-id-mismatch", "message": f"{slot_dir.name}: contract id {slot_id}"})
        elif slot_id in slots:
            errors.append({"code": "duplicate-slot-id", "message": f"duplicate slot id: {slot_id}"})
        else:
            slots[slot_id] = contract
    return slots, errors


def load_recipes(paths: list[Path]) -> tuple[dict[str, dict[str, Any]], list[dict[str, str]]]:
    recipes: dict[str, dict[str, Any]] = {}
    errors: list[dict[str, str]] = []
    for path in paths:
        try:
            recipe = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            errors.append({"code": "parse-error", "message": f"{path.name}: {exc}"})
            continue
        recipe_id = recipe.get("id")
        if not isinstance(recipe_id, str):
            errors.append({"code": "schema", "message": f"{path.name}: missing recipe id"})
        elif recipe_id in recipes:
            errors.append({"code": "duplicate-recipe-id", "message": f"duplicate recipe id: {recipe_id}"})
        else:
            recipes[recipe_id] = recipe
    return recipes, errors


def _safe_relative(value: object) -> bool:
    if not isinstance(value, str) or not value:
        return False
    path = PurePosixPath(value.replace("\\", "/"))
    return not path.is_absolute() and ".." not in path.parts


def _execution_record_problem(step: dict, workspace: Path) -> str | None:
    execution = step.get("execution")
    if not isinstance(execution, dict):
        return "missing execution record"
    if not isinstance(step.get("duration_ms"), (int, float)) or step["duration_ms"] < 0:
        return "missing duration"
    output_file = step.get("output_file")
    if not isinstance(output_file, str) or not output_file:
        return "missing output file"
    output_path = Path(output_file)
    if not output_path.is_absolute():
        output_path = workspace / output_path
    if not output_path.is_file():
        return "missing output artifact"
    if hashlib.sha256(output_path.read_bytes()).hexdigest() != step.get("output_sha256"):
        return "output hash mismatch"
    if execution.get("adapter") == "workspace":
        if not isinstance(execution.get("tool_events"), list) or not isinstance(execution.get("command_results"), list):
            return "missing workspace tool or command evidence"
        if not isinstance(execution.get("patch_file"), str) or not isinstance(execution.get("patch_sha256"), str):
            return "missing workspace patch evidence"
        patch = Path(execution["patch_file"])
        if not patch.is_absolute():
            patch = workspace / patch
        if not patch.is_file() or hashlib.sha256(patch.read_bytes()).hexdigest() != execution["patch_sha256"]:
            return "workspace patch hash mismatch"
    return None


def _validate_evidence_file(path: Path, *, expected_recipe: str | None = None, executed: bool = False, workspace: Path | None = None) -> str | None:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return f"invalid evidence {path.as_posix()}: {exc}"
    if data.get("passed") is not True and data.get("verdict") not in {"approved", "approved-for-release"}:
        return f"evidence is not passing: {path.as_posix()}"
    if expected_recipe is not None and data.get("recipe_id") not in {None, expected_recipe}:
        return f"evidence recipe mismatch: {path.as_posix()}"
    if executed:
        steps = data.get("steps_run")
        if not isinstance(steps, list) or not steps:
            return f"release evidence has no executed steps: {path.as_posix()}"
        for step in steps:
            if not isinstance(step, dict) or step.get("status") != "passed":
                return f"release evidence contains a non-passing step: {path.as_posix()}"
            problem = _execution_record_problem(step, workspace or path.parent)
            if problem:
                return f"release evidence {problem}: {path.as_posix()}"
    return None


def _validate_slot_run(path: Path, slot_id: str, workspace: Path) -> str | None:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return f"invalid slot evaluation {path.as_posix()}: {exc}"
    if data.get("slot_id") != slot_id or data.get("passed") is not True:
        return f"slot evaluation is not passing or mismatched: {path.as_posix()}"
    cases = data.get("cases")
    if not isinstance(cases, list) or not cases:
        return f"slot evaluation lacks executed cases: {path.as_posix()}"
    for case in cases:
        if not isinstance(case, dict) or case.get("slot_id") != slot_id or case.get("passed") is not True:
            return f"slot evaluation case failed or mismatched: {path.as_posix()}"
        if not all(isinstance(case.get(key), str) and case[key] for key in ("input_sha256", "output_sha256", "run_path")):
            return f"slot evaluation case lacks output and run provenance: {path.as_posix()}"
        if not _safe_relative(case["run_path"]):
            return f"unsafe slot run path: {case['run_path']}"
        run_path = workspace / case["run_path"]
        try:
            run = json.loads(run_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            return f"invalid slot run {run_path.as_posix()}: {exc}"
        if run.get("slot_id") != slot_id or run.get("case_id") != case.get("case_id"):
            return f"slot run identity mismatch: {run_path.as_posix()}"
        if not isinstance(run.get("duration_ms"), (int, float)) or run["duration_ms"] < 0:
            return f"slot run duration missing: {run_path.as_posix()}"
        if not isinstance(run.get("tool_events"), list) or not isinstance(run.get("command_results"), list):
            return f"slot run execution evidence missing: {run_path.as_posix()}"
        output = run.get("output_file")
        if not isinstance(output, str) or not _safe_relative(output):
            return f"slot run output path invalid: {run_path.as_posix()}"
        output_path = workspace / output
        if not output_path.is_file() or hashlib.sha256(output_path.read_bytes()).hexdigest() != case["output_sha256"]:
            return f"slot run output hash mismatch: {run_path.as_posix()}"
    return None


def verify_slot_release_evidence(slot_id: str, contract: dict, workspace: Path) -> list[str]:
    if contract.get("status") != "released" or contract.get("version") == "0.2.0":
        return []
    if not (workspace / "slots" / slot_id / "provenance.json").is_file():
        return [f"missing slot provenance: {slot_id}"] if (workspace / "curation/full-dev-loop-slot-selection.json").is_file() else []
    try:
        provenance = json.loads((workspace / "slots" / slot_id / "provenance.json").read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return [f"invalid slot provenance: {slot_id}: {exc}"]
    errors = []
    paths = provenance.get("release_evidence", [])
    for kind in ("baseline", "candidate", "holdout", "mutation"):
        candidates = [value for value in paths if isinstance(value, str) and value.endswith(f"/{kind}.json")]
        if len(candidates) != 1 or not _safe_relative(candidates[0]):
            errors.append(f"missing {kind} release evaluation: {slot_id}")
            continue
        problem = _validate_slot_run(workspace / candidates[0], slot_id, workspace)
        if problem:
            errors.append(problem)
    return errors


def find_cycles(steps: list[dict], edges: list[dict]) -> bool:
    graph = {step["id"]: set() for step in steps}
    for edge in edges:
        if edge.get("from") in graph and edge.get("to") in graph:
            graph[edge["from"]].add(edge["to"])

    def visit(node: str, seen: set[str], active: set[str]) -> bool:
        seen.add(node)
        active.add(node)
        for neighbor in graph[node]:
            if neighbor not in seen and visit(neighbor, seen, active):
                return True
            if neighbor in active:
                return True
        active.remove(node)
        return False

    seen: set[str] = set()
    return any(node not in seen and visit(node, seen, set()) for node in graph)


def _recipe_cycles(recipes: dict[str, dict[str, Any]]) -> list[str]:
    graph = {
        recipe_id: {
            step["recipe"].rsplit("@", 1)[0]
            for step in recipe.get("steps", [])
            if isinstance(step, dict) and isinstance(step.get("recipe"), str)
        }
        for recipe_id, recipe in recipes.items()
    }
    cycles: set[str] = set()

    def visit(node: str, trail: tuple[str, ...]) -> None:
        if node in trail:
            cycles.add(" -> ".join(trail[trail.index(node):] + (node,)))
            return
        for child in graph.get(node, set()):
            visit(child, trail + (node,))

    for recipe_id in graph:
        visit(recipe_id, ())
    return sorted(cycles)


def _permissions(contract: dict[str, Any]) -> set[str]:
    value = contract.get("permissions", {})
    if isinstance(value, dict):
        value = value.get("default", [])
    return set(value if isinstance(value, list) else [])


def verify_recipe(
    recipe: dict,
    slots: dict[str, dict],
    recipe_path: Path,
    workspace_root: Path,
    recipes: dict[str, dict[str, Any]] | None = None,
    *,
    allow_evaluating: bool = False,
) -> list[dict]:
    errors: list[dict[str, str]] = []
    recipes = recipes or {recipe.get("id"): recipe}
    required = ["id", "version", "status", "steps", "inputs", "outputs", "edges", "gates"]
    for field in required:
        if field not in recipe:
            errors.append({"code": "schema", "message": f"missing field: {field}"})
    if errors:
        return errors
    if recipe["status"] != "released" and not (allow_evaluating and recipe["status"] == "evaluating"):
        errors.append({"code": "unreleased-recipe", "message": f"recipe status: {recipe['status']}"})

    try:
        schema_path = recipe_path.parent / "schema.json"
        if not schema_path.is_file():
            schema_path = workspace_root / "recipes/schema.json"
        validator = Draft202012Validator(json.loads(schema_path.read_text(encoding="utf-8")))
        schema_errors = sorted(validator.iter_errors(recipe), key=lambda item: list(item.absolute_path))
    except (OSError, json.JSONDecodeError) as exc:
        return errors + [{"code": "schema", "message": f"cannot load recipe schema: {exc}"}]
    errors.extend({"code": "schema", "message": error.message} for error in schema_errors)
    if schema_errors:
        return errors

    steps = recipe["steps"]
    step_by_id = {step["id"]: step for step in steps}
    if len(step_by_id) != len(steps):
        errors.append({"code": "duplicate-step-id", "message": "step ids must be unique"})
    recipe_permissions = set(recipe["permissions"])
    artifacts: dict[str, list[str]] = {item: [] for item in recipe["inputs"]}
    logical_inputs: dict[str, set[str]] = {}

    for step in steps:
        step_id = step["id"]
        step_permissions = set(step["permissions"])
        if not step_permissions <= recipe_permissions:
            errors.append({"code": "permission-escalation", "message": f"step {step_id}: permissions exceed recipe"})

        target: dict[str, Any] | None = None
        target_name = ""
        if "recipe" in step:
            child_id, child_version = step["recipe"].rsplit("@", 1)
            target = recipes.get(child_id)
            target_name = f"recipe {child_id}"
            if target is None:
                errors.append({"code": "missing-recipe", "message": f"step {step_id}: recipe {child_id} not found"})
            elif target.get("version") != child_version:
                errors.append({"code": "recipe-version-mismatch", "message": f"step {step_id}: {step['recipe']} != {child_id}@{target.get('version')}"})
            elif target.get("status") != "released" and not (allow_evaluating and target.get("status") == "evaluating"):
                errors.append({"code": "unreleased-recipe", "message": f"step {step_id}: recipe {child_id} is not released"})
            target_permissions = set(target.get("permissions", [])) if target else set()
        else:
            slot_id = step["slot"]
            target = slots.get(slot_id)
            target_name = f"slot {slot_id}"
            if target is None:
                errors.append({"code": "missing-slot", "message": f"step {step_id}: slot {slot_id} not found"})
                target_permissions = set()
            else:
                if target.get("status") != "released" and not (allow_evaluating and target.get("status") == "evaluating"):
                    errors.append({"code": "unreleased-slot", "message": f"step {step_id}: slot {slot_id} status {target.get('status')}"})
                elif target.get("status") == "released":
                    errors.extend({"code": "missing-release-evidence", "message": problem} for problem in verify_slot_release_evidence(slot_id, target, workspace_root))
                expected_ref = f"{slot_id}@{target.get('version')}"
                if step["ref"] != expected_ref:
                    errors.append({"code": "slot-version-mismatch", "message": f"step {step_id}: ref {step['ref']} != {expected_ref}"})
                target_permissions = _permissions(target)
                adapter = step.get("execution_adapter")
                execution = target.get("execution")
                if adapter and (not isinstance(execution, dict) or execution.get("adapter") != adapter):
                    errors.append({"code": "execution-adapter-mismatch", "message": f"step {step_id}: adapter not allowed by {target_name}"})

        if target is not None:
            target_inputs = set(target.get("inputs", []))
            target_outputs = set(target.get("outputs", []))
            logical_inputs[step_id] = target_inputs
            for key in step["input_map"]:
                if key not in target_inputs:
                    errors.append({"code": "unknown-slot-input" if "slot" in step else "unknown-recipe-input", "message": f"step {step_id}: input key {key} not in {target_name}"})
            for key in step["output_map"]:
                if key not in target_outputs:
                    errors.append({"code": "unknown-slot-output" if "slot" in step else "unknown-recipe-output", "message": f"step {step_id}: output key {key} not in {target_name}"})
            for gate in step["gates"]:
                if gate not in set(target.get("gates", [])):
                    errors.append({"code": "unknown-gate", "message": f"step {step_id}: gate {gate} not in {target_name}"})
            if not step_permissions <= target_permissions:
                errors.append({"code": "permission-escalation", "message": f"step {step_id}: permissions exceed {target_name}"})
            if "slot" in step and isinstance(target.get("execution"), dict):
                authorization = target["execution"]["authorization"]
                scopes = set(authorization["scopes"])
                for permission in step_permissions & DANGEROUS_PERMISSIONS.keys():
                    if not authorization["required"] or DANGEROUS_PERMISSIONS[permission] not in scopes:
                        errors.append({"code": "missing-explicit-authorization", "message": f"step {step_id}: {permission} is not authorization-gated"})

        for artifact in set(step["output_map"].values()):
            artifacts.setdefault(artifact, []).append(step_id)

    for step in steps:
        for dependency in step.get("depends_on", []):
            if dependency not in step_by_id:
                errors.append({"code": "unknown-dependency", "message": f"step {step['id']}: dependency {dependency} not found"})
        for artifact in step["input_map"].values():
            if artifact not in artifacts:
                errors.append({"code": "input-without-producer", "message": f"step {step['id']}: input {artifact} has no producer"})
    for output in recipe["outputs"]:
        if output not in artifacts:
            errors.append({"code": "output-without-producer", "message": f"recipe output {output} has no producer"})
    for artifact, writers in artifacts.items():
        if len(writers) > 1 and not any(
            a in step_by_id[b].get("depends_on", []) or b in step_by_id[a].get("depends_on", [])
            for index, a in enumerate(writers) for b in writers[index + 1:]
        ):
            errors.append({"code": "parallel-artifact-write", "message": f"artifact {artifact} written by parallel steps {writers}"})

    all_edges = list(recipe["edges"])
    all_edges.extend({"from": dep, "to": step["id"]} for step in steps for dep in step.get("depends_on", []))
    if find_cycles(steps, all_edges):
        errors.append({"code": "step-cycle", "message": "dependency cycle detected"})

    routed: dict[tuple[str, str], int] = {}
    for route in recipe.get("failure_routes", []):
        if route["from"] not in step_by_id or route["to"] not in step_by_id:
            errors.append({"code": "invalid-failure-route", "message": f"unknown route endpoint: {route}"})
        for status in route["on_status"]:
            key = (route["from"], status)
            routed[key] = routed.get(key, 0) + 1
    if recipe.get("retry_policy"):
        for step_id in step_by_id:
            for status in FAILURE_STATUSES:
                count = routed.get((step_id, status), 0)
                if count == 0:
                    errors.append({"code": "missing-failure-route", "message": f"step {step_id}: no route for {status}"})
                elif count > 1:
                    errors.append({"code": "conflicting-failure-route", "message": f"step {step_id}: multiple routes for {status}"})

    for mapping in recipe.get("feedback_mappings", []):
        source, target = mapping["from_step"], mapping["to_step"]
        if source not in step_by_id or target not in step_by_id:
            errors.append({"code": "invalid-feedback-mapping", "message": f"unknown feedback endpoint: {mapping}"})
        elif mapping["artifact"] not in step_by_id[source]["output_map"].values():
            errors.append({"code": "invalid-feedback-mapping", "message": f"step {source} does not produce {mapping['artifact']}"})
        elif mapping.get("target_input") and mapping["target_input"] not in logical_inputs.get(target, set()):
            target_step = step_by_id[target]
            target_contract = slots.get(target_step.get("slot"), {})
            correction_inputs = target_contract.get("execution", {}).get("correction_inputs", []) if isinstance(target_contract, dict) else []
            if mapping["target_input"] not in correction_inputs:
                errors.append({"code": "invalid-feedback-mapping", "message": f"step {target} has no input {mapping['target_input']}"})

    evidence = recipe.get("evidence")
    if recipe["status"] == "released" and isinstance(evidence, dict):
        evidence_errors: list[str] = []
        for run in evidence.get("composition_runs", []):
            relative = run["path"]
            full = workspace_root / relative if _safe_relative(relative) else None
            if full is None:
                evidence_errors.append(f"unsafe evidence path: {relative}")
            elif not full.is_file():
                evidence_errors.append(f"missing: {full.as_posix()}")
            elif hashlib.sha256(full.read_bytes()).hexdigest() != run["sha256"]:
                evidence_errors.append(f"evidence hash mismatch: {relative}")
            else:
                problem = _validate_evidence_file(full, expected_recipe=recipe["id"], executed=recipe["version"] != "0.2.0", workspace=workspace_root)
                if problem:
                    evidence_errors.append(problem)
        review = evidence.get("review", {})
        relative = review.get("path")
        full = workspace_root / relative if _safe_relative(relative) else None
        if full is None:
            evidence_errors.append(f"unsafe review path: {relative}")
        elif not full.is_file():
            evidence_errors.append(f"missing: {full.as_posix()}")
        elif hashlib.sha256(full.read_bytes()).hexdigest() != review.get("sha256"):
            evidence_errors.append(f"review hash mismatch: {relative}")
        else:
            problem = _validate_evidence_file(full)
            if problem:
                evidence_errors.append(problem)
        if evidence_errors:
            errors.append({"code": "missing-release-evidence", "message": "; ".join(evidence_errors)})
    return errors


def verify_recipes(recipes_root: Path, slots_root: Path, workspace_root: Path, recipe_file: Path | None = None, *, allow_evaluating: bool = False) -> dict:
    try:
        slots, errors = load_slots(slots_root)
    except (OSError, json.JSONDecodeError) as exc:
        slots, errors = {}, [{"code": "invalid-slot-contract", "message": str(exc)}]
    paths = [recipe_file] if recipe_file else [p for p in sorted(recipes_root.glob("*.json")) if p.stem not in {"schema", "catalog"}]
    if not paths:
        return {"ok": False, "checked": [], "errors": [{"code": "missing-recipe", "message": "no recipes found"}]}
    catalog_paths = [p for p in sorted(recipes_root.glob("*.json")) if p.stem not in {"schema", "catalog"}]
    released_root = workspace_root / "recipes"
    if released_root.resolve() != recipes_root.resolve():
        catalog_paths += [p for p in sorted(released_root.glob("*.json")) if p.stem not in {"schema", "catalog"}]
    recipes, recipe_errors = load_recipes(catalog_paths)
    errors.extend(recipe_errors)
    cycles = _recipe_cycles(recipes)
    errors.extend({"code": "recipe-cycle", "message": cycle} for cycle in cycles)
    for path in paths:
        try:
            recipe = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        errors.extend(verify_recipe(recipe, slots, path, workspace_root, recipes, allow_evaluating=allow_evaluating))

    phrases: dict[str, str] = {}
    for recipe_id, recipe in recipes.items():
        for phrase in recipe.get("routing", {}).get("intents", []):
            folded = phrase.casefold().strip()
            if folded in phrases and phrases[folded] != recipe_id:
                errors.append({"code": "routing-conflict", "message": f"{phrase}: {phrases[folded]} and {recipe_id}"})
            phrases[folded] = recipe_id
    return {"ok": not errors, "checked": [str(path) for path in paths], "errors": errors}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--recipes-root", type=Path, required=True)
    parser.add_argument("--slots-root", type=Path, required=True)
    parser.add_argument("--recipe", type=Path)
    parser.add_argument("--workspace-root", type=Path, default=Path("."))
    args = parser.parse_args()
    result = verify_recipes(args.recipes_root, args.slots_root, args.workspace_root, args.recipe)
    print(json.dumps(result, indent=2))
    return 0 if result["ok"] else 1

if __name__ == "__main__":
    raise SystemExit(main())
