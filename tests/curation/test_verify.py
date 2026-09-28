import hashlib
import importlib.util
import json
import os
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
INVENTORY = ROOT / "tools" / "curation" / "inventory.py"
VERIFY = ROOT / "tools" / "curation" / "verify.py"
POLICY = ROOT / "curation" / "policy.json"


def run_script(script: Path, *args: str) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    return subprocess.run(
        [sys.executable, str(script), *args],
        cwd=ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        env=env,
    )


def test_policy_preserves_scope_and_hard_failures() -> None:
    policy = json.loads(POLICY.read_text(encoding="utf-8"))

    assert policy["source_root"] == "skills"
    assert policy["immutable"] is True
    assert policy["forbidden_providers"] == ["posthog"]
    assert set(policy["deferred_platform_families"]) == {
        "sentry",
        "datadog",
        "azure",
        "vercel",
        "cloudflare",
        "github-actions",
    }
    assert set(policy["deferred_skill_ids"]) == {
        "agent-observability-eval-pipeline",
        "agent-observability-trace-rca",
        "azure-kubernetes",
        "azure-reliability",
        "dd-apm",
        "dd-logs",
        "dd-monitors",
        "deploy-to-vercel",
        "github-actions-hardening",
        "sentry-create-alert",
        "sentry-debug-issue",
        "sentry-setup-ai-monitoring",
        "sentry-setup-releases",
        "vercel-optimize",
        "wrangler",
    }
    assert "web-perf" not in policy["deferred_skill_ids"]
    assert set(policy["status_values"]) == {
        "passed",
        "failed",
        "needs-input",
        "blocked",
    }
    assert {
        "fabricated-evidence",
        "unauthorized-action",
        "critical-rule-omission",
        "incorrect-gate-pass",
    }.issubset(policy["hard_failures"])
    assert policy["hard_failures_compensable_by_score"] is False


def test_source_verifier_detects_added_changed_and_removed_files(tmp_path: Path) -> None:
    source = tmp_path / "skills"
    source.mkdir()
    (source / "keep.md").write_text("original\n", encoding="utf-8")
    (source / "remove.md").write_text("remove me\n", encoding="utf-8")
    baseline = tmp_path / "baseline.json"

    generated = run_script(
        INVENTORY, "baseline", "--root", str(source), "--output", str(baseline)
    )
    assert generated.returncode == 0, generated.stderr

    (source / "keep.md").write_text("changed\n", encoding="utf-8")
    (source / "remove.md").unlink()
    (source / "added.md").write_text("new\n", encoding="utf-8")

    verified = run_script(
        VERIFY, "source", "--root", str(source), "--baseline", str(baseline)
    )

    assert verified.returncode == 1
    report = json.loads(verified.stdout)
    assert report["added"] == ["added.md"]
    assert report["changed"] == ["keep.md"]
    assert report["removed"] == ["remove.md"]
    assert report["ok"] is False


def test_source_verifier_passes_unchanged_tree(tmp_path: Path) -> None:
    source = tmp_path / "skills"
    source.mkdir()
    (source / "SKILL.md").write_text("---\nname: sample\n---\n", encoding="utf-8")
    baseline = tmp_path / "baseline.json"

    generated = run_script(
        INVENTORY, "baseline", "--root", str(source), "--output", str(baseline)
    )
    assert generated.returncode == 0, generated.stderr

    verified = run_script(
        VERIFY, "source", "--root", str(source), "--baseline", str(baseline)
    )

    assert verified.returncode == 0, verified.stderr
    assert json.loads(verified.stdout) == {
        "added": [],
        "changed": [],
        "ok": True,
        "removed": [],
    }


def test_inventory_gate_rejects_missing_lock_and_forbidden_asset_identity(tmp_path: Path) -> None:
    inventory = tmp_path / "inventory.json"
    inventory.write_text(
        json.dumps(
            {
                "skill_roots": [
                    {"kind": "top-level-skill", "path": "alpha", "name": "alpha"},
                    {
                        "kind": "top-level-skill",
                        "path": "posthog-adapter",
                        "name": "posthog-adapter",
                    },
                ],
                "catalog_entries": [
                    {"skill": "alpha", "scope": "included"},
                ],
            }
        ),
        encoding="utf-8",
    )
    policy = tmp_path / "policy.json"
    policy.write_text(
        json.dumps(
            {
                "forbidden_providers": ["posthog"],
                "deferred_skill_ids": [],
            }
        ),
        encoding="utf-8",
    )
    lock = tmp_path / "skills-lock.json"
    lock.write_text(json.dumps({"skills": {"alpha": {}}}), encoding="utf-8")

    verified = run_script(
        VERIFY,
        "inventory",
        "--inventory",
        str(inventory),
        "--policy",
        str(policy),
        "--lock",
        str(lock),
    )

    assert verified.returncode == 1
    report = json.loads(verified.stdout)
    assert report["ok"] is False
    assert report["missing_lock_entries"] == ["posthog-adapter"]
    assert report["forbidden_asset_identities"] == ["posthog-adapter"]


def test_inventory_gate_allows_historical_text_inside_source_snapshot(tmp_path: Path) -> None:
    inventory = tmp_path / "inventory.json"
    inventory.write_text(
        json.dumps(
            {
                "skill_roots": [
                    {"kind": "top-level-skill", "path": "metrics", "name": "metrics"}
                ],
                "catalog_entries": [
                    {"skill": "metrics", "scope": "included"},
                ],
            }
        ),
        encoding="utf-8",
    )
    policy = tmp_path / "policy.json"
    policy.write_text(
        json.dumps(
            {
                "forbidden_providers": ["posthog"],
                "deferred_skill_ids": [],
            }
        ),
        encoding="utf-8",
    )
    lock = tmp_path / "skills-lock.json"
    lock.write_text(json.dumps({"skills": {"metrics": {}}}), encoding="utf-8")
    source = tmp_path / "skills"
    source.mkdir()
    (source / "history.md").write_text(
        "Historical comparison mentions PostHog only.\n", encoding="utf-8"
    )

    verified = run_script(
        VERIFY,
        "inventory",
        "--inventory",
        str(inventory),
        "--policy",
        str(policy),
        "--lock",
        str(lock),
    )

    assert verified.returncode == 0, verified.stderr
    assert json.loads(verified.stdout)["ok"] is True


def test_phase2_gate_accepts_explicit_unknowns_and_mitigated_blockers(
    tmp_path: Path,
) -> None:
    inventory = tmp_path / "inventory.json"
    inventory.write_text(
        json.dumps(
            {
                "counts": {"catalog_entries": 2, "top_level_skill_roots": 2},
                "catalog_entries": [
                    {
                        "id": "catalog-entry:001",
                        "skill": "alpha",
                        "source": "owner/repo",
                        "scope": "included",
                        "resolution": "resolved",
                    },
                    {
                        "id": "catalog-entry:002",
                        "skill": "platform",
                        "source": "vendor/platform",
                        "scope": "deferred-platform",
                        "resolution": "resolved",
                    },
                ],
                "skill_roots": [
                    {
                        "kind": "top-level-skill",
                        "path": "alpha",
                        "name": "alpha",
                        "skill_path": "alpha/SKILL.md",
                    },
                    {
                        "kind": "top-level-skill",
                        "path": "platform",
                        "name": "platform",
                        "skill_path": "platform/SKILL.md",
                    },
                ],
                "sources": {
                    "owner/repo": {
                        "revision": None,
                        "revision_status": "unknown",
                        "license_paths": [],
                    },
                    "vendor/platform": {
                        "revision": "a" * 40,
                        "revision_status": "verified-from-download-cache",
                        "license_paths": ["LICENSE"],
                    },
                },
            }
        ),
        encoding="utf-8",
    )
    gaps = tmp_path / "gaps.json"
    gaps.write_text(
        json.dumps(
            {
                "gaps": [
                    {
                        "kind": "missing-relative-reference",
                        "severity": "review-required",
                        "source_path": "alpha/SKILL.md",
                        "line": 10,
                        "target": "../shared/SKILL.md",
                    },
                    {
                        "kind": "source-revision-unknown",
                        "severity": "review-required",
                        "source": "owner/repo",
                    },
                    {
                        "kind": "license-unverified-in-snapshot",
                        "severity": "review-required",
                        "source": "owner/repo",
                    },
                ]
            }
        ),
        encoding="utf-8",
    )
    review = tmp_path / "reference-review.json"
    review.write_text(
        json.dumps(
            {
                "source_scan_count": 1,
                "classifications": [
                    {
                        "kind": "missing-relative-reference",
                        "severity": "review-required",
                        "source_path": "alpha/SKILL.md",
                        "line": 10,
                        "target": "../shared/SKILL.md",
                        "classification": "missing-interaction-protocol",
                        "blocking_for_standalone": True,
                        "rationale": "The workflow delegates required behavior.",
                    }
                ],
            }
        ),
        encoding="utf-8",
    )
    dependency_scan = tmp_path / "dependency-scan.json"
    dependency_scan.write_text(
        json.dumps(
            {
                "records": [
                    {"skill": "alpha", "skill_path": "skills/alpha/SKILL.md"},
                    {"skill": "platform", "skill_path": "skills/platform/SKILL.md"},
                ]
            }
        ),
        encoding="utf-8",
    )
    supplements = tmp_path / "supplements"
    supplement_dir = supplements / "owner_repo" / "shared"
    supplement_dir.mkdir(parents=True)
    supplement_file = supplement_dir / "SKILL.md"
    supplement_file.write_text("# Shared\n", encoding="utf-8")
    supplement_hash = hashlib.sha256(supplement_file.read_bytes()).hexdigest()
    (supplement_dir / "supplement.json").write_text(
        json.dumps(
            {
                "source_repository": "owner/repo",
                "source_revision": "b" * 40,
                "reason": "Resolves alpha's required shared/SKILL.md reference.",
                "files": {"SKILL.md": supplement_hash},
            }
        ),
        encoding="utf-8",
    )
    policy = tmp_path / "policy.json"
    policy.write_text(
        json.dumps({"forbidden_providers": ["posthog"]}), encoding="utf-8"
    )

    verified = run_script(
        VERIFY,
        "phase2",
        "--inventory",
        str(inventory),
        "--gaps",
        str(gaps),
        "--reference-review",
        str(review),
        "--dependency-scan",
        str(dependency_scan),
        "--supplements-root",
        str(supplements),
        "--policy",
        str(policy),
    )

    assert verified.returncode == 0, verified.stderr
    report = json.loads(verified.stdout)
    assert report["ok"] is True
    assert report["explicit_unknown_sources"] == ["owner/repo"]
    assert report["unclassified_reference_gaps"] == []
    assert report["unmitigated_included_blockers"] == []
    assert report["missing_dependency_scans"] == []


def test_phase2_gate_rejects_unclassified_unscanned_and_forbidden_content(
    tmp_path: Path,
) -> None:
    inventory = tmp_path / "inventory.json"
    inventory.write_text(
        json.dumps(
            {
                "counts": {"catalog_entries": 1, "top_level_skill_roots": 1},
                "catalog_entries": [
                    {
                        "id": "catalog-entry:001",
                        "skill": "alpha",
                        "source": "owner/repo",
                        "scope": "included",
                        "resolution": "resolved",
                    }
                ],
                "skill_roots": [
                    {
                        "kind": "top-level-skill",
                        "path": "alpha",
                        "name": "alpha",
                        "skill_path": "alpha/SKILL.md",
                    }
                ],
                "sources": {
                    "owner/repo": {
                        "revision": None,
                        "revision_status": "unknown",
                        "license_paths": [],
                    }
                },
            }
        ),
        encoding="utf-8",
    )
    gaps = tmp_path / "gaps.json"
    gaps.write_text(
        json.dumps(
            {
                "gaps": [
                    {
                        "kind": "missing-relative-reference",
                        "severity": "review-required",
                        "source_path": "alpha/SKILL.md",
                        "line": 10,
                        "target": "required.md",
                    }
                ]
            }
        ),
        encoding="utf-8",
    )
    review = tmp_path / "reference-review.json"
    review.write_text(
        json.dumps(
            {
                "source_scan_count": 0,
                "classifications": [
                    {
                        "kind": "missing-relative-reference",
                        "severity": "review-required",
                        "source_path": "alpha/SKILL.md",
                        "line": 11,
                        "target": "different.md",
                        "classification": "missing-required-hydration",
                        "blocking_for_standalone": True,
                        "rationale": "A different reference was reviewed.",
                    }
                ],
            }
        ),
        encoding="utf-8",
    )
    dependency_scan = tmp_path / "dependency-scan.json"
    dependency_scan.write_text(json.dumps({"records": []}), encoding="utf-8")
    supplements = tmp_path / "supplements"
    supplements.mkdir()
    policy = tmp_path / "policy.json"
    policy.write_text(
        json.dumps({"forbidden_providers": ["posthog"]}), encoding="utf-8"
    )
    candidate = tmp_path / "candidate"
    candidate.mkdir()
    (candidate / "contract.json").write_text(
        '{"provider":"posthog"}\n', encoding="utf-8"
    )

    verified = run_script(
        VERIFY,
        "phase2",
        "--inventory",
        str(inventory),
        "--gaps",
        str(gaps),
        "--reference-review",
        str(review),
        "--dependency-scan",
        str(dependency_scan),
        "--supplements-root",
        str(supplements),
        "--policy",
        str(policy),
        "--content-root",
        str(candidate),
    )

    assert verified.returncode == 1
    report = json.loads(verified.stdout)
    assert report["ok"] is False
    assert report["unclassified_reference_gaps"] == [
        "alpha/SKILL.md:10:required.md"
    ]
    assert report["unmitigated_included_blockers"] == [
        "alpha/SKILL.md:10:required.md"
    ]
    assert report["missing_dependency_scans"] == ["alpha/SKILL.md"]
    assert report["forbidden_content_matches"] == [
        str(candidate / "contract.json")
    ]


DOSSIER_SECTIONS = [
    "Problem",
    "When to Use",
    "When Not to Use",
    "Role",
    "Inputs",
    "Outputs",
    "Workflow",
    "Branches",
    "Rules",
    "Exceptions",
    "Dependencies",
    "Permissions and Side Effects",
    "Gates",
    "Open Questions",
    "Unique Value",
    "Reading Coverage",
]


def test_phase3_contract_files_define_complete_dossier_and_unit_schema() -> None:
    dossier_template = ROOT / "curation" / "dossier-template.md"
    unit_schema_path = ROOT / "curation" / "unit-schema.json"

    headings = {
        line[3:].strip()
        for line in dossier_template.read_text(encoding="utf-8").splitlines()
        if line.startswith("## ")
    }
    assert set(DOSSIER_SECTIONS) <= headings

    schema = json.loads(unit_schema_path.read_text(encoding="utf-8"))
    assert schema["type"] == "object"
    assert schema["additionalProperties"] is False
    assert set(schema["required"]) == {
        "id",
        "source_path",
        "origin_line_start",
        "origin_line_end",
        "type",
        "raw_excerpt",
        "meaning",
        "boundary_condition",
        "dependency_skills",
        "candidate_destination",
        "validation_criteria",
        "status",
    }
    assert set(schema["properties"]["type"]["enum"]) == {
        "method",
        "rule",
        "exception",
        "template",
        "example",
        "tool-action",
        "gate",
    }
    assert set(schema["properties"]["status"]["enum"]) == {
        "retain",
        "merge",
        "rewrite",
        "conditionalize",
        "exclude",
        "defer",
    }


def write_complete_dossier(path: Path, name: str) -> None:
    content = [f"# {name} Dossier", ""]
    for section in DOSSIER_SECTIONS:
        content.extend([f"## {section}", f"Documented {section.lower()} for {name}.", ""])
    path.write_text("\n".join(content), encoding="utf-8")


def phase3_supplement_args(tmp_path: Path) -> list[str]:
    reference_review = tmp_path / "reference-review.json"
    reference_review.write_text(
        json.dumps({"classifications": []}), encoding="utf-8"
    )
    supplements_root = tmp_path / "supplements"
    supplements_root.mkdir(exist_ok=True)
    return [
        "--reference-review",
        str(reference_review),
        "--supplements-root",
        str(supplements_root),
    ]


def test_phase3_gate_accepts_complete_source_traceability(tmp_path: Path) -> None:
    skills = tmp_path / "skills"
    alpha = skills / "alpha"
    references = alpha / "references"
    references.mkdir(parents=True)
    (alpha / "SKILL.md").write_text(
        "---\nname: alpha\n---\n# Alpha\nRead [Guide](references/guide.md) and `template.md`.\n",
        encoding="utf-8",
    )
    (alpha / "template.md").write_text("# Template\n", encoding="utf-8")
    (references / "guide.md").write_text("# Guide\nUse carefully.\n", encoding="utf-8")
    scripts = alpha / "scripts"
    scripts.mkdir()
    (scripts / "check.py").write_text("print('check')\n", encoding="utf-8")
    inventory = tmp_path / "inventory.json"
    inventory.write_text(
        json.dumps(
            {
                "catalog_entries": [
                    {
                        "id": "catalog-entry:001",
                        "skill": "alpha",
                        "scope": "included",
                        "resolution": "resolved",
                    }
                ],
                "skill_roots": [
                    {
                        "kind": "top-level-skill",
                        "path": "alpha",
                        "skill_path": "alpha/SKILL.md",
                    }
                ],
            }
        ),
        encoding="utf-8",
    )
    dossiers = tmp_path / "dossiers"
    dossiers.mkdir()
    write_complete_dossier(dossiers / "alpha.md", "alpha")
    units = tmp_path / "units"
    units.mkdir()
    unit = {
        "id": "alpha:unit-001",
        "source_path": "alpha/SKILL.md",
        "origin_line_start": 4,
        "origin_line_end": 4,
        "type": "method",
        "raw_excerpt": "# Alpha",
        "meaning": "Defines the alpha capability.",
        "boundary_condition": "Use only for alpha tasks.",
        "dependency_skills": [],
        "candidate_destination": "slot:alpha",
        "validation_criteria": "The alpha result is observable.",
        "status": "retain",
    }
    (units / "alpha.jsonl").write_text(
        json.dumps(unit) + "\n", encoding="utf-8"
    )
    coverage = tmp_path / "coverage.json"
    coverage.write_text(
        json.dumps(
            {
                "version": 1,
                "sources": {
                    "alpha": {
                        "scope": "included",
                        "dossier": "alpha.md",
                        "units": "alpha.jsonl",
                        "files": [
                            {"path": "alpha/SKILL.md", "status": "read"},
                            {"path": "alpha/references/guide.md", "status": "read"},
                            {"path": "alpha/scripts/check.py", "status": "read"},
                            {"path": "alpha/template.md", "status": "read"},
                        ],
                    }
                },
            }
        ),
        encoding="utf-8",
    )

    verified = run_script(
        VERIFY,
        "phase3",
        "--inventory",
        str(inventory),
        "--skills-root",
        str(skills),
        "--dossiers-root",
        str(dossiers),
        "--units-root",
        str(units),
        "--coverage",
        str(coverage),
        *phase3_supplement_args(tmp_path),
    )

    assert verified.returncode == 0, verified.stderr
    report = json.loads(verified.stdout)
    assert report["ok"] is True
    assert report["included_sources"] == 1
    assert report["validated_units"] == 1
    assert report["missing_dossiers"] == []
    assert report["unread_required_files"] == []
    assert report["source_excerpt_mismatches"] == []


def test_phase3_gate_rejects_unread_backtick_relative_file(tmp_path: Path) -> None:
    skills = tmp_path / "skills"
    alpha = skills / "alpha"
    alpha.mkdir(parents=True)
    (alpha / "SKILL.md").write_text(
        "---\nname: alpha\n---\n# Alpha\nUse `template.md`.\n",
        encoding="utf-8",
    )
    (alpha / "template.md").write_text("# Template\n", encoding="utf-8")
    inventory = tmp_path / "inventory.json"
    inventory.write_text(
        json.dumps(
            {
                "catalog_entries": [
                    {
                        "id": "catalog-entry:001",
                        "skill": "alpha",
                        "scope": "included",
                        "resolution": "resolved",
                    }
                ],
                "skill_roots": [
                    {
                        "kind": "top-level-skill",
                        "path": "alpha",
                        "skill_path": "alpha/SKILL.md",
                    }
                ],
            }
        ),
        encoding="utf-8",
    )
    dossiers = tmp_path / "dossiers"
    dossiers.mkdir()
    write_complete_dossier(dossiers / "alpha.md", "alpha")
    units = tmp_path / "units"
    units.mkdir()
    unit = {
        "id": "alpha:unit-001",
        "source_path": "alpha/SKILL.md",
        "origin_line_start": 4,
        "origin_line_end": 4,
        "type": "method",
        "raw_excerpt": "# Alpha",
        "meaning": "Defines the alpha capability.",
        "boundary_condition": "Use only for alpha tasks.",
        "dependency_skills": [],
        "candidate_destination": "slot:alpha",
        "validation_criteria": "The alpha result is observable.",
        "status": "retain",
    }
    (units / "alpha.jsonl").write_text(json.dumps(unit) + "\n", encoding="utf-8")
    coverage = tmp_path / "coverage.json"
    coverage.write_text(
        json.dumps(
            {
                "version": 1,
                "sources": {
                    "alpha": {
                        "scope": "included",
                        "dossier": "alpha.md",
                        "units": "alpha.jsonl",
                        "files": [{"path": "alpha/SKILL.md", "status": "read"}],
                    }
                },
            }
        ),
        encoding="utf-8",
    )

    verified = run_script(
        VERIFY,
        "phase3",
        "--inventory",
        str(inventory),
        "--skills-root",
        str(skills),
        "--dossiers-root",
        str(dossiers),
        "--units-root",
        str(units),
        "--coverage",
        str(coverage),
        *phase3_supplement_args(tmp_path),
    )

    assert verified.returncode == 1
    report = json.loads(verified.stdout)
    assert report["unread_required_files"] == ["alpha/template.md"]


def run_phase3_with_entry(
    tmp_path: Path,
    entry_text: str,
    extra_files: dict[str, str],
) -> dict[str, object]:
    skills = tmp_path / "skills"
    alpha = skills / "alpha"
    alpha.mkdir(parents=True)
    (alpha / "SKILL.md").write_text(entry_text, encoding="utf-8")
    for relative_path, content in extra_files.items():
        path = skills / relative_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")

    inventory = tmp_path / "inventory.json"
    inventory.write_text(
        json.dumps(
            {
                "catalog_entries": [
                    {
                        "id": "catalog-entry:001",
                        "skill": "alpha",
                        "scope": "included",
                        "resolution": "resolved",
                    }
                ],
                "skill_roots": [
                    {
                        "kind": "top-level-skill",
                        "path": "alpha",
                        "skill_path": "alpha/SKILL.md",
                    }
                ],
            }
        ),
        encoding="utf-8",
    )
    dossiers = tmp_path / "dossiers"
    dossiers.mkdir()
    write_complete_dossier(dossiers / "alpha.md", "alpha")
    units = tmp_path / "units"
    units.mkdir()
    unit = {
        "id": "alpha:unit-001",
        "source_path": "alpha/SKILL.md",
        "origin_line_start": 4,
        "origin_line_end": 4,
        "type": "method",
        "raw_excerpt": "# Alpha",
        "meaning": "Defines the alpha capability.",
        "boundary_condition": "Use only for alpha tasks.",
        "dependency_skills": [],
        "candidate_destination": "slot:alpha",
        "validation_criteria": "The alpha result is observable.",
        "status": "retain",
    }
    (units / "alpha.jsonl").write_text(json.dumps(unit) + "\n", encoding="utf-8")
    coverage = tmp_path / "coverage.json"
    coverage.write_text(
        json.dumps(
            {
                "version": 1,
                "sources": {
                    "alpha": {
                        "scope": "included",
                        "dossier": "alpha.md",
                        "units": "alpha.jsonl",
                        "files": [{"path": "alpha/SKILL.md", "status": "read"}],
                    }
                },
            }
        ),
        encoding="utf-8",
    )

    verified = run_script(
        VERIFY,
        "phase3",
        "--inventory",
        str(inventory),
        "--skills-root",
        str(skills),
        "--dossiers-root",
        str(dossiers),
        "--units-root",
        str(units),
        "--coverage",
        str(coverage),
        *phase3_supplement_args(tmp_path),
    )
    report = json.loads(verified.stdout)
    report["returncode"] = verified.returncode
    return report


def run_phase3_with_supplement(
    tmp_path: Path,
    supplement_coverage: object | None,
    *,
    tamper_file: bool = False,
    source_revision: str = "b" * 40,
    extra_declared_path: str | None = None,
    write_extra_declared_file: bool = True,
    include_null_supplement_coverage: bool = False,
    include_root_manifest: bool = False,
    include_uncovered_matching_manifest: bool = False,
    include_null_coverage_sources: bool = False,
    include_null_source_files: bool = False,
    source_scope: str = "included",
    material_root_name: str = "workshop-facilitation",
) -> subprocess.CompletedProcess[str]:
    skills = tmp_path / "skills"
    alpha = skills / "alpha"
    alpha.mkdir(parents=True)
    (alpha / "SKILL.md").write_text(
        "---\nname: alpha\n---\n# Alpha\n", encoding="utf-8"
    )
    inventory = tmp_path / "inventory.json"
    inventory.write_text(
        json.dumps(
            {
                "catalog_entries": [
                    {
                        "skill": "alpha",
                        "source": "owner/repo",
                        "scope": source_scope,
                        "resolution": "resolved",
                    }
                ],
                "skill_roots": [
                    {
                        "kind": "top-level-skill",
                        "path": "alpha",
                        "skill_path": "alpha/SKILL.md",
                    }
                ],
            }
        ),
        encoding="utf-8",
    )
    dossiers = tmp_path / "dossiers"
    dossiers.mkdir()
    write_complete_dossier(dossiers / "alpha.md", "alpha")
    units = tmp_path / "units"
    units.mkdir()
    unit = {
        "id": "alpha:unit-001",
        "source_path": "alpha/SKILL.md",
        "origin_line_start": 4,
        "origin_line_end": 4,
        "type": "method",
        "raw_excerpt": "# Alpha",
        "meaning": "Defines alpha.",
        "boundary_condition": "Alpha only.",
        "dependency_skills": [],
        "candidate_destination": "slot:alpha",
        "validation_criteria": "Observable result.",
        "status": "retain",
    }
    (units / "alpha.jsonl").write_text(json.dumps(unit) + "\n", encoding="utf-8")
    coverage_entry: dict[str, object] = {
        "scope": source_scope,
        "dossier": "alpha.md",
        "units": "alpha.jsonl",
        "files": [{"path": "alpha/SKILL.md", "status": "read"}],
    }
    if include_null_source_files:
        coverage_entry["files"] = None
    if supplement_coverage is not None or include_null_supplement_coverage:
        coverage_entry["supplements"] = supplement_coverage
    coverage = tmp_path / "coverage.json"
    coverage_sources = None if include_null_coverage_sources else {"alpha": coverage_entry}
    coverage.write_text(
        json.dumps({"version": 1, "sources": coverage_sources}),
        encoding="utf-8",
    )
    review = tmp_path / "reference-review.json"
    review.write_text(
        json.dumps(
            {
                "classifications": [
                    {
                        "kind": "missing-relative-reference",
                        "source_path": "alpha/SKILL.md",
                        "line": 4,
                        "target": f"../{material_root_name}/SKILL.md",
                        "blocking_for_standalone": True,
                    }
                ]
            }
        ),
        encoding="utf-8",
    )
    supplements = tmp_path / "supplements"
    material_root = supplements / "owner_repo" / material_root_name
    examples = material_root / "examples"
    examples.mkdir(parents=True)
    skill_file = material_root / "SKILL.md"
    example_file = examples / "inline-input-flow.md"
    skill_file.write_text("# Workshop\n", encoding="utf-8")
    example_file.write_text("# Inline flow\n", encoding="utf-8")
    manifest = {
        "source_repository": "owner/repo",
        "source_revision": source_revision,
        "reason": "Restores the blocking workshop protocol.",
        "files": {
            "SKILL.md": hashlib.sha256(skill_file.read_bytes()).hexdigest(),
            "examples\\inline-input-flow.md": hashlib.sha256(
                example_file.read_bytes()
            ).hexdigest(),
        },
    }
    if extra_declared_path is not None:
        expected_hash = "0" * 64
        if write_extra_declared_file:
            extra_file = material_root / Path(extra_declared_path)
            extra_file.parent.mkdir(parents=True, exist_ok=True)
            extra_file.write_text("outside supplement root\n", encoding="utf-8")
            expected_hash = hashlib.sha256(extra_file.read_bytes()).hexdigest()
        manifest["files"][extra_declared_path] = expected_hash
    (material_root / "supplement.json").write_text(
        json.dumps(manifest), encoding="utf-8"
    )
    if include_root_manifest:
        (supplements / "supplement.json").write_text(
            json.dumps(
                {
                    "source_repository": "owner/repo",
                    "source_revision": "c" * 40,
                    "reason": "Has no material root.",
                    "files": {},
                }
            ),
            encoding="utf-8",
        )
    if include_uncovered_matching_manifest:
        alternate_root = supplements / "alternate_namespace" / "workshop-facilitation"
        alternate_root.mkdir(parents=True)
        alternate_skill = alternate_root / "SKILL.md"
        alternate_skill.write_text("# Alternate workshop\n", encoding="utf-8")
        (alternate_root / "supplement.json").write_text(
            json.dumps(
                {
                    "source_repository": "owner/repo",
                    "source_revision": "d" * 40,
                    "reason": "Restores the same blocking protocol from another revision.",
                    "files": {
                        "SKILL.md": hashlib.sha256(
                            alternate_skill.read_bytes()
                        ).hexdigest()
                    },
                }
            ),
            encoding="utf-8",
        )
    if tamper_file:
        example_file.write_text("tampered\n", encoding="utf-8")

    return run_script(
        VERIFY,
        "phase3",
        "--inventory",
        str(inventory),
        "--skills-root",
        str(skills),
        "--dossiers-root",
        str(dossiers),
        "--units-root",
        str(units),
        "--coverage",
        str(coverage),
        "--reference-review",
        str(review),
        "--supplements-root",
        str(supplements),
    )


def complete_supplement_coverage() -> list[dict[str, object]]:
    return [
        {
            "source_repository": "owner/repo",
            "source_revision": "b" * 40,
            "root": "workshop-facilitation",
            "files": [
                {"path": "workshop-facilitation/SKILL.md", "status": "read"},
                {
                    "path": "workshop-facilitation/examples/inline-input-flow.md",
                    "status": "read",
                },
            ],
        }
    ]


def test_phase3_requires_coverage_for_blocking_supplement(tmp_path: Path) -> None:
    verified = run_phase3_with_supplement(tmp_path, None)

    assert verified.returncode == 1
    report = json.loads(verified.stdout)
    assert report["missing_required_supplements"] == []
    assert report["missing_supplement_coverage"] == [
        "alpha:owner/repo@" + "b" * 40 + ":workshop-facilitation"
    ]


def test_phase3_treats_null_supplements_as_missing_coverage(tmp_path: Path) -> None:
    verified = run_phase3_with_supplement(
        tmp_path,
        None,
        include_null_supplement_coverage=True,
    )

    assert verified.returncode == 1
    report = json.loads(verified.stdout)
    assert report["missing_required_supplements"] == []
    assert report["missing_supplement_coverage"] == [
        "alpha:owner/repo@" + "b" * 40 + ":workshop-facilitation"
    ]


def test_phase3_treats_null_coverage_sources_as_missing(tmp_path: Path) -> None:
    verified = run_phase3_with_supplement(
        tmp_path,
        complete_supplement_coverage(),
        include_null_coverage_sources=True,
    )

    assert verified.returncode == 1
    report = json.loads(verified.stdout)
    assert report["missing_coverage_sources"] == ["alpha"]
    assert report["missing_supplement_coverage"] == [
        "alpha:owner/repo@" + "b" * 40 + ":workshop-facilitation"
    ]


def test_phase3_treats_null_source_files_as_unread(tmp_path: Path) -> None:
    verified = run_phase3_with_supplement(
        tmp_path,
        complete_supplement_coverage(),
        include_null_source_files=True,
    )

    assert verified.returncode == 1
    report = json.loads(verified.stdout)
    assert report["unread_required_files"] == ["alpha/SKILL.md"]
    assert report["missing_supplement_coverage"] == []
    assert report["unread_supplement_files"] == []


def test_phase3_treats_null_deferred_source_files_as_unread(
    tmp_path: Path,
) -> None:
    verified = run_phase3_with_supplement(
        tmp_path,
        None,
        include_null_source_files=True,
        source_scope="deferred-platform",
    )

    assert verified.returncode == 1
    report = json.loads(verified.stdout)
    assert report["missing_deferred_coverage"] == []
    assert report["unread_required_files"] == ["alpha/SKILL.md"]


def test_phase3_treats_null_supplement_files_as_unread(tmp_path: Path) -> None:
    coverage = complete_supplement_coverage()
    coverage[0]["files"] = None

    verified = run_phase3_with_supplement(tmp_path, coverage)

    assert verified.returncode == 1
    report = json.loads(verified.stdout)
    assert report["missing_supplement_coverage"] == []
    assert report["unread_supplement_files"] == [
        "alpha:workshop-facilitation/SKILL.md",
        "alpha:workshop-facilitation/examples/inline-input-flow.md",
    ]


def test_phase3_accepts_complete_supplement_coverage(tmp_path: Path) -> None:
    verified = run_phase3_with_supplement(tmp_path, complete_supplement_coverage())

    assert verified.returncode == 0, verified.stderr
    report = json.loads(verified.stdout)
    assert report["ok"] is True
    assert report["invalid_supplement_manifests"] == []
    assert report["missing_required_supplements"] == []
    assert report["missing_supplement_coverage"] == []
    assert report["unread_supplement_files"] == []


def test_phase3_rejects_non_string_supplement_coverage_root(tmp_path: Path) -> None:
    coverage = complete_supplement_coverage()
    coverage[0]["root"] = 123
    for item in coverage[0]["files"]:
        item["path"] = item["path"].replace("workshop-facilitation", "123")

    verified = run_phase3_with_supplement(
        tmp_path,
        coverage,
        material_root_name="123",
    )

    assert verified.returncode == 1
    report = json.loads(verified.stdout)
    assert report["missing_supplement_coverage"] == [
        "alpha:owner/repo@" + "b" * 40 + ":123"
    ]


def test_phase3_treats_non_string_supplement_file_path_as_unread(
    tmp_path: Path,
) -> None:
    coverage = complete_supplement_coverage()
    coverage[0]["files"][0]["path"] = 123

    verified = run_phase3_with_supplement(tmp_path, coverage)

    assert verified.returncode == 1
    report = json.loads(verified.stdout)
    assert report["unread_supplement_files"] == [
        "alpha:workshop-facilitation/SKILL.md"
    ]


def test_phase3_rejects_non_string_supplement_file_path_collision(
    tmp_path: Path,
) -> None:
    root = "['a"
    coverage = [
        {
            "source_repository": "owner/repo",
            "source_revision": "b" * 40,
            "root": root,
            "files": [
                {"path": f"{root}/SKILL.md", "status": "read"},
                {
                    "path": f"{root}/examples/inline-input-flow.md",
                    "status": "read",
                },
                {"path": ["a/b"], "status": "read"},
            ],
        }
    ]

    verified = run_phase3_with_supplement(
        tmp_path,
        coverage,
        material_root_name=root,
        extra_declared_path="b']",
    )

    assert verified.returncode == 1
    report = json.loads(verified.stdout)
    assert report["unread_supplement_files"] == ["alpha:['a/b']"]


def test_phase3_accepts_one_fully_covered_matching_manifest(tmp_path: Path) -> None:
    verified = run_phase3_with_supplement(
        tmp_path,
        complete_supplement_coverage(),
        include_uncovered_matching_manifest=True,
    )

    assert verified.returncode == 0, verified.stdout
    report = json.loads(verified.stdout)
    assert report["missing_supplement_coverage"] == []
    assert report["unread_supplement_files"] == []


def test_phase3_rejects_non_hex_supplement_revision(tmp_path: Path) -> None:
    revision = "z" * 40
    coverage = complete_supplement_coverage()
    coverage[0]["source_revision"] = revision

    verified = run_phase3_with_supplement(
        tmp_path, coverage, source_revision=revision
    )

    assert verified.returncode == 1
    report = json.loads(verified.stdout)
    assert report["invalid_supplement_manifests"] == [
        f"owner/repo@{revision}:workshop-facilitation:invalid-metadata"
    ]
    assert report["missing_required_supplements"] == [
        "alpha:owner/repo:workshop-facilitation/SKILL.md"
    ]


def test_phase3_rejects_supplement_path_traversal(tmp_path: Path) -> None:
    coverage = complete_supplement_coverage()
    coverage[0]["files"].append(
        {
            "path": "workshop-facilitation/../outside.md",
            "status": "read",
        }
    )

    verified = run_phase3_with_supplement(
        tmp_path, coverage, extra_declared_path="../outside.md"
    )

    assert verified.returncode == 1
    report = json.loads(verified.stdout)
    assert report["invalid_supplement_manifests"] == [
        "owner/repo@"
        + "b" * 40
        + ":workshop-facilitation:invalid-path:../outside.md"
    ]
    assert report["missing_required_supplements"] == [
        "alpha:owner/repo:workshop-facilitation/SKILL.md"
    ]


def test_phase3_rejects_absolute_supplement_paths(tmp_path: Path) -> None:
    unsafe_paths = [
        "/outside.md",
        "C:\\outside.md",
        "\\\\server\\share\\outside.md",
    ]

    for index, unsafe_path in enumerate(unsafe_paths):
        verified = run_phase3_with_supplement(
            tmp_path / str(index),
            complete_supplement_coverage(),
            extra_declared_path=unsafe_path,
            write_extra_declared_file=False,
        )

        assert verified.returncode == 1
        report = json.loads(verified.stdout)
        normalized = unsafe_path.replace("\\", "/")
        assert report["invalid_supplement_manifests"] == [
            "owner/repo@"
            + "b" * 40
            + f":workshop-facilitation:invalid-path:{normalized}"
        ]
        assert report["missing_required_supplements"] == [
            "alpha:owner/repo:workshop-facilitation/SKILL.md"
        ]


def test_phase3_ignores_invalid_unrelated_supplement_manifest(tmp_path: Path) -> None:
    workspace = tmp_path / "workspace"
    unrelated = workspace / "supplements" / "other_repo" / "unused"
    unrelated.mkdir(parents=True)
    (unrelated / "supplement.json").write_text("not json", encoding="utf-8")

    verified = run_phase3_with_supplement(
        workspace, complete_supplement_coverage()
    )

    assert verified.returncode == 0, verified.stdout
    assert json.loads(verified.stdout)["invalid_supplement_manifests"] == []


def test_phase3_uses_manifest_repository_to_resolve_namespace_collision(
    tmp_path: Path,
) -> None:
    workspace = tmp_path / "workspace"
    colliding = workspace / "supplements" / "owner_repo" / "unrelated"
    colliding.mkdir(parents=True)
    (colliding / "supplement.json").write_text(
        json.dumps(
            {
                "source_repository": "owner_repo",
                "source_revision": "z" * 40,
                "reason": "Belongs to a different repository.",
                "files": {},
            }
        ),
        encoding="utf-8",
    )

    verified = run_phase3_with_supplement(
        workspace, complete_supplement_coverage()
    )

    assert verified.returncode == 0, verified.stdout
    assert json.loads(verified.stdout)["invalid_supplement_manifests"] == []


def test_phase3_ignores_unattributable_manifest_json_shape(tmp_path: Path) -> None:
    workspace = tmp_path / "workspace"
    malformed = workspace / "supplements" / "owner_repo" / "malformed"
    malformed.mkdir(parents=True)
    (malformed / "supplement.json").write_text("[]", encoding="utf-8")

    verified = run_phase3_with_supplement(
        workspace, complete_supplement_coverage()
    )

    assert verified.returncode == 0, verified.stderr
    report = json.loads(verified.stdout)
    assert report["invalid_supplement_manifests"] == []
    assert report["missing_required_supplements"] == []


def test_phase3_ignores_unattributable_manifest_repository_shape(
    tmp_path: Path,
) -> None:
    workspace = tmp_path / "workspace"
    malformed = workspace / "supplements" / "owner_repo" / "malformed"
    malformed.mkdir(parents=True)
    (malformed / "supplement.json").write_text(
        json.dumps(
            {
                "source_repository": ["owner/repo"],
                "source_revision": "e" * 40,
                "reason": "Repository identity is not a string.",
                "files": {},
            }
        ),
        encoding="utf-8",
    )

    verified = run_phase3_with_supplement(
        workspace, complete_supplement_coverage()
    )

    assert verified.returncode == 0, verified.stderr
    report = json.loads(verified.stdout)
    assert report["invalid_supplement_manifests"] == []
    assert report["missing_required_supplements"] == []


def test_phase3_rejects_manifest_without_material_root(tmp_path: Path) -> None:
    verified = run_phase3_with_supplement(
        tmp_path,
        complete_supplement_coverage(),
        include_root_manifest=True,
    )

    assert verified.returncode == 1
    report = json.loads(verified.stdout)
    assert report["invalid_supplement_manifests"] == [
        "owner/repo@" + "c" * 40 + ":.:invalid-metadata"
    ]
    assert report["missing_required_supplements"] == []


def test_phase6_cli_accepts_complete_final_dispositions() -> None:
    verified = run_script(
        VERIFY,
        "phase6",
        "--clusters",
        str(ROOT / "curation" / "clusters.json"),
        "--units-root",
        str(ROOT / "curation" / "units"),
        "--slots-root",
        str(ROOT / "slots"),
        "--review-queue",
        str(ROOT / "curation" / "slot-review-queue.json"),
        "--release-status",
        str(ROOT / "curation" / "slot-release-status.json"),
        "--inventory",
        str(ROOT / "curation" / "inventory.json"),
    )

    assert verified.returncode == 0, verified.stderr
    report = json.loads(verified.stdout)
    assert report["gate"] == "phase-6-slot-coverage-release"
    assert report["cluster_count"] == 88
    assert report["unit_count"] == report["mapped_unit_count"] == 965
    assert report["ok"] is True


def test_phase7_cli_accepts_released_executable_recipe() -> None:
    verified = run_script(
        VERIFY,
        "phase7",
        "--recipes-root",
        str(ROOT / "recipes"),
        "--slots-root",
        str(ROOT / "slots"),
    )

    assert verified.returncode == 0, verified.stderr
    report = json.loads(verified.stdout)
    assert report["gate"] == "phase-7-recipe-composition"
    expected = sorted(
        str(path)
        for path in (ROOT / "recipes").glob("*.json")
        if path.stem not in {"schema", "catalog"}
    )
    assert report["checked"] == expected
    assert report["errors"] == []
    assert report["ok"] is True


def test_phase8_sync_cli_accepts_repository_source_without_local_install() -> None:
    verified = run_script(
        VERIFY,
        "phase8-sync",
        "--audit",
        str(ROOT / "curation" / "dev-loop-sync-audit.json"),
        "--workspace-root",
        str(ROOT),
    )

    assert verified.returncode == 0, verified.stderr
    report = json.loads(verified.stdout)
    assert report["gate"] == "phase-8-dev-loop-source"
    assert report["target_count"] == 2
    assert report["checked_file_count"] == 11
    assert report["errors"] == []
    assert report["ok"] is True


def test_phase3_rejects_tampered_and_unjustified_excluded_supplements(
    tmp_path: Path,
) -> None:
    tampered = run_phase3_with_supplement(
        tmp_path / "tampered", complete_supplement_coverage(), tamper_file=True
    )
    assert tampered.returncode == 1
    assert json.loads(tampered.stdout)["invalid_supplement_manifests"] == [
        "owner/repo@" + "b" * 40 + ":workshop-facilitation:hash-mismatch:workshop-facilitation/examples/inline-input-flow.md"
    ]

    coverage = complete_supplement_coverage()
    coverage[0]["files"][1] = {
        "path": "workshop-facilitation/examples/inline-input-flow.md",
        "status": "excluded",
        "reason": "",
    }
    excluded = run_phase3_with_supplement(tmp_path / "excluded", coverage)
    assert excluded.returncode == 1
    assert json.loads(excluded.stdout)["unread_supplement_files"] == [
        "alpha:workshop-facilitation/examples/inline-input-flow.md"
    ]


def test_phase3_ignores_markdown_targets_inside_fenced_code_blocks(
    tmp_path: Path,
) -> None:
    report = run_phase3_with_entry(
        tmp_path,
        """---
name: alpha
---
# Alpha
Read `body.md`.
```markdown
Ignore `fenced-backtick.md` and [Fenced link](fenced-link.md).
```
   ~~~text
Ignore `tilde-backtick.md` and [Tilde link](tilde-link.md).
   ~~~
""",
        {
            "alpha/body.md": "# Body\n",
            "alpha/fenced-backtick.md": "# Fenced backtick\n",
            "alpha/fenced-link.md": "# Fenced link\n",
            "alpha/tilde-backtick.md": "# Tilde backtick\n",
            "alpha/tilde-link.md": "# Tilde link\n",
        },
    )

    assert report["returncode"] == 1
    assert report["unread_required_files"] == ["alpha/body.md"]


def test_markdown_targets_rejects_backtick_fence_with_backtick_in_info(
    tmp_path: Path,
) -> None:
    markdown = tmp_path / "targets.md"
    markdown.write_text(
        "```markers``` followed by `required.md`\n",
        encoding="utf-8",
    )
    sys.path.insert(0, str(VERIFY.parent))
    try:
        spec = importlib.util.spec_from_file_location("curation_verify", VERIFY)
        assert spec is not None and spec.loader is not None
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
    finally:
        sys.path.pop(0)

    assert module.markdown_targets(markdown) == ["required.md"]


def test_markdown_targets_filters_non_files_and_normalizes_paths(
    tmp_path: Path,
) -> None:
    markdown = tmp_path / "targets.md"
    markdown.write_text(
        """Use `https://example.com/guide.md`, `docs.example.xyz/guide.md`,
`python script.py`, `${placeholder}.md`, `/absolute.md`,
`C:\\absolute\\guide.md`, `assets\\guide.md`, and `config.v2/guide.md`.
Inline ```markers``` do not hide `inline.md`.
~~~markdown
Ignore `after-unclosed-fence.md`.
""",
        encoding="utf-8",
    )
    sys.path.insert(0, str(VERIFY.parent))
    try:
        spec = importlib.util.spec_from_file_location("curation_verify", VERIFY)
        assert spec is not None and spec.loader is not None
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
    finally:
        sys.path.pop(0)

    assert module.markdown_targets(markdown) == [
        "assets/guide.md",
        "config.v2/guide.md",
        "inline.md",
    ]


def test_phase3_backticks_filter_non_files_and_normalize_windows_paths(
    tmp_path: Path,
) -> None:
    outside = tmp_path / "outside.md"
    outside.write_text("# Outside\n", encoding="utf-8")
    report = run_phase3_with_entry(
        tmp_path,
        """---
name: alpha
---
# Alpha
Use `docs.example.xyz/template.md`, `https://example.com/guide.md`,
`python script.py`, `${placeholder}.md`, `/absolute.md`,
`../../outside.md`, and `assets\\guide.md`.
""",
        {
            "alpha/docs.example.xyz/template.md": "# Domain-like local file\n",
            "alpha/assets/guide.md": "# Guide\n",
        },
    )

    assert report["returncode"] == 1
    assert report["unread_required_files"] == ["alpha/assets/guide.md"]


def test_phase3_keeps_ordinary_dotted_directories_as_local_paths(
    tmp_path: Path,
) -> None:
    report = run_phase3_with_entry(
        tmp_path,
        "---\nname: alpha\n---\n# Alpha\nRead `config.v2/guide.md`.\n",
        {"alpha/config.v2/guide.md": "# Guide\n"},
    )

    assert report["returncode"] == 1
    assert report["unread_required_files"] == ["alpha/config.v2/guide.md"]


def test_phase3_recursively_reports_root_markdown_references(tmp_path: Path) -> None:
    report = run_phase3_with_entry(
        tmp_path,
        "---\nname: alpha\n---\n# Alpha\nRead `notes.md`.\n",
        {
            "alpha/notes.md": "Read [Nested](nested.md).\n",
            "alpha/nested.md": "# Nested\n",
        },
    )

    assert report["returncode"] == 1
    assert report["unread_required_files"] == [
        "alpha/nested.md",
        "alpha/notes.md",
    ]


def test_phase3_allows_shared_references_within_skills_root_only(tmp_path: Path) -> None:
    outside = tmp_path / "outside.md"
    outside.write_text("# Outside\n", encoding="utf-8")
    report = run_phase3_with_entry(
        tmp_path,
        """---
name: alpha
---
# Alpha
Read `../beta/template.md` but not `../../outside.md`.
""",
        {"beta/template.md": "# Shared template\n"},
    )

    assert report["returncode"] == 1
    assert report["unread_required_files"] == ["beta/template.md"]


def test_phase3_gate_rejects_incomplete_dossier_units_and_reading_coverage(
    tmp_path: Path,
) -> None:
    skills = tmp_path / "skills"
    alpha = skills / "alpha"
    references = alpha / "references"
    references.mkdir(parents=True)
    (alpha / "SKILL.md").write_text(
        "---\nname: alpha\n---\n# Alpha\nRead [Guide](references/guide.md).\n",
        encoding="utf-8",
    )
    (references / "guide.md").write_text("# Guide\n", encoding="utf-8")
    scripts = alpha / "scripts"
    scripts.mkdir()
    (scripts / "hidden.py").write_text("print('hidden')\n", encoding="utf-8")
    beta = skills / "beta"
    beta.mkdir()
    (beta / "SKILL.md").write_text(
        "---\nname: beta\n---\n# Beta\n", encoding="utf-8"
    )
    inventory = tmp_path / "inventory.json"
    inventory.write_text(
        json.dumps(
            {
                "catalog_entries": [
                    {
                        "id": "catalog-entry:001",
                        "skill": "alpha",
                        "scope": "included",
                        "resolution": "resolved",
                    },
                    {
                        "id": "catalog-entry:002",
                        "skill": "beta",
                        "scope": "included",
                        "resolution": "resolved",
                    },
                ],
                "skill_roots": [
                    {
                        "kind": "top-level-skill",
                        "path": "alpha",
                        "skill_path": "alpha/SKILL.md",
                    },
                    {
                        "kind": "top-level-skill",
                        "path": "beta",
                        "skill_path": "beta/SKILL.md",
                    },
                ],
            }
        ),
        encoding="utf-8",
    )
    dossiers = tmp_path / "dossiers"
    dossiers.mkdir()
    (dossiers / "alpha.md").write_text(
        "# alpha Dossier\n\n## Problem\nOnly one section.\n", encoding="utf-8"
    )
    units = tmp_path / "units"
    units.mkdir()
    invalid_unit = {
        "id": "alpha:unit-001",
        "source_path": "alpha/SKILL.md",
        "origin_line_start": 4,
        "origin_line_end": 4,
        "type": "method",
        "raw_excerpt": "Not the source text",
        "meaning": "Defines alpha.",
        "boundary_condition": "Alpha only.",
        "dependency_skills": [],
        "candidate_destination": "slot:alpha",
        "validation_criteria": "Observable result.",
        "status": "retain",
    }
    (units / "alpha.jsonl").write_text(
        json.dumps(invalid_unit) + "\n", encoding="utf-8"
    )
    coverage = tmp_path / "coverage.json"
    coverage.write_text(
        json.dumps(
            {
                "version": 1,
                "sources": {
                    "alpha": {
                        "scope": "included",
                        "dossier": "alpha.md",
                        "units": "alpha.jsonl",
                        "files": [{"path": "alpha/SKILL.md", "status": "read"}],
                    }
                },
            }
        ),
        encoding="utf-8",
    )

    verified = run_script(
        VERIFY,
        "phase3",
        "--inventory",
        str(inventory),
        "--skills-root",
        str(skills),
        "--dossiers-root",
        str(dossiers),
        "--units-root",
        str(units),
        "--coverage",
        str(coverage),
        *phase3_supplement_args(tmp_path),
    )

    assert verified.returncode == 1
    report = json.loads(verified.stdout)
    assert report["ok"] is False
    assert report["missing_dossiers"] == ["beta"]
    assert report["missing_unit_files"] == ["beta"]
    assert report["missing_coverage_sources"] == ["beta"]
    assert report["invalid_dossiers"][0]["source"] == "alpha"
    assert "When to Use" in report["invalid_dossiers"][0]["missing_sections"]
    assert report["unread_required_files"] == [
        "alpha/references/guide.md",
        "alpha/scripts/hidden.py",
    ]
    assert report["source_excerpt_mismatches"] == ["alpha:unit-001"]


def test_phase3_gate_requires_scope_dossiers_for_deferred_platform_skills(
    tmp_path: Path,
) -> None:
    skills = tmp_path / "skills"
    platform = skills / "platform"
    platform.mkdir(parents=True)
    (platform / "SKILL.md").write_text(
        "---\nname: platform\n---\n# Platform\n", encoding="utf-8"
    )
    inventory = tmp_path / "inventory.json"
    inventory.write_text(
        json.dumps(
            {
                "catalog_entries": [
                    {
                        "id": "catalog-entry:001",
                        "skill": "platform",
                        "scope": "deferred-platform",
                        "resolution": "resolved",
                    }
                ],
                "skill_roots": [
                    {
                        "kind": "top-level-skill",
                        "path": "platform",
                        "skill_path": "platform/SKILL.md",
                    }
                ],
            }
        ),
        encoding="utf-8",
    )
    dossiers = tmp_path / "dossiers"
    dossiers.mkdir()
    units = tmp_path / "units"
    units.mkdir()
    coverage = tmp_path / "coverage.json"
    coverage.write_text(
        json.dumps(
            {
                "version": 1,
                "sources": {
                    "platform": {
                        "scope": "deferred-platform",
                        "dossier": "platform.md",
                        "units": None,
                        "files": [
                            {"path": "platform/SKILL.md", "status": "read"}
                        ],
                    }
                },
            }
        ),
        encoding="utf-8",
    )

    failed = run_script(
        VERIFY,
        "phase3",
        "--inventory",
        str(inventory),
        "--skills-root",
        str(skills),
        "--dossiers-root",
        str(dossiers),
        "--units-root",
        str(units),
        "--coverage",
        str(coverage),
        *phase3_supplement_args(tmp_path),
    )
    assert failed.returncode == 1
    assert json.loads(failed.stdout)["missing_deferred_dossiers"] == ["platform"]

    write_complete_dossier(dossiers / "platform.md", "platform")
    passed = run_script(
        VERIFY,
        "phase3",
        "--inventory",
        str(inventory),
        "--skills-root",
        str(skills),
        "--dossiers-root",
        str(dossiers),
        "--units-root",
        str(units),
        "--coverage",
        str(coverage),
        *phase3_supplement_args(tmp_path),
    )
    assert passed.returncode == 0, passed.stderr
    report = json.loads(passed.stdout)
    assert report["deferred_sources"] == 1
    assert report["validated_units"] == 0


def write_phase4_fixture(tmp_path: Path) -> dict[str, Path]:
    tmp_path.mkdir(parents=True, exist_ok=True)
    inventory = tmp_path / "inventory.json"
    inventory.write_text(
        json.dumps(
            {
                "catalog_entries": [
                    {
                        "skill": "developer-check",
                        "scope": "included",
                        "resolution": "resolved",
                    },
                    {
                        "skill": "qa-only",
                        "scope": "included",
                        "resolution": "resolved",
                    },
                ]
            }
        ),
        encoding="utf-8",
    )
    units = tmp_path / "units"
    units.mkdir()
    (units / "developer-check.jsonl").write_text(
        json.dumps(
            {
                "id": "developer-check:unit-001",
                "responsibility_key": "quality-check",
                "raw_excerpt": "May modify.",
            }
        )
        + "\n",
        encoding="utf-8",
    )
    (units / "qa-only.jsonl").write_text(
        json.dumps(
            {
                "id": "qa-only:unit-001",
                "responsibility_key": "quality-check",
                "raw_excerpt": "Report only.",
            }
        )
        + "\n",
        encoding="utf-8",
    )
    clusters = tmp_path / "clusters.json"
    clusters.write_text(
        json.dumps(
            {
                "clusters": [
                    {
                        "id": "cluster:quality-check",
                        "candidate_responsibility": "Evaluate product quality under an explicit operating mode.",
                        "input_boundary": "A runnable product and a requested testing mode.",
                        "output_boundary": "Evidence-backed findings; repairs only in developer self-check mode.",
                        "upstream_dependencies": [],
                        "downstream_dependencies": [],
                        "unit_ids": [
                            "developer-check:unit-001",
                            "qa-only:unit-001",
                        ],
                    }
                ],
                "relationships": [
                    {
                        "id": "relationship:quality-modes",
                        "type": "conditional-variant",
                        "source_unit_id": "developer-check:unit-001",
                        "target_unit_id": "qa-only:unit-001",
                        "cluster_id": "cluster:quality-check",
                        "condition": {
                            "source": {
                                "execution_mode": "developer-self-check",
                                "may_modify": True,
                                "report_only": False,
                            },
                            "target": {
                                "execution_mode": "independent-qa",
                                "may_modify": False,
                                "report_only": True,
                            },
                        },
                    }
                ],
            }
        ),
        encoding="utf-8",
    )
    decisions = tmp_path / "decisions.jsonl"
    decisions.write_text("", encoding="utf-8")
    return {
        "inventory": inventory,
        "units": units,
        "clusters": clusters,
        "decisions": decisions,
    }


def run_phase4(paths: dict[str, Path]) -> subprocess.CompletedProcess[str]:
    return run_script(
        VERIFY,
        "phase4",
        "--inventory",
        str(paths["inventory"]),
        "--units-root",
        str(paths["units"]),
        "--clusters",
        str(paths["clusters"]),
        "--decisions",
        str(paths["decisions"]),
    )


def read_phase4_json(paths: dict[str, Path], name: str) -> object:
    return json.loads(paths[name].read_text(encoding="utf-8"))


def write_phase4_json(paths: dict[str, Path], name: str, value: object) -> None:
    paths[name].write_text(json.dumps(value), encoding="utf-8")


def test_phase4_gate_accepts_complete_map_and_conditional_boundaries(
    tmp_path: Path,
) -> None:
    paths = write_phase4_fixture(tmp_path)

    verified = run_phase4(paths)

    assert verified.returncode == 0, verified.stderr
    report = json.loads(verified.stdout)
    assert report["ok"] is True
    assert report["included_units"] == 2
    assert report["validated_clusters"] == 1
    assert report["invalid_relationships"] == []
    assert report["unassigned_units"] == []
    assert report["duplicate_unit_assignments"] == []


def test_phase4_accepts_non_permission_conditional_applicability(
    tmp_path: Path,
) -> None:
    paths = write_phase4_fixture(tmp_path)
    data = read_phase4_json(paths, "clusters")
    data["relationships"][0]["condition"] = {
        "source": {"applicability": "Use for live experiments with traffic."},
        "target": {"applicability": "Use for restricted retrospective analysis."},
    }
    write_phase4_json(paths, "clusters", data)

    verified = run_phase4(paths)

    assert verified.returncode == 0, verified.stdout
    assert json.loads(verified.stdout)["invalid_relationships"] == []


def test_phase4_gate_rejects_unassigned_and_duplicate_units(tmp_path: Path) -> None:
    paths = write_phase4_fixture(tmp_path)
    data = read_phase4_json(paths, "clusters")
    data["clusters"].append(
        {
            "id": "cluster:duplicate",
            "candidate_responsibility": "A duplicate assignment fixture.",
            "input_boundary": "A quality finding.",
            "output_boundary": "A reviewed finding.",
            "upstream_dependencies": [],
            "downstream_dependencies": [],
            "unit_ids": ["qa-only:unit-001"],
        }
    )
    data["clusters"][0]["unit_ids"].remove("developer-check:unit-001")
    write_phase4_json(paths, "clusters", data)

    verified = run_phase4(paths)

    assert verified.returncode == 1
    report = json.loads(verified.stdout)
    assert report["unassigned_units"] == ["developer-check:unit-001"]
    assert report["duplicate_unit_assignments"] == ["qa-only:unit-001"]


def test_phase4_gate_accepts_explicit_defer_instead_of_cluster(tmp_path: Path) -> None:
    paths = write_phase4_fixture(tmp_path)
    data = read_phase4_json(paths, "clusters")
    data["clusters"][0]["unit_ids"].remove("qa-only:unit-001")
    data["relationships"] = []
    write_phase4_json(paths, "clusters", data)
    paths["decisions"].write_text(
        json.dumps(
            {
                "id": "decision:defer-qa",
                "action": "defer",
                "unit_ids": ["qa-only:unit-001"],
                "rationale": "Needs an independent execution environment.",
                "potential_loss": "Report-only coverage is unavailable until resumed.",
                "verification_method": "Run the QA-only holdout suite after resumption.",
            }
        )
        + "\n",
        encoding="utf-8",
    )

    verified = run_phase4(paths)

    assert verified.returncode == 0, verified.stdout
    assert json.loads(verified.stdout)["unassigned_units"] == []


def test_phase4_gate_rejects_invalid_relationship_type_and_dangling_references(
    tmp_path: Path,
) -> None:
    paths = write_phase4_fixture(tmp_path)
    data = read_phase4_json(paths, "clusters")
    data["relationships"] = [
        {
            "id": "relationship:bad",
            "type": "overlap",
            "source_unit_id": "missing:unit",
            "target_unit_id": "qa-only:unit-001",
            "cluster_id": "cluster:missing",
        }
    ]
    write_phase4_json(paths, "clusters", data)
    paths["decisions"].write_text(
        json.dumps(
            {
                "id": "decision:dangling",
                "action": "retain",
                "unit_ids": ["missing:decision-unit"],
                "cluster_id": "cluster:missing",
                "rationale": "Fixture.",
            }
        )
        + "\n",
        encoding="utf-8",
    )

    verified = run_phase4(paths)

    assert verified.returncode == 1
    report = json.loads(verified.stdout)
    assert "relationship:bad:invalid-type:overlap" in report["invalid_relationships"]
    assert report["dangling_unit_references"] == [
        "decision:dangling:missing:decision-unit",
        "relationship:bad:missing:unit",
    ]
    assert report["dangling_cluster_references"] == [
        "decision:dangling:cluster:missing",
        "relationship:bad:cluster:missing",
    ]


def test_phase4_gate_rejects_incomplete_cluster_contract(tmp_path: Path) -> None:
    paths = write_phase4_fixture(tmp_path)
    data = read_phase4_json(paths, "clusters")
    cluster = data["clusters"][0]
    cluster["candidate_responsibility"] = ""
    del cluster["input_boundary"]
    cluster["output_boundary"] = ""
    cluster["upstream_dependencies"] = "none"
    del cluster["downstream_dependencies"]
    write_phase4_json(paths, "clusters", data)

    verified = run_phase4(paths)

    assert verified.returncode == 1
    assert json.loads(verified.stdout)["invalid_clusters"] == [
        "cluster:quality-check:invalid-candidate-responsibility",
        "cluster:quality-check:invalid-downstream-dependencies",
        "cluster:quality-check:invalid-input-boundary",
        "cluster:quality-check:invalid-output-boundary",
        "cluster:quality-check:invalid-upstream-dependencies",
    ]


def test_phase4_gate_rejects_unjustified_defer_and_lossy_decisions(
    tmp_path: Path,
) -> None:
    paths = write_phase4_fixture(tmp_path)
    paths["decisions"].write_text(
        "\n".join(
            json.dumps(record)
            for record in [
                {
                    "id": "decision:defer",
                    "action": "defer",
                    "unit_ids": ["qa-only:unit-001"],
                },
                {
                    "id": "decision:exclude",
                    "action": "exclude",
                    "unit_ids": ["qa-only:unit-001"],
                },
                {
                    "id": "decision:merge",
                    "action": "merge",
                    "unit_ids": ["developer-check:unit-001"],
                    "rationale": "Consolidate shared checks.",
                },
            ]
        )
        + "\n",
        encoding="utf-8",
    )

    verified = run_phase4(paths)

    assert verified.returncode == 1
    report = json.loads(verified.stdout)
    assert report["invalid_decisions"] == [
        "decision:defer:missing-potential-loss",
        "decision:defer:missing-rationale",
        "decision:defer:missing-verification-method",
        "decision:exclude:missing-potential-loss",
        "decision:exclude:missing-rationale",
        "decision:exclude:missing-verification-method",
        "decision:merge:invalid-overlap-endpoints",
        "decision:merge:invalid-target-cluster-id",
        "decision:merge:missing-potential-loss",
        "decision:merge:missing-verification-method",
    ]
    assert report["conflicting_unit_dispositions"] == []


def test_phase4_gate_requires_visible_evidenced_conflict_status(tmp_path: Path) -> None:
    paths = write_phase4_fixture(tmp_path)
    data = read_phase4_json(paths, "clusters")
    data["relationships"] = [
        {
            "id": "relationship:conflict",
            "type": "conflict",
            "source_unit_id": "developer-check:unit-001",
            "target_unit_id": "qa-only:unit-001",
            "cluster_id": "cluster:quality-check",
        }
    ]
    write_phase4_json(paths, "clusters", data)

    verified = run_phase4(paths)

    assert verified.returncode == 1
    report = json.loads(verified.stdout)
    assert "relationship:conflict:missing-evidence" in report["invalid_conflicts"]
    assert "relationship:conflict:missing-resolution-status" in report["invalid_conflicts"]


PHASE4_REPORT_KEYS = {
    "conflicting_unit_dispositions",
    "dangling_cluster_references",
    "dangling_unit_references",
    "duplicate_cluster_ids",
    "duplicate_decision_ids",
    "duplicate_relationship_edges",
    "duplicate_relationship_ids",
    "duplicate_unit_assignments",
    "duplicate_unit_ids",
    "included_units",
    "input_errors",
    "invalid_clusters",
    "invalid_conflicts",
    "invalid_decisions",
    "invalid_relationships",
    "jsonl_errors",
    "ok",
    "unassigned_units",
    "unhandled_responsibility_overlaps",
    "validated_clusters",
}


def assert_phase4_failure(result: subprocess.CompletedProcess[str]) -> dict[str, object]:
    assert result.returncode == 1
    assert result.stderr == ""
    report = json.loads(result.stdout)
    assert report["ok"] is False
    assert PHASE4_REPORT_KEYS <= set(report)
    for key, value in report.items():
        if isinstance(value, list):
            assert value == sorted(value)
    return report


def test_phase4_fails_closed_for_missing_malformed_and_wrong_shape_inputs(
    tmp_path: Path,
) -> None:
    cases = [
        ("inventory", None),
        ("inventory", "{"),
        ("inventory", "[]"),
        ("clusters", "{"),
        ("clusters", "[]"),
        ("decisions", "{"),
    ]
    for index, (name, content) in enumerate(cases):
        paths = write_phase4_fixture(tmp_path / str(index))
        if content is None:
            paths[name].unlink()
        else:
            paths[name].write_text(content, encoding="utf-8")
        report = assert_phase4_failure(run_phase4(paths))
        assert report["input_errors"] or report["jsonl_errors"]


def test_phase4_rejects_missing_unit_file_and_duplicate_unit_ids(tmp_path: Path) -> None:
    missing = write_phase4_fixture(tmp_path / "missing")
    (missing["units"] / "qa-only.jsonl").unlink()
    assert assert_phase4_failure(run_phase4(missing))["input_errors"]

    duplicate = write_phase4_fixture(tmp_path / "duplicate")
    (duplicate["units"] / "qa-only.jsonl").write_text(
        json.dumps({"id": "developer-check:unit-001", "responsibility_key": "other"})
        + "\n",
        encoding="utf-8",
    )
    assert assert_phase4_failure(run_phase4(duplicate))["duplicate_unit_ids"] == [
        "developer-check:unit-001"
    ]


def test_phase4_strictly_validates_cluster_identity_members_and_dependencies(
    tmp_path: Path,
) -> None:
    paths = write_phase4_fixture(tmp_path)
    data = read_phase4_json(paths, "clusters")
    data["clusters"].append(
        {
            "id": "cluster:quality-check",
            "candidate_responsibility": " ",
            "input_boundary": "",
            "output_boundary": 1,
            "upstream_dependencies": ["cluster:missing", "cluster:missing"],
            "downstream_dependencies": ["cluster:quality-check", 3],
            "unit_ids": ["", "missing", "missing"],
        }
    )
    data["clusters"][0]["unit_ids"] = []
    write_phase4_json(paths, "clusters", data)

    report = assert_phase4_failure(run_phase4(paths))
    assert report["duplicate_cluster_ids"] == ["cluster:quality-check"]
    assert report["invalid_clusters"]
    assert report["dangling_cluster_references"]
    assert report["dangling_unit_references"]
    assert report["validated_clusters"] == 0


def test_phase4_rejects_invalid_relationships_and_normalized_duplicate_edges(
    tmp_path: Path,
) -> None:
    paths = write_phase4_fixture(tmp_path)
    data = read_phase4_json(paths, "clusters")
    valid = data["relationships"][0]
    data["relationships"] = [
        valid,
        {**valid, "id": "relationship:reverse", "source_unit_id": valid["target_unit_id"], "target_unit_id": valid["source_unit_id"]},
        {**valid, "id": "relationship:self", "target_unit_id": valid["source_unit_id"]},
        {**valid, "id": "relationship:missing", "source_unit_id": ""},
        {**valid, "id": "relationship:dangling", "target_unit_id": "missing"},
        {**valid, "id": valid["id"]},
    ]
    write_phase4_json(paths, "clusters", data)

    report = assert_phase4_failure(run_phase4(paths))
    assert report["duplicate_relationship_ids"] == [valid["id"]]
    assert report["duplicate_relationship_edges"]
    assert report["invalid_relationships"]
    assert report["dangling_unit_references"]


def test_phase4_accepts_all_five_relationship_types(tmp_path: Path) -> None:
    paths = write_phase4_fixture(tmp_path)
    data = read_phase4_json(paths, "clusters")
    base = data["relationships"][0]
    data["relationships"] = [base]
    for relationship_type in ("duplicate", "complementary", "strong-dependency"):
        data["relationships"].append({**base, "id": f"relationship:{relationship_type}", "type": relationship_type, "condition": None})
    conflict = {
        **base,
        "id": "relationship:conflict",
        "type": "conflict",
        "condition": None,
        "resolution_status": "unresolved",
        "source_excerpt": "May modify.",
        "target_excerpt": "Report only.",
        "applicability_conditions": {
            "source": {"execution_mode": "developer-self-check"},
            "target": {"execution_mode": "independent-qa"},
        },
        "evidence": "The source excerpts impose incompatible permissions.",
        "design_case": "Keep both modes visible.",
    }
    data["relationships"].append(conflict)
    write_phase4_json(paths, "clusters", data)
    paths["decisions"].write_text(
        json.dumps({"id": "decision:conflict", "action": "conflict-tracking", "unit_ids": ["developer-check:unit-001", "qa-only:unit-001"], "conflict_id": "relationship:conflict", "resolution_status": "unresolved", "rationale": "Track the incompatible permissions.", "next_design_case": "Preserve explicit modes."}) + "\n",
        encoding="utf-8",
    )

    result = run_phase4(paths)
    assert result.returncode == 0, result.stdout


def test_phase4_validates_conditional_permissions_and_responsibility_overlap(
    tmp_path: Path,
) -> None:
    paths = write_phase4_fixture(tmp_path)
    data = read_phase4_json(paths, "clusters")
    condition = data["relationships"][0]["condition"]
    del condition["source"]["execution_mode"]
    condition["target"]["execution_mode"] = "developer-self-check"
    condition["target"]["may_modify"] = True
    write_phase4_json(paths, "clusters", data)
    assert assert_phase4_failure(run_phase4(paths))["invalid_relationships"]

    overlap = write_phase4_fixture(tmp_path / "overlap")
    data = read_phase4_json(overlap, "clusters")
    data["clusters"] = [
        {**data["clusters"][0], "unit_ids": ["developer-check:unit-001"]},
        {**data["clusters"][0], "id": "cluster:qa", "unit_ids": ["qa-only:unit-001"]},
    ]
    data["relationships"] = []
    write_phase4_json(overlap, "clusters", data)
    assert assert_phase4_failure(run_phase4(overlap))["unhandled_responsibility_overlaps"] == ["quality-check:cluster:qa,cluster:quality-check"]


def test_phase4_accepts_candidate_destination_as_responsibility_key(
    tmp_path: Path,
) -> None:
    paths = write_phase4_fixture(tmp_path)
    for name in ("developer-check", "qa-only"):
        path = paths["units"] / f"{name}.jsonl"
        unit = json.loads(path.read_text(encoding="utf-8"))
        unit["candidate_destination"] = unit.pop("responsibility_key")
        path.write_text(json.dumps(unit) + "\n", encoding="utf-8")

    result = run_phase4(paths)

    assert result.returncode == 0, result.stdout
    assert json.loads(result.stdout)["input_errors"] == []


def test_phase4_rejects_invalid_explicit_or_missing_responsibility_key(
    tmp_path: Path,
) -> None:
    cases = [
        ({"responsibility_key": " ", "candidate_destination": "quality-check"}, "invalid-responsibility-key"),
        ({"responsibility_key": 7, "candidate_destination": "quality-check"}, "invalid-responsibility-key"),
        ({}, "missing-responsibility-key"),
    ]
    for index, (fields, error) in enumerate(cases):
        paths = write_phase4_fixture(tmp_path / str(index))
        path = paths["units"] / "developer-check.jsonl"
        unit = json.loads(path.read_text(encoding="utf-8"))
        unit.pop("responsibility_key", None)
        unit.update(fields)
        path.write_text(json.dumps(unit) + "\n", encoding="utf-8")

        report = assert_phase4_failure(run_phase4(paths))

        assert f"developer-check:unit-001:{error}" in report["input_errors"]


def test_phase4_rejects_missing_blank_or_non_string_raw_excerpt(
    tmp_path: Path,
) -> None:
    for index, raw_excerpt in enumerate((None, " ", 7)):
        paths = write_phase4_fixture(tmp_path / str(index))
        path = paths["units"] / "developer-check.jsonl"
        unit = json.loads(path.read_text(encoding="utf-8"))
        if raw_excerpt is None:
            unit.pop("raw_excerpt")
        else:
            unit["raw_excerpt"] = raw_excerpt
        path.write_text(json.dumps(unit) + "\n", encoding="utf-8")

        report = assert_phase4_failure(run_phase4(paths))

        assert "developer-check:unit-001:invalid-raw-excerpt" in report["input_errors"]


def split_phase4_overlap_clusters(paths: dict[str, Path]) -> dict[str, object]:
    data = read_phase4_json(paths, "clusters")
    data["clusters"] = [
        {**data["clusters"][0], "id": "cluster:developer", "unit_ids": ["developer-check:unit-001"]},
        {**data["clusters"][0], "id": "cluster:qa", "unit_ids": ["qa-only:unit-001"]},
    ]
    return data


def test_phase4_complementary_relationship_handles_cross_cluster_overlap(
    tmp_path: Path,
) -> None:
    paths = write_phase4_fixture(tmp_path)
    data = split_phase4_overlap_clusters(paths)
    data["relationships"] = [{
        "id": "relationship:complementary",
        "type": "complementary",
        "source_unit_id": "developer-check:unit-001",
        "target_unit_id": "qa-only:unit-001",
        "cluster_id": "cluster:developer",
    }]
    write_phase4_json(paths, "clusters", data)

    result = run_phase4(paths)

    assert result.returncode == 0, result.stdout
    assert json.loads(result.stdout)["unhandled_responsibility_overlaps"] == []


def test_phase4_strong_dependency_handles_overlap_when_dependency_gate_is_met(
    tmp_path: Path,
) -> None:
    paths = write_phase4_fixture(tmp_path)
    data = split_phase4_overlap_clusters(paths)
    data["clusters"][0]["downstream_dependencies"] = ["cluster:qa"]
    data["clusters"][1]["upstream_dependencies"] = ["cluster:developer"]
    data["relationships"] = [{
        "id": "relationship:dependency",
        "type": "strong-dependency",
        "source_unit_id": "developer-check:unit-001",
        "target_unit_id": "qa-only:unit-001",
        "cluster_id": "cluster:developer",
    }]
    write_phase4_json(paths, "clusters", data)

    result = run_phase4(paths)

    assert result.returncode == 0, result.stdout
    assert json.loads(result.stdout)["unhandled_responsibility_overlaps"] == []


def test_phase4_invalid_relationships_do_not_handle_overlap(tmp_path: Path) -> None:
    for index, relationship_type in enumerate(("complementary", "strong-dependency")):
        paths = write_phase4_fixture(tmp_path / str(index))
        data = split_phase4_overlap_clusters(paths)
        data["relationships"] = [{
            "id": f"relationship:{relationship_type}",
            "type": relationship_type,
            "source_unit_id": "developer-check:unit-001",
            "target_unit_id": "qa-only:unit-001",
            "cluster_id": "cluster:missing",
        }]
        write_phase4_json(paths, "clusters", data)

        report = assert_phase4_failure(run_phase4(paths))

        assert report["invalid_relationships"]
        assert report["unhandled_responsibility_overlaps"] == [
            "quality-check:cluster:developer,cluster:qa"
        ]


def conflict_fixture(paths: dict[str, Path], status: str, resolution: str | None = None) -> None:
    data = read_phase4_json(paths, "clusters")
    relationship = {
        "id": "relationship:conflict",
        "type": "conflict",
        "source_unit_id": "developer-check:unit-001",
        "target_unit_id": "qa-only:unit-001",
        "cluster_id": "cluster:quality-check",
        "resolution_status": status,
        "source_excerpt": "May modify.",
        "target_excerpt": "Report only.",
        "applicability_conditions": {
            "source": {"execution_mode": "developer-self-check"},
            "target": {"execution_mode": "independent-qa"},
        },
        "evidence": "The permissions differ.",
        "design_case": "Preserve explicit modes.",
    }
    if resolution is not None:
        relationship["resolution"] = resolution
    data["relationships"] = [relationship]
    write_phase4_json(paths, "clusters", data)


def test_phase4_conflicts_require_complete_schema_and_matching_decision(tmp_path: Path) -> None:
    paths = write_phase4_fixture(tmp_path)
    conflict_fixture(paths, "invalid")
    assert assert_phase4_failure(run_phase4(paths))["invalid_conflicts"]

    conflict_fixture(paths, "resolved")
    paths["decisions"].write_text(
        json.dumps({"id": "decision:conflict", "action": "conflict-resolution", "unit_ids": ["developer-check:unit-001", "qa-only:unit-001"], "conflict_id": "relationship:conflict", "resolution_status": "resolved", "resolution": "Apply permissions by execution mode.", "rationale": "Resolve by mode."}) + "\n",
        encoding="utf-8",
    )
    assert assert_phase4_failure(run_phase4(paths))["invalid_conflicts"]

    conflict_fixture(paths, "resolved", "Apply permissions by execution mode.")
    resolved = run_phase4(paths)
    assert resolved.returncode == 0, resolved.stdout
    conflict_fixture(paths, "unresolved")
    paths["decisions"].write_text(
        json.dumps({"id": "decision:conflict", "action": "conflict-tracking", "unit_ids": ["developer-check:unit-001", "qa-only:unit-001"], "conflict_id": "relationship:conflict", "resolution_status": "unresolved", "rationale": "Track until a design case resolves the conflict.", "next_design_case": "Preserve explicit modes."}) + "\n",
        encoding="utf-8",
    )
    unresolved = run_phase4(paths)
    assert unresolved.returncode == 0, unresolved.stdout


def test_phase4_strictly_validates_decisions_and_xor_dispositions(tmp_path: Path) -> None:
    paths = write_phase4_fixture(tmp_path)
    paths["decisions"].write_text(
        "\n".join(json.dumps(item) for item in [
            {"id": "", "action": "retain", "unit_ids": []},
            {"id": "decision:x", "action": "merge", "unit_ids": ["developer-check:unit-001", "developer-check:unit-001"]},
            {"id": "decision:x", "action": "rewrite", "unit_ids": ["missing"], "target_cluster_id": "cluster:missing"},
            {"id": "decision:defer", "action": "defer", "unit_ids": ["qa-only:unit-001"], "rationale": "Later.", "potential_loss": "Coverage.", "verification_method": "Retest."},
        ]) + "\n",
        encoding="utf-8",
    )
    report = assert_phase4_failure(run_phase4(paths))
    assert report["invalid_decisions"]
    assert report["duplicate_decision_ids"] == ["decision:x"]
    assert report["conflicting_unit_dispositions"] == ["qa-only:unit-001"]


def test_phase4_cross_cluster_strong_dependency_requires_boundary_contract(
    tmp_path: Path,
) -> None:
    paths = write_phase4_fixture(tmp_path)
    data = read_phase4_json(paths, "clusters")
    data["clusters"] = [
        {**data["clusters"][0], "id": "cluster:developer", "unit_ids": ["developer-check:unit-001"]},
        {**data["clusters"][0], "id": "cluster:qa", "unit_ids": ["qa-only:unit-001"]},
    ]
    data["relationships"] = [
        {"id": "relationship:dependency", "type": "strong-dependency", "source_unit_id": "developer-check:unit-001", "target_unit_id": "qa-only:unit-001", "cluster_id": "cluster:developer"},
        {"id": "relationship:overlap", "type": "duplicate", "source_unit_id": "developer-check:unit-001", "target_unit_id": "qa-only:unit-001", "cluster_id": "cluster:developer"},
    ]
    write_phase4_json(paths, "clusters", data)
    assert assert_phase4_failure(run_phase4(paths))["invalid_relationships"]

    paths["decisions"].write_text(json.dumps({"id": "decision:boundary", "action": "dependency-boundary", "unit_ids": ["developer-check:unit-001", "qa-only:unit-001"], "source_cluster_id": "cluster:developer", "target_cluster_id": "cluster:qa", "rationale": "Keep execution separate.", "potential_loss": "Coordination overhead.", "verification_method": "Exercise boundary integration."}) + "\n", encoding="utf-8")
    result = run_phase4(paths)
    assert result.returncode == 0, result.stdout


def test_phase4_conflict_decision_binds_exact_endpoints_and_status(tmp_path: Path) -> None:
    paths = write_phase4_fixture(tmp_path)
    conflict_fixture(paths, "resolved", "Use the mode-specific permission.")
    paths["decisions"].write_text(
        json.dumps({"id": "decision:conflict", "action": "conflict-resolution", "unit_ids": ["developer-check:unit-001"], "conflict_id": "relationship:conflict", "resolution_status": "unresolved", "resolution": "Different resolution.", "rationale": "Wrong endpoint and status."}) + "\n",
        encoding="utf-8",
    )

    report = assert_phase4_failure(run_phase4(paths))
    assert any("decision:conflict" in error for error in report["invalid_decisions"])


def test_phase4_unresolved_conflict_requires_tracking_contract(tmp_path: Path) -> None:
    paths = write_phase4_fixture(tmp_path)
    conflict_fixture(paths, "unresolved")
    paths["decisions"].write_text(
        json.dumps({"id": "decision:conflict", "action": "conflict-resolution", "unit_ids": ["developer-check:unit-001", "qa-only:unit-001"], "conflict_id": "relationship:conflict", "resolution_status": "unresolved", "rationale": "Do not resolve yet."}) + "\n",
        encoding="utf-8",
    )

    report = assert_phase4_failure(run_phase4(paths))
    assert any("decision:conflict" in error for error in report["invalid_decisions"])


def test_phase4_overlap_requires_one_record_covering_each_unit_pair(tmp_path: Path) -> None:
    paths = write_phase4_fixture(tmp_path)
    data = read_phase4_json(paths, "clusters")
    data["clusters"] = [
        {**data["clusters"][0], "unit_ids": ["developer-check:unit-001"]},
        {**data["clusters"][0], "id": "cluster:qa", "unit_ids": ["qa-only:unit-001"]},
    ]
    data["relationships"] = []
    write_phase4_json(paths, "clusters", data)
    paths["decisions"].write_text(
        "\n".join(json.dumps(item) for item in [
            {"id": "decision:left", "action": "merge", "unit_ids": ["developer-check:unit-001"], "target_cluster_id": "cluster:quality-check", "rationale": "Keep left.", "potential_loss": "None.", "verification_method": "Review."},
            {"id": "decision:right", "action": "rewrite", "unit_ids": ["qa-only:unit-001"], "target_cluster_id": "cluster:qa", "rationale": "Keep right.", "potential_loss": "None.", "verification_method": "Review."},
        ]) + "\n",
        encoding="utf-8",
    )

    report = assert_phase4_failure(run_phase4(paths))
    assert report["unhandled_responsibility_overlaps"] == ["quality-check:cluster:qa,cluster:quality-check"]


def test_phase4_dependency_boundary_binds_relationship_endpoints(tmp_path: Path) -> None:
    paths = write_phase4_fixture(tmp_path)
    data = read_phase4_json(paths, "clusters")
    data["clusters"] = [
        {**data["clusters"][0], "id": "cluster:developer", "unit_ids": ["developer-check:unit-001"]},
        {**data["clusters"][0], "id": "cluster:qa", "unit_ids": ["qa-only:unit-001"]},
    ]
    data["relationships"] = [{"id": "relationship:dependency", "type": "strong-dependency", "source_unit_id": "developer-check:unit-001", "target_unit_id": "qa-only:unit-001", "cluster_id": "cluster:developer"}]
    write_phase4_json(paths, "clusters", data)
    paths["decisions"].write_text(
        json.dumps({"id": "decision:boundary", "action": "dependency-boundary", "unit_ids": ["developer-check:unit-001"], "source_cluster_id": "cluster:developer", "target_cluster_id": "cluster:qa", "rationale": "Missing target endpoint.", "potential_loss": "Coordination overhead.", "verification_method": "Exercise boundary integration."}) + "\n",
        encoding="utf-8",
    )

    report = assert_phase4_failure(run_phase4(paths))
    assert any("decision:boundary" in error for error in report["invalid_decisions"])
    assert "relationship:dependency:missing-dependency-boundary" in report["invalid_relationships"]


def test_phase4_rejects_orphan_dependency_boundary(tmp_path: Path) -> None:
    paths = write_phase4_fixture(tmp_path)
    data = read_phase4_json(paths, "clusters")
    data["clusters"] = [
        {**data["clusters"][0], "id": "cluster:developer", "unit_ids": ["developer-check:unit-001"]},
        {**data["clusters"][0], "id": "cluster:qa", "unit_ids": ["qa-only:unit-001"]},
    ]
    data["relationships"] = [
        {"id": "relationship:overlap", "type": "duplicate", "source_unit_id": "developer-check:unit-001", "target_unit_id": "qa-only:unit-001", "cluster_id": "cluster:developer"}
    ]
    write_phase4_json(paths, "clusters", data)
    paths["decisions"].write_text(
        json.dumps({"id": "decision:boundary", "action": "dependency-boundary", "unit_ids": ["developer-check:unit-001", "qa-only:unit-001"], "source_cluster_id": "cluster:developer", "target_cluster_id": "cluster:qa", "rationale": "Separate execution.", "potential_loss": "Coordination.", "verification_method": "Integrate."}) + "\n",
        encoding="utf-8",
    )

    report = assert_phase4_failure(run_phase4(paths))
    assert "decision:boundary:orphan-dependency-boundary" in report["invalid_decisions"]


def test_phase4_rejects_orphan_and_single_unit_merge_rewrite(tmp_path: Path) -> None:
    for index, (action, unit_ids) in enumerate((
        ("merge", ["developer-check:unit-001"]),
        ("rewrite", ["developer-check:unit-001", "qa-only:unit-001"]),
    )):
        paths = write_phase4_fixture(tmp_path / str(index))
        data = read_phase4_json(paths, "clusters")
        if len(unit_ids) == 2:
            data["clusters"][0]["unit_ids"] = unit_ids
            data["relationships"] = []
            (paths["units"] / "qa-only.jsonl").write_text(
                json.dumps({"id": "qa-only:unit-001", "responsibility_key": "different", "raw_excerpt": "Report only."}) + "\n",
                encoding="utf-8",
            )
        write_phase4_json(paths, "clusters", data)
        paths["decisions"].write_text(
            json.dumps({"id": f"decision:{action}", "action": action, "unit_ids": unit_ids, "target_cluster_id": "cluster:quality-check", "rationale": "Consolidate.", "potential_loss": "Detail.", "verification_method": "Review."}) + "\n",
            encoding="utf-8",
        )

        report = assert_phase4_failure(run_phase4(paths))
        assert any(error.startswith(f"decision:{action}:") for error in report["invalid_decisions"])


def test_phase4_rejects_conditional_permission_and_role_violations(tmp_path: Path) -> None:
    invalid_conditions = [
        ({"may_modify": False, "report_only": False}, {"may_modify": False, "report_only": False}),
        ({"may_modify": False, "report_only": True}, {"may_modify": True, "report_only": False}),
        ({"may_modify": True, "report_only": False}, {"may_modify": False, "report_only": False}),
    ]
    for index, (source_flags, target_flags) in enumerate(invalid_conditions):
        paths = write_phase4_fixture(tmp_path / str(index))
        data = read_phase4_json(paths, "clusters")
        condition = data["relationships"][0]["condition"]
        condition["source"].update(source_flags)
        condition["target"].update(target_flags)
        write_phase4_json(paths, "clusters", data)

        report = assert_phase4_failure(run_phase4(paths))
        assert "relationship:quality-modes:invalid-condition" in report["invalid_relationships"]


def test_phase4_rejects_forged_conflict_excerpts(tmp_path: Path) -> None:
    paths = write_phase4_fixture(tmp_path)
    conflict_fixture(paths, "unresolved")
    data = read_phase4_json(paths, "clusters")
    data["relationships"][0]["source_excerpt"] = "Forged source text."
    write_phase4_json(paths, "clusters", data)
    paths["decisions"].write_text(
        json.dumps({"id": "decision:conflict", "action": "conflict-tracking", "unit_ids": ["developer-check:unit-001", "qa-only:unit-001"], "conflict_id": "relationship:conflict", "resolution_status": "unresolved", "rationale": "Track it.", "next_design_case": "Retest."}) + "\n",
        encoding="utf-8",
    )

    report = assert_phase4_failure(run_phase4(paths))
    assert "relationship:conflict:source-excerpt-mismatch" in report["invalid_conflicts"]


def test_phase4_rejects_non_structured_or_empty_conflict_applicability(tmp_path: Path) -> None:
    for index, applicability in enumerate(("developer vs qa", 7, {}, {"source": {}, "target": {}})):
        paths = write_phase4_fixture(tmp_path / str(index))
        conflict_fixture(paths, "unresolved")
        data = read_phase4_json(paths, "clusters")
        data["relationships"][0]["applicability_conditions"] = applicability
        write_phase4_json(paths, "clusters", data)
        paths["decisions"].write_text(
            json.dumps({"id": "decision:conflict", "action": "conflict-tracking", "unit_ids": ["developer-check:unit-001", "qa-only:unit-001"], "conflict_id": "relationship:conflict", "resolution_status": "unresolved", "rationale": "Track it.", "next_design_case": "Retest."}) + "\n",
            encoding="utf-8",
        )

        report = assert_phase4_failure(run_phase4(paths))
        assert "relationship:conflict:invalid-applicability-conditions" in report["invalid_conflicts"]


def test_phase4_invalid_records_never_cover_responsibility_overlap(tmp_path: Path) -> None:
    duplicate_edge = write_phase4_fixture(tmp_path / "duplicate-edge")
    data = split_phase4_overlap_clusters(duplicate_edge)
    relationship = {
        "id": "relationship:duplicate-a",
        "type": "duplicate",
        "source_unit_id": "developer-check:unit-001",
        "target_unit_id": "qa-only:unit-001",
        "cluster_id": "cluster:developer",
    }
    data["relationships"] = [
        relationship,
        {**relationship, "id": "relationship:duplicate-b"},
    ]
    write_phase4_json(duplicate_edge, "clusters", data)
    report = assert_phase4_failure(run_phase4(duplicate_edge))
    assert report["duplicate_relationship_edges"]
    assert report["unhandled_responsibility_overlaps"]

    invalid_conflict = write_phase4_fixture(tmp_path / "conflict-decision")
    data = split_phase4_overlap_clusters(invalid_conflict)
    write_phase4_json(invalid_conflict, "clusters", data)
    conflict_fixture(invalid_conflict, "unresolved")
    data = read_phase4_json(invalid_conflict, "clusters")
    data["clusters"] = split_phase4_overlap_clusters(invalid_conflict)["clusters"]
    write_phase4_json(invalid_conflict, "clusters", data)
    bad_decision = {
        "id": "decision:conflict",
        "action": "conflict-tracking",
        "unit_ids": [
            "developer-check:unit-001",
            "qa-only:unit-001",
            "qa-only:unit-001",
        ],
        "conflict_id": "relationship:conflict",
        "resolution_status": "unresolved",
        "rationale": "Track it.",
        "next_design_case": "Retest.",
    }
    invalid_conflict["decisions"].write_text(
        "\n".join(json.dumps(bad_decision) for _ in range(2)) + "\n",
        encoding="utf-8",
    )
    report = assert_phase4_failure(run_phase4(invalid_conflict))
    assert report["duplicate_decision_ids"] == ["decision:conflict"]
    assert report["unhandled_responsibility_overlaps"]

    invalid_merge = write_phase4_fixture(tmp_path / "merge-decision")
    data = split_phase4_overlap_clusters(invalid_merge)
    data["relationships"] = []
    write_phase4_json(invalid_merge, "clusters", data)
    invalid_merge["decisions"].write_text(
        json.dumps({
            "id": " ",
            "action": "merge",
            "unit_ids": ["developer-check:unit-001", "qa-only:unit-001"],
            "target_cluster_id": "cluster:developer",
            "rationale": "Merge duplicates.",
            "potential_loss": "Variant detail.",
            "verification_method": "Run both modes.",
        }) + "\n",
        encoding="utf-8",
    )
    report = assert_phase4_failure(run_phase4(invalid_merge))
    assert report["invalid_decisions"]
    assert report["unhandled_responsibility_overlaps"]

    invalid_boundary = write_phase4_fixture(tmp_path / "boundary-decision")
    data = split_phase4_overlap_clusters(invalid_boundary)
    data["relationships"] = [{
        "id": "relationship:dependency",
        "type": "strong-dependency",
        "source_unit_id": "developer-check:unit-001",
        "target_unit_id": "qa-only:unit-001",
        "cluster_id": "cluster:developer",
    }]
    write_phase4_json(invalid_boundary, "clusters", data)
    boundary = {
        "id": "decision:boundary",
        "action": "dependency-boundary",
        "unit_ids": ["developer-check:unit-001", "qa-only:unit-001"],
        "source_cluster_id": "cluster:developer",
        "target_cluster_id": "cluster:qa",
        "rationale": "Keep dependency explicit.",
        "potential_loss": "Coordination overhead.",
        "verification_method": "Run integration tests.",
    }
    invalid_boundary["decisions"].write_text(
        "\n".join(json.dumps(boundary) for _ in range(2)) + "\n",
        encoding="utf-8",
    )
    report = assert_phase4_failure(run_phase4(invalid_boundary))
    assert report["duplicate_decision_ids"] == ["decision:boundary"]
    assert "relationship:dependency:missing-dependency-boundary" in report["invalid_relationships"]
    assert report["unhandled_responsibility_overlaps"]


def test_phase4_fails_closed_on_unhashable_json_members(tmp_path: Path) -> None:
    cluster_case = write_phase4_fixture(tmp_path / "cluster")
    data = read_phase4_json(cluster_case, "clusters")
    data["clusters"][0]["upstream_dependencies"] = [[]]
    data["clusters"][0]["unit_ids"].append({})
    write_phase4_json(cluster_case, "clusters", data)
    report = assert_phase4_failure(run_phase4(cluster_case))
    assert report["invalid_clusters"]

    decision_case = write_phase4_fixture(tmp_path / "decision")
    decision_case["decisions"].write_text(
        json.dumps({
            "id": "decision:bad-unit",
            "action": "defer",
            "unit_ids": [[]],
            "rationale": "Wait.",
            "potential_loss": "Coverage.",
            "verification_method": "Retest.",
        }) + "\n",
        encoding="utf-8",
    )
    report = assert_phase4_failure(run_phase4(decision_case))
    assert report["invalid_decisions"]

    relationship_case = write_phase4_fixture(tmp_path / "relationship")
    data = read_phase4_json(relationship_case, "clusters")
    data["relationships"][0]["source_unit_id"] = []
    data["relationships"][0]["cluster_id"] = {}
    write_phase4_json(relationship_case, "clusters", data)
    report = assert_phase4_failure(run_phase4(relationship_case))
    assert report["invalid_relationships"]

    condition_case = write_phase4_fixture(tmp_path / "condition")
    data = read_phase4_json(condition_case, "clusters")
    data["relationships"][0]["condition"]["source"]["execution_mode"] = []
    write_phase4_json(condition_case, "clusters", data)
    report = assert_phase4_failure(run_phase4(condition_case))
    assert report["invalid_relationships"]

    conflict_case = write_phase4_fixture(tmp_path / "conflict")
    conflict_fixture(conflict_case, "unresolved")
    data = read_phase4_json(conflict_case, "clusters")
    data["relationships"][0]["resolution_status"] = {}
    write_phase4_json(conflict_case, "clusters", data)
    report = assert_phase4_failure(run_phase4(conflict_case))
    assert report["invalid_conflicts"]


def test_phase4_rejects_inventory_skill_path_escape(tmp_path: Path) -> None:
    unsafe_names = ("../outside", "a/b", "a\\b", "C:\\outside", "\\\\server\\share")
    for index, unsafe_name in enumerate(unsafe_names):
        paths = write_phase4_fixture(tmp_path / str(index))
        inventory = read_phase4_json(paths, "inventory")
        inventory["catalog_entries"][0]["skill"] = unsafe_name
        write_phase4_json(paths, "inventory", inventory)

        report = assert_phase4_failure(run_phase4(paths))

        assert any("invalid-skill" in error for error in report["input_errors"])
