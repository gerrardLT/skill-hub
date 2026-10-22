"""Mutation checks: the 1.1.0 revision gate must fail closed on each tampering."""
import json
import shutil
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools/curation"))
import v2_revision_gate as gate  # noqa: E402

COPY = ["evals/candidates/capability-compiler-v2/revision-1.1.0", "curation/v2/revision-1.1.0/structure.json", "curation/v2/skill-audit/ledger.json", "curation/v2/lifecycle/permission-identities.json", "slots/v2"]
CAND = "evals/candidates/capability-compiler-v2/revision-1.1.0"


@pytest.fixture(scope="module")
def base(tmp_path_factory):
    ws = tmp_path_factory.mktemp("ws")
    for rel in COPY:
        src, dst = ROOT / rel, ws / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copytree(src, dst) if src.is_dir() else shutil.copy2(src, dst)
    return ws


@pytest.fixture()
def ws(base, tmp_path):
    shutil.copytree(base, tmp_path / "w")
    return tmp_path / "w"


def failing(ws, name):
    return {c["name"]: c for c in gate.verify(ws, check_release=False)["checks"]}[name]


def edit_json(path, fn):
    data = json.loads(path.read_text(encoding="utf-8"))
    fn(data)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def test_pristine_candidate_passes(ws):
    report = gate.verify(ws, check_release=False)
    assert report["status"] == "passed", report


def test_unresolved_finding_fails(ws):
    edit_json(ws / CAND / "skills/testing-portfolio-strategy/provenance.json", lambda d: d["revision"]["resolves"].pop("testing-portfolio-strategy#F1"))
    assert not failing(ws, "findings-closed")["ok"]


def test_widened_permission_fails(ws):
    def widen(d):
        d["permission_identity"] = "workspace-write"
        d["execution"].update(model_tools=["read", "edit", "write"], mutation_scope="run-output")
    edit_json(ws / CAND / "skills/independent-code-review/contract.json", widen)
    assert not failing(ws, "permissions-only-narrowed")["ok"]


def test_dangling_reference_fails(ws):
    p = ws / CAND / "skills/independent-code-review/SKILL.md"
    p.write_text(p.read_text(encoding="utf-8") + "\nSee provider-review-comment-response.\n", encoding="utf-8")
    assert not failing(ws, "skill-text-and-contract")["ok"]


def test_missing_overlap_anti_trigger_fails(ws):
    p = ws / CAND / "skills/vitest-tooling/SKILL.md"
    p.write_text(p.read_text(encoding="utf-8").replace("Route to `playwright-test-engineering`", "Route elsewhere"), encoding="utf-8")
    assert not failing(ws, "skill-text-and-contract")["ok"]


def test_enabled_protected_step_fails(ws):
    path = ws / CAND / "recipes/stages/stage-11-deployment-change.json"

    def enable(d):
        for s in d["steps"]:
            if s.get("activation") == "disabled-pending-current-authorization":
                s["activation"] = "conditional"
                return

    edit_json(path, enable)
    assert not failing(ws, "recipes-and-router")["ok"]


def test_stale_contract_binding_fails(ws):
    edit_json(ws / CAND / "skills/qa-finding-triage/contract.json", lambda d: d["hard_gates"].append("extra gate"))
    assert not failing(ws, "recipes-and-router")["ok"]


def test_extra_candidate_file_fails(ws):
    (ws / CAND / "skills/qa-finding-triage/stray.txt").write_text("x", encoding="utf-8")
    assert not failing(ws, "candidate-files-and-skill-set")["ok"]
