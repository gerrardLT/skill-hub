# 命名规范与编写标准

创建任何资产前先读本文。目标：所有资产命名一致、触发词清晰、可直接分发。

## 1. 通用规范

- **目录名 = 资产名**，全小写 kebab-case（`my-video-trimmer`），不加日期、不加版本号（版本交给 git）
- 个人资产可加统一前缀区分来源，推荐无前缀，靠本仓库统一管理
- 描述文字用中文写清楚"做什么 + 什么时候用"，触发词写用户会自然说出的原话
- 一个资产只解决一类问题；发现自己在写"以及"时，考虑拆分

## 2. Skill（skills/）

```
skills/<skill-name>/
├── SKILL.md          # 必需，入口文件
├── references/       # 可选，复杂场景的补充文档（SKILL.md 保持精简）
├── scripts/          # 可选，可执行脚本
└── assets/           # 可选，模板等静态资源
```

SKILL.md 头部格式：

```markdown
---
name: <skill-name>
description: 一句话说明做什么。关键触发词：用户提到 "XX"、"YY"、"ZZ" 时使用。
---

# Skill 正文（保持 < 500 行；细节下沉到 references/）
```

description 编写要点：
- 第三人称，说明"做什么 + 适用 + 不适用"
- 必须包含触发信号（用户会说的原话），这是 skill 被正确调用的唯一线索

## 3. Plugin（plugins/）

```
plugins/<plugin-name>/
├── plugin.json       # 插件元数据
├── skills/           # 插件内含的 skill
└── commands/         # 可选，斜杠命令
```

- 结构由 `/create-plugin` 流程决定，本仓库只保留其产出的源
- plugin 名与内含主 skill 名保持一致，降低认知成本

## 4. Subagent（subagents/）

```
subagents/<agent-name>/
└── agent.md          # 定义文件
```

agent.md 头部格式：

```markdown
---
name: <agent-name>
description: 什么任务该派给这个代理，一句话。
tools:    # 可选，省略则继承全部工具
  - Read
  - Bash
---

# 系统提示词（角色、边界、必须遵守的规则、输出格式）
```

要点：
- description 是路由依据，写"任务特征"而不是"代理能力清单"
- 系统提示词开头先写清"你不做什么"，防止越界

## 5. Workflow（workflows/）

```
workflows/<workflow-name>/
├── WORKFLOW.md       # 流程定义：步骤、每步用哪个 skill、输入输出
└── examples/         # 可选，一次成功执行的记录
```

WORKFLOW.md 必须写清：
1. 触发条件（什么需求走这条流水线）
2. 步骤序列（每步：调哪个 skill / subagent、输入、产出）
3. 失败分支（某步失败时降级或中止的规则）

## 6. Git 提交规范

- 一个资产一个目录，一次提交只动一个资产：`add: <name>` / `fix: <name>` / `remove: <name>`
- `_template/` 目录不参与分发，仅作起步复制用
