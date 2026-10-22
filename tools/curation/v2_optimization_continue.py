"""Follow the already-running execution; then judge and report. Never duplicates active execution."""
import hashlib
import json
import subprocess
import sys
import time
from pathlib import Path
import v2_skill_audit_phase_d as pd
import v2_optimization_budget as budget

CONTROL = Path('curation/v2/optimization-1.1.0')
ROOT = budget.RUNS/'full'


def execution_status(ws):
    tasks = pd.load(ws/CONTROL/'full-task-set.json')['skills']
    valid = missing = 0
    errors = []
    for sid, entry in tasks.items():
        for task in entry['tasks']:
            for variant, base in [('v100',Path('slots/v2/1.0.0/skills')),('optimized',Path('evals/candidates/capability-compiler-v2/optimization-1.1.0/skills'))]:
                directory = ws/ROOT/'exec'/f'{sid}__{task["id"]}__{variant}'
                p = directory/'run.json'
                if not p.exists():
                    missing += 1
                    continue
                run = pd.load(p)
                method = (ws/base/sid/'SKILL.md').read_text(encoding='utf-8')
                prompt = pd.EXEC_PROMPT.format(method=pd.METHOD_BLOCK.format(skill=method),task=task['prompt'])
                if run.get('exit_status')!='completed' or run.get('prompt_sha256')!=pd.sha(prompt) or run.get('output_sha256')!=pd.sha(run.get('output','')):
                    errors.append(str(p))
                else:
                    valid += 1
    return {'valid':valid,'missing':missing,'errors':errors,'expected':sum(len(e['tasks'])*2 for e in tasks.values())}


def main():
    ws = Path('.').resolve()
    evidence = ws/CONTROL/'continuation-state.json'
    last = None
    last_progress = time.monotonic()
    while True:
        status = execution_status(ws)
        pd.write(evidence,{'stage':'waiting-for-existing-execution','execution':status,'recorded_at':pd.utc_now()})
        if status['errors']:
            raise RuntimeError('execution failed or stale; preserve evidence and diagnose')
        if status['valid']==status['expected'] and not status['missing']:
            break
        if status['valid']!=last:
            last=status['valid'];last_progress=time.monotonic()
        if time.monotonic()-last_progress>1800:
            raise RuntimeError('existing execution stalled for 30 minutes; no duplicate execution launched')
        time.sleep(30)
    for stage in ('judge','report'):
        directory=ws/ROOT/'continuation-commands'/stage
        directory.mkdir(parents=True,exist_ok=True)
        argv=[sys.executable,'tools/curation/v2_optimization_full_eval.py',stage]
        start=time.perf_counter()
        with (directory/'stdout.txt').open('wb') as out, (directory/'stderr.txt').open('wb') as err:
            run=subprocess.run(argv,stdout=out,stderr=err)
        pd.write(directory/'receipt.json',{'argv':argv,'exit_code':run.returncode,'duration_ms':round((time.perf_counter()-start)*1000,3),'stdout_sha256':hashlib.sha256((directory/'stdout.txt').read_bytes()).hexdigest(),'stderr_sha256':hashlib.sha256((directory/'stderr.txt').read_bytes()).hexdigest()})
        if run.returncode:
            pd.write(evidence,{'stage':stage,'status':'failed-preserve-and-diagnose','exit_code':run.returncode})
            raise RuntimeError(f'{stage} failed')
    report=pd.load(ws/ROOT/'report.json')
    flags=[r for r in report['tasks'] if r['new_overreach'] or r['new_fabrication']]
    pd.write(evidence,{'stage':'fresh-evaluation-finished-final-acceptance-pending','outcomes':report['outcomes'],'wins_at_least_losses':report['wins_at_least_losses'],'safety_flag_count':len(flags),'budget':budget.inspect(ws/budget.RUNS),'remaining':['old regressions','composition and behavior checks','routing and final gates','measured regression disposition','final report and release preview'],'release_approved':False})


if __name__=='__main__':
    main()
