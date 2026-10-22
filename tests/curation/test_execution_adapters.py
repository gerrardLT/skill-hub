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


def test_existing_patch_is_copied_as_baseline_for_incremental_fix(tmp_path: Path) -> None:
    repo = repository(tmp_path)
    (repo / "file.txt").write_text("first patch\n", encoding="utf-8")
    def runner(prompt: str, cwd: Path, tools: list[str], timeout: int):
        assert (cwd / "file.txt").read_text(encoding="utf-8") == "first patch\n"
        (cwd / "file.txt").write_text("second patch\n", encoding="utf-8")
        return "Status: passed", []
    _, evidence = workspace_adapter("change", 10, repository=repo, tools=["write"], mutation="isolated-worktree", policy=ExecutionPolicy(frozenset({"workspace-write"})), runner=runner, evidence_dir=tmp_path / "incremental", deliver_changes=True)
    assert evidence["delivered"] is True
    assert (repo / "file.txt").read_text(encoding="utf-8") == "second patch\n"
    assert b"second patch" in Path(evidence["patch_file"]).read_bytes()
    incremental = Path(evidence["incremental_patch_file"]).read_bytes()
    assert b"first patch" in incremental and b"second patch" in incremental


def test_authorized_change_runs_in_isolated_worktree_and_captures_diff(tmp_path: Path) -> None:
    repo = repository(tmp_path)
    seen: list[Path] = []
    def runner(prompt: str, cwd: Path, tools: list[str], timeout: int):
        seen.append(cwd)
        (cwd / "file.txt").write_text("after\n", encoding="utf-8")
        return "Status: passed\nchanged", [{"type": "tool_execution_end", "tool": "write", "is_error": False}]

    evidence_dir = tmp_path / "evidence"
    output, evidence = workspace_adapter("change", 10, repository=repo, tools=["read", "write"], mutation="isolated-worktree", policy=ExecutionPolicy(frozenset({"workspace-write"})), runner=runner, evidence_dir=evidence_dir)

    assert output.startswith("Status: passed")
    patch = Path(evidence["patch_file"]).read_text(encoding="utf-8")
    assert "-before" in patch and "+after" in patch
    assert evidence["tool_events"][0]["tool"] == "write"
    assert evidence["tools"] == ["read", "edit", "write"]
    assert (evidence_dir / "execution.json").is_file()
    assert (repo / "file.txt").read_text(encoding="utf-8") == "before\n"
    assert seen and not seen[0].exists()


def test_authorized_change_can_be_delivered_to_clean_repository(tmp_path: Path) -> None:
    repo = repository(tmp_path)
    def runner(prompt: str, cwd: Path, tools: list[str], timeout: int):
        (cwd / "file.txt").write_text("delivered\n", encoding="utf-8")
        return "Status: passed", []
    _, evidence = workspace_adapter("change", 10, repository=repo, tools=["write"], mutation="isolated-worktree", policy=ExecutionPolicy(frozenset({"workspace-write"})), runner=runner, evidence_dir=tmp_path / "delivery", deliver_changes=True)
    assert evidence["delivered"] is True
    assert (repo / "file.txt").read_text(encoding="utf-8") == "delivered\n"


def test_failed_run_keeps_patch_and_execution_evidence(tmp_path: Path) -> None:
    repo = repository(tmp_path)
    evidence_dir = tmp_path / "failed-evidence"
    def runner(prompt: str, cwd: Path, tools: list[str], timeout: int):
        (cwd / "file.txt").write_text("failed change\n", encoding="utf-8")
        raise RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        workspace_adapter("change", 10, repository=repo, tools=["write"], mutation="isolated-worktree", policy=ExecutionPolicy(frozenset({"workspace-write"})), runner=runner, evidence_dir=evidence_dir)
    assert "failed change" in (evidence_dir / "changes.patch").read_text(encoding="utf-8")
    assert (evidence_dir / "execution.json").is_file()


def test_read_only_run_detects_source_mutation(tmp_path: Path) -> None:
    repo = repository(tmp_path)
    def runner(prompt: str, cwd: Path, tools: list[str], timeout: int):
        assert tools == ["read"]
        (cwd / "file.txt").write_text("illegal\n", encoding="utf-8")
        return "Status: passed", []
    with pytest.raises(RuntimeError, match="read-only-worktree-modified"):
        workspace_adapter("qa", 10, repository=repo, tools=["read", "bash"], mutation="none", policy=ExecutionPolicy(), runner=runner, evidence_dir=tmp_path / "qa-evidence")
