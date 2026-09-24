#!/usr/bin/env python3
"""Run the repository-owned test and Capability Compiler gates."""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path


def command(name: str, *args: str) -> tuple[str, list[str]]:
    return name, [sys.executable, *args]


def run_all(workspace: Path) -> dict[str, object]:
    verify = "tools/curation/verify.py"
    commands = [
        command("tests", "-m", "pytest", "-q"),
        command("source", verify, "source", "--root", "skills", "--baseline", "curation/baseline.json"),
        command("phase2", verify, "phase2", "--inventory", "curation/inventory.json", "--gaps", "curation/gaps.json", "--reference-review", "curation/reference-review.json", "--dependency-scan", "curation/dependency-scan.json", "--supplements-root", "curation/supplements", "--policy", "curation/policy.json", "--content-root", "slots", "--content-root", "recipes", "--content-root", "dev-loop"),
        command("phase3", verify, "phase3", "--inventory", "curation/inventory.json", "--skills-root", "skills", "--dossiers-root", "curation/dossiers", "--units-root", "curation/units", "--coverage", "curation/coverage.json", "--reference-review", "curation/reference-review.json", "--supplements-root", "curation/supplements"),
        command("phase4", verify, "phase4", "--inventory", "curation/inventory.json", "--units-root", "curation/units", "--clusters", "curation/clusters.json", "--decisions", "curation/decisions.jsonl"),
        command("phase5-provenance", verify, "phase5", "--clusters", "curation/clusters.json", "--units-root", "curation/units", "--decisions", "curation/decisions.jsonl", "--coverage", "curation/coverage.json", "--slots-root", "slots"),
        command("phase5-release", verify, "phase5-release", "--workspace-root", "."),
        command("phase6", verify, "phase6", "--clusters", "curation/clusters.json", "--units-root", "curation/units", "--slots-root", "slots", "--review-queue", "curation/slot-review-queue.json", "--release-status", "curation/slot-release-status.json", "--inventory", "curation/inventory.json"),
        command("phase7", verify, "phase7", "--recipes-root", "recipes", "--slots-root", "slots"),
        command("phase8-source", verify, "phase8-sync", "--audit", "curation/dev-loop-sync-audit.json", "--workspace-root", "."),
    ]
    env = os.environ.copy()
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    results = []
    for name, args in commands:
        process = subprocess.run(args, cwd=workspace, text=True, capture_output=True, encoding="utf-8", env=env)
        results.append({"name": name, "ok": process.returncode == 0, "returncode": process.returncode, "stdout": process.stdout[-4000:], "stderr": process.stderr[-4000:]})
    return {"gate": "all-repository-gates", "ok": all(item["ok"] for item in results), "results": results}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workspace-root", type=Path, default=Path("."))
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    report = run_all(args.workspace_root.resolve())
    rendered = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    print(rendered, end="")
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
