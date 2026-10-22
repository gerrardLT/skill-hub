"""Evaluate repaired Skills on independently reviewed unseen post-fix tasks."""
import argparse, hashlib, json, shutil
from collections import Counter
from pathlib import Path
import v2_skill_audit_phase_d as pd
import v2_optimization_budget as budget

CAND=Path('evals/candidates/capability-compiler-v2/optimization-1.1.0/skills')
FREEZES={
 'change-scope-freeze':Path('evals/runs/capability-compiler-v2/optimization-1.1.0/post-fix-fixture-review/change-scope-freeze/attempt-1/freeze.json'),
 'requirements-and-delivery-contract':Path('evals/runs/capability-compiler-v2/optimization-1.1.0/post-fix-fixture-review/requirements-and-delivery-contract/attempt-4/freeze.json'),
}
JUDGE='taomu/gpt-5.6-sol'

def main():
 ap=argparse.ArgumentParser();ap.add_argument('stage',choices=['exec','judge','report']);a=ap.parse_args();w=Path('.').resolve();root=w/budget.RUNS/'post-fix-eval';exe=shutil.which('pi.cmd') or shutil.which('pi');rows=[]
 for sid,fp in FREEZES.items():
  freeze=pd.load(w/fp);fixture=w/freeze['fixture_path'];review=w/fp.parent/'review.json'
  if hashlib.sha256(fixture.read_bytes()).hexdigest()!=freeze['fixture_sha256'] or hashlib.sha256(review.read_bytes()).hexdigest()!=freeze['review_sha256']:raise RuntimeError('post-fix fixture drift')
  for t in freeze['tasks']:rows.append((sid,t))
 def call(d,m,think,p):
  if not (d/'run.json').exists():budget.require_budget(w/budget.RUNS,100000)
  r=pd.call(d,m,think,p,exe,900)
  if r['exit_status']!='completed' or r['prompt_sha256']!=pd.sha(p) or r['output_sha256']!=pd.sha(r['output']):raise RuntimeError(str(d))
  return r
 results=[]
 for sid,t in rows:
  outs={}
  for v,base in [('v100',w/'slots/v2/1.0.0/skills'),('optimized',w/CAND)]:
   skill=(base/sid/'SKILL.md').read_text(encoding='utf-8');p=pd.EXEC_PROMPT.format(method=pd.METHOD_BLOCK.format(skill=skill),task=t['prompt']);d=root/'exec'/f'{sid}__{t["id"]}__{v}';r=call(d,pd.EXEC_MODEL,'low',p) if a.stage=='exec' else pd.load(d/'run.json');outs[v]=r['output']
  if a.stage=='exec':continue
  orders=[]
  for order in ('xy','yx'):
   x,y=('optimized','v100') if order=='xy' else ('v100','optimized');p=pd.JUDGE_PROMPT.format(task=t['prompt'],rubric='\n'.join('- '+z for z in t['rubric']),a=outs[x],b=outs[y]);d=root/'judge'/f'{sid}__{t["id"]}__{order}';r=call(d,JUDGE,'medium',p) if a.stage=='judge' else pd.load(d/'run.json');v,n=pd.parse_json(r['output'])
   if not isinstance(v,dict) or v.get('overall') not in ('A','B','tie'):raise RuntimeError('invalid judge')
   mine='A' if order=='xy' else 'B';other='B' if mine=='A' else 'A';orders.append({'order':order,'outcome':'tie' if v['overall']=='tie' else 'win' if v['overall']==mine else 'loss','new_overreach':bool(v['overreach'][mine]) and not bool(v['overreach'][other]),'new_fabrication':bool(v['fabrication'][mine]) and not bool(v['fabrication'][other]),'reason':v['reason']})
  if a.stage=='report':results.append({'skill':sid,'task':t['id'],'outcome':orders[0]['outcome'] if orders[0]['outcome']==orders[1]['outcome'] else 'tie','new_overreach':all(x['new_overreach'] for x in orders),'new_fabrication':all(x['new_fabrication'] for x in orders),'orders':orders})
 if a.stage=='report':
  counts=dict(Counter(x['outcome'] for x in results));safe=not any(x['new_overreach'] or x['new_fabrication'] for x in results);pd.write(root/'report.json',{'status':'passed' if counts.get('win',0)>=counts.get('loss',0) and safe else 'failed','outcomes':counts,'tasks':results,'judge_model':JUDGE,'safety_clear':safe});print(json.dumps({'outcomes':counts,'safety_clear':safe}))

if __name__=='__main__':main()
