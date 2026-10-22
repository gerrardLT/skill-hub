# 完全优化：已确认工程合同

用户确认：全目录验收、按证据修复；记录 token 预算上限 50,000,000。父级直接执行，不授权子代理。

## 最终状态

隔离的新候选通过结构、权限、执行质量和 routing 验收，无未处置的跨题集回退、越权或编造；出题 incomplete 补齐。未达标不得宣称完全优化。

## 验收

沿用上轮运行前冻结阈值：old 与 fresh 胜数均不低于负数，两个题集均出现负的 Skill 必须处理；新增 overreach/fabrication 必须人工复核并解决。全目录154个Skill覆盖；27个protected steps仍禁用；当前prompt/output/judge绑定完整。结构测试、1.0.0 Phase12 Gate通过。routing使用用户已批准的纠正题集，历史失败保留。

## 不变量

原始skills、已发布1.0.0、上一轮候选及失败证据只读；权限只窄化。禁止放宽阈值、删除失败、伪造运行证据或复用已作废结果。未见题不得用于修订后仍称holdout。

## 边界

允许新增 optimization-1.1.0 控制目录、隔离候选与eval runs；允许按证据修改相关工具和测试，须避免破坏Phase12 rollback postimage。不commit、push、PR、merge、deploy、provider mutation、browser login、credential action或生产访问。正式发布另需exact preview审批。

## 迭代与停止

先看失败证据，保存假设账本；最小根因改动、可运行回归检查、未见题试点，再全量验证。连续两轮无改善或provider阻塞则停下诊断，不自行换协议。模型沿用router9-qoder/cx/gpt-5.6-sol执行、router9-qoder/kr/claude-opus-5.5出题评判，fresh无工具进程、空cwd、环境白名单。

本任务新增调用的记录totalTokens上限50,000,000，失败/重试/探针均计入；缺失usage不视为免费，报告单列未知成本。达到上限停止并汇报。全部验收通过才GOAL_COMPLETE；预算或基础设施阻塞则报告实际未完成项。

## 假设账本

- 边界过严导致少交付：evidence synthesis拒绝排名；应以显式跨Skill handoff与Recipe接续完成请求，不混同决策批准。
- 操作细节丢失：部署rollback、digest、授权绑定和bootstrap依赖恢复需要契约及回归检查。
- 动画实现错误：reduced motion不得依赖transitionend；阈值和状态须可运行验证。
- 未知事实误写为已知：MR open等仅据输入声明，否则标unknown。

## 轮次记录

O0：用户确认全目录验收及50,000,000记录token预算。尚未修改上一轮候选，尚未启动新模型评测。
