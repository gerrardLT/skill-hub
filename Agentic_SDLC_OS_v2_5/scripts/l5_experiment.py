#!/usr/bin/env python3
"""Preregister and analyze Agentic SDLC OS L5 real-project experiments.

This tool deliberately separates control-plane validation from outcome evidence.
It uses only the Python standard library and never claims causality from an
underpowered or synthetic dataset.
"""
from __future__ import annotations

import argparse
import json
import math
import os
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from statistics import mean
from typing import Any, Dict, Iterable, List, Optional, Sequence

VERSION = "1.0"
ARMS = {"baseline", "sdlc"}
COMPARISONS = {"historical-matched", "parallel", "sequential-crossover"}
METRICS: Dict[str, Dict[str, Any]] = {
    "lead_time_hours": {"direction": "lower", "category": "cycle", "minimum": 0.0},
    "rework_rate": {"direction": "lower", "category": "rework", "minimum": 0.0, "maximum": 1.0},
    "escaped_defects": {"direction": "lower", "category": "quality", "minimum": 0.0},
    "incidents": {"direction": "lower", "category": "quality", "minimum": 0.0},
    "rollback_rate": {"direction": "lower", "category": "quality", "minimum": 0.0, "maximum": 1.0},
    "trace_coverage": {"direction": "higher", "category": "traceability", "minimum": 0.0, "maximum": 1.0},
    "evidence_decision_rate": {"direction": "higher", "category": "traceability", "minimum": 0.0, "maximum": 1.0},
    "goal_attainment": {"direction": "higher", "category": "outcome", "minimum": 0.0, "maximum": 1.0},
    "human_hours": {"direction": "lower", "category": "effort", "minimum": 0.0},
    "token_cost_usd": {"direction": "lower", "category": "cost", "minimum": 0.0},
    "actionability_score": {"direction": "higher", "category": "usability", "minimum": 0.0, "maximum": 10.0},
}
PRIMARY_CATEGORIES = {"cycle", "rework", "quality", "traceability", "outcome"}


def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def atomic_write(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(prefix=f".{path.name}.", dir=str(path.parent))
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as fh:
            json.dump(payload, fh, ensure_ascii=False, indent=2)
            fh.write("\n")
        os.replace(tmp, path)
    finally:
        if os.path.exists(tmp):
            os.unlink(tmp)


def load(path: Path) -> Dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise RuntimeError(f"Experiment file not found: {path}") from exc
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"Invalid experiment JSON: {exc}") from exc
    if not isinstance(payload, dict):
        raise RuntimeError("Experiment file must contain a JSON object")
    return payload


def validate_metric(name: str, value: float) -> float:
    spec = METRICS[name]
    numeric = float(value)
    if not math.isfinite(numeric):
        raise RuntimeError(f"Metric {name} must be finite")
    if numeric < float(spec.get("minimum", -math.inf)):
        raise RuntimeError(f"Metric {name} is below its minimum")
    maximum = spec.get("maximum")
    if maximum is not None and numeric > float(maximum):
        raise RuntimeError(f"Metric {name} exceeds its maximum {maximum}")
    return numeric


def validate_experiment(exp: Dict[str, Any]) -> List[str]:
    errors: List[str] = []
    if exp.get("schema_version") != VERSION:
        errors.append(f"Unsupported schema_version: {exp.get('schema_version')}")
    if not str(exp.get("project", "")).strip():
        errors.append("Missing project")
    if exp.get("comparison") not in COMPARISONS:
        errors.append(f"Invalid comparison: {exp.get('comparison')}")
    if not isinstance(exp.get("target_iterations"), int) or int(exp.get("target_iterations", 0)) < 2:
        errors.append("target_iterations must be an integer >= 2")
    iterations = exp.get("iterations", [])
    reviews = exp.get("reviews", [])
    if not isinstance(iterations, list):
        errors.append("iterations must be an array")
        iterations = []
    if not isinstance(reviews, list):
        errors.append("reviews must be an array")
        reviews = []
    seen_iterations: set[tuple[str, str]] = set()
    seen_artifacts: set[str] = set()
    for item in iterations:
        if not isinstance(item, dict):
            errors.append("Iteration is not an object")
            continue
        arm = str(item.get("arm", ""))
        iteration_id = str(item.get("iteration_id", ""))
        artifact_id = str(item.get("artifact_id", ""))
        if arm not in ARMS:
            errors.append(f"Invalid arm: {arm}")
        if not iteration_id:
            errors.append("Iteration missing iteration_id")
        key = (arm, iteration_id)
        if key in seen_iterations:
            errors.append(f"Duplicate iteration: {arm}/{iteration_id}")
        seen_iterations.add(key)
        if not artifact_id:
            errors.append(f"Iteration {arm}/{iteration_id} missing artifact_id")
        elif artifact_id in seen_artifacts:
            errors.append(f"Duplicate artifact_id: {artifact_id}")
        seen_artifacts.add(artifact_id)
        metrics = item.get("metrics", {})
        for metric in METRICS:
            if metric not in metrics:
                errors.append(f"Iteration {arm}/{iteration_id} missing metric {metric}")
                continue
            try:
                validate_metric(metric, float(metrics[metric]))
            except (ValueError, TypeError, RuntimeError) as exc:
                errors.append(str(exc))
    seen_reviews: set[tuple[str, str]] = set()
    for review in reviews:
        if not isinstance(review, dict):
            errors.append("Review is not an object")
            continue
        key = (str(review.get("artifact_id", "")), str(review.get("reviewer_code", "")))
        if not all(key):
            errors.append("Review requires artifact_id and reviewer_code")
        if key in seen_reviews:
            errors.append(f"Duplicate review: {key[0]}/{key[1]}")
        seen_reviews.add(key)
        if key[0] not in seen_artifacts:
            errors.append(f"Review references unknown artifact: {key[0]}")
        if review.get("arm_code") not in {"A", "B"}:
            errors.append(f"Invalid blind arm code: {review.get('arm_code')}")
        for field in ["actionability", "correctness", "clarity"]:
            try:
                value = float(review.get(field))
                if not 0 <= value <= 10:
                    raise ValueError
            except (TypeError, ValueError):
                errors.append(f"Review {key[0]}/{key[1]} has invalid {field}")
    return list(dict.fromkeys(errors))


def new_experiment(
    project: str,
    comparison: str,
    target_iterations: int,
    hypothesis: str,
    synthetic: bool = False,
) -> Dict[str, Any]:
    if comparison not in COMPARISONS:
        raise RuntimeError(f"Invalid comparison: {comparison}")
    if target_iterations < 2:
        raise RuntimeError("target_iterations must be >= 2")
    return {
        "schema_version": VERSION,
        "project": project,
        "comparison": comparison,
        "target_iterations": target_iterations,
        "registered_at": now(),
        "synthetic": bool(synthetic),
        "hypothesis": hypothesis,
        "metric_definitions": METRICS,
        "decision_rule": {
            "minimum_iterations_per_arm": target_iterations,
            "positive": "At least two primary categories improve by >=5% and no severe regression occurs.",
            "negative": "A severe regression occurs or at least two primary categories worsen by >=5%.",
            "otherwise": "Inconclusive; collect more matched iterations or inspect confounders.",
            "severe_regression": "Quality/outcome metric worsens by >20%, including new incidents when baseline is zero.",
        },
        "iterations": [],
        "reviews": [],
        "analysis_history": [],
    }


def add_iteration(exp: Dict[str, Any], arm: str, iteration_id: str, artifact_id: str, metrics: Dict[str, float], notes: str = "") -> None:
    if arm not in ARMS:
        raise RuntimeError(f"Invalid arm: {arm}")
    for item in exp.get("iterations", []):
        if item.get("arm") == arm and item.get("iteration_id") == iteration_id:
            raise RuntimeError(f"Duplicate iteration: {arm}/{iteration_id}")
        if item.get("artifact_id") == artifact_id:
            raise RuntimeError(f"Duplicate artifact_id: {artifact_id}")
    normalized = {name: validate_metric(name, metrics[name]) for name in METRICS}
    exp.setdefault("iterations", []).append({
        "arm": arm,
        "iteration_id": iteration_id,
        "artifact_id": artifact_id,
        "metrics": normalized,
        "notes": notes,
        "recorded_at": now(),
    })


def add_review(
    exp: Dict[str, Any], artifact_id: str, reviewer_code: str, arm_code: str,
    actionability: float, correctness: float, clarity: float, notes: str = "",
) -> None:
    artifact_ids = {str(x.get("artifact_id")) for x in exp.get("iterations", [])}
    if artifact_id not in artifact_ids:
        raise RuntimeError(f"Unknown artifact_id: {artifact_id}")
    if arm_code not in {"A", "B"}:
        raise RuntimeError("arm_code must be A or B")
    for value, name in [(actionability, "actionability"), (correctness, "correctness"), (clarity, "clarity")]:
        if not 0 <= float(value) <= 10:
            raise RuntimeError(f"{name} must be between 0 and 10")
    if any(
        item.get("artifact_id") == artifact_id and item.get("reviewer_code") == reviewer_code
        for item in exp.get("reviews", [])
    ):
        raise RuntimeError(f"Duplicate review: {artifact_id}/{reviewer_code}")
    exp.setdefault("reviews", []).append({
        "artifact_id": artifact_id,
        "reviewer_code": reviewer_code,
        "arm_code": arm_code,
        "actionability": float(actionability),
        "correctness": float(correctness),
        "clarity": float(clarity),
        "notes": notes,
        "recorded_at": now(),
    })


def relative_improvement(baseline: float, treatment: float, direction: str) -> float:
    if abs(baseline) < 1e-12:
        if abs(treatment) < 1e-12:
            return 0.0
        return -1.0 if direction == "lower" else 1.0
    raw = (baseline - treatment) / abs(baseline) if direction == "lower" else (treatment - baseline) / abs(baseline)
    return raw


def means_for_arm(iterations: Iterable[Dict[str, Any]], arm: str) -> Dict[str, float]:
    rows = [x for x in iterations if x.get("arm") == arm]
    if not rows:
        return {}
    return {metric: mean(float(row["metrics"][metric]) for row in rows) for metric in METRICS}


def analyze(exp: Dict[str, Any]) -> Dict[str, Any]:
    errors = validate_experiment(exp)
    if errors:
        raise RuntimeError("Invalid experiment: " + "; ".join(errors))
    iterations = exp["iterations"]
    counts = {arm: sum(1 for x in iterations if x.get("arm") == arm) for arm in sorted(ARMS)}
    baseline = means_for_arm(iterations, "baseline")
    sdlc = means_for_arm(iterations, "sdlc")
    metrics: Dict[str, Any] = {}
    category_values: Dict[str, List[float]] = {}
    if baseline and sdlc:
        for name, spec in METRICS.items():
            improvement = relative_improvement(baseline[name], sdlc[name], spec["direction"])
            metrics[name] = {
                "baseline_mean": round(baseline[name], 6),
                "sdlc_mean": round(sdlc[name], 6),
                "absolute_change": round(sdlc[name] - baseline[name], 6),
                "relative_improvement": round(improvement, 6),
                "direction": spec["direction"],
                "category": spec["category"],
            }
            category_values.setdefault(spec["category"], []).append(improvement)
    category_results = {
        category: {
            "mean_relative_improvement": round(mean(values), 6),
            "status": "improved" if mean(values) >= 0.05 else "regressed" if mean(values) <= -0.05 else "flat",
        }
        for category, values in category_values.items()
    }

    severe_regressions: List[str] = []
    for name in ["escaped_defects", "incidents", "rollback_rate", "goal_attainment"]:
        if name in metrics and metrics[name]["relative_improvement"] < -0.20:
            severe_regressions.append(name)
    primary_improved = [
        name for name, result in category_results.items()
        if name in PRIMARY_CATEGORIES and result["status"] == "improved"
    ]
    primary_regressed = [
        name for name, result in category_results.items()
        if name in PRIMARY_CATEGORIES and result["status"] == "regressed"
    ]
    enough_data = all(counts[arm] >= int(exp["target_iterations"]) for arm in ARMS)
    if not enough_data:
        decision = "insufficient-data"
    elif severe_regressions or len(primary_regressed) >= 2:
        decision = "negative"
    elif len(primary_improved) >= 2:
        decision = "positive"
    else:
        decision = "inconclusive"

    artifact_to_arm = {str(x.get("artifact_id")): str(x.get("arm")) for x in iterations}
    review_by_arm: Dict[str, List[float]] = {"baseline": [], "sdlc": []}
    review_detail: List[Dict[str, Any]] = []
    for item in exp.get("reviews", []):
        composite = mean([float(item["actionability"]), float(item["correctness"]), float(item["clarity"])])
        arm = artifact_to_arm.get(str(item.get("artifact_id")))
        if arm in review_by_arm:
            review_by_arm[arm].append(composite)
        review_detail.append({
            "artifact_id": item.get("artifact_id"),
            "reviewer_code": item.get("reviewer_code"),
            "blind_arm_code": item.get("arm_code"),
            "composite": round(composite, 4),
        })
    review_summary = {
        arm: round(mean(values), 4) if values else None for arm, values in review_by_arm.items()
    }
    return {
        "generated_at": now(),
        "project": exp["project"],
        "comparison": exp["comparison"],
        "synthetic": bool(exp.get("synthetic")),
        "counts": counts,
        "target_iterations": exp["target_iterations"],
        "enough_data": enough_data,
        "decision": decision,
        "metrics": metrics,
        "categories": category_results,
        "primary_categories_improved": primary_improved,
        "primary_categories_regressed": primary_regressed,
        "severe_regressions": severe_regressions,
        "blind_review_summary": review_summary,
        "blind_reviews": review_detail,
        "limitations": [
            "This analysis does not establish causality unless allocation, matching, and confounders are controlled.",
            "Synthetic data is a tooling smoke test only and cannot validate real-project effectiveness.",
            "Means hide variance; inspect individual iterations before acting on small samples.",
        ],
    }


def markdown_report(exp: Dict[str, Any], result: Dict[str, Any]) -> str:
    lines = [
        "# Agentic SDLC OS — L5 Experiment Report",
        "",
        f"- Project: **{result['project']}**",
        f"- Comparison: `{result['comparison']}`",
        f"- Registered: `{exp.get('registered_at')}`",
        f"- Generated: `{result['generated_at']}`",
        f"- Synthetic: **{'YES — SMOKE TEST ONLY' if result['synthetic'] else 'NO'}**",
        f"- Decision: **{result['decision'].upper()}**",
        f"- Iterations: baseline={result['counts']['baseline']}, sdlc={result['counts']['sdlc']}, target={result['target_iterations']} each",
        "",
        "## Preregistered hypothesis",
        "",
        str(exp.get("hypothesis", "")),
        "",
        "## Metric results",
        "",
        "| Metric | Baseline | SDLC | Relative improvement | Direction |",
        "|---|---:|---:|---:|---|",
    ]
    for name, item in result["metrics"].items():
        lines.append(
            f"| `{name}` | {item['baseline_mean']} | {item['sdlc_mean']} | {item['relative_improvement']:.1%} | {item['direction']} |"
        )
    if not result["metrics"]:
        lines.append("| — | — | — | — | — |")
    lines.extend([
        "",
        "## Category decision",
        "",
        "| Category | Mean relative improvement | Status |",
        "|---|---:|---|",
    ])
    for name, item in result["categories"].items():
        lines.append(f"| {name} | {item['mean_relative_improvement']:.1%} | {item['status']} |")
    lines.extend([
        "",
        "## Blind review",
        "",
        f"- Baseline composite: {result['blind_review_summary']['baseline']}",
        f"- SDLC composite: {result['blind_review_summary']['sdlc']}",
        "",
        "## Decision basis",
        "",
        f"- Improved primary categories: {', '.join(result['primary_categories_improved']) or 'none'}",
        f"- Regressed primary categories: {', '.join(result['primary_categories_regressed']) or 'none'}",
        f"- Severe regressions: {', '.join(result['severe_regressions']) or 'none'}",
        "",
        "## Limitations",
        "",
    ])
    lines.extend(f"- {item}" for item in result["limitations"])
    return "\n".join(lines) + "\n"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Agentic SDLC OS L5 experiment harness")
    parser.add_argument("--version", action="version", version=VERSION)
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("init", help="Preregister an experiment")
    p.add_argument("file")
    p.add_argument("--project", required=True)
    p.add_argument("--comparison", choices=sorted(COMPARISONS), default="historical-matched")
    p.add_argument("--target-iterations", type=int, default=2)
    p.add_argument("--hypothesis", default="Agentic SDLC OS improves delivery quality or cycle outcomes without severe regressions.")
    p.add_argument("--synthetic", action="store_true")

    p = sub.add_parser("record", help="Record one baseline or SDLC iteration")
    p.add_argument("file")
    p.add_argument("--arm", choices=sorted(ARMS), required=True)
    p.add_argument("--iteration-id", required=True)
    p.add_argument("--artifact-id", required=True)
    for name in METRICS:
        p.add_argument("--" + name.replace("_", "-"), type=float, required=True)
    p.add_argument("--notes", default="")

    p = sub.add_parser("review", help="Add a blind artifact review")
    p.add_argument("file")
    p.add_argument("--artifact-id", required=True)
    p.add_argument("--reviewer-code", required=True)
    p.add_argument("--arm-code", choices=["A", "B"], required=True)
    p.add_argument("--actionability", type=float, required=True)
    p.add_argument("--correctness", type=float, required=True)
    p.add_argument("--clarity", type=float, required=True)
    p.add_argument("--notes", default="")

    p = sub.add_parser("validate", help="Validate an experiment file")
    p.add_argument("file")
    p.add_argument("--json", action="store_true")

    p = sub.add_parser("report", help="Analyze and report the experiment")
    p.add_argument("file")
    p.add_argument("--output")
    p.add_argument("--json", action="store_true")
    return parser


def main(argv: Optional[Sequence[str]] = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        path = Path(args.file).expanduser().resolve()
        if args.command == "init":
            if path.exists():
                raise RuntimeError(f"Experiment already exists: {path}")
            exp = new_experiment(args.project, args.comparison, args.target_iterations, args.hypothesis, args.synthetic)
            atomic_write(path, exp)
            print(path)
            return 0
        exp = load(path)
        if args.command == "record":
            metrics = {name: getattr(args, name) for name in METRICS}
            add_iteration(exp, args.arm, args.iteration_id, args.artifact_id, metrics, args.notes)
            atomic_write(path, exp)
            print(f"Recorded {args.arm}/{args.iteration_id}")
            return 0
        if args.command == "review":
            add_review(
                exp, args.artifact_id, args.reviewer_code, args.arm_code,
                args.actionability, args.correctness, args.clarity, args.notes,
            )
            atomic_write(path, exp)
            print(f"Reviewed {args.artifact_id}/{args.reviewer_code}")
            return 0
        if args.command == "validate":
            errors = validate_experiment(exp)
            payload = {"valid": not errors, "errors": errors}
            print(json.dumps(payload, ensure_ascii=False, indent=2) if args.json else ("VALID" if not errors else "\n".join(errors)))
            return 0 if not errors else 2
        result = analyze(exp)
        report = markdown_report(exp, result)
        if args.output:
            output = Path(args.output).expanduser().resolve()
            output.parent.mkdir(parents=True, exist_ok=True)
            output.write_text(report, encoding="utf-8")
        print(json.dumps(result, ensure_ascii=False, indent=2) if args.json else report)
        return 0
    except (RuntimeError, KeyError, ValueError) as exc:
        print(f"ERROR: {exc}", file=os.sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
