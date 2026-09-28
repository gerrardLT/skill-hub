# 六阶段契约

| 阶段 | Recipe | 核心边界 | 失败语义 |
|---|---|---|---|
| 需求 | `write-prd@1.0.0` | 事实、规则、未知项、AC 与只读质量 Gate | 缺输入停止；质量失败回需求规则 |
| 设计 | `design-web-flow@1.0.0` | 从已批准需求形成设计方向 Contract，不编码 | 缺权威停止；越界阻断 |
| 实现 | `build-feature-tdd@1.0.0` | 仅在显式 `workspace-write` 授权下，于隔离 worktree 做 RED/GREEN/重构 | 完成 Gate 失败回实现；预算耗尽阻断 |
| QA | `qa-only@1.0.0` | 独立、只读、只报不修 | 缺陷记录并回实现，不改源码 |
| 交付 | `ship-release@1.0.0` | 默认只做交付预检和 release-ready 包 | 缺证据阻断；无授权不 push/merge/deploy |
| 复盘 | `retro-to-requirements@1.0.0` | 用实际证据生成下一轮需求输入 | 缺实际数据停止；不编造根因 |

完整闭环 `full-dev-loop@1.0.0` 精确引用上述六个 Recipe，不内联 Slot 方法。复盘产物 `next-requirements` 映射到下一轮 `write-prd.validated-product-brief`。

共同 Gate：

```text
evidence-present
unknowns-preserved
authority-boundary
responsibility-boundary
```

任一步只有状态为 `passed` 且当前 Gate 证据有效，方可推进。
