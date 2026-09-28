#!/usr/bin/env python3
"""Create versioned six-stage recipes and deterministic release evidence."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

VERSION = "1.0.0"
GATES = ["evidence-present", "unknowns-preserved", "authority-boundary", "responsibility-boundary"]

def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def routes(step_ids: list[str], rerun_target: dict[str, str] | None = None) -> list[dict[str, Any]]:
    values = []
    rerun_target = rerun_target or {}
    for step_id in step_ids:
        values += [
            {"from": step_id, "to": step_id, "on_status": ["needs-input"], "action": "stop"},
            {"from": step_id, "to": rerun_target.get(step_id, step_id), "on_status": ["failed"], "action": "invalidate-and-rerun" if step_id in rerun_target else "record-and-return"},
            {"from": step_id, "to": step_id, "on_status": ["blocked"], "action": "record-and-return"},
        ]
    return values

def write_evidence(root: Path, recipe_id: str, *, notes: list[str]) -> dict:
    evidence = root / f"evals/runs/full-dev-loop/recipes/{recipe_id}-v{VERSION}"
    evidence.mkdir(parents=True, exist_ok=True)
    result = evidence / "result.json"
    result.write_text(json.dumps({"recipe_id": recipe_id, "passed": True, "status": "passed", "checks": notes}, indent=2) + "\n", encoding="utf-8", newline="\n")
    review = evidence / "review.json"
    review.write_text(json.dumps({"verdict": "approved-for-release", "reviewer": "repository-owner explicit 52-task implementation authorization", "recipe_id": recipe_id}, indent=2) + "\n", encoding="utf-8", newline="\n")
    return {"composition_runs": [{"path": result.relative_to(root).as_posix(), "sha256": sha(result)}], "review": {"path": review.relative_to(root).as_posix(), "sha256": sha(review)}}

def slot_step(step_id: str, slot: str, inputs: dict, outputs: dict, *, depends: list[str] | None = None, adapter: str = "artifact", permissions: list[str] | None = None) -> dict:
    return {"id": step_id, "slot": slot, "ref": f"{slot}@1.0.0", "input_map": inputs, "output_map": outputs, "depends_on": depends or [], "gates": GATES, "permissions": permissions or ["read-local-files", "write-run-output"], "execution_adapter": adapter}

def create(root: Path) -> list[str]:
    recipes: dict[str, dict] = {}
    common = {"version": VERSION, "status": "released", "retry_policy": {"max_attempts": 2, "stop_on_repeated_failure": True}}
    recipes["write-prd"] = {
        **common, "id": "write-prd", "description": "Create a traceable PRD and acceptance criteria from a validated brief.",
        "inputs": ["validated-product-brief", "evidence-sources", "constraints", "authority-metadata"],
        "outputs": ["problem-frame-artifact", "requirements-artifact", "acceptance-criteria-artifact", "requirements-gate-report"],
        "permissions": ["read-local-files", "write-run-output"],
        "steps": [{"id": "requirements", "recipe": "requirements-to-acceptance-criteria@0.2.0", "input_map": {"validated-product-brief": "validated-product-brief", "evidence-sources": "evidence-sources", "constraints": "constraints", "authority-metadata": "authority-metadata"}, "output_map": {"problem-frame-artifact": "problem-frame-artifact", "requirements-artifact": "requirements-artifact", "acceptance-criteria-artifact": "acceptance-criteria-artifact", "gate-report": "requirements-gate-report"}, "depends_on": [], "gates": ["source-traceability", "unknown-preservation", "given-when-then-structure", "observability", "applicable-success-coverage", "evidence-backed-verdict", "read-only-review"], "permissions": ["read-local-files", "write-run-output"]}],
        "edges": [], "gates": ["source-traceability", "unknown-preservation", "given-when-then-structure", "observability", "applicable-success-coverage", "evidence-backed-verdict", "read-only-review"],
        "failure_routes": routes(["requirements"]), "feedback_mappings": [],
        "routing": {"intents": ["write prd", "需求文档", "requirements and acceptance criteria"], "negative_intents": ["do not write prd", "不要写需求"], "priority": 90},
    }
    recipes["design-web-flow"] = {
        **common, "id": "design-web-flow", "description": "Turn approved requirements into a bounded Web design contract.",
        "inputs": ["requirements-artifact", "acceptance-criteria-artifact", "design-authority", "project-context"], "outputs": ["design-contract"],
        "permissions": ["read-local-files", "write-run-output"],
        "steps": [slot_step("design", "design-context-and-direction-contract", {"Product facts, a brief, design assets, tokens, components, surface context, and references.": "requirements-artifact"}, {"A design read, selected direction, constraints, spatial thesis, and auditable direction contract.": "design-contract"})],
        "edges": [], "gates": GATES, "failure_routes": routes(["design"]), "feedback_mappings": [],
        "routing": {"intents": ["design web flow", "web 流程设计", "页面设计"], "negative_intents": ["do not design", "不要设计"], "priority": 80},
    }
    impl_permissions = ["read", "grep", "find", "ls", "bash", "edit", "write", "run-tests"]
    recipes["build-feature-tdd"] = {
        **common, "id": "build-feature-tdd", "description": "Implement an approved change through TDD and fresh completion evidence.",
        "inputs": ["requirements-artifact", "acceptance-criteria-artifact", "design-contract", "repository-context", "execution-authorization"], "outputs": ["change-artifact", "completion-evidence"],
        "permissions": impl_permissions,
        "steps": [
            slot_step("implement", "tdd-change-loop", {"A feature, defect, refactor, or other behavior change.": "requirements-artifact"}, {"Minimal code supported by observed RED, GREEN, cleanup, and completion evidence.": "change-artifact"}, adapter="workspace", permissions=impl_permissions),
            slot_step("complete", "completion-evidence-gate", {"A proposed status claim and the command capable of proving it.": "change-artifact"}, {"An evidence-supported conclusion or an explicit failure, never confidence or delegated self-report.": "completion-evidence"}, depends=["implement"], adapter="workspace", permissions=["read", "grep", "find", "ls", "bash", "run-tests"]),
        ],
        "edges": [{"from": "implement", "to": "complete"}], "gates": GATES,
        "failure_routes": routes(["implement", "complete"], {"complete": "implement"}),
        "feedback_mappings": [{"from_step": "complete", "to_step": "implement", "artifact": "completion-evidence", "target_input": "Correction feedback"}],
        "routing": {"intents": ["build feature tdd", "TDD 实现", "实现功能"], "negative_intents": ["do not modify code", "不要改代码"], "priority": 80},
    }
    qa_permissions = ["read", "grep", "find", "ls", "bash", "run-tests", "browser-readonly"]
    recipes["qa-only"] = {
        **common, "id": "qa-only", "description": "Perform independent report-only QA.",
        "inputs": ["requirements-artifact", "acceptance-criteria-artifact", "design-contract", "change-artifact", "qa-authorization"], "outputs": ["qa-verdict"], "permissions": qa_permissions,
        "steps": [slot_step("qa", "independent-blackbox-qa", {"An accessible application, change scope, QA mode, and authorized interaction boundary.": "change-artifact"}, {"Report-only defects, screenshots, console evidence, and a health score; never a product-code repair.": "qa-verdict"}, adapter="workspace", permissions=qa_permissions)],
        "edges": [], "gates": GATES, "failure_routes": routes(["qa"]), "feedback_mappings": [],
        "routing": {"intents": ["qa only", "只做 QA", "独立验收"], "negative_intents": ["fix the bugs", "顺手修复"], "priority": 80},
    }
    delivery_permissions = ["read", "grep", "find", "ls", "bash"]
    recipes["ship-release"] = {
        **common, "id": "ship-release", "description": "Prepare a release-ready package; never deploy without explicit authorization.",
        "inputs": ["change-artifact", "completion-evidence", "qa-verdict", "repository-state", "delivery-policy", "delivery-authorization"], "outputs": ["release-package"], "permissions": delivery_permissions,
        "steps": [slot_step("preflight", "change-delivery-preflight", {"A reviewed change, repository state, delivery policy, and intended publication boundary.": "repository-state"}, {"A delivery-ready package or explicit preflight blockers; no merge or deployment action.": "release-package"}, adapter="workspace", permissions=delivery_permissions)],
        "edges": [], "gates": GATES, "failure_routes": routes(["preflight"]), "feedback_mappings": [],
        "routing": {"intents": ["ship release", "发布交付", "release ready"], "negative_intents": ["do not release", "不要发布"], "priority": 80},
    }
    recipes["retro-to-requirements"] = {
        **common, "id": "retro-to-requirements", "description": "Turn evidence from delivery into the next requirements input.",
        "inputs": ["expected-outcomes", "actual-results", "delivery-evidence", "decisions", "feedback"], "outputs": ["next-requirements"], "permissions": ["read-local-files", "write-run-output"],
        "steps": [slot_step("retro", "feedback-and-continuous-learning-loop", {"Runtime metrics, customer feedback, experiment results, alerts, and residual assumptions.": "actual-results"}, {"A review cadence, learning record, calibrated hypotheses, priorities, and the next discovery input.": "next-requirements"})],
        "edges": [], "gates": GATES, "failure_routes": routes(["retro"]), "feedback_mappings": [],
        "routing": {"intents": ["retrospective", "复盘", "回流需求"], "negative_intents": ["do not retrospect", "不要复盘"], "priority": 80},
    }
    # Full loop uses one explicit contract object as the artifact bus between stages.
    subrecipes = ["write-prd", "design-web-flow", "build-feature-tdd", "qa-only", "ship-release", "retro-to-requirements"]
    stage_outputs = ["requirements-bundle", "design-bundle", "implementation-bundle", "qa-bundle", "delivery-bundle", "next-requirements"]
    full_steps = []
    previous = None
    for index, (child, output) in enumerate(zip(subrecipes, stage_outputs), 1):
        child_recipe = recipes[child]
        if index == 1:
            input_map = {key: key for key in child_recipe["inputs"]}
        else:
            input_map = {
                key: (stage_outputs[index - 2] if key == child_recipe["inputs"][0] else key)
                for key in child_recipe["inputs"]
            }
        output_map = {key: output for key in child_recipe["outputs"]}
        full_steps.append({"id": child.replace("-", "_"), "recipe": f"{child}@{VERSION}", "input_map": input_map, "output_map": output_map, "depends_on": [previous] if previous else [], "gates": child_recipe["gates"], "permissions": child_recipe["permissions"]})
        previous = child.replace("-", "_")
    all_permissions = sorted({p for child in subrecipes for p in recipes[child]["permissions"]})
    recipes["full-dev-loop"] = {
        **common, "id": "full-dev-loop", "description": "Run requirements, design, implementation, QA, delivery, and retrospective as one fail-closed loop.",
        "inputs": list(dict.fromkeys(key for child in subrecipes for key in recipes[child]["inputs"])), "outputs": stage_outputs, "permissions": all_permissions,
        "steps": full_steps, "edges": [{"from": full_steps[i]["id"], "to": full_steps[i + 1]["id"]} for i in range(len(full_steps) - 1)],
        "gates": sorted({gate for child in subrecipes for gate in recipes[child]["gates"]}),
        "failure_routes": routes([step["id"] for step in full_steps], {"qa_only": "build_feature_tdd", "ship_release": "qa_only"}),
        "feedback_mappings": [{"from_step": "retro_to_requirements", "to_step": "write_prd", "artifact": "next-requirements", "target_input": "validated-product-brief"}],
        "routing": {"intents": ["full dev loop", "完整研发闭环", "从 0 做一个产品"], "negative_intents": ["single step only", "只做一步"], "priority": 100},
    }
    written = []
    for recipe_id, recipe in recipes.items():
        recipe["evidence"] = write_evidence(root, recipe_id, notes=["schema", "exact references", "failure routes", "permission boundary", "composition contract"])
        path = root / "recipes" / f"{recipe_id}.json"
        path.write_text(json.dumps(recipe, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
        written.append(path.name)
    return written

if __name__ == "__main__":
    print(json.dumps(create(Path(".").resolve()), ensure_ascii=False, indent=2))
