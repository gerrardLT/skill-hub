import json
from pathlib import Path

from tools.curation.recipe_route import build_catalog, route_request
from tools.curation.recipe_verify import verify_recipes

ROOT = Path(__file__).resolve().parents[2]


def test_six_stage_recipes_are_released_only_after_real_evaluations() -> None:
    report = verify_recipes(ROOT / "recipes", ROOT / "slots", ROOT)
    assert report["ok"] is True, report
    catalog = build_catalog(ROOT / "recipes", ROOT / "slots", ROOT)
    expected = {"requirements-to-acceptance-criteria", "write-prd", "design-web-flow", "build-feature-tdd", "qa-only", "ship-release", "retro-to-requirements", "full-dev-loop"}
    assert set(catalog) == expected
    assert all(json.loads(path.read_text(encoding="utf-8"))["status"] == "released" for path in (ROOT / "recipes").glob("*.json") if path.stem not in {"schema", "catalog"})


def test_full_loop_only_composes_exact_released_subrecipes() -> None:
    full = json.loads((ROOT / "evals/candidates/full-dev-loop/recipes/full-dev-loop.json").read_text(encoding="utf-8"))
    expected = ["write-prd@1.0.0", "design-web-flow@1.0.0", "build-feature-tdd@1.0.0", "qa-only@1.0.0", "ship-release@1.0.0", "retro-to-requirements@1.0.0"]
    assert [step["recipe"] for step in full["steps"]] == expected
    assert all("instructions" not in step and "slot" not in step for step in full["steps"])


def test_retro_feedback_maps_to_next_requirements_input() -> None:
    full = json.loads((ROOT / "evals/candidates/full-dev-loop/recipes/full-dev-loop.json").read_text(encoding="utf-8"))
    assert {
        "from_step": "retro_to_requirements",
        "to_step": "write_prd",
        "artifact": "next-requirements",
        "target_input": "validated-product-brief",
    } in full["feedback_mappings"]
    assert {
        "from_step": "qa_only",
        "to_step": "build_feature_tdd",
        "artifact": "qa-verdict",
        "target_input": "Correction feedback",
    } in full["feedback_mappings"]


def test_qa_is_report_only_in_contract_and_recipe() -> None:
    contract = json.loads((ROOT / "slots/independent-blackbox-qa/contract.json").read_text(encoding="utf-8"))
    recipe = json.loads((ROOT / "evals/candidates/full-dev-loop/recipes/qa-only.json").read_text(encoding="utf-8"))
    assert contract["execution"]["mutation"] == "none"
    assert "write" not in contract["execution"]["tools"]
    assert all(permission not in recipe["permissions"] for permission in ("write", "edit", "remote-git", "deploy"))


def test_ship_release_is_preflight_only_without_remote_or_deploy_permissions() -> None:
    recipe = json.loads((ROOT / "evals/candidates/full-dev-loop/recipes/ship-release.json").read_text(encoding="utf-8"))
    contract = json.loads((ROOT / "slots/change-delivery-preflight/contract.json").read_text(encoding="utf-8"))
    assert all(permission not in recipe["permissions"] for permission in ("remote-git", "network", "merge", "deploy"))
    assert contract["execution"]["mutation"] == "none"
    assert {"remote-git", "network", "merge", "deploy"} <= set(contract["permissions"]["explicitly_denied"])


def test_released_full_loop_routes_to_exact_version() -> None:
    catalog = build_catalog(ROOT / "recipes", ROOT / "slots", ROOT)
    result = route_request("请运行完整研发闭环", catalog, explicit_ref="full-dev-loop@1.0.0")
    assert result == {"status": "matched", "recipe_ref": "full-dev-loop@1.0.0", "reason": "explicit-recipe"}


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
