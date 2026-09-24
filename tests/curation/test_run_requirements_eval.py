import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from tools.curation.run_requirements_eval import load_cases, prompt_for


def test_prompt_is_self_contained_and_offline(tmp_path: Path) -> None:
    material = tmp_path / "SKILL.md"
    material.write_text("# Method\nPreserve unknowns.\n", encoding="utf-8")
    case = {"id": "case-1", "prompt": "Draft observable criteria."}

    prompt = prompt_for(case, [material], "candidate")

    assert "Do not use tools, network, repository context" in prompt
    assert "Draft observable criteria." in prompt
    assert "Preserve unknowns." in prompt
    assert "Status: needs-input" in prompt


def test_load_cases_requires_array(tmp_path: Path) -> None:
    path = tmp_path / "cases.json"
    path.write_text('{"cases": [{"id": "one", "prompt": "x"}]}', encoding="utf-8")

    assert load_cases(path)[0]["id"] == "one"
