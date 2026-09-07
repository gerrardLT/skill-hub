# Brownfield Rescue 示例

## 基线发现

- 产品定位与真实使用人群不一致。
- 核心流程存在 17 个未定义状态。
- 后端模块共享数据库表，缺少所有权边界。
- 自动化测试很多，但关键支付旅程没有真实集成验证。
- 部署可自动执行，但没有回滚演练和生产业务指标。

## 推荐路由

先进入 Evolution/DIAGNOSE 建立用户与运行基线，再分别回流 PM/STRATEGY、Design/USER_FLOWS、Engineering/ARCHITECTURE。修复波次必须逐个经过 QA 与 Release，不进行大爆炸重写。
