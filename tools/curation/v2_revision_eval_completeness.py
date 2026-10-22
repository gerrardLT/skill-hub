"""Read-only R5 completeness check against frozen tasks and current method text."""
import json
from pathlib import Path
import v2_revision_eval as ev
import v2_skill_audit_phase_d as pd


def verify(ws):
    errors, counts = [], {}
    for which in ('old', 'fresh'):
        tasks = ev.tasks_of(ws, which)
        expected_exec = expected_judge = completed_exec = completed_judge = 0
        for sid, entry in tasks.items():
            for task in entry['tasks']:
                for variant in ev.VARIANTS[which]:
                    expected_exec += 1
                    p = ev.run_dir(ws, which, sid, task['id'], variant) / 'run.json'
                    if not p.is_file():
                        errors.append(f'missing exec: {which}:{sid}:{task["id"]}:{variant}')
                        continue
                    run = pd.load(p)
                    method = pd.METHOD_BLOCK.format(skill=ev.skill_text(ws, sid, variant)) if variant != 'baseline' else ''
                    prompt = pd.EXEC_PROMPT.format(method=method, task=task['prompt'])
                    if run['exit_status'] != 'completed' or run['prompt_sha256'] != pd.sha(prompt) or run['output_sha256'] != pd.sha(run['output']):
                        errors.append(f'invalid exec: {p}')
                    else:
                        completed_exec += 1
                for x, y in ev.PAIRS[which]:
                    for order in ev.ORDERS:
                        expected_judge += 1
                        p = ws / ev.OUT / 'judge' / which / f'{x}_{y}' / f'{sid}__{task["id"]}__{order}' / 'run.json'
                        if not p.is_file():
                            errors.append(f'missing judge: {p}')
                            continue
                        run = pd.load(p)
                        a, b = (x, y) if order == 'xy' else (y, x)
                        paths = [ev.run_dir(ws, which, sid, task['id'], v) / 'run.json' for v in (a, b)]
                        if not all(q.is_file() for q in paths):
                            errors.append(f'judge without inputs: {p}')
                            continue
                        ra, rb = map(pd.load, paths)
                        prompt = pd.JUDGE_PROMPT.format(task=task['prompt'], rubric='\n'.join(f'- {i}' for i in task['rubric']), a=ra['output'], b=rb['output'])
                        value, _ = pd.parse_json(run.get('output', ''))
                        if run['exit_status'] != 'completed' or run['prompt_sha256'] != pd.sha(prompt) or not isinstance(value, dict) or value.get('overall') not in ('A', 'B', 'tie'):
                            errors.append(f'invalid judge: {p}')
                        else:
                            completed_judge += 1
        counts[which] = dict(exec_expected=expected_exec, exec_valid=completed_exec, judge_expected=expected_judge, judge_valid=completed_judge)
    return dict(status='passed' if not errors else 'incomplete', counts=counts, error_count=len(errors), errors=errors[:10])


if __name__ == '__main__':
    result = verify(Path('.').resolve())
    print(json.dumps(result, ensure_ascii=False, indent=2))
    raise SystemExit(0 if result['status'] == 'passed' else 1)
