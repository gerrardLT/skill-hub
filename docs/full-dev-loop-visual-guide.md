# Full Dev Loop：从模糊想法到完整系统

本文用图解释本项目已发布的 `full-dev-loop@1.0.0`。它不是“让 AI 一次性写完整个系统”，而是把软件开发拆成可验证、可返工、可审计的阶段。

> 核心规则：没有明确需求，不进入实现；没有真实执行证据，不算完成；QA 不替开发改代码；机器 Gate 与人工评审未同时通过，不得发布。

## 1. 一张图看完整流程

```mermaid
flowchart TD
    A([模糊想法]) --> B[收集产品简述、证据、约束与决策权限]
    B --> C{关键信息足够吗？}
    C -- 否 --> C1[Status: needs-input<br/>列出未知项与待确认问题]
    C1 --> B
    C -- 是 --> D

    subgraph S1[阶段 1：需求工程 write-prd]
      D[问题定义与范围边界] --> E[形成可追踪需求]
      E --> F[生成 Given / When / Then 验收标准]
      F --> G{需求 Gate}
      G -- 不通过 --> G1[补来源、边界、未知项或可观测结果]
      G1 --> D
    end

    G -- 通过 --> H
    subgraph S2[阶段 2：技术设计 design-web-flow]
      H[读取需求与验收标准] --> I[设计组件、接口、数据流、错误处理与权限边界]
      I --> J{设计 Gate}
      J -- 信息不足 --> J1[needs-input：请求设计决策]
      J1 --> H
      J -- 不通过 --> I
    end

    J -- 通过 --> K
    subgraph S3[阶段 3：TDD 实现 build-feature-tdd]
      K[建立隔离工作区与源码身份] --> L[先运行验收测试，观察 RED]
      L --> M[模型仅在授权工作区实现代码]
      M --> N[宿主运行固定测试命令]
      N --> O{测试与完成证据通过？}
      O -- 否 --> P[completion feedback]
      P --> M
      O -- 是 --> Q[产出 change artifact、patch、hash 与命令证据]
    end

    Q --> R
    subgraph S4[阶段 4：独立 QA qa-only]
      R[QA 只读检查需求、设计、变更与黑盒行为] --> S{QA verdict}
      S -- failed --> T[输出缺陷与复现证据<br/>QA 不改源码]
      T --> M
      S -- passed --> U[保存独立 QA 证据]
    end

    U --> V
    subgraph S5[阶段 5：交付预检 ship-release]
      V[核对 HEAD、patch、测试、QA、文档与交付策略] --> W{交付 Gate}
      W -- 不通过 --> X[blocked：指出缺失证据或越权动作]
      X --> M
      W -- 通过 --> Y[生成本地 release package]
    end

    Y --> Z
    subgraph S6[阶段 6：复盘回流 retro-to-requirements]
      Z[比较预期结果与实际结果] --> AA[记录缺陷、决策、未知项与经验]
      AA --> AB[生成 next-requirements]
    end

    AB --> AC{继续下一轮？}
    AC -- 是 --> D
    AC -- 否 --> AD{机器 Gate 全绿？}
    AD -- 否 --> AE[禁止发布并修复证据或实现]
    AE --> D
    AD -- 是 --> AF{人工语义评审批准？}
    AF -- 否 --> AG[保持 evaluating / blocked]
    AG --> D
    AF -- 是 --> AH[受控发布 Slots 与 Recipes]
    AH --> AI([系统完成：可运行、可验证、可审查、可继续迭代])
```

### 通俗解释

这条主线相当于六个角色接力：

1. **产品经理**：把“我想做个东西”变成明确需求。
2. **架构师**：决定系统应如何实现。
3. **开发者**：按测试驱动方式写代码。
4. **独立 QA**：专门找开发遗漏的问题，不能偷偷修代码。
5. **交付负责人**：检查是否具备安全交付条件，但不擅自 push、merge 或 deploy。
6. **复盘负责人**：把本轮经验变成下一轮输入。

## 2. 每个阶段实际交付什么

```mermaid
flowchart LR
    A[模糊想法] -->|产品简述、来源、约束| B[write-prd]
    B -->|requirements-artifact| C[design-web-flow]
    B -->|acceptance-criteria-artifact| C
    C -->|design-contract| D[build-feature-tdd]
    B -->|需求与 AC| D
    D -->|change-artifact| E[qa-only]
    D -->|completion-evidence| F[ship-release]
    B -->|需求与 AC| E
    C -->|design-contract| E
    E -->|qa-verdict| F
    D -->|change-artifact| F
    F -->|release-package| G[retro-to-requirements]
    G -->|next-requirements| B
```

| 阶段 | 输入 | 主要输出 | 最关键的问题 |
|---|---|---|---|
| `write-prd` | 模糊想法、证据、约束、权限信息 | 需求、验收标准、需求 Gate 报告 | 到底要做什么，怎样才算完成？ |
| `design-web-flow` | 需求、验收标准、项目上下文 | 技术设计合同 | 如何实现，边界与失败路径是什么？ |
| `build-feature-tdd` | 需求、AC、设计、仓库、写入授权 | 代码变更、完成证据 | 是否先见 RED，再由真实测试证明 GREEN？ |
| `qa-only` | 需求、AC、设计、代码变更、QA 授权 | QA verdict | 开发者遗漏了什么？ |
| `ship-release` | 变更、测试证据、QA、仓库状态、交付政策 | 本地 release package | 是否真的具备交付条件，且没有越权？ |
| `retro-to-requirements` | 预期、实际、交付证据、决策、反馈 | 下一轮需求 | 本轮学到了什么，下一轮应改变什么？ |

## 3. 三条返工回路

系统并非一路向右，而是允许失败暴露后回跳。

```mermaid
flowchart LR
    I[实现] --> C{Completion Gate}
    C -- failed / needs-input -->|Correction feedback| I
    C -- passed --> Q[独立 QA]
    Q -- failed -->|qa-verdict 与复现证据| I
    Q -- passed --> S[交付预检]
    S --> R[复盘]
    R -->|next-requirements| P[下一轮需求]
    P --> I2[新一轮设计与实现]
```

- **实现内循环**：测试或完成证据失败，退回实现。
- **QA 回跳**：QA 只报告缺陷，由实现阶段修复，再重新 QA。
- **产品迭代循环**：复盘不是归档终点，而是下一轮需求入口。

真实 IP Rate Limiting 案例走过第二条回路：首版通过 6 项测试，QA 发现路由匹配过宽；扩展测试后出现 `1 failed, 11 passed`，退回修复，最终 `12 passed`。

## 4. 一次执行如何决定“复用、重跑或失效”

```mermaid
flowchart TD
    A[步骤准备执行] --> B[计算当前输入 hash 与 Slot/Recipe ref]
    B --> C{存在历史 passed evidence？}
    C -- 否 --> F[真实执行]
    C -- 是 --> D{ref、输入 hash、输出文件 hash<br/>及重新计算 Gate 全部匹配？}
    D -- 是 --> E[安全复用证据]
    D -- 否 --> G[将旧证据标记 invalidated]
    G --> H{为何失效？}
    H -- 上游重跑 --> H1[upstream-reran]
    H -- 输入或合同变化 --> H2[input-or-contract-changed]
    H1 --> F
    H2 --> F
    F --> I[保存新输出、执行证据与 hash]
    I --> J[下游步骤必须使用新证据重算]
```

因此，旧测试报告不能证明新代码；上游一变，下游不能继续冒用旧结论。

## 5. 模型与宿主如何分工

```mermaid
sequenceDiagram
    participant U as 用户/负责人
    participant O as Workflow Orchestrator
    participant M as AI 模型
    participant W as 隔离工作区
    participant H as 宿主测试执行器
    participant Q as 独立 QA
    participant G as Machine Gates

    U->>O: 提交想法、约束与授权
    O->>M: 只发送当前阶段所需输入
    M->>W: 在允许的工具范围内读取或修改
    H->>W: 执行固定测试命令
    H-->>O: 返回 exit code、stdout、stderr、耗时
    O->>G: 校验状态、结构、权限、patch 与 hashes
    G-->>O: passed / needs-input / blocked / failed
    O->>Q: 提供需求、设计、变更与黑盒证据
    Q-->>O: 只读 QA verdict
    alt QA failed
        O->>M: 发送 Correction feedback
        M->>W: 修复实现
        H->>W: 重新执行测试
    else QA passed
        O-->>U: 提交本地交付包与人工评审材料
    end
```

最重要的分工是：

- **AI 负责推理和产出**，但不能自行证明自己成功。
- **宿主负责执行测试并记录事实**。
- **QA 负责独立找问题，但无权修改源码**。
- **机器 Gate 负责核对结构、权限和证据一致性**。
- **人负责判断业务语义是否真的正确**。

## 6. 权限与安全边界

```mermaid
flowchart TB
    subgraph M[模型可见能力]
      R[只读阶段：read]
      W[实现阶段：read / edit / write]
    end

    subgraph H[仅宿主掌握]
      T[固定测试命令]
      S[隔离 snapshot / worktree]
      P[生成 full 与 incremental patch]
      E[记录 exit code、stdout、stderr、duration、hash]
    end

    subgraph D[默认禁止]
      N[network]
      RG[remote Git]
      MG[merge]
      DP[deploy]
      B[bash 暴露给模型]
    end

    R --> E
    W --> S
    S --> T
    T --> E
    S --> P
    N -. security Gate 拒绝 .-> E
    RG -. security Gate 拒绝 .-> E
    MG -. security Gate 拒绝 .-> E
    DP -. security Gate 拒绝 .-> E
    B -. security Gate 拒绝 .-> E
```

注意：这里证明的是**模型工具层和执行合同层**的限制；它不冒充通用 OS 级网络沙箱。

## 7. 发布为何需要“两把钥匙”

```mermaid
flowchart TD
    A[候选 Slots / Recipes] --> B[真实项目执行]
    B --> C[Baseline suites]
    B --> D[Candidate suites]
    B --> E[Holdout suites]
    B --> F[Mutation suites]
    C --> G{机器 Release Gate}
    D --> G
    E --> G
    F --> G
    G -->|逐 case 重算| H[核对 run identity、duration、工具事件、命令、输出文件与 SHA-256]
    H --> I{全部通过？}
    I -- 否 --> J[保持 evaluating / blocked]
    I -- 是 --> K{六阶段人工语义评审批准？}
    K -- 否 --> J
    K -- 是 --> L[受控 publish]
    L --> M[status = released]
```

机器判断“证据是否真实一致”；人判断“需求、设计和行为是否符合真正意图”。任一把钥匙缺失，不能发布。

## 8. 状态机：流程会停在哪里

```mermaid
stateDiagram-v2
    [*] --> pending
    pending --> running: 输入与权限齐备
    pending --> needs_input: 缺关键事实
    pending --> blocked: 权限或合同不允许
    running --> passed: 输出与 Gate 均通过
    running --> needs_input: 发现不可安全假设的未知项
    running --> blocked: 权限、依赖或安全边界阻断
    running --> failed: 执行、测试或 Gate 失败
    failed --> running: 带 feedback 重跑
    needs_input --> running: 用户补充信息
    blocked --> running: 阻断原因被解决并重新授权
    passed --> invalidated: 上游重跑或输入/合同变化
    invalidated --> running: 重算
    passed --> [*]
```

`needs-input` 不是失败，而是系统拒绝脑补；`blocked` 表示当前权限或条件不允许继续；`failed` 表示已经真实尝试但验证失败。

## 9. 真实案例的运行轨迹

```mermaid
flowchart LR
    A[需求：为 MirrorMind 增加 IP Rate Limiting] --> B[冻结需求、边界与 6 项初始验收测试]
    B --> C[初始 RED：模块不存在]
    C --> D[隔离 worktree 实现首版]
    D --> E[宿主测试：6 passed]
    E --> F[独立 QA 扩展黑盒场景]
    F --> G[发现嵌套路由误匹配]
    G --> H[QA RED：1 failed, 11 passed]
    H --> I[qa-verdict 回跳实现]
    I --> J[生成 incremental correction patch]
    J --> K[宿主复测：12 passed]
    K --> L[交付预检通过]
    L --> M[复盘回流；缺生产数据时返回 needs-input]
    M --> N[机器 Gate + 人工评审]
    N --> O[受控发布]
```

这条轨迹说明系统的价值不在于“第一次便完美”，而在于错误会暴露、返工有边界、修复后必须重新举证。

## 10. 如何判断“整套系统完全完成”

```mermaid
mindmap
  root((完成定义))
    业务正确
      需求来源可追踪
      验收标准可观察
      人工语义批准
    技术正确
      设计边界明确
      RED 到 GREEN
      独立 QA 通过
    证据可信
      真实命令与退出码
      原始模型输出
      patch 与 SHA-256
      snapshot 身份一致
    安全受控
      最小工具权限
      QA 只读
      无未授权网络与远端 Git
      无擅自 merge / deploy
    可持续迭代
      失败可回跳
      旧证据会失效
      复盘进入下一轮需求
```

“完成”不是文件都生成了，而是：

```text
业务语义正确
× 实现和测试正确
× 独立 QA 可信
× 证据链可复算
× 发布获得授权
```

任何一项为零，整体都不应被称为完成。

## 11. 项目中的对应实现

| 机制 | 主要文件 |
|---|---|
| 六阶段总编排 | `recipes/full-dev-loop.json` |
| 需求 / 设计 / 实现 / QA / 交付 / 复盘 | `recipes/*.json` |
| 状态、恢复与证据复用 | `tools/curation/workflow_state.py`、`tools/curation/recipe_execute.py` |
| 隔离执行、宿主测试与 patch | `tools/curation/execution_adapters.py` |
| 安全边界 Gate | `tools/curation/full_dev_loop_security.py` |
| 完整证据清单 | `tools/curation/full_dev_loop_evidence.py` |
| 生命周期与回跳验证 | `tools/curation/full_dev_loop_lifecycle.py` |
| 复盘回流验证 | `tools/curation/full_dev_loop_feedback.py` |
| 最终发布 Gate | `tools/curation/full_dev_loop_release_gate.py` |
| 受控发布器 | `tools/curation/publish_full_dev_loop.py` |
| 真实运行证据 | `evals/runs/full-dev-loop/ip-rate-limiting-v1/` |
| 权威机器结果 | `curation/gate-report.json`、`curation/final-audit.json` |

## 12. 最简记忆版

```mermaid
flowchart LR
    A[想清楚] --> B[设计清楚] --> C[先测再写] --> D[独立挑错] --> E[证据交付] --> F[复盘迭代]
    D -- 有问题 --> C
    F -- 新认识 --> A
```

一句话：**把模糊想法逐步变成需求、设计、代码、测试和交付证据；允许失败返工，但不允许未经验证便宣称完成。**
