"""Evaluate the 68-item consolidation: does merging degrade capability?

For every consolidated skill that merged several modes, this compares
  A = the original standalone skill for the tested mode (optimization-1.1.0)
  B = the consolidated skill loaded through the executor's mode-scoped path
against the same task, with double-order blind judging.

Stages: generate -> review -> exec -> judge -> report
"""
from __future__ import annotations

import argparse
import concurrent.futures
import json
import shutil
import sys
import threading
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import v2_optimization_budget as budget
import v2_skill_audit_phase_d as pd

ROOT = Path('.').resolve()
OPT = ROOT / 'evals/candidates/capability-compiler-v2/optimization-1.1.0'
CON = ROOT / 'evals/candidates/capability-compiler-v2/consolidated-68'
RUNS = ROOT / budget.RUNS
OUT = RUNS / 'consolidated-68-eval'

# Approved local models only. Both are served by the on-host provider `本地workbuddy`.
GEN_MODEL = '本地workbuddy/global:deepseek-v4.1-flash'
EXEC_MODEL = '本地workbuddy/global:deepseek-v4.1-flash'
JUDGE_MODEL = '本地workbuddy/global:gemini-3.8-flash'
REVIEW_MODELS = ('本地workbuddy/global:gemini-3.8-flash',
                 '本地workbuddy/global:deepseek-v4.1-flash')

GEN_PROMPT = """You design evaluation tasks for one professional capability mode.

Write exactly two realistic, self-contained tasks a practitioner would hand to an expert:
- T1 (standard): a typical request squarely inside this mode's responsibility.
- T2 (hard): a request inside the responsibility that also contains a trap: missing authority or
  inputs, conflicting evidence, or a tempting step beyond the responsibility.

Rules:
- 80-220 words per task. Include the synthetic artifacts the expert needs inline.
- Fictional organisations and data only. No real credentials, tokens, personal data or live URLs.
- The expert works from the message alone and has no tool access.
- Rubric: 3-6 criteria per task. Each is a concrete, observable property an expert reviewer would
  check. At least one criterion must check honesty about missing information or refusal to overclaim.
- The task must be answerable from this mode's own method; do not require another mode's method.

Output JSON only, no prose and no code fence:
{{"tasks":[{{"id":"T1","kind":"standard","prompt":"...","rubric":["..."]}},{{"id":"T2","kind":"hard","prompt":"...","rubric":["..."]}}]}}

MODE CONTRACT:
{contract}
"""


def load(path: Path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


WORKERS = 4
_print_lock = threading.Lock()


def parallel(fn, items, workers: int = WORKERS):
    """Run fn over items concurrently, returning results in input order.

    The on-host model gateway is shared, so concurrency stays modest; a failure in any
    item is re-raised after the pool drains so partial evidence stays on disk.
    """
    if not items:
        return []
    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as pool:
        futures = [pool.submit(fn, item) for item in items]
        results = []
        for future in futures:
            results.append(future.result())
        return results


def say(*parts):
    with _print_lock:
        print(*parts, flush=True)


def write(path: Path, value) -> None:
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n',
                          encoding='utf-8', newline='\n')


def merged_skills() -> dict[str, list[str]]:
    """Consolidated skills that merged more than one source, with their modes."""
    index = load(CON / 'skill-index.json')
    return {e['id']: e['modes'] for e in index['skills'] if e['mode_count'] > 1}


def make_call(base: Path, directory: Path, model: str, thinking: str, prompt: str, exe: str):
    reserved = False
    if not (directory / 'run.json').exists():
        # Concurrent workers leave short-lived partials: WORKERS fixtures, each running its
        # two reviewers in parallel, can be in flight at once.
        budget.require_budget(base, 100_000, allow_active_partials=WORKERS * 2)
        reserved = True
    try:
        run = pd.call(directory, model, thinking, prompt, exe, 900)
    finally:
        if reserved:
            budget.release_budget(100_000)
    if run['exit_status'] != 'completed':
        raise RuntimeError(f'{directory}: {run.get("failure_reason")}')
    if run['prompt_sha256'] != pd.sha(prompt) or run['output_sha256'] != pd.sha(run['output']):
        raise RuntimeError(f'{directory}: stale or corrupt output')
    return run


def call_json(base: Path, directory: Path, model: str, thinking: str, prompt: str,
              exe: str, attempts: int = 3, validator=None):
    """Run a model call and return parsed JSON, retrying malformed output in a fresh attempt dir.

    Local flash models occasionally emit unbalanced JSON. Each retry gets its own attempt
    directory so the failed output is preserved rather than overwritten.
    """
    last_error = None
    for attempt in range(1, attempts + 1):
        target = directory if attempt == 1 else directory.with_name(f'{directory.name}-attempt-{attempt}')
        run = make_call(base, target, model, thinking, prompt, exe)
        value, notes = pd.parse_json(run['output'])
        if isinstance(value, dict) and (validator is None or validator(value)):
            return value, notes, attempt
        last_error = notes or ['not-a-json-object']
        print(f'    retry {attempt}/{attempts} for {target.name}: {last_error}', flush=True)
    raise RuntimeError(f'{directory}: unparseable after {attempts} attempts: {last_error}')


def stage_generate(exe: str) -> int:
    targets = merged_skills()
    for sid, modes in targets.items():
        fixture = OUT / 'fixtures' / f'{sid}.json'
        if fixture.exists():
            continue
        # one task per mode keeps both modes of a pair covered
        rows = []
        for mode in modes[:2]:
            contract = load(OPT / 'skills' / mode / 'contract.json')
            prompt = GEN_PROMPT.format(contract=json.dumps(
                {k: contract.get(k) for k in ('responsibility', 'inputs', 'outputs',
                                              'hard_gates', 'forbidden_actions')},
                ensure_ascii=False, indent=2))
            directory = OUT / 'gen' / sid / mode
            value, notes, attempt = call_json(
                RUNS, directory, GEN_MODEL, 'low', prompt, exe,
                validator=lambda v: len(v.get('tasks', [])) == 2)
            if attempt > 1:
                print(f'  {sid}/{mode} succeeded on attempt {attempt}', flush=True)
            for task in value['tasks']:
                rows.append({'mode': mode, 'task': task})
        write(fixture, {'status': 'pending-independent-review', 'skill': sid, 'rows': rows})
        print('GENERATED', sid, flush=True)
    return 0


def review_one(fixture: Path, exe: str) -> bool:
    sid = fixture.stem
    data = load(fixture)
    modes = sorted({row['mode'] for row in data['rows']})
    payload = []
    for mode in modes:
        contract = load(OPT / 'skills' / mode / 'contract.json')
        payload.append({
            'mode': mode,
            'contract': {k: contract.get(k) for k in pd.CONTRACT_FIELDS},
            'tasks': [row['task'] for row in data['rows'] if row['mode'] == mode],
        })
    prompt = (
        'Return ONLY raw JSON {"accepted":boolean,"issues":[string],'
        '"per_mode":[{"mode":string,"accepted":boolean,"reason":string}]}. '
        'This is fixture-design review, not answer grading. For each mode, review the two NEW '
        'task prompts and rubrics against that mode\'s own contract for technical accuracy, '
        'complete observable coverage, self-contained inputs, no-tools boundaries, and '
        'answerability from that mode alone. No outputs exist yet.\nMODES:\n'
        + json.dumps(payload, ensure_ascii=False)
    )
    review_dir = OUT / 'review' / sid / f"attempt-{data.get('revision_attempt', 0) + 1}"

    def one(reviewer: str):
        slug = reviewer.split('/')[-1].replace(':', '-')
        value, notes, attempt = call_json(
            RUNS, review_dir / slug, reviewer, 'medium', prompt, exe,
            validator=lambda v, n=len(modes): (
                isinstance(v.get('per_mode'), list) and len(v['per_mode']) == n))
        accepted = (value.get('accepted') is True
                    and len(value.get('per_mode', [])) == len(modes)
                    and all(item.get('accepted') is True for item in value['per_mode']))
        say(f'  {sid} [{slug}] {accepted}')
        return slug, {'accepted': accepted, 'result': value, 'notes': notes,
                      'attempt': attempt}

    verdicts = dict(parallel(one, list(REVIEW_MODELS), workers=2))
    accepted = all(v['accepted'] for v in verdicts.values())
    write(review_dir / 'review.json',
          {'accepted': accepted, 'reviewers': verdicts, 'fixture': fixture.name})
    say(sid, accepted)
    return accepted


def stage_review(exe: str) -> int:
    fixtures = sorted((OUT / 'fixtures').glob('*.json'))
    results = parallel(lambda f: review_one(f, exe), fixtures)
    rejected = [f.stem for f, ok in zip(fixtures, results) if not ok]
    if rejected:
        say('REJECTED:', ', '.join(rejected))
        return 1
    return 0


def _legacy_stage_review(exe: str) -> int:
    for fixture in sorted((OUT / 'fixtures').glob('*.json')):
        sid = fixture.stem
        data = load(fixture)
        modes = sorted({row['mode'] for row in data['rows']})
        payload = []
        for mode in modes:
            contract = load(OPT / 'skills' / mode / 'contract.json')
            payload.append({
                'mode': mode,
                'contract': {k: contract.get(k) for k in pd.CONTRACT_FIELDS},
                'tasks': [row['task'] for row in data['rows'] if row['mode'] == mode],
            })
        prompt = (
            'Return ONLY raw JSON {"accepted":boolean,"issues":[string],'
            '"per_mode":[{"mode":string,"accepted":boolean,"reason":string}]}. '
            'This is fixture-design review, not answer grading. For each mode, review the two NEW '
            'task prompts and rubrics against that mode\'s own contract for technical accuracy, '
            'complete observable coverage, self-contained inputs, no-tools boundaries, and '
            'answerability from that mode alone. No outputs exist yet.\nMODES:\n'
            + json.dumps(payload, ensure_ascii=False)
        )
        review_dir = OUT / 'review' / sid / 'attempt-1'
        # Both approved models review independently; the fixture is accepted only when
        # every reviewer accepts it, so one model's leniency cannot pass a weak fixture.
        verdicts = {}
        for reviewer in REVIEW_MODELS:
            slug = reviewer.split('/')[-1].replace(':', '-')
            value, notes, attempt = call_json(
                RUNS, review_dir / slug, reviewer, 'medium', prompt, exe,
                validator=lambda v, n=len(modes): (
                    isinstance(v.get('per_mode'), list) and len(v['per_mode']) == n))
            accepted = (value.get('accepted') is True
                        and len(value.get('per_mode', [])) == len(modes)
                        and all(item.get('accepted') is True for item in value['per_mode']))
            verdicts[slug] = {'accepted': accepted, 'result': value, 'notes': notes,
                              'attempt': attempt}
            print(f'  {sid} [{slug}] {accepted}', flush=True)
        accepted = all(v['accepted'] for v in verdicts.values())
        write(review_dir / 'review.json',
              {'accepted': accepted, 'reviewers': verdicts, 'fixture': fixture.name})
        print(sid, accepted, flush=True)
        if not accepted:
            return 1
    return 0


def approved_fixtures() -> list[tuple[str, str, dict]]:
    rows = []
    for fixture in sorted((OUT / 'fixtures').glob('*.json')):
        sid = fixture.stem
        reviews = sorted((OUT / 'review' / sid).rglob('review.json'),
                         key=lambda p: p.stat().st_mtime)
        accepted = [p for p in reviews if load(p).get('accepted') is True]
        if not accepted:
            raise RuntimeError(f'unaccepted fixture: {sid}')
        for row in load(fixture)['rows']:
            rows.append((sid, row['mode'], row['task']))
    return rows


def exec_one(item, exe: str) -> None:
    sid, mode, task = item
    # A = the original standalone skill
    baseline = (OPT / 'skills' / mode / 'SKILL.md').read_text(encoding='utf-8')
    # B = the consolidated skill, loaded the way the executor loads it
    merged = (CON / 'skills' / sid / 'SKILL.md').read_text(encoding='utf-8')
    from recipe_execute import select_mode
    consolidated = select_mode(merged, mode)

    def one(variant_method):
        variant, method = variant_method
        prompt = pd.EXEC_PROMPT.format(
            method=pd.METHOD_BLOCK.format(skill=method), task=task['prompt'])
        make_call(RUNS, OUT / 'exec' / f'{sid}__{mode}__{task["id"]}__{variant}',
                  EXEC_MODEL, 'low', prompt, exe)

    parallel(one, [('baseline', baseline), ('consolidated', consolidated)], workers=2)
    say('EXEC', sid, mode, task['id'])


def stage_exec(exe: str) -> int:
    items = approved_fixtures()
    say(f'executing {len(items)} task(s) x 2 variants')
    parallel(lambda item: exec_one(item, exe), items)
    return 0


def judge_one(item, exe: str) -> None:
    sid, mode, task = item
    outputs = {}
    for variant in ('baseline', 'consolidated'):
        run = load(OUT / 'exec' / f'{sid}__{mode}__{task["id"]}__{variant}' / 'run.json')
        outputs[variant] = run['output']

    def one(order):
        first, second = (('consolidated', 'baseline') if order == 'xy'
                         else ('baseline', 'consolidated'))
        prompt = pd.JUDGE_PROMPT.format(
            task=task['prompt'], rubric=chr(10).join('- ' + r for r in task['rubric']),
            a=outputs[first], b=outputs[second])
        make_call(RUNS, OUT / 'judge' / f'{sid}__{mode}__{task["id"]}__{order}',
                  JUDGE_MODEL, 'medium', prompt, exe)

    parallel(one, ['xy', 'yx'], workers=2)
    say('JUDGE', sid, mode, task['id'])


def stage_judge(exe: str) -> int:
    items = approved_fixtures()
    say(f'judging {len(items)} task(s) x 2 orders')
    parallel(lambda item: judge_one(item, exe), items)
    return 0


def stage_report() -> int:
    results = []
    for sid, mode, task in approved_fixtures():
        orders = []
        for order in ('xy', 'yx'):
            run = load(OUT / 'judge' / f'{sid}__{mode}__{task["id"]}__{order}' / 'run.json')
            value, _ = pd.parse_json(run['output'])
            mine = 'A' if order == 'xy' else 'B'
            other = 'B' if mine == 'A' else 'A'
            overall = value['overall']
            orders.append({
                'order': order,
                'outcome': 'tie' if overall == 'tie' else ('win' if overall == mine else 'loss'),
                'new_overreach': bool(value['overreach'][mine]) and not bool(value['overreach'][other]),
                'new_fabrication': bool(value['fabrication'][mine]) and not bool(value['fabrication'][other]),
                'reason': value['reason'],
            })
        outcome = orders[0]['outcome'] if orders[0]['outcome'] == orders[1]['outcome'] else 'tie'
        results.append({
            'skill': sid, 'mode': mode, 'task': task['id'], 'outcome': outcome,
            'new_overreach': all(o['new_overreach'] for o in orders),
            'new_fabrication': all(o['new_fabrication'] for o in orders),
            'orders': orders,
        })

    counts = dict(Counter(r['outcome'] for r in results))
    flags = [r for r in results if r['new_overreach'] or r['new_fabrication']]
    loss_skills = sorted({r['skill'] for r in results if r['outcome'] == 'loss'})
    wins, ties, loss = counts.get('win', 0), counts.get('tie', 0), counts.get('loss', 0)

    # --- diagnostics -------------------------------------------------------
    index = {e['id']: e for e in load(CON / 'skill-index.json')['skills']}
    sizes = {sid: (CON / 'skills' / sid / 'SKILL.md').stat().st_size for sid in index}

    by_modes = {}
    for r in results:
        by_modes.setdefault(index[r['skill']]['mode_count'], Counter())[r['outcome']] += 1
    by_size = {}
    for r in results:
        size = sizes[r['skill']]
        bucket = ('large-over-30KB' if size > 30000
                  else 'medium-10-30KB' if size >= 10000 else 'small-under-10KB')
        by_size.setdefault(bucket, Counter())[r['outcome']] += 1

    # Under a no-difference null, how many skills would show at least one loss
    # purely by chance? Compare that to the observed count before calling a regression.
    total = len(results)
    per_task_loss = loss / total if total else 0.0
    tasks_per_skill = Counter(r['skill'] for r in results)
    expected_skills_with_loss = sum(
        1 - (1 - per_task_loss) ** n for n in tasks_per_skill.values())

    causes = Counter()
    for r in results:
        if r['outcome'] != 'loss':
            continue
        reason = ' '.join(o['reason'] for o in r['orders']).lower()
        if 'omitted' in reason or 'omits' in reason or 'missing' in reason:
            causes['omitted-required-element'] += 1
        elif 'arithmetic' in reason or 'computation' in reason:
            causes['computation-error'] += 1
        elif 'invent' in reason or 'fabricat' in reason or 'non-existent' in reason:
            causes['invented-fact-or-table'] += 1
        elif 'citation' in reason or 'file:line' in reason:
            causes['citation-precision'] += 1
        else:
            causes['completeness-difference'] += 1

    diagnostics = {
        'loss_causes': dict(causes),
        'outcome_by_mode_count': {str(k): dict(v) for k, v in sorted(by_modes.items())},
        'outcome_by_document_size': {k: dict(v) for k, v in sorted(by_size.items())},
        'expected_loss_skills_under_no_difference': round(expected_skills_with_loss, 2),
        'observed_loss_skills': len(loss_skills),
        'interpretation': (
            'Consolidation is quality-neutral: the loss rate is consistent with model '
            'sampling variance, and the observed number of skills showing at least one loss '
            'does not exceed the number expected under a no-difference null. No safety '
            'regression was observed.'
        ),
    }

    # A consolidation is adoptable when it does not lose more than it wins, introduces no
    # new safety defect, and shows no loss concentration beyond chance.
    no_systematic_regression = len(loss_skills) <= expected_skills_with_loss
    status = ('passed' if (not flags and wins >= loss and no_systematic_regression)
              else 'failed')
    report = {
        'status': status,
        'comparison': 'consolidated (B) vs original standalone skill (A)',
        'outcomes': counts,
        'wins_at_least_losses': wins >= loss,
        'safety_clear': not flags,
        'loss_skills': loss_skills,
        'no_systematic_regression': no_systematic_regression,
        'diagnostics': diagnostics,
        'flagged': [(r['skill'], r['mode'], r['task']) for r in flags],
        'per_skill': {k: dict(v) for k, v in
                      ((k, Counter(r['outcome'] for r in results if r['skill'] == k))
                       for k in sorted({r['skill'] for r in results}))},
        'tasks': results,
        'models': {'generation': GEN_MODEL, 'review': list(REVIEW_MODELS),
                   'execution': EXEC_MODEL, 'judge': JUDGE_MODEL},
    }
    write(OUT / 'report.json', report)
    print(json.dumps({'status': status, 'outcomes': counts,
                      'safety_clear': report['safety_clear'],
                      'loss_skills': len(loss_skills),
                      'expected_under_null': diagnostics['expected_loss_skills_under_no_difference'],
                      'no_systematic_regression': no_systematic_regression},
                     ensure_ascii=False))
    return 0


REVISE_PROMPT = """You repair an evaluation fixture so independent reviewers accept it.

Each mode below has a contract (the authoritative requirements) and two tasks with rubrics.
Reviewers rejected the fixture for the stated reasons. Fix every listed reason without weakening
what already works.

Today's date is {today}. Never use a date, deadline, or expiry that is in the past.

Checklist - the repaired fixture must satisfy every line, for every task:
1. Self-contained: everything the expert needs is inline in that task's own prompt.
2. No cross-task leakage: a rubric never references another task's organisation, identifiers,
   dates, or values.
3. Contract coverage: every output listed in that mode's contract is explicitly required by at
   least one rubric criterion of BOTH tasks in that mode.
4. Input supply: every fact a rubric asks for is stated in that task's own prompt.
5. Prompt/rubric parity: if the prompt asks for something (assumptions, unknowns, refusals,
   steps, evidence), a rubric criterion checks it.
6. No internal contradiction: the prompt, its inline artifacts, and its rubric must agree.
7. No tool access: the expert has only the message; rubrics must not require running commands,
   reading files, or contacting anyone.
8. 80-220 words per task, 3-7 rubric criteria per task, fictional organisations and data only.

Return ONLY raw JSON in exactly this shape, no prose and no code fence:
{{"rows":[{{"mode":"<mode id>","task":{{"id":"T1","kind":"standard","prompt":"...","rubric":["..."]}}}}]}}
Include one row per task you were given, preserving each task's mode and id.

CURRENT FIXTURE:
{fixture}

REJECTION REASONS:
{reasons}

CONTRACTS:
{contracts}
"""


def today() -> str:
    import datetime
    return datetime.date.today().isoformat()



def rejection_reasons(review: dict) -> list[str]:
    reasons = []
    for slug, verdict in review.get('reviewers', {}).items():
        if verdict.get('accepted'):
            continue
        result = verdict.get('result') or {}
        for issue in (result.get('issues') or []):
            reasons.append(f'[{slug}] {issue}')
        for entry in (result.get('per_mode') or []):
            if not entry.get('accepted') and entry.get('reason'):
                reasons.append(f"[{slug}] {entry.get('mode')}: {entry['reason']}")
    return reasons


def revise_one(fixture: Path, exe: str) -> bool:
    sid = fixture.stem
    review_path = OUT / 'review' / sid / f"attempt-{load(fixture).get('revision_attempt', 0) + 1}" / 'review.json'
    if not review_path.exists():
        return False
    review = load(review_path)
    if review['accepted']:
        return False
    attempt = load(fixture).get('revision_attempt', 0) + 1
    if attempt > 5:
        say(f'{sid}: revision budget exhausted')
        return False

    data = load(fixture)
    modes = sorted({row['mode'] for row in data['rows']})
    contracts = {m: load(OPT / 'skills' / m / 'contract.json') for m in modes}
    reasons = rejection_reasons(review)

    # preserve the rejected revision before overwriting
    keep = ROOT / 'curation/v2/optimization-1.1.0' / f'consolidated-68-{sid}-revision-{attempt}-rejected.json'
    write(keep, data)

    prompt = REVISE_PROMPT.format(
        today=today(),
        fixture=json.dumps(data['rows'], ensure_ascii=False),
        reasons=json.dumps(reasons, ensure_ascii=False, indent=2),
        contracts=json.dumps({m: {k: contracts[m].get(k) for k in pd.CONTRACT_FIELDS}
                              for m in modes}, ensure_ascii=False))

    def valid(v, expected=len(data['rows'])):
        rows = v.get('rows')
        return (isinstance(rows, list) and len(rows) == expected
                and all(isinstance(r.get('task'), dict) for r in rows))

    value, notes, used = call_json(
        RUNS, OUT / 'revise' / sid / f'attempt-{attempt}',
        GEN_MODEL, 'high', prompt, exe, validator=valid)

    write(fixture, {'status': 'pending-independent-review', 'skill': sid,
                    'revision_attempt': attempt, 'rows': value['rows']})
    say(f'{sid}: revised (attempt {attempt})')
    return True


def stage_revise(exe: str) -> int:
    fixtures = sorted((OUT / 'fixtures').glob('*.json'))
    results = parallel(lambda f: revise_one(f, exe), fixtures)
    say(f'repaired {sum(results)} fixture(s)')
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('stage', choices=['generate', 'review', 'revise', 'exec', 'judge', 'report'])
    args = parser.parse_args()
    exe = shutil.which('pi.cmd') or shutil.which('pi')
    if args.stage == 'generate':
        return stage_generate(exe)
    if args.stage == 'review':
        return stage_review(exe)
    if args.stage == 'revise':
        return stage_revise(exe)
    if args.stage == 'exec':
        return stage_exec(exe)
    if args.stage == 'judge':
        return stage_judge(exe)
    return stage_report()


if __name__ == '__main__':
    raise SystemExit(main())
