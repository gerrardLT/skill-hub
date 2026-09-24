# -*- coding: utf-8 -*-
"""
Generator for vitest semantic units.
Extracts verbatim excerpts from skills/vitest/SKILL.md and references/
and validates each unit according to Phase 3 schema (12-key format).
"""

import json
import pathlib
import sys

sys.path.insert(0, "tools/curation")
from verify import verify_unit

def extract_lines(file_path: str, start: int, end: int) -> str:
    path = pathlib.Path("skills") / file_path
    lines = path.read_text(encoding="utf-8").splitlines()
    # 1-based indexing: lines[start-1:end]
    return "\n".join(lines[start - 1:end])

def build_units():
    units_def = [
        # 1. vitest:unit-001
        {
            "id": "vitest:unit-001",
            "source_path": "vitest/SKILL.md",
            "origin_line_start": 10,
            "origin_line_end": 20,
            "type": "rule",
            "meaning": "Vitest 核心定位与能力特性：基于 Vite 构建的高性能单元测试框架，兼容 Jest API，支持原生 ESM/TS/JSX、智能监听、多线程执行与覆盖率",
            "boundary_condition": "用于前端、Node.js 及全栈 TypeScript/JavaScript 项目单元与集成测试",
            "dependency_skills": [],
            "candidate_destination": "testing:vitest-core-features",
            "validation_criteria": "确认测试套件能够直接复用 Vite 变换管线并无缝执行 Jest 兼容断言",
            "status": "retain"
        },
        # 2. vitest:unit-002
        {
            "id": "vitest:unit-002",
            "source_path": "vitest/references/core-config.md",
            "origin_line_start": 12,
            "origin_line_end": 21,
            "type": "method",
            "meaning": "Vitest 基础配置方法：通过 vitest.config.ts 使用 defineConfig 声明测试参数与选项",
            "boundary_condition": "独立 Vitest 配置文件的标准化声明",
            "dependency_skills": [],
            "candidate_destination": "configuration:vitest-define-config",
            "validation_criteria": "配置文件正确导出 defineConfig 并包含 test 选项字段",
            "status": "retain"
        },
        # 3. vitest:unit-003
        {
            "id": "vitest:unit-003",
            "source_path": "vitest/references/core-config.md",
            "origin_line_start": 44,
            "origin_line_end": 54,
            "type": "method",
            "meaning": "Vite 现有配置集成方法：使用 mergeConfig 工具将现有 vite.config 与 Vitest 测试配置融合",
            "boundary_condition": "项目中存在既有 Vite 配置时避免配置冗余或冲突",
            "dependency_skills": [],
            "candidate_destination": "configuration:vitest-merge-config",
            "validation_criteria": "运行测试时能正确继承既有 Vite 别名与插件且生效测试环境配置",
            "status": "retain"
        },
        # 4. vitest:unit-004
        {
            "id": "vitest:unit-004",
            "source_path": "vitest/references/core-config.md",
            "origin_line_start": 117,
            "origin_line_end": 120,
            "type": "rule",
            "meaning": "现代版本进程池演化规程：默认采用 forks 子进程池，废弃 poolOptions，所有并发线程参数提升为顶级 maxWorkers",
            "boundary_condition": "Vitest v4/v5 版本配置迁移与性能调优",
            "dependency_skills": [],
            "candidate_destination": "configuration:worker-pool-rules",
            "validation_criteria": "配置中无过时的 poolOptions 嵌套，顶级 maxWorkers 正确生效",
            "status": "retain"
        },
        # 5. vitest:unit-005
        {
            "id": "vitest:unit-005",
            "source_path": "vitest/references/features-mocking.md",
            "origin_line_start": 10,
            "origin_line_end": 33,
            "type": "method",
            "meaning": "Mock 函数创建与返回值控制方法：使用 vi.fn() 创建函数并链式配置返回值、Promise 解决值与实现函数",
            "boundary_condition": "单元测试中隔离依赖组件与回调验证",
            "dependency_skills": [],
            "candidate_destination": "mocking:vi-fn-implementation",
            "validation_criteria": "Mock 函数记录调用参数与次数，且按预期返回配置的值或异常",
            "status": "retain"
        },
        # 6. vitest:unit-006
        {
            "id": "vitest:unit-006",
            "source_path": "vitest/references/features-mocking.md",
            "origin_line_start": 37,
            "origin_line_end": 53,
            "type": "method",
            "meaning": "对象方法间谍监听与覆盖方法：使用 vi.spyOn() 监听已有对象方法并在测试完成后通过 mockRestore 还原",
            "boundary_condition": "需要监控真实对象行为或临时重写特定方法且需干净恢复",
            "dependency_skills": [],
            "candidate_destination": "mocking:vi-spyon-restore",
            "validation_criteria": "被间谍监听的方法被正确劫持并在测试后安全复原",
            "status": "retain"
        },
        # 7. vitest:unit-007
        {
            "id": "vitest:unit-007",
            "source_path": "vitest/references/features-mocking.md",
            "origin_line_start": 64,
            "origin_line_end": 83,
            "type": "method",
            "meaning": "声明式条件 Mocking 方法：使用 v5 的 vi.when().calledWith().thenResolve() 按参数精确定义不同响应",
            "boundary_condition": "复杂分流调用而无需手写易错的 if-else mockImplementation",
            "dependency_skills": [],
            "candidate_destination": "mocking:vi-when-conditional",
            "validation_criteria": "按参数精准匹配并返回结果，未匹配调用按 onUnmatched 策略处理",
            "status": "retain"
        },
        # 8. vitest:unit-008
        {
            "id": "vitest:unit-008",
            "source_path": "vitest/references/features-mocking.md",
            "origin_line_start": 84,
            "origin_line_end": 94,
            "type": "rule",
            "meaning": "显式资源管理自动回收规则：利用 TS using 声明使 Spy/Mock 在测试块作用域退出时自动 restore，免写 afterEach",
            "boundary_condition": "Node 24+ 及 TypeScript 5.2+ 运行环境中的局部 Mocking",
            "dependency_skills": [],
            "candidate_destination": "mocking:explicit-resource-management",
            "validation_criteria": "测试用例块退出后被 using 声明的对象自动释放与还原",
            "status": "retain"
        },
        # 9. vitest:unit-009
        {
            "id": "vitest:unit-009",
            "source_path": "vitest/references/features-concurrency.md",
            "origin_line_start": 33,
            "origin_line_end": 51,
            "type": "gate",
            "meaning": "并发测试断言上下文绑定门禁：在 test.concurrent 中必须解构并使用用例级 expect 上下文，禁止使用顶层全局 expect",
            "boundary_condition": "任何 test.concurrent 或 describe.concurrent 并发执行流",
            "dependency_skills": [],
            "candidate_destination": "concurrency:expect-context-isolation",
            "validation_criteria": "并发执行中每个异步断言严格绑定独立上下文，无状态交叉污染",
            "status": "retain"
        },
        # 10. vitest:unit-010
        {
            "id": "vitest:unit-010",
            "source_path": "vitest/references/features-concurrency.md",
            "origin_line_start": 52,
            "origin_line_end": 72,
            "type": "rule",
            "meaning": "Vitest 5 退出并发模式规程：因 sequential 被移除，必须显式传入 { concurrent: false } 退出并发继承",
            "boundary_condition": "在全局并发或父级 describe.concurrent 下需要排他单线程执行的用例",
            "dependency_skills": [],
            "candidate_destination": "concurrency:opt-out-v5",
            "validation_criteria": "带有 { concurrent: false } 的测试或套件按串行顺序独立运行",
            "status": "retain"
        },
        # 11. vitest:unit-011
        {
            "id": "vitest:unit-011",
            "source_path": "vitest/references/features-context.md",
            "origin_line_start": 29,
            "origin_line_end": 52,
            "type": "method",
            "meaning": "自定义 Fixture 链式构建方法：通过 .extend() 构建强类型自推断夹具，并注入 onCleanup 生命周期释放资源",
            "boundary_condition": "测试用例需要可复用依赖注入与确定性资源清理",
            "dependency_skills": [],
            "candidate_destination": "fixtures:builder-pattern-extend",
            "validation_criteria": "Fixture 类型在测试入参中精准推断，且测试结束后 onCleanup 正确触发",
            "status": "retain"
        },
        # 12. vitest:unit-012
        {
            "id": "vitest:unit-012",
            "source_path": "vitest/references/features-context.md",
            "origin_line_start": 84,
            "origin_line_end": 93,
            "type": "rule",
            "meaning": "Fixture 生命周期作用域规则：划分 test（每个用例）、file（单文件一次）、worker（进程一次）三级边界与访问权限",
            "boundary_condition": "设计重型数据库容器、HTTP 服务或轻量上下文夹具时选择生命周期",
            "dependency_skills": [],
            "candidate_destination": "fixtures:scope-lifecycle-rules",
            "validation_criteria": "夹具按声明的作用域级别创建与销毁，未越界访问非法上下文",
            "status": "retain"
        },
        # 13. vitest:unit-013
        {
            "id": "vitest:unit-013",
            "source_path": "vitest/references/advanced-type-testing.md",
            "origin_line_start": 10,
            "origin_line_end": 23,
            "type": "method",
            "meaning": "TypeScript 静态类型测试方法：在 .test-d.ts 中使用 expectTypeOf 进行无运行时开销的编译期类型断言",
            "boundary_condition": "库开发或复杂泛型推断的静态正确性保障",
            "dependency_skills": [],
            "candidate_destination": "typecheck:expect-type-of",
            "validation_criteria": "类型测试在 tsc / vue-tsc 检查阶段验证类型匹配，失败时抛出编译诊断",
            "status": "retain"
        },
        # 14. vitest:unit-014
        {
            "id": "vitest:unit-014",
            "source_path": "vitest/references/advanced-vi.md",
            "origin_line_start": 57,
            "origin_line_end": 77,
            "type": "method",
            "meaning": "提升式模块 Mocking 与部分 Mocking：通过 vi.mock() 劫持 ESM 模块或通过 importOriginal 仅替换局部导出",
            "boundary_condition": "跨文件外部模块依赖隔离与 API 打桩",
            "dependency_skills": [],
            "candidate_destination": "mocking:vi-mock-hoisted",
            "validation_criteria": "模块在所有静态导入前被优先提升 Mock，指定导出按桩函数执行",
            "status": "retain"
        },
        # 15. vitest:unit-015
        {
            "id": "vitest:unit-015",
            "source_path": "vitest/references/advanced-vi.md",
            "origin_line_start": 81,
            "origin_line_end": 89,
            "type": "method",
            "meaning": "动态非提升式模块 Mocking：使用 vi.doMock() 配合动态 import() 实现运行时条件按需 Mock 与 unmock",
            "boundary_condition": "同一测试文件中需要动态切换不同模块实现的测试场景",
            "dependency_skills": [],
            "candidate_destination": "mocking:vi-domock-dynamic",
            "validation_criteria": "模块不会被顶部提升，后续动态 import 取得当前 mock 实例",
            "status": "retain"
        },
        # 16. vitest:unit-016
        {
            "id": "vitest:unit-016",
            "source_path": "vitest/references/advanced-vi.md",
            "origin_line_start": 133,
            "origin_line_end": 164,
            "type": "method",
            "meaning": "虚拟定时器与时钟步进控制：使用 vi.useFakeTimers() 劫持系统定时器并通过 advanceTimersByTime 控制时间流逝",
            "boundary_condition": "测试防抖节流、长轮询或延迟执行逻辑而无需真实等待",
            "dependency_skills": [],
            "candidate_destination": "timers:fake-timers-control",
            "validation_criteria": "定时器即刻触发回调，测试执行耗时压缩至毫秒级且时钟还原完整",
            "status": "retain"
        },
        # 17. vitest:unit-017
        {
            "id": "vitest:unit-017",
            "source_path": "vitest/references/core-test-api.md",
            "origin_line_start": 60,
            "origin_line_end": 73,
            "type": "method",
            "meaning": "条件化跳过与动态跳过方法：使用 test.skipIf、test.runIf 或测试上下文中的 skip() 动态跳过用例",
            "boundary_condition": "针对不同操作系统、CI 环境或特定外部服务可用性动态调节测试执行",
            "dependency_skills": [],
            "candidate_destination": "test-api:skip-modifiers",
            "validation_criteria": "符合条件的用例被正确跳过并记录在报告中，不触发失败",
            "status": "retain"
        },
        # 18. vitest:unit-018
        {
            "id": "vitest:unit-018",
            "source_path": "vitest/references/features-snapshots.md",
            "origin_line_start": 12,
            "origin_line_end": 19,
            "type": "method",
            "meaning": "快照测试比对方法：使用 toMatchSnapshot() 将复杂结构输出序列化至快照文件并进行防回归校验",
            "boundary_condition": "复杂 DOM 结构、AST 节点或大数据报表结构防退化检测",
            "dependency_skills": [],
            "candidate_destination": "snapshots:match-snapshot",
            "validation_criteria": "初次运行生成 .snap 文件，后续运行如输出变动则抛出详细 Diff",
            "status": "retain"
        },
        # 19. vitest:unit-019
        {
            "id": "vitest:unit-019",
            "source_path": "vitest/references/features-coverage.md",
            "origin_line_start": 17,
            "origin_line_end": 51,
            "type": "rule",
            "meaning": "代码覆盖率配置与质量门禁规程：配置 V8 提供者、显式 include 范围及行/函数/分支/语句 80% 阈值门禁",
            "boundary_condition": "项目 CI 流水线测试覆盖率准出校验",
            "dependency_skills": [],
            "candidate_destination": "coverage:threshold-gate-rules",
            "validation_criteria": "运行覆盖率统计，若任何维度未达到配置阈值则直接使进程返回非零退出码",
            "status": "retain"
        },
        # 20. vitest:unit-020
        {
            "id": "vitest:unit-020",
            "source_path": "vitest/references/core-cli.md",
            "origin_line_start": 14,
            "origin_line_end": 28,
            "type": "method",
            "meaning": "CLI 执行与精准过滤方法：通过 vitest run 一次性运行、按路径过滤及行号定位测试用例",
            "boundary_condition": "开发调试特定用例或 CI 脚本集成",
            "dependency_skills": [],
            "candidate_destination": "cli:run-and-filtering",
            "validation_criteria": "命令行能够精准命中指定文件或行号用例并输出简洁反馈",
            "status": "retain"
        }
    ]

    units = []
    for item in units_def:
        raw_excerpt = extract_lines(
            item["source_path"],
            item["origin_line_start"],
            item["origin_line_end"]
        )
        unit = {
            "id": item["id"],
            "source_path": item["source_path"],
            "origin_line_start": item["origin_line_start"],
            "origin_line_end": item["origin_line_end"],
            "type": item["type"],
            "raw_excerpt": raw_excerpt,
            "meaning": item["meaning"],
            "boundary_condition": item["boundary_condition"],
            "dependency_skills": item["dependency_skills"],
            "candidate_destination": item["candidate_destination"],
            "validation_criteria": item["validation_criteria"],
            "status": item["status"]
        }
        units.append(unit)

    return units

def main():
    units = build_units()
    skills_root = pathlib.Path("skills")
    errors = []

    for unit in units:
        errs, matches = verify_unit(unit, skills_root)
        if errs or not matches:
            errors.extend([f"[{unit['id']}] {e}" for e in errs])
            if not matches and not errs:
                errors.append(f"[{unit['id']}] excerpt does not match source")

    if errors:
        print(f"FAILED with {len(errors)} errors:")
        for err in errors:
            print(" ", err)
        sys.exit(1)

    output_path = pathlib.Path("curation/units/vitest.jsonl")
    with open(output_path, "w", encoding="utf-8") as f:
        for unit in units:
            f.write(json.dumps(unit, ensure_ascii=False) + "\n")

    print(f"SUCCESS: Generated {len(units)} validated units in {output_path}")

if __name__ == "__main__":
    main()
