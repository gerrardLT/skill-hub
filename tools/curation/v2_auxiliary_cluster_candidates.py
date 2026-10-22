#!/usr/bin/env python3
"""Propose V2 cluster destinations for auxiliary units from canonical source evidence."""
from __future__ import annotations

import argparse
import json
from collections import Counter,defaultdict
from pathlib import Path
from typing import Any

try:
    from tools.curation.v2_phase0_audit import load_units
except ModuleNotFoundError:
    from v2_phase0_audit import load_units

def load(path:Path)->Any:return json.loads(path.read_text(encoding="utf-8"))
def write(path:Path,value:Any)->None:path.parent.mkdir(parents=True,exist_ok=True);path.write_text(json.dumps(value,ensure_ascii=False,indent=2,sort_keys=True)+"\n",encoding="utf-8",newline="\n")
def propose(workspace:Path,auxiliary_path:Path,matches_path:Path)->dict:
    units,errors=load_units(workspace/"curation/units");clusters=load(workspace/"curation/clusters.json")["clusters"];aux=load(auxiliary_path);matches=load(matches_path)
    unit_cluster={unit_id:cluster["id"] for cluster in clusters for unit_id in cluster["unit_ids"]};canonical={u["id"]:u for u in units if u.get("id") in unit_cluster}
    source_clusters:dict[str,Counter]=defaultdict(Counter)
    for unit_id,unit in canonical.items():
        source=str(unit.get("source_path","")).removeprefix("skills/").split("/",1)[0];source_clusters[source][unit_cluster[unit_id]]+=1
    matches_by_id={item["auxiliary_unit_id"]:item for item in matches["matches"]};results=[]
    for item in aux["units"]:
        source=item["source_path"].split("/",1)[0];match=matches_by_id[item["id"]];scores=Counter()
        for candidate in match["candidates"]:scores[candidate["cluster_id"]]+=candidate["score"]*3
        for cluster_id,count in source_clusters.get(source,{}).items():scores[cluster_id]+=count/max(1,sum(source_clusters[source].values()))
        candidates=[{"cluster_id":cluster_id,"score":round(score,4),"evidence":{"semantic_match":next((c for c in match["candidates"] if c["cluster_id"]==cluster_id),None),"canonical_same_source_units":source_clusters.get(source,{}).get(cluster_id,0)}} for cluster_id,score in scores.most_common(5)]
        results.append({"auxiliary_unit_id":item["id"],"source":source,"candidates":candidates,"requires_semantic_decision":True})
    return {"schema_version":"2.0","gate":"capability-compiler-v2-auxiliary-cluster-candidates","ok":not errors and len(results)==114,"count":len(results),"without_candidates":sum(not x["candidates"] for x in results),"records":results,"errors":errors}
def main()->int:
    p=argparse.ArgumentParser(description=__doc__);p.add_argument("--workspace-root",type=Path,default=Path("."));p.add_argument("--auxiliary",type=Path,required=True);p.add_argument("--matches",type=Path,required=True);p.add_argument("--output",type=Path,required=True);a=p.parse_args();r=propose(a.workspace_root.resolve(),a.auxiliary.resolve(),a.matches.resolve());write(a.output.resolve(),r);print(json.dumps({k:r[k] for k in ("gate","ok","count","without_candidates","errors")},ensure_ascii=False,sort_keys=True));return 0 if r["ok"] else 1
if __name__=="__main__":raise SystemExit(main())
