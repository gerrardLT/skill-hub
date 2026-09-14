import hashlib
import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
INVENTORY = ROOT / "tools" / "curation" / "inventory.py"


def run_inventory(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(INVENTORY), *args],
        cwd=ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )


def test_baseline_is_deterministic_and_records_file_facts(tmp_path: Path) -> None:
    source = tmp_path / "skills"
    source.mkdir()
    (source / "b.txt").write_bytes(b"beta\n")
    nested = source / "alpha"
    nested.mkdir()
    (nested / "a.md").write_bytes(b"alpha\n")
    git_dir = source / ".git"
    git_dir.mkdir()
    (git_dir / "config").write_bytes(b"ignored\n")
    first = tmp_path / "first.json"
    second = tmp_path / "second.json"

    result_one = run_inventory(
        "baseline", "--root", str(source), "--output", str(first)
    )
    result_two = run_inventory(
        "baseline", "--root", str(source), "--output", str(second)
    )

    assert result_one.returncode == 0, result_one.stderr
    assert result_two.returncode == 0, result_two.stderr
    assert first.read_bytes() == second.read_bytes()
    baseline = json.loads(first.read_text(encoding="utf-8"))
    assert baseline["file_count"] == 2
    assert baseline["total_bytes"] == 11
    assert [entry["path"] for entry in baseline["files"]] == [
        "alpha/a.md",
        "b.txt",
    ]
    assert baseline["files"][0] == {
        "path": "alpha/a.md",
        "bytes": 6,
        "sha256": hashlib.sha256(b"alpha\n").hexdigest(),
    }
    assert baseline["algorithm"] == "sha256"
    assert len(baseline["tree_sha256"]) == 64


def test_inventory_distinguishes_catalog_entries_roots_and_suites(tmp_path: Path) -> None:
    source = tmp_path / "skills"
    alpha = source / "alpha"
    alpha.mkdir(parents=True)
    (alpha / "SKILL.md").write_text(
        "---\nname: alpha\ndescription: Alpha ability\n---\n# Alpha\n",
        encoding="utf-8",
    )
    suite = source / "suite"
    embedded = suite / "child"
    embedded.mkdir(parents=True)
    (suite / "SKILL.md").write_text(
        "---\nname: suite\ndescription: Suite root\n---\n# Suite\n",
        encoding="utf-8",
    )
    (embedded / "SKILL.md").write_text(
        "---\nname: child\ndescription: Child ability\n---\n# Child\n",
        encoding="utf-8",
    )
    catalog = tmp_path / "SKILLS.md"
    catalog.write_text(
        "# Catalog\n\n"
        "## ① 需求域\n\n"
        "| # | 技能名称 | 来源仓库 | 角色职责 | 本地目录状态 |\n"
        "|--:|---|---|---|:---:|\n"
        "| 1 | `alpha` | `owner/repo` | first | present |\n"
        "| 2 | `alpha` | `owner/repo` | duplicate use | present |\n"
        "## ⑤ 交付域\n\n"
        "| # | 技能名称 | 来源仓库 | 角色职责 | 本地目录状态 |\n"
        "|--:|---|---|---|:---:|\n"
        "| 0 | `suite` | `owner/suite` | full suite | present |\n",
        encoding="utf-8",
    )
    output = tmp_path / "inventory.json"
    gaps = tmp_path / "gaps.json"
    lock = tmp_path / "lock.json"

    result = run_inventory(
        "inventory",
        "--root",
        str(source),
        "--catalog",
        str(catalog),
        "--output",
        str(output),
        "--gaps-output",
        str(gaps),
        "--lock-output",
        str(lock),
    )

    assert result.returncode == 0, result.stderr
    inventory = json.loads(output.read_text(encoding="utf-8"))
    assert inventory["counts"] == {
        "catalog_entries": 2,
        "embedded_skill_roots": 1,
        "supplemental_entries": 1,
        "top_level_directories": 2,
        "top_level_skill_roots": 2,
        "unique_catalog_skill_names": 1,
        "all_skill_roots": 3,
    }
    entries = inventory["catalog_entries"]
    assert entries[0]["resolution"] == "resolved"
    assert entries[1]["resolution"] == "duplicate-reference"
    assert entries[1]["duplicate_of"] == entries[0]["id"]
    assert inventory["supplemental_entries"][0]["skill"] == "suite"
    embedded_root = next(root for root in inventory["skill_roots"] if root["name"] == "child")
    assert embedded_root["kind"] == "embedded-skill"
    assert embedded_root["parent_top_level"] == "suite"

    gap_data = json.loads(gaps.read_text(encoding="utf-8"))
    assert {gap["kind"] for gap in gap_data["gaps"]} >= {
        "source-revision-unknown",
        "license-unverified-in-snapshot",
    }
    lock_data = json.loads(lock.read_text(encoding="utf-8"))
    assert set(lock_data["skills"]) == {"alpha", "suite"}
    assert lock_data["skills"]["alpha"]["sourceRevision"] is None


def test_inventory_reports_missing_relative_references(tmp_path: Path) -> None:
    source = tmp_path / "skills"
    alpha = source / "alpha"
    alpha.mkdir(parents=True)
    (alpha / "SKILL.md").write_text(
        "---\nname: alpha\ndescription: Alpha ability\n---\n"
        "Read [present](reference.md) and [missing](missing.md).\n",
        encoding="utf-8",
    )
    (alpha / "reference.md").write_text("present\n", encoding="utf-8")
    catalog = tmp_path / "SKILLS.md"
    catalog.write_text(
        "## Domain\n"
        "| # | 技能名称 | 来源仓库 | 角色职责 | 本地目录状态 |\n"
        "|--:|---|---|---|:---:|\n"
        "| 1 | `alpha` | `owner/repo` | first | present |\n",
        encoding="utf-8",
    )
    output = tmp_path / "inventory.json"
    gaps = tmp_path / "gaps.json"
    lock = tmp_path / "lock.json"

    result = run_inventory(
        "inventory",
        "--root",
        str(source),
        "--catalog",
        str(catalog),
        "--output",
        str(output),
        "--gaps-output",
        str(gaps),
        "--lock-output",
        str(lock),
    )

    assert result.returncode == 0, result.stderr
    gap_data = json.loads(gaps.read_text(encoding="utf-8"))
    missing = [gap for gap in gap_data["gaps"] if gap["kind"] == "missing-relative-reference"]
    assert len(missing) == 1
    assert missing[0]["source_path"] == "alpha/SKILL.md"
    assert missing[0]["target"] == "missing.md"


def test_inventory_uses_verified_source_cache_evidence(tmp_path: Path) -> None:
    source = tmp_path / "skills"
    alpha = source / "alpha"
    alpha.mkdir(parents=True)
    (alpha / "SKILL.md").write_text(
        "---\nname: alpha\ndescription: Alpha ability\n---\n# Alpha\n",
        encoding="utf-8",
    )
    catalog = tmp_path / "SKILLS.md"
    catalog.write_text(
        "## Domain\n"
        "| # | 技能名称 | 来源仓库 | 角色职责 | 本地目录状态 |\n"
        "|--:|---|---|---|:---:|\n"
        "| 1 | `alpha` | `owner/repo` | first | present |\n",
        encoding="utf-8",
    )
    evidence = tmp_path / "source-evidence.json"
    commit = "a" * 40
    evidence.write_text(
        json.dumps(
            {
                "version": 1,
                "records": {
                    "owner_repo": {
                        "uniqueCommit": commit,
                        "commitObjects": [commit],
                        "licensePaths": ["LICENSE"],
                        "evidence": "verified cache object",
                    }
                },
            }
        ),
        encoding="utf-8",
    )
    output = tmp_path / "inventory.json"
    gaps = tmp_path / "gaps.json"
    lock = tmp_path / "lock.json"

    result = run_inventory(
        "inventory",
        "--root",
        str(source),
        "--catalog",
        str(catalog),
        "--source-evidence",
        str(evidence),
        "--output",
        str(output),
        "--gaps-output",
        str(gaps),
        "--lock-output",
        str(lock),
    )

    assert result.returncode == 0, result.stderr
    inventory = json.loads(output.read_text(encoding="utf-8"))
    assert inventory["sources"]["owner/repo"] == {
        "evidence": "verified cache object",
        "license_paths": ["LICENSE"],
        "revision": commit,
        "revision_status": "verified-from-download-cache",
    }
    gap_kinds = {
        gap["kind"] for gap in json.loads(gaps.read_text(encoding="utf-8"))["gaps"]
    }
    assert "source-revision-unknown" not in gap_kinds
    assert "license-unverified-in-snapshot" not in gap_kinds
    lock_data = json.loads(lock.read_text(encoding="utf-8"))
    assert lock_data["skills"]["alpha"]["sourceRevision"] == commit


def test_inventory_marks_deferred_and_unlisted_top_level_skills(tmp_path: Path) -> None:
    source = tmp_path / "skills"
    alpha = source / "alpha"
    alpha.mkdir(parents=True)
    (alpha / "SKILL.md").write_text(
        "---\nname: alpha\ndescription: Deferred ability\n---\n# Alpha\n",
        encoding="utf-8",
    )
    extra = source / "extra"
    extra.mkdir()
    (extra / "SKILL.md").write_text(
        "---\nname: extra\ndescription: Extra local ability\n---\n# Extra\n",
        encoding="utf-8",
    )
    catalog = tmp_path / "SKILLS.md"
    catalog.write_text(
        "## Domain\n"
        "| # | 技能名称 | 来源仓库 | 角色职责 | 本地目录状态 |\n"
        "|--:|---|---|---|:---:|\n"
        "| 1 | `alpha` | `owner/repo` | first | present |\n",
        encoding="utf-8",
    )
    policy = tmp_path / "policy.json"
    policy.write_text(
        json.dumps({"deferred_skill_ids": ["alpha"]}),
        encoding="utf-8",
    )
    output = tmp_path / "inventory.json"
    gaps = tmp_path / "gaps.json"
    lock = tmp_path / "lock.json"

    result = run_inventory(
        "inventory",
        "--root",
        str(source),
        "--catalog",
        str(catalog),
        "--policy",
        str(policy),
        "--output",
        str(output),
        "--gaps-output",
        str(gaps),
        "--lock-output",
        str(lock),
    )

    assert result.returncode == 0, result.stderr
    inventory = json.loads(output.read_text(encoding="utf-8"))
    assert inventory["catalog_entries"][0]["scope"] == "deferred-platform"
    assert inventory["unlisted_top_level_roots"] == ["extra"]
    assert set(json.loads(lock.read_text(encoding="utf-8"))["skills"]) == {
        "alpha",
        "extra",
    }
