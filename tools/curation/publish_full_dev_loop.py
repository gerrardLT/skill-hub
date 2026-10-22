#!/usr/bin/env python3
"""Publish the verified six-stage closure after release Gate approval."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

from tools.curation.full_dev_loop_release_gate import RECIPES, SLOTS, verify

RUN_RESULTS = {
    "write-prd": "evals/runs/full-dev-loop/ip-rate-limiting-v1/run/write_prd/result.json",
    "design-web-flow": "evals/runs/full-dev-loop/ip-rate-limiting-v1/run/design_web_flow/result.json",
    "build-feature-tdd": "evals/runs/full-dev-loop/ip-rate-limiting-v1/run/build_feature_tdd/result.json",
    "qa-only": "evals/runs/full-dev-loop/ip-rate-limiting-v1/run/qa_only/result.json",
    "ship-release": "evals/runs/full-dev-loop/ip-rate-limiting-v1/run/ship_release/result.json",
    "retro-to-requirements": "evals/runs/full-dev-loop/ip-rate-limiting-v1/run/retro_to_requirements/result.json",
    "full-dev-loop": "evals/runs/full-dev-loop/ip-rate-limiting-v1/run/result.json",
}
REVIEW = "evals/runs/full-dev-loop/ip-rate-limiting-v1/human-review.json"

def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def write(path: Path, value: object) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

def publish(workspace: Path) -> dict:
    gate = verify(workspace)
    if not gate["ok"]:
        return {"gate": "publish-full-dev-loop", "ok": False, "errors": gate["errors"]}
    evidence_root = "evals/runs/full-dev-loop/ip-rate-limiting-v1/slot-evaluations"
    status_path = workspace / "curation/slot-release-status.json"
    status = json.loads(status_path.read_text(encoding="utf-8"))
    by_id = {item["slot_id"]: item for item in status["items"]}
    queue_path = workspace / "curation/slot-review-queue.json"
    queue = json.loads(queue_path.read_text(encoding="utf-8"))
    for slot_id in sorted(SLOTS):
        contract_path = workspace / "slots" / slot_id / "contract.json"
        provenance_path = workspace / "slots" / slot_id / "provenance.json"
        contract = json.loads(contract_path.read_text(encoding="utf-8")); contract["status"] = "released"; write(contract_path, contract)
        evidence = [f"{evidence_root}/{slot_id}/{suite}.json" for suite in ("baseline", "candidate", "holdout", "mutation")]
        provenance = json.loads(provenance_path.read_text(encoding="utf-8"))
        provenance.update(status="released", evaluation={"semantic": "approved", "status": "passed", "case_id": "mirrormind-ip-rate-limiting-v1"}, release_evidence=evidence)
        write(provenance_path, provenance)
        skill = workspace / "slots" / slot_id / "SKILL.md"
        skill.write_text(skill.read_text(encoding="utf-8").replace("Status: evaluating 1.0.0", "Status: released 1.0.0"), encoding="utf-8")
        item = by_id[slot_id]
        item.update(disposition="released", materialization_status="released", blocking_gaps=[], reason="real full-dev-loop evaluation and human semantic review passed", evaluation_references=evidence, release_evidence=evidence, review={"human_review": REVIEW})
    for item in queue.get("items", []):
        if item.get("slot_id") in SLOTS:
            item["review_status"] = "approved"
    write(status_path, status); write(queue_path, queue)

    candidates = workspace / "evals/candidates/full-dev-loop/recipes"
    review_path = workspace / REVIEW
    for recipe_id in sorted(RECIPES):
        recipe = json.loads((candidates / f"{recipe_id}.json").read_text(encoding="utf-8"))
        result_path = workspace / RUN_RESULTS[recipe_id]
        recipe["status"] = "released"
        recipe["evidence"] = {
            "composition_runs": [{"path": RUN_RESULTS[recipe_id], "sha256": sha(result_path)}],
            "review": {"path": REVIEW, "sha256": sha(review_path)},
        }
        write(workspace / "recipes" / f"{recipe_id}.json", recipe)
    catalog = json.loads((workspace / "recipes/catalog.json").read_text(encoding="utf-8"))
    catalog["recipes"] = sorted(["requirements-to-acceptance-criteria@0.2.0", *(f"{recipe}@1.0.0" for recipe in RECIPES)])
    write(workspace / "recipes/catalog.json", catalog)
    return {"gate": "publish-full-dev-loop", "ok": True, "released_slots": len(SLOTS), "released_recipes": len(RECIPES), "errors": []}

if __name__ == "__main__":
    result = publish(Path(".").resolve()); print(json.dumps(result, ensure_ascii=False, sort_keys=True)); raise SystemExit(0 if result["ok"] else 1)
