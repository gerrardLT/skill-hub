#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from dataclasses import asdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / "control_plane"))

from tailor_process import FACTOR_NAMES, assess
from apply_domain_pack import apply as apply_pack


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="One-command Agentic SDLC OS project bootstrap")
    parser.add_argument("project")
    parser.add_argument("--name", required=True)
    parser.add_argument("--type", choices=["greenfield", "brownfield", "incident", "migration"], default="greenfield")
    parser.add_argument("--domain-pack", action="append", default=[])
    parser.add_argument("--budget-usd", type=float)
    parser.add_argument("--token-budget", type=int)
    parser.add_argument("--database-url")
    parser.add_argument("--force", action="store_true")
    for name in FACTOR_NAMES:
        parser.add_argument("--" + name.replace("_", "-"), type=int, default=0)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    project = Path(args.project).expanduser().resolve()
    factors = {name: getattr(args, name) for name in FACTOR_NAMES}
    domain_risk = 0.0
    for pack_id in args.domain_pack:
        pack = json.loads((ROOT / "domain-packs" / pack_id / "pack.json").read_text(encoding="utf-8"))
        domain_risk += float(pack.get("risk_adjustment", 0.0))
    decision = assess(factors, domain_risk=domain_risk)
    criticality = "high" if decision.profile == "high-assurance" else "medium" if decision.profile == "standard" else "low"
    repo_cli = ROOT / "skills" / "agentic-sdlc-os" / "scripts" / "sdlc.py"
    cli = repo_cli if repo_cli.exists() else ROOT / "scripts" / "sdlc.py"
    command = [
        sys.executable, str(cli), "init", str(project), "--name", args.name,
        "--type", args.type, "--criticality", criticality, "--profile", decision.profile,
    ]
    if args.force:
        command.append("--force")
    completed = subprocess.run(command, text=True, capture_output=True, check=False)
    if completed.returncode != 0:
        print(completed.stdout, end="")
        print(completed.stderr, end="", file=sys.stderr)
        return completed.returncode
    for pack_id in args.domain_pack:
        apply_pack(project, pack_id)
    config_path = project / ".sdlc" / "config.json"
    config = json.loads(config_path.read_text(encoding="utf-8"))
    config.update({
        "auto_tailoring": asdict(decision) | {"factors": factors},
        "cost_budget_usd": args.budget_usd,
        "token_budget": args.token_budget,
    })
    config_path.write_text(json.dumps(config, indent=2) + "\n", encoding="utf-8")
    bootstrap = {
        "system_version": "2.2.0",
        "project": str(project),
        "profile": decision.profile,
        "criticality": criticality,
        "tailoring": asdict(decision),
        "domain_packs": args.domain_pack,
        "budget_usd": args.budget_usd,
        "token_budget": args.token_budget,
    }
    (project / ".sdlc" / "bootstrap.json").write_text(json.dumps(bootstrap, indent=2) + "\n", encoding="utf-8")
    if args.database_url:
        from agentic_sdlc_cp.db import create_database, init_database
        from agentic_sdlc_cp.repository import ProjectRepository
        database = create_database(args.database_url)
        init_database(database)
        state = json.loads((project / ".sdlc" / "state.json").read_text(encoding="utf-8"))
        with database.session() as session:
            record = ProjectRepository().create_project(
                session,
                name=args.name,
                project_type=args.type,
                criticality=criticality,
                profile=decision.profile,
                actor="bootstrap-cli",
                state=state,
            )
            bootstrap["control_plane_project_id"] = record.id
        (project / ".sdlc" / "bootstrap.json").write_text(json.dumps(bootstrap, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(bootstrap, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
