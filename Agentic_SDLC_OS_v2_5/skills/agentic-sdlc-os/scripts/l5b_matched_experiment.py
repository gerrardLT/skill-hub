#!/usr/bin/env python3
"""Preregistered matched-pair L5-B evaluation for Agentic SDLC OS.

The harness controls task identity, assignment order, model/tool budgets, blind review,
record integrity and paired uncertainty. Synthetic results are never treated as evidence.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import random
import tempfile
import uuid
from datetime import datetime, timezone
from pathlib import Path
from statistics import mean, median
from typing import Any

VERSION = "2.3"
ARMS = {"baseline", "sdlc"}
METRICS: dict[str, dict[str, Any]] = {
    "lead_time_minutes": {"direction": "lower", "category": "cycle", "min": 0.0},
    "human_minutes": {"direction": "lower", "category": "effort", "min": 0.0},
    "token_cost_usd": {"direction": "lower", "category": "cost", "min": 0.0},
    "rework_fraction": {"direction": "lower", "category": "rework", "min": 0.0, "max": 1.0},
    "escaped_defects": {"direction": "lower", "category": "quality", "min": 0.0},
    "critical_defects": {"direction": "lower", "category": "quality", "min": 0.0},
    "trace_coverage": {"direction": "higher", "category": "traceability", "min": 0.0, "max": 1.0},
    "acceptance_pass_rate": {"direction": "higher", "category": "outcome", "min": 0.0, "max": 1.0},
    "maintainability_score": {"direction": "higher", "category": "quality", "min": 0.0, "max": 10.0},
}
PRIMARY_CATEGORIES = {"cycle", "rework", "quality", "traceability", "outcome"}


def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def canonical(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value).encode("utf-8")).hexdigest()


def atomic_write(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temp = tempfile.mkstemp(prefix=f".{path.name}.", dir=str(path.parent))
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            json.dump(payload, handle, indent=2)
            handle.write("\n")
        os.replace(temp, path)
    finally:
        if os.path.exists(temp):
            os.unlink(temp)


def load(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise RuntimeError("Experiment file must contain an object")
    return payload


def new_experiment(project: str, target_pairs: int, seed: int, hypothesis: str, synthetic: bool) -> dict[str, Any]:
    if target_pairs < 3:
        raise RuntimeError("target_pairs must be at least 3; 5 or more is recommended")
    return {
        "schema_version": VERSION,
        "experiment_id": f"l5b-{uuid.uuid4().hex}",
        "project": project,
        "target_pairs": target_pairs,
        "randomization_seed": seed,
        "hypothesis": hypothesis,
        "synthetic": synthetic,
        "created_at": now(),
        "frozen_at": None,
        "preregistration_hash": None,
        "protocol": {
            "design": "matched-pair randomized-order crossover",
            "same_task": True,
            "same_model_family": True,
            "same_tool_access": True,
            "same_time_budget": True,
            "blind_review": True,
            "independent_execution_contexts": True,
            "identical_start_state": True,
            "same_model_exact": True,
            "same_toolset_hash": True,
            "balanced_order": True,
            "complete_blind_review": True,
            "independent_reviewer": True,
            "seal_required_for_formal_evidence": True,
            "minimum_effect": 0.05,
            "bootstrap_samples": 5000,
            "decision_rule": "Positive only when at least two primary categories improve by >=5%, at least one has a 95% paired bootstrap CI above zero, and no severe quality/outcome regression exists.",
        },
        "metrics": METRICS,
        "tasks": [],
        "assignments": [],
        "runs": [],
        "reviews": [],
        "record_chain_head": "GENESIS",
        "analysis_history": [],
        "sealed_at": None,
        "seal_hash": None,
    }


def require_mutable(exp: dict[str, Any]) -> None:
    if exp.get("frozen_at"):
        raise RuntimeError("Preregistration is frozen; task or protocol changes are prohibited")


def add_task(exp: dict[str, Any], task_id: str, task_hash: str, domain: str, complexity: int, time_budget_minutes: int) -> None:
    require_mutable(exp)
    if any(item["task_id"] == task_id for item in exp["tasks"]):
        raise RuntimeError(f"Duplicate task_id: {task_id}")
    if not re_hex(task_hash):
        raise RuntimeError("task_hash must be a SHA-256 hex digest")
    if complexity < 1 or complexity > 5:
        raise RuntimeError("complexity must be between 1 and 5")
    if time_budget_minutes <= 0:
        raise RuntimeError("time_budget_minutes must be positive")
    exp["tasks"].append({
        "task_id": task_id, "task_hash": task_hash, "domain": domain,
        "complexity": complexity, "time_budget_minutes": time_budget_minutes,
    })


def re_hex(value: str) -> bool:
    return len(value) == 64 and all(ch in "0123456789abcdef" for ch in value.lower())


def freeze(exp: dict[str, Any]) -> None:
    require_mutable(exp)
    if len(exp["tasks"]) != int(exp["target_pairs"]):
        raise RuntimeError(f"Expected exactly {exp['target_pairs']} tasks before freeze")
    rng = random.Random(int(exp["randomization_seed"]))
    tasks = sorted(exp["tasks"], key=lambda item: item["task_id"])
    baseline_first = (len(tasks) + 1) // 2
    orders = [["baseline", "sdlc"] for _ in range(baseline_first)] + [["sdlc", "baseline"] for _ in range(len(tasks) - baseline_first)]
    rng.shuffle(orders)
    assignments = []
    for task, order in zip(tasks, orders):
        codes = {arm: f"artifact-{uuid.UUID(int=rng.getrandbits(128)).hex[:12]}" for arm in ARMS}
        assignments.append({"task_id": task["task_id"], "order": order, "blind_artifact_codes": codes})
    exp["assignments"] = assignments
    exp["frozen_at"] = now()
    prereg = {key: exp[key] for key in ["schema_version", "experiment_id", "project", "target_pairs", "randomization_seed", "hypothesis", "synthetic", "protocol", "metrics", "tasks", "assignments", "frozen_at"]}
    exp["preregistration_hash"] = digest(prereg)


def assignment_for(exp: dict[str, Any], task_id: str) -> dict[str, Any]:
    for item in exp.get("assignments", []):
        if item["task_id"] == task_id:
            return item
    raise RuntimeError(f"Unknown or unassigned task: {task_id}")


def validate_metric(name: str, value: float) -> float:
    spec = METRICS[name]
    number = float(value)
    if not math.isfinite(number) or number < float(spec["min"]):
        raise RuntimeError(f"Invalid metric {name}: {value}")
    if "max" in spec and number > float(spec["max"]):
        raise RuntimeError(f"Invalid metric {name}: {value}")
    return number


def append_chained_record(exp: dict[str, Any], record: dict[str, Any]) -> None:
    record["previous_hash"] = exp.get("record_chain_head", "GENESIS")
    record["record_hash"] = digest({k: v for k, v in record.items() if k != "record_hash"})
    exp["record_chain_head"] = record["record_hash"]
    exp["runs"].append(record)


def record_run(exp: dict[str, Any], *, task_id: str, arm: str, executor_code: str, execution_context_id: str, model: str, prompt_hash: str, toolset_hash: str, start_state_hash: str, environment_hash: str, artifact_hash: str, run_log_hash: str, metrics: dict[str, float], contamination: str = "none") -> None:
    if exp.get("sealed_at"):
        raise RuntimeError("Experiment is sealed; runs cannot be changed")
    if not exp.get("frozen_at"):
        raise RuntimeError("Freeze the preregistration before recording runs")
    if arm not in ARMS:
        raise RuntimeError(f"Invalid arm: {arm}")
    assignment = assignment_for(exp, task_id)
    task_runs = [item for item in exp["runs"] if item["task_id"] == task_id]
    if any(item["arm"] == arm for item in task_runs):
        raise RuntimeError(f"Duplicate run: {task_id}/{arm}")
    if len(task_runs) >= len(assignment["order"]) or assignment["order"][len(task_runs)] != arm:
        expected = assignment["order"][len(task_runs)] if len(task_runs) < len(assignment["order"]) else "none"
        raise RuntimeError(f"Run order violation for {task_id}: expected {expected}, got {arm}")
    if not execution_context_id.strip():
        raise RuntimeError("execution_context_id is required")
    if any(item.get("execution_context_id") == execution_context_id for item in exp["runs"]):
        raise RuntimeError("execution_context_id must be unique per run")
    for name, value in {
        "prompt_hash": prompt_hash,
        "toolset_hash": toolset_hash,
        "start_state_hash": start_state_hash,
        "environment_hash": environment_hash,
        "artifact_hash": artifact_hash,
        "run_log_hash": run_log_hash,
    }.items():
        if not re_hex(value):
            raise RuntimeError(f"{name} must be a SHA-256 hex digest")
    normalized = {name: validate_metric(name, metrics[name]) for name in METRICS}
    append_chained_record(exp, {
        "task_id": task_id,
        "arm": arm,
        "blind_artifact_code": assignment["blind_artifact_codes"][arm],
        "executor_code": executor_code,
        "execution_context_id": execution_context_id,
        "model": model,
        "prompt_hash": prompt_hash,
        "toolset_hash": toolset_hash,
        "start_state_hash": start_state_hash,
        "environment_hash": environment_hash,
        "artifact_hash": artifact_hash,
        "run_log_hash": run_log_hash,
        "metrics": normalized,
        "contamination": contamination,
        "recorded_at": now(),
    })


def add_review(exp: dict[str, Any], *, blind_artifact_code: str, reviewer_code: str, correctness: float, completeness: float, maintainability: float, usability: float, notes: str = "") -> None:
    if exp.get("sealed_at"):
        raise RuntimeError("Experiment is sealed; reviews cannot be changed")
    valid_codes = {code for assignment in exp.get("assignments", []) for code in assignment["blind_artifact_codes"].values()}
    if blind_artifact_code not in valid_codes:
        raise RuntimeError("Unknown blind artifact code")
    if any(item["blind_artifact_code"] == blind_artifact_code and item["reviewer_code"] == reviewer_code for item in exp["reviews"]):
        raise RuntimeError("Duplicate blind review")
    scores = {"correctness": correctness, "completeness": completeness, "maintainability": maintainability, "usability": usability}
    if any(float(value) < 0 or float(value) > 10 for value in scores.values()):
        raise RuntimeError("Review scores must be between 0 and 10")
    exp["reviews"].append({"blind_artifact_code": blind_artifact_code, "reviewer_code": reviewer_code, **{key: float(value) for key, value in scores.items()}, "notes": notes, "recorded_at": now()})


def relative_improvement(baseline: float, sdlc: float, direction: str) -> float:
    if abs(baseline) < 1e-12:
        if abs(sdlc) < 1e-12:
            return 0.0
        return -1.0 if direction == "lower" else 1.0
    return (baseline - sdlc) / abs(baseline) if direction == "lower" else (sdlc - baseline) / abs(baseline)


def percentile(values: list[float], p: float) -> float:
    if not values:
        return math.nan
    ordered = sorted(values)
    position = (len(ordered) - 1) * p
    lower = int(math.floor(position)); upper = int(math.ceil(position))
    if lower == upper:
        return ordered[lower]
    return ordered[lower] + (ordered[upper] - ordered[lower]) * (position - lower)


def bootstrap_ci(values: list[float], samples: int, seed: int) -> tuple[float, float]:
    if not values:
        return (math.nan, math.nan)
    rng = random.Random(seed)
    estimates = [mean(rng.choice(values) for _ in values) for _ in range(samples)]
    return (percentile(estimates, 0.025), percentile(estimates, 0.975))


def sign_test_p(values: list[float]) -> float:
    nonzero = [value for value in values if abs(value) > 1e-12]
    n = len(nonzero)
    if n == 0:
        return 1.0
    positives = sum(value > 0 for value in nonzero)
    tail = sum(math.comb(n, k) for k in range(positives, n + 1)) / (2 ** n)
    return min(1.0, 2 * min(tail, 1 - tail + math.comb(n, positives) / (2 ** n)))


def verify_chain(exp: dict[str, Any]) -> list[str]:
    errors = []
    previous = "GENESIS"
    for index, record in enumerate(exp.get("runs", []), 1):
        if record.get("previous_hash") != previous:
            errors.append(f"run {index} previous_hash mismatch")
        claimed = record.get("record_hash")
        calculated = digest({k: v for k, v in record.items() if k != "record_hash"})
        if claimed != calculated:
            errors.append(f"run {index} record_hash mismatch")
        previous = str(claimed)
    if previous != exp.get("record_chain_head", "GENESIS"):
        errors.append("record_chain_head mismatch")
    return errors


def _runs_by_task(exp: dict[str, Any]) -> dict[str, dict[str, dict[str, Any]]]:
    by_task: dict[str, dict[str, dict[str, Any]]] = {}
    for run in exp.get("runs", []):
        by_task.setdefault(str(run.get("task_id")), {})[str(run.get("arm"))] = run
    return by_task


def _reviewers_for(exp: dict[str, Any], blind_code: str) -> set[str]:
    return {
        str(item.get("reviewer_code"))
        for item in exp.get("reviews", [])
        if item.get("blind_artifact_code") == blind_code
    }


def _seal_payload(exp: dict[str, Any]) -> dict[str, Any]:
    return {
        "schema_version": exp.get("schema_version"),
        "experiment_id": exp.get("experiment_id"),
        "preregistration_hash": exp.get("preregistration_hash"),
        "record_chain_head": exp.get("record_chain_head"),
        "reviews_hash": digest(exp.get("reviews", [])),
        "sealed_at": exp.get("sealed_at"),
    }


def formal_readiness_errors(exp: dict[str, Any]) -> list[str]:
    """Return controls that must pass before a real experiment can be sealed."""
    errors: list[str] = []
    by_task = _runs_by_task(exp)
    complete = {task: arms for task, arms in by_task.items() if ARMS.issubset(arms)}
    if len(complete) < int(exp.get("target_pairs", 0)):
        errors.append("insufficient complete pairs")

    contaminated = [run for run in exp.get("runs", []) if run.get("contamination", "none") != "none"]
    if contaminated:
        errors.append("contamination present")

    all_executors = {str(run.get("executor_code")) for run in exp.get("runs", [])}
    for assignment in exp.get("assignments", []):
        task_id = str(assignment.get("task_id"))
        arms = complete.get(task_id)
        if not arms:
            continue
        baseline = arms["baseline"]
        sdlc = arms["sdlc"]
        if baseline.get("model") != sdlc.get("model"):
            errors.append(f"model mismatch for {task_id}")
        if baseline.get("toolset_hash") != sdlc.get("toolset_hash"):
            errors.append(f"toolset mismatch for {task_id}")
        if baseline.get("start_state_hash") != sdlc.get("start_state_hash"):
            errors.append(f"start state mismatch for {task_id}")
        if baseline.get("environment_hash") != sdlc.get("environment_hash"):
            errors.append(f"environment mismatch for {task_id}")
        if baseline.get("execution_context_id") == sdlc.get("execution_context_id"):
            errors.append(f"execution context reused across arms for {task_id}")

        codes = assignment.get("blind_artifact_codes", {})
        baseline_reviewers = _reviewers_for(exp, str(codes.get("baseline", "")))
        sdlc_reviewers = _reviewers_for(exp, str(codes.get("sdlc", "")))
        if not baseline_reviewers or not sdlc_reviewers:
            errors.append(f"blind review incomplete for {task_id}")
        elif baseline_reviewers != sdlc_reviewers:
            errors.append(f"reviewer set mismatch for {task_id}")
        for reviewer in baseline_reviewers | sdlc_reviewers:
            if reviewer in all_executors:
                errors.append(f"reviewer is also an executor: {reviewer}")

    return list(dict.fromkeys(errors))


def validate(exp: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if exp.get("schema_version") != VERSION:
        errors.append("unsupported schema_version")
    if exp.get("frozen_at"):
        prereg = {key: exp[key] for key in ["schema_version", "experiment_id", "project", "target_pairs", "randomization_seed", "hypothesis", "synthetic", "protocol", "metrics", "tasks", "assignments", "frozen_at"]}
        if digest(prereg) != exp.get("preregistration_hash"):
            errors.append("preregistration hash mismatch")

    assignments = exp.get("assignments", [])
    if assignments:
        baseline_first = sum(1 for item in assignments if item.get("order") == ["baseline", "sdlc"])
        sdlc_first = sum(1 for item in assignments if item.get("order") == ["sdlc", "baseline"])
        invalid_orders = len(assignments) - baseline_first - sdlc_first
        if invalid_orders:
            errors.append("invalid assignment order")
        if abs(baseline_first - sdlc_first) > 1:
            errors.append("assignment order is not balanced")

    seen: set[tuple[Any, Any]] = set()
    contexts: set[str] = set()
    run_positions: dict[str, list[str]] = {}
    for run in exp.get("runs", []):
        key = (run.get("task_id"), run.get("arm"))
        if key in seen:
            errors.append(f"duplicate run {key}")
        seen.add(key)
        if run.get("arm") not in ARMS:
            errors.append(f"invalid arm {run.get('arm')}")
        run_positions.setdefault(str(run.get("task_id")), []).append(str(run.get("arm")))
        context_id = str(run.get("execution_context_id", ""))
        if not context_id:
            errors.append(f"missing execution_context_id in {key}")
        elif context_id in contexts:
            errors.append(f"duplicate execution_context_id {context_id}")
        contexts.add(context_id)
        for field in ["prompt_hash", "toolset_hash", "start_state_hash", "environment_hash", "artifact_hash", "run_log_hash"]:
            if not re_hex(str(run.get(field, ""))):
                errors.append(f"invalid {field} in {key}")
        for name in METRICS:
            if name not in run.get("metrics", {}):
                errors.append(f"missing metric {name} in {key}")

    for assignment in assignments:
        task_id = str(assignment.get("task_id"))
        observed = run_positions.get(task_id, [])
        expected = list(assignment.get("order", []))[: len(observed)]
        if observed != expected:
            errors.append(f"run order mismatch for {task_id}")

    errors.extend(verify_chain(exp))
    if exp.get("sealed_at"):
        if exp.get("seal_hash") != digest(_seal_payload(exp)):
            errors.append("seal hash mismatch")
    elif exp.get("seal_hash"):
        errors.append("seal hash present without sealed_at")
    return list(dict.fromkeys(errors))


def seal(exp: dict[str, Any]) -> str:
    if exp.get("sealed_at"):
        raise RuntimeError("Experiment is already sealed")
    errors = validate(exp)
    errors.extend(formal_readiness_errors(exp))
    errors = list(dict.fromkeys(errors))
    if errors:
        raise RuntimeError("Cannot seal experiment: " + "; ".join(errors))
    exp["sealed_at"] = now()
    exp["seal_hash"] = digest(_seal_payload(exp))
    return str(exp["seal_hash"])

def analyze(exp: dict[str, Any]) -> dict[str, Any]:
    errors = validate(exp)
    if errors:
        raise RuntimeError("Invalid experiment: " + "; ".join(errors))
    by_task: dict[str, dict[str, dict[str, Any]]] = {}
    for run in exp["runs"]:
        by_task.setdefault(run["task_id"], {})[run["arm"]] = run
    complete = {task: arms for task, arms in by_task.items() if ARMS.issubset(arms)}
    metric_results = {}
    categories: dict[str, list[float]] = {}
    for metric, spec in METRICS.items():
        paired = [relative_improvement(arms["baseline"]["metrics"][metric], arms["sdlc"]["metrics"][metric], spec["direction"]) for arms in complete.values()]
        if not paired:
            continue
        low, high = bootstrap_ci(paired, int(exp["protocol"]["bootstrap_samples"]), int(exp["randomization_seed"]) + sum(ord(ch) for ch in metric))
        result = {
            "pairs": len(paired), "mean_relative_improvement": round(mean(paired), 6),
            "median_relative_improvement": round(median(paired), 6),
            "ci95": [round(low, 6), round(high, 6)], "sign_test_p": round(sign_test_p(paired), 6),
            "category": spec["category"], "paired_values": [round(value, 6) for value in paired],
        }
        metric_results[metric] = result
        categories.setdefault(spec["category"], []).append(result["mean_relative_improvement"])
    category_results = {}
    for category, values in categories.items():
        category_results[category] = {"mean_relative_improvement": round(mean(values), 6), "status": "improved" if mean(values) >= 0.05 else "regressed" if mean(values) <= -0.05 else "flat"}
    severe = []
    for metric in ["critical_defects", "escaped_defects", "acceptance_pass_rate"]:
        item = metric_results.get(metric)
        if item and item["mean_relative_improvement"] < -0.20:
            severe.append(metric)
    improved_primary = [name for name, item in category_results.items() if name in PRIMARY_CATEGORIES and item["status"] == "improved"]
    regressed_primary = [name for name, item in category_results.items() if name in PRIMARY_CATEGORIES and item["status"] == "regressed"]
    significant_positive = [name for name, item in metric_results.items() if item["category"] in PRIMARY_CATEGORIES and item["mean_relative_improvement"] >= 0.05 and item["ci95"][0] > 0]
    enough = len(complete) >= int(exp["target_pairs"])
    contaminated = [run for run in exp["runs"] if run.get("contamination", "none") != "none"]
    controls = formal_readiness_errors(exp)
    noncontamination_controls = [item for item in controls if item not in {"contamination present", "insufficient complete pairs"}]
    if severe or len(regressed_primary) >= 2:
        raw_decision = "negative"
    elif len(improved_primary) >= 2 and significant_positive:
        raw_decision = "positive"
    else:
        raw_decision = "inconclusive"

    if exp.get("synthetic"):
        decision = "synthetic-smoke-only"
    elif not enough:
        decision = "insufficient-data"
    elif contaminated:
        decision = "invalid-contamination"
    elif noncontamination_controls:
        decision = "invalid-controls"
    elif not exp.get("sealed_at"):
        decision = f"provisional-{raw_decision}"
    else:
        decision = raw_decision
    code_to_arm = {assignment["blind_artifact_codes"][arm]: arm for assignment in exp["assignments"] for arm in ARMS}
    review_scores: dict[str, list[float]] = {arm: [] for arm in ARMS}
    for review in exp["reviews"]:
        arm = code_to_arm[review["blind_artifact_code"]]
        review_scores[arm].append(mean(float(review[name]) for name in ["correctness", "completeness", "maintainability", "usability"]))
    return {
        "generated_at": now(), "project": exp["project"], "experiment_id": exp["experiment_id"],
        "synthetic": exp["synthetic"], "complete_pairs": len(complete), "target_pairs": exp["target_pairs"],
        "decision": decision, "metrics": metric_results, "categories": category_results,
        "improved_primary_categories": improved_primary, "regressed_primary_categories": regressed_primary,
        "significant_positive_metrics": significant_positive, "severe_regressions": severe,
        "contaminated_runs": len(contaminated),
        "sealed": bool(exp.get("sealed_at")),
        "seal_hash": exp.get("seal_hash"),
        "formal_evidence_eligible": bool(not exp.get("synthetic") and exp.get("sealed_at") and enough and not controls),
        "control_errors": controls,
        "blind_review_means": {arm: round(mean(values), 4) if values else None for arm, values in review_scores.items()},
        "limitations": [
            "A positive result applies only to the sampled tasks, executors, models, tools and time window.",
            "Synthetic data validates the harness only and is never effectiveness evidence.",
            "Small matched samples have low power; retain raw paired results and inspect heterogeneity.",
        ],
    }


def report_markdown(exp: dict[str, Any], result: dict[str, Any]) -> str:
    lines = [
        "# Agentic SDLC OS L5-B Matched Experiment", "",
        f"- Experiment: `{result['experiment_id']}`", f"- Project: **{result['project']}**",
        f"- Preregistration: `{exp.get('preregistration_hash')}`", f"- Complete pairs: {result['complete_pairs']}/{result['target_pairs']}",
        f"- Synthetic: **{result['synthetic']}**", f"- Decision: **{result['decision'].upper()}**", "",
        "## Paired metric effects", "", "| Metric | Mean improvement | 95% CI | Sign-test p |", "|---|---:|---:|---:|",
    ]
    for name, item in result["metrics"].items():
        lines.append(f"| `{name}` | {item['mean_relative_improvement']:.1%} | [{item['ci95'][0]:.1%}, {item['ci95'][1]:.1%}] | {item['sign_test_p']} |")
    lines += [
        "", "## Decision controls", "",
        f"- Improved primary categories: {', '.join(result['improved_primary_categories']) or 'none'}",
        f"- Significant positive metrics: {', '.join(result['significant_positive_metrics']) or 'none'}",
        f"- Severe regressions: {', '.join(result['severe_regressions']) or 'none'}",
        f"- Contaminated runs: {result['contaminated_runs']}",
        f"- Sealed: {result['sealed']}",
        f"- Formal evidence eligible: {result['formal_evidence_eligible']}",
        f"- Control errors: {', '.join(result['control_errors']) or 'none'}",
        "", "## Blind review", "",
        f"- Baseline: {result['blind_review_means']['baseline']}",
        f"- SDLC: {result['blind_review_means']['sdlc']}",
        "", "## Limitations", "",
    ]
    lines.extend(f"- {item}" for item in result["limitations"])
    return "\n".join(lines) + "\n"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Agentic SDLC OS L5-B matched-pair experiment")
    parser.add_argument("--version", action="version", version=VERSION)
    sub = parser.add_subparsers(dest="command", required=True)
    p = sub.add_parser("init"); p.add_argument("file"); p.add_argument("--project", required=True); p.add_argument("--target-pairs", type=int, default=5); p.add_argument("--seed", type=int, default=20260831); p.add_argument("--hypothesis", default="Agentic SDLC OS improves delivery outcomes without severe quality regression."); p.add_argument("--synthetic", action="store_true")
    p = sub.add_parser("add-task"); p.add_argument("file"); p.add_argument("--task-id", required=True); p.add_argument("--task-hash", required=True); p.add_argument("--domain", required=True); p.add_argument("--complexity", type=int, required=True); p.add_argument("--time-budget-minutes", type=int, required=True)
    p = sub.add_parser("freeze"); p.add_argument("file")
    p = sub.add_parser("record"); p.add_argument("file"); p.add_argument("--task-id", required=True); p.add_argument("--arm", choices=sorted(ARMS), required=True); p.add_argument("--executor-code", required=True); p.add_argument("--execution-context-id", required=True); p.add_argument("--model", required=True); p.add_argument("--prompt-hash", required=True); p.add_argument("--toolset-hash", required=True); p.add_argument("--start-state-hash", required=True); p.add_argument("--environment-hash", required=True); p.add_argument("--artifact-hash", required=True); p.add_argument("--run-log-hash", required=True); p.add_argument("--contamination", default="none")
    for name in METRICS: p.add_argument("--" + name.replace("_", "-"), type=float, required=True)
    p = sub.add_parser("review"); p.add_argument("file"); p.add_argument("--blind-artifact-code", required=True); p.add_argument("--reviewer-code", required=True); p.add_argument("--correctness", type=float, required=True); p.add_argument("--completeness", type=float, required=True); p.add_argument("--maintainability", type=float, required=True); p.add_argument("--usability", type=float, required=True); p.add_argument("--notes", default="")
    p = sub.add_parser("seal"); p.add_argument("file")
    p = sub.add_parser("validate"); p.add_argument("file"); p.add_argument("--json", action="store_true")
    p = sub.add_parser("report"); p.add_argument("file"); p.add_argument("--output"); p.add_argument("--json", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    path = Path(args.file).expanduser().resolve()
    try:
        if args.command == "init":
            if path.exists(): raise RuntimeError(f"Experiment already exists: {path}")
            exp = new_experiment(args.project, args.target_pairs, args.seed, args.hypothesis, args.synthetic); atomic_write(path, exp); print(path); return 0
        exp = load(path)
        if args.command == "add-task":
            add_task(exp, args.task_id, args.task_hash, args.domain, args.complexity, args.time_budget_minutes); atomic_write(path, exp); print(args.task_id); return 0
        if args.command == "freeze":
            freeze(exp); atomic_write(path, exp); print(exp["preregistration_hash"]); return 0
        if args.command == "record":
            metrics = {name: getattr(args, name) for name in METRICS}
            record_run(exp, task_id=args.task_id, arm=args.arm, executor_code=args.executor_code, execution_context_id=args.execution_context_id, model=args.model, prompt_hash=args.prompt_hash, toolset_hash=args.toolset_hash, start_state_hash=args.start_state_hash, environment_hash=args.environment_hash, artifact_hash=args.artifact_hash, run_log_hash=args.run_log_hash, metrics=metrics, contamination=args.contamination); atomic_write(path, exp); print(f"{args.task_id}/{args.arm}"); return 0
        if args.command == "review":
            add_review(exp, blind_artifact_code=args.blind_artifact_code, reviewer_code=args.reviewer_code, correctness=args.correctness, completeness=args.completeness, maintainability=args.maintainability, usability=args.usability, notes=args.notes); atomic_write(path, exp); print("reviewed"); return 0
        if args.command == "seal":
            seal_hash = seal(exp); atomic_write(path, exp); print(seal_hash); return 0
        if args.command == "validate":
            errors = validate(exp); payload = {"valid": not errors, "errors": errors}; print(json.dumps(payload, indent=2) if args.json else ("VALID" if not errors else "\n".join(errors))); return 0 if not errors else 2
        result = analyze(exp); report = report_markdown(exp, result)
        if args.output: Path(args.output).write_text(report, encoding="utf-8")
        print(json.dumps(result, indent=2) if args.json else report); return 0
    except (RuntimeError, ValueError, KeyError, OSError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=os.sys.stderr); return 2


if __name__ == "__main__":
    raise SystemExit(main())
