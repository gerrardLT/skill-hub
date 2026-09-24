"""Execute a verified recipe through released slot contracts."""
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

from tools.curation.recipe_verify import verify_recipes

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


def execute_recipe(
    recipe_path: Path,
    input_file: Path,
    output_dir: Path,
    *,
    workspace_root: Path | None = None,
    timeout: int = 300,
    worker: Callable[[str, int], str] = _pi_worker,
    require_release_evidence: bool = True,
) -> dict[str, object]:
    workspace = (workspace_root or Path.cwd()).resolve()
    recipe_path = recipe_path.resolve()
    slots_root = workspace / "slots"
    verification = verify_recipes(recipe_path.parent, slots_root, workspace, recipe_path)
    if require_release_evidence and not verification["ok"]:
        return {"recipe_id": None, "passed": False, "status": "blocked", "steps_run": [], "errors": [f"recipe-verification: {error['code']}" for error in verification["errors"]]}

    recipe = json.loads(recipe_path.read_text(encoding="utf-8"))
    try:
        supplied = json.loads(input_file.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return {"recipe_id": recipe.get("id"), "passed": False, "status": "needs-input", "steps_run": [], "errors": [f"input-json-invalid: {exc}"]}
    if not isinstance(supplied, dict):
        return {"recipe_id": recipe.get("id"), "passed": False, "status": "needs-input", "steps_run": [], "errors": ["input must be a JSON object"]}
    missing = [key for key in recipe["inputs"] if key not in supplied]
    if missing:
        return {"recipe_id": recipe["id"], "passed": False, "status": "needs-input", "steps_run": [], "errors": [f"missing inputs: {missing}"]}

    output_dir.mkdir(parents=True, exist_ok=True)
    artifacts: dict[str, object] = dict(supplied)
    steps_run: list[dict[str, object]] = []
    errors: list[str] = []
    final_status = "passed"
    for step in _topological_steps(recipe):
        step_id = step["id"]
        slot_id = step["slot"]
        if not _safe_id(slot_id):
            errors.append(f"{step_id}: unsafe-slot-id")
            final_status = "blocked"
            break
        slot_dir = slots_root / slot_id
        contract = json.loads((slot_dir / "contract.json").read_text(encoding="utf-8"))
        skill = (slot_dir / "SKILL.md").read_text(encoding="utf-8")
        input_data = {logical: artifacts[source] for logical, source in step["input_map"].items()}
        prompt = "\n".join([
            f"You are executing slot: {slot_id}",
            f"Responsibility: {contract['responsibility']}",
            f"Required gates: {json.dumps(step['gates'])}",
            f"\nSKILL.md:\n{skill}",
            f"\nINPUT:\n{json.dumps(input_data, ensure_ascii=False, indent=2)}",
            "\nProduce the complete output artifact. The first line must be exactly Status: passed, Status: needs-input, Status: blocked, or Status: failed.",
        ])
        started = time.perf_counter()
        try:
            output = worker(prompt, timeout)
        except RuntimeError as exc:
            errors.append(f"{step_id}: {exc}")
            final_status = "failed"
            break
        status = _status(output)
        if status is None:
            errors.append(f"{step_id}: invalid-status")
            final_status = "failed"
            break
        output_path = output_dir / f"{step_id}.md"
        output_path.write_text(output, encoding="utf-8")
        for _, artifact in step["output_map"].items():
            artifacts[artifact] = output
        steps_run.append({
            "step_id": step_id,
            "slot_id": slot_id,
            "slot_ref": step["ref"],
            "status": status,
            "duration_ms": round((time.perf_counter() - started) * 1000, 3),
            "output_file": output_path.relative_to(workspace).as_posix() if output_path.is_relative_to(workspace) else output_path.as_posix(),
            "output_sha256": hashlib.sha256(output_path.read_bytes()).hexdigest(),
            "gates": step["gates"],
        })
        final_status = status
        if status != "passed":
            break

    result = {
        "recipe_id": recipe["id"],
        "recipe_version": recipe["version"],
        "passed": not errors and final_status == "passed" and len(steps_run) == len(recipe["steps"]),
        "status": final_status,
        "steps_run": steps_run,
        "errors": errors,
        "input_sha256": hashlib.sha256(input_file.read_bytes()).hexdigest(),
    }
    (output_dir / "result.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--recipe", type=Path, required=True)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--workspace-root", type=Path, default=Path("."))
    parser.add_argument("--timeout", type=int, default=300)
    args = parser.parse_args()
    result = execute_recipe(args.recipe, args.input, args.output_dir, workspace_root=args.workspace_root, timeout=args.timeout)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
