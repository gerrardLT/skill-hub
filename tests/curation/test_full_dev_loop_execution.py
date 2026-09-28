import json
from pathlib import Path

from tools.curation.recipe_execute import execute_recipe

ROOT = Path(__file__).resolve().parents[2]


def artifact_output(slot: str) -> str:
    if slot == "problem-framing":
        return "Status: passed\nEvidence: Source SRC-1\nResponsibility: frame\nGate Results: passed\nUnknowns: none identified"
    if slot == "requirements-rules":
        return "Status: passed\nEvidence: SRC-1\nREQ-1 requirement\nRULE-1 unknown parameterized\nResponsibility: rules\nGate Results: passed\nUnknowns: unknown"
    if slot == "acceptance-criteria":
        return "Status: passed\nEvidence: EV-1\n### AC-1 success\n**Given** ready\n**When** used\n**Then** result remains available\nResponsibility: criteria\nGate Results: passed\nUnknowns: none identified"
    if slot == "requirements-quality-gate":
        return "Status: passed\nEvidence: EV-1 EV-2 EV-3\nEvidence Citations\nVerdict: passed\nread-only\nResponsibility: review\nGate Results: passed\nUnknowns: none identified"
    return "Status: passed\nEvidence: EV-1\nResponsibility: bounded\nAuthority: supplied\nGate Results: passed\nUnknowns: none identified"


def test_full_loop_executes_all_subrecipes_and_persists_state(tmp_path: Path) -> None:
    full = json.loads((ROOT / "recipes/full-dev-loop.json").read_text(encoding="utf-8"))
    supplied = {key: f"value for {key}" for key in full["inputs"]}
    input_path = tmp_path / "input.json"
    input_path.write_text(json.dumps(supplied), encoding="utf-8")
    calls = []
    def worker(prompt: str, timeout: int) -> str:
        slot = prompt.split("You are executing slot: ", 1)[1].splitlines()[0]
        calls.append(slot)
        return artifact_output(slot)
    def workspace_runner(prompt: str, cwd: Path, tools: list[str], timeout: int):
        slot = prompt.split("You are executing slot: ", 1)[1].splitlines()[0]
        calls.append(slot)
        return artifact_output(slot), []

    result = execute_recipe(
        ROOT / "recipes/full-dev-loop.json", input_path, tmp_path / "run",
        workspace_root=ROOT, worker=worker, state_dir=tmp_path / ".workflow",
        authorization={"workspace-write"}, repository=ROOT,
        workspace_runner=workspace_runner,
    )

    assert result["passed"] is True, result
    assert len(result["steps_run"]) == 6
    assert calls == [
        "problem-framing", "requirements-rules", "acceptance-criteria", "requirements-quality-gate",
        "design-context-and-direction-contract", "tdd-change-loop", "completion-evidence-gate",
        "independent-blackbox-qa", "change-delivery-preflight", "feedback-and-continuous-learning-loop",
    ]
    state = json.loads((tmp_path / ".workflow/state.json").read_text(encoding="utf-8"))
    assert state["status"] == "passed"
    assert len(state["steps"]) == 6
