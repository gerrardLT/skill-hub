#!/usr/bin/env python3
"""Selectively inspect or install third-party skills for Agentic SDLC OS.

Dry-run is the default. Execution requires --execute and explicit acknowledgement.
Evolution observability integrations are opt-in provider adapters.
"""
from __future__ import annotations

import argparse
import json
import shlex
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Sequence

OS_NAMES = ["pm", "design", "engineering", "qa", "release", "evolution"]
PROVIDERS = ["sentry", "datadog", "posthog"]
PROFILE_TIERS = {
    "core": {"core"},
    "recommended": {"core", "recommended"},
    "full": {"core", "recommended", "conditional"},
}


def script_root() -> Path:
    return Path(__file__).resolve().parent


def find_manifest() -> Path:
    candidates = [
        script_root().parent / "references" / "manifests" / "external-skills.json",
        script_root().parents[3] / "manifest" / "external-skills.json" if len(script_root().parents) >= 4 else Path("/__missing__"),
        Path.cwd() / "manifest" / "external-skills.json",
    ]
    for candidate in candidates:
        if candidate.exists():
            return candidate
    raise RuntimeError("Cannot locate external-skills.json")


def load_manifest() -> Dict[str, Any]:
    with find_manifest().open("r", encoding="utf-8") as fh:
        data = json.load(fh)
    if not isinstance(data, dict) or not isinstance(data.get("skills"), list):
        raise RuntimeError("Invalid external skill manifest")
    if data.get("provider_adapters") is not None and not isinstance(data.get("provider_adapters"), list):
        raise RuntimeError("Invalid provider_adapters manifest")
    return data


def gstack_command(agent: str) -> str:
    if agent == "claude":
        return "git clone --single-branch --depth 1 https://github.com/garrytan/gstack.git ~/.claude/skills/gstack && cd ~/.claude/skills/gstack && ./setup"
    host_map = {"codex": "codex", "cursor": "cursor", "opencode": "opencode"}
    host = host_map.get(agent)
    if host:
        return f"git clone --single-branch --depth 1 https://github.com/garrytan/gstack.git ~/gstack && cd ~/gstack && ./setup --host {host}"
    return "git clone --single-branch --depth 1 https://github.com/garrytan/gstack.git ~/gstack && cd ~/gstack && ./setup"


def selected_entries(
    data: Dict[str, Any],
    os_names: Iterable[str],
    profile: str,
    providers: Iterable[str] = (),
) -> List[Dict[str, Any]]:
    allowed = PROFILE_TIERS[profile]
    os_set = set(os_names)
    chosen = [x for x in data["skills"] if x.get("os") in os_set and x.get("tier") in allowed]
    provider_set = set(providers)
    if provider_set:
        if "evolution" not in os_set:
            raise RuntimeError("--provider is valid only with --os evolution or --os all")
        for item in data.get("provider_adapters", []):
            if item.get("provider") in provider_set and item.get("tier") in allowed:
                chosen.append(item)
    return sorted(
        chosen,
        key=lambda x: (
            OS_NAMES.index(str(x["os"])),
            0 if not x.get("provider") else 1,
            PROVIDERS.index(str(x.get("provider"))) if x.get("provider") in PROVIDERS else 999,
            int(x.get("rank", 999)),
        ),
    )


def resolve_install(entry: Dict[str, Any], agent: str) -> tuple[str, str]:
    install_type = str(entry.get("install_type", "skills-cli"))
    if entry.get("repo") == "garrytan/gstack":
        return gstack_command(agent), ""
    if install_type == "plugin":
        by_agent = entry.get("install_by_agent") or {}
        if not isinstance(by_agent, dict):
            return "", "invalid install_by_agent mapping"
        command = str(by_agent.get(agent, "")).strip()
        if command:
            return command, ""
        note = str(entry.get("notes", "")).strip()
        suffix = f"; {note}" if note else ""
        return "", f"no automated plugin installer for agent={agent}{suffix}"
    command = str(entry.get("install", "")).strip()
    return command, "" if command else "missing install command"


def normalize_commands(entries: List[Dict[str, Any]], agent: str, allow_custom: bool) -> List[Dict[str, Any]]:
    output: List[Dict[str, Any]] = []
    seen_commands: set[str] = set()
    for entry in entries:
        command, skipped_reason = resolve_install(entry, agent)
        install_type = str(entry.get("install_type", "skills-cli"))
        if not skipped_reason and install_type in {"custom", "plugin"} and not allow_custom:
            skipped_reason = f"{install_type} installer requires --allow-custom"
        if command and command in seen_commands:
            skipped_reason = "duplicate suite/provider installer; run once"
        if command and not skipped_reason:
            seen_commands.add(command)
        output.append({**entry, "resolved_install": command, "skipped_reason": skipped_reason})
    return output


def run_command(command: str, install_type: str) -> int:
    if install_type in {"custom", "plugin"} or "&&" in command:
        return subprocess.run(["bash", "-lc", command], check=False).returncode
    return subprocess.run(shlex.split(command), check=False).returncode


def print_human(entries: List[Dict[str, Any]]) -> None:
    current = None
    for item in entries:
        section = item["os"].upper()
        if item.get("provider"):
            section += f":{str(item['provider']).upper()}"
        if section != current:
            current = section
            print(f"\n[{section}]")
        print(f"{item['rank']:>2}. {item['skill']} ({item['tier']}) — {item['role']}")
        if item.get("notes"):
            print(f"    Note: {item['notes']}")
        if item.get("skipped_reason"):
            print(f"    SKIP: {item['skipped_reason']}")
        else:
            print(f"    {item['resolved_install']}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Inspect or install Agentic SDLC OS external skills")
    parser.add_argument("--os", choices=["all", *OS_NAMES], default="all")
    parser.add_argument("--profile", choices=sorted(PROFILE_TIERS), default="core")
    parser.add_argument("--provider", action="append", choices=PROVIDERS, default=[], help="Evolution observability provider adapter; repeatable")
    parser.add_argument("--agent", choices=["generic", "claude", "codex", "cursor", "opencode"], default="generic")
    parser.add_argument("--execute", action="store_true", help="Actually execute selected commands")
    parser.add_argument("--allow-custom", action="store_true", help="Allow custom/plugin installers after review")
    parser.add_argument("--acknowledge-review", action="store_true", help="Confirm that source, permissions, dependencies and licenses were reviewed")
    parser.add_argument("--continue-on-error", action="store_true")
    parser.add_argument("--json", action="store_true")
    return parser


def main(argv: Optional[Sequence[str]] = None) -> int:
    args = build_parser().parse_args(argv)
    data = load_manifest()
    os_names = OS_NAMES if args.os == "all" else [args.os]
    try:
        chosen = selected_entries(data, os_names, args.profile, args.provider)
    except RuntimeError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    entries = normalize_commands(chosen, args.agent, args.allow_custom)
    if args.json:
        print(json.dumps({"metadata": data.get("metadata", {}), "providers": args.provider, "selection": entries}, ensure_ascii=False, indent=2))
    else:
        print("Dry-run" if not args.execute else "Execution mode")
        print("Third-party skills are untrusted code/instructions. Review source, permissions, dependencies and license before installation.")
        if args.provider:
            print("Provider adapters are explicitly enabled: " + ", ".join(args.provider))
        print_human(entries)
    if not args.execute:
        return 0
    if not args.acknowledge_review:
        print("ERROR: execution requires --acknowledge-review", file=sys.stderr)
        return 2
    failures: List[str] = []
    for item in entries:
        if item.get("skipped_reason"):
            continue
        command = item["resolved_install"]
        label = f"{item['os']}/{item.get('provider') + '/' if item.get('provider') else ''}{item['skill']}"
        print(f"\nExecuting: {label}")
        code = run_command(command, str(item.get("install_type", "skills-cli")))
        if code != 0:
            failures.append(f"{label} (exit {code})")
            if not args.continue_on_error:
                break
    if failures:
        print("Failed: " + ", ".join(failures), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
