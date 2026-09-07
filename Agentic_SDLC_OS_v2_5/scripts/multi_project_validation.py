#!/usr/bin/env python3
from __future__ import annotations

import json
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SCENARIOS = ROOT / "validation" / "multi_project" / "scenarios.json"
RUNS = ROOT / "validation" / "multi_project" / "runs"
RESULT_JSON = ROOT / "validation" / "multi_project" / "latest.json"
REPORT_MD = ROOT / "validation" / "multi_project" / "REPORT.md"
BOOTSTRAP = ROOT / "scripts" / "bootstrap_project.py"
SDLC = ROOT / "skills" / "agentic-sdlc-os" / "scripts" / "sdlc.py"


def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def run(command: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(command, cwd=ROOT, text=True, capture_output=True, check=False)


def validate_scenario(scenario: dict[str, Any]) -> dict[str, Any]:
    project = RUNS / scenario["id"]
    if project.exists():
        shutil.rmtree(project)
    database_path = project.parent / f"{scenario['id']}.db"
    for suffix in ("", "-wal", "-shm", "-journal"):
        Path(str(database_path) + suffix).unlink(missing_ok=True)
    db_url = f"sqlite+pysqlite:///{database_path}"
    command = [
        sys.executable, str(BOOTSTRAP), str(project), "--name", scenario["name"],
        "--type", scenario["project_type"], "--domain-pack", scenario["domain_pack"],
        "--budget-usd", "25", "--token-budget", "500000", "--database-url", db_url,
    ]
    for name, value in scenario["factors"].items():
        command.extend(["--" + name.replace("_", "-"), str(value)])
    bootstrap = run(command)
    checks: dict[str, bool] = {"bootstrap": bootstrap.returncode == 0}
    if bootstrap.returncode != 0:
        return {"id": scenario["id"], "passed": False, "checks": checks, "error": bootstrap.stderr or bootstrap.stdout}
    bootstrap_payload = json.loads(bootstrap.stdout)
    checks["profile"] = bootstrap_payload["profile"] == scenario["expected_profile"]
    checks["domain_pack"] = scenario["domain_pack"] in bootstrap_payload["domain_packs"]
    route = run([sys.executable, str(SDLC), "route", str(project), scenario["task"], "--json"])
    route_payload = json.loads(route.stdout) if route.returncode == 0 else {}
    checks["route"] = route.returncode == 0 and route_payload.get("decision") == "route" and route_payload.get("recommended_os") == scenario["expected_os"]
    validate = run([sys.executable, str(SDLC), "validate", str(project), "--json"])
    checks["local_state"] = validate.returncode == 0
    config = json.loads((project / ".sdlc" / "config.json").read_text(encoding="utf-8"))
    pack = json.loads((ROOT / "domain-packs" / scenario["domain_pack"] / "pack.json").read_text(encoding="utf-8"))
    checks["domain_controls"] = set(pack["required_controls"]).issubset(config.get("domain_required_controls", []))
    checks["budget"] = config.get("cost_budget_usd") == 25 and config.get("token_budget") == 500000

    sys.path.insert(0, str(ROOT / "control_plane"))
    from agentic_sdlc_cp.costs import BudgetService
    from agentic_sdlc_cp.db import create_database, init_database
    from agentic_sdlc_cp.jobs import JobQueue
    from agentic_sdlc_cp.repository import ProjectRepository

    database = create_database(db_url)
    try:
        init_database(database)
        project_id = bootstrap_payload["control_plane_project_id"]
        queue = JobQueue(); budgets = BudgetService(); repo = ProjectRepository()
        with database.session() as session:
            budgets.upsert(session, project_id=project_id, soft_limit_usd=20, hard_limit_usd=25, token_limit=500000)
            decision = budgets.assess(session, project_id=project_id, estimated_cost_usd=5, estimated_tokens=5000)
            job = queue.enqueue(session, project_id=project_id, job_type="echo", payload={"scenario": scenario["id"]}, idempotency_key=f"{scenario['id']}-echo")
        with database.session() as session:
            lease = queue.lease_next(session, worker_id="validation-worker", lease_seconds=60, job_types=["echo"])
            if lease:
                queue.complete(session, job_id=lease.id, worker_id="validation-worker", fencing_token=lease.fencing_token, result={"ok": True})
        with database.session() as session:
            audit = repo.verify_audit_chain(session, project_id)
        checks["control_plane_budget"] = decision.allowed and decision.level in {"normal", "watch", "degraded"}
        checks["concurrent_job_queue"] = lease is not None and lease.id == job.id
        checks["audit_chain"] = audit["valid"]
    finally:
        database.engine.dispose()
    return {
        "id": scenario["id"], "name": scenario["name"], "passed": all(checks.values()),
        "profile": bootstrap_payload["profile"], "expected_profile": scenario["expected_profile"],
        "route": route_payload, "checks": checks,
    }


def markdown(payload: dict[str, Any]) -> str:
    lines = [
        "# Multi-project executable validation", "",
        f"Generated: `{payload['generated_at']}`", f"Decision: **{'PASS' if payload['passed'] else 'FAIL'}**", "",
        "This suite validates cross-archetype control behavior. It is not a substitute for longitudinal production use.", "",
        "| Scenario | Profile | Route | Result |", "|---|---|---|---|",
    ]
    for item in payload["scenarios"]:
        route = item.get("route", {}).get("recommended_os") or item.get("route", {}).get("decision", "-")
        lines.append(f"| {item.get('name', item['id'])} | {item.get('profile', '-')} | {route} | {'PASS' if item['passed'] else 'FAIL'} |")
    lines += ["", "## Boundaries", "", "- Uses executable local kernels, SQLite control-plane storage and deterministic scenario checks.", "- PostgreSQL-specific integration is defined separately and requires a live PostgreSQL service.", "- Does not prove business impact or 30-day operational reliability."]
    return "\n".join(lines) + "\n"


def main() -> int:
    RUNS.mkdir(parents=True, exist_ok=True)
    scenarios = json.loads(SCENARIOS.read_text(encoding="utf-8"))
    results = [validate_scenario(item) for item in scenarios]
    payload = {"generated_at": now(), "passed": all(item["passed"] for item in results), "scenarios": results}
    RESULT_JSON.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    REPORT_MD.write_text(markdown(payload), encoding="utf-8")
    print(json.dumps(payload, indent=2))
    return 0 if payload["passed"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
