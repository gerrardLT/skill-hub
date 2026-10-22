#!/usr/bin/env python3
"""Validate Phase 1 root review batches and cited semantic audit reports."""
from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from pathlib import Path
from typing import Any

REQUIRED_TERMS = ("Trigger", "Responsibility", "Inputs", "Outputs", "Workflow", "Permissions", "Unique", "Weakness", "Support")
CITATION = re.compile(r"(?:skills/)?[^\s`|]+/SKILL\.md(?::|#L|\s+lines?\s+|\s+L)\d+(?:[-–:]\d+)?", re.IGNORECASE)

def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))

def verify(workspace: Path, reports_root: Path | None = None) -> dict[str, Any]:
    ledger = load(workspace / "curation/v2/coverage.json")
    batch_data = load(workspace / "curation/v2/root-batches.json")
    expected = {item["path"] for item in ledger["roots"]}
    assignments = [root for roots in batch_data.get("batches", {}).values() for root in roots]
    counts = Counter(assignments)
    errors = []
    missing = sorted(expected - set(assignments))
    extra = sorted(set(assignments) - expected)
    duplicate = sorted(root for root, count in counts.items() if count != 1)
    if missing: errors.append(f"unassigned roots: {missing}")
    if extra: errors.append(f"unknown assigned roots: {extra}")
    if duplicate: errors.append(f"roots assigned other than once: {duplicate}")
    report_results = []
    if reports_root:
        for batch, roots in batch_data["batches"].items():
            path = reports_root / f"{batch}.md"
            if not path.is_file():
                errors.append(f"missing review report: {batch}")
                continue
            text = path.read_text(encoding="utf-8", errors="replace")
            absent_roots = [root for root in roots if root not in text]
            absent_terms = [term for term in REQUIRED_TERMS if term.lower() not in text.lower()]
            citations = CITATION.findall(text)
            if absent_roots: errors.append(f"review report {batch} lacks roots: {absent_roots}")
            if absent_terms: errors.append(f"review report {batch} lacks sections: {absent_terms}")
            if len(citations) < len(roots): errors.append(f"review report {batch} lacks per-root line citations: {len(citations)} < {len(roots)}")
            report_results.append({"batch": batch, "path": path.as_posix(), "root_count": len(roots), "citation_count": len(citations), "bytes": path.stat().st_size})
    return {"gate": "capability-compiler-v2-phase-1-review", "ok": not errors, "root_count": len(expected), "assignment_count": len(assignments), "reports": report_results, "errors": errors}

def main() -> int:
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument("--workspace-root",type=Path,default=Path("."));parser.add_argument("--reports-root",type=Path);args=parser.parse_args();workspace=args.workspace_root.resolve();reports=args.reports_root.resolve() if args.reports_root else None;result=verify(workspace,reports);print(json.dumps(result,ensure_ascii=False,sort_keys=True));return 0 if result["ok"] else 1
if __name__=="__main__":raise SystemExit(main())
