#!/usr/bin/env python3
"""Propose evidence-backed canonical matches for auxiliary units without deciding disposition."""
from __future__ import annotations

import argparse
import difflib
import json
import re
from pathlib import Path
from typing import Any

try:
    from tools.curation.v2_phase0_audit import load_units
except ModuleNotFoundError:
    from v2_phase0_audit import load_units


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))

def write(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")

def normalized(text: Any) -> str:
    return re.sub(r"\s+", " ", str(text or "")).strip().casefold()

def line_overlap(a: dict[str, Any], b: dict[str, Any]) -> float:
    if a.get("source_path") != b.get("source_path"):
        return 0.0
    starts = (a.get("origin_line_start"), b.get("origin_line_start"));ends=(a.get("origin_line_end"),b.get("origin_line_end"))
    if not all(isinstance(value,int) for value in starts+ends):
        return 0.0
    intersection=max(0,min(ends)-max(starts)+1);union=max(ends)-min(starts)+1
    return intersection/union if union else 0.0

def propose(workspace: Path, auxiliary_path: Path) -> dict[str, Any]:
    units, errors = load_units(workspace / "curation/units")
    clusters = load(workspace / "curation/clusters.json")
    clustered={unit_id:cluster["id"] for cluster in clusters["clusters"] for unit_id in cluster["unit_ids"]}
    canonical=[unit for unit in units if unit.get("id") in clustered]
    auxiliary=load(auxiliary_path)
    results=[]
    for item in auxiliary["units"]:
        candidates=[]
        excerpt=normalized(item.get("raw_excerpt"));meaning=normalized(item.get("meaning"))
        for unit in canonical:
            exact_excerpt=bool(excerpt and excerpt==normalized(unit.get("raw_excerpt")))
            overlap=line_overlap(item,unit)
            excerpt_similarity=difflib.SequenceMatcher(None,excerpt,normalized(unit.get("raw_excerpt"))).ratio() if excerpt else 0.0
            meaning_similarity=difflib.SequenceMatcher(None,meaning,normalized(unit.get("meaning"))).ratio() if meaning else 0.0
            score=max(1.0 if exact_excerpt else 0.0, overlap, excerpt_similarity*0.9, meaning_similarity*0.7)
            if score>=0.55:
                candidates.append({"unit_id":unit["id"],"cluster_id":clustered[unit["id"]],"score":round(score,4),"evidence":{"exact_excerpt":exact_excerpt,"line_overlap":round(overlap,4),"excerpt_similarity":round(excerpt_similarity,4),"meaning_similarity":round(meaning_similarity,4)}})
        candidates.sort(key=lambda value:(-value["score"],value["unit_id"]))
        results.append({"auxiliary_unit_id":item["id"],"source_path":item["source_path"],"candidates":candidates[:5],"recommendation":"exact-match-review" if candidates and candidates[0]["evidence"]["exact_excerpt"] else "manual-semantic-review"})
    return {"schema_version":"2.0","gate":"capability-compiler-v2-auxiliary-match","ok":not errors and len(results)==114,"count":len(results),"exact_match_suggestions":sum(item["recommendation"]=="exact-match-review" for item in results),"manual_review":sum(item["recommendation"]=="manual-semantic-review" for item in results),"matches":results,"errors":errors}

def main()->int:
    p=argparse.ArgumentParser(description=__doc__);p.add_argument("--workspace-root",type=Path,default=Path("."));p.add_argument("--auxiliary",type=Path,required=True);p.add_argument("--output",type=Path,required=True);a=p.parse_args();r=propose(a.workspace_root.resolve(),a.auxiliary.resolve());write(a.output.resolve(),r);print(json.dumps({k:r[k] for k in ("gate","ok","count","exact_match_suggestions","manual_review","errors")},ensure_ascii=False,sort_keys=True));return 0 if r["ok"] else 1
if __name__=="__main__":raise SystemExit(main())
