"""Verify recipe structure, slot references, and composition constraints."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
from typing import Any

from jsonschema import Draft202012Validator


def load_slots(slots_root: Path) -> tuple[dict[str, dict[str, Any]], list[dict[str, str]]]:
    """Load slot contracts and reject duplicate or invalid identities."""
    slots: dict[str, dict[str, Any]] = {}
    errors: list[dict[str, str]] = []
    schema_path = slots_root / "schema.json"
    validator = Draft202012Validator(json.loads(schema_path.read_text(encoding="utf-8")))
    for slot_dir in sorted(slots_root.iterdir()):
        if not slot_dir.is_dir():
            continue
        contract_path = slot_dir / "contract.json"
        if not contract_path.exists():
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


def _safe_relative(value: object) -> bool:
    if not isinstance(value, str) or not value:
        return False
    path = PurePosixPath(value.replace("\\", "/"))
    return not path.is_absolute() and ".." not in path.parts


def _validate_evidence_file(path: Path, *, expected_recipe: str | None = None) -> str | None:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return f"invalid evidence {path.as_posix()}: {exc}"
    if data.get("passed") is not True and data.get("verdict") not in {"approved", "approved-for-release"}:
        return f"evidence is not passing: {path.as_posix()}"
    if expected_recipe is not None and data.get("recipe_id") not in {None, expected_recipe}:
        return f"evidence recipe mismatch: {path.as_posix()}"
    return None


def find_cycles(steps: list[dict], edges: list[dict]) -> bool:
    """Return True if dependency graph has a cycle."""
    graph = {step["id"]: set() for step in steps}
    for edge in edges:
        graph[edge["from"]].add(edge["to"])

    def has_cycle_from(node: str, visited: set, rec_stack: set) -> bool:
        visited.add(node)
        rec_stack.add(node)
        for neighbor in graph.get(node, []):
            if neighbor not in visited:
                if has_cycle_from(neighbor, visited, rec_stack):
                    return True
            elif neighbor in rec_stack:
                return True
        rec_stack.remove(node)
        return False

    visited = set()
    for node in graph:
        if node not in visited:
            if has_cycle_from(node, visited, set()):
                return True
    return False


def verify_recipe(recipe: dict, slots: dict[str, dict], recipe_path: Path, workspace_root: Path) -> list[dict]:
    """Verify a single recipe and return errors."""
    errors = []

    # Check required fields
    for field in ["id", "version", "status", "steps", "inputs", "outputs", "edges", "gates"]:
        if field not in recipe:
            errors.append({"code": "schema", "message": f"missing field: {field}"})

    if errors:
        return errors

    # Check status
    if recipe["status"] != "released":
        errors.append({"code": "unreleased-recipe", "message": f"recipe status: {recipe['status']}"})

    schema_path = recipe_path.parent / "schema.json"
    try:
        validator = Draft202012Validator(json.loads(schema_path.read_text(encoding="utf-8")))
        schema_errors = sorted(validator.iter_errors(recipe), key=lambda item: list(item.absolute_path))
    except (OSError, json.JSONDecodeError) as exc:
        errors.append({"code": "schema", "message": f"cannot load recipe schema: {exc}"})
        return errors
    for error in schema_errors:
        errors.append({"code": "schema", "message": error.message})
    if schema_errors:
        return errors

    # Check steps
    step_ids = {step["id"] for step in recipe["steps"]}
    if len(step_ids) != len(recipe["steps"]):
        errors.append({"code": "duplicate-step-id", "message": "step ids must be unique"})
    artifacts = {}  # artifact -> (step_id, parallel_writes)

    # Map inputs to recipe inputs
    for inp in recipe["inputs"]:
        artifacts[inp] = (None, [])

    for step in recipe["steps"]:
        step_id = step["id"]
        slot_id = step.get("slot")
        ref = step.get("ref")

        # Check slot exists and is released
        if slot_id not in slots:
            errors.append({"code": "missing-slot", "message": f"step {step_id}: slot {slot_id} not found"})
            continue

        slot = slots[slot_id]
        if slot.get("status") != "released":
            errors.append({"code": "unreleased-slot", "message": f"step {step_id}: slot {slot_id} status {slot.get('status')}"})

        # Check exact slot identity and version.
        expected_ref = f"{slot_id}@{slot.get('version')}"
        if ref != expected_ref:
            errors.append({"code": "slot-version-mismatch", "message": f"step {step_id}: ref {ref} != {expected_ref}"})

        # Recipe maps stable machine keys declared by the slot contract.
        slot_inputs = set(slot.get("inputs", []))
        slot_outputs = set(slot.get("outputs", []))

        for logical_input in step.get("input_map", {}):
            if logical_input not in slot_inputs:
                errors.append({"code": "unknown-slot-input", "message": f"step {step_id}: input key {logical_input} not in slot {slot_id}"})

        for logical_output in step.get("output_map", {}):
            if logical_output not in slot_outputs:
                errors.append({"code": "unknown-slot-output", "message": f"step {step_id}: output key {logical_output} not in slot {slot_id}"})

        # Check gates are defined in slot
        slot_gates = set(slot.get("gates", []))
        for gate in step.get("gates", []):
            if gate not in slot_gates:
                errors.append({"code": "unknown-gate", "message": f"step {step_id}: gate {gate} not in slot {slot_id}"})

        # Check permission escalation
        permissions = slot.get("permissions", {})
        defaults = permissions.get("default", []) if isinstance(permissions, dict) else []
        slot_permissions = set(defaults if isinstance(defaults, list) else [])
        for perm in step.get("permissions", []):
            if perm not in slot_permissions:
                errors.append({"code": "permission-escalation", "message": f"step {step_id}: permission {perm} not in slot {slot_id}"})

        # Check for inline instructions (schema violation)
        if "instructions" in step:
            errors.append({"code": "schema", "message": f"step {step_id}: inline instructions forbidden"})

        # Track artifact producers
        for artifact in step.get("output_map", {}).values():
            if artifact not in artifacts:
                artifacts[artifact] = (step_id, [step_id])
            else:
                artifacts[artifact][1].append(step_id)

    # Check for parallel writes
    for artifact, (_, writers) in artifacts.items():
        if len(writers) > 1:
            # Check if these steps have dependencies that serialize them
            serialized = False
            for i, w1 in enumerate(writers):
                for w2 in writers[i+1:]:
                    # Check if w1 depends on w2 or vice versa via edges
                    if any(e["from"] == w1 and e["to"] == w2 or e["from"] == w2 and e["to"] == w1 for e in recipe["edges"]):
                        serialized = True
                        break
            if not serialized:
                errors.append({"code": "parallel-artifact-write", "message": f"artifact {artifact} written by parallel steps {writers}"})

    # Check input producers
    for step in recipe["steps"]:
        for artifact in step.get("input_map", {}).values():
            if artifact not in artifacts:
                errors.append({"code": "input-without-producer", "message": f"step {step['id']}: input {artifact} has no producer"})

    # Check recipe outputs have producers
    for output in recipe["outputs"]:
        if output not in artifacts:
            errors.append({"code": "output-without-producer", "message": f"recipe output {output} has no producer"})

    # Check for cycles (before evidence check)
    # Build complete edge set from both edges array and depends_on
    all_edges = list(recipe["edges"])
    for step in recipe["steps"]:
        for dep in step.get("depends_on", []):
            all_edges.append({"from": dep, "to": step["id"]})

    if find_cycles(recipe["steps"], all_edges):
        errors.append({"code": "step-cycle", "message": "dependency cycle detected"})

    # Check failure route endpoints after schema validation.
    for route in recipe.get("failure_routes", []):
        if route["from"] not in step_ids or route["to"] not in step_ids:
            errors.append({"code": "invalid-failure-route", "message": f"unknown route endpoint: {route}"})

    # Check evidence for released recipes.
    if recipe["status"] == "released" and "evidence" in recipe:
        evidence = recipe["evidence"]
        composition_runs = evidence.get("composition_runs", [])
        review_path = evidence.get("review")

        evidence_errors = []
        for run in composition_runs:
            run_path = run["path"]
            if not _safe_relative(run_path):
                evidence_errors.append(f"unsafe evidence path: {run_path}")
                continue
            result_file = workspace_root / run_path
            if not result_file.is_file():
                evidence_errors.append(f"missing: {result_file.as_posix()}")
            elif hashlib.sha256(result_file.read_bytes()).hexdigest() != run["sha256"]:
                evidence_errors.append(f"evidence hash mismatch: {run_path}")
            else:
                problem = _validate_evidence_file(result_file, expected_recipe=recipe["id"])
                if problem:
                    evidence_errors.append(problem)

        review_path = review_path["path"]
        if not _safe_relative(review_path):
            evidence_errors.append(f"unsafe review path: {review_path}")
        else:
            full_review = workspace_root / review_path
            if not full_review.is_file():
                evidence_errors.append(f"missing: {full_review.as_posix()}")
            elif hashlib.sha256(full_review.read_bytes()).hexdigest() != evidence["review"]["sha256"]:
                evidence_errors.append(f"review hash mismatch: {review_path}")
            else:
                problem = _validate_evidence_file(full_review)
                if problem:
                    evidence_errors.append(problem)

        if evidence_errors:
            errors.append({"code": "missing-release-evidence", "message": "; ".join(evidence_errors)})

    return errors


def verify_recipes(recipes_root: Path, slots_root: Path, workspace_root: Path, recipe_file: Path | None = None) -> dict:
    """Verify all recipes or a single recipe."""
    try:
        slots, slot_errors = load_slots(slots_root)
    except (OSError, json.JSONDecodeError) as exc:
        slots, slot_errors = {}, [{"code": "invalid-slot-contract", "message": str(exc)}]

    if recipe_file:
        recipes = [recipe_file]
    else:
        recipes = sorted(recipes_root.glob("*.json"))
        recipes = [r for r in recipes if r.stem not in ("schema",)]

    if not recipes:
        return {
            "ok": False,
            "checked": [],
            "errors": [{"code": "missing-recipe", "message": "no recipes found"}]
        }

    all_errors = list(slot_errors)
    for recipe_path in recipes:
        try:
            recipe = json.loads(recipe_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            all_errors.append({"code": "parse-error", "message": f"{recipe_path.name}: {exc}"})
            continue

        errors = verify_recipe(recipe, slots, recipe_path, workspace_root)
        all_errors.extend(errors)

    return {
        "ok": not all_errors,
        "checked": [str(r) for r in recipes],
        "errors": all_errors
    }


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
