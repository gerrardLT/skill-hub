#!/usr/bin/env python3
"""Validate structured V2 root dossiers against the immutable source index."""
from __future__ import annotations

import argparse
import fnmatch
import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

REQUIRED_FIELDS = {
    "root_id", "skill_path", "source_sha256", "trigger", "non_trigger", "responsibility",
    "non_responsibility", "inputs", "outputs", "workflow", "branches", "rules_gates",
    "stop_conditions", "tools_dependencies", "permissions_side_effects", "unique_methods",
    "weaknesses_failure_modes", "relationship_hypotheses", "source_citations", "support_file_reviews",
}
DISPOSITIONS = {"semantic-read", "behavior-reviewed", "excluded"}

def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))

def verify(workspace: Path, dossiers_root: Path) -> dict[str, Any]:
    index = load(workspace / "curation/v2/source-index.json")
    ledger = load(workspace / "curation/v2/coverage.json")
    validator = Draft202012Validator(load(workspace / "curation/v2/root-dossier.schema.json"))
    expected = {item["root_id"]: item for item in index["records"]}
    files = {item["path"]: item for item in ledger["files"]}
    seen={};errors=[]
    for path in sorted(dossiers_root.glob("*.json")):
        try:data=load(path)
        except (OSError,json.JSONDecodeError) as exc:errors.append(f"invalid dossier {path}: {exc}");continue
        root_id=data.get("root_id")
        schema_errors = sorted(validator.iter_errors(data), key=lambda item: list(item.absolute_path))
        if schema_errors:
            errors.extend(f"dossier schema {path.name}: {'/'.join(map(str, item.absolute_path))}: {item.message}" for item in schema_errors)
            continue
        if root_id in seen:errors.append(f"duplicate root dossier: {root_id}")
        seen[root_id]=path.as_posix()
        missing=sorted(REQUIRED_FIELDS-set(data))
        if missing:errors.append(f"dossier missing fields {root_id}: {missing}");continue
        source=expected.get(root_id)
        if not source:errors.append(f"unknown dossier root: {root_id}");continue
        if data["skill_path"]!=source["path"] or data["source_sha256"]!=source["sha256"]:errors.append(f"dossier source identity mismatch: {root_id}")
        for field in ("trigger","non_trigger","responsibility","non_responsibility"):
            if not isinstance(data[field],str) or not data[field].strip():errors.append(f"dossier empty {field}: {root_id}")
        for field in ("inputs","outputs","workflow","rules_gates","unique_methods","weaknesses_failure_modes","source_citations"):
            if not isinstance(data[field],list) or not data[field]:errors.append(f"dossier lacks {field}: {root_id}")
        if not all(
            isinstance(item, dict)
            and item.get("path") == data["skill_path"]
            and isinstance(item.get("line_start"), int)
            and isinstance(item.get("line_end"), int)
            and 1 <= item["line_start"] <= item["line_end"] <= source["line_count"]
            for item in data["source_citations"]
        ):
            errors.append(f"dossier has invalid citations: {root_id}")
        owned_paths = {path for path, item in files.items() if item.get("primary_owner") == root_id}
        covered_paths: set[str] = set()
        for review in data["support_file_reviews"]:
            pattern = review.get("path")
            matched = sorted(path for path in owned_paths if isinstance(pattern, str) and fnmatch.fnmatchcase(path, pattern))
            if review.get("disposition") not in DISPOSITIONS or not matched:
                errors.append(f"invalid support review: {root_id}:{review}")
            if review.get("disposition")=="excluded" and (not review.get("reason") or not review.get("subkind")):
                errors.append(f"excluded support review lacks reason or subkind: {root_id}:{pattern}")
            if not review.get("evidence"):errors.append(f"support review lacks evidence: {root_id}:{pattern}")
            declared_matches = review.get("matched_paths")
            if declared_matches is not None and declared_matches != matched:
                errors.append(f"support review matched_paths drift: {root_id}:{pattern}")
            review["matched_paths"] = matched
            covered_paths.update(matched)
        uncovered_paths = sorted(owned_paths - covered_paths)
        if uncovered_paths:
            errors.append(f"dossier leaves support files unreviewed: {root_id}:{uncovered_paths}")
    missing_roots=sorted(set(expected)-set(seen));extra_roots=sorted(set(seen)-set(expected))
    if missing_roots:errors.append(f"missing root dossiers: {missing_roots}")
    if extra_roots:errors.append(f"extra root dossiers: {extra_roots}")
    return {"gate":"capability-compiler-v2-root-dossiers","ok":not errors,"expected":len(expected),"checked":len(seen),"errors":errors}

def main()->int:
    p=argparse.ArgumentParser(description=__doc__);p.add_argument("--workspace-root",type=Path,default=Path("."));p.add_argument("--dossiers-root",type=Path,required=True);a=p.parse_args();r=verify(a.workspace_root.resolve(),a.dossiers_root.resolve());print(json.dumps(r,ensure_ascii=False,sort_keys=True));return 0 if r["ok"] else 1
if __name__=="__main__":raise SystemExit(main())
