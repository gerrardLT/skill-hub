#!/usr/bin/env python3
"""Compile source-by-dimension matrices and relationship audits for 88 V2 clusters."""
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
from collections import Counter,defaultdict
from itertools import combinations
from pathlib import Path
from typing import Any

try:
    from tools.curation.v2_phase0_audit import load_units
except ModuleNotFoundError:
    from v2_phase0_audit import load_units

DIMENSIONS={
 "responsibility":"What responsibility the source contributes to this cluster.",
 "method":"Methods, phases, tools, or templates contributed by the source.",
 "boundary-and-applicability":"Applicability, exceptions, variants, and non-responsibilities.",
 "inputs-and-outputs":"Inputs consumed and artifacts or decisions produced.",
 "gates-and-validation":"Rules, gates, evidence checks, and validation criteria.",
 "permissions-and-side-effects":"Tools, mutation authority, external effects, and consent boundaries.",
 "failure-modes":"Known limitations, failure modes, and unsupported assumptions.",
}
TYPE_DIMENSION={"method":"method","template":"inputs-and-outputs","rule":"gates-and-validation","gate":"gates-and-validation","exception":"boundary-and-applicability","example":"method","tool-action":"permissions-and-side-effects"}
AESTHETIC_CLUSTERS={"cluster:design-context-and-direction-contract","cluster:ui-task-routing-and-governance","cluster:visual-language-and-anti-template-controls","cluster:rendered-ui-critique-and-release-disposition","cluster:content-copy-and-authentic-assets","cluster:responsive-layout-and-spatial-composition","cluster:purposeful-motion-and-animation-engineering"}
DATA_GOVERNANCE_CLUSTERS={"cluster:customer-interview-execution","cluster:qualitative-evidence-synthesis","cluster:feedback-and-continuous-learning-loop","cluster:data-analysis-validation","cluster:research-planning-and-governance","cluster:llm-quality-evaluation"}
HUMAN_DECISION_CLUSTERS={"cluster:results-analysis-and-decision-readout","cluster:strategic-choice-and-differentiation","cluster:decision-and-outcome-roadmapping","cluster:evidence-synthesis-and-opportunity-prioritization","cluster:opportunity-prioritization-and-frameworks"}

def load(path:Path)->Any:return json.loads(path.read_text(encoding="utf-8"))
def write(path:Path,value:Any)->None:path.parent.mkdir(parents=True,exist_ok=True);path.write_text(json.dumps(value,ensure_ascii=False,indent=2,sort_keys=True)+"\n",encoding="utf-8",newline="\n")
def source(unit:dict[str,Any])->str:return str(unit.get("source_path","")).split("/",1)[0]
def citation(unit:dict[str,Any])->str:return f"{unit['source_path']}:{unit['origin_line_start']}-{unit['origin_line_end']}"
def dimension_units(units:list[dict[str,Any]],dimension:str)->list[dict[str,Any]]:
    if dimension=="responsibility":return units
    if dimension=="method":return [unit for unit in units if unit.get("type") in {"method","template","example","tool-action"}]
    if dimension=="boundary-and-applicability":return [unit for unit in units if unit.get("boundary_condition")]
    if dimension=="inputs-and-outputs":return [unit for unit in units if unit.get("type")=="template"]
    if dimension=="gates-and-validation":return [unit for unit in units if unit.get("type") in {"rule","gate"}]
    if dimension=="permissions-and-side-effects":return [unit for unit in units if unit.get("type")=="tool-action"]
    return [unit for unit in units if unit.get("type")=="exception"]
def summarize(units:list[dict[str,Any]],dimension:str,field:str)->str:
    explicit=dimension_units(units,dimension)
    if not explicit:
        defaults={"approach":f"No explicit {dimension} atom is present; infer nothing beyond the cited source units.","strengths":f"No evidenced strength is claimed for {dimension}.","limitations":f"Missing explicit {dimension} coverage; Phase 2 synthesis must add or defer it."}
        return defaults[field]
    if field=="approach":
        values=[unit.get("boundary_condition") if dimension=="boundary-and-applicability" else unit.get("validation_criteria") if dimension=="gates-and-validation" else unit.get("meaning") for unit in explicit]
        return "; ".join(str(value).strip() for value in values[:3] if value)[:1400]
    if field=="strengths":
        types=", ".join(f"{kind}={count}" for kind,count in sorted(Counter(unit.get("type") for unit in explicit).items()))
        return f"Provides {len(explicit)} source-grounded atom(s) for {dimension} ({types}); each is bound to an exact source citation."
    boundaries=[str(unit.get("boundary_condition")).strip() for unit in explicit if unit.get("boundary_condition")]
    if boundaries:return ("Explicit limits: "+"; ".join(boundaries[:3]))[:1400]
    return f"The source provides {dimension} guidance but does not define a broader cross-source applicability or authority contract."
def policy_rules(cluster_id:str)->tuple[list[dict[str,Any]],list[str]]:
    rules=[];decisions=[]
    if cluster_id in AESTHETIC_CLUSTERS:
        decisions.append("V2-DEC-002");rules.append({"id":f"{cluster_id}:policy:contextual-aesthetics","rule":"Treat typography, color, card, eyebrow, theme, motion, and other aesthetic prescriptions as context-selected variants. Only accessibility, safety, and performance constraints may be global hard rules.","evidence":["curation/v2/fusion-policy.json:V2-DEC-002"]})
    if cluster_id=="cluster:opportunity-prioritization-and-frameworks":
        decisions.append("V2-DEC-005");rules.append({"id":f"{cluster_id}:policy:named-formulas","rule":"Preserve named formula variants. Every score must record framework name, exact formula, variable definitions, assumptions, and selected or custom variant.","evidence":["curation/v2/fusion-policy.json:V2-DEC-005"]})
    if cluster_id in HUMAN_DECISION_CLUSTERS:
        decisions.append("V2-DEC-003");rules.append({"id":f"{cluster_id}:policy:human-decision","rule":"Produce evidence-backed recommendations and unknowns; GO, PIVOT, KILL, prioritization adoption, roadmap commitment, and build approval remain human decisions.","evidence":["curation/v2/fusion-policy.json:V2-DEC-003"]})
    if cluster_id in DATA_GOVERNANCE_CLUSTERS:
        decisions.append("V2-DEC-004");rules.append({"id":f"{cluster_id}:policy:data-governance","rule":"Before processing customer, proprietary, recorded, or externally judged data, require authorization, minimization, redaction, retention, external-transfer boundary, and deletion policy; otherwise return needs-input or blocked.","evidence":["curation/v2/fusion-policy.json:V2-DEC-004"]})
    return rules,sorted(set(decisions))
def compile_all(workspace:Path,comparisons_root:Path,relationships_path:Path)->dict[str,Any]:
    cluster_data=load(workspace/"curation/clusters.json");clusters=cluster_data["clusters"];canonical,errors=load_units(workspace/"curation/units");by_id={item["id"]:item for item in canonical};aux=load(workspace/"curation/v2/units/auxiliary.json")["units"];retained=[item for item in aux if item.get("v2_disposition")=="retain"];retained_by_cluster=defaultdict(list)
    for item in retained:retained_by_cluster[item["target_cluster_id"]].append(item)
    legacy_by_cluster=defaultdict(list)
    for item in cluster_data.get("relationships",[]):legacy_by_cluster[item["cluster_id"]].append(item)
    if comparisons_root.exists():shutil.rmtree(comparisons_root)
    comparisons_root.mkdir(parents=True);audits=[];relationship_count=0;pair_count=0
    global_units={**by_id,**{item["id"]:item for item in retained}}
    for cluster_index,cluster in enumerate(clusters,1):
        cluster_id=cluster["id"];units=[by_id[item] for item in cluster["unit_ids"]]+retained_by_cluster[cluster_id];source_groups=defaultdict(list)
        for unit in units:source_groups[source(unit)].append(unit)
        sources=[];cells=[];evidence=[]
        for source_id in sorted(source_groups):
            source_units=source_groups[source_id];unit_ids=sorted(item["id"] for item in source_units);cites=sorted({citation(item) for item in source_units});evidence.extend(cites)
            sources.append({"source_id":source_id,"unit_ids":unit_ids,"contribution_types":dict(sorted(Counter(item.get("type") for item in source_units).items())),"evidence":cites})
            for dimension in DIMENSIONS:
                explicit=dimension_units(source_units,dimension)
                cells.append({"source_id":source_id,"dimension_id":dimension,"approach":summarize(source_units,dimension,"approach"),"strengths":summarize(source_units,dimension,"strengths"),"limitations":summarize(source_units,dimension,"limitations"),"coverage":"explicit" if explicit else "missing-explicit-atom","unit_ids":sorted(item["id"] for item in explicit),"evidence":sorted({citation(item) for item in explicit}) or cites})
        missing=[]
        for dimension in DIMENSIONS:
            absent=sorted(source_id for source_id in source_groups if next(item for item in cells if item["source_id"]==source_id and item["dimension_id"]==dimension)["coverage"]!="explicit")
            if absent:missing.append({"dimension_id":dimension,"sources":absent,"disposition":"preserve-as-gap-for-phase-2"})
        policy_specific,decision_refs=policy_rules(cluster_id)
        fusion_rules=[
          {"id":f"{cluster_id}:fusion:boundary","rule":cluster["candidate_responsibility"],"evidence":[f"curation/clusters.json:{cluster_id}"]},
          {"id":f"{cluster_id}:fusion:inputs","rule":f"Accept only: {cluster['input_boundary']}","evidence":[f"curation/clusters.json:{cluster_id}"]},
          {"id":f"{cluster_id}:fusion:outputs","rule":f"Produce only: {cluster['output_boundary']}","evidence":[f"curation/clusters.json:{cluster_id}"]},
          {"id":f"{cluster_id}:fusion:evidence","rule":"Preserve explicit source variants and gaps; never upgrade a missing dimension or source preference into a universal rule.","evidence":["curation/v2/fusion-policy.json"]},
          *policy_specific,
        ]
        comparison={"schema_version":"2.0","cluster_id":cluster_id,"candidate_responsibility":cluster["candidate_responsibility"],"input_boundary":cluster["input_boundary"],"output_boundary":cluster["output_boundary"],"decision_references":decision_refs,"unit_ids":sorted(item["id"] for item in units),"canonical_unit_ids":sorted(cluster["unit_ids"]),"retained_auxiliary_unit_ids":sorted(item["id"] for item in retained_by_cluster[cluster_id]),"sources":sources,"dimensions":[{"id":key,"question":value} for key,value in DIMENSIONS.items()],"source_dimension_matrix":cells,"missing_dimensions":missing,"fusion_rules":fusion_rules,"evidence_citations":sorted(set(evidence))}
        write(comparisons_root/(cluster_id.removeprefix("cluster:")+".json"),comparison)
        decisions=[];relations=[];source_pairs=[]
        legacy=legacy_by_cluster[cluster_id]
        existing_pairs={frozenset((item["source_unit_id"],item["target_unit_id"])) for item in legacy};exact_groups=defaultdict(list)
        for unit in units:
            normalized=" ".join(str(unit.get("raw_excerpt","")).split()).casefold()
            if normalized:exact_groups[hashlib.sha256(normalized.encode("utf-8")).hexdigest()].append(unit)
        inferred=[]
        for digest,group in sorted(exact_groups.items()):
            if len(group)<2:continue
            representative=sorted(group,key=lambda item:item["id"])[0]
            for duplicate in sorted(group,key=lambda item:item["id"])[1:]:
                pair=frozenset((representative["id"],duplicate["id"]))
                if pair in existing_pairs:continue
                inferred.append({"cluster_id":cluster_id,"id":f"relationship:v2-exact-duplicate:{digest[:12]}:{len(inferred)+1}","source_unit_id":representative["id"],"target_unit_id":duplicate["id"],"type":"duplicate","evidence":f"normalized-excerpt-sha256:{digest}","resolution":"Merge into one semantic behavior while preserving both provenance citations."});existing_pairs.add(pair)
        explicit_relations=[*legacy,*inferred]
        pair_to_legacy=defaultdict(list)
        for relation in explicit_relations:
            a=source(global_units[relation["source_unit_id"]]);b=source(global_units[relation["target_unit_id"]]);pair_to_legacy[tuple(sorted((a,b)))].append(relation)
        for pair_index,(a,b) in enumerate(combinations(sorted(source_groups),2),1):
            decision_id=f"V2-REL-{cluster_index:03d}-PAIR-{pair_index:03d}";matched=pair_to_legacy.get((a,b),[])
            if matched:
                relation_type="conflict" if any(item["type"]=="conflict" for item in matched) else "conditional-variant" if any(item["type"]=="conditional-variant" for item in matched) else "strong-dependency" if any(item["type"]=="strong-dependency" for item in matched) else "complementary" if any(item["type"]=="complementary" for item in matched) else "duplicate"
                rationale="Legacy source-grounded relationship evidence exists for this source pair; preserve its conditions and resolution."
                pair_evidence=[item["id"] for item in matched]
                disposition="branch" if relation_type in {"conflict","conditional-variant"} else "merge" if relation_type=="duplicate" else "retain"
            else:
                relation_type="none";rationale="No source-grounded cross-source relationship is proven beyond co-membership in this cluster; do not invent one.";pair_evidence=[*sources[[x["source_id"] for x in sources].index(a)]["evidence"][:1],*sources[[x["source_id"] for x in sources].index(b)]["evidence"][:1]];disposition="not-related"
            decisions.append({"id":decision_id,"disposition":disposition,"rationale":rationale,"evidence":pair_evidence});source_pairs.append({"source_a":a,"source_b":b,"type":relation_type,"rationale":rationale,"evidence":pair_evidence,"decision_id":decision_id});pair_count+=1
        for relation_index,relation in enumerate(explicit_relations,1):
            decision_id=f"V2-REL-{cluster_index:03d}-LEGACY-{relation_index:03d}"
            if relation["type"]=="duplicate":disposition="merge"
            elif relation["type"] in {"conflict","conditional-variant"}:disposition="branch"
            else:disposition="retain"
            relation_evidence=[relation["id"],citation(global_units[relation["source_unit_id"]]),citation(global_units[relation["target_unit_id"]])]
            if relation.get("evidence"):relation_evidence.append(str(relation["evidence"]))
            decisions.append({"id":decision_id,"disposition":disposition,"rationale":relation.get("resolution") or relation.get("design_case") or f"Preserve the existing {relation['type']} relationship and its applicability conditions.","evidence":relation_evidence})
            relations.append({"id":relation["id"],"type":relation["type"],"source_unit_id":relation["source_unit_id"],"target_unit_id":relation["target_unit_id"],"evidence":relation_evidence,"conditions":relation.get("condition") or relation.get("applicability_conditions"),"decision_id":decision_id});relationship_count+=1
        if not decisions:
            decisions.append({"id":f"V2-REL-{cluster_index:03d}-SINGLE","disposition":"no-conflict","rationale":"Single-source cluster has no cross-source pair and no explicit intra-source relationship requiring a separate fusion decision.","evidence":comparison["evidence_citations"][:1]})
        dependencies=[]
        for direction,key in (("upstream","upstream_dependencies"),("downstream","downstream_dependencies")):
            for target in cluster[key]:dependencies.append({"direction":direction,"target_cluster_id":target,"type":"strong-dependency","evidence":[f"curation/clusters.json:{cluster_id}:{key}"]})
        audits.append({"cluster_id":cluster_id,"source_pair_audits":source_pairs,"relationships":relations,"dependency_audits":dependencies,"decisions":decisions,"unresolved_conflicts":[]})
    relationships={"schema_version":"2.0","cluster_audits":audits,"counts":{"clusters":len(audits),"source_pair_audits":pair_count,"explicit_unit_relationships":relationship_count,"unresolved_conflicts":0},"policy":"Only legacy source-grounded or exact evidence may assert a non-none relationship; cluster co-membership alone is not relationship evidence."};write(relationships_path,relationships)
    return {"gate":"capability-compiler-v2-cluster-comparison-compile","ok":not errors,"cluster_count":len(clusters),"canonical_unit_count":sum(len(item["unit_ids"]) for item in clusters),"retained_auxiliary_count":len(retained),"source_pair_audit_count":pair_count,"explicit_relationship_count":relationship_count,"errors":errors}
def main()->int:
    p=argparse.ArgumentParser(description=__doc__);p.add_argument("--workspace-root",type=Path,default=Path("."));p.add_argument("--comparisons-root",type=Path,required=True);p.add_argument("--relationships",type=Path,required=True);a=p.parse_args();r=compile_all(a.workspace_root.resolve(),a.comparisons_root.resolve(),a.relationships.resolve());print(json.dumps(r,ensure_ascii=False,sort_keys=True));return 0 if r["ok"] else 1
if __name__=="__main__":raise SystemExit(main())
