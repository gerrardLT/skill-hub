# Venue Reservation Pilot - Source Requirements

- Source file: `requirements.xlsx`
- Source SHA-256: `2ca5adada91ea5a5967382e2d2aca480c94585b12fd908cb44c00f195816e7bc`
- Selection rule: D26, D33, reservation/waitlist/hold state invariants, and outcome metrics.
- Purpose: preserve a reproducible, narrow vertical slice rather than reinterpret the full product backlog.

## Product capabilities

| ID | 功能 | 级别 | 解决问题 | 触发 | 输入 | 状态/输出 | 主流程 | 核心规则 | 异常边界 | 交互设计 | 后台配置 | 自动化/通知 | 数据/KPI | 权限/审计 | 验收 | 研究依据 | 依据URL |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| D26 | 球台地图与动态锁台 | 核心+特色 | 传统“选日期再分配任意球台”无法表达球台偏好、VIP台、训练台和设备状态，也难处理高峰并发。 | 订台、换台、续时、赛事占台 | TableResource、时段库存、会员等级、价格、维护状态 | AVAILABLE/HELD/RESERVED/IN_USE/CLEANING/MAINTENANCE | 地图选台→连续时段选择→Hold→支付/权益→订台→签到→使用→续时/结束 | Table Hold原子唯一；维护/赛事为硬占用；连续时段必须完整可用；会员等级只影响可订窗口/价格而非随机抢占。 | 支付回调晚到、换台、临时封台、赛事超时 | 区域地图+球台编号+状态；默认推荐最匹配球台，也允许手选；失败推荐最近可用台。 | 球台类型、区域、峰谷价格、Hold TTL、清洁缓冲、维护窗 | 球台故障/被赛事占用自动通知并生成换台任务 | 球台利用率、峰时满台率、每台小时收入、换台率 | 强制封台/换台记录原因 | 100并发抢同一球台时段不超卖；换台不重复收费 | PingPod / TT Clubs | https://pingpod.com/membership/<br>https://www.tabletennisengland.co.uk/clubs/tt-clubs/ |
| D33 | 抢课公平队列与反超售 | 核心+特色 | 热门训练课同时开抢会因网络差异、重复请求和脚本造成不公平/超售。 | 用户截图：抢课功能；结合Seat Hold与候补机制。 | 确保“同规则下公平、绝不超售、失败有候补去向”。 | 服务端统一开放→请求签发token→资格预检→排队→原子SeatHold→预约/支付→失败释放→未抢到自动提示候补。 | QueueToken WAITING→ADMITTED/EXPIRED；SeatHold HELD→CONVERTED/RELEASED | 以服务端时钟为准；会员同场次只允许一个有效token；限频/设备风控；支付不永久占位。 | 断网、重复点击、token超时、付款晚回调。 | 明确排队状态/当前结果；不做虚假倒计时；失败直接提供候补。 | QueueToken / SeatHold / Reservation / RiskEvent | 超售=0、排队成功率、P95等待、候补转正率 | 用户上传智火功能截图 | P1 |  |  |  |

## State machines and invariants

| 对象 | 中文名 | 状态/主要迁移 | 关键不变量 | 恢复/补偿 |
|---|---|---|---|---|
| Reservation | 预约 | ELIGIBILITY_CHECK→HELD→RESERVED→CHECKED_IN→ATTENDED/COMPLETED；支路：CANCELED_EARLY/LATE_CANCELED/NO_SHOW | RESERVED必须占用1个名额；完成后不可直接回到预约 | 取消释放库存；错误考勤走更正/冲正 |
| WaitlistEntry | 候补 | WAITLISTED→AUTO_PROMOTED或OFFERED→ACCEPTED/DECLINED/EXPIRED；也可CANCELED | 同会员同场次最多1个有效候补；转正前二次资格 | 失败跳过下一位并记录reason_code |
| SeatHold | 名额/Spot短锁 | HELD→CONVERTED/EXPIRED/RELEASED | TTL内唯一占用；不可超过场次/Spot库存 | 定时释放；支付成功未转预约进入补偿 |
| Session | 训练课程场次 | DRAFT→PUBLISHED/OPEN→FULL/WAITLIST_OPEN→CHECKIN_OPEN→IN_PROGRESS→COMPLETED；支路CANCELED | 已预约场次重大变更必须影响分析 | 取消触发会员通知、退款/退权益和候补清理 |
| R02 | 硬限制先行 | 安全/欠费/黑名单/库存/时间冲突等硬限制先于营销优惠 | 避免“有优惠券所以绕过资格”。 |  |
| R08 | 幂等与不可变流水 | 支付/课消/提成/退款采用不可变事件和冲正 | 保障财务可追溯。 |  |

## Product metrics

| 指标 | 口径/公式 | 主要事件源 | 设计注意 |
|---|---|---|---|
| 预约成功率 | 成功创建正式预约人数/预约提交人数 | Reservation | 按门店/课程/卡项/原因码下钻 |
| 候补转正率 | 转正式预约/候补人数 | WaitlistEntry | 分自动/确认/Quick Fill |
| 空位填补率 | 因取消产生且最终被填补空位/取消释放空位 | Reservation+Waitlist | 衡量候补价值 |
| 平均候补等待时长 | 转正时间-加入候补时间平均 | WaitlistEntry | 分课程/时段 |
| 球台利用率 | 实际被占用球台分钟 / 可售球台分钟 | TableReservation / CheckIn | 按门店/区域/球台/时段切片；维护时段从可售分母剔除 |

## Pilot commitment

The implementation must allocate capacity atomically, maintain one active reservation or waitlist entry per member and session, use FIFO promotion, make retries idempotent, preserve an immutable audit trail, expose actionable error states, and prove that concurrent demand cannot oversell capacity.
