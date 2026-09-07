#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "manifest" / "external-skills.json"
INSTALLER = ROOT / "skills" / "agentic-sdlc-os" / "scripts" / "install_external_skills.py"


def record(case: str, passed: bool, expected: str, observed: Any, severity: str = "P0") -> dict[str, Any]:
    return {"case": case, "severity": severity, "control_passed": passed, "expected": expected, "observed": observed}


def run_json(*args: str) -> tuple[int, dict[str, Any], str]:
    r = subprocess.run([sys.executable, str(INSTALLER), *args, "--json"], cwd=ROOT, capture_output=True, text=True, check=False)
    try:
        data = json.loads(r.stdout) if r.stdout.strip() else {}
    except json.JSONDecodeError:
        data = {}
    return r.returncode, data, r.stderr


def main() -> int:
    m = json.loads(MANIFEST.read_text(encoding="utf-8"))
    results: list[dict[str, Any]] = []

    design_core = {x["skill"] for x in m["skills"] if x["os"] == "design" and x["tier"] == "core"}
    results.append(record(
        "design_has_single_primary_visual_director",
        "impeccable" in design_core and "frontend-design" not in design_core and "design-taste-frontend" not in design_core,
        "Design Core must avoid multiple competing visual directors.", sorted(design_core), "P1",
    ))

    qa_text = (ROOT / "skills" / "qa-operating-system" / "SKILL.md").read_text(encoding="utf-8")
    qa_core = {x["skill"] for x in m["skills"] if x["os"] == "qa" and x["tier"] == "core"}
    results.append(record(
        "qa_cannot_self_fix_product_source",
        "不得修改产品源码" in qa_text and "qa-only" in qa_core and "qa" not in qa_core,
        "QA must report/reproduce/verify while production remediation routes to Engineering.",
        {"qa_core": sorted(qa_core), "policy_present": "不得修改产品源码" in qa_text},
    ))

    rc, generic, _ = run_json("--os", "evolution", "--profile", "core")
    provider_selected = [x for x in generic.get("selection", []) if x.get("provider")]
    results.append(record(
        "evolution_provider_adapters_are_opt_in",
        rc == 0 and not provider_selected,
        "Generic Evolution Core must not silently activate Sentry, Datadog or PostHog.", provider_selected,
    ))

    rc, _, stderr = run_json("--os", "qa", "--profile", "core", "--provider", "sentry")
    results.append(record(
        "provider_adapter_cannot_escape_evolution_boundary",
        rc == 2 and "provider" in stderr.lower(),
        "Provider adapters are Evolution-only and must be rejected for other OS selections.", stderr.strip(),
    ))

    evo_text = (ROOT / "skills" / "evolution-operating-system" / "SKILL.md").read_text(encoding="utf-8")
    results.append(record(
        "provider_adapter_cannot_override_learning_gate",
        "must not" in evo_text and "learning-decision" in evo_text and "不得绕过 Release/QA Gate" in evo_text,
        "Provider evidence/actions must remain subordinate to learning and release/QA gates.",
        {"provider_policy_present": "Provider Adapter" in evo_text},
    ))

    passed = sum(bool(x["control_passed"]) for x in results)
    output = {
        "system_version": "2.4.0",
        "scope": "skill-composition-separation-provider-safety",
        "summary": {"cases": len(results), "passed": passed, "failed": len(results) - passed, "all_controls_passed": passed == len(results)},
        "results": results,
    }
    (ROOT / "validation" / "v24_red_team_results.json").write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(output, ensure_ascii=False, indent=2))
    return 0 if passed == len(results) else 2


if __name__ == "__main__":
    raise SystemExit(main())
