#!/usr/bin/env python3
"""Normalize Phase 0 auxiliary units without making semantic disposition decisions."""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

try:
    from tools.curation.v2_phase0_audit import load_units
except ModuleNotFoundError:
    from v2_phase0_audit import load_units

LINE_ID = re.compile(r"^(?:skills/)?(.+?):(\d+)(?:-(\d+))?(?:-.*)?$")
PATH_ID = re.compile(r"^(?:skills/)?(.+?\.(?:md|py|js|ts)):")

def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))

def write(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")

def infer_source_path(unit: dict[str, Any]) -> str | None:
    if unit.get("source_path"):
        return str(unit["source_path"]).removeprefix("skills/")
    unit_id = str(unit.get("id", ""))
    match = LINE_ID.match(unit_id)
    if match and match.group(1).endswith((".md", ".py", ".js", ".ts")):
        return match.group(1)
    path_match = PATH_ID.match(unit_id)
    if path_match:
        return path_match.group(1)
    if str(unit.get("id", "")).startswith("impeccable:craft-floor:"):
        return "impeccable/reference/craft-floor.md"
    return None

def normalize(workspace: Path) -> dict[str, Any]:
    units, errors = load_units(workspace / "curation/units")
    clusters = load(workspace / "curation/clusters.json")
    clustered = {unit_id for cluster in clusters["clusters"] for unit_id in cluster["unit_ids"]}
    records = []
    for unit in units:
        unit_id = unit.get("id")
        if not isinstance(unit_id, str) or unit_id in clustered:
            continue
        source_path = infer_source_path(unit)
        if not source_path:
            errors.append(f"cannot infer source path: {unit_id}")
        status = unit.get("status")
        records.append({
            "id": unit_id,
            "source_path": source_path,
            "origin_line_start": unit.get("origin_line_start"),
            "origin_line_end": unit.get("origin_line_end"),
            "type": unit.get("type"),
            "raw_excerpt": unit.get("raw_excerpt"),
            "meaning": unit.get("meaning"),
            "boundary_condition": unit.get("boundary_condition"),
            "dependency_skills": unit.get("dependency_skills", []),
            "candidate_destination": unit.get("candidate_destination"),
            "validation_criteria": unit.get("validation_criteria"),
            "legacy_status": status,
            "source_unit_file": unit.get("_file"),
            "v2_disposition": "pending-semantic-review",
            "target_unit_id": None,
            "target_cluster_id": None,
            "decision_id": None,
        })
    return {"schema_version": "2.0", "gate": "capability-compiler-v2-auxiliary-units", "ok": not errors and len(records) == 114, "count": len(records), "units": records, "errors": errors + ([] if len(records) == 114 else [f"expected 114 auxiliary units, found {len(records)}"])}

def verify_disposed(data: dict[str, Any]) -> list[str]:
    errors=[];allowed={"merge","supersede","retain","defer","exclude"}
    for unit in data.get("units",[]):
        if unit.get("v2_disposition") not in allowed or not unit.get("decision_id"):
            errors.append(f"auxiliary unit lacks disposition: {unit.get('id')}")
        if unit.get("v2_disposition") in {"merge","supersede"} and not unit.get("target_unit_id"):
            errors.append(f"auxiliary merge lacks target: {unit.get('id')}")
        if unit.get("v2_disposition")=="retain" and not unit.get("target_cluster_id"):
            errors.append(f"retained auxiliary unit lacks cluster: {unit.get('id')}")
        if unit.get("v2_disposition") in {"merge","supersede","retain"} and unit.get("source_validation") not in {"exact-source-slice","source-supported-summary","relocated-source-supported-summary"}:
            errors.append(f"active auxiliary disposition lacks source validation: {unit.get('id')}")
        if unit.get("v2_disposition")=="defer" and not unit.get("defer_reason"):
            errors.append(f"deferred auxiliary unit lacks reason: {unit.get('id')}")
    return errors

def main() -> int:
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument("--workspace-root",type=Path,default=Path("."));parser.add_argument("--output",type=Path,required=True);parser.add_argument("--verify-disposed",action="store_true");args=parser.parse_args()
    if args.verify_disposed:
        data=load(args.output);errors=verify_disposed(data);result={"gate":"capability-compiler-v2-auxiliary-disposition","ok":not errors,"errors":errors};print(json.dumps(result,ensure_ascii=False,sort_keys=True));return 0 if result["ok"] else 1
    result=normalize(args.workspace_root.resolve());write(args.output.resolve(),result);print(json.dumps({"gate":result["gate"],"ok":result["ok"],"count":result["count"],"errors":result["errors"]},ensure_ascii=False,sort_keys=True));return 0 if result["ok"] else 1
if __name__=="__main__":raise SystemExit(main())
