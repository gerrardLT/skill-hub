"""A completed process is not proof of complete, current evaluation evidence."""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'tools/curation'))
import v2_revision_eval_completeness as gate


def test_missing_execution_is_incomplete(tmp_path, monkeypatch):
    monkeypatch.setattr(gate.ev, 'tasks_of', lambda ws, which: {'demo': {'tasks': [{'id': 'T1', 'prompt': 'test', 'rubric': ['correct']}]}})
    result = gate.verify(tmp_path)
    assert result['status'] == 'incomplete'
    assert result['counts']['old']['exec_expected'] == 1
    assert result['counts']['fresh']['exec_expected'] == 3
    assert result['counts']['fresh']['judge_expected'] == 4
    assert result['error_count'] == 10


def test_changed_method_invalidates_completed_execution(tmp_path, monkeypatch):
    monkeypatch.setattr(gate.ev, 'tasks_of', lambda ws, which: {'demo': {'tasks': [{'id': 'T1', 'prompt': 'test', 'rubric': ['correct']}]}})
    monkeypatch.setattr(gate.ev, 'skill_text', lambda ws, sid, variant: 'current method')
    for which in ('old', 'fresh'):
        for variant in gate.ev.VARIANTS[which]:
            p = gate.ev.run_dir(tmp_path, which, 'demo', 'T1', variant) / 'run.json'
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(json.dumps({'exit_status': 'completed', 'prompt_sha256': 'stale', 'output': 'answer', 'output_sha256': gate.pd.sha('answer')}), encoding='utf-8')
    result = gate.verify(tmp_path)
    assert result['status'] == 'incomplete'
    assert result['counts']['old']['exec_valid'] == 0
    assert result['counts']['fresh']['exec_valid'] == 0
    assert sum('invalid exec' in e for e in result['errors']) == 4
