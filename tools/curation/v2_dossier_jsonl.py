#!/usr/bin/env python3
"""Import strict JSONL root dossiers and update V2 review coverage from cited evidence."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

try:
    from tools.curation.v2_root_dossier_gate import verify
except ModuleNotFoundError:
    from v2_root_dossier_gate import verify


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))

def write(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")

def import_jsonl(workspace: Path, jsonl_root: Path, dossiers_root: Path, coverage_path: Path) -> dict[str, Any]:
    dossiers_root.mkdir(parents=True, exist_ok=True)
    errors=[];count=0
    for path in sorted(jsonl_root.glob("*.jsonl")):
        for line_number,line in enumerate(path.read_text(encoding="utf-8").splitlines(),1):
            if not line.strip():continue
            try:data=json.loads(line)
            except json.JSONDecodeError as exc:errors.append(f"invalid JSONL {path.name}:{line_number}: {exc}");continue
            root_id=data.get("root_id")
            if not isinstance(root_id,str) or not root_id.startswith("skill-root:"):errors.append(f"invalid root identity {path.name}:{line_number}");continue
            output=dossiers_root/(root_id.removeprefix("skill-root:").replace("/","__")+".json")
            if output.exists():errors.append(f"duplicate dossier output: {root_id}");continue
            write(output,data);count+=1
    if errors:
        return {"gate":"capability-compiler-v2-dossier-import","ok":False,"count":count,"errors":errors}
    gate=verify(workspace,dossiers_root)
    if not gate["ok"]:
        return {"gate":"capability-compiler-v2-dossier-import","ok":False,"count":count,"errors":gate["errors"]}
    coverage=load(coverage_path)
    by_root={item["root_id"]:item for item in (load(path) for path in dossiers_root.glob("*.json"))}
    files_by_owner: dict[str, set[str]] = {}
    for item in coverage["files"]:
        files_by_owner.setdefault(item["primary_owner"], set()).add(item["path"])
    file_evidence: dict[str,list[str]]={}
    for root_id,dossier in by_root.items():
        dossier_file=dossiers_root/(root_id.removeprefix("skill-root:").replace("/","__")+".json")
        try:
            dossier_path=dossier_file.relative_to(workspace).as_posix()
        except ValueError:
            dossier_path=dossier_file.as_posix()
        root=next(item for item in coverage["roots"] if item["id"]==root_id)
        root.update(v2_status="semantic-read",dossier=dossier_path,review_evidence=[dossier_path])
        for review in dossier["support_file_reviews"]:
            import fnmatch
            matched_paths = sorted(path for path in files_by_owner.get(root_id, set()) if fnmatch.fnmatchcase(path, review["path"]))
            for matched in matched_paths:
                record=next(item for item in coverage["files"] if item["path"]==matched)
                record.update(v2_status=review["disposition"],reason=review.get("reason"),subkind=review.get("subkind"),review_evidence=[dossier_path,*review.get("evidence",[])])
                file_evidence.setdefault(matched,[]).append(root_id)
    unreviewed=[item["path"] for item in coverage["files"] if item["v2_status"] not in {"semantic-read","behavior-reviewed","excluded"}]
    duplicate_primary=[path for path,roots in file_evidence.items() if len(roots)!=1]
    if unreviewed:errors.append(f"files remain unreviewed: {unreviewed}")
    if duplicate_primary:errors.append(f"files reviewed by other than one primary root: {duplicate_primary}")
    coverage["counts"]["semantic-read"]=sum(item["v2_status"]=="semantic-read" for item in coverage["files"])
    coverage["counts"]["behavior-reviewed"]=sum(item["v2_status"]=="behavior-reviewed" for item in coverage["files"])
    coverage["counts"]["excluded"]=sum(item["v2_status"]=="excluded" for item in coverage["files"])
    coverage["counts"].pop("semantic-review-required",None);coverage["counts"].pop("behavior-review-required",None)
    coverage["ok"]=not errors;coverage["errors"]=errors
    write(coverage_path,coverage)
    return {"gate":"capability-compiler-v2-dossier-import","ok":not errors,"count":count,"reviewed_files":len(file_evidence),"errors":errors}

def main()->int:
    p=argparse.ArgumentParser(description=__doc__);p.add_argument("--workspace-root",type=Path,default=Path("."));p.add_argument("--jsonl-root",type=Path,required=True);p.add_argument("--dossiers-root",type=Path,required=True);p.add_argument("--coverage",type=Path,required=True);a=p.parse_args();r=import_jsonl(a.workspace_root.resolve(),a.jsonl_root.resolve(),a.dossiers_root.resolve(),a.coverage.resolve());print(json.dumps(r,ensure_ascii=False,sort_keys=True));return 0 if r["ok"] else 1
if __name__=="__main__":raise SystemExit(main())
