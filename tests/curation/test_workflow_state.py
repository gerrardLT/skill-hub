import json
from pathlib import Path

import pytest

from tools.curation.workflow_state import StateError, load_state, new_state, save_state


def test_initial_state_round_trip_and_markdown_view(tmp_path: Path) -> None:
    state = new_state("demo", "build it", "full-dev-loop@1.0.0")
    state["steps"].append({
        "step_id": "requirements",
        "ref": "write-prd@1.0.0",
        "status": "passed",
        "input_sha256": "a" * 64,
        "artifacts": ["runs/requirements.md"],
        "evidence": ["runs/requirements.json"],
        "attempts": 1,
    })

    save_state(tmp_path / ".workflow", state)
    loaded = load_state(tmp_path / ".workflow")

    assert loaded is not None
    assert loaded["steps"][0]["ref"] == "write-prd@1.0.0"
    markdown = (tmp_path / ".workflow/state.md").read_text(encoding="utf-8")
    assert "recipe: full-dev-loop@1.0.0" in markdown
    assert "requirements: write-prd@1.0.0 | passed" in markdown


def test_missing_state_is_a_clean_first_run(tmp_path: Path) -> None:
    assert load_state(tmp_path / ".workflow") is None


def test_corrupt_state_is_preserved_and_blocks(tmp_path: Path) -> None:
    workflow = tmp_path / ".workflow"
    workflow.mkdir()
    (workflow / "state.json").write_text("{broken", encoding="utf-8")

    with pytest.raises(StateError):
        load_state(workflow)

    assert list(workflow.glob("state.corrupt-*.json"))
    assert (workflow / "state.json").read_text(encoding="utf-8") == "{broken"


def test_unsupported_state_version_blocks_without_migration_guess(tmp_path: Path) -> None:
    workflow = tmp_path / ".workflow"
    workflow.mkdir()
    state = new_state("demo", "resume", "write-prd@1.0.0")
    state["schema_version"] = "0.1"
    (workflow / "state.json").write_text(json.dumps(state), encoding="utf-8")

    with pytest.raises(StateError, match="unsupported state version"):
        load_state(workflow)
