#!/usr/bin/env python3
"""Create a line-addressable evidence index for every source SKILL.md."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path
from typing import Any

try:
    from tools.curation.inventory import build_skill_roots, normalized_bytes
except ModuleNotFoundError:  # direct script execution
    from inventory import build_skill_roots, normalized_bytes

LINK = re.compile(r"\[[^\]]*\]\(([^)]+)\)|`([^`]+)`")

def write(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")

def build(workspace: Path) -> dict[str, Any]:
    skills = workspace / "skills"
    records = []
    errors = []
    for root in build_skill_roots(skills):
        path = skills / root["skill_path"]
        text = path.read_text(encoding="utf-8", errors="replace")
        lines = text.splitlines()
        headings = [{"line": number, "level": len(line) - len(line.lstrip("#")), "text": line.lstrip("#").strip()} for number, line in enumerate(lines, 1) if line.startswith("#")]
        local_refs = []
        for number, line in enumerate(lines, 1):
            for markdown_target, code_target in LINK.findall(line):
                target = (markdown_target or code_target).split("#", 1)[0].strip()
                if not target or target.startswith(("http://", "https://", "mailto:", "#", "/")):
                    continue
                candidate = (path.parent / target).resolve()
                try:
                    relative = candidate.relative_to(skills.resolve()).as_posix()
                except ValueError:
                    continue
                if candidate.exists():
                    local_refs.append({"line": number, "target": relative, "kind": "directory" if candidate.is_dir() else "file"})
        records.append({
            "root_id": root["id"], "path": root["skill_path"], "sha256": hashlib.sha256(normalized_bytes(path)).hexdigest(),
            "line_count": len(lines), "headings": headings, "local_references": local_refs,
        })
        if not headings:
            errors.append(f"SKILL.md has no headings: {root['skill_path']}")
    return {"schema_version": "2.0", "ok": not errors, "root_count": len(records), "line_count": sum(item["line_count"] for item in records), "records": records, "errors": errors}

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__);parser.add_argument("--workspace-root",type=Path,default=Path("."));parser.add_argument("--output",type=Path,required=True);args=parser.parse_args()
    result=build(args.workspace_root.resolve());write(args.output.resolve(),result);print(json.dumps({"ok":result["ok"],"root_count":result["root_count"],"line_count":result["line_count"],"errors":result["errors"]},ensure_ascii=False,sort_keys=True));return 0 if result["ok"] else 1
if __name__=="__main__":raise SystemExit(main())
