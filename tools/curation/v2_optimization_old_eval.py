"""Evaluate repaired optimization candidate on the frozen pre-revision old task set."""
import argparse, concurrent.futures, json, shutil
from collections import Counter
from pathlib import Path
import v2_skill_audit_phase_d as pd
import v2_optimization_budget as budget

TASKS=Path('evals/runs/capability-compiler-v2/skill-audit/phase-d/task-set.json')
CAND=Path('evals/candidates/capability-compiler-v2/optimization-1.1.0/skills')
STRUCT=Path('curation/v2/optimization-1.1.0/structure.json')
JUDGE='taomu/gpt-5.6-sol'

def main():
 ap=argparse.ArgumentParser();ap.add_argument('stage',choices=['exec','judge','report']);ap.add_argument('--concurrency',type=int,default=1);ap.add_argument('--judge-model',default=JUDGE);ap.add_argument('--judge-root',default='judge');a=ap.parse_args();
 if not 1<=a.concurrency<=4:raise ValueError('concurrency must be 1..4')
 w=Path('.').resolve();root=w/budget.RUNS/'old-regression-post-fix';exe=shutil.which('pi.cmd') or shutil.which('pi');tasks=pd.load(w/TASKS)['skills'];merges=pd.load(w/STRUCT)['merges'];results=[]
 def call(d,m,think,p):
  needs=not (d/'run.json').exists()
  if needs:budget.require_budget(w/budget.RUNS,100000,a.concurrency)
  try:r=pd.call(d,m,think,p,exe,900)
  finally:
   if needs:budget.release_budget(100000)
  if r['exit_status']!='completed' or r['prompt_sha256']!=pd.sha(p) or r['output_sha256']!=pd.sha(r['output']):raise RuntimeError(str(d))
  return r
 rows=[(source_sid,merges.get(source_sid,source_sid),t) for source_sid,e in sorted(tasks.items()) for t in e['tasks']]
 if a.stage=='exec':
  jobs=[]
  for source_sid,sid,t in rows:
   for v,base in [('v100',w/'slots/v2/1.0.0/skills'),('optimized',w/CAND)]:
    skill=(base/(source_sid if v=='v100' else sid)/'SKILL.md').read_text(encoding='utf-8');p=pd.EXEC_PROMPT.format(method=pd.METHOD_BLOCK.format(skill=skill),task=t['prompt']);jobs.append((root/'exec'/f'{source_sid}__{t["id"]}__{v}',p))
  with concurrent.futures.ThreadPoolExecutor(max_workers=a.concurrency) as pool:list(pool.map(lambda x:call(x[0],pd.EXEC_MODEL,'low',x[1]),jobs))
  return
 if a.stage=='judge':
  jobs=[]
  for source_sid,sid,t in rows:
   outs={}
   for v,base in [('v100',w/'slots/v2/1.0.0/skills'),('optimized',w/CAND)]:
    skill=(base/(source_sid if v=='v100' else sid)/'SKILL.md').read_text(encoding='utf-8');p=pd.EXEC_PROMPT.format(method=pd.METHOD_BLOCK.format(skill=skill),task=t['prompt']);d=root/'exec'/f'{source_sid}__{t["id"]}__{v}';r=pd.load(d/'run.json');outs[v]=r['output']
   for order in ('xy','yx'):
    x,y=('optimized','v100') if order=='xy' else ('v100','optimized');p=pd.JUDGE_PROMPT.format(task=t['prompt'],rubric='\n'.join('- '+z for z in t['rubric']),a=outs[x],b=outs[y]);jobs.append((root/a.judge_root/f'{source_sid}__{t["id"]}__{order}',p))
  def judge_call(job):
   r=call(job[0],a.judge_model,'medium',job[1]);v,n=pd.parse_json(r['output'])
   if not isinstance(v,dict) or v.get('overall') not in ('A','B','tie') or set(v.get('overreach',{}))!={'A','B'} or set(v.get('fabrication',{}))!={'A','B'}:raise RuntimeError(f'invalid judge: {job[0]}')
   return True
  with concurrent.futures.ThreadPoolExecutor(max_workers=a.concurrency) as pool:list(pool.map(judge_call,jobs))
  return
 for source_sid,sid,t in rows:
   outs={}
   for v,base in [('v100',w/'slots/v2/1.0.0/skills'),('optimized',w/CAND)]:
    skill=(base/(source_sid if v=='v100' else sid)/'SKILL.md').read_text(encoding='utf-8');p=pd.EXEC_PROMPT.format(method=pd.METHOD_BLOCK.format(skill=skill),task=t['prompt']);d=root/'exec'/f'{source_sid}__{t["id"]}__{v}';r=pd.load(d/'run.json');outs[v]=r['output']
   orders=[]
   for order in ('xy','yx'):
    x,y=('optimized','v100') if order=='xy' else ('v100','optimized');p=pd.JUDGE_PROMPT.format(task=t['prompt'],rubric='\n'.join('- '+z for z in t['rubric']),a=outs[x],b=outs[y]);d=root/a.judge_root/f'{source_sid}__{t["id"]}__{order}';r=call(d,a.judge_model,'medium',p) if a.stage=='judge' else pd.load(d/'run.json');v,n=pd.parse_json(r['output'])
    if not isinstance(v,dict) or v.get('overall') not in ('A','B','tie'):raise RuntimeError('invalid judge')
    mine='A' if order=='xy' else 'B';other='B' if mine=='A' else 'A';orders.append({'order':order,'outcome':'tie' if v['overall']=='tie' else 'win' if v['overall']==mine else 'loss','new_overreach':bool(v['overreach'][mine]) and not bool(v['overreach'][other]),'new_fabrication':bool(v['fabrication'][mine]) and not bool(v['fabrication'][other]),'reason':v['reason']})
   if a.stage=='report':results.append({'source_skill':source_sid,'candidate_skill':sid,'task':t['id'],'outcome':orders[0]['outcome'] if orders[0]['outcome']==orders[1]['outcome'] else 'tie','new_overreach':all(x['new_overreach'] for x in orders),'new_fabrication':all(x['new_fabrication'] for x in orders),'orders':orders})
 if a.stage=='report':
  counts=dict(Counter(x['outcome'] for x in results));both={}
  for x in results:
   if x['outcome']=='loss':both.setdefault(x['source_skill'],0);both[x['source_skill']]+=1
  safe=not any(x['new_overreach'] or x['new_fabrication'] for x in results);pd.write(root/f'report-{a.judge_root}.json',{'status':'measured','outcomes':counts,'tasks':results,'judge_model':a.judge_model,'judge_root':a.judge_root,'wins_at_least_losses':counts.get('win',0)>=counts.get('loss',0),'safety_clear':safe,'loss_skills':sorted(both)});print(json.dumps({'outcomes':counts,'safety_clear':safe,'loss_skills':sorted(both)}))
if __name__=='__main__':main()
