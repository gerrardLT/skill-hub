"""Budget-controlled full head-to-head evaluation on frozen accepted tasks."""
import argparse
import concurrent.futures
import hashlib
import json
import shutil
from pathlib import Path
import v2_skill_audit_phase_d as pd
import v2_optimization_budget as budget

CONTROL = Path('curation/v2/optimization-1.1.0')
CAND = Path('evals/candidates/capability-compiler-v2/optimization-1.1.0')


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('stage', choices=['exec','judge','report'])
    ap.add_argument('--concurrency', type=int, default=1)
    ap.add_argument('--timeout', type=int, default=900)
    ap.add_argument('--judge-model', default=pd.JUDGE_MODEL)
    ap.add_argument('--judge-root', default='judge')
    args = ap.parse_args()
    if args.concurrency < 1 or args.concurrency > 8:
        raise ValueError('concurrency must be 1..8')
    ws = Path('.').resolve(); root = ws/budget.RUNS/'full'; doc = pd.load(ws/CONTROL/'full-task-set.json')
    freeze = pd.load(ws/CONTROL/'candidate-freeze.json')
    if hashlib.sha256((ws/CONTROL/'candidate-freeze.json').read_bytes()).hexdigest()!=doc['candidate_freeze_sha256']:
        raise RuntimeError('candidate freeze changed')
    for f in freeze['files']:
        if hashlib.sha256((ws/f['path']).read_bytes()).hexdigest()!=f['sha256']:
            raise RuntimeError('candidate drift')
    if pd.sha(json.dumps(doc['skills'],ensure_ascii=False,sort_keys=True))!=doc['task_set_sha256']:
        raise RuntimeError('task set changed')
    exe = shutil.which('pi.cmd') or shutil.which('pi'); results=[]
    def invoke(directory, model, thinking, prompt):
        reserve=100000
        needs_call=not (directory/'run.json').exists()
        if needs_call: budget.require_budget(ws/budget.RUNS,reserve,args.concurrency)
        try:
            run=pd.call(directory,model,thinking,prompt,exe,args.timeout)
        finally:
            if needs_call: budget.release_budget(reserve)
        if run['exit_status']!='completed' or run['prompt_sha256']!=pd.sha(prompt) or run['output_sha256']!=pd.sha(run['output']):
            raise RuntimeError(f'failed/stale evidence: {directory}')
        return run
    task_rows=[]
    for sid, entry in sorted(doc['skills'].items()):
        frozen_path=ws/entry['freeze_path']
        if hashlib.sha256(frozen_path.read_bytes()).hexdigest()!=entry['freeze_sha256']: raise RuntimeError('fixture freeze drift')
        for task in entry['tasks']:
            task_rows.append((sid,task))
    if args.stage=='exec':
        jobs=[]
        for sid,task in task_rows:
            for variant,base in [('v100',Path('slots/v2/1.0.0/skills')),('optimized',CAND/'skills')]:
                skill=(ws/base/sid/'SKILL.md').read_text(encoding='utf-8')
                prompt=pd.EXEC_PROMPT.format(method=pd.METHOD_BLOCK.format(skill=skill),task=task['prompt'])
                jobs.append((sid,task['id'],variant,root/'exec'/f'{sid}__{task["id"]}__{variant}',prompt))
        def execute_one(job):
            sid,tid,variant,directory,prompt=job
            run=invoke(directory,pd.EXEC_MODEL,'low',prompt)
            if run['exit_status']!='completed' or run['prompt_sha256']!=pd.sha(prompt) or run['output_sha256']!=pd.sha(run['output']): raise RuntimeError(f'invalid execution input: {directory}')
            return sid,tid,variant
        with concurrent.futures.ThreadPoolExecutor(max_workers=args.concurrency) as pool:
            for sid,tid,variant in pool.map(execute_one,jobs): print(sid,tid,variant,'exec completed',flush=True)
        return
    judge_rows=[]
    for sid, task in task_rows:
        outputs={}
        for variant,base in [('v100',Path('slots/v2/1.0.0/skills')),('optimized',CAND/'skills')]:
            skill=(ws/base/sid/'SKILL.md').read_text(encoding='utf-8')
            prompt=pd.EXEC_PROMPT.format(method=pd.METHOD_BLOCK.format(skill=skill),task=task['prompt'])
            directory=root/'exec'/f'{sid}__{task["id"]}__{variant}'
            run=pd.load(directory/'run.json')
            if run['exit_status']!='completed' or run['prompt_sha256']!=pd.sha(prompt) or run['output_sha256']!=pd.sha(run['output']):raise RuntimeError('invalid execution input')
            outputs[variant]=run['output']
        for order in ('xy','yx'):
            a,b=('optimized','v100') if order=='xy' else ('v100','optimized')
            prompt=pd.JUDGE_PROMPT.format(task=task['prompt'],rubric='\n'.join('- '+x for x in task['rubric']),a=outputs[a],b=outputs[b])
            judge_rows.append((sid,task['id'],order,root/args.judge_root/f'{sid}__{task["id"]}__{order}',prompt))
    def judge_one(row):
        sid,tid,order,directory,prompt=row
        run=invoke(directory,args.judge_model,'medium',prompt) if args.stage=='judge' else pd.load(directory/'run.json')
        value,notes=pd.parse_json(run['output'])
        if run['exit_status']!='completed' or run['prompt_sha256']!=pd.sha(prompt) or run['output_sha256']!=pd.sha(run['output']) or not isinstance(value,dict) or value.get('overall') not in ('A','B','tie') or set(value.get('overreach',{}))!={'A','B'} or set(value.get('fabrication',{}))!={'A','B'}:
            raise RuntimeError(f'invalid judge: {directory}')
        mine='A' if order=='xy' else 'B';other='B' if mine=='A' else 'A'
        return sid,tid,{'order':order,'outcome':'tie' if value['overall']=='tie' else 'win' if value['overall']==mine else 'loss','new_overreach':value['overreach'][mine] and not value['overreach'][other],'new_fabrication':value['fabrication'][mine] and not value['fabrication'][other],'reason':value['reason']}
    if args.stage=='judge':
        with concurrent.futures.ThreadPoolExecutor(max_workers=args.concurrency) as pool:
            for sid,tid,order in ((s,t,o['order']) for s,t,o in pool.map(judge_one,judge_rows)): print(sid,tid,order,'judge completed',flush=True)
        return
    grouped={}
    for sid,tid,order in map(judge_one,judge_rows): grouped.setdefault((sid,tid),[]).append(order)
    for (sid,tid),orders in grouped.items():
        orders=sorted(orders,key=lambda x:x['order'])
        results.append({'skill':sid,'task':tid,'outcome':orders[0]['outcome'] if orders[0]['outcome']==orders[1]['outcome'] else 'tie','new_overreach':all(x['new_overreach'] for x in orders),'new_fabrication':all(x['new_fabrication'] for x in orders),'orders':orders})
    if args.stage=='report':
        from collections import Counter
        counts=dict(Counter(r['outcome'] for r in results));pd.write(root/f'report-{args.judge_root}.json',{'status':'measured-pending-final-acceptance','judge_model':args.judge_model,'judge_root':args.judge_root,'outcomes':counts,'tasks':results,'task_set_sha256':doc['task_set_sha256'],'wins_at_least_losses':counts.get('win',0)>=counts.get('loss',0),'limitations':['two tasks per Skill; one judge model in both orders','atomic single-call comparison; synthesis composition separately evaluated','old regression, runtime behavior and routing gates still required']});print(counts)


if __name__=='__main__':main()
