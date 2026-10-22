import json
import sys
from pathlib import Path
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'tools/curation'))
import v2_optimization_budget as budget


def record(root, name, usage, status='completed'):
    p = root/name/'run.json'
    p.parent.mkdir(parents=True)
    p.write_text(json.dumps({'token_usage': usage, 'exit_status': status}), encoding='utf-8')


def test_failed_calls_count_and_unknown_usage_blocks(tmp_path):
    record(tmp_path, 'success', {'totalTokens': 20})
    record(tmp_path, 'failure', {'totalTokens': 10}, 'failed')
    assert budget.require_budget(tmp_path, 1)['recorded_tokens'] == 30
    budget.release_budget(1)
    record(tmp_path, 'unknown', {}, 'failed')
    with pytest.raises(RuntimeError, match='unknown'):
        budget.require_budget(tmp_path, 1)


def test_limit_and_partial_call_fail_closed(tmp_path):
    record(tmp_path, 'full', {'totalTokens': budget.LIMIT})
    with pytest.raises(RuntimeError, match='budget'):
        budget.require_budget(tmp_path, 1)
    assert budget.inspect(tmp_path)['remaining_recorded_tokens'] == 0


def test_bounded_concurrent_partials_and_reservations(tmp_path, monkeypatch):
    monkeypatch.setattr(budget, '_RESERVED', 0)
    for name in ('active-a', 'active-b'):
        p=tmp_path/name/'prompt.md';p.parent.mkdir(parents=True);p.write_text('x',encoding='utf-8')
    budget.require_budget(tmp_path, 100, allow_active_partials=2)
    budget.require_budget(tmp_path, 100, allow_active_partials=2)
    assert budget._RESERVED == 200
    with pytest.raises(RuntimeError, match='partial'):
        budget.require_budget(tmp_path, 100, allow_active_partials=1)
    budget.release_budget(100);budget.release_budget(100)
    assert budget._RESERVED == 0
