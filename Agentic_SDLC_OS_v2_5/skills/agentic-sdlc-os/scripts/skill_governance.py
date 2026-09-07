#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
import urllib.error
import urllib.request
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from statistics import mean
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
POLICY_PATH = ROOT / "manifest" / "skill-policy.json"
EXTERNAL_PATH = ROOT / "manifest" / "external-skills.json"
LOCK_PATH = ROOT / "manifest" / "skills.lock.json"


def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def load_json(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise RuntimeError(f"Expected JSON object: {path}")
    return payload


def tree_hash(path: Path) -> str:
    """Hash stable Skill content while excluding generated/self-referential files."""
    digest = hashlib.sha256()
    excluded_parts = {"__pycache__", ".pytest_cache", "dist", ".git", ".sdlc"}
    excluded_files = {"skills.lock.json", ".DS_Store", ".coverage"}
    items = []
    for item in path.rglob("*"):
        if not item.is_file():
            continue
        rel = item.relative_to(path)
        if any(part in excluded_parts for part in rel.parts):
            continue
        if item.name in excluded_files or item.suffix == ".pyc":
            continue
        items.append(item)
    for item in sorted(items):
        rel = item.relative_to(path).as_posix()
        digest.update(rel.encode("utf-8"))
        digest.update(b"\0")
        digest.update(item.read_bytes())
    return digest.hexdigest()


def parse_frontmatter(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
    match = re.match(r"^---\s*\n(.*?)\n---\s*\n", text, re.S)
    if not match:
        return {}
    result: dict[str, str] = {}
    for line in match.group(1).splitlines():
        if ":" in line:
            key, value = line.split(":", 1)
            result[key.strip()] = value.strip().strip("\"'")
    return result


def scan_skill(path: Path, policy: dict[str, Any]) -> dict[str, Any]:
    entry = path / "SKILL.md"
    if not entry.exists():
        return {"path": str(path), "valid": False, "errors": ["missing SKILL.md"]}
    meta = parse_frontmatter(entry)
    errors: list[str] = []
    warnings: list[str] = []
    findings: list[dict[str, str]] = []
    if not meta.get("name") or not meta.get("description"):
        errors.append("frontmatter must contain name and description")
    referenced = re.findall(r"\((references/[^)]+|scripts/[^)]+|assets/[^)]+)\)", entry.read_text(encoding="utf-8"))
    for rel in referenced:
        if not (path / rel).exists():
            errors.append(f"missing referenced resource: {rel}")
    security = policy["security"]
    policy_literal_files = {"manifest/skill-policy.json", "references/manifests/skill-policy.json"}
    for file in sorted(x for x in path.rglob("*") if x.is_file() and x.stat().st_size <= 2_000_000):
        relative = file.relative_to(path).as_posix()
        if relative in policy_literal_files:
            continue
        try:
            text = file.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for pattern in security["forbidden_patterns"]:
            if pattern.lower() in text.lower():
                findings.append({"severity": "critical", "file": str(file.relative_to(path)), "pattern": pattern})
        for pattern in security["sensitive_patterns"]:
            if pattern.lower() in text.lower():
                findings.append({"severity": "review", "file": str(file.relative_to(path)), "pattern": pattern})
    if any(item["severity"] == "critical" for item in findings):
        errors.append("critical security pattern detected")
    elif findings:
        warnings.append("network, shell, environment or destructive capability requires review")
    line_count = len(entry.read_text(encoding="utf-8").splitlines())
    if line_count > 500:
        warnings.append("SKILL.md exceeds 500 lines")
    return {
        "path": str(path), "name": meta.get("name"), "description": meta.get("description"),
        "valid": not errors, "errors": errors, "warnings": warnings, "findings": findings,
        "content_hash": tree_hash(path), "files": sum(1 for x in path.rglob("*") if x.is_file()),
        "skill_lines": line_count,
    }


def github_commit(repo: str, ref: str = "HEAD") -> str:
    url = f"https://api.github.com/repos/{repo}/commits/{ref}"
    headers = {"User-Agent": "agentic-sdlc-os-skill-governance"}
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    request = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(request, timeout=15) as response:
        payload = json.loads(response.read().decode("utf-8"))
    sha = str(payload.get("sha", ""))
    if not re.fullmatch(r"[0-9a-f]{40}", sha):
        raise RuntimeError(f"Could not resolve commit for {repo}")
    return sha


def external_entries(manifest: dict[str, Any]) -> list[dict[str, Any]]:
    """Return generic external skills plus explicit provider adapters."""
    items = list(manifest.get("skills", []))
    items.extend(manifest.get("provider_adapters", []))
    return items


def build_lock(*, resolve_external: bool, offline: bool) -> dict[str, Any]:
    policy = load_json(POLICY_PATH)
    local = []
    skills_root = ROOT / "skills"
    candidates = sorted(path for path in skills_root.iterdir() if path.is_dir()) if skills_root.exists() else [ROOT]
    for path in candidates:
        scan = scan_skill(path, policy)
        rel = path.relative_to(ROOT).as_posix() if path != ROOT else "."
        local.append({
            "source": "local", "name": path.name, "content_hash": scan.get("content_hash"),
            "security_status": "pass" if scan.get("valid") else "blocked",
            "lifecycle_status": "active", "path": rel,
        })
    external_manifest = load_json(EXTERNAL_PATH)
    resolved: dict[str, str | None] = {}
    external = []
    for item in external_entries(external_manifest):
        repo = str(item["repo"])
        if repo not in resolved:
            commit = None
            if resolve_external and not offline:
                try:
                    commit = github_commit(repo)
                except (urllib.error.URLError, TimeoutError, RuntimeError):
                    commit = None
            resolved[repo] = commit
        external.append({
            "source": "github", "repo": repo, "skill": item["skill"], "os": item["os"],
            "provider": item.get("provider"),
            "commit_sha": resolved[repo], "resolution_status": "locked" if resolved[repo] else "unresolved",
            "install_allowed": bool(resolved[repo]), "review_source_and_license": item.get("review_source_and_license", False),
        })
    return {
        "schema_version": "2.0.0", "generated_at": now(), "policy_hash": hashlib.sha256(POLICY_PATH.read_bytes()).hexdigest(),
        "mode": policy["default_mode"], "local_skills": local, "external_skills": external,
    }


def effectiveness(state: dict[str, Any], policy: dict[str, Any]) -> list[dict[str, Any]]:
    groups: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for run in state.get("runs", []):
        groups[str(run.get("skill", "unknown"))].append(run)
    result = []
    spec = policy["effectiveness"]
    for skill, runs in sorted(groups.items()):
        success = sum(1 for run in runs if str(run.get("outcome", "")).lower() in {"success", "passed", "pass"})
        success_rate = success / len(runs)
        avg_cost = mean(float(run.get("cost_usd", 0.0)) for run in runs)
        avg_duration = mean(float(run.get("duration_ms", 0.0)) for run in runs)
        if len(runs) < int(spec["minimum_runs_for_active"]):
            status = "canary"
        elif success_rate < float(spec["deprecate_below_success_rate"]):
            status = "deprecated"
        elif success_rate >= float(spec["minimum_success_rate"]):
            status = "active"
        else:
            status = "watch"
        score = round(100 * (0.75 * success_rate + 0.25 * min(1.0, len(runs) / 20)), 2)
        result.append({"skill": skill, "runs": len(runs), "success_rate": round(success_rate, 4), "average_cost_usd": round(avg_cost, 6), "average_duration_ms": round(avg_duration, 2), "score": score, "recommended_status": status})
    return result


def conflicts(external: dict[str, Any]) -> list[dict[str, Any]]:
    by_name: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for item in external_entries(external):
        by_name[str(item.get("skill"))].append(item)
    return [{"type": "duplicate-skill-name", "skill": name, "sources": sorted({item["repo"] for item in items})} for name, items in by_name.items() if len({item["repo"] for item in items}) > 1]


def select_skills(os_name: str, profile: str, tiers: set[str], providers: set[str] | None = None) -> dict[str, Any]:
    policy = load_json(POLICY_PATH)
    manifest = load_json(EXTERNAL_PATH)
    limit = int(policy["maximum_active_skills"][profile])
    items = [item for item in manifest["skills"] if item["os"] == os_name and item["tier"] in tiers]
    items.sort(key=lambda item: int(item["rank"]))
    selected = items[:limit]
    adapters: list[dict[str, Any]] = []
    provider_set = providers or set()
    if provider_set:
        if os_name != "evolution":
            raise RuntimeError("provider adapters are supported only for evolution")
        adapters = [
            item for item in manifest.get("provider_adapters", [])
            if item.get("provider") in provider_set and item.get("tier") in tiers
        ]
        adapters.sort(key=lambda item: (str(item.get("provider")), int(item.get("rank", 999))))
    return {
        "os": os_name, "profile": profile, "limit": limit, "selected": selected,
        "provider_adapters": adapters, "truncated": len(items) > len(selected),
    }


def verify_lock_payload(lock: dict[str, Any], *, root: Path = ROOT) -> dict[str, Any]:
    """Verify every installed local Skill while tolerating absent siblings in a standalone package."""
    suite_mode = (root / "skills").is_dir()
    issues: list[dict[str, Any]] = []
    verified: list[str] = []
    not_installed: list[str] = []
    for item in lock.get("local_skills", []):
        declared = root / str(item.get("path", ""))
        if declared.exists():
            path = declared
        elif not suite_mode and str(item.get("name")) == root.name and (root / "SKILL.md").exists():
            path = root
        elif not suite_mode:
            not_installed.append(str(item.get("name")))
            continue
        else:
            path = declared
        actual = tree_hash(path) if path.exists() else None
        if actual != item.get("content_hash"):
            issues.append({"skill": item.get("name"), "expected": item.get("content_hash"), "actual": actual})
        else:
            verified.append(str(item.get("name")))
    unresolved = [item for item in lock.get("external_skills", []) if not item.get("install_allowed")]
    return {
        "valid": not issues and bool(verified),
        "scope": "repository-suite" if suite_mode else "standalone-installed-set",
        "local_verified": verified,
        "local_not_installed": not_installed,
        "local_issues": issues,
        "external_unresolved": len(unresolved),
        "strict_external_install_ready": not unresolved,
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Lock, scan, score and retire Agentic SDLC Skills")
    sub = parser.add_subparsers(dest="command", required=True)
    p = sub.add_parser("scan"); p.add_argument("path", nargs="?", default=str(ROOT / "skills"))
    p = sub.add_parser("lock"); p.add_argument("--resolve-external", action="store_true"); p.add_argument("--offline", action="store_true"); p.add_argument("--output", default=str(LOCK_PATH))
    p = sub.add_parser("verify-lock"); p.add_argument("--lock", default=str(LOCK_PATH))
    p = sub.add_parser("score"); p.add_argument("state")
    sub.add_parser("conflicts")
    p = sub.add_parser("select"); p.add_argument("--os", required=True); p.add_argument("--profile", choices=["lite", "standard", "high-assurance"], required=True); p.add_argument("--tiers", default="core,recommended"); p.add_argument("--provider", action="append", choices=["sentry", "datadog", "posthog"], default=[])
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        policy = load_json(POLICY_PATH)
        if args.command == "scan":
            path = Path(args.path).resolve()
            payload = [scan_skill(item, policy) for item in sorted(path.iterdir()) if item.is_dir()] if not (path / "SKILL.md").exists() else scan_skill(path, policy)
        elif args.command == "lock":
            payload = build_lock(resolve_external=args.resolve_external, offline=args.offline)
            Path(args.output).write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
        elif args.command == "verify-lock":
            lock = load_json(Path(args.lock))
            payload = verify_lock_payload(lock)
        elif args.command == "score":
            payload = effectiveness(load_json(Path(args.state)), policy)
        elif args.command == "conflicts":
            payload = conflicts(load_json(EXTERNAL_PATH))
        else:
            payload = select_skills(args.os, args.profile, set(x.strip() for x in args.tiers.split(",") if x.strip()), set(args.provider))
        print(json.dumps(payload, indent=2))
        if args.command == "verify-lock" and not payload.get("valid"):
            return 3
        return 0
    except (OSError, ValueError, RuntimeError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
