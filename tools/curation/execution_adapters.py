#!/usr/bin/env python3
"""Execution adapters with explicit authorization and isolated mutation."""
from __future__ import annotations

import json
import shutil
import subprocess
import tempfile
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable

DANGEROUS_SCOPES = {"workspace-write", "remote-git", "network", "merge", "deploy"}
TOOL_BY_SCOPE = {
    "workspace-write": {"edit", "write"},
    "remote-git": {"remote-git"},
    "network": {"network"},
    "merge": {"merge"},
    "deploy": {"deploy"},
}

class AuthorizationError(PermissionError):
    pass

@dataclass(frozen=True)
class ExecutionPolicy:
    authorized_scopes: frozenset[str] = field(default_factory=frozenset)

    def require(self, scopes: set[str]) -> None:
        unknown = scopes - DANGEROUS_SCOPES
        if unknown:
            raise AuthorizationError(f"unknown authorization scopes: {sorted(unknown)}")
        missing = scopes - self.authorized_scopes
        if missing:
            raise AuthorizationError(f"explicit authorization required: {sorted(missing)}")


def required_scopes(tools: set[str], mutation: str) -> set[str]:
    scopes = {scope for scope, controlled in TOOL_BY_SCOPE.items() if tools & controlled}
    if mutation == "isolated-worktree":
        scopes.add("workspace-write")
    return scopes


def artifact_adapter(prompt: str, timeout: int, worker: Callable[[str, int], str]) -> tuple[str, dict]:
    started = time.perf_counter()
    output = worker(prompt, timeout)
    return output, {"adapter": "artifact", "duration_ms": round((time.perf_counter() - started) * 1000, 3), "tools": []}


def _default_workspace_runner(prompt: str, cwd: Path, tools: list[str], timeout: int) -> tuple[str, list[dict]]:
    executable = shutil.which("pi") or shutil.which("pi.cmd")
    if not executable:
        raise RuntimeError("pi-unavailable")
    process = subprocess.run(
        [executable, "-p", "--mode", "json", "--no-skills", "--no-extensions", "--no-context-files", "--no-session", "--tools", ",".join(tools), prompt],
        cwd=cwd,
        capture_output=True,
        timeout=timeout,
        check=False,
    )
    if process.returncode:
        raise RuntimeError(process.stderr.decode("utf-8", errors="replace") or f"pi-exit-{process.returncode}")
    events = [json.loads(line) for line in process.stdout.decode("utf-8", errors="replace").splitlines() if line.strip()]
    ends = [event for event in events if event.get("type") == "message_end" and event.get("message", {}).get("role") == "assistant"]
    if not ends:
        raise RuntimeError("no-output")
    output = "".join(part.get("text", "") for part in ends[-1]["message"].get("content", []) if part.get("type") == "text")
    tool_events = [
        {"type": event.get("type"), "tool": event.get("toolName"), "is_error": event.get("isError", False)}
        for event in events if str(event.get("type", "")).startswith("tool_execution_")
    ]
    return output, tool_events


def workspace_adapter(
    prompt: str,
    timeout: int,
    *,
    repository: Path,
    tools: list[str],
    mutation: str,
    policy: ExecutionPolicy,
    runner: Callable[[str, Path, list[str], int], tuple[str, list[dict]]] = _default_workspace_runner,
) -> tuple[str, dict]:
    requested = set(tools)
    policy.require(required_scopes(requested, mutation))
    if mutation not in {"none", "isolated-worktree"}:
        raise AuthorizationError("workspace adapter requires read-only or isolated-worktree mutation")
    base = repository.resolve()
    if subprocess.run(["git", "status", "--porcelain"], cwd=base, capture_output=True, text=True, check=True).stdout.strip():
        raise RuntimeError("repository-worktree-not-clean")
    with tempfile.TemporaryDirectory(prefix="dev-loop-worktree-") as temp:
        worktree = Path(temp) / "repo"
        subprocess.run(["git", "worktree", "add", "--detach", str(worktree), "HEAD"], cwd=base, capture_output=True, text=True, check=True)
        started = time.perf_counter()
        try:
            output, events = runner(prompt, worktree, tools, timeout)
            diff = subprocess.run(["git", "diff", "--binary"], cwd=worktree, capture_output=True, text=True, check=True).stdout
            status = subprocess.run(["git", "status", "--short"], cwd=worktree, capture_output=True, text=True, check=True).stdout
            if mutation == "none" and status.strip():
                raise RuntimeError("read-only-worktree-modified")
            evidence = {
                "adapter": "workspace",
                "worktree": str(worktree),
                "tools": tools,
                "authorized_scopes": sorted(policy.authorized_scopes),
                "duration_ms": round((time.perf_counter() - started) * 1000, 3),
                "tool_events": events,
                "git_status": status,
                "diff": diff,
            }
            return output, evidence
        finally:
            subprocess.run(["git", "worktree", "remove", "--force", str(worktree)], cwd=base, capture_output=True, text=True, check=False)
