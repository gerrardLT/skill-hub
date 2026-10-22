"""Sequential, budget-checked pilot on independently accepted fixtures."""
import argparse
import hashlib
import json
import shutil
from pathlib import Path
import v2_skill_audit_phase_d as pd
import v2_optimization_budget as budget

SKILLS = {'deployment-trigger-execution': 1, 'kubernetes-application-deployment': 1, 'purposeful-motion-and-animation-engineering': 1, 'test-runtime-bootstrap': 3, 'website-audit-remediation': 2, 'remote-pull-request-merge': 1}
CAND = Path('evals/candidates/capability-compiler-v2/optimization-1.1.0')


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('stage', choices=['exec', 'judge'])
    args = ap.parse_args()
    ws = Path('.').resolve()
    root = ws / budget.RUNS
    exe = shutil.which('pi.cmd') or shutil.which('pi')
    if not exe:
        raise RuntimeError('pi unavailable')
    counts = 0
    for sid, attempt in SKILLS.items():
        frozen = pd.load(root/'fixture-review'/sid/f'attempt-{attempt}/freeze.json')
        fixture = ws/frozen['fixture_path']
        if hashlib.sha256(fixture.read_bytes()).hexdigest() != frozen['fixture_sha256']:
            raise ValueError('frozen fixture changed')
        for task in frozen['tasks']:
            outputs = {}
            for variant, base in [('v100', Path('slots/v2/1.0.0/skills')), ('optimized', CAND/'skills')]:
                method = (ws/base/sid/'SKILL.md').read_text(encoding='utf-8')
                prompt = pd.EXEC_PROMPT.format(method=pd.METHOD_BLOCK.format(skill=method), task=task['prompt'])
                directory = root/'pilot/exec'/f'{sid}__{task["id"]}__{variant}'
                if args.stage == 'exec':
                    if not (directory/'run.json').is_file():
                        budget.require_budget(root, 100_000)
                    run = pd.call(directory, pd.EXEC_MODEL, 'low', prompt, exe, 900)
                else:
                    run = pd.load(directory/'run.json')
                if run['exit_status'] != 'completed' or run['prompt_sha256'] != pd.sha(prompt):
                    raise RuntimeError(f'failed or stale execution: {directory}')
                outputs[variant] = run['output']
                if args.stage == 'exec':
                    counts += 1
                    print(sid, task['id'], variant, 'completed', flush=True)
            if args.stage == 'judge':
                for order in ('xy', 'yx'):
                    a, b = ('optimized', 'v100') if order == 'xy' else ('v100', 'optimized')
                    prompt = pd.JUDGE_PROMPT.format(task=task['prompt'], rubric='\n'.join('- '+x for x in task['rubric']), a=outputs[a], b=outputs[b])
                    directory = root/'pilot/judge'/f'{sid}__{task["id"]}__{order}'
                    if not (directory/'run.json').is_file():
                        budget.require_budget(root, 100_000)
                    run = pd.call(directory, pd.JUDGE_MODEL, 'medium', prompt, exe, 900)
                    value, _ = pd.parse_json(run['output'])
                    if run['exit_status'] != 'completed' or run['prompt_sha256'] != pd.sha(prompt) or not isinstance(value, dict) or value.get('overall') not in ('A','B','tie'):
                        raise RuntimeError(f'invalid judge: {directory}')
                    counts += 1
                    print(sid, task['id'], order, value['overall'], flush=True)
    print(json.dumps({'stage': args.stage, 'validated_calls': counts}))


if __name__ == '__main__':
    main()
