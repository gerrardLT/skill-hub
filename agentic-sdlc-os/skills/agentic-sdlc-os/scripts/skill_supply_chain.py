#!/usr/bin/env python3
"""Evidence-backed supply-chain audit for third-party Agent Skills.

The audit is deliberately fail-closed. A GitHub URL or a mutable branch name is not
sufficient evidence. Formal install approval requires a 40-character commit SHA, a
local snapshot of that exact repository state, an allowed license, a passing static
security/resource audit, and an install simulation. Custom/plugin installers also
require an explicit runtime-install attestation from the target harness.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "manifest" / "external-skills.json"
POLICY_PATH = ROOT / "manifest" / "skill-policy.json"
LOCK_PATH = ROOT / "manifest" / "skills.lock.json"
DEFAULT_EVIDENCE = ROOT / "validation" / "supply_chain" / "repository-evidence.json"
DEFAULT_REPORT = ROOT / "validation" / "supply_chain" / "audit-report.json"

HEX40 = re.compile(r"^[0-9a-f]{40}$", re.I)
FRONTMATTER = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.S)
MARKDOWN_LINK = re.compile(r"\[[^\]]*\]\(([^)]+)\)")


def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def load_json(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise RuntimeError(f"Expected JSON object: {path}")
    return payload


def atomic_write(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", dir=path.parent, delete=False, prefix=f".{path.name}.") as handle:
        json.dump(payload, handle, indent=2, ensure_ascii=False)
        handle.write("\n")
        temp = Path(handle.name)
    os.replace(temp, path)


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def tree_hash(path: Path) -> str:
    h = hashlib.sha256()
    excluded = {".git", "__pycache__", ".pytest_cache", "node_modules", ".DS_Store"}
    for file in sorted(x for x in path.rglob("*") if x.is_file() and not any(part in excluded for part in x.relative_to(path).parts)):
        rel = file.relative_to(path).as_posix()
        h.update(rel.encode("utf-8")); h.update(b"\0")
        h.update(file.read_bytes()); h.update(b"\0")
    return h.hexdigest()


def external_entries(manifest: dict[str, Any]) -> list[dict[str, Any]]:
    return [*manifest.get("skills", []), *manifest.get("provider_adapters", [])]


def parse_frontmatter(path: Path) -> dict[str, str]:
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return {}
    match = FRONTMATTER.match(text)
    if not match:
        return {}
    result: dict[str, str] = {}
    for line in match.group(1).splitlines():
        if ":" in line:
            key, value = line.split(":", 1)
            result[key.strip()] = value.strip().strip("\"'")
    return result


def detect_license(snapshot: Path) -> tuple[str | None, str | None]:
    candidates = [p for p in snapshot.iterdir() if p.is_file() and p.name.lower().startswith(("license", "copying"))]
    for path in sorted(candidates):
        try:
            text = path.read_text(encoding="utf-8", errors="ignore").lower()
        except OSError:
            continue
        if "apache license" in text and "version 2.0" in text:
            return "Apache-2.0", path.name
        if "permission is hereby granted, free of charge" in text and "the software is provided \"as is\"" in text:
            return "MIT", path.name
        if "redistribution and use in source and binary forms" in text:
            if "neither the name" in text or "contributors may be used to endorse" in text:
                return "BSD-3-Clause", path.name
            return "BSD-2-Clause", path.name
        if "isc license" in text or ("permission to use, copy, modify" in text and "the software is provided \"as is\"" in text):
            return "ISC", path.name
        if "creative commons attribution 4.0" in text:
            return "CC-BY-4.0", path.name
        if "gnu affero general public license" in text:
            return "AGPL-3.0-only", path.name
        if "business source license" in text:
            return "BUSL-1.1", path.name
    return None, candidates[0].name if candidates else None


def resolve_local_link(base_file: Path, raw: str) -> Path | None:
    target = raw.strip().split("#", 1)[0].split("?", 1)[0]
    if not target or target.startswith(("http://", "https://", "mailto:", "#", "data:")):
        return None
    return (base_file.parent / target).resolve()


def scan_tree(path: Path, policy: dict[str, Any]) -> dict[str, Any]:
    forbidden = [str(x).lower() for x in policy["security"].get("forbidden_patterns", [])]
    sensitive = [str(x).lower() for x in policy["security"].get("sensitive_patterns", [])]
    findings: list[dict[str, str]] = []
    broken_links: list[str] = []
    symlink_escapes: list[str] = []
    root = path.resolve()
    for node in path.rglob("*"):
        try:
            rel = node.relative_to(path).as_posix()
        except ValueError:
            rel = str(node)
        if node.is_symlink():
            try:
                resolved = node.resolve(strict=True)
                if root != resolved and root not in resolved.parents:
                    symlink_escapes.append(rel)
            except OSError:
                symlink_escapes.append(rel)
            continue
        if not node.is_file() or node.stat().st_size > 2_000_000:
            continue
        try:
            text = node.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        low = text.lower()
        for pattern in forbidden:
            if pattern in low:
                findings.append({"severity": "critical", "file": rel, "pattern": pattern})
        for pattern in sensitive:
            if pattern in low:
                findings.append({"severity": "review", "file": rel, "pattern": pattern})
        if node.suffix.lower() in {".md", ".mdx"}:
            for raw in MARKDOWN_LINK.findall(text):
                target = resolve_local_link(node, raw)
                if target is not None and not target.exists():
                    broken_links.append(f"{rel} -> {raw}")
    return {
        "critical_findings": [x for x in findings if x["severity"] == "critical"],
        "review_findings": [x for x in findings if x["severity"] == "review"],
        "broken_links": sorted(set(broken_links)),
        "symlink_escapes": sorted(set(symlink_escapes)),
    }


def skill_index(snapshot: Path) -> dict[str, list[Path]]:
    by_name: dict[str, list[Path]] = {}
    for entry in snapshot.rglob("SKILL.md"):
        meta = parse_frontmatter(entry)
        name = meta.get("name")
        if name:
            by_name.setdefault(name, []).append(entry.parent)
    return by_name


def simulate_install(skill_dir: Path, skill_name: str, policy: dict[str, Any]) -> dict[str, Any]:
    with tempfile.TemporaryDirectory(prefix="sdlc-skill-install-") as temp:
        target = Path(temp) / skill_name
        try:
            shutil.copytree(skill_dir, target, symlinks=True)
        except OSError as exc:
            return {"passed": False, "error": f"copy failed: {exc}"}
        entry = target / "SKILL.md"
        if not entry.is_file():
            return {"passed": False, "error": "SKILL.md missing after install simulation"}
        installed_name = parse_frontmatter(entry).get("name")
        if installed_name != skill_name:
            return {"passed": False, "error": f"frontmatter name mismatch: {installed_name!r}"}
        scan = scan_tree(target, policy)
        passed = not scan["critical_findings"] and not scan["broken_links"] and not scan["symlink_escapes"]
        return {"passed": passed, "installed_hash": tree_hash(target), **scan}


def _safe_repo_dir(repo: str) -> str:
    return re.sub(r"[^A-Za-z0-9_.-]+", "__", repo)


def online_intake(workspace: Path, *, formal: bool = False) -> dict[str, Any]:
    """Resolve immutable HEAD commits and snapshot repositories without executing them.

    This requires outbound GitHub access and git. It intentionally does not mark
    custom/plugin runtime installers as verified; those require explicit execution
    attestations from the actual target harness.
    """
    workspace = workspace.resolve()
    workspace.mkdir(parents=True, exist_ok=True)
    evidence = build_template()
    evidence["formal"] = bool(formal)
    for item in evidence["repositories"]:
        repo = str(item["repo"])
        url = f"https://github.com/{repo}.git"
        try:
            remote = subprocess.run(
                ["git", "ls-remote", url, "HEAD"], text=True, capture_output=True,
                timeout=60, check=False,
            )
        except (OSError, subprocess.TimeoutExpired) as exc:
            item["intake_error"] = f"ls-remote failed: {exc}"
            continue
        if remote.returncode != 0 or not remote.stdout.strip():
            item["intake_error"] = "ls-remote failed: " + remote.stderr.strip()[-1000:]
            continue
        commit = remote.stdout.split()[0].lower()
        if not HEX40.fullmatch(commit):
            item["intake_error"] = f"HEAD did not resolve to an immutable SHA: {commit!r}"
            continue
        clone_dir = workspace / (_safe_repo_dir(repo) + ".git-snapshot")
        snapshot_dir = workspace / _safe_repo_dir(repo)
        shutil.rmtree(clone_dir, ignore_errors=True); shutil.rmtree(snapshot_dir, ignore_errors=True)
        clone = subprocess.run(
            ["git", "-c", "core.hooksPath=/dev/null", "clone", "--filter=blob:none", "--no-checkout", url, str(clone_dir)],
            text=True, capture_output=True, timeout=180, check=False,
        )
        if clone.returncode != 0:
            item["intake_error"] = "clone failed: " + clone.stderr.strip()[-1000:]
            shutil.rmtree(clone_dir, ignore_errors=True)
            continue
        checkout = subprocess.run(
            ["git", "-C", str(clone_dir), "-c", "core.hooksPath=/dev/null", "checkout", "--detach", commit],
            text=True, capture_output=True, timeout=180, check=False,
        )
        if checkout.returncode != 0:
            item["intake_error"] = "checkout failed: " + checkout.stderr.strip()[-1000:]
            shutil.rmtree(clone_dir, ignore_errors=True)
            continue
        # Copy the checked-out tree without VCS metadata. No repository code is run.
        shutil.copytree(clone_dir, snapshot_dir, ignore=shutil.ignore_patterns(".git"), symlinks=True)
        shutil.rmtree(clone_dir, ignore_errors=True)
        detected, _ = detect_license(snapshot_dir)
        item.update({
            "commit_sha": commit,
            "snapshot_path": str(snapshot_dir),
            "snapshot_sha256": tree_hash(snapshot_dir),
            "license_id": detected or "",
            "runtime_install_verified": False,
            "runtime_install_harnesses": [],
            "reviewer": "automated-static-intake",
            "verified_at": now(),
        })
    return evidence

def build_template() -> dict[str, Any]:
    manifest = load_json(MANIFEST_PATH)
    repos = sorted({str(item["repo"]) for item in external_entries(manifest)})
    return {
        "schema_version": "2.5.0",
        "generated_at": now(),
        "formal": False,
        "notes": "Populate each repository from an immutable 40-char commit snapshot. formal=true is allowed only when every snapshot and runtime attestation comes from the target environment.",
        "repositories": [
            {
                "repo": repo,
                "commit_sha": "",
                "snapshot_path": "",
                "snapshot_sha256": "",
                "license_id": "",
                "runtime_install_verified": False,
                "runtime_install_harnesses": [],
                "reviewer": "",
                "verified_at": "",
            }
            for repo in repos
        ],
    }


def audit(evidence_path: Path) -> dict[str, Any]:
    manifest = load_json(MANIFEST_PATH)
    policy = load_json(POLICY_PATH)
    evidence = load_json(evidence_path)
    base = evidence_path.parent
    repo_evidence = {str(item.get("repo")): item for item in evidence.get("repositories", [])}
    by_repo: dict[str, list[dict[str, Any]]] = {}
    for item in external_entries(manifest):
        by_repo.setdefault(str(item["repo"]), []).append(item)

    repo_reports: list[dict[str, Any]] = []
    unit_reports: list[dict[str, Any]] = []
    for repo, items in sorted(by_repo.items()):
        supplied = repo_evidence.get(repo, {})
        failures: list[str] = []
        warnings: list[str] = []
        commit = str(supplied.get("commit_sha", "")).lower()
        if not HEX40.fullmatch(commit):
            failures.append("missing immutable 40-char commit_sha")
        raw_path = str(supplied.get("snapshot_path", "")).strip()
        snapshot: Path | None = None
        if raw_path:
            snapshot = Path(raw_path)
            if not snapshot.is_absolute():
                snapshot = (base / snapshot).resolve()
            if not snapshot.is_dir():
                failures.append(f"snapshot_path is not a directory: {snapshot}")
                snapshot = None
        else:
            failures.append("missing snapshot_path")

        detected_license = None
        license_file = None
        repository_hash = None
        repo_scan: dict[str, Any] = {"critical_findings": [], "review_findings": [], "broken_links": [], "symlink_escapes": []}
        index: dict[str, list[Path]] = {}
        if snapshot:
            repository_hash = tree_hash(snapshot)
            expected_hash = str(supplied.get("snapshot_sha256", "")).strip().lower()
            if expected_hash and expected_hash != repository_hash:
                failures.append("snapshot_sha256 mismatch")
            elif not expected_hash:
                failures.append("missing snapshot_sha256")
            detected_license, license_file = detect_license(snapshot)
            index = skill_index(snapshot)
            repo_scan = scan_tree(snapshot, policy)
            if repo_scan["symlink_escapes"]:
                failures.append("repository contains escaping/broken symlinks")

        declared_license = str(supplied.get("license_id", "")).strip() or detected_license
        allowed_licenses = set(policy.get("allowed_licenses", []))
        if not declared_license:
            failures.append("license could not be established")
        elif declared_license not in allowed_licenses:
            failures.append(f"license not allowed by policy: {declared_license}")
        if detected_license and supplied.get("license_id") and detected_license != supplied.get("license_id"):
            failures.append(f"declared license {supplied.get('license_id')} != detected {detected_license}")
        if repo_scan["critical_findings"]:
            warnings.append("repository-level critical strings found; unit-level scan decides installability")

        for manifest_item in items:
            skill = str(manifest_item["skill"])
            install_type = str(manifest_item.get("install_type", "skills-cli"))
            unit_failures = list(failures)
            unit_warnings: list[str] = []
            install_sim: dict[str, Any] = {"passed": False, "error": "snapshot unavailable"}
            locations = index.get(skill, []) if snapshot else []
            if install_type == "skills-cli":
                if len(locations) != 1:
                    unit_failures.append(f"expected exactly one SKILL.md named {skill}; found {len(locations)}")
                else:
                    install_sim = simulate_install(locations[0], skill, policy)
                    if not install_sim.get("passed"):
                        unit_failures.append("static install simulation failed")
                    if install_sim.get("review_findings"):
                        unit_warnings.append("network/shell/environment-sensitive content requires human review")
            else:
                # Custom/plugin installers execute host-specific code. Static repository
                # inspection is necessary but not sufficient; formal approval requires a
                # recorded runtime install on an explicitly named harness.
                runtime_ok = supplied.get("runtime_install_verified") is True
                if not runtime_ok:
                    unit_failures.append(f"{install_type} runtime install not verified")
                install_sim = {"passed": runtime_ok, "mode": "runtime-attestation", "harnesses": supplied.get("runtime_install_harnesses", [])}

            if snapshot and locations:
                unit_scan = scan_tree(locations[0], policy)
                if unit_scan["critical_findings"]:
                    unit_failures.append("critical security pattern in skill")
                if unit_scan["broken_links"]:
                    unit_failures.append("broken local resource links in skill")
                if unit_scan["symlink_escapes"]:
                    unit_failures.append("skill contains escaping/broken symlink")
            else:
                unit_scan = {"critical_findings": [], "review_findings": [], "broken_links": [], "symlink_escapes": []}

            unit_reports.append({
                "repo": repo,
                "skill": skill,
                "os": manifest_item.get("os"),
                "provider": manifest_item.get("provider"),
                "tier": manifest_item.get("tier"),
                "install_type": install_type,
                "commit_sha": commit or None,
                "license_id": declared_license,
                "repository_hash": repository_hash,
                "skill_path": locations[0].relative_to(snapshot).as_posix() if snapshot and len(locations) == 1 else None,
                "security": unit_scan,
                "install_test": install_sim,
                "warnings": list(dict.fromkeys(unit_warnings)),
                "failures": list(dict.fromkeys(unit_failures)),
                "install_allowed": not unit_failures,
            })

        repo_reports.append({
            "repo": repo,
            "commit_sha": commit or None,
            "snapshot_path": str(snapshot) if snapshot else None,
            "repository_hash": repository_hash,
            "license_id": declared_license,
            "detected_license": detected_license,
            "license_file": license_file,
            "runtime_install_verified": supplied.get("runtime_install_verified") is True,
            "reviewer": supplied.get("reviewer", ""),
            "verified_at": supplied.get("verified_at", ""),
            "failures": list(dict.fromkeys(failures)),
            "warnings": list(dict.fromkeys(warnings)),
        })

    unique_units: dict[tuple[str, str], dict[str, Any]] = {}
    for unit in unit_reports:
        unique_units.setdefault((str(unit["repo"]), str(unit["skill"])), unit)
    allowed_unique = sum(1 for unit in unique_units.values() if unit["install_allowed"])
    allowed_entries = sum(1 for unit in unit_reports if unit["install_allowed"])
    formal = evidence.get("formal") is True
    all_allowed = allowed_entries == len(unit_reports)
    return {
        "schema_version": "2.5.0",
        "generated_at": now(),
        "formal": formal,
        "passed": formal and all_allowed,
        "entries": len(unit_reports),
        "unique_units": len(unique_units),
        "repositories": len(repo_reports),
        "allowed_entries": allowed_entries,
        "allowed_unique_units": allowed_unique,
        "blocked_entries": len(unit_reports) - allowed_entries,
        "strict_external_install_ready": formal and all_allowed,
        "repository_reports": repo_reports,
        "unit_reports": unit_reports,
    }


def build_lock_from_report(report: dict[str, Any], output: Path) -> dict[str, Any]:
    # Preserve freshly generated local hashes from skill_governance, but never
    # allow a third-party entry unless its repo+skill audit is passing.
    import importlib.util
    path = ROOT / "scripts" / "skill_governance.py"
    spec = importlib.util.spec_from_file_location("sdlc_skill_governance", path)
    if spec is None or spec.loader is None:
        raise RuntimeError("Cannot load skill_governance.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    lock = module.build_lock(resolve_external=False, offline=True)
    units = {(str(x["repo"]), str(x["skill"])): x for x in report.get("unit_reports", [])}
    for item in lock.get("external_skills", []):
        unit = units.get((str(item.get("repo")), str(item.get("skill"))))
        if not unit:
            continue
        allowed = bool(report.get("formal") and unit.get("install_allowed"))
        item.update({
            "commit_sha": unit.get("commit_sha"),
            "resolution_status": "locked-reviewed" if allowed else "blocked",
            "install_allowed": allowed,
            "license_id": unit.get("license_id"),
            "repository_hash": unit.get("repository_hash"),
            "security_status": "pass" if not unit.get("failures") else "blocked",
            "install_test_status": "pass" if unit.get("install_test", {}).get("passed") else "blocked",
        })
    lock["schema_version"] = "2.5.0"
    lock["supply_chain_report_hash"] = hashlib.sha256(json.dumps(report, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()
    atomic_write(output, lock)
    return lock


def summary(report: dict[str, Any]) -> str:
    return (
        f"formal={report.get('formal')} passed={report.get('passed')} "
        f"entries={report.get('allowed_entries')}/{report.get('entries')} "
        f"unique={report.get('allowed_unique_units')}/{report.get('unique_units')} "
        f"repos={report.get('repositories')}"
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Third-party Agent Skill supply-chain audit")
    sub = parser.add_subparsers(dest="command", required=True)
    p = sub.add_parser("template"); p.add_argument("--output", default=str(DEFAULT_EVIDENCE))
    p = sub.add_parser("online-intake"); p.add_argument("--workspace", required=True); p.add_argument("--output", default=str(DEFAULT_EVIDENCE)); p.add_argument("--formal", action="store_true")
    p = sub.add_parser("audit"); p.add_argument("evidence", nargs="?", default=str(DEFAULT_EVIDENCE)); p.add_argument("--output", default=str(DEFAULT_REPORT)); p.add_argument("--json", action="store_true")
    p = sub.add_parser("build-lock"); p.add_argument("report", nargs="?", default=str(DEFAULT_REPORT)); p.add_argument("--output", default=str(LOCK_PATH)); p.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    try:
        if args.command == "template":
            payload = build_template(); atomic_write(Path(args.output), payload); print(json.dumps(payload, indent=2)); return 0
        if args.command == "online-intake":
            payload = online_intake(Path(args.workspace), formal=args.formal); atomic_write(Path(args.output), payload); print(json.dumps(payload, indent=2)); return 0
        if args.command == "audit":
            payload = audit(Path(args.evidence).resolve()); atomic_write(Path(args.output), payload)
            print(json.dumps(payload, indent=2) if args.json else summary(payload))
            return 0 if payload.get("passed") else 2
        report = load_json(Path(args.report).resolve())
        payload = build_lock_from_report(report, Path(args.output).resolve())
        print(json.dumps(payload, indent=2) if args.json else f"wrote {args.output}")
        return 0
    except (OSError, ValueError, RuntimeError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=os.sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
