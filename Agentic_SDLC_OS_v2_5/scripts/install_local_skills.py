#!/usr/bin/env python3
"""Install the seven Agentic SDLC OS skills into an agent-specific directory."""
from __future__ import annotations

import argparse
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional, Sequence

SKILLS = [
    "agentic-sdlc-os",
    "pm-operating-system",
    "design-operating-system",
    "engineering-operating-system",
    "qa-operating-system",
    "release-operating-system",
    "evolution-operating-system",
]
PROJECT_TARGETS = {
    "generic": ".agents/skills",
    "claude": ".claude/skills",
    "cursor": ".cursor/skills",
    "codex": ".codex/skills",
    "copilot": ".github/skills",
    "opencode": ".opencode/skills",
}


def repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def validate_source(path: Path) -> None:
    required = [path / "SKILL.md", path / "agents" / "openai.yaml"]
    missing = [str(x) for x in required if not x.exists()]
    if missing:
        raise RuntimeError("Invalid skill source, missing: " + ", ".join(missing))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Install Agentic SDLC OS local skills")
    parser.add_argument("--agent", choices=sorted(PROJECT_TARGETS), default="generic")
    parser.add_argument("--project", default=".", help="Project root")
    parser.add_argument("--target", help="Explicit skills destination; overrides --agent")
    parser.add_argument("--skill", action="append", choices=SKILLS, help="Install only selected skill; repeatable")
    parser.add_argument("--no-backup", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    return parser


def main(argv: Optional[Sequence[str]] = None) -> int:
    args = build_parser().parse_args(argv)
    root = repo_root()
    project = Path(args.project).expanduser().resolve()
    target = Path(args.target).expanduser().resolve() if args.target else project / PROJECT_TARGETS[args.agent]
    selected = args.skill or SKILLS
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")
    print(f"Source: {root / 'skills'}")
    print(f"Target: {target}")
    for name in selected:
        source = root / "skills" / name
        validate_source(source)
        destination = target / name
        if destination.exists():
            if args.no_backup:
                action = f"replace {destination}"
            else:
                backup = target / ".backups" / stamp / name
                action = f"backup {destination} -> {backup}; install"
        else:
            action = f"install {destination}"
        print(f"- {name}: {action}")
        if args.dry_run:
            continue
        target.mkdir(parents=True, exist_ok=True)
        if destination.exists():
            if args.no_backup:
                shutil.rmtree(destination)
            else:
                backup.parent.mkdir(parents=True, exist_ok=True)
                shutil.move(str(destination), str(backup))
        shutil.copytree(source, destination)
    if not args.dry_run:
        print(f"Installed {len(selected)} skill(s).")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except RuntimeError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        sys.exit(2)
