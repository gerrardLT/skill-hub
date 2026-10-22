#!/usr/bin/env python3
"""Validate owner-approved Capability Compiler V2 fusion policy."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

EXPECTED_DECISIONS={f"V2-DEC-{number:03d}" for number in range(1,8)}

def load(path:Path):return json.loads(path.read_text(encoding="utf-8"))
def verify(workspace:Path)->dict:
    policy=load(workspace/"curation/v2/fusion-policy.json");errors=[]
    decisions=[]
    for line in (workspace/"curation/v2/decisions.jsonl").read_text(encoding="utf-8").splitlines():
        if line.strip():decisions.append(json.loads(line))
    approved={item.get("id") for item in decisions if item.get("authority")=="user" and item.get("status")=="approved"}
    if approved!=EXPECTED_DECISIONS:errors.append(f"approved decision set mismatch: {sorted(approved)}")
    if set(policy.get("decision_references",[]))!=EXPECTED_DECISIONS:errors.append("fusion policy does not cite every approved decision")
    if policy.get("skill_architecture",{}).get("production_unit")!="atomic-skill" or policy["skill_architecture"].get("monolith_disposition")!="source-or-recipe":errors.append("monolith decomposition policy mismatch")
    if policy.get("global_hard_rules",{}).get("aesthetic_rules")!="contextual-variants":errors.append("aesthetic rules were promoted globally")
    if policy.get("product_authority",{}).get("final_decision_authority")!="human" or policy["product_authority"].get("automatic-build-approval") is not False:errors.append("product authority is not human-owned")
    if policy.get("data_governance",{}).get("required") is not True or len(policy["data_governance"].get("required_fields",[]))<6:errors.append("mandatory data governance is incomplete")
    if policy.get("named_frameworks",{}).get("formula_policy")!="named-variants" or policy["named_frameworks"].get("universal-formula_claim_allowed") is not False:errors.append("formula variant policy mismatch")
    if policy.get("source_defects",{}).get("source_mutation_allowed") is not False or policy["source_defects"].get("affected_capability_status")!="deferred":errors.append("source defect policy mismatch")
    states=policy.get("file_review_states",{});expected={"semantic-read","behavior-reviewed","excluded"}
    if set(states.get("allowed",[]))!=expected or states.get("excluded_requires_subkind") is not True:errors.append("file review state policy mismatch")
    return {"gate":"capability-compiler-v2-fusion-policy","ok":not errors,"approved_decisions":len(approved),"errors":errors}
def main()->int:
    p=argparse.ArgumentParser(description=__doc__);p.add_argument("--workspace-root",type=Path,default=Path("."));a=p.parse_args();r=verify(a.workspace_root.resolve());print(json.dumps(r,ensure_ascii=False,sort_keys=True));return 0 if r["ok"] else 1
if __name__=="__main__":raise SystemExit(main())
