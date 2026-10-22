#!/usr/bin/env python3
"""Execution adapters with explicit authorization and isolated mutation."""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import hashlib
import tempfile
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable

DANGEROUS_SCOPES = {"workspace-write", "remote-git", "network", "merge", "deploy"}
EVAL_MODEL = os.environ.get("CAPABILITY_EVAL_MODEL", "cx/gpt-5.6-terra")
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
    result = worker(prompt, timeout)
    output, extra = result if isinstance(result, tuple) else (result, {})
    return output, {"adapter": "artifact", "duration_ms": round((time.perf_counter() - started) * 1000, 3), "tools": [], **extra}


def _default_workspace_runner(prompt: str, cwd: Path, tools: list[str], timeout: int) -> tuple[str, list[dict]]:
    executable = shutil.which("pi") or shutil.which("pi.cmd")
    if not executable:
        raise RuntimeError("pi-unavailable")
    with tempfile.NamedTemporaryFile("w", suffix=".md", encoding="utf-8", delete=False) as handle:
        handle.write(prompt)
        prompt_path = Path(handle.name)
    try:
        process = subprocess.run(
            [
                executable, "-p", "--mode", "json", "--model", EVAL_MODEL, "--thinking", "low", "--no-skills", "--no-extensions",
                "--no-context-files", "--no-session", "--offline", "--tools", ",".join(tools),
                "--system-prompt", "Operate only inside the current workspace. Use only the enabled tools. Never access network, remote Git, merge, or deployment.",
                f"@{prompt_path}",
            ],
            cwd=cwd,
            capture_output=True,
            timeout=timeout,
            check=False,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise RuntimeError(f"workspace-model-launch-failed:{type(exc).__name__}") from exc
    finally:
        prompt_path.unlink(missing_ok=True)
    if process.returncode:
        raise RuntimeError(process.stderr.decode("utf-8", errors="replace") or f"pi-exit-{process.returncode}")
    events = [json.loads(line) for line in process.stdout.decode("utf-8", errors="replace").splitlines() if line.strip()]
    outputs = [
        "".join(part.get("text", "") for part in event["message"].get("content", []) if part.get("type") == "text")
        for event in events
        if event.get("type") == "message_end" and event.get("message", {}).get("role") == "assistant"
    ]
    output = next((value for value in reversed(outputs) if value.strip()), "")
    if not output:
        raise RuntimeError("no-output")
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
    evidence_dir: Path | None = None,
    verification_commands: list[list[str]] | None = None,
    deliver_changes: bool = False,
) -> tuple[str, dict]:
    requested = set(tools)
    policy.require(required_scopes(requested, mutation))
    if mutation not in {"none", "isolated-worktree"}:
        raise AuthorizationError("workspace adapter requires read-only or isolated-worktree mutation")
    if requested & {"remote-git", "network", "merge", "deploy"}:
        raise AuthorizationError("remote Git, network, merge, and deploy tools are disabled")
    effective_tools = ["read"] if mutation == "none" else ["read", "edit", "write"]
    base = repository.resolve()
    base_status = subprocess.run(["git", "status", "--porcelain"], cwd=base, capture_output=True, text=True, encoding="utf-8", errors="replace", check=True).stdout
    evidence_dir = evidence_dir.resolve() if evidence_dir else Path(tempfile.mkdtemp(prefix="dev-loop-evidence-")).resolve()
    evidence_dir.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="dev-loop-worktree-") as temp:
        worktree = Path(temp) / "repo"
        subprocess.run(["git", "worktree", "add", "--detach", str(worktree), "HEAD"], cwd=base, capture_output=True, text=True, check=True)
        if base_status.strip():
            base_patch = subprocess.run(["git", "diff", "--binary", "HEAD"], cwd=base, capture_output=True, check=True).stdout
            applied = subprocess.run(["git", "apply", "--index", "-"], cwd=worktree, input=base_patch, capture_output=True, check=False)
            if applied.returncode:
                raise RuntimeError(f"working-state-copy-failed:{applied.stderr.decode('utf-8', errors='replace').strip()}")
        baseline_diff = subprocess.run(["git", "diff", "--binary", "HEAD"], cwd=worktree, capture_output=True, check=True).stdout
        source_head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=base, capture_output=True, text=True, encoding="utf-8", check=True).stdout.strip()
        isolated_head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=worktree, capture_output=True, text=True, encoding="utf-8", check=True).stdout.strip()
        baseline_patch_sha256 = hashlib.sha256(baseline_diff).hexdigest()
        started = time.perf_counter()
        output = ""
        events: list[dict] = []
        command_results: list[dict] = []
        failure: Exception | None = None

        def run_verification_commands() -> None:
            for command in verification_commands or []:
                command_started = time.perf_counter()
                process = subprocess.run(command, cwd=worktree, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=timeout, check=False)
                command_results.append({
                    "argv": command, "returncode": process.returncode,
                    "duration_ms": round((time.perf_counter() - command_started) * 1000, 3),
                    "stdout": process.stdout[-12000:], "stderr": process.stderr[-12000:],
                })

        try:
            if mutation == "none":
                run_verification_commands()
                prompt += "\n\nHOST PREFLIGHT EVIDENCE (observed in this exact isolated snapshot):\n" + json.dumps({
                    "source_repository": str(base), "source_head": source_head,
                    "isolated_head": isolated_head, "baseline_patch_sha256": baseline_patch_sha256,
                    "command_results": command_results,
                }, ensure_ascii=False, indent=2)
            runner_result = runner(prompt, worktree, effective_tools, timeout)
            output, events = runner_result[:2]
            if len(runner_result) == 3:
                command_results.extend(runner_result[2])
            model_output_file = evidence_dir / "model-output.md"
            model_output_file.write_text(output, encoding="utf-8")
            if mutation == "isolated-worktree" and output.startswith("Status: passed"):
                run_verification_commands()
        except Exception as exc:
            failure = exc
        finally:
            subprocess.run(["git", "add", "-N", "--all"], cwd=worktree, capture_output=True, text=True, check=False)
            diff = subprocess.run(["git", "diff", "--binary", "HEAD"], cwd=worktree, capture_output=True, check=True).stdout
            incremental_diff = subprocess.run(["git", "diff", "--binary"], cwd=worktree, capture_output=True, check=True).stdout
            status = subprocess.run(["git", "status", "--short"], cwd=worktree, capture_output=True, text=True, encoding="utf-8", errors="replace", check=True).stdout
            patch_file = evidence_dir / "changes.patch"
            patch_file.write_bytes(diff)
            incremental_patch_file = evidence_dir / "incremental.patch"
            incremental_patch_file.write_bytes(incremental_diff)
            delivered = False
            verification_passed = all(item.get("returncode") == 0 for item in command_results)
            if failure is None and verification_passed and output.startswith("Status: passed") and deliver_changes and mutation == "isolated-worktree" and incremental_diff:
                applied = subprocess.run(["git", "apply", str(incremental_patch_file)], cwd=base, capture_output=True, text=True, encoding="utf-8", errors="replace", check=False)
                if applied.returncode:
                    failure = RuntimeError(f"patch-delivery-failed:{applied.stderr.strip()}")
                else:
                    delivered = True
            evidence = {
                "adapter": "workspace", "tools": effective_tools,
                "authorized_scopes": sorted(policy.authorized_scopes),
                "duration_ms": round((time.perf_counter() - started) * 1000, 3),
                "tool_events": events, "command_results": command_results,
                "source_repository": str(base), "source_head": source_head,
                "isolated_head": isolated_head, "baseline_patch_sha256": baseline_patch_sha256,
                "git_status": status, "patch_file": str(patch_file),
                "patch_sha256": hashlib.sha256(patch_file.read_bytes()).hexdigest(),
                "incremental_patch_file": str(incremental_patch_file),
                "incremental_patch_sha256": hashlib.sha256(incremental_patch_file.read_bytes()).hexdigest(),
                "model_output_file": str(evidence_dir / "model-output.md") if (evidence_dir / "model-output.md").is_file() else None,
                "model_output_sha256": hashlib.sha256((evidence_dir / "model-output.md").read_bytes()).hexdigest() if (evidence_dir / "model-output.md").is_file() else None,
                "verification_passed": verification_passed,
                "delivered": delivered, "failed": failure is not None or not verification_passed,
            }
            (evidence_dir / "execution.json").write_text(json.dumps(evidence, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            subprocess.run(["git", "worktree", "remove", "--force", str(worktree)], cwd=base, capture_output=True, text=True, check=False)
        if mutation == "none" and diff != baseline_diff:
            raise RuntimeError("read-only-worktree-modified")
        if failure is not None:
            raise failure
        if output.startswith("Status: passed") and not evidence["verification_passed"]:
            output = "Status: failed\n\nverification-command-failed\n\n## Raw model output\n\n" + output
        return output, evidence
