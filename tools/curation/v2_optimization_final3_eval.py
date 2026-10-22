"""Review and evaluate final unseen tasks for five last-remediated Skills."""
import argparse,json,shutil
from collections import Counter
from pathlib import Path
import v2_skill_audit_phase_d as pd
import v2_optimization_budget as budget
SKILLS=['documentation-authoring','persona-jtbd-and-journey-modeling','qa-finding-triage']
CAND=Path('evals/candidates/capability-compiler-v2/optimization-1.1.0/skills');JUDGE='router9-qoder/cx/gpt-5.6-sol'
def main():
 ap=argparse.ArgumentParser();ap.add_argument('stage',choices=['review','exec','judge','report']);a=ap.parse_args();w=Path('.').resolve();base=w/budget.RUNS;root=base/'final3';exe=shutil.which('pi.cmd') or shutil.which('pi')
 def call(d,m,think,p):
  if not (d/'run.json').exists():budget.require_budget(base,100000)
  r=pd.call(d,m,think,p,exe,900)
  if r['exit_status']!='completed' or r['prompt_sha256']!=pd.sha(p) or r['output_sha256']!=pd.sha(r['output']):raise RuntimeError(str(d))
  return r
 if a.stage=='review':
  for sid in SKILLS:
   if sid=='documentation-authoring':fixture=w/'curation/v2/optimization-1.1.0/documentation-authoring-final3-revision-2.json';attempt='attempt-2'
   elif sid=='persona-jtbd-and-journey-modeling':fixture=w/'curation/v2/optimization-1.1.0/persona-jtbd-and-journey-modeling-final3-revision-5.json';attempt='attempt-7'
   elif sid=='qa-finding-triage':fixture=w/'curation/v2/optimization-1.1.0/qa-finding-triage-final3-revision-6.json';attempt='attempt-6'
   else:fixture=base/'fresh-gen'/sid/'attempt-4/fixture-validation.json';attempt='attempt-1'
   f=pd.load(fixture);cap=pd.load(w/f'curation/v2/capabilities/{sid}.json');p='Return ONLY raw JSON {"accepted":boolean,"issues":[string],"per_task":[{"id":string,"accepted":boolean,"reason":string}]}. This is fixture-design review, not answer grading. Review both NEW task prompts and rubrics against only the original contract for technical accuracy, complete observable coverage, self-contained inputs, no-tools boundaries and independence from all seen scenarios. No outputs exist yet and optimized text is unavailable.\nCONTRACT:\n'+json.dumps({k:cap[k] for k in pd.CONTRACT_FIELDS},ensure_ascii=False)+'\nTASKS:\n'+json.dumps(f['tasks'],ensure_ascii=False);d=root/'review'/sid/attempt;r=call(d,JUDGE,'medium',p);v,n=pd.parse_json(r['output']);ok=isinstance(v,dict) and v.get('accepted') is True and len(v.get('per_task',[]))==2 and all(x.get('accepted') is True for x in v['per_task']);pd.write(d/'review.json',{'accepted':ok,'result':v,'notes':n,'fixture_path':fixture.relative_to(w).as_posix()});print(sid,ok,flush=True)
   if not ok:return 1
  return 0
 rows=[]
 for sid in SKILLS:
  reviews=sorted((root/'review'/sid).rglob('review.json'),key=lambda p:p.stat().st_mtime);accepted=[p for p in reviews if pd.load(p).get('accepted') is True];rev=pd.load(accepted[-1] if accepted else root/'review'/sid/'review.json');
  if not rev['accepted']:raise RuntimeError(sid)
  f=pd.load(w/rev['fixture_path']);rows += [(sid,t) for t in f['tasks']]
 results=[]
 for sid,t in rows:
  outs={}
  for var,folder in [('v100',w/'slots/v2/1.0.0/skills'),('optimized',w/CAND)]:
   skill=(folder/sid/'SKILL.md').read_text(encoding='utf-8');p=pd.EXEC_PROMPT.format(method=pd.METHOD_BLOCK.format(skill=skill),task=t['prompt']);d=root/'exec'/f'{sid}__{t["id"]}__{var}';r=call(d,pd.EXEC_MODEL,'low',p) if a.stage=='exec' else pd.load(d/'run.json');outs[var]=r['output']
  if a.stage=='exec':continue
  orders=[]
  for order in ('xy','yx'):
   x,y=('optimized','v100') if order=='xy' else ('v100','optimized');p=pd.JUDGE_PROMPT.format(task=t['prompt'],rubric='\n'.join('- '+z for z in t['rubric']),a=outs[x],b=outs[y]);d=root/'judge'/f'{sid}__{t["id"]}__{order}';r=call(d,JUDGE,'medium',p) if a.stage=='judge' else pd.load(d/'run.json');v,n=pd.parse_json(r['output']);
   if not isinstance(v,dict) or v.get('overall') not in ('A','B','tie'):raise RuntimeError('invalid')
   mine='A' if order=='xy' else 'B';other='B' if mine=='A' else 'A';orders.append({'order':order,'outcome':'tie' if v['overall']=='tie' else 'win' if v['overall']==mine else 'loss','new_overreach':bool(v['overreach'][mine]) and not bool(v['overreach'][other]),'new_fabrication':bool(v['fabrication'][mine]) and not bool(v['fabrication'][other]),'reason':v['reason']})
  if a.stage=='report':results.append({'skill':sid,'task':t['id'],'outcome':orders[0]['outcome'] if orders[0]['outcome']==orders[1]['outcome'] else 'tie','new_overreach':all(x['new_overreach'] for x in orders),'new_fabrication':all(x['new_fabrication'] for x in orders),'orders':orders})
 if a.stage=='report':
  counts=dict(Counter(x['outcome'] for x in results));safe=not any(x['new_overreach'] or x['new_fabrication'] for x in results);loss=sorted({x['skill'] for x in results if x['outcome']=='loss'});pd.write(root/'report.json',{'status':'passed' if safe and not loss and counts.get('win',0)>=counts.get('loss',0) else 'failed','outcomes':counts,'safety_clear':safe,'loss_skills':loss,'tasks':results,'judge_model':JUDGE});print(json.dumps({'outcomes':counts,'safety_clear':safe,'loss_skills':loss}))
if __name__=='__main__':raise SystemExit(main())
