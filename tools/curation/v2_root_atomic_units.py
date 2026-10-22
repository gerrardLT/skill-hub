#!/usr/bin/env python3
"""Extract source-grounded atomic capability candidates for roots absent from canonical units."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from collections import defaultdict
from pathlib import Path
from typing import Any

try:
    from tools.curation.v2_phase0_audit import load_units
except ModuleNotFoundError:
    from v2_phase0_audit import load_units

SEMANTIC_HEAD=re.compile(r"(?i)\b(?:phase|step|workflow|procedure|process|method|mode|decision|gate|check|validate|verify|install|enable|configure|setup|deploy|rollback|monitor|alert|troubleshoot|diagnos|investigat|review|audit|benchmark|freeze|guard|ship|release|restore|sync|generate|scrape|health|security|architecture|readiness|reliability|observability|instrument|remap|root cause|runbook|pair|plan|spec|retro|learn|office hours)")
BOILERPLATE=re.compile(r"(?i)^(?:preamble|when to invoke|plan mode|skill invocation|askuserquestion|tool resolution|model-specific|writing style|voice$|context restoration|browser setup|translate the aside|continuous checkpoint|confusion protocol|completeness principle|report writing standards|interaction protocol)")
GENERIC={"overview","usage","inputs","outputs","summary","examples","example","references","contents","purpose","context"}

def load(path:Path)->Any:return json.loads(path.read_text(encoding="utf-8"))
def write(path:Path,value:Any)->None:path.parent.mkdir(parents=True,exist_ok=True);path.write_text(json.dumps(value,ensure_ascii=False,indent=2,sort_keys=True)+"\n",encoding="utf-8",newline="\n")
def clean(text:str,limit:int=500)->str:
    return re.sub(r"\s+"," ",re.sub(r"[`*_#|]","",text)).strip(" -:\t")[:limit]
def sections(lines:list[str])->list[tuple[int,int,int,str]]:
    heads=[]
    for number,line in enumerate(lines,1):
        match=re.match(r"^(#{1,6})\s+(.+?)\s*$",line)
        if match:heads.append((number,len(match.group(1)),clean(match.group(2))))
    result=[]
    for index,(start,level,title) in enumerate(heads):
        end=len(lines)
        for next_start,next_level,_ in heads[index+1:]:
            if next_level<=level:end=next_start-1;break
        result.append((start,end,level,title))
    return result

def excerpt(lines:list[str],start:int,end:int,max_lines:int=40)->tuple[str,int]:
    actual_end=min(end,start+max_lines-1);value="\n".join(lines[start-1:actual_end]).strip();return value,actual_end

def slug(text:str)->str:
    value=re.sub(r"[^a-z0-9]+","-",text.casefold()).strip("-");return value[:72] or "responsibility"
def root_sources(workspace:Path)->set[str]:
    units,errors=load_units(workspace/"curation/units");clusters=load(workspace/"curation/clusters.json")["clusters"];clustered={item for cluster in clusters for item in cluster["unit_ids"]}
    return {str(unit.get("source_path","")).removesuffix("/SKILL.md") for unit in units if unit.get("id") in clustered and str(unit.get("source_path","")).endswith("/SKILL.md")}
def compile_units(workspace:Path)->dict[str,Any]:
    index=load(workspace/"curation/v2/source-index.json")["records"];covered=root_sources(workspace);records=[];root_counts={};errors=[]
    for source in index:
        root=source["root_id"].removeprefix("skill-root:")
        if root in covered:continue
        path=workspace/"skills"/source["path"];lines=path.read_text(encoding="utf-8",errors="replace").splitlines();selected=[]
        for start,end,level,title in sections(lines):
            if title.casefold() in GENERIC or BOILERPLATE.search(title):continue
            if SEMANTIC_HEAD.search(title):selected.append((start,end,title))
        desc_line=next((i for i,line in enumerate(lines,1) if line.strip().startswith("description:")),1);desc_end=min(len(lines),desc_line+4)
        candidates=[(desc_line,desc_end,"Root responsibility"),*selected]
        seen=set();count=0
        for start,end,title in candidates:
            key=(start,title.casefold())
            if key in seen:continue
            seen.add(key);raw,actual_end=excerpt(lines,start,end)
            if not raw:continue
            count+=1;unit_id=f"v2-root:{root}:{count:03d}:{slug(title)}";kind="responsibility" if title=="Root responsibility" else "gate" if re.search(r"(?i)gate|check|validate|verify|readiness",title) else "method"
            records.append({"id":unit_id,"root_id":source["root_id"],"source_path":source["path"],"source_sha256":source["sha256"],"origin_line_start":start,"origin_line_end":actual_end,"type":kind,"title":title,"raw_excerpt":raw,"meaning":f"{title}: {clean(raw,700)}","boundary_condition":"Use only within the root trigger and authority recorded by its V2 dossier; shared gstack preamble is not treated as an atomic capability.","validation_criteria":f"Recompute SHA-256 and verify exact source slice {source['path']}:{start}-{actual_end}.","v2_disposition":"defer","target_cluster_id":None,"decision_id":f"V2-ROOT-ATOM-{len(records)+1:04d}","defer_reason":"No canonical Phase 1 cluster assignment exists for this previously uncovered root; Phase 2 must classify this source-grounded atom into the lifecycle taxonomy before synthesis.","evidence":[f"{source['path']}:{start}-{actual_end}",f"sha256:{source['sha256']}",f"curation/v2/dossiers/{root.replace('/','__')}.json"]})
        root_counts[source["root_id"]]=count
        if count==0:errors.append(f"root produced no atomic units: {source['root_id']}")
    groups:dict[str,list[dict[str,Any]]]=defaultdict(list)
    for unit in records:groups[hashlib.sha256(unit["raw_excerpt"].encode("utf-8")).hexdigest()].append(unit)
    merged=0
    for digest,group in groups.items():
        if len(group)<2:continue
        representative=sorted(group,key=lambda item:(0 if item["root_id"]=="skill-root:gstack" else 1,item["root_id"],item["id"]))[0]
        representative["duplicate_group_sha256"]=digest;representative["duplicate_count"]=len(group)
        for unit in group:
            if unit is representative:continue
            unit.update(v2_disposition="merge",target_unit_id=representative["id"],defer_reason=None,decision_rationale="Exact source slice duplicates the representative derived atom; merge prevents shared runtime or copied guidance from becoming multiple capabilities.",decision_evidence=[f"exact-excerpt-sha256:{digest}",representative["id"],*unit["evidence"]]);merged+=1
    expected={source["root_id"] for source in index if source["root_id"].removeprefix("skill-root:") not in covered}
    if set(root_counts)!=expected:errors.append("missing derived root coverage")
    return {"schema_version":"2.0","gate":"capability-compiler-v2-root-atomic-units","ok":not errors,"previously_clustered_roots":len(covered),"derived_root_count":len(root_counts),"derived_unit_count":len(records),"distinct_excerpt_count":len(groups),"merged_exact_duplicates":merged,"root_unit_counts":root_counts,"units":records,"errors":errors}
def verify(workspace:Path,path:Path)->dict[str,Any]:
    data=load(path);index={item["root_id"]:item for item in load(workspace/"curation/v2/source-index.json")["records"]};covered=root_sources(workspace);expected=set(index)-{"skill-root:"+item for item in covered};errors=[];roots=set()
    all_units={item.get("id"):item for item in data.get("units",[])}
    for unit in data.get("units",[]):
        roots.add(unit.get("root_id"));source=index.get(unit.get("root_id"));path_on_disk=workspace/"skills"/str(unit.get("source_path"));
        if not source or unit.get("source_path")!=source["path"] or unit.get("source_sha256")!=source["sha256"]:errors.append(f"unit source identity mismatch: {unit.get('id')}");continue
        lines=path_on_disk.read_text(encoding="utf-8",errors="replace").splitlines();start=unit.get("origin_line_start");end=unit.get("origin_line_end")
        if not isinstance(start,int) or not isinstance(end,int) or "\n".join(lines[start-1:end]).strip()!=unit.get("raw_excerpt"):errors.append(f"unit excerpt mismatch: {unit.get('id')}")
        disposition=unit.get("v2_disposition")
        if disposition=="defer":
            if not unit.get("defer_reason") or not unit.get("decision_id"):errors.append(f"unit lacks explicit deferred disposition: {unit.get('id')}")
        elif disposition=="merge":
            target=all_units.get(unit.get("target_unit_id"))
            if not target or target.get("raw_excerpt")!=unit.get("raw_excerpt") or not unit.get("decision_id"):errors.append(f"derived merge lacks exact target: {unit.get('id')}")
        else:errors.append(f"invalid derived unit disposition: {unit.get('id')}:{disposition}")
    if roots!=expected:errors.append(f"derived root coverage mismatch: missing={sorted(expected-roots)}, extra={sorted(roots-expected)}")
    return {"gate":"capability-compiler-v2-root-atomic-units-verify","ok":not errors,"derived_root_count":len(roots),"derived_unit_count":len(data.get("units",[])),"errors":errors}
def main()->int:
    p=argparse.ArgumentParser(description=__doc__);p.add_argument("--workspace-root",type=Path,default=Path("."));p.add_argument("--output",type=Path,required=True);p.add_argument("--verify",action="store_true");a=p.parse_args();r=verify(a.workspace_root.resolve(),a.output.resolve()) if a.verify else compile_units(a.workspace_root.resolve());
    if not a.verify:write(a.output.resolve(),r)
    print(json.dumps({k:r[k] for k in r if k not in {"units","root_unit_counts"}},ensure_ascii=False,sort_keys=True));return 0 if r["ok"] else 1
if __name__=="__main__":raise SystemExit(main())
