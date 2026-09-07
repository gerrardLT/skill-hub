#!/usr/bin/env python3
"""Adversarial regression suite for v2.1 Work Item governance."""
from __future__ import annotations

import io
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from tests.test_v21_work_items import TestV21WorkItems

OUTPUT = ROOT / "validation" / "v21_work_item_red_team_results.json"

CASES = {
    "test_bounded_low_risk_change_can_downgrade_high_assurance_project": "bounded low-risk change avoids project-wide over-governance without inheriting unrelated high-assurance artifacts",
    "test_unbounded_work_cannot_downgrade_project_profile": "unbounded work cannot use Work Item tailoring to evade project governance",
    "test_protected_path_escalates_bounded_lite_work_to_standard": "protected CI/deployment/security-like paths cannot remain lite",
    "test_domain_overlay_applies_only_when_work_impacts_domain": "domain overlays are isolated to materially impacted work",
    "test_project_and_previous_work_artifacts_do_not_satisfy_active_work_gate": "historical or project-scoped artifacts cannot be borrowed to satisfy a new change gate",
    "test_trace_and_quality_use_artifact_work_profile": "artifact integrity is checked against the governance profile that created it rather than an unrelated project profile",
    "test_bounded_lite_work_compresses_stage_machine": "bounded-lite work compresses orchestration while retaining the build gate",
}


def main() -> int:
    results = []
    for method, expected in CASES.items():
        suite = unittest.TestSuite([TestV21WorkItems(method)])
        stream = io.StringIO()
        outcome = unittest.TextTestRunner(stream=stream, verbosity=2).run(suite)
        passed = outcome.wasSuccessful()
        results.append({
            "case": method.removeprefix("test_"),
            "severity": "P0" if "artifact" in method or "unbounded" in method else "P1",
            "control_passed": passed,
            "expected": expected,
            "observed": stream.getvalue().strip()[-1600:],
        })
    failed = [item for item in results if not item["control_passed"]]
    report = {
        "system_version": "2.1.0",
        "scope": "work-item-tailoring-scope-and-compact-flow",
        "summary": {
            "cases": len(results),
            "passed": len(results) - len(failed),
            "failed": len(failed),
            "all_controls_passed": not failed,
        },
        "results": results,
    }
    OUTPUT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if not failed else 1


if __name__ == "__main__":
    raise SystemExit(main())
