# aus-ele 真实 Brownfield Dogfooding — v2.1

## 结论

`DONE_WITH_CONCERNS`：真实代码缺陷已修复并通过本地目标回归；Release-ready 通过；Production-ready 被正确阻断。Dogfooding 同时暴露并修复了 v2.0 四类流程缺陷。

## 项目证据

- 项目 Profile：high-assurance；工作项 `WORK-NPM-LOCK` Profile：lite / low，risk=7.4。
- 修改范围：仅 `web/package-lock.json`。
- 修复前：106 个 `registry.npmmirror.com`；目标仓库测试 FAIL。
- 修复后：0 个；106 个地址切换至 `registry.npmjs.org`；package 键集合不变，355 个条目。
- Docker artifacts：3/3 PASS。
- 前端 Node：317/317 PASS。
- 后端完整套件：运行 725 个，0 FAIL / 248 ERROR；错误受当前环境缺 `psycopg2`/PostgreSQL 等依赖约束。
- 前端 build：未完成，当前环境无 node_modules 且网络不可用。
- Production-ready：FAIL，缺真实 deployment evidence 与 production verification；未 Force/Waive。

## v2.0 → v2.1 实战修复

1. 项目级 Profile 改为 Project + Work Item 双层风险裁剪。
2. Artifact/Evidence/Risk/Decision/Trace/Run/Learning 绑定 Work Item，禁止跨变更借旧证据过 Gate。
3. Artifact/Trace/Quality/Health 按制品所属 Work Item Profile 复核，避免 high-assurance 项目误杀 lite 小修复。
4. Domain Pack 按 Work Item 实际影响启用，并将 bounded-lite 压缩为 Change Plan → Change Verification → Release Recommendation；Engineering/QA 使用压缩状态机。

## 证据边界

本试点证明 v2.1 可以在真实 Brownfield 仓库中识别缺陷、执行修复、保留审计、按变更裁剪并正确阻断无生产证据的发布。它不证明整体提效、降本或降低长期缺陷率。
