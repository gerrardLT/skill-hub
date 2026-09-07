# Incident 示例：支付成功但订单未生成

## 事实

- 09:41 新版本开始灰度。
- 09:47 支付回调成功率正常，订单创建错误率升高。
- 受影响范围仅新版本流量。

## 竞争假设

1. 新版本事件结构与订单消费者不兼容。
2. 消费者积压导致观察窗口内延迟。
3. 幂等键变化触发错误去重。

## 路由

Evolution/TRIAGE → Release 授权回滚/冻结灰度 → Evolution/DIAGNOSE → Engineering 最小修复 → QA 回归 → Release canary → Evolution learning-decision。

不要把时间相关性直接当成根因；需要消息样本、消费者日志、队列延迟和版本差异证据。
