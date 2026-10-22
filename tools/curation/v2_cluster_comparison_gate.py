#!/usr/bin/env python3
"""Validate complete V2 source matrices and semantic relationship audits for every cluster."""
from __future__ import annotations

import argparse
import json
from itertools import combinations
from pathlib import Path
from typing import Any

try:
    from tools.curation.v2_phase0_audit import load_units
except ModuleNotFoundError:
    from v2_phase0_audit import load_units

RELATION_TYPES={"none","duplicate","complementary","conditional-variant","conflict","strong-dependency"}
DISPOSITIONS={"retain","merge","branch","reject","defer","no-conflict","not-related"}
REQUIRED_DIMENSIONS={"responsibility","method","boundary-and-applicability","inputs-and-outputs","gates-and-validation","permissions-and-side-effects","failure-modes"}
POLICY_REQUIREMENTS={
 "V2-DEC-002":{"cluster:design-context-and-direction-contract","cluster:ui-task-routing-and-governance","cluster:visual-language-and-anti-template-controls","cluster:rendered-ui-critique-and-release-disposition","cluster:content-copy-and-authentic-assets","cluster:responsive-layout-and-spatial-composition","cluster:purposeful-motion-and-animation-engineering"},
 "V2-DEC-005":{"cluster:opportunity-prioritization-and-frameworks"},
 "V2-DEC-003":{"cluster:results-analysis-and-decision-readout","cluster:strategic-choice-and-differentiation","cluster:decision-and-outcome-roadmapping","cluster:evidence-synthesis-and-opportunity-prioritization","cluster:opportunity-prioritization-and-frameworks"},
 "V2-DEC-004":{"cluster:customer-interview-execution","cluster:qualitative-evidence-synthesis","cluster:feedback-and-continuous-learning-loop","cluster:data-analysis-validation","cluster:research-planning-and-governance","cluster:llm-quality-evaluation"},
}

def load(path:Path)->Any:return json.loads(path.read_text(encoding="utf-8"))
def source(unit:dict[str,Any])->str:return str(unit.get("source_path","")).split("/",1)[0]
def verify(workspace:Path,comparisons_root:Path,relationships_path:Path)->dict[str,Any]:
    cluster_data=load(workspace/"curation/clusters.json");clusters=cluster_data["clusters"];expected={item["id"] for item in clusters};units,unit_errors=load_units(workspace/"curation/units");by_id={item["id"]:item for item in units};aux=load(workspace/"curation/v2/units/auxiliary.json")["units"];retained=[item for item in aux if item.get("v2_disposition")=="retain"];retained_by_cluster={cid:[item for item in retained if item.get("target_cluster_id")==cid] for cid in expected};global_unit_ids=set(by_id)|{item["id"] for item in retained}
    errors=list(unit_errors);checked=[]
    comparison_sources={};comparison_units={}
    for cluster in clusters:
        cluster_id=cluster["id"];path=comparisons_root/(cluster_id.removeprefix("cluster:")+".json")
        if not path.is_file():errors.append(f"missing comparison: {cluster_id}");continue
        data=load(path);expected_units=sorted([*cluster["unit_ids"],*(item["id"] for item in retained_by_cluster[cluster_id])]);expected_sources=sorted({source(by_id[item]) for item in cluster["unit_ids"]}|{source(item) for item in retained_by_cluster[cluster_id]})
        if data.get("cluster_id")!=cluster_id:errors.append(f"comparison identity mismatch: {cluster_id}")
        if sorted(data.get("unit_ids",[]))!=expected_units:errors.append(f"comparison unit coverage mismatch: {cluster_id}")
        sources=data.get("sources",[]);source_ids=sorted(item.get("source_id") for item in sources if isinstance(item,dict))
        if source_ids!=expected_sources:errors.append(f"comparison source coverage mismatch: {cluster_id}")
        dimensions=data.get("dimensions",[]);dimension_ids={item.get("id") for item in dimensions if isinstance(item,dict)}
        if dimension_ids!=REQUIRED_DIMENSIONS:errors.append(f"comparison dimension coverage mismatch: {cluster_id}")
        cells=data.get("source_dimension_matrix",[]);pairs={(item.get("source_id"),item.get("dimension_id")) for item in cells if isinstance(item,dict)};expected_cells={(s,d) for s in expected_sources for d in REQUIRED_DIMENSIONS}
        if pairs!=expected_cells:errors.append(f"comparison source-dimension matrix incomplete: {cluster_id}")
        for item in cells:
            if not all(item.get(field) for field in ("approach","strengths","limitations","evidence")):errors.append(f"comparison cell incomplete: {cluster_id}:{item.get('source_id')}:{item.get('dimension_id')}")
            if item.get("approach")==item.get("strengths") or item.get("approach")==item.get("limitations"):errors.append(f"comparison cell copies semantic columns: {cluster_id}:{item.get('source_id')}:{item.get('dimension_id')}")
        if not data.get("missing_dimensions") and data.get("missing_dimensions")!=[]:errors.append(f"comparison lacks missing dimension analysis: {cluster_id}")
        if not data.get("fusion_rules") or not data.get("evidence_citations"):errors.append(f"comparison lacks fusion rules or evidence: {cluster_id}")
        decision_refs=set(data.get("decision_references",[]))
        for decision,cluster_ids in POLICY_REQUIREMENTS.items():
            if cluster_id in cluster_ids and decision not in decision_refs:errors.append(f"comparison lacks required owner policy {decision}: {cluster_id}")
        comparison_sources[cluster_id]=expected_sources;comparison_units[cluster_id]=set(expected_units);checked.append(cluster_id)
    relationship_data=load(relationships_path) if relationships_path.is_file() else {"cluster_audits":[]};audits={item.get("cluster_id"):item for item in relationship_data.get("cluster_audits",[]) if isinstance(item,dict)}
    if set(audits)!=expected:errors.append(f"relationship audit coverage mismatch: missing={sorted(expected-set(audits))}, extra={sorted(set(audits)-expected)}")
    cluster_ids=expected
    for cluster_id,audit in audits.items():
        relations=audit.get("relationships",[]);decisions=audit.get("decisions",[]);source_pairs=audit.get("source_pair_audits",[]);dependencies=audit.get("dependency_audits",[])
        if not decisions:errors.append(f"relationship audit lacks decisions: {cluster_id}")
        expected_pairs={tuple(pair) for pair in combinations(comparison_sources.get(cluster_id,[]),2)};actual_pairs={tuple(sorted((item.get("source_a"),item.get("source_b")))) for item in source_pairs}
        if actual_pairs!=expected_pairs:errors.append(f"relationship source pair coverage mismatch: {cluster_id}")
        for pair in source_pairs:
            if pair.get("type") not in RELATION_TYPES or not pair.get("evidence") or not pair.get("rationale") or not pair.get("decision_id"):errors.append(f"invalid source pair audit: {cluster_id}:{pair}")
        expected_dependencies={("upstream",target) for target in next((c["upstream_dependencies"] for c in clusters if c["id"]==cluster_id),[])}|{("downstream",target) for target in next((c["downstream_dependencies"] for c in clusters if c["id"]==cluster_id),[])}
        actual_dependencies={(item.get("direction"),item.get("target_cluster_id")) for item in dependencies}
        if actual_dependencies!=expected_dependencies:errors.append(f"dependency audit coverage mismatch: {cluster_id}")
        for item in dependencies:
            if item.get("type")!="strong-dependency" or item.get("target_cluster_id") not in cluster_ids or not item.get("evidence"):errors.append(f"invalid dependency audit: {cluster_id}:{item}")
        decision_ids={item.get("id") for item in decisions}
        for relation in relations:
            if relation.get("type") not in RELATION_TYPES-{"none"}:errors.append(f"invalid relationship type: {cluster_id}")
            if not relation.get("source_unit_id") or not relation.get("target_unit_id") or not relation.get("evidence"):errors.append(f"relationship lacks evidence: {cluster_id}")
            if relation.get("source_unit_id") not in global_unit_ids or relation.get("target_unit_id") not in global_unit_ids:errors.append(f"relationship references unknown unit: {cluster_id}")
            if relation.get("decision_id") not in decision_ids:errors.append(f"relationship lacks decision: {cluster_id}")
        decisions_by_id={item.get("id"):item for item in decisions}
        for decision in decisions:
            if decision.get("disposition") not in DISPOSITIONS or not decision.get("rationale") or not decision.get("evidence"):errors.append(f"invalid relationship decision: {cluster_id}:{decision.get('id')}")
        for relation in relations:
            if relation.get("type")=="conflict" and decisions_by_id.get(relation.get("decision_id"),{}).get("disposition") not in {"branch","reject","defer"}:errors.append(f"conflict decision does not resolve behavior: {cluster_id}:{relation.get('id')}")
        if any(pair.get("decision_id") not in decision_ids for pair in source_pairs):errors.append(f"source pair lacks decision: {cluster_id}")
        if any(relation.get("type")=="conflict" and relation.get("decision_id") not in decision_ids for relation in relations):errors.append(f"unresolved conflict: {cluster_id}")
    return {"gate":"capability-compiler-v2-cluster-comparisons","ok":not errors,"cluster_count":len(expected),"comparison_count":len(checked),"relationship_audit_count":len(audits),"canonical_unit_count":sum(len(c["unit_ids"]) for c in clusters),"retained_auxiliary_count":len(retained),"errors":errors}
def main()->int:
    p=argparse.ArgumentParser(description=__doc__);p.add_argument("--workspace-root",type=Path,default=Path("."));p.add_argument("--comparisons-root",type=Path,required=True);p.add_argument("--relationships",type=Path,required=True);a=p.parse_args();r=verify(a.workspace_root.resolve(),a.comparisons_root.resolve(),a.relationships.resolve());print(json.dumps(r,ensure_ascii=False,sort_keys=True));return 0 if r["ok"] else 1
if __name__=="__main__":raise SystemExit(main())
