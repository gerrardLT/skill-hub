# 安全模型

## 信任边界

- 用户与 Agent 输入默认不可信。
- 第三方 Skill、脚本、Hook 和安装命令默认不可信。
- 本地文件可被绕过 CLI 修改；Gate 必须重新哈希并传播 stale。
- Bearer Token 只代表主体，不代表任务内容正确。
- 数据库 lease 过期后，旧执行者可能仍在运行；外部副作用必须校验 fencing token。

## 关键控制

- RBAC 和最小权限；高保障审批职责分离。
- AES-GCM Secret，加密上下文绑定 project/name/version。
- 审批与项目 revision 绑定。
- 链式审计和 revision snapshot。
- Skill 锁、静态扫描、许可证审查和严格拒绝未解析依赖。
- Prompt injection、工具权限、支付/账本、租户隔离等由领域包加强。

## 非目标

本系统不是完整 IAM、SIEM、KMS、WAF 或合规认证产品。生产部署必须接入组织现有安全平台。
