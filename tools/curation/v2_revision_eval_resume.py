#!/usr/bin/env python3
"""Resume R5 exec/judge with a quota probe. Failed runs are moved (never deleted) to infra-failed/<stage>-attempt-N, then retried unchanged."""
import json, shutil, subprocess, sys, time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import v2_skill_audit_phase_d as pd  # noqa: E402

ROUND = "round-2"
R = Path("evals/runs/capability-compiler-v2/revision-1.1.0-eval") / ROUND
EVAL = [sys.executable, "tools/curation/v2_revision_eval.py"]
LOG = R.parent / "logs/resume.log"
MAX_CYCLES, PROBE_SLEEP = 24, 300


def log(msg):
    LOG.parent.mkdir(parents=True, exist_ok=True)
    with LOG.open("a", encoding="utf-8") as f:
        f.write(f"[{time.strftime('%FT%TZ', time.gmtime())}] {msg}\n")


def probe(exe):
    d = (R / "probe").resolve() / time.strftime("quota-resume-%H%M%S")
    return pd.call(d, pd.EXEC_MODEL, "low", "Reply with the single word: ready.", exe, 180)["exit_status"] == "completed"


def run(stage, extra):
    out = subprocess.run([*EVAL, stage, "--round", ROUND, "--skills", "all", *extra], capture_output=True, text=True, encoding="utf-8")
    log(f"{stage} rc={out.returncode} {out.stdout.strip()[:300]} {out.stderr.strip()[-200:]}")


def quarantine(root, tag):
    bad = [d for d in root.rglob("*") if d.is_dir() and ((d / "run.json").is_file() and json.loads((d / "run.json").read_text(encoding="utf-8"))["exit_status"] != "completed" or (d / "prompt.md").is_file() and not (d / "run.json").is_file())]
    dest = R / "infra-failed" / tag
    for d in bad:
        dest.mkdir(parents=True, exist_ok=True)
        shutil.move(str(d), str(dest / "__".join(d.relative_to(root).parts)))
    return len(bad)


def complete(root):
    return not any(True for _ in root.rglob("prompt.md") if not (_.parent / "run.json").is_file())


exe = shutil.which("pi.cmd") or shutil.which("pi")
for cycle in range(1, MAX_CYCLES + 1):
    if not probe(exe):
        log(f"cycle {cycle}: quota still exhausted; sleeping {PROBE_SLEEP}s")
        time.sleep(PROBE_SLEEP)
        continue
    log(f"cycle {cycle}: quota ok, exec")
    run("exec", ["--concurrency", "3", "--timeout", "900"])
    n = quarantine(R / "exec", f"exec-resume-cycle-{cycle}")
    log(f"cycle {cycle}: quarantined {n} failed exec runs")
    if n == 0:
        break
else:
    log("gave up: exec not complete within cycle budget"); sys.exit(2)
for cycle in range(1, 6):
    run("judge", ["--concurrency", "6", "--timeout", "900"])
    n = quarantine(R / "judge", f"judge-resume-cycle-{cycle}")
    log(f"judge cycle {cycle}: quarantined {n}")
    if n == 0:
        break
run("report", [])
log("DONE")
