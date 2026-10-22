"""Run owner-corrected frozen routing cases against repaired optimization candidate."""
import hashlib,json,shutil
from pathlib import Path
import v2_skill_audit_phase_d as pd
import v2_optimization_budget as budget
from v2_phase9_runner import ROUTER_SYSTEM

def main():
 w=Path('.').resolve();control=w/'curation/v2/optimization-1.1.0';cand=w/'evals/candidates/capability-compiler-v2/optimization-1.1.0';plan_path=w/'curation/v2/revision-1.1.0/routing-regression-plan-v2.json';plan=pd.load(plan_path);freeze=pd.load(control/'candidate-freeze-post-safety-fix.json')
 fm={x['path']:x['sha256'] for x in freeze['files']}
 for rel in ['recipes/router.json','skill-index.json']:
  p=cand/rel
  if hashlib.sha256(p.read_bytes()).hexdigest()!=fm[p.relative_to(w).as_posix()]:raise RuntimeError('candidate routing drift')
 router=pd.load(cand/'recipes/router.json');index=pd.load(cand/'skill-index.json');material=json.dumps({'router':router,'atomic_targets':index['skills']},ensure_ascii=False);root=w/budget.RUNS/'routing-post-fix';exe=shutil.which('pi.cmd') or shutil.which('pi');results=[]
 for case in plan['cases']:
  prompt=f"{ROUTER_SYSTEM}\nUSER REQUEST:\n{case['input']}\n\nROUTER MATERIAL:\n{material}";d=root/case['id']
  if not (d/'run.json').exists():budget.require_budget(w/budget.RUNS,100000)
  run=pd.call(d,plan['model'],'low',prompt,exe,900);value,notes=pd.parse_json(run['output']);valid=isinstance(value,dict) and set(value)=={'target','reason','would_execute'};ok=run['exit_status']=='completed' and run['prompt_sha256']==pd.sha(prompt) and valid and value['target']==case['expected_target'] and value['would_execute'] is False;results.append({'id':case['id'],'expected':case['expected_target'],'actual':value,'passed':ok,'status':run['exit_status'],'parse_notes':notes});print(case['id'],ok,flush=True)
 report={'status':'passed' if all(x['passed'] for x in results) else 'failed','candidate_freeze':hashlib.sha256((control/'candidate-freeze-post-safety-fix.json').read_bytes()).hexdigest(),'plan_sha256':hashlib.sha256(plan_path.read_bytes()).hexdigest(),'passed':sum(x['passed'] for x in results),'total':len(results),'cases':results,'historical_20_of_22_preserved':'evals/runs/capability-compiler-v2/revision-1.1.0-eval/routing/report.json'};pd.write(root/'report.json',report);return 0 if report['status']=='passed' else 1
if __name__=='__main__':raise SystemExit(main())
