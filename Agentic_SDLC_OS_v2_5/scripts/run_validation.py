#!/usr/bin/env python3
"""Run the reproducible Agentic SDLC OS v2.5 validation matrix."""
from __future__ import annotations

import importlib.util
import json
import os
import re
import signal
import subprocess
import sys
import tempfile
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
CLI = ROOT / "skills" / "agentic-sdlc-os" / "scripts" / "sdlc.py"
LEGACY_L5 = ROOT / "scripts" / "l5_experiment.py"
L5B = ROOT / "scripts" / "l5b_matched_experiment.py"
PILOT = ROOT / "validation" / "l5" / "pilots" / "venue-reservation"
PILOT_VERIFY = PILOT / "scripts" / "verify_pilot.py"
PILOT_RESULT = PILOT / "reports" / "pilot-verification.json"
RESULTS_DIR = ROOT / "validation" / "results"
LATEST_JSON = RESULTS_DIR / "latest.json"
REPORT_MD = ROOT / "VALIDATION_REPORT.md"


def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def run(command: list[str], *, cwd: Path = ROOT, timeout_seconds: int = 300) -> dict[str, Any]:
    """Run nested validators without pipe-inheritance deadlocks."""
    print("+", " ".join(command), file=sys.stderr, flush=True)
    started = time.monotonic()
    with tempfile.TemporaryDirectory(prefix="sdlc-validation-command-") as temp:
        stdout_path = Path(temp) / "stdout.log"
        stderr_path = Path(temp) / "stderr.log"
        with stdout_path.open("w", encoding="utf-8") as stdout, stderr_path.open("w", encoding="utf-8") as stderr:
            process = subprocess.Popen(
                command,
                cwd=cwd,
                text=True,
                stdout=stdout,
                stderr=stderr,
                start_new_session=True,
            )
            timed_out = False
            try:
                returncode = process.wait(timeout=timeout_seconds)
            except subprocess.TimeoutExpired:
                timed_out = True
                os.killpg(process.pid, signal.SIGKILL)
                returncode = process.wait()
        stdout_text = stdout_path.read_text(encoding="utf-8", errors="replace")
        stderr_text = stderr_path.read_text(encoding="utf-8", errors="replace")
    duration = round(time.monotonic() - started, 3)
    print(f"  -> {returncode} ({duration}s){' TIMEOUT' if timed_out else ''}", file=sys.stderr, flush=True)
    return {
        "command": command,
        "returncode": returncode,
        "passed": returncode == 0 and not timed_out,
        "timed_out": timed_out,
        "duration_seconds": duration,
        "stdout_tail": stdout_text[-6000:],
        "stderr_tail": stderr_text[-6000:],
    }


def load_json(path: Path, default: Any = None) -> Any:
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def load_cli():
    spec = importlib.util.spec_from_file_location("agentic_sdlc_cli", CLI)
    if spec is None or spec.loader is None:
        raise RuntimeError("Cannot load Agentic SDLC CLI")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def parse_pytest(output: str) -> dict[str, int | None]:
    tests = re.search(r"(\d+) passed", output)
    subtests = re.search(r"(\d+) subtests passed", output)
    return {
        "tests": int(tests.group(1)) if tests else None,
        "subtests": int(subtests.group(1)) if subtests else 0,
    }


def router_metrics(module: Any, benchmark_path: Path, current_os: str) -> dict[str, Any]:
    cases = load_json(benchmark_path, [])
    routing = load_json(ROOT / "manifest" / "os-routing.json", {})
    state = {
        "current_os": current_os,
        "os_states": {name: {"stage": stages[0]} for name, stages in routing["os_stages"].items()},
    }
    auto_routes = 0
    correct_auto_routes = 0
    correct_fallbacks = 0
    unsafe_routes: list[dict[str, Any]] = []
    abstentions: list[dict[str, Any]] = []
    for case in cases:
        result = module.route_task(state, case["task"])
        if result["fallback_os"] == case["expected_os"]:
            correct_fallbacks += 1
        if result["decision"] == "route":
            auto_routes += 1
            if result["recommended_os"] == case["expected_os"]:
                correct_auto_routes += 1
            else:
                unsafe_routes.append({
                    "task": case["task"],
                    "expected": case["expected_os"],
                    "actual": result["recommended_os"],
                    "confidence": result["confidence"],
                })
        else:
            abstentions.append({
                "task": case["task"],
                "expected": case["expected_os"],
                "fallback": result["fallback_os"],
                "confidence": result["confidence"],
            })
    total = len(cases)
    return {
        "cases": total,
        "auto_routes": auto_routes,
        "correct_auto_routes": correct_auto_routes,
        "unsafe_auto_routes": len(unsafe_routes),
        "precision": round(correct_auto_routes / auto_routes, 4) if auto_routes else None,
        "coverage": round(auto_routes / total, 4) if total else 0.0,
        "safe_success_rate": round((correct_auto_routes + len(abstentions)) / total, 4) if total else 0.0,
        "fallback_accuracy": round(correct_fallbacks / total, 4) if total else 0.0,
        "unsafe_routes": unsafe_routes,
        "abstention_count": len(abstentions),
    }


def ambiguous_router_metrics(module: Any, benchmark_path: Path, current_os: str) -> dict[str, Any]:
    cases = load_json(benchmark_path, [])
    routing = load_json(ROOT / "manifest" / "os-routing.json", {})
    state = {
        "current_os": current_os,
        "os_states": {name: {"stage": stages[0]} for name, stages in routing["os_stages"].items()},
    }
    unsafe = []
    for case in cases:
        result = module.route_task(state, case["task"])
        if result["decision"] != "abstain":
            unsafe.append({
                "task": case["task"],
                "actual": result["recommended_os"],
                "confidence": result["confidence"],
            })
    total = len(cases)
    return {
        "cases": total,
        "abstentions": total - len(unsafe),
        "abstention_rate": round((total - len(unsafe)) / total, 4) if total else 0.0,
        "unsafe_auto_routes": len(unsafe),
        "auto_routes": unsafe,
    }


def percent(value: Any) -> str:
    return "N/A" if value is None else f"{float(value):.1%}"


def report_markdown(result: dict[str, Any]) -> str:
    overall = result["overall"]
    tests = result["automated_tests"]
    legacy_red = result["red_team"]["legacy"]["summary"]
    v20_red = result["red_team"]["v20"]["summary"]
    v21_red = result["red_team"]["v21"]["summary"]
    v23_red = result["red_team"]["v23"]["summary"]
    v24_red = result["red_team"]["v24"]["summary"]
    v25_red = result["red_team"]["v25"]["summary"]
    red_summaries = [legacy_red, v20_red, v21_red, v23_red, v24_red, v25_red]
    combined_red = sum(item["cases"] for item in red_summaries)
    combined_passed = sum(item["passed"] for item in red_summaries)
    routing = result["routing"]
    pilot = result["l5a_real_project"]
    pilot_perf = pilot.get("performance", {})
    pilot_sdlc = pilot.get("sdlc", {})
    pilot_gates = pilot_sdlc.get("gates", {})
    l5b = result["l5b_matched_experiment"]
    multi = result["multi_project_validation"]
    postgres = result["postgresql_conformance"]
    skill = result["skill_governance"]

    lines = [
        "# Agentic SDLC OS v2.5 验证报告",
        "",
        f"- 生成时间：`{result['generated_at']}`",
        f"- 工程验证结论：**{'有条件通过 / Beta Candidate' if overall['decision'] == 'beta-candidate' else '未通过'}**",
        f"- 生产就绪结论：**{'是' if overall['production_ready'] else '否'}**",
        "- 证据边界：已证明控制机制和参考场景可执行；尚未证明真实生产环境中的因果提效、长期稳定性或 PostgreSQL 实机一致性。",
        "",
        "## 1. 总体验证",
        "",
        "| 验证层 | 结果 |",
        "|---|---:|",
        f"| 7 个 OS Skills 静态验证 | {'PASS' if result['static_validation']['passed'] else 'FAIL'} |",
        f"| 自动化测试 | {tests.get('tests', '?')} tests + {tests.get('subtests', 0)} subtests PASS |",
        f"| 红队攻击 | {combined_passed}/{combined_red} 阻断 |",
        f"| 路由安全 | {'PASS' if routing['passed'] else 'FAIL'} |",
        f"| L5-A 可执行试点 | {'PASS' if pilot.get('passed') else 'FAIL'} |",
        f"| L5-B 工具链合成烟测 | {'PASS' if l5b.get('passed') else 'FAIL'}，{l5b.get('pairs', '?')} 对 |",
        f"| 五类参考项目场景 | {multi.get('passed_scenarios', 0)}/{multi.get('scenario_count', 0)} PASS |",
        f"| PostgreSQL DDL/迁移静态一致性 | {'PASS' if postgres.get('passed') else 'FAIL'} |",
        f"| PostgreSQL 实机集成 | {'PASS' if postgres.get('live') else 'NOT RUN'} |",
        f"| 第三方 Skill 锁定状态 | 本地有效；外部未锁定 {skill.get('external_unresolved', '?')} 个，默认禁止安装 |",
        "",
        "## 2. 八项优化完成度",
        "",
        "| 优化项 | 已落地能力 | 验证状态 |",
        "|---|---|---|",
        "| L5-B 对照实验 | 预注册、随机交叉顺序、双臂盲码、日志/制品哈希、污染检测、配对统计、Bootstrap CI | 工具链 PASS；真实实验 NOT RUN |",
        "| 多项目验证 | Web SaaS、HarmonyOS、AI Agent、旧系统改造、金融发布五类可执行场景 | 5/5 PASS；非外部长期项目 |",
        "| 生产级控制面 | SQLAlchemy/PostgreSQL 模型、乐观并发、租约 fencing、幂等队列、RBAC、审批、审计链、恢复、密钥加密 | SQLite 集成 + PostgreSQL 静态 PASS；实机 PG NOT RUN |",
        "| 使用体验 | 一键初始化、风险自动裁剪、Dashboard、Gate 审批、Git/JUnit/Coverage/部署证据采集 | 自动化测试 PASS |",
        "| 动态流程裁剪 | Project + Work Item 双层风险、硬升级、bounded-lite 压缩 | v2.1 Work Item 红队 PASS |",
        "| Skill 治理 | 安全扫描、版本哈希锁、依赖冲突、效果评分、canary/watch/deprecated 生命周期 | 本地锁校验 PASS；未锁外部默认拒绝 |",
        "| 成本治理 | Token/工具/美元/人工时预算、watch/degraded/blocked、降级顺序 | 硬预算阻断 PASS |",
        "| 领域扩展包 | HarmonyOS、SaaS、AI Agent、电商、金融控制、制品、证据与 Gate Overlay | 5 个 Pack 校验 PASS |",
        "",
        "## 3. 控制面红队",
        "",
        f"旧控制面：**{legacy_red['passed']}/{legacy_red['cases']}**；v2.0：**{v20_red['passed']}/{v20_red['cases']}**；v2.1 Work Item：**{v21_red['passed']}/{v21_red['cases']}**；v2.3 并发/L5-B/成熟度：**{v23_red['passed']}/{v23_red['cases']}**；v2.4 Skill 组合/职责分离/Provider：**{v24_red['passed']}/{v24_red['cases']}**；v2.5 生产证据链：**{v25_red['passed']}/{v25_red['cases']}**。",
        "",
        "重点验证：并发丢写、审计篡改、过期租约、错误 Worker 完成、重复任务、自己审批、过期审批、无认证访问、越权写入、无密钥操作、预算绕过、恶意 Skill、未锁定依赖、实验数据篡改和跨臂污染。",
        "",
        "## 4. 路由器",
        "",
        "| 数据集 | 覆盖率 | 精确率/拒绝率 | 错误自动路由 |",
        "|---|---:|---:|---:|",
        f"| 开发集（{routing['development']['cases']}） | {percent(routing['development']['coverage'])} | {percent(routing['development']['precision'])} | {routing['development']['unsafe_auto_routes']} |",
        f"| 改写集（{routing['paraphrase_stress']['cases']}） | {percent(routing['paraphrase_stress']['coverage'])} | {percent(routing['paraphrase_stress']['precision'])} | {routing['paraphrase_stress']['unsafe_auto_routes']} |",
        f"| 歧义集（{routing['ambiguous']['cases']}） | — | 拒绝率 {percent(routing['ambiguous']['abstention_rate'])} | {routing['ambiguous']['unsafe_auto_routes']} |",
        "",
        "## 5. L5-A 真实需求试点",
        "",
        "试点范围：乒乓球馆 SaaS 的原子预约、FIFO 候补、取消自动转正与并发防超售。",
        "",
        "| 指标 | 结果 |",
        "|---|---:|",
        f"| 试点测试 | {pilot.get('tests', {}).get('count', '?')} PASS |",
        f"| 覆盖率 | {pilot.get('tests', {}).get('coverage_percent', '?')}% |",
        f"| 并发请求 / 容量 | {pilot_perf.get('requests', '?')} / {pilot_perf.get('capacity', '?')} |",
        f"| 预约 / 候补 / 超售 | {pilot_perf.get('reserved', '?')} / {pilot_perf.get('waitlisted', '?')} / {1 if pilot_perf.get('oversold') else 0} |",
        f"| Accepted 制品 | {pilot_sdlc.get('artifacts', '?')} |",
        f"| Gate | {sum(1 for value in pilot_gates.values() if value == 'pass')}/{len(pilot_gates)} PASS |",
        f"| 最终学习回流 | {pilot_sdlc.get('final_state', '?')} |",
        "",
        "## 6. 尚未验证",
        "",
        "1. **真实 L5-B 对照实验**：当前只有合成烟测，不能据此宣称提效、降本或降缺陷。",
        "2. **PostgreSQL 实机**：已编译 PostgreSQL DDL 和迁移，但当前环境没有可用 PostgreSQL 服务。",
        "3. **独立真实多项目**：五类场景是可执行参考项目，不等于五个外部团队的长期项目。",
        "4. **30 天生产运行**：未验证持续负载、值班响应、备份恢复、密钥轮换和组织权限变化。",
        f"5. **第三方 Skills**：{skill.get('external_unresolved', '?')} 个通用候选/Provider Adapter 尚未锁定，严格模式下保持禁用。",
        "",
        "## 7. 当前决策",
        "",
        "可以进入受控 Dogfooding 和真实 L5-B 实验；不能直接标记为 Production Ready。",
        "",
        "## 8. 复现命令",
        "",
        "```bash",
        "python scripts/run_validation.py",
        "python validation/red_team_validation.py",
        "python validation/v20_red_team.py",
        "python validation/v21_work_item_red_team.py",
        "python validation/v23_red_team.py",
        "python validation/v24_red_team.py",
        "python validation/v25_red_team.py",
        "python scripts/multi_project_validation.py",
        "python validation/l5b/generate_synthetic_smoke.py",
        "python scripts/postgres_conformance.py",
        "python scripts/build_release.py",
        "```",
    ]
    return "\n".join(lines) + "\n"


def main() -> int:
    module = load_cli()

    # The L5-A pilot is a preserved executable evidence package. It was replayed
    # during release preparation and is rechecked structurally by test_v14.
    # Avoid replaying it in this aggregate runner because it rewrites the same
    # workspace that the repository suite inspects.
    pilot_payload = load_json(PILOT_RESULT, {})
    pilot_run = {
        "command": [str(PILOT_VERIFY)],
        "returncode": 0 if pilot_payload.get("passed") else 1,
        "passed": pilot_payload.get("passed") is True,
        "stdout_tail": "Preserved L5-A evidence; validated by automated tests.",
        "stderr_tail": "",
        "scope": "precomputed-executable-evidence",
    }

    # Run cross-archetype scenarios first so they start from a clean validation
    # workspace and cannot inherit SQLite auxiliary files from later attacks.
    multi_run = run([sys.executable, "scripts/multi_project_validation.py"])
    multi_payload = load_json(ROOT / "validation" / "multi_project" / "latest.json", {})

    static_run = run([sys.executable, "scripts/validate_all.py"])
    sample_run = run([sys.executable, str(CLI), "validate", "examples/saas-mvp", "--json"])

    legacy_red_run = run([sys.executable, "validation/red_team_validation.py"])
    legacy_red = load_json(ROOT / "validation" / "red_team_results.json", {"summary": {}})
    v20_red_run = run([sys.executable, "validation/v20_red_team.py"])
    v20_red = load_json(ROOT / "validation" / "v20_red_team_results.json", {"summary": {}})
    v21_red_run = run([sys.executable, "validation/v21_work_item_red_team.py"])
    v21_red = load_json(ROOT / "validation" / "v21_work_item_red_team_results.json", {"summary": {}})
    v23_red_run = run([sys.executable, "validation/v23_red_team.py"])
    v23_red = load_json(ROOT / "validation" / "v23_red_team_results.json", {"summary": {}})
    v24_red_run = run([sys.executable, "validation/v24_red_team.py"])
    v24_red = load_json(ROOT / "validation" / "v24_red_team_results.json", {"summary": {}})
    v25_red_run = run([sys.executable, "validation/v25_red_team.py"])
    v25_red = load_json(ROOT / "validation" / "v25_red_team_results.json", {"summary": {}})

    legacy_l5_validate = run([sys.executable, str(LEGACY_L5), "validate", "validation/l5/synthetic-smoke.json", "--json"])
    legacy_l5_report = run([sys.executable, str(LEGACY_L5), "report", "validation/l5/synthetic-smoke.json", "--json"])

    l5b_generate = run([sys.executable, "validation/l5b/generate_synthetic_smoke.py"])
    l5b_validate = run([sys.executable, str(L5B), "validate", "validation/l5b/synthetic-matched.json", "--json"])
    l5b_report = run([sys.executable, str(L5B), "report", "validation/l5b/synthetic-matched.json", "--json"])
    l5b_result = load_json(ROOT / "validation" / "l5b" / "synthetic-result.json", {})
    l5b_passed = all(item["passed"] for item in [l5b_generate, l5b_validate, l5b_report]) and l5b_result.get("decision") == "synthetic-smoke-only"

    skill_scan = run([sys.executable, "scripts/skill_governance.py", "scan", "skills"])
    skill_verify = run([sys.executable, "scripts/skill_governance.py", "verify-lock"])
    skill_verify_payload = json.loads(skill_verify["stdout_tail"]) if skill_verify["passed"] else {}

    postgres_run = run([sys.executable, "scripts/postgres_conformance.py"])
    postgres_payload = json.loads(postgres_run["stdout_tail"]) if postgres_run["passed"] else {"passed": False, "live": False}

    # Run the repository test suite last. Some tests intentionally exercise
    # filesystem and SQLite lifecycle controls; no further child validator is
    # started after it.
    # multi_project_validation.py is already executed above. Exclude the one test
    # that only invokes the same long-running scenario suite a second time.
    test_run = run([sys.executable, "-m", "pytest", "-q", "tests", "-k", "not multi_project_suite"])
    counts = parse_pytest(test_run["stdout_tail"] + "\n" + test_run["stderr_tail"])
    if counts.get("tests") is not None and multi_run["passed"] and multi_payload.get("passed") is True:
        counts["tests"] = int(counts["tests"]) + 1
    automated_tests = test_run | counts | {"multi_project_equivalent_test": 1 if multi_run["passed"] and multi_payload.get("passed") is True else 0}

    dev = router_metrics(module, ROOT / "validation" / "benchmarks" / "router-cases.json", "pm")
    holdout = router_metrics(module, ROOT / "validation" / "benchmarks" / "router-holdout.json", "engineering")
    ambiguous = ambiguous_router_metrics(module, ROOT / "validation" / "benchmarks" / "router-ambiguous.json", "engineering")
    routing_passed = (
        dev["unsafe_auto_routes"] == 0
        and dev["coverage"] >= 0.90
        and (dev["precision"] or 0.0) >= 0.95
        and holdout["unsafe_auto_routes"] == 0
        and holdout["coverage"] >= 0.90
        and (holdout["precision"] or 0.0) >= 0.95
        and ambiguous["unsafe_auto_routes"] == 0
        and ambiguous["abstention_rate"] >= 0.90
    )

    legacy_red_ok = legacy_red_run["passed"] and legacy_red.get("summary", {}).get("all_controls_passed") is True
    v20_red_ok = v20_red_run["passed"] and v20_red.get("summary", {}).get("all_controls_passed") is True
    v21_red_ok = v21_red_run["passed"] and v21_red.get("summary", {}).get("all_controls_passed") is True
    v23_red_ok = v23_red_run["passed"] and v23_red.get("summary", {}).get("all_controls_passed") is True
    v24_red_ok = v24_red_run["passed"] and v24_red.get("summary", {}).get("all_controls_passed") is True
    v25_red_ok = v25_red_run["passed"] and v25_red.get("summary", {}).get("all_controls_passed") is True
    pilot_ok = pilot_run["passed"] and pilot_payload.get("passed") is True
    multi_ok = multi_run["passed"] and multi_payload.get("passed") is True
    skills_ok = skill_scan["passed"] and skill_verify["passed"] and skill_verify_payload.get("valid") is True
    postgres_static_ok = postgres_run["passed"] and postgres_payload.get("passed") is True
    legacy_l5_ok = legacy_l5_validate["passed"] and legacy_l5_report["passed"]

    core_passed = all([
        automated_tests["passed"],
        static_run["passed"],
        sample_run["passed"],
        legacy_red_ok,
        v20_red_ok,
        v21_red_ok,
        v23_red_ok,
        v24_red_ok,
        v25_red_ok,
        routing_passed,
        legacy_l5_ok,
        l5b_passed,
        pilot_ok,
        multi_ok,
        skills_ok,
        postgres_static_ok,
    ])

    real_l5b_run = False
    independent_external_projects = False
    live_postgres = bool(postgres_payload.get("live"))
    thirty_day_soak = False
    production_ready = core_passed and real_l5b_run and independent_external_projects and live_postgres and thirty_day_soak

    result = {
        "generated_at": now(),
        "system_version": module.VERSION,
        "overall": {
            "core_engineering_validation": "pass" if core_passed else "fail",
            "decision": "beta-candidate" if core_passed else "fail",
            "production_ready": production_ready,
            "real_l5b_matched_experiment": "not-run",
            "independent_external_multi_project": "not-run",
            "live_postgresql": "pass" if live_postgres else "not-run",
            "thirty_day_soak": "not-run",
        },
        "automated_tests": automated_tests,
        "static_validation": static_run,
        "sample_validation": sample_run,
        "red_team": {
            "passed": legacy_red_ok and v20_red_ok and v21_red_ok and v23_red_ok and v24_red_ok and v25_red_ok,
            "legacy": legacy_red,
            "v20": v20_red,
            "v21": v21_red,
            "v23": v23_red,
            "v24": v24_red,
            "v25": v25_red,
            "legacy_run": legacy_red_run,
            "v20_run": v20_red_run,
            "v21_run": v21_red_run,
            "v23_run": v23_red_run,
            "v24_run": v24_red_run,
            "v25_run": v25_red_run,
        },
        "routing": {
            "passed": routing_passed,
            "development": dev,
            "paraphrase_stress": holdout,
            "ambiguous": ambiguous,
        },
        "legacy_l5_harness": {
            "passed": legacy_l5_ok,
            "validate": legacy_l5_validate,
            "report": legacy_l5_report,
            "scope": "synthetic-tooling-smoke-only",
        },
        "l5a_real_project": pilot_payload,
        "l5a_run": pilot_run,
        "l5b_matched_experiment": {
            "passed": l5b_passed,
            "scope": "synthetic-harness-smoke-only",
            "decision": l5b_result.get("decision"),
            "pairs": l5b_result.get("complete_pairs"),
            "result": l5b_result,
            "generate": l5b_generate,
            "validate": l5b_validate,
            "report": l5b_report,
            "real_effect_claim_allowed": False,
        },
        "multi_project_validation": {
            "passed": multi_ok,
            "scenario_count": len(multi_payload.get("scenarios", [])),
            "passed_scenarios": sum(1 for item in multi_payload.get("scenarios", []) if item.get("passed")),
            "scope": "executable-reference-archetypes-not-independent-external-projects",
            "result": multi_payload,
            "run": multi_run,
        },
        "skill_governance": {
            "passed": skills_ok,
            "lock_valid": skill_verify_payload.get("valid"),
            "external_unresolved": skill_verify_payload.get("external_unresolved"),
            "strict_external_install_ready": skill_verify_payload.get("strict_external_install_ready"),
            "scan": skill_scan,
            "verify": skill_verify,
        },
        "postgresql_conformance": postgres_payload | {"run": postgres_run},
        "evidence_boundaries": [
            "No real L5-B matched experiment has been run.",
            "No live PostgreSQL service was available in this environment.",
            "The five multi-project cases are executable reference archetypes, not independent external long-running projects.",
            "No 30-day production soak has been run.",
            "Unresolved third-party Skills remain disabled under deny-unlocked policy.",
        ],
    }

    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    LATEST_JSON.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    REPORT_MD.write_text(report_markdown(result), encoding="utf-8")
    summary = {
        "decision": result["overall"]["decision"],
        "production_ready": result["overall"]["production_ready"],
        "tests": counts,
        "red_team": {
            "legacy": legacy_red.get("summary"),
            "v20": v20_red.get("summary"),
            "v21": v21_red.get("summary"),
            "v23": v23_red.get("summary"),
            "v24": v24_red.get("summary"),
            "v25": v25_red.get("summary"),
        },
        "router": {
            "development": dev,
            "holdout": holdout,
            "ambiguous": ambiguous,
        },
        "l5a": pilot_ok,
        "l5b_synthetic": l5b_passed,
        "l5b_real": "not-run",
        "multi_project_reference_scenarios": f"{sum(1 for item in multi_payload.get('scenarios', []) if item.get('passed'))}/{len(multi_payload.get('scenarios', []))}",
        "postgresql_static": postgres_static_ok,
        "postgresql_live": "pass" if live_postgres else "not-run",
        "report": str(REPORT_MD),
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0 if core_passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
