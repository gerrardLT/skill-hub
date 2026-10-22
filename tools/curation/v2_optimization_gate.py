"""Reuse revision invariants for isolated optimization, including unchanged release evidence."""
import json
from pathlib import Path
import v2_revision_gate as gate
import v2_optimization_budget as budget


def verify(ws):
    gate.OUT = Path('evals/candidates/capability-compiler-v2/optimization-1.1.0')
    gate.REV = Path('curation/v2/optimization-1.1.0')
    report = gate.verify(ws)
    report['budget'] = budget.inspect(ws / budget.RUNS)
    return report


if __name__ == '__main__':
    ws = Path('.').resolve()
    result = verify(ws)
    path = ws / 'curation/v2/optimization-1.1.0/gate-report.json'
    path.write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    print(json.dumps(result, ensure_ascii=False))
    raise SystemExit(0 if result['status'] == 'passed' else 1)
