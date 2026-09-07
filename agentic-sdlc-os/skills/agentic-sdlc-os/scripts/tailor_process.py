#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "manifest" / "process-tailoring.json"
FACTOR_NAMES = [
    "blast_radius", "data_sensitivity", "regulatory_exposure", "irreversibility",
    "technical_novelty", "problem_uncertainty", "user_exposure", "change_size",
    "operational_complexity",
]


@dataclass(frozen=True)
class TailoringDecision:
    profile: str
    risk_score: float
    hard_escalations: list[str]
    required_controls: list[str]
    optional_controls: list[str]
    minimum_independent_reviewers: int
    rationale: list[str]


def load_manifest(path: Path = MANIFEST) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def assess(factors: dict[str, int], *, domain_risk: float = 0.0, manifest: dict[str, Any] | None = None) -> TailoringDecision:
    spec = manifest or load_manifest()
    normalized: dict[str, int] = {}
    rationale: list[str] = []
    for name in FACTOR_NAMES:
        value = int(factors.get(name, 0))
        if value < 0 or value > 5:
            raise ValueError(f"{name} must be between 0 and 5")
        normalized[name] = value
    score = sum(normalized[name] * float(spec["factors"][name]["weight"]) for name in FACTOR_NAMES) + float(domain_risk)
    thresholds = spec["thresholds"]
    profile = "lite" if score <= float(thresholds["lite_max"]) else "standard" if score <= float(thresholds["standard_max"]) else "high-assurance"
    escalations: list[str] = []
    order = {"lite": 0, "standard": 1, "high-assurance": 2}
    for rule in spec.get("hard_escalations", []):
        factor = str(rule["factor"])
        if normalized[factor] >= int(rule["minimum"]):
            target = str(rule["profile"])
            escalations.append(f"{factor}>={rule['minimum']}")
            if order[target] > order[profile]:
                profile = target
    high = sorted(normalized.items(), key=lambda item: (-item[1], item[0]))[:3]
    rationale.append("Highest risk factors: " + ", ".join(f"{name}={value}" for name, value in high))
    if domain_risk:
        rationale.append(f"Domain risk adjustment: {domain_risk:+.1f}")
    if escalations:
        rationale.append("Hard escalation: " + ", ".join(escalations))
    profile_spec = spec["profiles"][profile]
    return TailoringDecision(
        profile=profile,
        risk_score=round(score, 2),
        hard_escalations=escalations,
        required_controls=list(profile_spec["required_controls"]),
        optional_controls=list(profile_spec["optional_controls"]),
        minimum_independent_reviewers=int(profile_spec["minimum_independent_reviewers"]),
        rationale=rationale,
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Select the smallest safe Agentic SDLC process profile")
    for name in FACTOR_NAMES:
        parser.add_argument("--" + name.replace("_", "-"), type=int, default=0)
    parser.add_argument("--domain-risk", type=float, default=0.0)
    parser.add_argument("--output")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    factors = {name: getattr(args, name) for name in FACTOR_NAMES}
    try:
        decision = assess(factors, domain_risk=args.domain_risk)
    except ValueError as exc:
        print(f"ERROR: {exc}")
        return 2
    payload = asdict(decision) | {"factors": factors}
    text = json.dumps(payload, indent=2)
    if args.output:
        Path(args.output).write_text(text + "\n", encoding="utf-8")
    print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
