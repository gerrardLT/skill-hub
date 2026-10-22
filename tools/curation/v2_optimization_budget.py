"""Read-only token accounting; includes failed calls and exposes unknown usage."""
import json
import threading
from pathlib import Path

RUNS = Path('evals/runs/capability-compiler-v2/optimization-1.1.0')
LIMIT = 50_000_000
_LOCK = threading.Lock()
_RESERVED = 0


def inspect(root):
    tokens = calls = unknown = failed = 0
    for path in root.rglob('run.json'):
        run = json.loads(path.read_text(encoding='utf-8'))
        calls += 1
        failed += run.get('exit_status') != 'completed'
        usage = run.get('token_usage', {})
        value = usage.get('totalTokens')
        if not isinstance(value, int) or isinstance(value, bool) or value < 0:
            unknown += 1
        else:
            tokens += value
    partial = sum(not (p.parent / 'run.json').exists() for p in root.rglob('prompt.md'))
    return {'calls': calls, 'failed_calls': failed, 'recorded_tokens': tokens, 'unknown_usage_calls': unknown, 'partial_calls': partial, 'limit': LIMIT, 'remaining_recorded_tokens': max(0, LIMIT-tokens)}


def require_budget(root, reserve, allow_active_partials=0):
    global _RESERVED
    if not isinstance(reserve, int) or isinstance(reserve, bool) or reserve <= 0:
        raise ValueError('positive per-call token reserve required')
    if not isinstance(allow_active_partials, int) or isinstance(allow_active_partials, bool) or allow_active_partials < 0:
        raise ValueError('allow_active_partials must be a non-negative integer')
    with _LOCK:
        status = inspect(root)
        if status['recorded_tokens'] + _RESERVED + reserve > LIMIT:
            raise RuntimeError('optimization token budget exhausted or insufficient reserve')
        if status['unknown_usage_calls'] or status['partial_calls'] > allow_active_partials:
            raise RuntimeError('unknown or partial call usage requires reconciliation before more calls')
        _RESERVED += reserve
        return status


def release_budget(reserve):
    global _RESERVED
    with _LOCK:
        _RESERVED -= reserve
        if _RESERVED < 0:
            _RESERVED = 0
            raise RuntimeError('budget reservation underflow')


if __name__ == '__main__':
    print(json.dumps(inspect(RUNS), indent=2))
