"""Protocol tests only: fake worker is not model-quality evidence."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'tools/curation'))
import v2_optimization_handoff as h


def setup_candidate(tmp_path):
    for sid in h.OWNERS:
        p = tmp_path / h.CAND / 'skills' / sid / 'SKILL.md'
        p.parent.mkdir(parents=True)
        p.write_text('method', encoding='utf-8')


def test_upstream_output_is_passed_and_hash_bound(tmp_path):
    setup_candidate(tmp_path)
    calls = []
    def worker(directory, model, thinking, prompt, exe, timeout):
        calls.append(prompt)
        output = 'synthesis artifact' if len(calls) == 1 else 'scoring artifact'
        return {'exit_status': 'completed', 'output': output, 'prompt_sha256': h.pd.sha(prompt), 'output_sha256': h.pd.sha(output)}
    r = h.compose(tmp_path, 'rank candidates', tmp_path/'run', 'unused', worker)
    assert r['status'] == 'executed-pending-quality-review'
    assert 'synthesis artifact' in calls[1]
    assert r['steps'][1]['upstream_sha256'] == h.pd.sha('synthesis artifact')
    assert r['would_execute_target'] is False


def test_failed_synthesis_does_not_run_scoring(tmp_path):
    setup_candidate(tmp_path)
    calls = []
    def worker(*args):
        calls.append(args)
        return {'exit_status': 'failed', 'output': ''}
    r = h.compose(tmp_path, 'task', tmp_path/'run', 'unused', worker)
    assert r['status'] == 'failed'
    assert len(calls) == 1
