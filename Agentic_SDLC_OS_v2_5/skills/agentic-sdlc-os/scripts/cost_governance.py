#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
POLICY = json.loads((ROOT / "manifest" / "cost-policy.json").read_text(encoding="utf-8"))


def load_project(project: Path) -> tuple[dict[str, Any], dict[str, Any]]:
    base = project.resolve() / ".sdlc"
    return (
        json.loads((base / "state.json").read_text(encoding="utf-8")),
        json.loads((base / "config.json").read_text(encoding="utf-8")),
    )


def usage(state: dict[str, Any]) -> dict[str, Any]:
    runs = state.get("runs", [])
    by_os: dict[str, dict[str, float]] = {}
    for item in runs:
        os_name = str(item.get("os", "unknown"))
        row = by_os.setdefault(os_name, {"runs": 0, "cost_usd": 0.0, "tokens": 0, "tool_calls": 0, "human_hours": 0.0})
        row["runs"] += 1
        row["cost_usd"] += float(item.get("cost_usd", 0.0))
        row["tokens"] += int(item.get("tokens_input", 0)) + int(item.get("tokens_output", 0))
        row["tool_calls"] += int(item.get("tool_calls", 0))
        row["human_hours"] += float(item.get("human_hours", 0.0))
    total = {
        "runs": len(runs),
        "cost_usd": round(sum(float(item.get("cost_usd", 0.0)) for item in runs), 6),
        "tokens": sum(int(item.get("tokens_input", 0)) + int(item.get("tokens_output", 0)) for item in runs),
        "tool_calls": sum(int(item.get("tool_calls", 0)) for item in runs),
        "human_hours": round(sum(float(item.get("human_hours", 0.0)) for item in runs), 4),
    }
    return {"total": total, "by_os": by_os}


def assess(state: dict[str, Any], config: dict[str, Any], forecast_usd: float = 0.0, forecast_tokens: int = 0) -> dict[str, Any]:
    current = usage(state)
    cost_limit = config.get("cost_budget_usd")
    token_limit = config.get("token_budget")
    projected_cost = current["total"]["cost_usd"] + forecast_usd
    projected_tokens = current["total"]["tokens"] + forecast_tokens
    ratios = []
    if cost_limit not in (None, 0):
        ratios.append(projected_cost / float(cost_limit))
    if token_limit not in (None, 0):
        ratios.append(projected_tokens / int(token_limit))
    ratio = max(ratios) if ratios else 0.0
    thresholds = POLICY["thresholds"]
    if ratio >= thresholds["block"]:
        level, allowed = "blocked", False
    elif ratio >= thresholds["degrade"]:
        level, allowed = "degraded", True
    elif ratio >= thresholds["watch"]:
        level, allowed = "watch", True
    else:
        level, allowed = "normal", True
    actions = [] if level == "normal" else POLICY["degradation_order"][:2] if level == "watch" else POLICY["degradation_order"][:5] if level == "degraded" else POLICY["degradation_order"]
    return {
        "allowed": allowed,
        "level": level,
        "utilization": round(ratio, 4),
        "projected_cost_usd": round(projected_cost, 6),
        "projected_tokens": projected_tokens,
        "remaining_cost_usd": None if cost_limit is None else round(float(cost_limit) - projected_cost, 6),
        "remaining_tokens": None if token_limit is None else int(token_limit) - projected_tokens,
        "actions": actions,
        "protected_work": POLICY["protected_work"],
        "usage": current,
    }


def set_budget(project: Path, cost: float | None, tokens: int | None) -> dict[str, Any]:
    path = project.resolve() / ".sdlc" / "config.json"
    config = json.loads(path.read_text(encoding="utf-8"))
    if cost is not None:
        config["cost_budget_usd"] = cost
    if tokens is not None:
        config["token_budget"] = tokens
    path.write_text(json.dumps(config, indent=2) + "\n", encoding="utf-8")
    return config


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Budget, forecast and degrade Agentic SDLC execution")
    sub = parser.add_subparsers(dest="command", required=True)
    p = sub.add_parser("assess"); p.add_argument("project"); p.add_argument("--forecast-usd", type=float, default=0.0); p.add_argument("--forecast-tokens", type=int, default=0)
    p = sub.add_parser("set"); p.add_argument("project"); p.add_argument("--cost-usd", type=float); p.add_argument("--tokens", type=int)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        project = Path(args.project)
        if args.command == "set":
            payload = set_budget(project, args.cost_usd, args.tokens)
        else:
            state, config = load_project(project)
            payload = assess(state, config, args.forecast_usd, args.forecast_tokens)
        print(json.dumps(payload, indent=2))
        return 0 if payload.get("allowed", True) else 3
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
