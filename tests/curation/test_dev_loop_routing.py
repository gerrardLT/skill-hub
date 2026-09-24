from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DEV_LOOP = ROOT / "dev-loop"
ROUTING_FILES = (
    DEV_LOOP / ".qoder-plugin" / "plugin.json",
    DEV_LOOP / "README.md",
    DEV_LOOP / "skills" / "dev-loop" / "SKILL.md",
    DEV_LOOP / "skills" / "dev-loop" / "references" / "routing.md",
    DEV_LOOP / "skills" / "dev-loop" / "references" / "stages.md",
)


def test_dev_loop_routes_only_through_released_recipes_and_slots() -> None:
    combined = "\n".join(path.read_text(encoding="utf-8") for path in ROUTING_FILES)

    assert "released recipe" in combined
    assert "released slot contract" in combined
    assert "needs-input" in combined
    assert "blocked" in combined
    assert "上游哈希变化使依赖它的旧证据失效" in combined
    assert "QA 不修改产品源码" in combined


def test_dev_loop_contains_no_unverified_fallback_or_direct_skill_routes() -> None:
    combined = "\n".join(path.read_text(encoding="utf-8") for path in ROUTING_FILES)

    forbidden = (
        "流程永不中断",
        "降级执行",
        "自产 1 页",
        "手写核心逻辑实现",
        "直接调度当前环境中成熟",
        "直连 Qoder 成熟核心能力",
        "product-management:PRD生成",
        "ui-ux-pro-max-skill:ui-ux-pro-max",
        "superpowers:test-driven-development",
    )
    for phrase in forbidden:
        assert phrase not in combined


def test_dev_loop_names_all_required_recipe_entrypoints() -> None:
    routing = (ROUTING_FILES[3]).read_text(encoding="utf-8")
    expected = {
        "write-prd.json",
        "design-web-flow.json",
        "build-feature-tdd.json",
        "qa-only.json",
        "ship-release.json",
        "retro-to-requirements.json",
        "full-dev-loop.json",
    }

    assert all(name in routing for name in expected)
