import hashlib
import json
import shutil
from pathlib import Path

from tools.curation.recipe_execute import execute_recipe

ROOT = Path(__file__).resolve().parents[2]


def workspace(tmp_path: Path) -> tuple[Path, Path, Path]:
    root = tmp_path / "workspace"
    shutil.copytree(ROOT / "slots", root / "slots")
    shutil.copytree(ROOT / "recipes", root / "recipes")
    recipe_path = root / "recipes/requirements-to-acceptance-criteria.json"
    run = root / "evals/runs/composition/verified"
    run.mkdir(parents=True)
    result = run / "result.json"
    result.write_text('{"passed": true, "recipe_id": "requirements-to-acceptance-criteria"}\n', encoding="utf-8")
    review = run / "review.json"
    review.write_text('{"verdict": "approved"}\n', encoding="utf-8")
    recipe = json.loads(recipe_path.read_text(encoding="utf-8"))
    recipe["evidence"] = {
        "composition_runs": [{"path": result.relative_to(root).as_posix(), "sha256": hashlib.sha256(result.read_bytes()).hexdigest()}],
        "review": {"path": review.relative_to(root).as_posix(), "sha256": hashlib.sha256(review.read_bytes()).hexdigest()},
    }
    recipe_path.write_text(json.dumps(recipe), encoding="utf-8")
    input_path = root / "input.json"
    input_path.write_text(json.dumps({
        "validated-product-brief": "brief",
        "evidence-sources": "evidence",
        "constraints": "constraints",
        "authority-metadata": "authority",
    }), encoding="utf-8")
    return root, recipe_path, input_path


def test_executor_stops_on_needs_input(tmp_path: Path) -> None:
    root, recipe, input_path = workspace(tmp_path)
    calls = []
    def worker(prompt: str, timeout: int) -> str:
        calls.append(prompt)
        return "Status: needs-input\nNeed an authority decision."

    result = execute_recipe(recipe, input_path, root / "runs/one", workspace_root=root, worker=worker)

    assert result["status"] == "needs-input"
    assert result["passed"] is False
    assert len(result["steps_run"]) == 1
    assert len(calls) == 1


def released_outputs() -> iter:
    for name in ("step-1-frame.md", "step-2-rules.md", "step-3-criteria.md", "step-4-gate.md"):
        yield (ROOT / "evals/runs/composition/requirements-to-acceptance-criteria-v0.2.0" / name).read_text(encoding="utf-8")


def test_executor_runs_topological_order_and_records_hashes(tmp_path: Path) -> None:
    root, recipe, input_path = workspace(tmp_path)
    outputs = released_outputs()
    def worker(prompt: str, timeout: int) -> str:
        return next(outputs)

    result = execute_recipe(recipe, input_path, root / "runs/full", workspace_root=root, worker=worker)

    assert result["passed"] is True
    assert [step["step_id"] for step in result["steps_run"]] == ["step-1-frame", "step-2-rules", "step-3-criteria", "step-4-gate"]
    assert all(len(step["output_sha256"]) == 64 for step in result["steps_run"])
    assert all(all(gate["passed"] for gate in step["gates"]) for step in result["steps_run"])


def test_executor_rejects_status_pass_when_deterministic_gate_fails(tmp_path: Path) -> None:
    root, recipe, input_path = workspace(tmp_path)

    result = execute_recipe(recipe, input_path, root / "runs/gate-fail", workspace_root=root, worker=lambda *_: "Status: passed\nUnsupported prose.")

    assert result["status"] == "failed"
    assert result["steps_run"][0]["status"] == "failed"
    assert "Unsupported prose." in Path(root / result["steps_run"][0]["output_file"]).read_text(encoding="utf-8")
    assert result["errors"] == ["step-1-frame: gate-failed: ['source-traceability']"]


def test_executor_rejects_invalid_status(tmp_path: Path) -> None:
    root, recipe, input_path = workspace(tmp_path)

    result = execute_recipe(recipe, input_path, root / "runs/invalid", workspace_root=root, worker=lambda *_: "Status: maybe\nArtifact.")

    assert result["status"] == "failed"
    assert result["steps_run"][0]["status"] == "failed"
    assert "Status: maybe" in Path(root / result["steps_run"][0]["output_file"]).read_text(encoding="utf-8")
    assert result["errors"] == ["step-1-frame: invalid-status"]


def test_contract_compatible_replacement_runs_without_internal_prompt_coupling(tmp_path: Path) -> None:
    root, recipe_path, input_path = workspace(tmp_path)
    replacement = root / "slots/problem-framing-compatible"
    shutil.copytree(root / "slots/problem-framing", replacement)
    contract_path = replacement / "contract.json"
    contract = json.loads(contract_path.read_text(encoding="utf-8"))
    contract["id"] = "problem-framing-compatible"
    contract_path.write_text(json.dumps(contract), encoding="utf-8")
    provenance_path = replacement / "provenance.json"
    provenance = json.loads(provenance_path.read_text(encoding="utf-8"))
    provenance["id"] = "problem-framing-compatible"
    provenance_path.write_text(json.dumps(provenance), encoding="utf-8")
    recipe_data = json.loads(recipe_path.read_text(encoding="utf-8"))
    recipe_data["steps"][0]["slot"] = "problem-framing-compatible"
    recipe_data["steps"][0]["ref"] = "problem-framing-compatible@0.2.0"
    recipe_path.write_text(json.dumps(recipe_data), encoding="utf-8")
    outputs = released_outputs()

    result = execute_recipe(
        recipe_path,
        input_path,
        root / "runs/replacement",
        workspace_root=root,
        worker=lambda *_: next(outputs),
        require_release_evidence=False,
    )

    assert result["passed"] is True
    assert result["steps_run"][0]["slot_id"] == "problem-framing-compatible"


def test_upstream_input_change_invalidates_downstream_evidence(tmp_path: Path) -> None:
    root, recipe, input_path = workspace(tmp_path)
    run = root / "runs/invalidation"
    calls: list[str] = []
    outputs = released_outputs()
    def first_worker(prompt: str, timeout: int) -> str:
        calls.append(prompt)
        return next(outputs)
    first = execute_recipe(recipe, input_path, run, workspace_root=root, worker=first_worker)
    assert first["passed"] is True
    assert len(calls) == 4

    input_data = json.loads(input_path.read_text(encoding="utf-8"))
    input_data["validated-product-brief"] = "changed brief"
    input_path.write_text(json.dumps(input_data), encoding="utf-8")
    calls.clear()
    outputs = released_outputs()
    second = execute_recipe(recipe, input_path, run, workspace_root=root, worker=first_worker)

    assert second["passed"] is True
    assert len(calls) == 4
    assert all(step["reused"] is False for step in second["steps_run"])
    assert first["steps_run"][0]["input_sha256"] != second["steps_run"][0]["input_sha256"]
    assert second["steps_run"][0]["invalidated_previous_evidence"] == "input-or-contract-changed"
    assert all(step["invalidated_previous_evidence"] == "upstream-reran" for step in second["steps_run"][1:])


def test_unchanged_input_reuses_validated_step_evidence(tmp_path: Path) -> None:
    root, recipe, input_path = workspace(tmp_path)
    run = root / "runs/reuse"
    outputs = released_outputs()
    first = execute_recipe(recipe, input_path, run, workspace_root=root, worker=lambda *_: next(outputs))
    assert first["passed"] is True

    second = execute_recipe(recipe, input_path, run, workspace_root=root, worker=lambda *_: (_ for _ in ()).throw(AssertionError("worker should not run")))

    assert second["passed"] is True
    assert all(step["reused"] is True for step in second["steps_run"])


def test_executor_requires_named_inputs(tmp_path: Path) -> None:
    root, recipe, input_path = workspace(tmp_path)
    input_path.write_text('{}\n', encoding="utf-8")

    result = execute_recipe(recipe, input_path, root / "runs/missing", workspace_root=root, worker=lambda *_: "Status: passed")

    assert result["status"] == "needs-input"
    assert result["steps_run"] == []


def test_executor_persists_machine_state_and_generated_view(tmp_path: Path) -> None:
    root, recipe, input_path = workspace(tmp_path)
    outputs = released_outputs()
    state_dir = root / ".workflow"

    result = execute_recipe(recipe, input_path, root / "runs/state", workspace_root=root, worker=lambda *_: next(outputs), state_dir=state_dir)

    assert result["passed"] is True
    state = json.loads((state_dir / "state.json").read_text(encoding="utf-8"))
    assert state["recipe_ref"] == "requirements-to-acceptance-criteria@0.2.0"
    assert len(state["steps"]) == 4
    assert all(step["attempts"] == 1 for step in state["steps"])
    assert "status: passed" in (state_dir / "state.md").read_text(encoding="utf-8")


def routed_recipe(tmp_path: Path, *, action: str = "invalidate-and-rerun", max_attempts: int = 2) -> tuple[Path, Path, Path]:
    root, recipe_path, input_path = workspace(tmp_path)
    recipe_data = json.loads(recipe_path.read_text(encoding="utf-8"))
    recipe_data["retry_policy"] = {"max_attempts": max_attempts, "stop_on_repeated_failure": True}
    statuses = ["needs-input", "failed", "blocked"]
    recipe_data["failure_routes"] = [
        {"from": step["id"], "to": ("step-1-frame" if step["id"] == "step-1-frame" else recipe_data["steps"][index - 1]["id"]), "on_status": statuses, "action": action}
        for index, step in enumerate(recipe_data["steps"])
    ]
    recipe_data["feedback_mappings"] = [{"from_step": "step-2-rules", "to_step": "step-1-frame", "artifact": "requirements-artifact", "target_input": "Supplied product context"}]
    recipe_path.write_text(json.dumps(recipe_data), encoding="utf-8")
    return root, recipe_path, input_path


def test_stop_route_preserves_failure_and_does_not_run_downstream(tmp_path: Path) -> None:
    root, recipe, input_path = routed_recipe(tmp_path, action="stop")
    calls = []
    result = execute_recipe(recipe, input_path, root / "runs/stop", workspace_root=root, worker=lambda *_: calls.append(1) or "Status: needs-input\nNeed decision.", require_release_evidence=False)
    assert result["status"] == "needs-input"
    assert len(calls) == 1
    assert result["failures"][0]["status"] == "needs-input"


def test_record_and_return_preserves_failed_artifact(tmp_path: Path) -> None:
    root, recipe, input_path = routed_recipe(tmp_path, action="record-and-return")
    result = execute_recipe(recipe, input_path, root / "runs/record", workspace_root=root, worker=lambda *_: "Status: blocked\nNo authority.", require_release_evidence=False)
    assert result["status"] == "blocked"
    assert Path(root / result["failures"][0]["output_file"]).is_file()


def test_invalidate_and_rerun_stops_at_retry_budget(tmp_path: Path) -> None:
    root, recipe, input_path = routed_recipe(tmp_path, max_attempts=2)
    calls = []
    result = execute_recipe(recipe, input_path, root / "runs/retry", workspace_root=root, worker=lambda *_: calls.append(1) or "Status: failed\nSame failure.", require_release_evidence=False, state_dir=root / ".workflow")
    assert result["status"] == "blocked"
    assert len(calls) == 2
    assert any("retry-budget-or-repeated-failure" in error for error in result["errors"])
    state = json.loads((root / ".workflow/state.json").read_text(encoding="utf-8"))
    assert state["attempts"]["step-1-frame"] == 2


def test_failure_feedback_reaches_rerun_and_invalidates_downstream(tmp_path: Path) -> None:
    root, recipe, input_path = routed_recipe(tmp_path, max_attempts=2)
    outputs = list(released_outputs())
    call = 0
    def worker(prompt: str, timeout: int) -> str:
        nonlocal call
        call += 1
        if call == 1:
            return outputs[0]
        if call == 2:
            return "Status: failed\nCorrection feedback: preserve the exact route."
        if call == 3:
            assert "preserve the exact route" in prompt
            return outputs[0]
        return outputs[call - 3]

    result = execute_recipe(recipe, input_path, root / "runs/feedback", workspace_root=root, worker=worker, require_release_evidence=False, state_dir=root / ".workflow")

    assert result["passed"] is True, result
    assert call == 6
    state = json.loads((root / ".workflow/state.json").read_text(encoding="utf-8"))
    assert state["attempts"]["step-1-frame"] == 2
    assert any("failure-route:step-2-rules->step-1-frame" in item["reason"] for item in state["invalidated_evidence"])
