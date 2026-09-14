# AI 中文搜索工具 PRD（Purified — TC01）

> 生成方式：pr_to_ac_concise 提纯方法——单轮直出，内嵌问题定义/优先级/AC 规则，跳过 workshop 交互协议。
> 同一输入：「我想做一个 AI 搜索工具，像 Perplexity 但更聚焦中文内容」

## 📌 Executive Summary

做一个专注中文的答案优先 AI 搜索：中文信源检索 + 逐句引用生成。解决现有英文优先工具在中文查询上信源失配、答案无据的问题。

## ❓ Problem Statement

中文用户用 Perplexity/ChatGPT 搜索中文内容时，答案质量差、引用缺失。假设：中文优质信源未被有效索引。用户被迫手动翻网页验证。

## 👥 Target Users

- **研究者**：查中文文献与数据，需要带出处的答案
- **内容创作者**：事实核查，确认数据原始出处

## ✅ User Stories & Acceptance Criteria

**P0**

**US-1 带引用的中文答案**
- AC-1 Given 中文问题提交 When 答案生成 Then 每个事实论断带编号引用
- AC-2 Given 引用编号被点击 When 跳转 Then 定位到信源卡片与原文摘录
- AC-3 Given 查询无可靠信源 When 生成 Then 明确提示"未找到可靠信源"，禁止编造

**P1**

**US-2 信源可信度标签**
- AC-4 Given 信源卡片展示 When 加载 Then 显示域名+可信度标签（官方/媒体/社区/未验证）

**US-3 追问深挖**
- AC-5 Given 某引用存在 When 用户追问 Then 返回该信源相关段落

## ⚠️ Open Questions

1. 用户搜索频率与付费意愿？（影响商业模式）
2. Perplexity 中文质量差距的量化证据？（验证核心假设）
3. 中文信源抓取的版权合规边界？（影响技术路线）
4. 竞品（秘塔等）市场验证数据？（影响进入策略）

## 🚫 Out of Scope

写作助手功能、移动原生 App、账号体系、英文专门优化
