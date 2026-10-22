#!/usr/bin/env python3
"""Aggregate Capability Compiler V2 Phase 1 semantic evidence gates."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

try:
    from tools.curation.v2_auxiliary_units import verify_disposed
    from tools.curation.v2_cluster_comparison_gate import verify as verify_comparisons
    from tools.curation.v2_fusion_policy_gate import verify as verify_policy
    from tools.curation.v2_phase0_audit import audit as phase0_audit, compare_expected
    from tools.curation.v2_phase1_ledger import verify_reviewed
    from tools.curation.v2_root_dossier_gate import verify as verify_dossiers
    from tools.curation.v2_root_atomic_units import verify as verify_root_atoms
except ModuleNotFoundError:
    from v2_auxiliary_units import verify_disposed
    from v2_cluster_comparison_gate import verify as verify_comparisons
    from v2_fusion_policy_gate import verify as verify_policy
    from v2_phase0_audit import audit as phase0_audit, compare_expected
    from v2_phase1_ledger import verify_reviewed
    from v2_root_dossier_gate import verify as verify_dossiers
    from v2_root_atomic_units import verify as verify_root_atoms

def load(path:Path):return json.loads(path.read_text(encoding="utf-8"))
def verify(workspace:Path)->dict:
    checks=[]
    phase0=phase0_audit(workspace);compat=compare_expected(phase0,load(workspace/".specs/capability-compiler-v2/phase-0/baseline.json"));checks.append({"name":"source-and-v1-compatibility","ok":phase0["ok"] and not compat,"errors":[*phase0["errors"],*compat]})
    dossier=verify_dossiers(workspace,workspace/"curation/v2/dossiers");checks.append({"name":"root-dossiers","ok":dossier["ok"],"errors":dossier["errors"]})
    review_errors=verify_reviewed(load(workspace/"curation/v2/coverage.json"));checks.append({"name":"file-review-ledger","ok":not review_errors,"errors":review_errors})
    auxiliary_errors=verify_disposed(load(workspace/"curation/v2/units/auxiliary.json"));checks.append({"name":"auxiliary-unit-dispositions","ok":not auxiliary_errors,"errors":auxiliary_errors})
    root_atoms=verify_root_atoms(workspace,workspace/"curation/v2/units/root-derived.json");checks.append({"name":"previously-uncovered-root-atoms","ok":root_atoms["ok"],"errors":root_atoms["errors"]})
    comparison=verify_comparisons(workspace,workspace/"curation/v2/comparisons",workspace/"curation/v2/relationships.json");checks.append({"name":"cluster-comparisons","ok":comparison["ok"],"errors":comparison["errors"]})
    policy=verify_policy(workspace);checks.append({"name":"owner-fusion-policy","ok":policy["ok"],"errors":policy["errors"]})
    return {"gate":"capability-compiler-v2-phase-1","ok":all(item["ok"] for item in checks),"checks":checks,"errors":[f"{item['name']}: {error}" for item in checks for error in item["errors"]]}
def main()->int:
    p=argparse.ArgumentParser(description=__doc__);p.add_argument("--workspace-root",type=Path,default=Path("."));a=p.parse_args();r=verify(a.workspace_root.resolve());print(json.dumps(r,ensure_ascii=False,sort_keys=True));return 0 if r["ok"] else 1
if __name__=="__main__":raise SystemExit(main())
