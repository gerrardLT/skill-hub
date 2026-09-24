import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
VERIFY = ROOT / "tools" / "curation" / "dev_loop_sync_verify.py"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_audit(tmp_path: Path) -> tuple[Path, Path, Path]:
    workspace = tmp_path / "workspace"
    source = workspace / "dev-loop"
    plugin = tmp_path / "plugin"
    standalone = tmp_path / "standalone"
    (source / "skills" / "dev-loop").mkdir(parents=True)
    plugin.mkdir()
    standalone.mkdir()
    (source / "README.md").write_text("plugin\n", encoding="utf-8")
    (source / "skills" / "dev-loop" / "SKILL.md").write_text(
        "skill\n", encoding="utf-8"
    )
    (plugin / "README.md").write_text("plugin\n", encoding="utf-8")
    (standalone / "SKILL.md").write_text("skill\n", encoding="utf-8")
    audit = {
        "audit_id": "fixture",
        "generated_at": "2026-09-14",
        "source_root": "dev-loop",
        "targets": [
            {
                "id": "plugin-cache",
                "root": str(plugin),
                "files": [
                    {
                        "source_path": "README.md",
                        "target_path": "README.md",
                        "bytes": (source / "README.md").stat().st_size,
                        "sha256": digest(source / "README.md"),
                    }
                ],
            },
            {
                "id": "standalone-skill",
                "root": str(standalone),
                "files": [
                    {
                        "source_path": "skills/dev-loop/SKILL.md",
                        "target_path": "SKILL.md",
                        "bytes": (source / "skills" / "dev-loop" / "SKILL.md").stat().st_size,
                        "sha256": digest(
                            source / "skills" / "dev-loop" / "SKILL.md"
                        ),
                    }
                ],
            },
        ],
    }
    audit_path = workspace / "curation" / "dev-loop-sync-audit.json"
    audit_path.parent.mkdir()
    audit_path.write_text(json.dumps(audit), encoding="utf-8")
    return audit_path, workspace, standalone


def run_verify(audit: Path, workspace: Path) -> tuple[subprocess.CompletedProcess, dict]:
    env = os.environ.copy()
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    result = subprocess.run(
        [
            sys.executable,
            str(VERIFY),
            "--audit",
            str(audit),
            "--workspace-root",
            str(workspace),
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        env=env,
    )
    return result, json.loads(result.stdout)


def test_accepts_identical_declared_trees(tmp_path: Path) -> None:
    audit, workspace, _ = write_audit(tmp_path)

    result, report = run_verify(audit, workspace)

    assert result.returncode == 0, report
    assert report == {
        "checked_file_count": 2,
        "errors": [],
        "gate": "phase-8-dev-loop-sync",
        "ok": True,
        "target_count": 2,
    }


def test_source_only_checks_repository_without_local_install(tmp_path: Path) -> None:
    audit, workspace, _ = write_audit(tmp_path)
    data = json.loads(audit.read_text(encoding="utf-8"))
    for target in data["targets"]:
        target["root"] = str(tmp_path / "missing" / target["id"])
    audit.write_text(json.dumps(data), encoding="utf-8")

    report = __import__("tools.curation.dev_loop_sync_verify", fromlist=["verify_sync"]).verify_sync(audit, workspace, source_only=True)

    assert report["ok"] is True
    assert report["gate"] == "phase-8-dev-loop-source"
    assert report["checked_file_count"] == 2


def test_rejects_changed_target(tmp_path: Path) -> None:
    audit, workspace, standalone = write_audit(tmp_path)
    (standalone / "SKILL.md").write_text("changed\n", encoding="utf-8")

    result, report = run_verify(audit, workspace)

    assert result.returncode == 1
    assert "target-hash-mismatch" in {item["code"] for item in report["errors"]}


def test_rejects_extra_target_file(tmp_path: Path) -> None:
    audit, workspace, standalone = write_audit(tmp_path)
    (standalone / "extra.txt").write_text("extra\n", encoding="utf-8")

    result, report = run_verify(audit, workspace)

    assert result.returncode == 1
    assert "extra-target-file" in {item["code"] for item in report["errors"]}
