"""Budget-checked full-directory generation; stop at the first unaccepted generation."""
import json
import subprocess
import sys
import time
from pathlib import Path
import hashlib

ROOT = Path('curation/v2/optimization-1.1.0')
RUNS = Path('evals/runs/capability-compiler-v2/optimization-1.1.0')
CAND = Path('evals/candidates/capability-compiler-v2/optimization-1.1.0')


def main():
    frozen = json.loads((ROOT/'candidate-freeze.json').read_text(encoding='utf-8'))
    for item in frozen['files']:
        if hashlib.sha256(Path(item['path']).read_bytes()).hexdigest() != item['sha256']:
            raise RuntimeError('candidate changed after freeze')
    ids = [s['id'] for s in json.loads((CAND/'skill-index.json').read_text(encoding='utf-8'))['skills']]
    outcomes = []
    for sid in ids:
        if sid == 'browser-data-acquisition-runtime':
            outcomes.append({'skill': sid, 'status': 'owner-approved-parent-fixtures-reviewed'})
            continue
        accepted = sorted((RUNS/'fixture-review'/sid).glob('attempt-*/freeze.json'))
        if accepted:
            outcomes.append({'skill': sid, 'status': 'reviewed-existing-unseen-before-pilot-now-regression', 'freeze_path': accepted[-1].as_posix()})
            continue
        fixture = RUNS/'fresh-gen'/sid/'attempt-1/fixture-validation.json'
        if fixture.exists():
            value = json.loads(fixture.read_text(encoding='utf-8'))
            code = 0 if value['status'] == 'generated-pending-independent-fixture-review' else 1
        else:
            start = time.perf_counter()
            run = subprocess.run([sys.executable, 'tools/curation/v2_optimization_generate.py', sid, '--attempt', '1'], capture_output=True)
            dest = RUNS/'generation-commands'/sid
            dest.mkdir(parents=True, exist_ok=True)
            (dest/'stdout.txt').write_bytes(run.stdout)
            (dest/'stderr.txt').write_bytes(run.stderr)
            (dest/'receipt.json').write_text(json.dumps({'exit_code': run.returncode, 'duration_ms': round((time.perf_counter()-start)*1000,3)}), encoding='utf-8')
            code = run.returncode
        outcomes.append({'skill': sid, 'status': 'generated-pending-review' if code == 0 else 'blocked-generation'})
        (ROOT/'full-generation-progress.json').write_text(json.dumps({'status': 'in-progress' if code == 0 else 'blocked', 'skills_expected': len(ids), 'items': outcomes}, indent=2)+'\n', encoding='utf-8')
        print(sid, code, flush=True)
        if code:
            return 1
    (ROOT/'full-generation-progress.json').write_text(json.dumps({'status': 'generation-complete-review-pending', 'skills_expected': len(ids), 'items': outcomes}, indent=2)+'\n', encoding='utf-8')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
