"""Regression checks on isolated generated contracts and ranking handoff."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'evals/candidates/capability-compiler-v2/optimization-1.1.0'


def test_superseded_scoring_gate_removed_from_text_and_contract():
    root = OUT / 'skills/opportunity-prioritization-and-frameworks'
    md = (root / 'SKILL.md').read_text(encoding='utf-8')
    contract = json.loads((root / 'contract.json').read_text(encoding='utf-8'))
    assert 'Reject any unnamed, hybrid, or partially specified' not in md
    assert any('Declare the exact named or custom scoring formula' in g for g in contract['hard_gates'])
    assert all(g in md for g in contract['hard_gates'])


def test_conditional_ranking_dependency_is_bound_to_scoring_owner():
    stage = json.loads((OUT / 'recipes/stages/stage-03-strategy-prioritization.json').read_text(encoding='utf-8'))
    dep = next(d for d in stage['dependency_records'] if d['id'] == 'OPT-DEPENDENCY-0001')
    assert dep['kind'] == 'optional'
    assert dep['source_capability_id'] == 'capability:evidence-synthesis-and-opportunity-prioritization'
    assert dep['target_capability_id'] == 'capability:opportunity-prioritization-and-frameworks'
    assert 'ranking' in dep['condition']
    step = next(s for s in stage['steps'] if s['id'] == 'opportunity-prioritization-and-frameworks')
    assert dep['id'] in step['dependency_refs']
    assert step['contract_sha256'] == hashlib.sha256((OUT / 'skills/opportunity-prioritization-and-frameworks/contract.json').read_bytes()).hexdigest()


def test_previous_candidate_bytes_unchanged():
    frozen = json.loads((ROOT / 'curation/v2/optimization-1.1.0/baseline-freeze.json').read_text(encoding='utf-8'))
    for f in frozen['files']:
        assert hashlib.sha256((ROOT / f['path']).read_bytes()).hexdigest() == f['sha256'], f['path']
