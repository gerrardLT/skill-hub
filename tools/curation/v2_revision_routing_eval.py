"""Run frozen R5 routing cases without executing their targets; preserve raw model evidence."""
import argparse
import hashlib
import json
import shutil
from pathlib import Path
import v2_skill_audit_phase_d as pd
from v2_phase9_runner import ROUTER_SYSTEM


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--run', action='store_true', help='Explicitly enable model calls; otherwise validate the frozen inputs only.')
    ap.add_argument('--revision', choices=['v1', 'v2'], default='v1', help='Use the original or owner-approved corrected frozen plan; results stay isolated.')
    args = ap.parse_args()
    ws = Path('.').resolve()
    suffix = '-v2' if args.revision == 'v2' else ''
    plan_path = ws / f'curation/v2/revision-1.1.0/routing-regression-plan{suffix}.json'
    plan = pd.load(plan_path)
    candidate = ws / 'evals/candidates/capability-compiler-v2/revision-1.1.0'
    for rel, key in [('recipes/router.json', 'candidate_router_sha256'), ('skill-index.json', 'candidate_index_sha256')]:
        if hashlib.sha256((candidate / rel).read_bytes()).hexdigest() != plan[key]:
            raise ValueError(f'frozen routing input changed: {rel}')
    router = pd.load(candidate / 'recipes/router.json')
    index = pd.load(candidate / 'skill-index.json')
    material = json.dumps({'router': router, 'atomic_targets': index['skills']}, ensure_ascii=False)
    if not args.run:
        print(json.dumps({'status': 'inputs-verified-not-executed', 'cases': len(plan['cases'])}))
        return 0
    exe = shutil.which('pi.cmd') or shutil.which('pi')
    if not exe:
        raise RuntimeError('pi executable unavailable')
    root = ws / f'evals/runs/capability-compiler-v2/revision-1.1.0-eval/routing{suffix}'
    results = []
    for case in plan['cases']:
        prompt = f"{ROUTER_SYSTEM}\nUSER REQUEST:\n{case['input']}\n\nROUTER MATERIAL:\n{material}"
        run = pd.call(root / case['id'], plan['model'], 'low', prompt, exe, 900)
        if run['prompt_sha256'] != pd.sha(prompt):
            raise ValueError(f'stale routing evidence: {case["id"]}')
        value, notes = pd.parse_json(run['output'])
        valid = isinstance(value, dict) and set(value) == {'target', 'reason', 'would_execute'}
        ok = run['exit_status'] == 'completed' and valid and value['target'] == case['expected_target'] and value['would_execute'] is False
        results.append({'id': case['id'], 'expected': case['expected_target'], 'actual': value, 'passed': ok, 'run_status': run['exit_status'], 'parse_notes': notes})
    report = {'status': 'passed' if all(r['passed'] for r in results) else 'failed', 'plan_sha256': hashlib.sha256(plan_path.read_bytes()).hexdigest(), 'cases': results}
    pd.write(root / 'report.json', report)
    print(json.dumps({'status': report['status'], 'passed': sum(r['passed'] for r in results), 'total': len(results)}))
    return 0 if report['status'] == 'passed' else 1


if __name__ == '__main__':
    raise SystemExit(main())
