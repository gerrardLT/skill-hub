# azure-reliability 来源能力档案

## Problem

识别并修复 Azure Functions 与 App Service 在可用区、存储、健康探针和多区域容灾上的单点故障。

## When to Use

用于评估或提升 Functions/App Service 的可靠性、区域冗余、高可用和灾备能力。

## When Not to Use

不深度评估 Container Apps 或其他未支持计算服务；不替代完整预部署验证或一般部署技能。

## Role

Azure PaaS 可靠性评估与分阶段整改控制器。

## Inputs

目标 subscription/resource group/app 范围、Azure 登录状态、现有资源与 IaC、用户选择的 CLI 或 IaC 路径及变更确认。

## Outputs

四项 feature-pivoted checklist、整改计划、CLI 变更或 Bicep/Terraform patch、部署结果与重评估。

## Workflow

发现资源并严格限定查询范围；做平台检查和支持服务 deep dive；输出四项表；确认后先做 quick wins；单独确认存储迁移；重评估；条件满足后再询问多区域。

## Branches

CLI 即时修复或 IaC patch；Bicep/Terraform 检测；存储 yes/no/later；核心项目全绿后才提供多区域分支；不支持资源标记 not assessed。

## Rules

不打分；表格固定特性顺序；变更前展示成本和破坏性影响；quick wins 与存储迁移分两次部署；多区域必须显式同意。

## Exceptions

若核心能力已全开，跳过 fix-it 直接询问多区域；FC1/Consumption 健康端点属于需同意的代码改动；长存储迁移可暂停等待。

## Dependencies

Azure CLI、Resource Graph 扩展、Azure MCP 工具；Reader 用于评估，Contributor 用于配置；可选 azd/Bicep/Terraform。

## Permissions and Side Effects

读取 Azure 资源；经确认后修改 live resources、源代码或 IaC，并可能执行部署、重启应用、迁移存储和新增跨区域资源及成本。

## Gates

所有写操作前确认；Deploy 1 前确认；存储迁移单独确认；Deploy 2 前确认；多区域生成或部署前再次确认。

## Open Questions

顶层 SKILL.md 对 App Service 支持的描述与 Phase 1 “non-Functions 不 deep-dive”文字存在张力，应在平台适配提纯时澄清。

## Unique Value

以功能为轴而非资源为轴呈现可靠性缺口，并用风险分层的两次部署流程隔离快速安全修复与长时迁移。

## Reading Coverage

本轮只完整读取了顶层 `skills/azure-reliability/SKILL.md`。reachable supporting files 未做本轮语义拆解，详见 `curation/coverage.json` 中各 excluded reason；不得据此视为已阅读附件、references、scripts 或其他子技能。
