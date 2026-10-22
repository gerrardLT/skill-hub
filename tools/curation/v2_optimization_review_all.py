"""Sequential independent review of post-freeze generated fixtures; reject -> stop, never auto-accept."""
import hashlib
import json
import shutil
from pathlib import Path
import v2_skill_audit_phase_d as pd
import v2_optimization_budget as budget


def main():
    ws = Path('.').resolve()
    control = ws/'curation/v2/optimization-1.1.0'
    root = ws/budget.RUNS
    progress = pd.load(control/'full-generation-progress.json')
    if progress['status'] != 'generation-complete-review-pending':
        raise RuntimeError('generation must be finished before independent review starts')
    frozen = pd.load(control/'candidate-freeze.json')
    for item in frozen['files']:
        if hashlib.sha256((ws/item['path']).read_bytes()).hexdigest() != item['sha256']:
            raise RuntimeError('candidate drift')
    exe = shutil.which('pi.cmd') or shutil.which('pi')
    if not exe:
        raise RuntimeError('pi unavailable')
    results = []
    for item in progress['items']:
        sid = item['skill']
        if item['status'] != 'generated-pending-review':
            results.append({'skill': sid, 'status': 'post-freeze-supplement-required'})
            continue
        fixture = root/'fresh-gen'/sid/'attempt-1/fixture-validation.json'
        data = pd.load(fixture)
        cap_path = ws/f'curation/v2/capabilities/{sid}.json'
        cap = pd.load(cap_path)
        accepted_revisions = sorted((root/'full-fixture-review'/sid).glob('attempt-*/freeze.json'))
        if accepted_revisions:
            frozen_revision = pd.load(accepted_revisions[-1])
            source = ws/frozen_revision['fixture_path']
            if hashlib.sha256(source.read_bytes()).hexdigest() != frozen_revision['fixture_sha256']:
                raise RuntimeError('accepted fixture revision drift')
            review_path = accepted_revisions[-1].parent/'review.json'
            if hashlib.sha256(review_path.read_bytes()).hexdigest() != frozen_revision['review_sha256']:
                raise RuntimeError('accepted fixture review drift')
            reviewed = pd.load(review_path)
            value = reviewed.get('result')
            if not isinstance(value, dict) or value.get('accepted') is not True or len(value.get('per_task', [])) != 2 or {t.get('id') for t in value['per_task']} != {'T1', 'T2'} or not all(t.get('accepted') is True for t in value['per_task']):
                raise RuntimeError('accepted freeze lacks valid independent review')
            results.append({'skill':sid,'status':'accepted','freeze_path':accepted_revisions[-1].relative_to(ws).as_posix()})
            continue
        directory = root/'full-fixture-review'/sid/'attempt-1'
        prompt = 'Return ONLY raw JSON {"accepted":boolean,"issues":[string],"per_task":[{"id":string,"accepted":boolean,"reason":string}]}. Independently check BOTH tasks against the original contract: technical rubric accuracy, supplied authority, observable fairness, self-contained synthetic data and no-tool/proposal-only boundaries. Do not execute tasks or infer optimized Skill text. Reject concrete defects; report advisory gaps separately.\nCONTRACT:\n'+json.dumps({k:cap[k] for k in pd.CONTRACT_FIELDS},ensure_ascii=False)+'\nTASKS:\n'+json.dumps(data['tasks'],ensure_ascii=False)
        if not (directory/'run.json').exists():
            budget.require_budget(root,100_000)
        run = pd.call(directory,pd.JUDGE_MODEL,'medium',prompt,exe,900)
        value, notes = pd.parse_json(run['output'])
        ok = run['exit_status']=='completed' and run['prompt_sha256']==pd.sha(prompt) and isinstance(value,dict) and value.get('accepted') is True and len(value.get('per_task',[]))==2 and {t.get('id') for t in value['per_task']}=={'T1','T2'} and all(t.get('accepted') is True for t in value['per_task'])
        pd.write(directory/'review.json',{'status':'accepted' if ok else 'rejected-or-invalid','result':value,'parse_notes':notes})
        if ok:
            pd.write(directory/'freeze.json',{'status':'accepted-not-executed','tasks':data['tasks'],'fixture_path':fixture.relative_to(ws).as_posix(),'fixture_sha256':hashlib.sha256(fixture.read_bytes()).hexdigest(),'review_sha256':hashlib.sha256((directory/'review.json').read_bytes()).hexdigest(),'contract_sha256':hashlib.sha256(cap_path.read_bytes()).hexdigest(),'limitations':value.get('issues',[])})
        results.append({'skill':sid,'status':'accepted' if ok else 'rejected-or-invalid'})
        pd.write(control/'full-review-progress.json',{'status':'in-progress' if ok else 'blocked-review','items':results})
        print(sid,results[-1]['status'],flush=True)
        if not ok:
            return 1
    pd.write(control/'full-review-progress.json',{'status':'reviewed-generation-supplements-still-required','items':results})
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
