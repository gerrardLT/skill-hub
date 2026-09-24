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


def test_executor_runs_topological_order_and_records_hashes(tmp_path: Path) -> None:
    root, recipe, input_path = workspace(tmp_path)
    def worker(prompt: str, timeout: int) -> str:
        return "Status: passed\nArtifact."

    result = execute_recipe(recipe, input_path, root / "runs/full", workspace_root=root, worker=worker)

    assert result["passed"] is True
    assert [step["step_id"] for step in result["steps_run"]] == ["step-1-frame", "step-2-rules", "step-3-criteria", "step-4-gate"]
    assert all(len(step["output_sha256"]) == 64 for step in result["steps_run"])


def test_executor_rejects_invalid_status(tmp_path: Path) -> None:
    root, recipe, input_path = workspace(tmp_path)

    result = execute_recipe(recipe, input_path, root / "runs/invalid", workspace_root=root, worker=lambda *_: "Status: maybe\nArtifact.")

    assert result["status"] == "failed"
    assert result["steps_run"] == []
    assert result["errors"] == ["step-1-frame: invalid-status"]


def test_executor_requires_named_inputs(tmp_path: Path) -> None:
    root, recipe, input_path = workspace(tmp_path)
    input_path.write_text('{}\n', encoding="utf-8")

    result = execute_recipe(recipe, input_path, root / "runs/missing", workspace_root=root, worker=lambda *_: "Status: passed")

    assert result["status"] == "needs-input"
    assert result["steps_run"] == []
