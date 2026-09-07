# 第三方 Skills 研究与采用规则

## v2.4 选择模型

采用 **Core + bounded Recommended + Conditional + explicit Provider Adapter**。

- `core`：该 OS 的最小高价值能力。
- `recommended`：只有真实工作流缺口出现后再加。
- `conditional`：必须由技术栈、平台、产品类型或任务证据触发。
- `provider_adapters`：仅 Evolution 使用；Sentry、Datadog、PostHog 都必须显式激活。

## 研究口径

清单以 2026-09-01 可核验信息为基线，综合源码/官方资料、公开采用信号、Issue/社区反馈、方法完整度、Agent 可执行性、安全权限、维护状态和与现有 OS 的互补度。安装量/Stars 不能单独证明质量。

## v2.4 三项重要调整

1. **Design 去重**：一个工作项只保留一个主视觉导演，默认 `impeccable`；其他 Skill 作为知识层、规范层、Motion 专项或条件性候选。
2. **QA 职责分离**：QA 不得通过修改产品源码让自己的测试通过；修复必须交给 Engineering，再由 QA 独立复验。
3. **Evolution 厂商解耦**：Generic Core 负责诊断和学习；Observability Provider 只提供证据和受限动作，不能拥有 `learning-decision`。

## 安装策略

```bash
# 默认只看 Core，不执行
python skills/agentic-sdlc-os/scripts/install_external_skills.py --os design --profile core
python skills/agentic-sdlc-os/scripts/install_external_skills.py --os qa --profile core
python skills/agentic-sdlc-os/scripts/install_external_skills.py --os evolution --profile core

# 只有项目实际使用 Datadog 时才加
python skills/agentic-sdlc-os/scripts/install_external_skills.py --os evolution --profile core --provider datadog
```

真正执行必须 `--execute --acknowledge-review`。自定义套件/官方插件还需 `--allow-custom`。所有外部条目都进入 Skill Lock；未锁定 Commit 时严格模式保持禁用。

完整排名见 `SKILLS_RANKINGS.md`；机器可读清单见 `manifest/external-skills.json`。
