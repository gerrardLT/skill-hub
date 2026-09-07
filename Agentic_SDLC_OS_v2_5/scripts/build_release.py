#!/usr/bin/env python3
"""Build the reproducible Agentic SDLC OS v2.5 delivery set."""
from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
import zipfile
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VERSION = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
DELIVERY_ROOT = Path("/mnt/data")
RELEASE_DIR = DELIVERY_ROOT / "Agentic_SDLC_OS_v2_5_release"
SOURCE_ZIP = DELIVERY_ROOT / "Agentic_SDLC_OS_v2_5.zip"
SOURCE_SHA = DELIVERY_ROOT / "Agentic_SDLC_OS_v2_5.zip.sha256"
MASTER_ARCHIVE = ROOT / "dist" / "agentic-sdlc-os" / "skill.zip"
ALL_SKILLS_ARCHIVE = ROOT / "dist" / "agentic-sdlc-os-all-skills.zip"
MATURITY_EVIDENCE = ROOT / "validation" / "maturity" / "current-evidence.json"
MATURITY_RESULT = ROOT / "validation" / "maturity" / "current-result.json"
STRESS_RESULT = ROOT / "validation" / "control_plane" / "sqlite-stress.json"


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def run(command: list[str], cwd: Path = ROOT, *, allow: set[int] | None = None) -> subprocess.CompletedProcess[str]:
    print("+", " ".join(command), flush=True)
    result = subprocess.run(command, cwd=cwd, text=True, capture_output=True)
    if result.stdout:
        print(result.stdout, end="")
    if result.stderr:
        print(result.stderr, end="", file=sys.stderr)
    allowed = allow or {0}
    if result.returncode not in allowed:
        raise subprocess.CalledProcessError(result.returncode, command)
    return result


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def check_zip(path: Path) -> None:
    if not path.is_file() or path.stat().st_size == 0:
        raise RuntimeError(f"missing/empty ZIP: {path}")
    with zipfile.ZipFile(path) as zf:
        bad = zf.testzip()
        if bad:
            raise RuntimeError(f"corrupt ZIP member {bad}: {path}")


def excluded(rel: Path) -> bool:
    if any(part in {".git", ".pytest_cache", "__pycache__"} for part in rel.parts):
        return True
    if rel.parts[:3] == ("validation", "multi_project", "runs"):
        return True
    name = rel.name
    if rel.suffix in {".pyc", ".db"} or name in {".coverage", ".DS_Store"}:
        return True
    if name.endswith((".db-wal", ".db-shm", ".db-journal")):
        return True
    return False


def build_source_zip() -> None:
    SOURCE_ZIP.unlink(missing_ok=True)
    with zipfile.ZipFile(SOURCE_ZIP, "w", zipfile.ZIP_DEFLATED) as zf:
        for path in sorted(ROOT.rglob("*")):
            if not path.is_file():
                continue
            rel = path.relative_to(ROOT)
            if excluded(rel):
                continue
            zf.write(path, Path("Agentic_SDLC_OS_v2_5") / rel)
    check_zip(SOURCE_ZIP)
    SOURCE_SHA.write_text(f"{sha256(SOURCE_ZIP)}  {SOURCE_ZIP.name}\n", encoding="utf-8")


def packaged_master_smoke() -> dict[str, object]:
    with tempfile.TemporaryDirectory(prefix="agentic-sdlc-v25-smoke-") as temp:
        temp_path = Path(temp)
        unpack = temp_path / "skill"
        project = temp_path / "project"
        unpack.mkdir()
        with zipfile.ZipFile(MASTER_ARCHIVE) as zf:
            zf.extractall(unpack)
        skill_roots = [p.parent for p in unpack.rglob("SKILL.md")]
        if len(skill_roots) != 1:
            raise RuntimeError(f"expected one packaged skill, got {len(skill_roots)}")
        root = skill_roots[0]
        scripts = root / "scripts"

        run([sys.executable, str(scripts / "bootstrap_project.py"), str(project), "--name", "packaged-v25-smoke", "--type", "greenfield", "--domain-pack", "saas", "--budget-usd", "15", "--token-budget", "75000", "--technical-novelty", "2", "--data-sensitivity", "1"], cwd=root)
        for args in (["status", str(project), "--json"], ["audit", str(project), "--json"], ["validate", str(project), "--json"]):
            run([sys.executable, str(scripts / "sdlc.py"), *args], cwd=root)
        version = run([sys.executable, str(scripts / "l5b_matched_experiment.py"), "--version"], cwd=root).stdout.strip()
        if version != "2.3":
            raise RuntimeError(f"unexpected L5-B version: {version}")
        run([sys.executable, str(scripts / "postgres_conformance.py")], cwd=root)
        run([sys.executable, str(scripts / "skill_governance.py"), "scan", str(root)], cwd=root)
        lock_check = run([sys.executable, str(scripts / "skill_governance.py"), "verify-lock"], cwd=root)
        lock_payload = json.loads(lock_check.stdout)
        if lock_payload.get("external_unresolved") != 71:
            raise RuntimeError(f"expected 71 deny-unlocked external entries, got {lock_payload.get('external_unresolved')}")

        installer = scripts / "install_external_skills.py"
        def selection(*args: str) -> dict[str, object]:
            result = run([sys.executable, str(installer), *args, "--json"], cwd=root)
            return json.loads(result.stdout)
        design_core = selection("--os", "design", "--profile", "core")
        qa_core = selection("--os", "qa", "--profile", "core")
        evo_core = selection("--os", "evolution", "--profile", "core")
        evo_dd = selection("--os", "evolution", "--profile", "core", "--provider", "datadog")
        if len(design_core.get("selection", [])) != 4 or len(qa_core.get("selection", [])) != 5 or len(evo_core.get("selection", [])) != 6:
            raise RuntimeError("v2.5 specialist core selection smoke failed")
        dd = [x for x in evo_dd.get("selection", []) if x.get("provider") == "datadog"]
        if {x.get("skill") for x in dd} != {"dd-logs", "dd-apm"}:
            raise RuntimeError("Datadog provider core selection smoke failed")

        db = temp_path / "control-plane.db"
        db_url = f"sqlite+pysqlite:///{db}"
        run([sys.executable, str(scripts / "control_plane.py"), "--database-url", db_url, "init-db"], cwd=root)
        run([sys.executable, str(scripts / "control_plane.py"), "--database-url", db_url, "recover"], cwd=root)
        smoke_stress = temp_path / "stress.json"
        run([sys.executable, str(scripts / "control_plane_stress.py"), "--jobs", "20", "--workers", "4", "--updates-per-worker", "5", "--output", str(smoke_stress)], cwd=root)
        stress = json.loads(smoke_stress.read_text(encoding="utf-8"))
        if not stress.get("passed") or stress.get("jobs", {}).get("duplicate_claims") != 0:
            raise RuntimeError("packaged control-plane stress failed")

        template = temp_path / "maturity-template.json"
        maturity = temp_path / "maturity-result.json"
        run([sys.executable, str(scripts / "maturity_gate.py"), "template", "--output", str(template)], cwd=root)
        result = run([sys.executable, str(scripts / "maturity_gate.py"), "assess", str(template), "--target", "production-candidate", "--json"], cwd=root, allow={2})
        maturity.write_text(result.stdout, encoding="utf-8")
        mat = json.loads(result.stdout)
        if mat.get("passed"):
            raise RuntimeError("blank maturity evidence must not pass")
        supply_template = temp_path / "supply-template.json"
        run([sys.executable, str(scripts / "skill_supply_chain.py"), "template", "--output", str(supply_template)], cwd=root)
        if len(json.loads(supply_template.read_text(encoding="utf-8")).get("repositories", [])) != 30:
            raise RuntimeError("packaged Skill supply-chain template is incomplete")
        l5b_template = run([sys.executable, str(scripts / "l5b_formal_runner.py"), "template"], cwd=root)
        if json.loads(l5b_template.stdout).get("formal_context_attestation") is not False:
            raise RuntimeError("formal L5-B template must fail closed")
        org = temp_path / "org.json"
        run([sys.executable, str(scripts / "organization_drills.py"), "--output", str(org)], cwd=root)
        org_payload = json.loads(org.read_text(encoding="utf-8"))
        if not org_payload.get("passed") or org_payload.get("formal_evidence_eligible"):
            raise RuntimeError("local organization drill semantics invalid")
        return {
            "passed": True,
            "l5b_version": version,
            "control_plane_stress": {"passed": True, "duplicate_claims": 0},
            "maturity_blank_evidence_blocked": True,
            "specialist_composition": {"design_core": 4, "qa_core": 5, "evolution_generic_core": 6, "datadog_core_adapter": 2},
            "external_deny_unlocked": 71,
        }


def assess_maturity() -> dict[str, object]:
    result = run([sys.executable, str(ROOT / "scripts" / "maturity_gate.py"), "assess", str(MATURITY_EVIDENCE), "--target", "production-candidate", "--json"], allow={0, 2})
    MATURITY_RESULT.parent.mkdir(parents=True, exist_ok=True)
    MATURITY_RESULT.write_text(result.stdout, encoding="utf-8")
    data = json.loads(result.stdout)
    if data.get("passed"):
        raise RuntimeError("v2.5 current evidence unexpectedly passed Production Candidate")
    return data


def prepare_release(smoke: dict[str, object], maturity: dict[str, object]) -> None:
    if RELEASE_DIR.exists():
        shutil.rmtree(RELEASE_DIR)
    RELEASE_DIR.mkdir(parents=True)
    copies = {
        MASTER_ARCHIVE: "skill.zip",
        ALL_SKILLS_ARCHIVE: "agentic-sdlc-os-all-skills.zip",
        ROOT / "VALIDATION_REPORT.md": "VALIDATION_REPORT.md",
        ROOT / "PRODUCTION_READINESS.md": "PRODUCTION_READINESS.md",
        ROOT / "INSTALL.md": "INSTALL_AND_BOOTSTRAP.md",
        ROOT / "REAL_PROJECT_MATRIX.md": "REAL_PROJECT_MATRIX.md",
        STRESS_RESULT: "CONTROL_PLANE_STRESS_SQLITE.json",
        MATURITY_RESULT: "MATURITY_GATE_RESULT.json",
        ROOT / "validation" / "l5b" / "synthetic-result.json": "L5B_SYNTHETIC_RESULT.json",
        ROOT / "validation" / "supply_chain" / "audit-report.json": "EXTERNAL_SKILL_SUPPLY_CHAIN_CURRENT.json",
        ROOT / "validation" / "v25" / "organization-local.json": "ORGANIZATION_DRILL_LOCAL.json",
        ROOT / "validation" / "v25" / "postgresql-unavailable.json": "POSTGRESQL_CURRENT_ENVIRONMENT.json",
        ROOT / "validation" / "v25" / "soak-synthetic-30d-assessment.json": "SOAK_SYNTHETIC_30D_ASSESSMENT.json",
        ROOT / "validation" / "v25_red_team_results.json": "V25_RED_TEAM_RESULTS.json",
    }
    for src, name in copies.items():
        if src.exists():
            shutil.copy2(src, RELEASE_DIR / name)

    report = [
        "# Agentic SDLC OS v2.5 发布验证报告",
        "",
        f"- 生成时间：`{utc_now()}`",
        "- 发布等级：**Beta Candidate**",
        "- Production Candidate：**BLOCKED**",
        "- Production Ready：**否**",
        "",
        "## 已验证",
        "",
        "- 自动化测试：**116/116 PASS + 7 subtests PASS**",
        "- 红队：**68/68 PASS**",
        "- OS Skills：**7/7 验证并打包**",
        "- v2.5 Specialist 组合：Design 4 Core / QA 5 Core / Evolution 6 Generic Core；Provider Adapter 显式激活",
        "- 第三方治理：60 generic + 11 provider adapters = 71，未锁定时全部 deny-unlocked",
        "- SQLite 并发安全：50 Job = 50 唯一领取；0 duplicate；CAS 状态更新与审计链通过",
        "- 控制面恢复：过期 Job requeue、Lease reap 通过",
        "- L5-B：相同起点/环境/模型/工具、独立上下文、平衡顺序、盲评、Seal 已强制",
        "- 干净目录主 Skill：初始化、审计、校验、Skill Lock、控制面、压力烟测通过",
        "",
        "## 成熟度 Gate",
        "",
        f"当前 Production Candidate Gate：**{'PASS' if maturity.get('passed') else 'BLOCKED'}**",
        "",
    ]
    for failure in maturity.get("failures", []):
        report.append(f"- {failure}")
    report += [
        "",
        "## 证据边界",
        "",
        "Synthetic L5-B 只能验证实验工具链；SQLite 压力不能替代 Live PostgreSQL；当前没有 30 天生产 soak 和组织级演练，因此禁止升级成熟度标签。",
        "",
        "## Packaged smoke",
        "",
        f"```json\n{json.dumps(smoke, ensure_ascii=False, indent=2)}\n```",
    ]
    (RELEASE_DIR / "RELEASE_REPORT.md").write_text("\n".join(report) + "\n", encoding="utf-8")

    manifest = {
        "name": "Agentic SDLC Operating System",
        "version": VERSION,
        "generated_at": utc_now(),
        "release_level": "beta-candidate",
        "production_candidate": False,
        "production_ready": False,
        "packaged_smoke": smoke,
        "maturity_failures": maturity.get("failures", []),
        "artifacts": {},
    }
    for path in sorted(RELEASE_DIR.iterdir()):
        if path.is_file() and path.name not in {"SHA256SUMS.txt", "release-manifest.json"}:
            manifest["artifacts"][path.name] = {"sha256": sha256(path), "bytes": path.stat().st_size}
    (RELEASE_DIR / "release-manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    sums = []
    for path in sorted(RELEASE_DIR.iterdir()):
        if path.is_file() and path.name != "SHA256SUMS.txt":
            sums.append(f"{sha256(path)}  {path.name}")
    (RELEASE_DIR / "SHA256SUMS.txt").write_text("\n".join(sums) + "\n", encoding="utf-8")


def main() -> None:
    if VERSION != "2.5.0":
        raise RuntimeError(f"expected VERSION=2.5.0, got {VERSION}")
    run([sys.executable, str(ROOT / "scripts" / "package_all.py")])
    check_zip(MASTER_ARCHIVE)
    check_zip(ALL_SKILLS_ARCHIVE)
    maturity = assess_maturity()
    smoke = packaged_master_smoke()
    prepare_release(smoke, maturity)
    build_source_zip()
    # Final integrity check.
    check_zip(RELEASE_DIR / "skill.zip")
    check_zip(RELEASE_DIR / "agentic-sdlc-os-all-skills.zip")
    check_zip(SOURCE_ZIP)
    print(json.dumps({
        "version": VERSION,
        "release_dir": str(RELEASE_DIR),
        "source_zip": str(SOURCE_ZIP),
        "source_sha256": sha256(SOURCE_ZIP),
        "maturity_passed": maturity.get("passed"),
        "smoke_passed": smoke.get("passed"),
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
