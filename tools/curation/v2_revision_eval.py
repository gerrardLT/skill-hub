#!/usr/bin/env python3
"""R5: head-to-head evaluation of the 1.1.0 candidate against frozen 1.0.0 (and a no-Skill baseline).

Stages: gen (fresh tasks) -> freeze -> exec -> judge -> report. Model calls reuse the Phase D isolation
(fresh `pi -p --mode json`, no tools, empty cwd, env allowlist). Thresholds live in .specs/.../r5-design.md.
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
from collections import Counter
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).parent))
import v2_skill_audit_phase_d as pd  # noqa: E402

OUT_BASE = Path("evals/runs/capability-compiler-v2/revision-1.1.0-eval")
OUT = OUT_BASE / "round-2"  # main() overrides via --round; one directory per round so call() never reuses a stale run.json
PD = pd.OUT
CAND = Path("evals/candidates/capability-compiler-v2/revision-1.1.0")
REV = Path("curation/v2/revision-1.1.0")
DESIGN = Path(".specs/capability-compiler-v2/revision-1.1.0/r5-design.md")
PILOT = ["completion-evidence-gate", "test-case-design-and-export", "customer-interview-execution", "opportunity-prioritization-and-frameworks", "ai-model-and-data-architecture", "cross-domain-ui-preflight-checklists"]
VARIANTS = {"old": ["v110"], "fresh": ["baseline", "v100", "v110"]}
PAIRS = {"old": [("v110", "v100")], "fresh": [("v110", "v100"), ("v110", "baseline")]}
ORDERS = ("xy", "yx")
GEN_FRESH = pd.GEN_PROMPT.replace("CAPABILITY CONTRACT:", "EXISTING TASKS FOR THIS CAPABILITY (use a different industry, artifact type and scenario from each):\n{avoid}\n\nCAPABILITY CONTRACT:")


def merges(ws: Path) -> dict[str, str]:
    return pd.load(ws / REV / "structure.json")["merges"]


def select(ws: Path, selection: str, which: str) -> list[str]:
    old = list(pd.load(ws / PD / "task-set.json")["skills"])
    fresh = [s["id"] for s in pd.load(ws / "slots/v2/catalog.json")["skills"] if s["id"] not in merges(ws)]
    base = old if which == "old" else fresh
    chosen = PILOT if selection == "pilot" else base if selection == "all" else [s.strip() for s in selection.split(",") if s.strip()]
    unknown = sorted(set(chosen) - set(old) - set(fresh))
    if unknown:
        raise ValueError(f"unknown skills: {unknown}")
    return [s for s in chosen if s in base]


def tasks_of(ws: Path, which: str) -> dict[str, Any]:
    return pd.load(ws / (PD / "task-set.json" if which == "old" else OUT / "fresh/task-set.json"))["skills"]


def skill_text(ws: Path, sid: str, variant: str) -> str:
    if variant == "baseline":
        return ""
    path = ws / (f"slots/v2/1.0.0/skills/{sid}/SKILL.md" if variant == "v100" else CAND / f"skills/{merges(ws).get(sid, sid)}/SKILL.md")
    return path.read_text(encoding="utf-8")


def run_dir(ws: Path, which: str, sid: str, tid: str, variant: str) -> Path:
    if which == "old" and variant in ("baseline", "v100"):  # reuse Phase D outputs
        return ws / PD / "exec" / f"{sid}__{tid}__{'candidate' if variant == 'v100' else 'baseline'}"
    return ws / OUT / "exec" / which / f"{sid}__{tid}__{variant}"


def generate(ws: Path, skills: list[str], exe: str, conc: int, timeout: int) -> dict[str, Any]:
    old = pd.load(ws / PD / "task-set.json")["skills"]

    def one(sid: str) -> dict[str, Any]:
        cap = pd.load(ws / f"curation/v2/capabilities/{sid}.json")
        rule = pd.WRITE_RULE_REMOTE if cap["permission_identity"] in pd.WRITE_IDENTITIES else pd.WRITE_RULE_DEFAULT
        seen = list(old.get(sid, {}).get("tasks", []))
        for prior in sorted((ws / OUT_BASE).glob("round-*/fresh/task-set.json")):
            if prior.parent.parent != ws / OUT:
                seen += pd.load(prior)["skills"].get(sid, {}).get("tasks", [])
        avoid = "\n".join("- " + " ".join(t["prompt"].split()[:30]) + " ..." for t in seen) or "- (none)"
        prompt = GEN_FRESH.format(write_rule=rule, avoid=avoid, contract=json.dumps({f: cap[f] for f in pd.CONTRACT_FIELDS}, ensure_ascii=False, indent=2))
        run = pd.call(ws / OUT / "fresh/gen" / sid, pd.JUDGE_MODEL, "medium", prompt, exe, timeout)
        return {"skill": sid, "status": run["exit_status"], "failure": run.get("failure_reason")}

    res = pd.pool_map(one, skills, conc)
    return {"stage": "gen", "count": len(res), "statuses": dict(Counter(r["status"] for r in res)), "failures": [r for r in res if r["status"] != "completed"]}


def shingles(text: str, size: int = 6) -> set[str]:
    words = re.findall(r"[a-z0-9][a-z0-9'-]*", text.lower())
    return {" ".join(words[i:i + size]) for i in range(len(words) - size + 1)}


def freeze(ws: Path, skills: list[str]) -> dict[str, Any]:
    path = ws / OUT / "fresh/task-set.json"
    frozen = pd.load(path)["skills"] if path.is_file() else {}
    problems = []
    for sid in skills:
        run = pd.load(ws / OUT / "fresh/gen" / sid / "run.json")
        value, notes = pd.parse_json(run.get("output", ""))
        tasks = value.get("tasks") if isinstance(value, dict) else None
        errors = [n for n in notes if n.startswith("invalid")]
        if not isinstance(tasks, list) or [t.get("id") for t in tasks] != ["T1", "T2"]:
            errors.append("tasks-shape")
        else:
            for t in tasks:
                words, rub = len(str(t.get("prompt", "")).split()), t.get("rubric")
                if not 60 <= words <= 320:
                    errors.append(f"{t['id']}-length-{words}")
                if not isinstance(rub, list) or not 3 <= len(rub) <= 6 or not all(isinstance(i, str) and i.strip() for i in rub):
                    errors.append(f"{t['id']}-rubric")
        if errors:
            problems.append({"skill": sid, "errors": errors})
            continue
        cap = pd.load(ws / f"curation/v2/capabilities/{sid}.json")
        contract = shingles(json.dumps({f: cap[f] for f in pd.CONTRACT_FIELDS}, ensure_ascii=False))
        private = (shingles(skill_text(ws, sid, "v100")) | shingles(skill_text(ws, sid, "v110"))) - contract
        text = " ".join(re.findall(r"[a-z0-9][a-z0-9'-]*", " ".join([x for t in tasks for x in [t["prompt"], *t["rubric"]]]).lower()))
        frozen[sid] = {"generation_run_sha256": pd.sha(json.dumps(run, sort_keys=True)), "leak_shingles": sorted(s for s in private if s in text), "tasks": tasks}
    doc = {"schema_version": "2.0", "generator_model": pd.JUDGE_MODEL, "design_sha256": pd.sha((ws / DESIGN).read_text(encoding="utf-8")), "skills": dict(sorted(frozen.items()))}
    doc["task_set_sha256"] = pd.sha(json.dumps(doc["skills"], ensure_ascii=False, sort_keys=True))
    pd.write(path, doc)
    return {"stage": "freeze", "frozen": len(frozen), "problems": problems, "leak_flags": {k: len(v["leak_shingles"]) for k, v in frozen.items() if v["leak_shingles"]}, "task_set_sha256": doc["task_set_sha256"]}


def execute(ws: Path, which: str, skills: list[str], exe: str, conc: int, timeout: int) -> dict[str, Any]:
    tasks, jobs = tasks_of(ws, which), []
    for sid in skills:
        if sid not in tasks:  # generation failed; reported as not-generated
            continue
        for t in tasks[sid]["tasks"]:
            for v in VARIANTS[which]:
                method = pd.METHOD_BLOCK.format(skill=skill_text(ws, sid, v)) if v != "baseline" else ""
                jobs.append((sid, t["id"], v, pd.EXEC_PROMPT.format(method=method, task=t["prompt"])))

    def one(job):
        sid, tid, v, prompt = job
        return pd.call(run_dir(ws, which, sid, tid, v), pd.EXEC_MODEL, "low", prompt, exe, timeout)["exit_status"]

    return {"stage": "exec", "set": which, "calls": len(jobs), "statuses": dict(Counter(pd.pool_map(one, jobs, conc)))}


def judge(ws: Path, which: str, skills: list[str], exe: str, conc: int, timeout: int) -> dict[str, Any]:
    tasks, jobs = tasks_of(ws, which), []
    for sid in skills:
        if sid not in tasks:
            continue
        for t in tasks[sid]["tasks"]:
            for x, y in PAIRS[which]:
                if not all((run_dir(ws, which, sid, t["id"], v) / "run.json").is_file() for v in (x, y)):
                    continue
                runs = {v: pd.load(run_dir(ws, which, sid, t["id"], v) / "run.json") for v in (x, y)}
                if any(r["exit_status"] != "completed" for r in runs.values()):
                    continue
                for order in ORDERS:
                    a, b = (x, y) if order == "xy" else (y, x)
                    prompt = pd.JUDGE_PROMPT.format(task=t["prompt"], rubric="\n".join(f"- {i}" for i in t["rubric"]), a=runs[a]["output"], b=runs[b]["output"])
                    jobs.append((f"{x}_{y}", sid, t["id"], order, prompt))

    def one(job):
        pair, sid, tid, order, prompt = job
        return pd.call(ws / OUT / "judge" / which / pair / f"{sid}__{tid}__{order}", pd.JUDGE_MODEL, "medium", prompt, exe, timeout)["exit_status"]

    return {"stage": "judge", "set": which, "calls": len(jobs), "statuses": dict(Counter(pd.pool_map(one, jobs, conc)))}


def outcomes(ws: Path, which: str, pair: tuple[str, str], sid: str) -> list[dict[str, Any]]:
    x, y, result = pair[0], pair[1], []
    for t in tasks_of(ws, which)[sid]["tasks"]:
        per = {}
        for order in ORDERS:
            p = ws / OUT / "judge" / which / f"{x}_{y}" / f"{sid}__{t['id']}__{order}" / "run.json"
            if not p.is_file():
                continue
            run = pd.load(p)
            value, _ = pd.parse_json(run.get("output", ""))
            if run["exit_status"] != "completed" or not isinstance(value, dict) or value.get("overall") not in {"A", "B", "tie"}:
                continue
            mine = "A" if order == "xy" else "B"
            other = "B" if mine == "A" else "A"
            per[order] = {"outcome": "tie" if value["overall"] == "tie" else "win" if value["overall"] == mine else "loss",
                          "x_over": bool(value.get("overreach", {}).get(mine)), "y_over": bool(value.get("overreach", {}).get(other)),
                          "x_fab": bool(value.get("fabrication", {}).get(mine)), "y_fab": bool(value.get("fabrication", {}).get(other)), "reason": value.get("reason")}
        if len(per) < 2:
            result.append({"task": t["id"], "outcome": "incomplete", "orders": per})
            continue
        a, b = per["xy"], per["yx"]
        both = lambda k: a[k] and b[k]
        result.append({"task": t["id"], "outcome": a["outcome"] if a["outcome"] == b["outcome"] else "tie", "orders_agree": a["outcome"] == b["outcome"],
                       "new_overreach": both("x_over") and not both("y_over"), "new_fabrication": both("x_fab") and not both("y_fab"), "orders": per})
    return result


def report(ws: Path, which_sets: list[str], skills_sel: str) -> dict[str, Any]:
    summary: dict[str, Any] = {"schema_version": "2.0", "exec_model": pd.EXEC_MODEL, "judge_model": pd.JUDGE_MODEL, "design_sha256": pd.sha((ws / DESIGN).read_text(encoding="utf-8")), "sets": {}}
    losses: dict[str, set[str]] = {}
    for which in which_sets:
        skills = select(ws, skills_sel, which)
        for pair in PAIRS[which]:
            key, per = f"{which}:{pair[0]}_vs_{pair[1]}", {}
            for sid in skills:
                if sid not in tasks_of(ws, which):
                    per[sid] = {"wins": 0, "losses": 0, "verdict": "not-generated", "outcomes": []}
                    continue
                outs = outcomes(ws, which, pair, sid)
                w, l = sum(o["outcome"] == "win" for o in outs), sum(o["outcome"] == "loss" for o in outs)
                per[sid] = {"wins": w, "losses": l, "verdict": "incomplete" if any(o["outcome"] == "incomplete" for o in outs) else "mixed" if w and l else "regressed" if l else "improved" if w else "unchanged", "outcomes": outs}
                if pair == ("v110", "v100") and l:
                    losses.setdefault(sid, set()).add(which)
            flat = [o for v in per.values() for o in v["outcomes"]]
            summary["sets"][key] = {"skills": len(per), "task_outcomes": dict(Counter(o["outcome"] for o in flat)), "verdicts": dict(Counter(v["verdict"] for v in per.values())),
                                    "order_agreement": dict(Counter("agree" if o.get("orders_agree") else "disagree" for o in flat if "orders_agree" in o)),
                                    "new_overreach": sorted(f"{s}:{o['task']}" for s, v in per.items() for o in v["outcomes"] if o.get("new_overreach")),
                                    "new_fabrication": sorted(f"{s}:{o['task']}" for s, v in per.items() for o in v["outcomes"] if o.get("new_fabrication")), "per_skill": per}
    old_loss = pd.load(ws / REV / "phase-d-loss-reasons.json")
    gate = {}
    for which in which_sets:
        s = summary["sets"].get(f"{which}:v110_vs_v100")
        if s:
            gate[f"{which}_wins_at_least_losses"] = s["task_outcomes"].get("win", 0) >= s["task_outcomes"].get("loss", 0)
    gate["skills_lost_in_both_sets"] = sorted(sid for sid, sets in losses.items() if len(sets) == 2)
    gate["new_overreach_or_fabrication"] = sorted({x for k, v in summary["sets"].items() if k.endswith("v110_vs_v100") for x in v["new_overreach"] + v["new_fabrication"]})
    gate["recovery_of_phase_d_negative_or_mixed"] = {sid: summary["sets"].get("old:v110_vs_v100", {}).get("per_skill", {}).get(sid, {}).get("verdict") for sid in old_loss}
    summary["threshold_check"] = gate
    tokens = calls = 0
    for p in (ws / OUT).rglob("run.json"):
        calls += 1
        tokens += int(pd.load(p).get("token_usage", {}).get("totalTokens") or 0)
    summary.update(calls_recorded=calls, total_tokens=tokens, limitations=["Two tasks per Skill per set, one judge model in two orders; win or loss only when both orders agree; old-set v100 outputs come from Phase D (different run time)."])
    pd.write(ws / OUT / "report.json", summary)
    return {"threshold_check": {k: v for k, v in gate.items() if k != "recovery_of_phase_d_negative_or_mixed"}, "sets": {k: {kk: vv for kk, vv in v.items() if kk != "per_skill"} for k, v in summary["sets"].items()}, "calls": calls, "tokens": tokens}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("stage", choices=["gen", "freeze", "exec", "judge", "report"])
    ap.add_argument("--workspace-root", type=Path, default=Path("."))
    ap.add_argument("--set", dest="which", choices=["old", "fresh", "both"], default="both")
    ap.add_argument("--skills", default="pilot", help="pilot | all | comma-separated ids")
    ap.add_argument("--concurrency", type=int, default=6)
    ap.add_argument("--timeout", type=int, default=600)
    ap.add_argument("--round", default="round-2")
    a = ap.parse_args()
    globals()["OUT"] = OUT_BASE / a.round
    ws = a.workspace_root.resolve()
    exe = shutil.which("pi.cmd") or shutil.which("pi") or ""
    sets = ["old", "fresh"] if a.which == "both" else [a.which]
    if a.stage in {"gen", "exec", "judge"} and not exe:
        raise RuntimeError("pi executable unavailable")
    out: list[Any] = []
    if a.stage == "gen":
        out.append(generate(ws, select(ws, a.skills, "fresh"), exe, a.concurrency, a.timeout))
    elif a.stage == "freeze":
        out.append(freeze(ws, select(ws, a.skills, "fresh")))
    elif a.stage == "report":
        out.append(report(ws, sets, a.skills))
    else:
        for which in sets:
            fn = execute if a.stage == "exec" else judge
            out.append(fn(ws, which, select(ws, a.skills, which), exe, a.concurrency, a.timeout))
    print(json.dumps(out, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
