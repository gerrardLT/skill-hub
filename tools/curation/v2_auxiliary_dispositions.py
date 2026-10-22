#!/usr/bin/env python3
"""Apply explicit, source-grounded dispositions to all 114 V2 auxiliary units."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path
from typing import Any

try:
    from tools.curation.v2_auxiliary_units import verify_disposed
except ModuleNotFoundError:
    from v2_auxiliary_units import verify_disposed

SOURCE_DEFAULTS={
 "canary":"cluster:production-canary-monitoring","code-review":"cluster:independent-code-review","executing-plans":"cluster:plan-execution-control",
 "impeccable":"cluster:design-context-and-direction-contract","prd-development":"cluster:requirements-and-delivery-contract",
 "pre-mortem":"cluster:risk-preflight-and-safety-governance","qa-only":"cluster:independent-blackbox-qa","requesting-code-review":"cluster:independent-code-review",
 "retro":"cluster:engineering-retrospective-and-improvement","ship":"cluster:change-delivery-preflight","subagent-driven-development":"cluster:subagent-task-pipeline",
 "systematic-debugging":"cluster:root-cause-investigation","test-case-generator":"cluster:testing-portfolio-strategy","test-driven-development":"cluster:tdd-change-loop",
 "ui-ux-pro-max":"cluster:ui-task-routing-and-governance","verification-before-completion":"cluster:completion-evidence-gate",
 "web-accessibility":"cluster:accessibility-contracts-and-assistive-validation","writing-plans":"cluster:implementation-planning-and-handoff",
}
OVERRIDES={
 "skills/pre-mortem/SKILL.md:80-80":"cluster:artifact-persistence-and-tool-actions",
 "skills/qa-only/SKILL.md:398-403":"cluster:baseline-regression-control",
 "skills/prd-development/SKILL.md:8-12":"cluster:problem-framing-and-customer-research",
 "skills/prd-development/SKILL.md:18-45":"cluster:problem-framing-and-customer-research",
 "skills/prd-development/SKILL.md:48-62":"cluster:problem-framing-and-customer-research",
 "skills/prd-development/SKILL.md:164-172":"cluster:requirements-and-delivery-contract",
 "skills/prd-development/SKILL.md:220-228":"cluster:requirements-and-delivery-contract",
 "skills/prd-development/SKILL.md:230-235":"cluster:requirements-and-delivery-contract",
 "skills/prd-development/SKILL.md:240-248":"cluster:requirements-and-delivery-contract",
 "skills/prd-development/SKILL.md:252-258":"cluster:artifact-persistence-and-tool-actions",
 "skills/ui-ux-pro-max/SKILL.md:33-55":"cluster:design-system-foundation-and-token-extraction",
 "skills/ui-ux-pro-max/SKILL.md:58-68":"cluster:design-system-foundation-and-token-extraction",
 "skills/ui-ux-pro-max/SKILL.md:142-149":"cluster:design-context-and-direction-contract",
 "skills/ui-ux-pro-max/SKILL.md:212-214":"cluster:cross-domain-ui-preflight-checklists",
 "impeccable:craft-floor:states-complete":"cluster:interaction-states-forms-and-navigation",
 "impeccable:craft-floor:verify-layout":"cluster:rendered-ui-critique-and-release-disposition",
 "impeccable:craft-floor:verify-spacing":"cluster:rendered-ui-critique-and-release-disposition",
 "impeccable:craft-floor:verify-type-measure":"cluster:rendered-ui-critique-and-release-disposition",
 "impeccable:craft-floor:verify-font-weight":"cluster:rendered-ui-critique-and-release-disposition",
 "impeccable:craft-floor:verify-images":"cluster:rendered-ui-critique-and-release-disposition",
 "impeccable:craft-floor:refuse-modal-default":"cluster:interaction-states-forms-and-navigation",
 "impeccable:craft-floor:refuse-unicode-icons":"cluster:design-system-foundation-and-token-extraction",
 "impeccable:craft-floor:refuse-light-dark-by-category":"cluster:design-context-and-direction-contract",
}
EXACT_MERGE={
 "skills/qa-only/SKILL.md:429-431":("qao-rule-blackbox-identity","cluster:independent-blackbox-qa","canonical"),
 "skills/ship/SKILL.md:5-5-review":("skills/ship/SKILL.md:5-5","cluster:change-delivery-preflight","auxiliary"),
}
RELOCATIONS={
 "skills/subagent-driven-development/SKILL.md:summary:parallel-tasks":(3,10),
 "skills/prd-development/SKILL.md:23-29":(20,21),
 "skills/pre-mortem/SKILL.md:80-80":(79,79),
 "skills/ship/SKILL.md:316-316":(318,318),
 "skills/ship/SKILL.md:12-20":(8,20),
 "skills/canary/SKILL.md:6-11":(5,11),
 "skills/ui-ux-pro-max/SKILL.md:22-31":(20,20),
 "skills/ui-ux-pro-max/SKILL.md:176-187":(174,189),
 "skills/ui-ux-pro-max/SKILL.md:41-43":(39,42),
}
MIN_SOURCE_SUPPORT=.75

def load(path:Path)->Any:return json.loads(path.read_text(encoding="utf-8"))
def write(path:Path,value:Any)->None:path.parent.mkdir(parents=True,exist_ok=True);path.write_text(json.dumps(value,ensure_ascii=False,indent=2,sort_keys=True)+"\n",encoding="utf-8",newline="\n")
def source_support(workspace:Path,unit:dict[str,Any])->tuple[str,float,int,int]:
    path=workspace/"skills"/unit["source_path"];lines=path.read_text(encoding="utf-8",errors="replace").splitlines();start,end=RELOCATIONS.get(unit["id"],(unit["origin_line_start"],unit["origin_line_end"]));source="\n".join(lines[start-1:end]);raw=str(unit["raw_excerpt"])
    normalize=lambda value: re.sub(r"[^\w]+"," ",value.casefold()).strip()
    expected=normalize(raw);actual=normalize(source)
    if expected==actual:return "exact-source-slice",1.0,start,end
    tokens=set(expected.split());support=len(tokens & set(actual.split()))/len(tokens) if tokens else 0.0
    kind="relocated-source-supported-summary" if unit["id"] in RELOCATIONS and support>=MIN_SOURCE_SUPPORT else "source-supported-summary" if support>=MIN_SOURCE_SUPPORT else "unsupported-summary"
    return kind,round(support,4),start,end

def apply(workspace:Path,auxiliary_path:Path,matches_path:Path)->dict[str,Any]:
    data=load(auxiliary_path);matches={item["auxiliary_unit_id"]:item for item in load(matches_path)["matches"]};clusters={item["id"] for item in load(workspace/"curation/clusters.json")["clusters"]};errors=[];counts={}
    for index,unit in enumerate(data["units"],1):
        unit_id=unit["id"];source=unit["source_path"].split("/",1)[0];decision_id=f"V2-AUX-{index:03d}";validation,support,start,end=source_support(workspace,unit)
        unit.update(source_validation=validation,source_support_score=support,validated_line_start=start,validated_line_end=end)
        if validation=="unsupported-summary":
            unit.update(v2_disposition="defer",target_unit_id=None,target_cluster_id=None,decision_id=decision_id,defer_reason="Legacy auxiliary summary is not sufficiently supported by its declared immutable source or any approved relocated range; re-extract from source before fusion.",decision_rationale="Deferred rather than guessed because source support is below the 0.75 evidence threshold.",decision_evidence=[f"{unit['source_path']}:{start}-{end}",f"source-token-support:{support}"])
        elif unit_id in EXACT_MERGE:
            target,cluster,target_kind=EXACT_MERGE[unit_id]
            if target_kind=="canonical":
                candidate=next((item for item in matches[unit_id]["candidates"] if item["unit_id"]==target),None)
                if not candidate or not candidate["evidence"]["exact_excerpt"]:errors.append(f"exact merge evidence missing: {unit_id}")
            else:
                target_unit=next((item for item in data["units"] if item["id"]==target),None)
                normalize=lambda value: re.sub(r"\s+"," ",str(value)).strip().casefold()
                if not target_unit or normalize(target_unit.get("raw_excerpt"))!=normalize(unit.get("raw_excerpt")):errors.append(f"auxiliary exact merge evidence missing: {unit_id}")
            unit.update(v2_disposition="merge",target_unit_id=target,target_cluster_id=cluster,decision_id=decision_id,defer_reason=None,decision_rationale=f"Exact source excerpt duplicates an existing {target_kind} unit; merge preserves one behavior identity.",decision_evidence=[f"exact-target:{target}",f"{unit['source_path']}:{start}-{end}",f"source-token-support:{support}"])
        else:
            cluster=OVERRIDES.get(unit_id,SOURCE_DEFAULTS.get(source))
            if cluster not in clusters:errors.append(f"unknown retained cluster: {unit_id}:{cluster}")
            policy=" Contextual aesthetic variant; V2-DEC-002 forbids promotion to a universal style rule." if source=="impeccable" and unit_id.startswith("impeccable:craft-floor:refuse-") else ""
            unit.update(v2_disposition="retain",target_unit_id=None,target_cluster_id=cluster,decision_id=decision_id,defer_reason=None,decision_rationale=f"Distinct source-grounded atomic contribution retained in {cluster}; no exact canonical duplicate was proven.{policy}",decision_evidence=[f"{unit['source_path']}:{start}-{end}",f"source-token-support:{support}","curation/v2/units/auxiliary-matches.json","curation/v2/fusion-policy.json"])
        counts[unit["v2_disposition"]]=counts.get(unit["v2_disposition"],0)+1
    errors.extend(verify_disposed(data));data.update(ok=not errors,errors=errors,disposition_counts=counts,decision_policy="exact-excerpt-only-merge; otherwise retain distinct evidenced atom in an explicit semantic cluster")
    return data

def main()->int:
    p=argparse.ArgumentParser(description=__doc__);p.add_argument("--workspace-root",type=Path,default=Path("."));p.add_argument("--auxiliary",type=Path,required=True);p.add_argument("--matches",type=Path,required=True);p.add_argument("--output",type=Path,required=True);a=p.parse_args();r=apply(a.workspace_root.resolve(),a.auxiliary.resolve(),a.matches.resolve());write(a.output.resolve(),r);print(json.dumps({"gate":"capability-compiler-v2-auxiliary-dispositions","ok":r["ok"],"count":r["count"],"disposition_counts":r["disposition_counts"],"errors":r["errors"]},ensure_ascii=False,sort_keys=True));return 0 if r["ok"] else 1
if __name__=="__main__":raise SystemExit(main())
