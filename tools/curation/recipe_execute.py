"""Execute verified recipes with durable state, evidence reuse, and failure routing."""
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
import tempfile
import time
from pathlib import Path, PurePosixPath
from typing import Callable

from tools.curation.execution_adapters import ExecutionPolicy, artifact_adapter, workspace_adapter
from tools.curation.recipe_verify import verify_recipes
from tools.curation.slot_gate import evaluate_gates
from tools.curation.workflow_state import StateError, load_state, new_state, save_state

VALID_STATUSES = {"passed", "needs-input", "blocked", "failed"}


def _safe_id(value: object) -> bool:
    return isinstance(value, str) and value and PurePosixPath(value).name == value and value not in {".", ".."}


def _topological_steps(recipe: dict) -> list[dict]:
    steps = {step["id"]: step for step in recipe["steps"]}
    dependencies = {step_id: set(step.get("depends_on", [])) for step_id, step in steps.items()}
    order: list[dict] = []
    ready = sorted(step_id for step_id, deps in dependencies.items() if not deps)
    while ready:
        step_id = ready.pop(0)
        order.append(steps[step_id])
        for other, deps in dependencies.items():
            if step_id in deps:
                deps.remove(step_id)
                if not deps and steps[other] not in order and other not in ready:
                    ready.append(other)
                    ready.sort()
    if len(order) != len(steps):
        raise ValueError("recipe dependency graph contains a cycle")
    return order


def _status(text: str) -> str | None:
    for line in text.splitlines():
        if line.startswith("Status:"):
            value = line.split(":", 1)[1].strip()
            return value if value in VALID_STATUSES else None
    return None


def _pi_worker(prompt: str, timeout: int) -> str:
    executable = shutil.which("pi") or shutil.which("pi.cmd")
    if not executable:
        raise RuntimeError("pi-unavailable")
    with tempfile.NamedTemporaryFile("w", suffix=".md", encoding="utf-8", delete=False) as handle:
        handle.write(prompt)
        prompt_path = Path(handle.name)
    try:
        process = subprocess.run(
            [
                executable, "-p", "--mode", "json", "--no-tools", "--no-skills",
                "--no-extensions", "--no-context-files", "--no-session",
                "--system-prompt", "Follow the slot contract exactly. Return the complete artifact.",
                f"@{prompt_path}",
            ],
            capture_output=True,
            check=False,
            timeout=timeout,
        )
    except subprocess.TimeoutExpired as exc:
        raise RuntimeError(f"execution-timeout-after-{timeout}s") from exc
    finally:
        prompt_path.unlink(missing_ok=True)
    if process.returncode:
        raise RuntimeError(process.stderr.decode("utf-8", errors="replace").strip() or f"pi-exit-{process.returncode}")
    try:
        events = [json.loads(line) for line in process.stdout.decode("utf-8", errors="replace").splitlines() if line.strip()]
    except json.JSONDecodeError as exc:
        raise RuntimeError("invalid-pi-output") from exc
    ends = [event for event in events if event.get("type") == "message_end" and event.get("message", {}).get("role") == "assistant"]
    if not ends:
        raise RuntimeError("no-output")
    return "".join(part.get("text", "") for part in ends[-1]["message"].get("content", []) if part.get("type") == "text")


def _failure_route(recipe: dict, step_id: str, status: str) -> dict | None:
    matches = [route for route in recipe.get("failure_routes", []) if route["from"] == step_id and status in route["on_status"]]
    return matches[0] if len(matches) == 1 else None


def _affected_steps(recipe: dict, target: str) -> set[str]:
    affected = {target}
    changed = True
    while changed:
        changed = False
        for step in recipe["steps"]:
            if step["id"] not in affected and affected.intersection(step.get("depends_on", [])):
                affected.add(step["id"])
                changed = True
    return affected


def _state_step(item: dict[str, object]) -> dict[str, object]:
    evidence = [item["output_file"]] if item.get("output_file") else []
    return {
        "step_id": item["step_id"],
        "ref": item["slot_ref"],
        "status": item["status"],
        "input_sha256": item["input_sha256"],
        "artifacts": [item["output_file"]] if item.get("output_file") else [],
        "evidence": evidence,
        "attempts": item.get("attempt", 1),
    }


def _persist_workflow(state_dir: Path | None, state: dict | None, steps_run: list[dict], status: str, next_action: str) -> None:
    if state_dir is None or state is None:
        return
    state["steps"] = [_state_step(item) for item in steps_run]
    state["status"] = status
    state["next_action"] = next_action
    save_state(state_dir, state)


def _artifact_for_recipe_output(child_recipe: dict, child_result: dict, artifact: str, workspace: Path) -> str:
    producers = [step["id"] for step in child_recipe["steps"] if artifact in step["output_map"].values()]
    if not producers:
        raise RuntimeError(f"child-output-without-producer:{artifact}")
    records = {item["step_id"]: item for item in child_result.get("steps_run", [])}
    record = records.get(producers[-1])
    if not record or not record.get("output_file"):
        raise RuntimeError(f"child-output-missing:{artifact}")
    path = Path(record["output_file"])
    if not path.is_absolute():
        path = workspace / path
    return path.read_text(encoding="utf-8")


def execute_recipe(
    recipe_path: Path,
    input_file: Path,
    output_dir: Path,
    *,
    workspace_root: Path | None = None,
    timeout: int = 300,
    worker: Callable[[str, int], str] = _pi_worker,
    require_release_evidence: bool = True,
    state_dir: Path | None = None,
    authorization: set[str] | None = None,
    repository: Path | None = None,
    workspace_runner: Callable | None = None,
) -> dict[str, object]:
    workspace = (workspace_root or Path.cwd()).resolve()
    recipe_path = recipe_path.resolve()
    slots_root = workspace / "slots"
    verification = verify_recipes(recipe_path.parent, slots_root, workspace, recipe_path)
    if require_release_evidence and not verification["ok"]:
        return {"recipe_id": None, "passed": False, "status": "blocked", "steps_run": [], "errors": [f"recipe-verification: {error['code']}" for error in verification["errors"]]}

    recipe = json.loads(recipe_path.read_text(encoding="utf-8"))
    recipe_ref = f"{recipe['id']}@{recipe['version']}"
    try:
        supplied = json.loads(input_file.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return {"recipe_id": recipe.get("id"), "passed": False, "status": "needs-input", "steps_run": [], "errors": [f"input-json-invalid: {exc}"]}
    if not isinstance(supplied, dict):
        return {"recipe_id": recipe.get("id"), "passed": False, "status": "needs-input", "steps_run": [], "errors": ["input must be a JSON object"]}
    missing = [key for key in recipe["inputs"] if key not in supplied]
    if missing:
        return {"recipe_id": recipe["id"], "passed": False, "status": "needs-input", "steps_run": [], "errors": [f"missing inputs: {missing}"]}

    workflow_state = None
    if state_dir is not None:
        try:
            workflow_state = load_state(state_dir)
        except StateError as exc:
            return {"recipe_id": recipe["id"], "passed": False, "status": "blocked", "steps_run": [], "errors": [str(exc)]}
        if workflow_state is None:
            workflow_state = new_state(workspace.name, recipe.get("description", recipe["id"]), recipe_ref)
        elif workflow_state["recipe_ref"] != recipe_ref:
            return {"recipe_id": recipe["id"], "passed": False, "status": "blocked", "steps_run": [], "errors": ["workflow-state-recipe-mismatch"]}

    previous: dict[str, object] = {}
    previous_result = output_dir / "result.json"
    if previous_result.is_file():
        try:
            previous = json.loads(previous_result.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            previous = {}
    previous_steps = {item.get("step_id"): item for item in previous.get("steps_run", []) if isinstance(item, dict) and item.get("step_id")}

    output_dir.mkdir(parents=True, exist_ok=True)
    artifacts: dict[str, object] = dict(supplied)
    steps_run: list[dict[str, object]] = []
    failures: list[dict[str, object]] = []
    errors: list[str] = []
    final_status = "running"
    upstream_reran = False
    ordered = _topological_steps(recipe)
    ordered_by_id = {step["id"]: step for step in ordered}
    queue = [step["id"] for step in ordered]
    attempts: dict[str, int] = dict(workflow_state.get("attempts", {})) if workflow_state else {}
    fingerprints = set(workflow_state.get("failure_fingerprints", [])) if workflow_state else set()
    retry = recipe.get("retry_policy", {"max_attempts": 1, "stop_on_repeated_failure": True})
    feedback: dict[tuple[str, str], object] = {}
    policy = ExecutionPolicy(frozenset(authorization or set()))
    _persist_workflow(state_dir, workflow_state, steps_run, "running", queue[0] if queue else "complete")

    while queue:
        step_id = queue.pop(0)
        step = ordered_by_id[step_id]
        attempts[step_id] = attempts.get(step_id, 0) + 1
        if workflow_state is not None:
            workflow_state["attempts"] = attempts

        is_child = "recipe" in step
        target_ref = step.get("recipe") if is_child else step.get("ref")
        input_data = {logical: artifacts[source] for logical, source in step["input_map"].items()}
        for (target_step, target_input), value in feedback.items():
            if target_step == step_id:
                input_data[target_input] = value
        step_input_sha256 = hashlib.sha256(json.dumps(input_data, ensure_ascii=False, sort_keys=True).encode("utf-8")).hexdigest()
        output_path = output_dir / f"{step_id}.md"
        cached = previous_steps.get(step_id, {})
        invalidated_previous_evidence = None
        if cached:
            if upstream_reran:
                invalidated_previous_evidence = "upstream-reran"
            elif cached.get("slot_ref") != target_ref or cached.get("input_sha256") != step_input_sha256:
                invalidated_previous_evidence = "input-or-contract-changed"

        if not is_child and not upstream_reran and cached.get("status") == "passed" and cached.get("slot_ref") == target_ref and cached.get("input_sha256") == step_input_sha256 and output_path.is_file() and hashlib.sha256(output_path.read_bytes()).hexdigest() == cached.get("output_sha256"):
            output = output_path.read_text(encoding="utf-8")
            gate_results = evaluate_gates(step["gates"], output, input_data)
            if all(result["passed"] is True for result in gate_results):
                for artifact in step["output_map"].values():
                    artifacts[artifact] = output
                reused = dict(cached)
                reused.update({"reused": True, "gates": gate_results, "attempt": attempts[step_id]})
                steps_run.append(reused)
                _persist_workflow(state_dir, workflow_state, steps_run, "running", queue[0] if queue else "complete")
                continue

        upstream_reran = True
        started = time.perf_counter()
        execution_evidence: dict = {}
        execution_exception = False
        try:
            if is_child:
                child_id = step["recipe"].rsplit("@", 1)[0]
                child_path = recipe_path.parent / f"{child_id}.json"
                child_input = output_dir / f"{step_id}-input.json"
                child_input.write_text(json.dumps({source: artifacts[source] for source in step["input_map"].values()}, ensure_ascii=False, indent=2), encoding="utf-8")
                child_result = execute_recipe(
                    child_path, child_input, output_dir / step_id,
                    workspace_root=workspace, timeout=timeout, worker=worker,
                    require_release_evidence=require_release_evidence,
                    state_dir=(state_dir / step_id) if state_dir else None,
                    authorization=authorization, repository=repository,
                    workspace_runner=workspace_runner,
                )
                status = child_result["status"]
                child_recipe = json.loads(child_path.read_text(encoding="utf-8"))
                rendered = []
                for logical_output, artifact in step["output_map"].items():
                    value = _artifact_for_recipe_output(child_recipe, child_result, logical_output, workspace)
                    artifacts[artifact] = value
                    rendered.append(f"## {logical_output}\n\n{value}")
                output = f"Status: {status}\n\n" + "\n\n".join(rendered)
                gate_results = [{"gate": gate, "passed": bool(child_result.get("passed")), "evidence": [str(output_dir / step_id / "result.json")]} for gate in step["gates"]]
                execution_evidence = {"adapter": "subrecipe", "result": child_result}
            else:
                slot_id = step["slot"]
                if not _safe_id(slot_id):
                    raise RuntimeError("unsafe-slot-id")
                slot_dir = slots_root / slot_id
                contract = json.loads((slot_dir / "contract.json").read_text(encoding="utf-8"))
                skill = (slot_dir / "SKILL.md").read_text(encoding="utf-8")
                prompt = "\n".join([
                    f"You are executing slot: {slot_id}",
                    f"Responsibility: {contract['responsibility']}",
                    f"Required gates: {json.dumps(step['gates'])}",
                    f"\nSKILL.md:\n{skill}",
                    f"\nINPUT:\n{json.dumps(input_data, ensure_ascii=False, indent=2)}",
                    "\nProduce the complete output artifact. The first line must be exactly Status: passed, Status: needs-input, Status: blocked, or Status: failed.",
                ])
                execution = contract.get("execution", {"adapter": "artifact", "tools": [], "mutation": "run-output", "authorization": {"required": False, "scopes": []}, "correction_inputs": []})
                adapter = step.get("execution_adapter", execution["adapter"])
                if adapter == "workspace":
                    kwargs = {
                        "repository": (repository or workspace), "tools": execution["tools"],
                        "mutation": execution["mutation"], "policy": policy,
                    }
                    if workspace_runner is not None:
                        kwargs["runner"] = workspace_runner
                    output, execution_evidence = workspace_adapter(prompt, timeout, **kwargs)
                else:
                    output, execution_evidence = artifact_adapter(prompt, timeout, worker)
                status = _status(output)
                if status is None:
                    raise RuntimeError("invalid-status")
                gate_results = evaluate_gates(step["gates"], output, input_data)
                failed_gates = [result["gate"] for result in gate_results if result["passed"] is not True]
                if status == "passed" and failed_gates:
                    raise RuntimeError(f"gate-failed: {failed_gates}")
                for artifact in step["output_map"].values():
                    artifacts[artifact] = output
        except (RuntimeError, PermissionError) as exc:
            execution_exception = True
            status = "blocked" if isinstance(exc, PermissionError) else "failed"
            output = f"Status: {status}\n\n{exc}"
            gate_results = []
            errors.append(f"{step_id}: {exc}")

        output_path.write_text(output, encoding="utf-8")
        record = {
            "step_id": step_id,
            "slot_id": step.get("slot"),
            "slot_ref": target_ref,
            "status": status,
            "input_sha256": step_input_sha256,
            "duration_ms": round((time.perf_counter() - started) * 1000, 3),
            "reused": False,
            "attempt": attempts[step_id],
            "invalidated_previous_evidence": invalidated_previous_evidence,
            "output_file": output_path.relative_to(workspace).as_posix() if output_path.is_relative_to(workspace) else output_path.as_posix(),
            "output_sha256": hashlib.sha256(output_path.read_bytes()).hexdigest(),
            "gates": gate_results,
            "execution": execution_evidence,
        }
        if not execution_exception:
            steps_run = [item for item in steps_run if item["step_id"] != step_id] + [record]
        final_status = status
        _persist_workflow(state_dir, workflow_state, steps_run, status if status != "passed" else "running", queue[0] if queue else "complete")
        if status == "passed":
            continue

        fingerprint = hashlib.sha256(f"{step_id}\0{status}\0{output}".encode("utf-8")).hexdigest()
        repeated = fingerprint in fingerprints
        fingerprints.add(fingerprint)
        if workflow_state is not None:
            workflow_state["failure_fingerprints"] = sorted(fingerprints)
        failures.append({"step_id": step_id, "status": status, "fingerprint": fingerprint, "output_file": record["output_file"]})
        route = _failure_route(recipe, step_id, status)
        if route is None or route["action"] in {"stop", "record-and-return"}:
            break
        if attempts.get(route["to"], 0) >= retry["max_attempts"] or (retry.get("stop_on_repeated_failure") and repeated):
            final_status = "blocked"
            errors.append(f"{step_id}: retry-budget-or-repeated-failure")
            break

        target = route["to"]
        affected = _affected_steps(recipe, target)
        for item in list(steps_run):
            if item["step_id"] in affected:
                if workflow_state is not None and item.get("output_file"):
                    workflow_state["invalidated_evidence"].append({"path": item["output_file"], "reason": f"failure-route:{step_id}->{target}"})
                steps_run.remove(item)
                for artifact in ordered_by_id[item["step_id"]]["output_map"].values():
                    artifacts.pop(artifact, None)
        for mapping in recipe.get("feedback_mappings", []):
            if mapping["from_step"] == step_id and mapping["to_step"] == target:
                feedback[(target, mapping.get("target_input", "Correction feedback"))] = output
        queue = [item["id"] for item in ordered if item["id"] in affected]
        final_status = "running"
        _persist_workflow(state_dir, workflow_state, steps_run, "running", queue[0])

    passed = not errors and final_status in {"running", "passed"} and len(steps_run) == len(recipe["steps"]) and all(item["status"] == "passed" for item in steps_run)
    if passed:
        final_status = "passed"
    elif final_status == "running":
        final_status = "failed"
    result = {
        "recipe_id": recipe["id"], "recipe_version": recipe["version"],
        "passed": passed, "status": final_status, "steps_run": steps_run,
        "failures": failures, "errors": errors,
        "input_sha256": hashlib.sha256(input_file.read_bytes()).hexdigest(),
    }
    (output_dir / "result.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    _persist_workflow(state_dir, workflow_state, steps_run, final_status, "complete" if passed else "inspect-failure")
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--recipe", type=Path, required=True)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--workspace-root", type=Path, default=Path("."))
    parser.add_argument("--state-dir", type=Path)
    parser.add_argument("--timeout", type=int, default=300)
    parser.add_argument("--authorize", action="append", default=[])
    args = parser.parse_args()
    result = execute_recipe(args.recipe, args.input, args.output_dir, workspace_root=args.workspace_root, state_dir=args.state_dir, timeout=args.timeout, authorization=set(args.authorize))
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["passed"] else 1

if __name__ == "__main__":
    raise SystemExit(main())
