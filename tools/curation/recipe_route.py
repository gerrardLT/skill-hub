#!/usr/bin/env python3
"""Route requests only to released recipes; ambiguity always needs input."""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any, Callable

try:
    from tools.curation.recipe_verify import verify_recipes
    from tools.curation.workflow_state import StateError, load_state
except ModuleNotFoundError:  # direct script execution
    from recipe_verify import verify_recipes
    from workflow_state import StateError, load_state

TOKEN_RE = re.compile(r"[a-z0-9][a-z0-9-]*|[\u4e00-\u9fff]+", re.IGNORECASE)


def build_catalog(recipes_root: Path, slots_root: Path, workspace_root: Path) -> dict[str, dict[str, Any]]:
    verification = verify_recipes(recipes_root, slots_root, workspace_root)
    if not verification["ok"]:
        raise ValueError("recipe catalog verification failed")
    catalog: dict[str, dict[str, Any]] = {}
    for path in sorted(recipes_root.glob("*.json")):
        if path.stem in {"schema", "catalog"}:
            continue
        recipe = json.loads(path.read_text(encoding="utf-8"))
        if recipe.get("status") == "released":
            catalog[recipe["id"]] = recipe
    return catalog


def model_schema(catalog: dict[str, dict[str, Any]]) -> dict[str, Any]:
    return {
        "type": "object",
        "additionalProperties": False,
        "required": ["status", "recipe_id", "confidence", "reason"],
        "properties": {
            "status": {"enum": ["matched", "needs-input"]},
            "recipe_id": {"type": ["string", "null"], "enum": [None, *sorted(catalog)]},
            "confidence": {"type": "number", "minimum": 0, "maximum": 1},
            "reason": {"type": "string"},
        },
    }


def _tokens(text: str) -> set[str]:
    return {token.casefold() for token in TOKEN_RE.findall(text)}


def _deterministic_matches(intent: str, catalog: dict[str, dict[str, Any]]) -> list[tuple[int, int, str]]:
    folded = intent.casefold()
    request_tokens = _tokens(intent)
    matches: list[tuple[int, int, str]] = []
    for recipe_id, recipe in catalog.items():
        routing = recipe.get("routing", {})
        if any(phrase.casefold() in folded for phrase in routing.get("negative_intents", [])):
            continue
        score = 0
        for phrase in routing.get("intents", []):
            phrase_folded = phrase.casefold()
            if phrase_folded in folded:
                score += 10 + len(_tokens(phrase))
            else:
                score += len(request_tokens & _tokens(phrase))
        if score:
            matches.append((score, int(routing.get("priority", 0)), recipe_id))
    return sorted(matches, reverse=True)


def route_request(
    intent: str,
    catalog: dict[str, dict[str, Any]],
    *,
    explicit_ref: str | None = None,
    state_dir: Path | None = None,
    model_router: Callable[[str, dict[str, Any]], dict[str, Any]] | None = None,
) -> dict[str, Any]:
    if explicit_ref:
        recipe_id, _, version = explicit_ref.partition("@")
        recipe = catalog.get(recipe_id)
        if recipe is None or not version or recipe.get("version") != version:
            return {"status": "blocked", "recipe_ref": None, "reason": "explicit recipe is not released"}
        return {"status": "matched", "recipe_ref": explicit_ref, "reason": "explicit-recipe"}

    if state_dir is not None:
        try:
            state = load_state(state_dir)
        except StateError as exc:
            return {"status": "blocked", "recipe_ref": None, "reason": str(exc)}
        if state and state.get("status") not in {"passed", "failed", "blocked"}:
            recipe_id, _, version = state["recipe_ref"].partition("@")
            recipe = catalog.get(recipe_id)
            if recipe and recipe.get("version") == version:
                return {"status": "matched", "recipe_ref": state["recipe_ref"], "reason": "resumable-state"}
            return {"status": "blocked", "recipe_ref": None, "reason": "state references unreleased recipe"}

    matches = _deterministic_matches(intent, catalog)
    if matches:
        explicit_phrase_matches = [
            recipe_id
            for recipe_id, recipe in catalog.items()
            if any(phrase.casefold() in intent.casefold() for phrase in recipe.get("routing", {}).get("intents", []))
            and not any(phrase.casefold() in intent.casefold() for phrase in recipe.get("routing", {}).get("negative_intents", []))
        ]
        best = matches[0]
        peers = [match for match in matches if match[:2] == best[:2]]
        if len(explicit_phrase_matches) <= 1 and len(peers) == 1 and (len(matches) == 1 or best[0] > matches[1][0]):
            recipe = catalog[best[2]]
            return {"status": "matched", "recipe_ref": f"{best[2]}@{recipe['version']}", "reason": "deterministic-intent"}

    if model_router is not None:
        candidate_ids = sorted({item[2] for item in matches} or catalog)
        restricted = {recipe_id: catalog[recipe_id] for recipe_id in candidate_ids}
        answer = model_router(intent, model_schema(restricted))
        recipe_id = answer.get("recipe_id") if isinstance(answer, dict) else None
        if answer.get("status") == "matched" and recipe_id in restricted and answer.get("confidence", 0) >= 0.85:
            recipe = restricted[recipe_id]
            return {"status": "matched", "recipe_ref": f"{recipe_id}@{recipe['version']}", "reason": "structured-model"}

    choices = [f"{recipe_id}@{catalog[recipe_id]['version']}" for recipe_id in sorted({item[2] for item in matches} or catalog)]
    return {"status": "needs-input", "recipe_ref": None, "reason": "ambiguous-or-unmatched", "choices": choices}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("intent")
    parser.add_argument("--recipes-root", type=Path, default=Path("recipes"))
    parser.add_argument("--slots-root", type=Path, default=Path("slots"))
    parser.add_argument("--workspace-root", type=Path, default=Path("."))
    parser.add_argument("--recipe")
    parser.add_argument("--state-dir", type=Path)
    args = parser.parse_args()
    try:
        catalog = build_catalog(args.recipes_root, args.slots_root, args.workspace_root)
    except ValueError as exc:
        print(json.dumps({"status": "blocked", "reason": str(exc)}))
        return 1
    result = route_request(args.intent, catalog, explicit_ref=args.recipe, state_dir=args.state_dir)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["status"] == "matched" else 1

if __name__ == "__main__":
    raise SystemExit(main())
