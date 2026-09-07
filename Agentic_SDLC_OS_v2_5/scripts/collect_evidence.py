#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import os
import shlex
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
REPO_SDLC = ROOT / "skills" / "agentic-sdlc-os" / "scripts" / "sdlc.py"
SDLC = REPO_SDLC if REPO_SDLC.exists() else ROOT / "scripts" / "sdlc.py"


def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def hash_path(path: Path) -> tuple[str, int, int]:
    digest = hashlib.sha256()
    total = 0
    count = 0
    paths = [path] if path.is_file() else sorted(item for item in path.rglob("*") if item.is_file())
    for item in paths:
        rel = item.name if path.is_file() else item.relative_to(path).as_posix()
        digest.update(rel.encode())
        with item.open("rb") as handle:
            for chunk in iter(lambda: handle.read(1024 * 1024), b""):
                digest.update(chunk)
                total += len(chunk)
        count += 1
    return digest.hexdigest(), total, count


def run_git(project: Path) -> dict[str, Any] | None:
    if not (project / ".git").exists():
        return None
    def call(*args: str) -> str:
        result = subprocess.run(["git", "-C", str(project), *args], text=True, capture_output=True, check=False)
        return result.stdout.strip()
    return {
        "head": call("rev-parse", "HEAD"),
        "branch": call("rev-parse", "--abbrev-ref", "HEAD"),
        "status": call("status", "--porcelain"),
        "diff_stat": call("diff", "--stat"),
    }


def parse_junit(path: Path) -> dict[str, Any]:
    root = ET.parse(path).getroot()
    suites = [root] if root.tag == "testsuite" else list(root.findall("testsuite"))
    totals = {"tests": 0, "failures": 0, "errors": 0, "skipped": 0, "time_seconds": 0.0}
    for suite in suites:
        for key in ["tests", "failures", "errors", "skipped"]:
            totals[key] += int(float(suite.attrib.get(key, 0)))
        totals["time_seconds"] += float(suite.attrib.get("time", 0.0))
    totals["passed"] = totals["failures"] == 0 and totals["errors"] == 0
    return totals


def parse_coverage(path: Path) -> dict[str, Any]:
    root = ET.parse(path).getroot()
    line_rate = float(root.attrib.get("line-rate", 0.0))
    branch_rate = float(root.attrib.get("branch-rate", 0.0))
    return {"line_coverage": round(line_rate, 6), "branch_coverage": round(branch_rate, 6)}


def collect(args: argparse.Namespace) -> dict[str, Any]:
    project = Path(args.project).expanduser().resolve()
    evidence: list[dict[str, Any]] = []
    git = run_git(project)
    if git:
        evidence.append({
            "claim": f"Source revision {git['head']} on branch {git['branch']} was collected; dirty={bool(git['status'])}",
            "source": "git://local-repository",
            "source_type": "code",
            "quality": "high",
            "method": "git rev-parse and git status",
            "details": git,
        })
    if args.test_command:
        started = now()
        result = subprocess.run(shlex.split(args.test_command), cwd=project, text=True, capture_output=True, check=False, timeout=args.test_timeout)
        output_path = project / ".sdlc" / "evidence" / f"test-command-{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}.log"
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(result.stdout + "\n--- STDERR ---\n" + result.stderr, encoding="utf-8")
        evidence.append({
            "claim": f"Test command exited with code {result.returncode}",
            "source": str(output_path.relative_to(project)),
            "source_type": "test",
            "quality": "high",
            "method": args.test_command,
            "details": {"returncode": result.returncode, "started_at": started, "passed": result.returncode == 0},
        })
    if args.junit:
        path = Path(args.junit).expanduser().resolve()
        details = parse_junit(path)
        evidence.append({
            "claim": f"JUnit report contains {details['tests']} tests with {details['failures']} failures and {details['errors']} errors",
            "source": str(path), "source_type": "test", "quality": "high", "method": "JUnit XML parser", "details": details,
        })
    if args.coverage:
        path = Path(args.coverage).expanduser().resolve()
        details = parse_coverage(path)
        evidence.append({
            "claim": f"Coverage report shows line={details['line_coverage']:.1%}, branch={details['branch_coverage']:.1%}",
            "source": str(path), "source_type": "test", "quality": "high", "method": "Cobertura XML parser", "details": details,
        })
    for raw in args.artifact:
        path = Path(raw).expanduser().resolve()
        digest, total, count = hash_path(path)
        evidence.append({
            "claim": f"Build artifact {path.name} has SHA-256 {digest}, {total} bytes across {count} files",
            "source": str(path), "source_type": "audit", "quality": "high", "method": "deterministic SHA-256", "details": {"sha256": digest, "bytes": total, "files": count},
        })
    if args.deployment:
        path = Path(args.deployment).expanduser().resolve()
        details = json.loads(path.read_text(encoding="utf-8"))
        evidence.append({
            "claim": f"Deployment metadata recorded for environment {details.get('environment', 'unknown')} version {details.get('version', 'unknown')}",
            "source": str(path), "source_type": "official", "quality": "high", "method": "deployment metadata import", "details": details,
        })
    payload = {"schema_version": "2.0.0", "project": str(project), "collected_at": now(), "evidence": evidence}
    output = Path(args.output).expanduser().resolve() if args.output else project / ".sdlc" / "evidence" / f"collection-{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    payload["output"] = str(output)
    if args.register:
        registrations = []
        for item in evidence:
            command = [
                sys.executable, str(SDLC), "add-evidence", str(project),
                "--claim", item["claim"], "--source", item["source"],
                "--source-type", item["source_type"], "--quality", item["quality"],
                "--method", item["method"], "--limitations", "Automatically collected; review semantic relevance before gate use",
            ]
            if args.supports:
                command.extend(["--supports", args.supports])
            result = subprocess.run(command, text=True, capture_output=True, check=False)
            registrations.append({"returncode": result.returncode, "stdout": result.stdout.strip(), "stderr": result.stderr.strip()})
        payload["registrations"] = registrations
    return payload


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Collect code, test, coverage, build and deployment evidence")
    parser.add_argument("project")
    parser.add_argument("--test-command")
    parser.add_argument("--test-timeout", type=int, default=900)
    parser.add_argument("--junit")
    parser.add_argument("--coverage")
    parser.add_argument("--artifact", action="append", default=[])
    parser.add_argument("--deployment")
    parser.add_argument("--supports")
    parser.add_argument("--register", action="store_true")
    parser.add_argument("--output")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        payload = collect(args)
        print(json.dumps(payload, indent=2))
        return 0
    except (OSError, ValueError, RuntimeError, subprocess.TimeoutExpired, ET.ParseError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
