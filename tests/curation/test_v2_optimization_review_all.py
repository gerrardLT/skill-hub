"""Early review cannot consume budget or mistake partial generation for accepted coverage."""
import json
import sys
from pathlib import Path
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'tools/curation'))
import v2_optimization_review_all as review


def test_generation_must_finish_before_review(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    p = tmp_path/'curation/v2/optimization-1.1.0/full-generation-progress.json'
    p.parent.mkdir(parents=True)
    p.write_text(json.dumps({'status': 'in-progress', 'items': []}), encoding='utf-8')
    def forbidden(*args, **kwargs):
        raise AssertionError('model call occurred before generation completed')
    monkeypatch.setattr(review.pd, 'call', forbidden)
    with pytest.raises(RuntimeError, match='generation must be finished'):
        review.main()


def test_frozen_candidate_drift_stops_before_model_call(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    c = tmp_path/'curation/v2/optimization-1.1.0'
    c.mkdir(parents=True)
    (c/'full-generation-progress.json').write_text(json.dumps({'status': 'generation-complete-review-pending', 'items': []}), encoding='utf-8')
    (tmp_path/'candidate.txt').write_text('changed', encoding='utf-8')
    (c/'candidate-freeze.json').write_text(json.dumps({'files': [{'path': 'candidate.txt', 'sha256': 'wrong'}]}), encoding='utf-8')
    def forbidden(*args, **kwargs):
        raise AssertionError('model call occurred with candidate drift')
    monkeypatch.setattr(review.pd, 'call', forbidden)
    with pytest.raises(RuntimeError, match='candidate drift'):
        review.main()
