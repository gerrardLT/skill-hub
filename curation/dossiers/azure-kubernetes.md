# azure-kubernetes 来源能力档案

## Problem

依据需求规划和配置生产级 AKS，特别保护难以事后变更的网络与 API server Day-0 决策。

## When to Use

用于新建 AKS、选择 Automatic/Standard、设计网络与身份、配置治理、可观测性、升级、扩缩、可靠性和成本控制。

## When Not to Use

不用于向既有集群部署应用或一般 AKS 故障诊断；这些分别交给相关 Azure 技能。

## Role

AKS 集群规划与配置顾问，输出带理由的推荐配置和 Day-0 checklist。

## Inputs

环境类型、区域与可用区、节点规格和规模、网络、身份与镜像仓库、安全、升级、可观测性及成本要求。

## Outputs

推荐的 AKS SKU、网络、安全、观测、升级、节点池、可靠性与成本配置，以及必要命令建议。

## Workflow

收集必要需求；优先选择 Automatic；依次确定网络、安全、观测、升级、性能、节点池、可靠性和成本；按具体场景分派 deep-dive。

## Branches

默认 Automatic；需要自定义网络、扩缩或节点池时选 Standard；pod 可路由需求决定 CNI 模型；rightsizing、VPA、autoscaler、Spot 分派对应参考。

## Rules

先发现 AKS MCP 工具并选最小适用工具，CLI 仅作 fallback；记录 Day-0 决策理由；生产避免 B-series，节点至少 4 vCPU，并采用身份、策略和可用区保护。

## Exceptions

模糊的 Day-0 决策必须追问；Day-1 功能可给安全选项与保守默认；不承诺零停机。

## Dependencies

Azure MCP 的 AKS 入口，或 Azure CLI `az aks` 与 `kubectl`；Azure 身份、订阅与资源上下文。

## Permissions and Side Effects

可能创建或修改 AKS、网络、身份、策略、日志和节点池资源；不得请求或输出 secrets 或要求粘贴 subscription ID。

## Gates

确认目标环境与关键 Day-0 要求；先解析 Azure scope；执行前选择正确 SKU、网络和安全配置；错误时核验登录、quota 与 IP 空间。

## Open Questions

顶层 SKILL.md 未定义最终推荐配置的固定输出模板。

## Unique Value

将 AKS 的不可逆 Day-0 决策与可后置 Day-1 能力分离，并给出面向生产的统一默认基线。

## Reading Coverage

本轮只完整读取了顶层 `skills/azure-kubernetes/SKILL.md`。reachable supporting files 未做本轮语义拆解，详见 `curation/coverage.json` 中各 excluded reason；不得据此视为已阅读附件、references、scripts 或其他子技能。
