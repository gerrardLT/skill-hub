import subprocess
from pathlib import Path

import pytest

from tools.curation.execution_adapters import AuthorizationError, ExecutionPolicy, artifact_adapter, workspace_adapter


def git(repo: Path, *args: str) -> str:
    return subprocess.run(["git", *args], cwd=repo, capture_output=True, text=True, check=True).stdout


def repository(tmp_path: Path) -> Path:
    repo = tmp_path / "repo"
    repo.mkdir()
    git(repo, "init")
    git(repo, "config", "user.email", "test@example.com")
    git(repo, "config", "user.name", "Test")
    (repo / "file.txt").write_text("before\n", encoding="utf-8")
    git(repo, "add", "file.txt")
    git(repo, "commit", "-m", "initial")
    return repo


def test_artifact_adapter_uses_supplied_no_tool_worker() -> None:
    output, evidence = artifact_adapter("prompt", 10, lambda prompt, timeout: f"{prompt}:{timeout}")
    assert output == "prompt:10"
    assert evidence["adapter"] == "artifact"
    assert evidence["tools"] == []


def test_workspace_mutation_requires_explicit_authorization(tmp_path: Path) -> None:
    repo = repository(tmp_path)
    with pytest.raises(AuthorizationError, match="workspace-write"):
        workspace_adapter("change", 10, repository=repo, tools=["read", "write"], mutation="isolated-worktree", policy=ExecutionPolicy())


def test_remote_git_network_merge_and_deploy_require_their_own_scopes(tmp_path: Path) -> None:
    repo = repository(tmp_path)
    with pytest.raises(AuthorizationError) as error:
        workspace_adapter("ship", 10, repository=repo, tools=["remote-git", "network", "merge", "deploy"], mutation="isolated-worktree", policy=ExecutionPolicy(frozenset({"workspace-write"})))
    assert "deploy" in str(error.value)
    assert "remote-git" in str(error.value)


def test_authorized_change_runs_in_isolated_worktree_and_captures_diff(tmp_path: Path) -> None:
    repo = repository(tmp_path)
    seen: list[Path] = []
    def runner(prompt: str, cwd: Path, tools: list[str], timeout: int):
        seen.append(cwd)
        (cwd / "file.txt").write_text("after\n", encoding="utf-8")
        return "Status: passed\nchanged", [{"type": "tool_execution_end", "tool": "write", "is_error": False}]

    output, evidence = workspace_adapter("change", 10, repository=repo, tools=["read", "write"], mutation="isolated-worktree", policy=ExecutionPolicy(frozenset({"workspace-write"})), runner=runner)

    assert output.startswith("Status: passed")
    assert "-before" in evidence["diff"] and "+after" in evidence["diff"]
    assert evidence["tool_events"][0]["tool"] == "write"
    assert (repo / "file.txt").read_text(encoding="utf-8") == "before\n"
    assert seen and not seen[0].exists()
