#!/usr/bin/env python3
"""Import completed Phase 1B review artifacts with hashes and batch identity."""
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
from pathlib import Path
from typing import Any

try:
    from tools.curation.v2_phase1_review_gate import verify
except ModuleNotFoundError:
    from v2_phase1_review_gate import verify


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))

def write(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")

def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes().replace(b"\r\n", b"\n")).hexdigest()

def import_artifacts(workspace: Path, source_root: Path, output_root: Path, workflow_run_id: str, origins_path: Path | None = None) -> dict[str, Any]:
    batches = load(workspace / "curation/v2/root-batches.json")["batches"]
    origins = load(origins_path).get("batches", {}) if origins_path else {}
    output_root.mkdir(parents=True, exist_ok=True)
    errors=[];records=[]
    for batch, roots in batches.items():
        source=source_root/f"{batch}.md";destination=output_root/f"{batch}.md"
        if not source.is_file():errors.append(f"missing source review artifact: {batch}");continue
        shutil.copyfile(source,destination)
        try:
            stored_path = destination.relative_to(workspace).as_posix()
        except ValueError:
            stored_path = destination.as_posix()
        record={"batch":batch,"workflow_run_id":workflow_run_id,"source_artifact":source.as_posix(),"path":stored_path,"sha256":digest(destination),"bytes":destination.stat().st_size,"root_ids":[f"skill-root:{root}" for root in roots]}
        if origins_path:
            if batch not in origins:errors.append(f"missing review origin: {batch}")
            else:record["origin"]=origins[batch]
        records.append(record)
    if not errors:
        gate=verify(workspace,output_root)
        errors.extend(gate["errors"])
    result={"schema_version":"2.0","gate":"capability-compiler-v2-review-import","ok":not errors,"workflow_run_id":workflow_run_id,"batch_count":len(records),"root_count":sum(len(item["root_ids"]) for item in records),"records":records,"errors":errors}
    write(output_root/"manifest.json",result)
    return result

def main()->int:
    p=argparse.ArgumentParser(description=__doc__);p.add_argument("--workspace-root",type=Path,default=Path("."));p.add_argument("--source-root",type=Path,required=True);p.add_argument("--output-root",type=Path,required=True);p.add_argument("--workflow-run-id",required=True);p.add_argument("--origins",type=Path);a=p.parse_args();r=import_artifacts(a.workspace_root.resolve(),a.source_root.resolve(),a.output_root.resolve(),a.workflow_run_id,a.origins.resolve() if a.origins else None);print(json.dumps({k:r[k] for k in ("gate","ok","batch_count","root_count","errors")},ensure_ascii=False,sort_keys=True));return 0 if r["ok"] else 1
if __name__=="__main__":raise SystemExit(main())
