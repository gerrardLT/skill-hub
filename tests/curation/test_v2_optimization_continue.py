import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]/'tools/curation'))
import v2_optimization_continue as driver
import v2_optimization_full_eval as full_eval


def test_incomplete_and_corrupt_execution_not_counted(tmp_path):
    control=tmp_path/driver.CONTROL
    control.mkdir(parents=True)
    (control/'full-task-set.json').write_text(json.dumps({'skills':{'demo':{'tasks':[{'id':'T1','prompt':'task'}]}}}),encoding='utf-8')
    for base in ('slots/v2/1.0.0/skills','evals/candidates/capability-compiler-v2/optimization-1.1.0/skills'):
        p=tmp_path/base/'demo/SKILL.md';p.parent.mkdir(parents=True);p.write_text('method',encoding='utf-8')
    result=driver.execution_status(tmp_path)
    assert result=={'valid':0,'missing':2,'errors':[],'expected':2}
    p=tmp_path/driver.ROOT/'exec/demo__T1__optimized/run.json';p.parent.mkdir(parents=True)
    p.write_text(json.dumps({'exit_status':'completed','prompt_sha256':'wrong','output':'answer','output_sha256':'wrong'}),encoding='utf-8')
    result=driver.execution_status(tmp_path)
    assert result['valid']==0 and len(result['errors'])==1 and result['missing']==1


def test_full_eval_rejects_invalid_concurrency(monkeypatch):
    monkeypatch.setattr(sys, 'argv', ['v2_optimization_full_eval.py', 'exec', '--concurrency', '0', '--judge-model', 'taomu/gpt-5.6-sol', '--judge-root', 'judge-replacement'])
    try:
        full_eval.main()
    except ValueError as exc:
        assert str(exc) == 'concurrency must be 1..8'
    else:
        raise AssertionError('invalid concurrency accepted')
