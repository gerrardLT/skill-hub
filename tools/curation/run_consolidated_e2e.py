"""Run consolidated-68 recipes end to end with real local models.

Two modes:
  python run_consolidated_e2e.py <stage-name> [step,step,...]
  python run_consolidated_e2e.py --composite <composite-name>

This drives the real executor against the real consolidated recipes with no mock worker, so
it is the decisive check for whether the full flow can actually run.
"""
from __future__ import annotations

import json
import shutil
import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path('tools/curation').resolve()))
import v2_optimization_budget as budget
from recipe_execute import execute_composite, execute_recipe

ROOT = Path('.').resolve()
CON = ROOT / 'evals/candidates/capability-compiler-v2/consolidated-68'
OUT = ROOT / 'evals/runs/capability-compiler-v2/optimization-1.1.0/consolidated-68-e2e'
MODEL = '本地workbuddy/global:deepseek-v4.1-flash'

BASE_INPUT = {
    'request': 'Add a Redis-backed per-tenant rate limiter to the public API.',
    'brief': (
        'Northwind Ledger needs per-tenant API rate limiting. Today all tenants share one '
        'quota, so a single noisy integration can exhaust capacity for everyone. Product '
        'wants a 100 requests/minute default per tenant with a configurable override, '
        'returning HTTP 429 with Retry-After when exceeded. Redis is already deployed for '
        'sessions. Out of scope: billing, per-endpoint quotas, and admin UI.'),
    'evidence': (
        'Last 30 days: 1 tenant produced 41% of all API calls and 3 separate incidents where '
        'other tenants saw elevated latency. No per-tenant quota mechanism exists today. '
        'Redis 7.2 is deployed with 2 replicas and is used for session storage.'),
    'constraints': (
        'No new infrastructure. Must not add more than 5 ms p95 latency to the request path. '
        'Must degrade open (allow the request) if Redis is unavailable, and log the bypass.'),
    'acceptance_intent': (
        'A tenant exceeding its quota receives 429 with Retry-After; other tenants are '
        'unaffected; Redis outage does not take down the API.'),
    'authority': (
        'Change authority RA-4471 covers the api-platform repository. API platform owner '
        'Nadia Osei owns this change. Production rollout approval PR-8891 was signed by the '
        'release board on 2026-09-02 and is attached. The decision owner for scope is Nadia '
        'Osei; the decision owner for rollout is the release board.'),
    'decisions': (
        'Tenant identity source: the `X-Tenant-Id` header, validated against the tenants '
        'table. Quota window: fixed 60-second tumbling window keyed on tenant and window '
        'start. Override source: the `tenant_quota_overrides` table, owned by the platform '
        'team. Retry-After value: seconds remaining in the current window, as an integer. '
        'Bypass log: structured JSON to the existing `api_events` topic, fields {tenant_id, '
        'reason, window_start}, retained 30 days. Redis failure detection: a command timeout '
        'of 50 ms or a connection error. Load profile: peak 8,000 requests/second across all '
        'tenants, p95 payload 12 KB. Shared Redis: the limiter uses a dedicated logical '
        'database, not the session database. Recovery: on Redis recovery the next request '
        'resumes normal evaluation with a fresh window. 429 body: RFC 9457 problem+json with '
        'type, title, status, and retry_after.'),
}


def make_worker(model: str):
    exe = shutil.which('pi.cmd') or shutil.which('pi')
    calls = {'n': 0, 'tokens': 0}

    def worker(prompt: str, timeout: int):
        budget.require_budget(ROOT / budget.RUNS, 100_000, allow_active_partials=4)
        calls['n'] += 1
        directory = OUT / 'calls' / f'{calls["n"]:03d}'
        directory.mkdir(parents=True, exist_ok=True)
        prompt_file = directory / 'prompt.md'
        prompt_file.write_text(prompt, encoding='utf-8', newline='\n')
        temp = directory / 'empty-cwd'
        temp.mkdir(exist_ok=True)
        argv = [exe, '-p', '--mode', 'json', '--model', model, '--thinking', 'low',
                '--no-tools', '--no-skills', '--no-extensions', '--no-context-files',
                '--no-session', '--system-prompt',
                'Do not use tools. Follow the prompt exactly.', f'@{prompt_file}']
        started = time.perf_counter()
        try:
            process = subprocess.run(argv, cwd=temp, capture_output=True, timeout=timeout,
                                     check=False)
        except subprocess.TimeoutExpired:
            budget.release_budget(100_000)
            raise RuntimeError(f'timeout-after-{timeout}s')
        finally:
            shutil.rmtree(temp, ignore_errors=True)
        events = []
        for line in process.stdout.decode('utf-8', 'replace').splitlines():
            try:
                events.append(json.loads(line))
            except json.JSONDecodeError:
                pass
        message = {}
        for event in events:
            if event.get('type') == 'message_end' and event.get('message', {}).get('role') == 'assistant':
                message = event['message']
        output = ''.join(p.get('text', '') for p in message.get('content', [])
                         if p.get('type') == 'text')
        usage = message.get('usage') or {}
        calls['tokens'] += usage.get('totalTokens') or 0
        (directory / 'run.json').write_text(json.dumps({
            'model': model, 'exit_status': 'completed' if output else 'failed',
            'token_usage': usage,
            'duration_ms': round((time.perf_counter() - started) * 1000, 1),
            'output': output,
        }, ensure_ascii=False, indent=2) + '\n', encoding='utf-8', newline='\n')
        budget.release_budget(100_000)
        if not output:
            raise RuntimeError('no-output')
        return output, {'model': model, 'tokens': usage.get('totalTokens')}

    return worker, calls


def write_input(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(BASE_INPUT, ensure_ascii=False, indent=2) + '\n',
                    encoding='utf-8', newline='\n')


def run_stage(stage: str, only: list[str] | None) -> int:
    recipe = CON / 'recipes/stages' / f'{stage}.json'
    data = json.loads(recipe.read_text(encoding='utf-8'))
    worker, calls = make_worker(MODEL)

    work = OUT / stage
    input_file = work / 'input.json'
    write_input(input_file)

    selected = only or [s['id'] for s in data['steps']]
    print(f"recipe: {stage} | steps: {len(selected)}/{len(data['steps'])} | model: {MODEL}")
    result = execute_recipe(
        recipe, input_file, work / 'output',
        workspace_root=ROOT, worker=worker,
        require_release_evidence=False, allow_evaluating=True,
        active_steps=list(only) if only else None,
    )
    (work / 'result.json').write_text(
        json.dumps(result, ensure_ascii=False, indent=2, default=str) + '\n',
        encoding='utf-8', newline='\n')

    print(f"\nstatus: {result['status']} | passed: {result['passed']}")
    print(f"model calls: {calls['n']} | tokens: {calls['tokens']:,}")
    print("\nper-step:")
    for s in result['steps_run']:
        gates = s.get('gates') or []
        ok = sum(1 for g in gates if g.get('passed') is True)
        adv = len(s.get('advisory_gates') or [])
        print(f"  {s['step_id']:<45} {s['status']:<10} gates {ok}/{len(gates)}  advisory {adv}")
    if result.get('skipped_steps'):
        print(f"\nskipped: {len(result['skipped_steps'])} step(s)")
    if result.get('errors'):
        print(f"\nerrors: {result['errors']}")
    return 0 if result['passed'] else 1


def run_composite(name: str) -> int:
    recipe = CON / 'recipes/composites' / f'{name}.json'
    data = json.loads(recipe.read_text(encoding='utf-8'))
    worker, calls = make_worker(MODEL)

    active_by_stage = {}
    for entry in data['stage_steps']:
        stage_name = entry['recipe_ref'].rsplit('@', 1)[0]
        stage = json.loads((CON / 'recipes/stages' / f'{stage_name}.json').read_text(encoding='utf-8'))
        active_by_stage[entry['stage_id']] = [s['id'] for s in stage['steps']]

    work = OUT / name
    input_file = work / 'input.json'
    write_input(input_file)

    print(f"composite: {name} | stages: {len(data['stage_steps'])} | model: {MODEL}")
    result = execute_composite(
        recipe, input_file, work / 'output',
        workspace_root=ROOT, active_by_stage=active_by_stage, worker=worker,
        require_release_evidence=False, allow_evaluating=True,
    )
    (work / 'composite-result.json').write_text(
        json.dumps(result, ensure_ascii=False, indent=2, default=str) + '\n',
        encoding='utf-8', newline='\n')

    print(f"\nstatus: {result['status']} | passed: {result['passed']}")
    print(f"model calls: {calls['n']} | tokens: {calls['tokens']:,}")
    print("\nper-stage:")
    for st in result['stages']:
        print(f"  {st['stage_order']}. {st['stage_id']:<45} {st['status']:<12} "
              f"steps={len(st['steps_run'])}/{len(st['activated_steps'])}")
    if result.get('stopped_at'):
        print(f"\nstopped at: {result['stopped_at']}")
    if result.get('errors'):
        print(f"errors: {result['errors']}")
    return 0 if result['passed'] else 1


def main() -> int:
    if len(sys.argv) > 2 and sys.argv[1] == '--composite':
        return run_composite(sys.argv[2])
    stage = sys.argv[1] if len(sys.argv) > 1 else 'stage-04-requirements-planning'
    only = sys.argv[2].split(',') if len(sys.argv) > 2 else None
    return run_stage(stage, only)


if __name__ == '__main__':
    raise SystemExit(main())
