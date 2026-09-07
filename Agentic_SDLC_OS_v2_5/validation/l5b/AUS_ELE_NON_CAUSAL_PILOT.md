# aus-ele L5-B 非因果预演

状态：**INVALID FOR CAUSAL CLAIM / 仅用于工具链与验收口径预演**。

同一执行者已经看过 SDLC arm，再运行 baseline arm，因此存在明确 cross-arm contamination；也没有独立盲评和可比 Token/人工时间记录。不能把本结果称为正式 L5-B。

## Baseline direct arm

- 从未修复的归一化源码复制独立 arm。
- 仅执行 106 个 registry host 替换。
- 结果 SHA-256 与 SDLC arm 完全一致：`bb15d4e7e26f0d419c7eeac28f0ab27d2c5330fd6de37a317668463215657c43`。
- Docker artifact：3/3 PASS，执行 wall time 约 0.59s。
- 前端 Node：317/317 PASS，执行 wall time 约 0.87s。

## SDLC arm

- 产出相同代码结果并通过相同目标测试。
- 额外提供 Work Item 风险裁剪、Artifact/Evidence 作用域、Gate、Trace、Audit、Release/Production 边界。
- v2.0 在此类微小变更上的治理开销过高，直接促成 v2.1 bounded-lite 压缩。

## 可得结论

- 两个 arm 的机械修复正确性相同。
- 对这个极小修复，额外 SDLC 控制的价值主要是治理与可审计性，不应假设能缩短机械执行时间。
- 正式 L5-B 必须由独立执行者、冻结任务、匹配工具/模型、盲评并记录 Token/人工时间后重新运行。
