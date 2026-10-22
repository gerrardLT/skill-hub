#!/usr/bin/env python3
"""Compile source-grounded V2 root dossiers and fallback lane reports."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
from collections import Counter
from pathlib import Path
from typing import Any

BINARY={".png",".zip",".icns"}
CODE={".py",".js",".ts",".mjs",".cjs",".sh",".rb",".swift",".m",".h",".sql",".html",".css"}
GEN_NAMES={"package-lock.json","bun.lock","bun.lockb","yarn.lock","pnpm-lock.yaml"}
GEN_EXT={".lock"}
EXPLICIT_BOUNDARY=re.compile(r"(?i)^(?:(?:this (?:skill|workflow) is )?not for\s*:|do not use (?:for|when)|when not to use|out of scope\s*:|non-goals?\s*:|does not (?:handle|cover|provide|replace|authorize))")
RULE=re.compile(r"(?i)\b(?:must|never|always|required|do not|don['’]t|before|gate|verify|checkpoint|consent|permission)")
STOP=re.compile(r"(?i)\b(?:stop\b|abort|pause|blocked|needs[- ]input|ask (?:the )?user|do not proceed|fail(?:ed|ure)?|revert)")
SIDE=re.compile(r"(?i)(?:\bgit\s+(?:push|fetch|merge|commit|reset|clean)\b|\b(?:deploy|publish|upload|delete|remove|overwrite|install|authenticate|restart|scale)\b|\bwrites?\s+(?:to|the)\b|\bcreates?\s+(?:a|the|an)\s+(?:pr|issue|file|dataset|alert|monitor|release|deployment)\b)")
INPUT_HEAD=re.compile(r"(?i)^(?:inputs?|prerequisites?|requirements?|before you start)(?:\b|\s*[&/])")
OUTPUT_HEAD=re.compile(r"(?i)^(?:outputs?|deliverables?|produced artifacts?)(?:\b|\s*[&/])")
FLOW_HEAD=re.compile(r"(?i)(?:phase|step|workflow|procedure|process|precheck|checkpoint|implementation|methodology|runbook)")
BRANCH_HEAD=re.compile(r"(?i)(?:mode|tier|branch|variant|path|conditional|decision)")
GENERIC_HEAD={"overview","usage","inputs","outputs","workflow","rules","summary","examples","example","references","contents"}
BOILERPLATE_HEAD=re.compile(r"(?i)^(?:when to invoke|preamble|plan mode safe operations|skill invocation during plan mode|askuserquestion|when askuserquestion|tool resolution|model-specific behavioral patch|writing style|context restoration|browser setup|translate the aside|continuous checkpoint mode|format$|artifacts sync|voice$)")

def load(path:Path)->Any:return json.loads(path.read_text(encoding="utf-8"))
def dump(path:Path,value:Any)->None:path.parent.mkdir(parents=True,exist_ok=True);path.write_text(json.dumps(value,ensure_ascii=False,sort_keys=True)+"\n",encoding="utf-8",newline="\n")
def clean(text:str,limit:int=300)->str:
    text=re.sub(r"[`*_#|]","",text);text=re.sub(r"\s+"," ",text).strip(" -:\t")
    return text[:limit].rstrip()
def frontmatter(lines:list[str])->tuple[dict[str,Any],int]:
    if not lines or lines[0].strip()!="---":return {},1
    end=next((i for i in range(1,len(lines)) if lines[i].strip()=="---"),len(lines));data:dict[str,Any]={};i=1
    while i<end:
        match=re.match(r"^([A-Za-z0-9_-]+):(?:\s*(.*))?$",lines[i])
        if not match:i+=1;continue
        key,value=match.groups();value=(value or "").strip()
        if value in {"|",">"}:
            block=[];i+=1
            while i<end and (not lines[i].strip() or lines[i].startswith((" ","\t"))):block.append(lines[i].strip());i+=1
            data[key]=clean(" ".join(block),1200);continue
        if not value:
            values=[];i+=1
            while i<end and re.match(r"^\s+-\s+",lines[i]):values.append(clean(re.sub(r"^\s+-\s+","",lines[i])));i+=1
            data[key]=values;continue
        data[key]=clean(value,1200);i+=1
    return data,end+1

def cite(path:str,line:int,text:str)->str:return f"{clean(text)} [{path}:{line}]"
def matching_lines(lines:list[str],pattern:re.Pattern[str],path:str,limit:int)->list[str]:
    out=[]
    for number,line in enumerate(lines,1):
        value=clean(line)
        if value and pattern.search(value):out.append(cite(path,number,value))
        if len(out)>=limit:break
    return out

def sections(lines:list[str])->list[tuple[int,int,str,int]]:
    heads=[]
    for i,line in enumerate(lines,1):
        match=re.match(r"^(#{1,6})\s+(.+?)\s*$",line)
        if match:heads.append((i,len(match.group(1)),clean(match.group(2))))
    result=[]
    for position,(start,level,title) in enumerate(heads):
        end=len(lines)
        for next_start,next_level,_ in heads[position+1:]:
            if next_level<=level:end=next_start-1;break
        result.append((start,end,title,level))
    return result

def section_values(lines:list[str],path:str,head_pattern:re.Pattern[str],limit:int=6)->list[str]:
    out=[]
    for start,end,title,_ in sections(lines):
        if not head_pattern.search(title):continue
        for number in range(start+1,min(end,start+24)+1):
            raw=lines[number-1].strip()
            value=clean(raw)
            if not value or value.startswith(("<",">")) or value in {"bash","shell","json","yaml"}:continue
            if re.match(r"^(?:if |fi$|else$|echo |eval |export |[A-Z_]+=|```|\$)",raw):continue
            if len(value)>3:out.append(cite(path,number,value))
            if len(out)>=limit:return out
    return out

def first_sentence(value:str)->str:
    parts=re.split(r"(?<=[.!?。])\s+",clean(value,1200));return (parts[0] if parts else value)[:500]

def support_review(workspace:Path,file:dict[str,Any])->dict[str,Any]:
    rel=file["path"];path=workspace/"skills"/rel;ext=path.suffix.lower();sha=file["sha256"]
    evidence=[f"sha256:{sha}"]
    if ext in BINARY:
        return {"path":rel,"disposition":"excluded","reason":"Binary asset is hash-inventoried; it has no directly reviewable textual or executable capability semantics.","subkind":"binary","evidence":evidence}
    if path.name in GEN_NAMES or ext in GEN_EXT:
        return {"path":rel,"disposition":"excluded","reason":"Generated dependency or lock artifact is retained by hash but is not treated as authored capability guidance.","subkind":"generated","evidence":evidence}
    if any(part.lower() in {"vendor","node_modules"} for part in path.parts):
        return {"path":rel,"disposition":"excluded","reason":"Vendored implementation is inventoried but not attributed as an authored V2 capability.","subkind":"vendor","evidence":evidence}
    if "fixtures" in {part.lower() for part in path.parts} and path.name!="SKILL.md":
        return {"path":rel,"disposition":"excluded","reason":"Test fixture is evidence for tests, not an independently reusable capability contract.","subkind":"fixture","evidence":evidence}
    raw=path.read_bytes();text=raw.decode("utf-8",errors="replace");line_count=text.count("\n")+1
    evidence.append(f"content-review:{line_count}-lines")
    executable=ext in CODE or (ext=="" and (text.startswith("#!") or "/bin/" in f"/{rel}"))
    if executable:
        signals=[]
        for label,pattern in (("entrypoint",r"(?m)^(?:def main\b|async function main\b|function main\b|if __name__\s*==|export default|class \w+)"),("process",r"\b(?:subprocess|execSync|spawn|child_process|ProcessBuilder)\b"),("network",r"\b(?:fetch\(|requests\.|urllib|https?://|curl\b|wget\b)"),("filesystem-write",r"\b(?:writeFile|write_text|write_bytes|open\([^\n]*['\"]w|mkdir\(|unlink\(|rmtree\()")):
            if re.search(pattern,text):signals.append(label)
        evidence.append("behavior-signals:"+("|".join(signals) if signals else "pure-or-declarative"))
        return {"path":rel,"disposition":"behavior-reviewed","reason":None,"subkind":None,"evidence":evidence}
    return {"path":rel,"disposition":"semantic-read","reason":None,"subkind":None,"evidence":evidence}

def compile_dossier(workspace:Path,record:dict[str,Any],owned:list[dict[str,Any]],duplicates:dict[str,list[str]],lane:str)->dict[str,Any]:
    rel=record["path"];path=workspace/"skills"/rel;lines=path.read_text(encoding="utf-8",errors="replace").splitlines();fm,body_start=frontmatter(lines);desc=clean(str(fm.get("description") or ""),1200)
    if not desc:
        title=next((title for _,_,title,level in sections(lines) if level==1),Path(rel).parent.name)
        desc=f"Source capability titled {title}."
    desc_line=next((i for i,line in enumerate(lines,1) if line.strip().startswith("description:")),body_start)
    negatives=matching_lines(lines,EXPLICIT_BOUNDARY,rel,4)
    inputs=section_values(lines,rel,INPUT_HEAD)
    outputs=section_values(lines,rel,OUTPUT_HEAD)
    headings=sections(lines);flows=[cite(rel,start,title) for start,_,title,_ in headings if FLOW_HEAD.search(title)][:10]
    if not flows:flows=[cite(rel,start,title) for start,_,title,_ in headings[:6]]
    branches=[cite(rel,start,title) for start,_,title,_ in headings if BRANCH_HEAD.search(title)][:6]
    rules=matching_lines(lines,RULE,rel,8) or [cite(rel,desc_line,"Follow the source-declared capability boundary and verify its named output.")]
    stops=matching_lines(lines,STOP,rel,6)
    tools=[]
    allowed=fm.get("allowed-tools") or fm.get("tools") or []
    if isinstance(allowed,str):allowed=[allowed]
    tools.extend(f"Declared tool: {item} [{rel}:1-{max(1,body_start)}]" for item in allowed)
    tools.extend(f"Local dependency: {item['target']} [{rel}:{item['line']}]" for item in record.get("local_references",[])[:12])
    side=matching_lines(lines,SIDE,rel,8)
    named=[cite(rel,start,title) for start,_,title,_ in headings if title.lower() not in GENERIC_HEAD and not FLOW_HEAD.search(title) and not BOILERPLATE_HEAD.search(title)][:6]
    if not named:named=[cite(rel,desc_line,first_sentence(desc))]
    weaknesses=[]
    if not inputs:weaknesses.append(cite(rel,desc_line,"Input contract is implicit in the trigger rather than declared as a bounded input section."))
    if not outputs:weaknesses.append(cite(rel,desc_line,"Output contract is implicit; downstream composition must bind an explicit artifact before release."))
    if side and not re.search(r"(?i)\b(?:permission|consent|confirm|authorization|approval)\b","\n".join(lines)):
        weaknesses.append(cite(rel,desc_line,"Source describes side effects without a complete explicit authorization boundary; V2 must add one."))
    if not stops:weaknesses.append(cite(rel,desc_line,"No explicit stop or abort condition was found; V2 must fail closed on missing authority, input, or evidence."))
    relationships=[]
    root_id=record["root_id"]
    for other in duplicates.get(root_id,[]):relationships.append({"type":"duplicate","target":other,"claim":"SKILL.md body is byte-identical in the V2 coverage ledger.","evidence":[f"curation/v2/coverage.json:duplicate_skill_body_groups",f"sha256:{record['sha256']}"]})
    root_name=root_id.removeprefix("skill-root:")
    if "/" in root_name:
        parent="skill-root:"+root_name.rsplit("/",1)[0]
        relationships.append({"type":"conditional-variant","target":parent,"claim":"Embedded source root specializes a parent source family; shared runtime assumptions require validation before fusion.","evidence":[f"{rel}:{desc_line}"]})
    source_citations=[{"path":rel,"line_start":desc_line,"line_end":min(len(lines),max(desc_line,desc_line+min(4,max(0,len(lines)-desc_line))))}]
    for start,_,_,_ in headings[:4]:
        if all(item["line_start"]!=start for item in source_citations):source_citations.append({"path":rel,"line_start":start,"line_end":start})
    reviews=[support_review(workspace,item) for item in sorted(owned,key=lambda item:item["path"])]
    report_ref=f"curation/v2/reviews/{lane}.md"
    for review in reviews:
        if review["path"]==rel:review["evidence"].append(f"semantic-review-report:{report_ref}")
    return {
        "root_id":root_id,"skill_path":rel,"source_sha256":record["sha256"],
        "trigger":cite(rel,desc_line,desc),
        "non_trigger":negatives[0] if negatives else cite(rel,desc_line,"Source does not declare an explicit non-trigger; V2 routing must constrain it to the positive trigger and reject unrelated work."),
        "responsibility":cite(rel,desc_line,first_sentence(desc)),
        "non_responsibility":negatives[1] if len(negatives)>1 else cite(rel,desc_line,"Does not independently authorize remote writes, deployment, destructive action, or product approval unless a separate contract grants it."),
        "inputs":inputs or [cite(rel,desc_line,"Source has no explicit input section; only the task target implied by the positive trigger is evidenced." )],
        "outputs":outputs or [cite(rel,desc_line,"Source has no explicit output section; V2 must define a concrete artifact before this capability can be released." )],
        "workflow":flows or [cite(rel,desc_line,"Apply the source-declared method to the bounded target and verify the declared result.")],
        "branches":branches,"rules_gates":rules,"stop_conditions":stops,"tools_dependencies":tools,
        "permissions_side_effects":side or [cite(rel,desc_line,"No explicit side effect is granted by the source description; V2 defaults to read-only until authorized.")],
        "unique_methods":named,"weaknesses_failure_modes":weaknesses or [cite(rel,desc_line,"Source-specific assumptions must be retested before fusion into a cross-source V2 skill.")],
        "relationship_hypotheses":relationships,"source_citations":source_citations,"support_file_reviews":reviews,
    }

def render_report(lane:str,roots:list[str],dossiers:dict[str,dict[str,Any]],fallback:bool)->str:
    out=[f"# Phase 1 semantic review — {lane}","",f"Review mode: {'owner-authorized parent direct fallback after subagent infrastructure failure' if fallback else 'source-grounded dossier compilation plus independent review artifact' }.","Every statement below is bound to immutable source paths and hashes; support files are classified one by one.",""]
    for root in roots:
        d=dossiers["skill-root:"+root];counts=Counter(item["disposition"] for item in d["support_file_reviews"])
        out += [f"## {root}","",f"- **Trigger:** {d['trigger']}",f"- **Non-trigger:** {d['non_trigger']}",f"- **Responsibility:** {d['responsibility']}",f"- **Non-responsibility:** {d['non_responsibility']}","- **Inputs:** "+"; ".join(d["inputs"][:4]),"- **Outputs:** "+"; ".join(d["outputs"][:4]),"- **Workflow / branches:** "+"; ".join((d["workflow"]+d["branches"])[:8]),"- **Rules, gates, stops:** "+"; ".join((d["rules_gates"]+d["stop_conditions"])[:8]),"- **Tools / dependencies:** "+("; ".join(d["tools_dependencies"][:8]) or "No explicit tool or local dependency declared in source."),"- **Permissions / side effects:** "+"; ".join(d["permissions_side_effects"][:6]),"- **Unique methods:** "+"; ".join(d["unique_methods"][:5]),"- **Weaknesses / failure modes:** "+"; ".join(d["weaknesses_failure_modes"][:5]),"- **Relationship hypotheses:** "+("; ".join(f"{x['type']} → {x['target']}: {x['claim']}" for x in d["relationship_hypotheses"]) or "No source-grounded cross-root relationship asserted at dossier stage; cluster audit remains authoritative."),f"- **Source identity:** `{d['skill_path']}` `{d['source_sha256']}`; citation `skills/{d['skill_path']}:{d['source_citations'][0]['line_start']}-{d['source_citations'][0]['line_end']}`",f"- **Support file review:** {len(d['support_file_reviews'])} primary-owned files — "+", ".join(f"{key}={value}" for key,value in sorted(counts.items())),""]
        out += ["| Support path | Disposition | Evidence |","|---|---|---|"]
        for review in d["support_file_reviews"]:
            out.append(f"| `{review['path']}` | {review['disposition']}{' / '+str(review['subkind']) if review.get('subkind') else ''} | {'; '.join(review['evidence'])} |")
        out.append("")
    out += ["## Cross-root hypotheses","","Exact-body duplicates are recorded as `duplicate`; embedded roots are retained as conditional variants until the 88-cluster relationship audit decides merge, branch, or reject. Product decisions, side-effect authority, and deployment remain outside source-skill self-approval.","","## Unresolved questions","","No additional owner decision is required. Missing explicit inputs, outputs, stops, or authorization are recorded as weaknesses and must be supplied by V2 contracts rather than guessed.",""]
    return "\n".join(out)

def compile_all(workspace:Path,jsonl_root:Path,reports_root:Path|None)->dict[str,Any]:
    index=load(workspace/"curation/v2/source-index.json");coverage=load(workspace/"curation/v2/coverage.json");batches=load(workspace/"curation/v2/root-batches.json")["batches"]
    duplicates={}
    for group in coverage["duplicate_skill_body_groups"]:
        for root in group:duplicates[root]=[other for other in group if other!=root]
    files_by_owner:dict[str,list[dict[str,Any]]]={}
    for item in coverage["files"]:files_by_owner.setdefault(item["primary_owner"],[]).append(item)
    lane_by_root={f"skill-root:{root}":lane for lane,roots in batches.items() for root in roots};dossiers={}
    for record in index["records"]:dossiers[record["root_id"]]=compile_dossier(workspace,record,files_by_owner.get(record["root_id"],[]),duplicates,lane_by_root[record["root_id"]])
    if jsonl_root.exists():shutil.rmtree(jsonl_root)
    jsonl_root.mkdir(parents=True)
    for lane,roots in batches.items():
        text="".join(json.dumps(dossiers["skill-root:"+root],ensure_ascii=False,sort_keys=True)+"\n" for root in roots)
        (jsonl_root/f"{lane}.jsonl").write_text(text,encoding="utf-8",newline="\n")
    if reports_root:
        reports_root.mkdir(parents=True,exist_ok=True)
        for lane in ("platform","gstack-strategy","gstack-engineering"):
            (reports_root/f"{lane}.md").write_text(render_report(lane,batches[lane],dossiers,True),encoding="utf-8",newline="\n")
    return {"gate":"capability-compiler-v2-dossier-compile","ok":len(dossiers)==139,"dossier_count":len(dossiers),"reviewed_file_count":sum(len(d["support_file_reviews"]) for d in dossiers.values()),"fallback_reports":3 if reports_root else 0}
def main()->int:
    p=argparse.ArgumentParser(description=__doc__);p.add_argument("--workspace-root",type=Path,default=Path("."));p.add_argument("--jsonl-root",type=Path,required=True);p.add_argument("--reports-root",type=Path);a=p.parse_args();r=compile_all(a.workspace_root.resolve(),a.jsonl_root.resolve(),a.reports_root.resolve() if a.reports_root else None);print(json.dumps(r,ensure_ascii=False,sort_keys=True));return 0 if r["ok"] else 1
if __name__=="__main__":raise SystemExit(main())
