"""Execute verified recipes with durable state, evidence reuse, and failure routing."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import tempfile
import time
from pathlib import Path, PurePosixPath
from typing import Callable

try:
    from tools.curation.execution_adapters import ExecutionPolicy, artifact_adapter, workspace_adapter
    from tools.curation.recipe_verify import verify_recipes
    from tools.curation.slot_gate import evaluate_gates as evaluate_v1_gates
    from tools.curation.v2_machine_gates import MACHINE_GATES as V2_GATES
    from tools.curation.v2_machine_gates import evaluate_machine_gate
    from tools.curation.workflow_state import StateError, load_state, new_state, save_state
except ModuleNotFoundError:  # direct script execution
    from execution_adapters import ExecutionPolicy, artifact_adapter, workspace_adapter
    from recipe_verify import verify_recipes
    from slot_gate import evaluate_gates as evaluate_v1_gates
    from v2_machine_gates import MACHINE_GATES as V2_GATES
    from v2_machine_gates import evaluate_machine_gate
    from workflow_state import StateError, load_state, new_state, save_state


def evaluate_gates(gates: list[str], output: str, inputs: dict[str, Any]) -> list[dict[str, object]]:
    """Evaluate a step's gates.

    V1 recipes name structural gate ids handled by slot_gate. V2 consolidated recipes name
    machine gates handled by v2_machine_gates. A gate neither layer recognises is a defect
    and fails closed rather than passing silently.
    """
    results: list[dict[str, object]] = []
    v1_gates = [gate for gate in gates if gate not in V2_GATES]
    if v1_gates:
        results.extend(evaluate_v1_gates(v1_gates, output, inputs))
    for gate in gates:
        if gate in V2_GATES:
            results.append(evaluate_machine_gate(gate, output, inputs))
    return results

VALID_STATUSES = {"passed", "needs-input", "blocked", "failed"}
EVAL_MODEL = os.environ.get("CAPABILITY_EVAL_MODEL", "cx/gpt-5.6-terra")


def _safe_id(value: object) -> bool:
    return isinstance(value, str) and value and PurePosixPath(value).name == value and value not in {".", ".."}


def _topological_steps(recipe: dict) -> list[dict]:
    steps = {step["id"]: step for step in recipe["steps"]}
    dependencies = {step_id: set(step.get("depends_on", [])) for step_id, step in steps.items()}

    # Dependency records name capabilities, while a step is keyed by its mode. Resolve both
    # so an edge is found whichever form the recipe used.
    by_capability: dict[str, set[str]] = {}
    for step_id, step in steps.items():
        for key in (step.get('skill'), step.get('id')):
            if key:
                by_capability.setdefault(key, set()).add(step_id)

    def resolve(capability: str) -> set[str]:
        return by_capability.get(capability, set())

    for dep in recipe.get("dependency_records", []):
        kind = dep.get("kind")
        # Only `hard` orders steps. `optional` means "use it if present, do not wait for it",
        # and `feedback` carries later evidence into a future lifecycle pass. Treating either
        # as an ordering edge invents prerequisites the recipe did not declare and can create
        # cycles, so both are recorded rather than enforced.
        if kind != "hard":
            continue
        src = dep.get("source_capability_id", "").replace("capability:", "")
        tgt = dep.get("target_capability_id", "").replace("capability:", "")
        for target_step in resolve(tgt):
            for source_step in resolve(src):
                if source_step != target_step:
                    dependencies[target_step].add(source_step)

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
                executable, "-p", "--mode", "json", "--model", EVAL_MODEL, "--thinking", "low", "--no-tools", "--no-skills",
                "--no-extensions", "--no-context-files", "--no-session", "--offline",
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
    outputs = [
        "".join(part.get("text", "") for part in event["message"].get("content", []) if part.get("type") == "text")
        for event in events
        if event.get("type") == "message_end" and event.get("message", {}).get("role") == "assistant"
    ]
    output = next((value for value in reversed(outputs) if value.strip()), "")
    if not output:
        raise RuntimeError("no-output")
    return output, {
        "model_events": [{"type": event.get("type"), "role": event.get("message", {}).get("role")} for event in events],
        "process_returncode": process.returncode,
        "model": EVAL_MODEL,
        "prompt_sha256": hashlib.sha256(prompt.encode("utf-8")).hexdigest(),
    }


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


def _recipe_path(parent: Path, recipe_id: str, workspace: Path) -> Path:
    local = parent / f"{recipe_id}.json"
    released = workspace / "recipes" / f"{recipe_id}.json"
    if local.is_file():
        return local
    if released.is_file():
        return released
    raise RuntimeError(f"child-recipe-missing:{recipe_id}")


def _artifact_for_recipe_output(child_recipe: dict, child_result: dict, artifact: str, workspace: Path) -> str:
    producer_steps = [step for step in child_recipe["steps"] if artifact in step["output_map"].values()]
    if not producer_steps:
        raise RuntimeError(f"child-output-without-producer:{artifact}")
    producer = producer_steps[-1]
    records = {item["step_id"]: item for item in child_result.get("steps_run", [])}
    record = records.get(producer["id"])
    if not record:
        raise RuntimeError(f"child-output-missing:{artifact}")
    nested_artifacts = record.get("execution", {}).get("artifacts", {})
    logical_output = next((key for key, value in producer["output_map"].items() if value == artifact), None)
    if logical_output in nested_artifacts:
        return nested_artifacts[logical_output]
    if not record.get("output_file"):
        raise RuntimeError(f"child-output-missing:{artifact}")
    path = Path(record["output_file"])
    if not path.is_absolute():
        path = workspace / path
    return path.read_text(encoding="utf-8")


def resolve_permission(contract: dict, mode: str | None) -> str | None:
    """Return the permission identity that governs a run.

    A consolidated capability may declare several modes with different permissions. The
    selected mode's permission wins; the document-level value is only a default and is
    never allowed to widen the mode.
    """
    per_mode = contract.get('mode_permissions') or {}
    if mode and mode in per_mode:
        return per_mode[mode]
    return contract.get('permission_identity')


def select_mode(skill_text: str, mode: str) -> str:
    """Return the shared preamble plus exactly one mode section.

    Consolidated capabilities embed several modes in one document. Loading all of them
    floods the prompt and invites cross-mode blending, so the executor loads the mode
    selection table plus the single requested mode when one is named. A single-mode
    skill has no mode sections and is returned unchanged.
    """
    if not mode:
        return skill_text
    marker = f"## Mode: `{mode}`"
    start = skill_text.find(marker)
    if start == -1:
        return skill_text
    preamble = skill_text[:start]
    rest = skill_text[start:]
    following = rest.find("\n## Mode: `", 1)
    section = rest if following == -1 else rest[:following]
    return preamble.rstrip() + "\n\n" + section.strip() + "\n"


def _step_is_runnable(step: dict, active_steps: set[str] | None) -> bool:
    """Decide whether a step may run at all.

    V2 stage recipes declare most steps `conditional` with `default_state: skipped`, so a
    stage is an opt-in menu rather than a fixed pipeline: a step runs only when the caller
    names it. Steps marked `disabled-pending-current-authorization` never run automatically,
    whatever the caller asks for.
    """
    activation = step.get('activation')
    if activation == 'disabled-pending-current-authorization':
        return False
    if activation == 'conditional':
        return bool(active_steps) and step.get('id') in active_steps
    return True


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
    verification_commands: list[list[str]] | None = None,
    deliver_changes: bool = False,
    allow_evaluating: bool = False,
    active_steps: set[str] | None = None,
) -> dict[str, object]:
    workspace = (workspace_root or Path.cwd()).resolve()
    recipe_path = recipe_path.resolve()
    slots_root = workspace / "slots"
    verification = verify_recipes(recipe_path.parent, slots_root, workspace, recipe_path, allow_evaluating=allow_evaluating)
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
    required_inputs = recipe.get("inputs", [])
    missing = [key for key in required_inputs if key not in supplied]
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
    skipped: list[dict[str, object]] = []
    runnable = []
    for step in ordered:
        if _step_is_runnable(step, active_steps):
            runnable.append(step)
        else:
            skipped.append({
                'step_id': step.get('id'),
                'skill': step.get('skill'),
                'mode': step.get('mode'),
                'activation': step.get('activation'),
                'reason': ('disabled-pending-current-authorization'
                           if step.get('activation') == 'disabled-pending-current-authorization'
                           else 'conditional-step-not-activated'),
            })
    ordered = runnable
    if active_steps is not None:
        # Expand active_steps with transitive hard prerequisites
        needed = set(active_steps)
        for dep in recipe.get("dependency_records", []):
            if dep.get("kind") == "hard":
                src = dep.get("source_capability_id", "").replace("capability:", "")
                tgt = dep.get("target_capability_id", "").replace("capability:", "")
                if tgt in needed:
                    needed.add(src)
        ordered = [step for step in ordered if step["id"] in needed]
    ordered_by_id = {step["id"]: step for step in ordered}
    # A stage declares no strict order between its conditional steps, so the caller supplies
    # one. An ordered activation list is honoured for every step whose hard prerequisites are
    # already satisfied; anything else keeps the recipe's own topological order.
    if active_steps:
        caller_order = [sid for sid in active_steps if sid in ordered_by_id]
        leftovers = [step["id"] for step in ordered if step["id"] not in caller_order]
        queue = caller_order + leftovers
    else:
        queue = [step["id"] for step in ordered]

    # A stage is an opt-in menu. If the caller activated nothing and every remaining step is
    # conditional, the stage cannot proceed until the owner chooses; that is needs-input,
    # not a failure.
    if not queue and skipped and all(
            entry.get('reason') == 'conditional-step-not-activated' for entry in skipped):
        menu = [{'step_id': entry['step_id'], 'skill': entry.get('skill'), 'mode': entry.get('mode')}
                for entry in skipped]
        result = {
            'recipe_id': recipe['id'], 'recipe_version': recipe['version'],
            'passed': False, 'status': 'needs-input', 'steps_run': [],
            'skipped_steps': skipped, 'available_steps': menu,
            'failures': [],
            'errors': ['no step activated: name the capabilities that apply to this request'],
            'input_sha256': hashlib.sha256(input_file.read_bytes()).hexdigest(),
        }
        output_dir.mkdir(parents=True, exist_ok=True)
        (output_dir / 'result.json').write_text(
            json.dumps(result, ensure_ascii=False, indent=2) + '\n',
            encoding='utf-8', newline='\n')
        _persist_workflow(state_dir, workflow_state, [], 'needs-input', 'select-steps')
        return result
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
        target_ref = step.get("recipe") if is_child else (step.get("ref") or step.get("skill_ref") or step["id"])
        step_input_map = step.get("input_map")
        if step_input_map is not None:
            input_data = {logical: artifacts[source] for logical, source in step_input_map.items()}
        else:
            input_data = dict(artifacts)
        step_output_map = step.get("output_map") or {out: out for out in step.get("outputs", [f"{step['id']}-artifact"])}
        step_gates = step.get("gates") if "gates" in step else step.get("hard_gates", [])
        advisory_gates = step.get("advisory_gates") or []
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
            gate_results = evaluate_gates(step_gates, output, input_data)
            if all(result["passed"] is True for result in gate_results):
                for artifact in step_output_map.values():
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
        raw_output = ""
        try:
            if is_child:
                child_id = step["recipe"].rsplit("@", 1)[0]
                child_path = _recipe_path(recipe_path.parent, child_id, workspace)
                child_input = output_dir / f"{step_id}-input.json"
                child_input.write_text(json.dumps(input_data, ensure_ascii=False, indent=2), encoding="utf-8")
                child_result = execute_recipe(
                    child_path, child_input, output_dir / step_id,
                    workspace_root=workspace, timeout=timeout, worker=worker,
                    require_release_evidence=require_release_evidence,
                    state_dir=(state_dir / step_id) if state_dir else None,
                    authorization=authorization, repository=repository,
                    workspace_runner=workspace_runner,
                    verification_commands=verification_commands,
                    deliver_changes=deliver_changes,
                    allow_evaluating=allow_evaluating,
                )
                status = child_result["status"]
                child_recipe = json.loads(child_path.read_text(encoding="utf-8"))
                rendered = []
                child_artifacts: dict[str, str] = {}
                if child_result.get("passed"):
                    for logical_output, artifact in step_output_map.items():
                        value = _artifact_for_recipe_output(child_recipe, child_result, logical_output, workspace)
                        child_artifacts[logical_output] = value
                        artifacts[artifact] = value
                        rendered.append(f"## {logical_output}\n\n{value}")
                else:
                    rendered.append("## Child result\n\n" + json.dumps(child_result, ensure_ascii=False, indent=2))
                output = f"Status: {status}\n\n" + "\n\n".join(rendered)
                gate_results = [{"gate": gate, "passed": bool(child_result.get("passed")), "evidence": [str(output_dir / step_id / "result.json")]} for gate in step_gates]
                execution_evidence = {"adapter": "subrecipe", "result": child_result, "artifacts": child_artifacts}
            else:
                slot_id = step.get("slot") or step["id"]
                if not _safe_id(slot_id):
                    raise RuntimeError("unsafe-slot-id")
                if "candidate_path" in step:
                    slot_dir = (workspace / step["candidate_path"]).resolve()
                else:
                    slot_dir = slots_root / slot_id
                contract = json.loads((slot_dir / "contract.json").read_text(encoding="utf-8"))
                skill = (slot_dir / "SKILL.md").read_text(encoding="utf-8")
                requested_mode = step.get("mode")
                declared_modes = contract.get("modes") or []
                if requested_mode and requested_mode in declared_modes:
                    skill = select_mode(skill, requested_mode)
                elif requested_mode and declared_modes:
                    raise RuntimeError(f"unknown-mode: {requested_mode}")
                effective_permission = resolve_permission(contract, requested_mode)
                prompt = "\n".join([
                    f"You are executing slot: {slot_id}",
                    f"Responsibility: {contract['responsibility']}",
                    f"Required gates: {json.dumps(step_gates)}",
                    f"\nSKILL.md:\n{skill}",
                    f"\nINPUT:\n{json.dumps(input_data, ensure_ascii=False, indent=2)}",
                    "\nProduce the complete output artifact. The first line must be exactly Status: passed, Status: needs-input, Status: blocked, or Status: failed.",
                ])
                if advisory_gates:
                    # Obligations that cannot be checked mechanically travel with the artifact so
                    # independent review receives them instead of a fake regex verdict.
                    prompt += "\n\nOBLIGATIONS TO SATISFY (checked by independent review, not by a machine gate):\n" + "\n".join(
                        f"- {gate}" for gate in advisory_gates)
                execution = contract.get("execution", {"adapter": "artifact", "tools": [], "mutation": "run-output", "authorization": {"required": False, "scopes": []}, "correction_inputs": []})
                execution_evidence = {"permission_identity": effective_permission}
                adapter = step.get("execution_adapter", execution.get("adapter", "artifact"))
                tools_list = execution.get("tools") if "tools" in execution else execution.get("model_tools", [])
                mutation_val = execution.get("mutation") if "mutation" in execution else execution.get("mutation_scope", "run-output")
                if adapter == "workspace":
                    kwargs = {
                        "repository": (repository or workspace), "tools": tools_list,
                        "mutation": mutation_val, "policy": policy,
                        "evidence_dir": output_dir / f"{step_id}-execution",
                        "verification_commands": verification_commands or [],
                        "deliver_changes": deliver_changes and mutation_val == "isolated-worktree",
                    }
                    if workspace_runner is not None:
                        kwargs["runner"] = workspace_runner
                    output, execution_evidence = workspace_adapter(prompt, timeout, **kwargs)
                    execution_evidence = {"permission_identity": effective_permission, **(execution_evidence or {})}
                    host_evidence = {
                        key: execution_evidence.get(key)
                        for key in ("duration_ms", "command_results", "git_status", "patch_file", "patch_sha256", "verification_passed", "delivered")
                    }
                    output += "\n\n## Host Execution Evidence\n\n```json\n" + json.dumps(host_evidence, ensure_ascii=False, indent=2) + "\n```"
                else:
                    output, execution_evidence = artifact_adapter(prompt, timeout, worker)
                    execution_evidence = {"permission_identity": effective_permission, **(execution_evidence or {})}
                raw_output = output
                status = _status(output)
                if status is None:
                    raise RuntimeError("invalid-status")
                gate_results = evaluate_gates(step_gates, output, input_data)
                failed_gates = [result["gate"] for result in gate_results if result["passed"] is not True]
                if status == "passed" and failed_gates:
                    raise RuntimeError(f"gate-failed: {failed_gates}")
                for artifact in step_output_map.values():
                    artifacts[artifact] = output
        except (RuntimeError, PermissionError) as exc:
            execution_exception = True
            status = "blocked" if isinstance(exc, PermissionError) else "failed"
            raw_section = f"\n\n## Raw model output\n\n{raw_output}" if raw_output else ""
            output = f"Status: {status}\n\n{exc}{raw_section}"
            gate_results = []
            errors.append(f"{step_id}: {exc}")

        output_path.write_text(output, encoding="utf-8")
        raw_output_path = output_dir / f"{step_id}.raw.md"
        if raw_output:
            raw_output_path.write_text(raw_output, encoding="utf-8")
        record = {
            "step_id": step_id,
            "slot_id": step.get("slot"),
            "slot_ref": target_ref,
            "skill": step.get("skill"),
            "mode": step.get("mode"),
            "status": status,
            "input_sha256": step_input_sha256,
            "duration_ms": round((time.perf_counter() - started) * 1000, 3),
            "reused": False,
            "attempt": attempts[step_id],
            "invalidated_previous_evidence": invalidated_previous_evidence,
            "output_file": output_path.relative_to(workspace).as_posix() if output_path.is_relative_to(workspace) else output_path.as_posix(),
            "output_sha256": hashlib.sha256(output_path.read_bytes()).hexdigest(),
            "raw_output_file": (raw_output_path.relative_to(workspace).as_posix() if raw_output_path.is_relative_to(workspace) else raw_output_path.as_posix()) if raw_output else None,
            "raw_output_sha256": hashlib.sha256(raw_output_path.read_bytes()).hexdigest() if raw_output else None,
            "gates": gate_results,
            "advisory_gates": advisory_gates,
            "advisory_review_required": bool(advisory_gates),
            "execution": execution_evidence,
        }
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

    passed = not errors and final_status in {"running", "passed"} and len(steps_run) == len(ordered) and all(item["status"] == "passed" for item in steps_run)
    if passed:
        final_status = "passed"
    elif final_status == "running":
        final_status = "failed"
    result = {
        "recipe_id": recipe["id"], "recipe_version": recipe["version"],
        "passed": passed, "status": final_status, "steps_run": steps_run,
        "skipped_steps": skipped,
        "failures": failures, "errors": errors,
        "input_sha256": hashlib.sha256(input_file.read_bytes()).hexdigest(),
    }
    (output_dir / "result.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    _persist_workflow(state_dir, workflow_state, steps_run, final_status, "complete" if passed else "inspect-failure")
    return result


def _handoff_between(composite: dict, source_stage: str, target_stage: str) -> dict | None:
    for handoff in composite.get('handoffs', []):
        if (handoff.get('source_stage_id') == source_stage
                and handoff.get('target_stage_id') == target_stage):
            return handoff
    return None


def _artifact_contract_satisfied(handoff: dict, stage_result: dict) -> tuple[bool, list[str]]:
    """Check the four handoff obligations against a stage result.

    The contract asks for identities and hashes, a decision and authority record, completion
    evidence, and known gaps with residual risk. Each is looked for in the step records the
    stage produced, so a stage that emits nothing cannot silently satisfy a handoff.
    """
    steps = stage_result.get('steps_run') or []
    if not steps:
        return False, ['stage produced no step evidence']

    missing = []
    if not any(s.get('output_sha256') for s in steps):
        missing.append('artifact identities and hashes')
    if not any((s.get('execution') or {}).get('permission_identity') for s in steps):
        missing.append('decision and authority record')
    if not any(s.get('gates') for s in steps):
        missing.append('completion evidence')
    if not any(s.get('advisory_gates') is not None for s in steps):
        missing.append('known gaps and residual risk')
    return (not missing), missing


def execute_composite(
    recipe_path: Path,
    input_file: Path,
    output_dir: Path,
    *,
    workspace_root: Path | None = None,
    active_by_stage: dict[str, set[str]] | None = None,
    **kwargs: Any,
) -> dict[str, object]:
    """Run a composite recipe: its stages in dependency order, with handoffs enforced.

    A composite is a DAG of stages. Each stage is itself an opt-in menu, so the caller names
    the steps to activate per stage. A stage that does not pass stops the composite: the next
    stage never starts on unproven input.
    """
    workspace = (workspace_root or Path.cwd()).resolve()
    recipe_path = recipe_path.resolve()
    composite = json.loads(recipe_path.read_text(encoding='utf-8'))
    stage_steps = composite.get('stage_steps') or []
    active_by_stage = active_by_stage or {}

    by_id = {entry['stage_id']: entry for entry in stage_steps}

    def normalise(reference: str) -> str:
        """Stage ids carry a `stage:` prefix; depends_on entries write `stage-NN-...`."""
        if reference in by_id:
            return reference
        candidates = [f'stage:{reference}', re.sub(r'^stage-', 'stage:', reference)]
        for candidate in candidates:
            if candidate in by_id:
                return candidate
        return reference

    deps = {entry['stage_id']: {normalise(d) for d in (entry.get('depends_on') or [])}
            for entry in stage_steps}
    order, ready = [], sorted(sid for sid, d in deps.items() if not d)
    while ready:
        sid = ready.pop(0)
        order.append(sid)
        for other, d in deps.items():
            if sid in d:
                d.discard(sid)
                if not d and other not in order and other not in ready:
                    ready.append(other)
                    ready.sort()
    if len(order) != len(stage_steps):
        return {'composite_id': composite.get('id'), 'status': 'blocked', 'passed': False,
                'stages': [], 'errors': ['composite stage graph contains a cycle']}

    output_dir.mkdir(parents=True, exist_ok=True)
    stages: list[dict[str, object]] = []
    artifacts: dict[str, object] = json.loads(input_file.read_text(encoding='utf-8'))

    for index, stage_id in enumerate(order):
        entry = by_id[stage_id]
        recipe_ref = entry.get('recipe_ref') or ''
        stage_name = recipe_ref.rsplit('@', 1)[0]
        stage_recipe = recipe_path.parent.parent / 'stages' / f'{stage_name}.json'
        if not stage_recipe.exists():
            return {'composite_id': composite.get('id'), 'status': 'blocked', 'passed': False,
                    'stages': stages, 'errors': [f'missing stage recipe: {stage_name}']}

        activated = active_by_stage.get(stage_id)
        if entry.get('mandatory_in_recipe') and not activated:
            activated = [s['id'] for s in json.loads(stage_recipe.read_text(encoding='utf-8'))['steps']]

        stage_input = output_dir / f'{stage_id}-input.json'
        stage_input.write_text(json.dumps(artifacts, ensure_ascii=False, indent=2) + '\n',
                               encoding='utf-8', newline='\n')
        # stage ids carry a colon, which is not a legal path character on Windows
        safe_dir = re.sub(r'[^A-Za-z0-9._-]+', '_', stage_id)
        stage_result = execute_recipe(
            stage_recipe, stage_input, output_dir / safe_dir,
            workspace_root=workspace, active_steps=activated, **kwargs)
        stages.append({'stage_id': stage_id, 'stage_order': index + 1,
                       'status': stage_result.get('status'),
                       'passed': stage_result.get('passed'),
                       'activated_steps': list(activated) if activated else [],
                       'steps_run': [s.get('step_id') for s in stage_result.get('steps_run', [])],
                       'result_file': (output_dir / safe_dir / 'result.json').as_posix()})

        if stage_result.get('status') != 'passed':
            return {'composite_id': composite.get('id'), 'status': stage_result.get('status'),
                    'passed': False, 'stages': stages,
                    'stopped_at': stage_id,
                    'errors': [f'{stage_id}: {stage_result.get("status")}'],
                    'stage_result': stage_result}

        # carry the stage's artifacts forward, and enforce the handoff that leads out of it
        for step in stage_result.get('steps_run', []):
            path = step.get('output_file')
            if path and (workspace / path).is_file():
                artifacts[f"{stage_id}:{step.get('step_id')}"] = (workspace / path).read_text(encoding='utf-8')
        next_stage = order[index + 1] if index + 1 < len(order) else None
        if next_stage:
            handoff = _handoff_between(composite, stage_id, next_stage)
            if handoff:
                ok, missing = _artifact_contract_satisfied(handoff, stage_result)
                if not ok:
                    return {'composite_id': composite.get('id'), 'status': 'blocked',
                            'passed': False, 'stages': stages, 'stopped_at': stage_id,
                            'errors': [f'handoff {handoff.get("id")} unsatisfied: {missing}'],
                            'stage_result': stage_result}

    result = {
        'composite_id': composite.get('id'),
        'composite_version': composite.get('version'),
        'status': 'passed', 'passed': True, 'stages': stages,
        'human_checkpoints': composite.get('human_checkpoints') or [],
        'input_sha256': hashlib.sha256(input_file.read_bytes()).hexdigest(),
        'errors': [],
    }
    (output_dir / 'composite-result.json').write_text(
        json.dumps(result, ensure_ascii=False, indent=2, default=str) + '\n',
        encoding='utf-8', newline='\n')
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
    parser.add_argument("--repository", type=Path)
    parser.add_argument("--deliver-changes", action="store_true")
    parser.add_argument("--allow-evaluating", action="store_true")
    parser.add_argument("--verify-command", action="append", default=[])
    args = parser.parse_args()
    result = execute_recipe(args.recipe, args.input, args.output_dir, workspace_root=args.workspace_root, state_dir=args.state_dir, timeout=args.timeout, authorization=set(args.authorize), repository=args.repository, deliver_changes=args.deliver_changes, allow_evaluating=args.allow_evaluating, verification_commands=[value.split("\0") for value in args.verify_command])
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["passed"] else 1

if __name__ == "__main__":
    raise SystemExit(main())
