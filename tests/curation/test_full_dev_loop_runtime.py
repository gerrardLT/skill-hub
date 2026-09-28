import json
from pathlib import Path

from tools.curation.recipe_route import build_catalog, route_request
from tools.curation.recipe_verify import verify_recipes

ROOT = Path(__file__).resolve().parents[2]


def test_all_six_stage_recipes_and_full_loop_are_released_and_verified() -> None:
    report = verify_recipes(ROOT / "recipes", ROOT / "slots", ROOT)
    assert report["ok"] is True, report
    catalog = build_catalog(ROOT / "recipes", ROOT / "slots", ROOT)
    assert {"write-prd", "design-web-flow", "build-feature-tdd", "qa-only", "ship-release", "retro-to-requirements", "full-dev-loop"} <= set(catalog)


def test_full_loop_only_composes_exact_released_subrecipes() -> None:
    full = json.loads((ROOT / "recipes/full-dev-loop.json").read_text(encoding="utf-8"))
    expected = ["write-prd@1.0.0", "design-web-flow@1.0.0", "build-feature-tdd@1.0.0", "qa-only@1.0.0", "ship-release@1.0.0", "retro-to-requirements@1.0.0"]
    assert [step["recipe"] for step in full["steps"]] == expected
    assert all("instructions" not in step and "slot" not in step for step in full["steps"])


def test_retro_feedback_maps_to_next_requirements_input() -> None:
    full = json.loads((ROOT / "recipes/full-dev-loop.json").read_text(encoding="utf-8"))
    assert full["feedback_mappings"] == [{
        "from_step": "retro_to_requirements",
        "to_step": "write_prd",
        "artifact": "next-requirements",
        "target_input": "validated-product-brief",
    }]


def test_qa_is_report_only_in_contract_and_recipe() -> None:
    contract = json.loads((ROOT / "slots/independent-blackbox-qa/contract.json").read_text(encoding="utf-8"))
    recipe = json.loads((ROOT / "recipes/qa-only.json").read_text(encoding="utf-8"))
    assert contract["execution"]["mutation"] == "none"
    assert "write" not in contract["execution"]["tools"]
    assert all(permission not in recipe["permissions"] for permission in ("write", "edit", "remote-git", "deploy"))


def test_ship_release_is_preflight_only_without_remote_or_deploy_permissions() -> None:
    recipe = json.loads((ROOT / "recipes/ship-release.json").read_text(encoding="utf-8"))
    contract = json.loads((ROOT / "slots/change-delivery-preflight/contract.json").read_text(encoding="utf-8"))
    assert all(permission not in recipe["permissions"] for permission in ("remote-git", "network", "merge", "deploy"))
    assert contract["execution"]["mutation"] == "none"
    assert "no merge or deployment action" in contract["outputs"][0]


def test_natural_language_route_is_real_catalog_to_exact_recipe_ref() -> None:
    catalog = build_catalog(ROOT / "recipes", ROOT / "slots", ROOT)
    result = route_request("请运行完整研发闭环", catalog)
    assert result == {"status": "matched", "recipe_ref": "full-dev-loop@1.0.0", "reason": "deterministic-intent"}


def test_only_selected_slots_were_promoted() -> None:
    selection = json.loads((ROOT / "curation/full-dev-loop-slot-selection.json").read_text(encoding="utf-8"))["selected"]
    selected = set(sum(selection.values(), []))
    original = {"problem-framing", "requirements-rules", "acceptance-criteria", "requirements-quality-gate"}
    released = {
        path.parent.name
        for path in (ROOT / "slots").glob("*/contract.json")
        if json.loads(path.read_text(encoding="utf-8"))["status"] == "released"
    }
    assert released == selected | original
