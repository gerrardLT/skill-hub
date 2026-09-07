# 乒乓球馆 VenueOS — Rally Atelier / 回合艺境
## Google Stitch + 艺术审美 + App UI/UX 完整设计文档

> Combined edition. 实际 Stitch 使用时请优先使用 `.stitch/DESIGN.md` 与 `.stitch/SITE.md`。

---
# PART I — 艺术审美与 App UI/UX 总纲
# 乒乓球馆 VenueOS — Rally Atelier / 回合艺境
## 艺术审美、Google Stitch 设计系统与 App UI/UX 总纲

> 版本：2026-08-28  
> 功能基线：`乒乓球馆SaaS_完整闭环功能清单_20260828_V2_图片功能融合版.xlsx`  
> Stitch 视觉源：`.stitch/DESIGN.md`  
> Stitch 页面源：`.stitch/SITE.md`

---

# 1. 最终结论

这套系统不应该继续沿用此前为“泛场馆 / Pilates / wellness”推导出的视觉语境。乒乓球的身体节奏、空间结构、时间库存和竞技关系与普拉提完全不同。

最终建议主题：

# **Rally Atelier / 回合艺境**

它不是“传统体育蓝”，不是“红黑电竞”，也不是“黑金会所”。

它把乒乓球拆成三个最有设计价值的视觉原语：

1. **Precision Geometry / 精准几何**  
   球台、边线、中线、网、时间槽、比分都是严格结构。

2. **Spin Trajectory / 旋转轨迹**  
   乒乓球最独特的不是速度本身，而是旋转、弧线、落点和方向变化。

3. **Rally Rhythm / 回合节奏**  
   订台、抢课、候补、比分、签到都是高频快速状态变化，动效应该像回合：短、准、可预期。

整体艺术母题可以描述为：

> **一张被精确照亮的比赛球台，置于当代建筑式精品球馆中；信息像场馆导视一样克制，交互像击球一样快速明确。**

消费者端是“**精品球馆数字前厅**”；员工端是“**现场赛事/运营工作台**”；管理端是“**精密球馆驾驶舱**”。

---

# 2. 为什么乒乓球必须重新设计

从功能清单看，本系统实际包含：

- 球台预约、地图选台、连续时段；
- 教练 / 陪练预约；
- 团训、小班、少儿/成人固定班；
- 候补、抢课、迟取消、No-show；
- 会员卡、时长卡、训练课包、储值；
- 球台 / 课程签到与课消；
- 球友匹配、公开约球、水平等级；
- 赛事报名、签表、比分、Rating；
- 发球机 / 球拍 / 器材；
- 支付、退款、对账；
- CRM、会员360、续费、生命周期；
- 员工权限、教练关系、提成；
- 多门店、经营数据、私有化部署。

这意味着前端不是“课程商城”。它是一个**实时资源系统 + 会员系统 + 社交竞技系统**。

乒乓球 App 需要比普通预约 App 更强地表达：

- 时间；
- 球台库存；
- 球台类型；
- 参与者；
- 水平；
- 当前状态；
- 竞争性 / 友好局；
- 分账；
- 下一场；
- 比分变化。

所以视觉必须同时具备**秩序感**和**动势感**。

---

# 3. 多轮调研

本次设计采用四轮调研，而不是从一个 App 直接抄视觉。

## 3.1 第一轮：乒乓球本体与职业赛事视觉

### World Table Tennis / WTT

官方资料：
- https://www.worldtabletennis.com/aboutus
- https://www.worldtabletennis.com/teamarticle?article_no=team_partners
- https://www.worldtabletennis.com/description?artId=5841

得到的关键启发：

### A. “一张台”的聚焦能力

WTT 近年的场馆表现强调单台、灯光聚焦的 Infinity Arena 逻辑：环境降低存在感，球台成为视觉中心。

这对于 App 很重要：

> 一个屏幕只能有一个“被照亮的球台”。

例如：

- 首页：下一次预约；
- 订台：当前选择的时间；
- 选台：当前选择球台；
- 候补：当前位次；
- 比赛：下一场；
- 会员：当前最重要权益。

这形成本方案的 **One-Table Rule / 单台聚焦原则**。

### B. 乒乓球需要现代化，而不是传统协会风

WTT 对品牌的目标之一是用更现代、更专业的方式重塑乒乓球呈现。

因此 UI 不使用：

- 红黄体育馆宣传板；
- 奖杯、火焰、盾牌的大量图形；
- 传统体育协会信息密度。

---

## 3.2 第二轮：真实球馆数字服务

### PingPod

官方资料：
- https://pingpod.com/
- https://pingpod.com/pricing/
- https://pingpod.com/membership/
- https://pingpod.com/classes/

重要发现：

PingPod 已经把乒乓球馆设计成一种数字化空间服务：

- 自动订台；
- contactless check-in；
- 24/7；
- 课程；
- 联赛 / 活动；
- 会员；
- robot table；
- 自动分配最佳球台；
- 指定球台可额外收费；
- 高峰 / 非高峰价格和会员权益不同。

这说明现代乒乓球馆的前端核心不是“课程列表”，而是：

> **时间库存 + 球台库存 + 会员权益 + 无人化履约。**

因此本方案把“订台”独立成 App 一级入口。

---

## 3.3 第三轮：成熟拍类运动预订与社交

### Playtomic

官方资料：
- https://playerhelp.playtomic.com/hc/en-gb/articles/19831881490449-How-to-make-a-reservation-in-Playtomic-app
- https://playerhelp.playtomic.com/hc/en-gb/articles/19831715222929-How-to-book-a-court-or-a-spot-in-a-match-in-your-favourite-Club
- https://playerhelp.playtomic.com/hc/en-gb/articles/19831958258193-Private-Bookings-vs-Open-Matches
- https://playerhelp.playtomic.com/hc/en-gb/articles/19832089052561-How-to-split-the-payment-of-a-reservation
- https://playerhelp.playtomic.com/hc/en-gb/articles/19831425477649-What-is-a-Club-Membership

Playtomic 在 2026 年的预订流程中明确使用：

`运动 → 地点 → 日期时间 → 场地 → 时长 → 分账/全付 → 取消规则 → 支付`

得到的关键启发：

### A. 私人订台与公开约球必须是两个心智模型

私人订台：

> 我已经知道和谁打，只需要一张台。

公开约球：

> 我需要找到合适的人，再确定一场球。

不能把这两个流程塞进同一个“预约”页。

### B. 费用必须在承诺前完整可见

价格、会员优惠、分账、取消规则都要在确认层出现。

### C. 自动推荐可以减少选择

普通用户不一定关心是 A03 还是 A06；系统可以默认“智能分配”，高级用户再进入地图手选。

这会显著降低认知负荷。

---

## 3.4 第四轮：设计系统、动效与心理学

### Google DESIGN.md / Stitch

官方资料：
- https://github.com/google-labs-code/design.md
- https://github.com/google-labs-code/design.md/blob/main/PHILOSOPHY.md
- https://github.com/google-labs-code/stitch-skills

核心原则：

- YAML frontmatter 提供机器可读 token；
- Markdown prose 表达设计意图；
- Google 官方明确强调：**真正决定设计质量的是 prose 中的“为什么”和具体参考世界，而不是 token 数量。**

因此此次 DESIGN.md 不只提供颜色/字号，而是写明：

- 什么是高级感；
- 为什么使用该色；
- 什么时候能用红色；
- 球台地图应该是什么心理模型；
- 动效为什么存在；
- 哪些视觉必须禁止。

### Apple HIG Motion

官方资料：
- https://developer.apple.com/design/human-interface-guidelines/motion
- https://developer.apple.com/design/human-interface-guidelines/design-principles
- https://developer.apple.com/design/human-interface-guidelines/accessibility

吸收原则：

- 动效必须有目的；
- 反馈要短且精确；
- 动画不应阻塞用户；
- 状态变化要有明确反馈；
- Reduce Motion 必须有降级策略；
- 可恢复与用户控制权是信任的一部分。

### Material 3 Expressive 2026

官方资料：
- https://m3.material.io/
- https://developer.android.com/reference/kotlin/androidx/compose/material3/MotionScheme

吸收原则：

- recurring interaction 使用 standard motion；
- hero / prominent interaction 才使用 expressive spatial motion；
- shape、motion、type 可以共同建立情绪；
- spring 应用于空间运动，color/alpha 使用不 overshoot 的 effect motion。

### VisAWI

审美评价采用四维框架：

- Simplicity
- Diversity
- Colorfulness
- Craftsmanship

乒乓球馆 App 目标权重：

| 维度 | 目标 | 原因 |
|---|---:|---|
| Simplicity | 6.4/7 | 高频预约必须极快 |
| Diversity | 5.7/7 | 需要运动感和品牌识别 |
| Colorfulness | 5.1/7 | 颜色应克制而成熟 |
| Craftsmanship | 6.7/7 | 高级感最关键来源 |

目标不是“丰富”，而是**工艺感**。

---

# 4. 主题世界：Rally Atelier / 回合艺境

## 4.1 一句话定义

> **Precision sports club meets contemporary gallery.**

中文：

> **竞技精度 × 当代艺廊 × 数字球馆。**

## 4.2 视觉联想

不是：

- 电竞馆；
- 传统体育局；
- 健身房；
- SPA；
- 商城；
- 儿童培训机构。

而是：

- 当代建筑空间；
- 专业比赛场地；
- 高端运动器材；
- 精密计时设备；
- 编辑式运动摄影；
- 有控制的动态光线。

## 4.3 设计人格

### Precise / 精准

球台与时间的结构不允许模糊。

### Kinetic / 动势

动效来自旋转与回合，而非无意义飘动。

### Tactile / 触感

点击、选台、签到、比分确认有清晰的物理反馈。

### Calm / 克制

每日使用界面必须安静，不能像赛事直播页。

### Competitive / 竞技

赛事、比分、Rating 有更强张力，但不破坏主系统。

---

# 5. 色彩系统

完整 token 见 `.stitch/DESIGN.md`。

## 5.1 主基底：Porcelain Court

`#F4F2EC`

不是纯白。

目的：

- 有建筑材料感；
- 让纯白内容层自然浮出；
- 降低传统 SaaS 的冷感；
- 更适合真实场馆摄影。

## 5.2 Primary：Table Teal

`#16464B`

用于：

- 订台确认；
- 课程预约；
- 约球加入；
- 支付继续；
- 签到；
- 选中时间 / 球台。

它来自球台的深色视觉记忆，但不是直接复制“乒乓球桌蓝”。

## 5.3 Kinetic Accent：Rally Vermilion

`#E24A36`

这是整个系统最重要的艺术性颜色。

它不负责普通 CTA，而负责：

- Live；
- 比分变化；
- Rating delta；
- 球轨短线；
- 赛事焦点；
- 极少量品牌识别。

普通页面面积 <= 3%。

## 5.4 Carbon Ink

`#101414`

用于：

- 标题；
- 强数据；
- membership pass；
- tournament deep surface。

## 5.5 为什么不用大面积红黑

红黑确实最容易让人联想到职业乒乓，但大面积红黑会很快进入：

- 电竞；
- 体育直播；
- 硬核男性化；
- 长期视觉疲劳。

Rally Atelier 使用**红色作为“发生变化”的颜色**，而不是背景色。

---

# 6. 排版系统

## 6.1 核心目标

页面不是靠大标题堆高级感，而是通过：

- 稳定网格；
- 数字对齐；
- 清晰留白；
- 少字号层级；
- 强弱合理的字重。

## 6.2 字体

跨平台设计参考：

`Inter Variable + PingFang SC + HarmonyOS Sans SC`

实际原生端：

- iOS：SF Pro / PingFang；
- HarmonyOS：HarmonyOS Sans；
- Android：系统 / Inter-like；
- Web：Inter + CJK fallback。

## 6.3 数字是核心品牌元素

乒乓球产品的信息里，数字异常重要：

- 19:30；
- 90 min；
- 6号台；
- #2 候补；
- 11:8；
- 1468 Rating；
- 3.5h 剩余。

所有关键数字启用 tabular numerals。

## 6.4 移动端层级

| Role | Size | 用途 |
|---|---:|---|
| Display | 40 | 极少数赛事/里程碑 |
| Page | 30 | 页面标题 |
| Section | 22 | 一级模块 |
| Card | 18 | 球台/课程/教练 |
| Title | 16 | 列表 |
| Body | 15–17 | 主要文本 |
| Meta | 12–13 | 次要状态 |
| Score | 44 | 比分 |

一屏明显字号最多 3 个。

---

# 7. 布局系统：Table-Line Grid

## 7.1 设计来源

乒乓球台提供了一个天然的高质量网格隐喻：

- 清晰外框；
- 中线；
- 网线；
- 左右空间；
- 对称但具有方向性。

我们不直接画球台，而是吸收它的**结构秩序**。

## 7.2 Mobile Grid

- 390px 基准；
- 20px screen margin；
- 4px micro grid；
- 8 / 12 / 16 内部节奏；
- 28 / 40 section；
- 44px minimum target；
- 48–50px primary CTA。

## 7.3 单台聚焦原则

每屏一个视觉核心。

### 首页

下一次预约。

### 订台

当前时段。

### 球台地图

当前选择台。

### 候补

当前排位。

### 比赛

下一场或当前比分。

### 会员

当前最重要权益。

这个原则直接解决复杂功能清单带来的“什么都重要”的问题。

---

# 8. 空间层次：Arena Depth

高级感的空间层次不靠很多阴影。

## Layer 0 — Club Space

暖灰白基底，稳定不动。

## Layer 1 — Play Surface

内容本体：列表、时间、球台、课程。

主要通过：

- 色差；
- 边线；
- 留白；
- 结构关系。

## Layer 2 — Control Rail

- 顶部 material bar；
- 日期轨；
- 筛选；
- floating tab bar。

使用少量半透明材料。

## Layer 3 — Commitment Sheet

- 确认订台；
- 取消；
- 加入候补；
- 分账；
- 添加器材；
- 报名确认。

背景轻微退后：

- scale 0.992–0.985；
- y +2–4px；
- scrim 46%；
- 原对象保持可辨识。

## Layer 4 — Critical

只用于：

- 支付异常；
- 不可逆退款；
- 身份验证；
- 重大业务冲突。

## Ambient Trajectory

球轨永远不是永久装饰层。

它只在：

- 页面转场；
- 成功确认；
- 赛事；
- Rating 变化；

短暂出现。

---

# 9. App 信息架构

底部导航：

# **首页 / 订台 / 训练 / 约球 / 我的**

## 9.1 首页

回答：

> 我现在最值得做什么？

## 9.2 订台

回答：

> 什么时候、哪张台可以打？

## 9.3 训练

回答：

> 我怎么进步？

包含：

- 课程；
- 私教；
- 陪练；
- 教练；
- 成长。

## 9.4 约球

回答：

> 我可以和谁打？

## 9.5 我的

回答：

> 我的承诺、权益和身份是什么？

赛事是阶段性行为，不应该永久占据一个 Tab；在赛事期可通过 Home live module 加强曝光。

---

# 10. 首页 / Today + Play

## 10.1 首屏目标

3 秒回答：

- 今天有预约吗？
- 多久后开始？
- 哪里还有台？
- 我下一步干什么？

## 10.2 结构

### A. Identity

`晚上好，沈言`  
`静安旗舰馆⌄`

右侧仅保留通知。

### B. One Big Thing

如果已有预约：

**19:30**  
`A06 · 90 min`  
`距开始 42 分钟`

状态：`已预约`

主动作随着时间动态改变：

- >60min：查看详情；
- 30–60min：路线；
- 签到窗：签到；
- 使用中：延时；
- 完成后：再订一次 / 记录比分。

### C. Three Quick Actions

最多三个：

- 订台；
- 约教练；
- 约球。

不是九宫格。

### D. Live Availability

例：

`今晚 20:00 后 · A区 4台可订`

用短时间轨 + 台数，而不是复杂地图。

### E. Training recommendation

仅 1–3 个高相关项目。

### F. Rating / membership pulse

仅一个最相关状态：

`TTR 1468 · +18`  
或  
`非高峰免费时长 · 剩余3.5h`

不要同时展示所有资产。

---

# 11. 订台：最核心的 App 任务

## 11.1 用户心理模型

顺序应该是：

> **什么时候 → 打多久 → 哪张台 → 和谁 → 多少钱 → 确认**

不是：

> 先展示全部 12 张球台，再让用户自己找空闲。

## 11.2 第一步：时间

### 日期

7 日横轨。

### 时间

分段：

- 上午；
- 下午；
- 晚间。

时段 chip：

`18:30`  
`19:00`  
`19:30 · 仅2台`

峰谷价格不用全屏颜色标记。

## 11.3 智能分配优先

默认按钮：

`智能分配最佳球台`

副动作：

`自己选台`

这是 Choice Architecture 的关键：

大部分用户并不需要认识每张台，减少无意义选择。

## 11.4 手动选台

地图展示：

- A区；
- B区私享；
- 发球机区；
- 接待；
- 入口。

球台状态：

- 可订；
- 已选择；
- 刚被锁；
- 已订；
- 使用中；
- 维护。

不能只用颜色。

## 11.5 选台微动效：Table Focus

选中 A06：

1. node 1.02 scale；
2. y -1–2px；
3. 内部白色中线变亮；
4. 周围球台降低 8–12% 对比度；
5. light haptic；
6. 160–200ms 完成。

不会弹跳。

---

# 12. 订台确认 Bottom Sheet

这是系统最重要的商业界面之一。

## 内容必须一屏可知

### 时间

`今天 · 19:30–21:00`

### 地点

`静安旗舰馆 · A06`

### 时长

`90 分钟`

### 会员权益

`旗舰会员 · 非高峰免费`

或：

`会员折后 ¥72`

### 参与者

`我 + 2 位球友`

### 器材

`球拍×1 / 发球机×0`

### 取消

`18:30 前免费取消；之后扣 ¥18 / 小时`

### CTA

`确认订台`

或：

`支付 ¥72 并确认`

不要用“查看规则”隐藏关键后果。

---

# 13. 订台成功

成功不是一个 Toast。

稳定页面：

`已订台`

`A06`  
`19:30–21:00`

接着展示：

- 签到方式；
- 导航；
- 邀请球友；
- 加入日历。

## Signature：Booking Seal

一个 6–8px Ball White 点：

- 沿 36–52px Rally Vermilion 短线移动一次；
- 260–340ms；
- 收束到确认状态；
- medium haptic。

没有 confetti。

---

# 14. 训练首页

训练不是课程商城。

## 结构

### 当前训练

若有预约，优先展示下一课。

### 三个 segment

- 课程；
- 私教 / 陪练；
- 教练。

### 推荐

根据：

- 当前等级；
- 已上课程；
- 常打时间；
- 教练关系。

短解释：

`适合你当前的发接发阶段`

而不是：

`猜你喜欢`

---

# 15. 课程列表

## Schedule Mode

以信息为主，不使用大图卡。

一行结构：

左：

`19:30`  
`75min`

中：

`进阶弧圈与衔接`  
`林骁 · A区`

右：

`剩1位`

或：

`候补2`

状态：

`可用进阶小班卡`

无需进入详情即可判断能不能报。

---

# 16. 课程详情

## Hero 不应该像瑜伽 App

摄影：

- 低机位；
- 真实拉球；
- 边线 / 网线；
- 动作过程；
- 控制光；
- 球体可有轻微运动模糊。

## 信息优先级

1. 课程名；
2. 等级；
3. 训练目标；
4. 教练；
5. 时间；
6. 余位；
7. 使用卡项；
8. 取消规则；
9. 详情。

CTA sticky：

`预约 · 消耗1次`

满员：

`加入候补 · 当前2人`

---

# 17. 候补

候补容易产生焦虑，设计目标不是强化“抢”，而是增加确定性。

## 主数字

`#2`

`当前排在第 2 位`

## 状态解释

`开课前 2 小时内有名额释放时，将给你 10 分钟确认。`

## Waitlist Roll

#3 → #2：

- 旧数向上 8px；
- 新数从下方进入；
- 160–200ms；
- 卡片本身不移动；
- 不闪红。

---

# 18. 教练 / 陪练

## 列表不是“明星海报”

卡片显示：

`林骁`  
`横板两面弧圈 · 成人进阶 · 赛事陪练`  
`最近可约：今晚 21:00`

## 教练详情

### 上半层

自然环境肖像。

### 中层

- 技术特点；
- 适合水平；
- 服务类型；
- 经过验证的资质。

### 下层

可约时间。

CTA：

`查看可约时间`

---

# 19. 私教 / 陪练时间

这是一个资源合并结果，不是简单教练日历。

后台已经计算：

- 教练 availability；
- 已有训练；
- 团课；
- 请假；
- 球台；
- 缓冲时间。

会员只看真正可订时段。

默认：

`最快可约`

专家用户可换日期/时段。

---

# 20. 约球 / Open Match

这是乒乓系统最重要的差异化体验之一。

## 20.1 不是社交动态

页面核心不是 feed，而是：

> **今晚谁和我水平接近、时间匹配，而且真的能打一场。**

## 20.2 推荐卡

`今晚 21:00 · 静安旗舰馆`

`友谊局`

`TTR 1400–1550`

头像 3 个 + `还差1人`

`约 ¥24/人`

推荐理由：

- 水平接近；
- 同馆常打；
- 时间匹配。

## 20.3 私人信息

加入确认前：

不显示手机号码。

可显示：

- 昵称；
- 水平；
- 履约率；
- 常打馆；
- 比赛意图。

---

# 21. 水平 / Rating

## 核心原则

不要创造“AI 精准测评”幻觉。

### 显示

`TTR 1468`

`本月 +36`

`最近正式对局 6 场 · 4胜2负`

### Rating Arc

比赛确认后：

- 旧值静止；
- 新值数字短 roll；
- 外部弧线 280–360ms 推进；
- `+18` 使用 Rally Vermilion；
- 最后完全静止。

---

# 22. 赛事中心

赛事可提高视觉张力。

## 允许的变化

- Carbon 大面积；
- Rally Vermilion 稍增；
- 运动摄影更强；
- 数字更大；
- bracket 线更明显。

但不能成为一个新设计系统。

## 赛事主页面

优先：

- 我的报名；
- 下一场；
- 报名截止。

而不是把整个签表扔在首屏。

## 下一场

`20:10`  
`vs. 顾澈 · TTR 1492`  
`A03`

CTA：

`赛前签到`

---

# 23. 比分

比分是最强数字场景。

## Score Tile

Carbon Ink 背景。

44px tabular numeral。

## Score Flip

每分：

- 140–180ms；
- 纵向替换；
- 0–1px overshoot；
- 得分方底部 Rally line 亮 160ms；
- 无爆炸、无粒子。

高频比分记录不应产生视觉疲劳。

---

# 24. 到馆签到

用户可能：

- 正在走路；
- 手拿球拍包；
- 光线复杂；
- 临近开台。

因此签到界面只保留：

1. 当前预约；
2. 大型 QR/扫码框；
3. fallback。

## 成功

`已签到 · 19:18`  
`A06 · 前方右侧`

## Check-in Line

扫描时：

- 一次扫描线；
- 成功后四角收束；
- 转成 A06 状态块；
- 240–320ms。

失败必须说明：

- 太早；
- 太晚；
- 预约不存在；
- 欠费；
- 台被调整。

---

# 25. 会员 / Wallet

会员权益是“可进入俱乐部的能力”，不是信用卡。

## 主 Pass

Carbon：

`ARC FLAGSHIP`

`非高峰免费 8h/月`

`剩余 3.5h`

`订台提前 21 天`

小 Rally 标记可用。

不使用：

- 金属金；
- 仿信用卡；
- 黑金 VIP；
- 3D 光泽。

## 次级资产

- 训练课包；
- 私教；
- 储值；
- 优惠券。

按即将到期 / 使用频率排序，而不是按产品类型硬排序。

---

# 26. 我的 / Me

结构：

## Identity

头像、昵称、Rating、主会员。

## Commitments

- 我的预约；
- 候补；
- 赛事。

## Assets

- 会员；
- 课包；
- 订单。

## History

- 打球；
- 训练；
- 比赛。

## Service

客服、门店、设置。

禁止所有入口同权重的 4×3 宫格。

---

# 27. 状态页

## 27.1 Empty

错误：

`暂无数据`

正确：

`今晚 19:00–21:00 已订满`  
`21:30 后有 4 张台，或加入候补`

## 27.2 Table Taken

`这张台刚刚被预订`

动作：

`智能选择其他球台`

并保留日期、时间、时长、参与者。

## 27.3 Membership Ineligible

`你的训练课包不能用于球台预订`

动作：

- 使用会员时长；
- 单次支付；
- 查看适用权益。

## 27.4 Payment Failure

必须说明：

- 是否扣款；
- 球台是否还在 Hold；
- Hold 剩余多久；
- 是否能重试。

---

# 28. Bottom Sheet 系统

Bottom Sheet 用于“仍在原任务中”的决策。

适用：

- 订台确认；
- 取消；
- 时长；
- 分账；
- 器材；
- 候补 Offer；
- 筛选；
- 退款影响。

不适用：

- 长表单；
- 赛事完整规则；
- 教练完整资料；
- 订单完整历史。

---

# 29. Motion System：Quiet Rally Physics

## 29.1 两档体系

### Standard Motion

用于：

- Tab；
- filter；
- chip；
- 普通 list；
- 高频按钮。

特点：

短、准、低 overshoot。

### Expressive Spatial Motion

用于：

- 卡片→详情；
- 选台；
- 订台成功；
- 签到；
- Rating；
- 赛事。

## 29.2 时间

| 类型 | 时长 |
|---|---:|
| Press | 80–120ms |
| Chip/slot | 140–190ms |
| Number update | 150–220ms |
| List state | 180–240ms |
| Filter/local sheet | 240–300ms |
| Commitment sheet | 280–360ms |
| Shared element | 320–420ms |

## 29.3 Curve

Quick:

`cubic-bezier(0.2, 0, 0, 1)`

Enter:

`cubic-bezier(0.16, 1, 0.3, 1)`

Exit:

`cubic-bezier(0.4, 0, 1, 1)`

Spatial：

系统 native spring，低 overshoot。

---

# 30. 细节微动效库

## 30.1 Serve Dot

主动作被按下：

- 6px 小球点轻压缩；
- 沿动作方向移动 <=16px；
- 转化为 loading / success 标识。

不要每个按钮都使用。

## 30.2 Slot Sweep

时间 chip 选中：

- 从中心向两侧填充；
- 150–180ms；
- 类似中线展开。

## 30.3 Table Focus

选台微抬升 + 中线亮起。

## 30.4 Booking Seal

成功短球轨。

## 30.5 Waitlist Roll

候补数滚动。

## 30.6 Check-in Line

扫描线 → 收束为球台状态。

## 30.7 Score Flip

比分数字短替换。

## 30.8 Rating Arc

Rating 弧线增长。

## 30.9 Live Dot

“LIVE”小点只做一次 600ms fade-in，不无限 pulse。

## 30.10 Table State Crossfade

实时台况：

`可用 → Held → 已订`

使用 180–240ms tone/label crossfade，不改变卡片位置，避免地图跳动。

---

# 31. Haptics

## Light

- slot；
- table；
- filter；
- score increment。

## Medium

- booking confirmed；
- check-in；
- join match confirmed；
- tournament registered。

## Warning

- payment fail；
- destructive consequence；
- booking conflict。

滚动和普通 Tab 不震动。

---

# 32. 用户心理学设计

## 32.1 Recognition over Recall

不要让用户记住：

- 哪张卡能用；
- 是否高峰；
- 取消截止；
- 有没有器材；
- 会员折扣。

全部在确认层展示。

## 32.2 Progressive Disclosure

第一层：

`可订`

第二层：

`会员免费 / ¥48`

第三层：

完整会员和价格规则。

## 32.3 Choice Overload

普通订台：

先提供“智能分配最佳台”。

只有主动点“自己选台”才打开地图。

## 32.4 Fitts's Law

订台、加入、签到、确认等主动作位于下方 thumb zone。

## 32.5 Agency

- 取消入口可见；
- 改期可用时优先提供；
- 高风险后果提前明确；
- 自动补位规则提前说清；
- 可恢复操作支持 undo / return。

## 32.6 Scarcity

只说事实：

`仅剩2台`

不说：

`火爆抢订！仅剩最后机会！`

## 32.7 Social Trust

约球优先显示：

- 水平；
- 友谊/计分；
- 履约；
- 共同球馆；
- 价格。

不是先展示点赞、关注、动态。

## 32.8 Peak-End

最值得做好的四个结束时刻：

1. 订台完成；
2. 候补转正；
3. 到馆签到；
4. 赛事 / Rating 更新。

---

# 33. 摄影艺术指导

## 33.1 核心风格

**Controlled Kinetic Photography**

### 光线

- 单方向控制光；
- 深背景但不是黑洞；
- 球台面、网、球拍边缘有清楚轮廓；
- 人体不需要完全照亮。

### 动作

拍击球过程中间态：

- 引拍；
- 重心交换；
- 球即将过网；
- 步法切换。

不要拍：

- 对镜头举拍摆 pose；
- 双手抱胸教练证件照；
- 过度笑脸团建图。

### 负空间

30–45% 可放置标题或 UI overlay 的负空间。

## 33.2 四类图库

1. Match / 对打
2. Training / 训练
3. Club Architecture / 球馆空间
4. Detail / 球台、网、胶皮、球、发球机

## 33.3 色彩

图片自身不要过度红黑。

建议：

- 中性场馆；
- 青绿球台；
- 黑/白衣着；
- 红色局部点缀。

让 UI 的 Rally Vermilion 与摄影形成统一。

---

# 34. 图标系统

## 34.1 原则

乒乓球特色不等于每个 icon 都是球拍。

基础图标仍使用通用语义：

- calendar；
- location；
- person；
- wallet；
- filter；
- notification。

领域 icon 仅用于：

- table；
- robot；
- paddle rental；
- tournament；
- rating。

## 34.2 视觉

- 1.75–2px stroke；
- 圆端；
- 24px frame；
- 20px optical；
- 线性为主。

---

# 35. 数据可视化

消费者端数据不是 BI。

## Rating

大数 + delta + recent matches。

## 训练

到店 / 课程次数使用 small sparkline。

## 会员

时长/次数使用进度条或简单环。

## 管理端

最重要的是：

- 球台利用率 heatmap；
- 时段供需；
- 课程候补压力；
- 会员续费；
- 教练利用率；
- 支付失败；
- 赛事参与。

避免 donut wall。

---

# 36. 多租户白标

用户截图明确要求小程序装修 / 软件换肤，因此必须产品化，而不是无限开放颜色。

## 租户可配置

- Logo；
- Primary hue；
- 摄影；
- 首页模块顺序；
- 底部入口开关；
- App icon；
- 门店 Hero。

## 系统强制

- error / warning / success；
- 文本颜色；
- spacing；
- typography scale；
- table state；
- motion；
- accessibility；
- destructive action。

## 自动生成

输入租户主色后：

- active；
- soft；
- on-primary；
- dark variant。

并进行对比度检查。

---

# 37. 员工端

员工端视觉继承 Rally Atelier，但 Density = 7。

首页：

- 当前课程；
- 当前球台；
- 待签到；
- 待处理候补；
- 维护异常；
- 会员任务。

员工端不需要 lifestyle hero。

## 球台板

实时状态必须稳定位置：

A01 A02 A03 …

状态只变化 tone/label，不让卡片重新排序。

这符合现场快速扫描。

---

# 38. 管理后台

管理端是**Precision Cockpit**。

## 38.1 圆角

8–12px。

## 38.2 图片

几乎不用。

## 38.3 主体

- 时间轴；
- 表格；
- heatmap；
- queue；
- exception；
- saved views。

## 38.4 首页

顺序：

1. Needs Attention；
2. 现金/球台利用率/课程利用率/活跃会员；
3. 时段热力；
4. 会员风险；
5. 门店对比。

不是 12 个 KPI 卡。

---

# 39. Accessibility

## Contrast

正文 >= WCAG AA。

## 状态

球台可用性、比分、错误不得只靠颜色。

## Dynamic Type

至少支持 130–150%。

## Reduce Motion

开启时：

- shared element → crossfade；
- scale depth → 删除；
- trajectory → 删除；
- score roll → fade；
- rating arc → 直接显示最终值；
- blur transition → 删除。

---

# 40. 性能就是高级感

## 目标

- 高频操作 feedback <100ms；
- 动效稳定 60fps；
- 不为玻璃效果创建多层实时 blur；
- 表格/球台实时刷新不导致 layout shift；
- 图片渐进加载；
- 骨架与真实布局同构。

真实球台状态变化要保持位置稳定。

---

# 41. 高保真页面首批优先级

如果接下来生成高保真图，建议先生成：

1. 首页
2. 日期/时段
3. 球台地图
4. 订台确认
5. 订台成功
6. 训练课程列表
7. 课程详情
8. 教练详情
9. 约球首页
10. 会员中心
11. 到馆签到
12. 赛事下一场
13. 候补状态
14. 状态页
15. Bottom Sheet / 组件页

第一轮不要先生成启动页；启动页无法验证产品系统真正的视觉质量。

---

# 42. 页面验收标准

## 首页

- 3 秒内知道下一步；
- <=3 个 quick actions；
- 无大 Banner 抢焦点。

## 订台

- <=10 秒找到一个可订时间；
- 默认推荐减少选择；
- 价格与政策在确认前可见。

## 球台地图

- 用户立即能分辨可用/不可用；
- 选中状态不只靠颜色；
- 空间锚点存在。

## 约球

- 一眼看懂水平/时间/人数/费用；
- 私人联系方式未被过早暴露。

## 签到

- <=2 个动作；
- success 稳定显示台号。

## 管理后台

- 首屏是异常和决策；
- 不是装饰数据大屏。

---

# 43. 设计评分

## Visual / 40

- Simplicity 10
- Diversity 7
- Color 7
- Craftsmanship 16

## Interaction / 35

- task efficiency 8
- state feedback 7
- recovery 6
- cognitive load 5
- rule transparency 5
- social trust 4

## Business Closure / 15

- booking
- waitlist
- payment
- check-in
- consumption
- match/tournament

## Accessibility & Performance / 10

目标：

**>=92 / 100**

Craftsmanship 最低：

**14 / 16**

---

# 44. Google Stitch 使用方式

目录：

```text
.stitch/
  DESIGN.md
  SITE.md
  next-prompt.md
```

其中：

- `DESIGN.md`：视觉系统；
- `SITE.md`：页面、状态、路线、路线图；
- `next-prompt.md`：一次只生成一组相关页面。

Google 的 Stitch Loop 建议保持 DESIGN 与 SITE 作为持久上下文，而不是每轮重新描述风格。

---

# 45. Stitch 首轮视觉校准 Prompt

```text
Design a production-quality mobile member app for a premium table-tennis club.

Strictly follow .stitch/DESIGN.md: Rally Atelier / 回合艺境.

Generate these 4 screens as one coherent visual calibration family:
1. Home / 首页
2. Table booking — date & time
3. Table map selection
4. Booking confirmation bottom sheet

Brand dataset:
ARC TT CLUB / 弧线乒乓
Current club: 静安旗舰馆
Member: 沈言
Rating: TTR 1468
Membership: 旗舰会员
Next reservation: 19:30, A06, 90 min

Core design intent:
- One-Table Rule: one focal object per screen
- Porcelain Court warm canvas
- Table Teal as primary action
- Rally Vermilion as kinetic accent only
- Carbon Ink typography
- exact tabular time and pricing
- spatial depth through tonal layers and material controls, not heavy shadows
- table-tennis identity through geometry, table availability, rating and motion, not paddle clip-art

Interaction:
- time-slot selection uses Slot Sweep
- table selection uses Table Focus
- booking confirmation uses a commitment sheet
- booking success would use Booking Seal

Avoid:
- Pilates/yoga visual language
- esports neon red/black
- giant feature grids
- excessive cards
- black-gold VIP style
- hidden cancellation/price rules
```

---

# 46. Stitch 订台 Prompt

```text
Create a high-fidelity Table Booking screen for the Rally Atelier table-tennis app.

Primary task: reserve a table with the fewest decisions possible.

Hierarchy:
1. Current club
2. 7-day date rail
3. morning / afternoon / evening time sections
4. time slots with factual availability
5. selected duration
6. primary action: 智能分配最佳球台
7. secondary action: 自己选台

Examples:
18:30 — 可订
19:00 — 仅剩2台
19:30 — 高峰 ¥48/h
21:00 — 会员非高峰免费

Do not show all tables before a time is selected.
Use tabular numerals.
Use Table Teal for selected/primary action.
Rally Vermilion should be almost absent on this utility screen.
```

---

# 47. Stitch 球台地图 Prompt

```text
Create a high-fidelity table map selection screen for ARC TT CLUB.

Zones:
A区 — 标准比赛台 01–08
B区 — 私享台 09–10
C区 — 发球机台 11–12

Current selected time: 19:30–21:00.
Available: A03, A06, B09.
Held by someone else: A05.
Maintenance: C11.
Booked/in use: remaining tables.

Show spatial anchors: reception, entrance, private zone.
Selected table A06 should use Table Focus micro-interaction intent: slight lift, brighter internal court line, one light haptic.
Status must use label/shape/tone, not color alone.
Keep a sticky summary + Continue button at bottom.
```

---

# 48. Stitch 约球 Prompt

```text
Create the Open Match / 约球 home screen.

Primary intent: help a player find a trustworthy game tonight.

Show recommended matches ordered by:
time fit → club → level compatibility → intent → reliability.

Example primary card:
今晚 21:00
静安旗舰馆
友谊局
TTR 1400–1550
3 players joined · 1 spot left
约 ¥24/人
Why recommended: 水平接近 · 同馆常打

Primary action: 加入
Secondary action: 发起约球

Do not design this as a social feed.
Do not show phone numbers.
Use avatars sparingly.
```

---

# 49. 研发映射

## HarmonyOS / ArkUI

建议：

- `animateTo` 用于短 state；
- `geometryTransition` 用于 card→detail；
- spring 用于 spatial motion；
- color/opacity 使用非 overshoot curve；
- 系统 vibration 用于 selection / success；
- Reduce Motion 读取系统辅助设置。

## iOS

- matchedGeometry / navigation transition；
- spring；
- material；
- Core Haptics / UIImpactFeedbackGenerator；
- Reduce Motion。

## Web / Mini Program

- transform + opacity 优先；
- View Transition API 可用时做 shared element；
- fallback 为 crossfade；
- 不用大面积实时 backdrop-filter；
- 球台实时状态更新避免 DOM reflow 排序。

---

# 50. 最终十条原则

1. **乒乓球的高级感来自精度与动势，不来自红黑电竞。**
2. **每屏只有一张“被照亮的球台”。**
3. **订台先选时间，再选台。**
4. **默认推荐，专家再手选。**
5. **价格、权益、取消规则在承诺前可见。**
6. **动效像回合：短、准、有来有回，不拖。**
7. **Rally Vermilion 是变化信号，不是满屏品牌色。**
8. **约球是信任匹配，不是社交 Feed。**
9. **消费者端像精品球馆，管理端像精密比赛控制台。**
10. **高级感的最高维度是 Craftsmanship：每个状态都像被认真设计过。**

---

# 51. 研究来源

### Google DESIGN.md / Stitch
- https://github.com/google-labs-code/design.md
- https://github.com/google-labs-code/design.md/blob/main/PHILOSOPHY.md
- https://github.com/google-labs-code/stitch-skills

### World Table Tennis
- https://www.worldtabletennis.com/aboutus
- https://www.worldtabletennis.com/teamarticle?article_no=team_partners
- https://www.worldtabletennis.com/description?artId=5841

### PingPod
- https://pingpod.com/
- https://pingpod.com/pricing/
- https://pingpod.com/membership/
- https://pingpod.com/classes/

### Playtomic
- https://playerhelp.playtomic.com/hc/en-gb/articles/19831881490449-How-to-make-a-reservation-in-Playtomic-app
- https://playerhelp.playtomic.com/hc/en-gb/articles/19831715222929-How-to-book-a-court-or-a-spot-in-a-match-in-your-favourite-Club
- https://playerhelp.playtomic.com/hc/en-gb/articles/19831958258193-Private-Bookings-vs-Open-Matches
- https://playerhelp.playtomic.com/hc/en-gb/articles/19832089052561-How-to-split-the-payment-of-a-reservation
- https://playerhelp.playtomic.com/hc/en-gb/articles/19831425477649-What-is-a-Club-Membership

### Apple HIG
- https://developer.apple.com/design/human-interface-guidelines/motion
- https://developer.apple.com/design/human-interface-guidelines/design-principles
- https://developer.apple.com/design/human-interface-guidelines/accessibility

### Material 3
- https://m3.material.io/
- https://developer.android.com/reference/kotlin/androidx/compose/material3/MotionScheme

### Visual aesthetics
- VisAWI / Moshagen & Thielsch research family: Simplicity, Diversity, Colorfulness, Craftsmanship.

---
# PART II — Google Stitch DESIGN.md
---
version: alpha
name: "Rally Atelier / 回合艺境"
description: "A premium table-tennis venue operating system. The member experience combines the single-table focus of a professional arena, the quiet precision of contemporary product design, and the kinetic rhythm of a rally. The admin experience inherits the same geometry and color discipline at a denser operational cadence."
colors:
  canvas: "#F4F2EC"
  canvas-cool: "#EEF1EF"
  surface: "#FBFAF7"
  surface-elevated: "#FFFFFF"
  surface-deep: "#E9EDEB"
  ink: "#101414"
  body: "#343C3A"
  muted: "#6B7471"
  muted-soft: "#969F9C"
  court: "#16464B"
  court-strong: "#10383C"
  court-soft: "#DCE9E7"
  rally: "#E24A36"
  rally-strong: "#C93A28"
  rally-soft: "#F7E1DB"
  ball: "#FEFEFA"
  line: "#D7DEDB"
  line-strong: "#BAC5C1"
  success: "#2E6D56"
  success-soft: "#DDECE5"
  warning: "#A4672D"
  warning-soft: "#F3E6D6"
  error: "#B0443C"
  error-soft: "#F4DEDC"
  info: "#476A7B"
  scrim: "rgba(8,14,14,0.46)"
  material: "rgba(255,255,255,0.84)"
  material-dark: "rgba(19,25,24,0.86)"
  dark-canvas: "#0C1110"
  dark-surface: "#141A18"
  dark-surface-elevated: "#1B2320"
  dark-ink: "#F6F5F0"
  dark-body: "#D4D9D6"
  dark-muted: "#98A29E"
  dark-line: "#2B3431"
typography:
  display-hero:
    fontFamily: "'Inter Variable','PingFang SC','HarmonyOS Sans SC',system-ui,sans-serif"
    fontSize: 40px
    fontWeight: 680
    lineHeight: 1.04
    letterSpacing: -1.2px
  page-title:
    fontFamily: "'Inter Variable','PingFang SC','HarmonyOS Sans SC',system-ui,sans-serif"
    fontSize: 30px
    fontWeight: 660
    lineHeight: 1.12
    letterSpacing: -0.7px
  section-title:
    fontFamily: "'Inter Variable','PingFang SC','HarmonyOS Sans SC',system-ui,sans-serif"
    fontSize: 22px
    fontWeight: 630
    lineHeight: 1.22
    letterSpacing: -0.35px
  title-lg:
    fontFamily: "'Inter Variable','PingFang SC','HarmonyOS Sans SC',system-ui,sans-serif"
    fontSize: 18px
    fontWeight: 620
    lineHeight: 1.30
    letterSpacing: -0.18px
  title-md:
    fontFamily: "'Inter Variable','PingFang SC','HarmonyOS Sans SC',system-ui,sans-serif"
    fontSize: 16px
    fontWeight: 600
    lineHeight: 1.36
    letterSpacing: -0.08px
  body-lg:
    fontFamily: "'Inter Variable','PingFang SC','HarmonyOS Sans SC',system-ui,sans-serif"
    fontSize: 17px
    fontWeight: 430
    lineHeight: 1.55
    letterSpacing: 0px
  body-md:
    fontFamily: "'Inter Variable','PingFang SC','HarmonyOS Sans SC',system-ui,sans-serif"
    fontSize: 15px
    fontWeight: 430
    lineHeight: 1.55
    letterSpacing: 0px
  body-sm:
    fontFamily: "'Inter Variable','PingFang SC','HarmonyOS Sans SC',system-ui,sans-serif"
    fontSize: 13px
    fontWeight: 440
    lineHeight: 1.48
    letterSpacing: 0px
  label:
    fontFamily: "'Inter Variable','PingFang SC','HarmonyOS Sans SC',system-ui,sans-serif"
    fontSize: 13px
    fontWeight: 610
    lineHeight: 1.35
    letterSpacing: 0.03px
  caption:
    fontFamily: "'Inter Variable','PingFang SC','HarmonyOS Sans SC',system-ui,sans-serif"
    fontSize: 12px
    fontWeight: 500
    lineHeight: 1.42
    letterSpacing: 0.06px
  metric-xl:
    fontFamily: "'Inter Variable','PingFang SC','HarmonyOS Sans SC',system-ui,sans-serif"
    fontSize: 40px
    fontWeight: 660
    lineHeight: 1.00
    letterSpacing: -1px
    fontFeature: "'tnum' 1, 'ss01' 1"
  score-xl:
    fontFamily: "'Inter Variable','PingFang SC','HarmonyOS Sans SC',system-ui,sans-serif"
    fontSize: 44px
    fontWeight: 700
    lineHeight: 0.96
    letterSpacing: -1.1px
    fontFeature: "'tnum' 1, 'ss01' 1"
  metric-md:
    fontFamily: "'Inter Variable','PingFang SC','HarmonyOS Sans SC',system-ui,sans-serif"
    fontSize: 24px
    fontWeight: 640
    lineHeight: 1.08
    letterSpacing: -0.4px
    fontFeature: "'tnum' 1, 'ss01' 1"
  button:
    fontFamily: "'Inter Variable','PingFang SC','HarmonyOS Sans SC',system-ui,sans-serif"
    fontSize: 15px
    fontWeight: 630
    lineHeight: 1.20
    letterSpacing: 0px
rounded:
  xs: 8px
  sm: 10px
  md: 14px
  lg: 20px
  xl: 26px
  xxl: 32px
  full: 9999px
spacing:
  xxs: 2px
  xs: 4px
  sm: 8px
  md: 12px
  base: 16px
  screen: 20px
  lg: 24px
  section: 28px
  xl: 32px
  xxl: 40px
  xxxl: 48px
  hero: 64px
components:
  button-primary:
    backgroundColor: "{colors.court}"
    textColor: "{colors.ball}"
    typography: "{typography.button}"
    rounded: "{rounded.full}"
    padding: 14px 22px
    height: 50px
  button-primary-pressed:
    backgroundColor: "{colors.court-strong}"
    textColor: "{colors.ball}"
    typography: "{typography.button}"
    rounded: "{rounded.full}"
    padding: 14px 22px
    height: 50px
  button-secondary:
    backgroundColor: "{colors.surface-elevated}"
    textColor: "{colors.ink}"
    typography: "{typography.button}"
    rounded: "{rounded.full}"
    padding: 13px 20px
    height: 48px
  button-danger:
    backgroundColor: "{colors.error-soft}"
    textColor: "{colors.error}"
    typography: "{typography.button}"
    rounded: "{rounded.full}"
    padding: 13px 20px
    height: 48px
  top-material-bar:
    backgroundColor: "{colors.material}"
    textColor: "{colors.ink}"
    typography: "{typography.title-md}"
    rounded: "{rounded.xs}"
    padding: 8px 20px
    height: 56px
  floating-tabbar:
    backgroundColor: "{colors.material}"
    textColor: "{colors.muted}"
    typography: "{typography.caption}"
    rounded: "{rounded.xl}"
    padding: 8px 10px
    height: 64px
  focus-card:
    backgroundColor: "{colors.surface-elevated}"
    textColor: "{colors.ink}"
    typography: "{typography.body-md}"
    rounded: "{rounded.xl}"
    padding: 22px
  table-availability-card:
    backgroundColor: "{colors.surface-elevated}"
    textColor: "{colors.ink}"
    typography: "{typography.body-md}"
    rounded: "{rounded.lg}"
    padding: 16px
  table-map-node:
    backgroundColor: "{colors.surface-deep}"
    textColor: "{colors.body}"
    typography: "{typography.caption}"
    rounded: "{rounded.sm}"
    padding: 8px
    width: 72px
    height: 42px
  table-map-node-selected:
    backgroundColor: "{colors.court}"
    textColor: "{colors.ball}"
    typography: "{typography.label}"
    rounded: "{rounded.sm}"
    padding: 8px
    width: 76px
    height: 44px
  time-slot-chip:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.body}"
    typography: "{typography.label}"
    rounded: "{rounded.full}"
    padding: 10px 14px
    height: 42px
  time-slot-chip-selected:
    backgroundColor: "{colors.court}"
    textColor: "{colors.ball}"
    typography: "{typography.label}"
    rounded: "{rounded.full}"
    padding: 10px 14px
    height: 42px
  filter-chip:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.body}"
    typography: "{typography.label}"
    rounded: "{rounded.full}"
    padding: 9px 14px
    height: 38px
  filter-chip-active:
    backgroundColor: "{colors.court-soft}"
    textColor: "{colors.court}"
    typography: "{typography.label}"
    rounded: "{rounded.full}"
    padding: 9px 14px
    height: 38px
  date-chip:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.body}"
    typography: "{typography.caption}"
    rounded: "{rounded.full}"
    padding: 9px 12px
    height: 48px
  date-chip-selected:
    backgroundColor: "{colors.ink}"
    textColor: "{colors.ball}"
    typography: "{typography.label}"
    rounded: "{rounded.full}"
    padding: 9px 12px
    height: 48px
  booking-summary:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.ink}"
    typography: "{typography.body-md}"
    rounded: "{rounded.lg}"
    padding: 18px
  booking-sheet:
    backgroundColor: "{colors.surface-elevated}"
    textColor: "{colors.ink}"
    typography: "{typography.body-md}"
    rounded: "{rounded.xl}"
    padding: 24px
  status-pill:
    backgroundColor: "{colors.court-soft}"
    textColor: "{colors.court}"
    typography: "{typography.caption}"
    rounded: "{rounded.full}"
    padding: 6px 10px
    height: 28px
  live-pill:
    backgroundColor: "{colors.rally-soft}"
    textColor: "{colors.rally-strong}"
    typography: "{typography.caption}"
    rounded: "{rounded.full}"
    padding: 6px 10px
    height: 28px
  training-card:
    backgroundColor: "{colors.surface-elevated}"
    textColor: "{colors.ink}"
    typography: "{typography.body-md}"
    rounded: "{rounded.lg}"
    padding: 16px
  coach-card:
    backgroundColor: "{colors.surface-elevated}"
    textColor: "{colors.ink}"
    typography: "{typography.body-md}"
    rounded: "{rounded.lg}"
    padding: 16px
  match-card:
    backgroundColor: "{colors.surface-elevated}"
    textColor: "{colors.ink}"
    typography: "{typography.body-md}"
    rounded: "{rounded.lg}"
    padding: 18px
  tournament-card:
    backgroundColor: "{colors.ink}"
    textColor: "{colors.ball}"
    typography: "{typography.body-md}"
    rounded: "{rounded.xl}"
    padding: 20px
  membership-pass:
    backgroundColor: "{colors.ink}"
    textColor: "{colors.ball}"
    typography: "{typography.body-md}"
    rounded: "{rounded.xl}"
    padding: 22px
  rating-badge:
    backgroundColor: "{colors.rally-soft}"
    textColor: "{colors.rally-strong}"
    typography: "{typography.label}"
    rounded: "{rounded.full}"
    padding: 7px 11px
    height: 30px
  score-tile:
    backgroundColor: "{colors.ink}"
    textColor: "{colors.ball}"
    typography: "{typography.score-xl}"
    rounded: "{rounded.md}"
    padding: 12px
    width: 72px
    height: 72px
  checkin-card:
    backgroundColor: "{colors.surface-elevated}"
    textColor: "{colors.ink}"
    typography: "{typography.body-md}"
    rounded: "{rounded.xl}"
    padding: 22px
  search-field:
    backgroundColor: "{colors.surface-elevated}"
    textColor: "{colors.ink}"
    typography: "{typography.body-md}"
    rounded: "{rounded.full}"
    padding: 12px 16px
    height: 46px
  text-input:
    backgroundColor: "{colors.surface-elevated}"
    textColor: "{colors.ink}"
    typography: "{typography.body-md}"
    rounded: "{rounded.md}"
    padding: 14px 16px
    height: 54px
  list-row:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.ink}"
    typography: "{typography.body-md}"
    rounded: "{rounded.sm}"
    padding: 14px 0px
    height: 58px
  metric-card:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.ink}"
    typography: "{typography.metric-md}"
    rounded: "{rounded.md}"
    padding: 16px
  alert-card:
    backgroundColor: "{colors.warning-soft}"
    textColor: "{colors.warning}"
    typography: "{typography.body-sm}"
    rounded: "{rounded.md}"
    padding: 14px
  error-card:
    backgroundColor: "{colors.error-soft}"
    textColor: "{colors.error}"
    typography: "{typography.body-sm}"
    rounded: "{rounded.md}"
    padding: 14px
  toast:
    backgroundColor: "{colors.ink}"
    textColor: "{colors.ball}"
    typography: "{typography.body-sm}"
    rounded: "{rounded.full}"
    padding: 10px 16px
    height: 40px
  skeleton:
    backgroundColor: "{colors.surface-deep}"
    textColor: "{colors.muted-soft}"
    rounded: "{rounded.md}"
    padding: 8px
    height: 16px
---

## Overview

**Rally Atelier / 回合艺境** is designed for a table-tennis venue system whose real product surface is much broader than “book a class.” It must handle table reservation, time-slot inventory, training classes, private coaching and sparring, waitlists, membership entitlements, check-in, consumptions, player matching, rating, equipment, tournaments, payments and refunds, while still feeling like a premium sports club rather than an ERP wrapped in a mobile shell.

The visual reference is **a single competition table under controlled arena light, inside a contemporary sports club designed by an architecture studio**. World Table Tennis has made the one-table, lights-down “Infinity Arena” a recognizable presentation device; this system borrows the **focus logic**, not the event spectacle. One important object is lit. Everything else recedes. The app should feel expensive because its attention is disciplined.

Three table-tennis-specific ideas shape the interface:

1. **Precision geometry** — the table rectangle, center line, net line and timed court grid become a subtle compositional grammar. Alignment should feel exact and physical.
2. **Spin trajectory** — movement appears as short arcs, directional traces and state continuity. It is never a decorative wave pasted across every page.
3. **Rally rhythm** — frequent interactions are fast and repeatable; high-value moments such as booking, check-in and match confirmation are slightly more expressive.

The member side is **athletic editorial**: calm surfaces, precise typography, real club photography, small areas of kinetic color, strong temporal hierarchy. The employee and admin side is **precision cockpit**: the same colors and geometry at higher density, shorter motion durations, stronger tabular alignment and fewer image surfaces.

### Experience dials

- Creativity: **7/10** — distinctive enough to be ownable, never artsy for its own sake.
- Density: **5/10 member / 8/10 admin** — comfortable member screens, compact operational screens.
- Variance: **5/10** — one stable structural system with controlled asymmetry in hero and editorial areas.
- Motion intent: **7/10 hero moments / 4/10 recurring controls** — premium choreography only when it improves continuity or feedback.
- Contrast: **7/10** — sharp ink, restrained palette, no low-contrast “luxury gray text.”

The system must communicate five user truths instantly:

- **When can I play?**
- **Which table / coach / class is actually available?**
- **What will this cost or consume?**
- **What happens if I cancel or do not show?**
- **What is my next action?**

Every screen is built around the hierarchy **Orientation → Focus → Action → Context → Explore**.

## Colors

The palette is a **Porcelain Court** system: warm mineral neutrals for quiet premium space, deep table teal for trust and decisive interaction, carbon ink for structure, and a small amount of vermilion for the speed and tension unique to table tennis.

### Foundation

- **Porcelain Court** `{colors.canvas}` is the main member background. It is deliberately warmer than pure white so the product feels architectural and tactile rather than clinical.
- **Cool Court Fog** `{colors.canvas-cool}` is allowed in data-heavy or utility zones where a cooler register improves separation.
- **Gallery Surface** `{colors.surface}` and `{colors.surface-elevated}` carry information without creating a “card wall.” Use them only when a real grouping or elevation relationship exists.
- **Carbon Ink** `{colors.ink}` is the main structural text and deep surface color. It replaces both pure black and fashionable low-contrast gray.

### Brand and interaction

- **Table Teal** `{colors.court}` is the primary interactive color: confirm table, confirm training, check in, join a match, continue payment. It is stable, professional and recognizably tied to the physical table without imitating a specific table manufacturer.
- **Court Soft** `{colors.court-soft}` is the selected/filter/available-state tint.
- **Rally Vermilion** `{colors.rally}` is the kinetic accent. It represents live play, ball trajectory, score emphasis, tournament energy and rare identity moments. It is **not** the generic CTA color and should usually occupy less than 3% of a member screen.
- **Ball White** `{colors.ball}` is used inside deep surfaces and tiny trajectory motifs. It should read as a clean point of light, not as a literal ping-pong-ball illustration everywhere.

### Semantic colors

Success, warning, error and information colors are functional only. Never use error red as a brand substitute. `Rally Vermilion` and `Error` are visually related but semantically distinct through tone, container treatment and iconography.

### Area discipline

A typical member page should visually approximate:

- 55–68% canvas / open space
- 20–30% neutral content surfaces
- 8–12% ink and deep content
- 2–5% Table Teal
- 0.5–3% Rally Vermilion
- <1% additional semantic color

### Dark mode

Dark mode is **Night Rally**, not neon esports.

- Use `{colors.dark-canvas}` as a matte room around lit content surfaces.
- Use `{colors.dark-surface}` and `{colors.dark-surface-elevated}` for table and schedule layers.
- Preserve Table Teal as the main interaction hue with adjusted luminance as needed for contrast.
- Rally Vermilion becomes a crisp live accent, not a glow.
- Do not add RGB gradients, luminous borders, cyberpunk grids or chromatic shadows.

## Typography

Typography is **sports precision without sports aggression**. It should feel closer to a timing instrument, contemporary architecture signage and premium hardware UI than to a gym poster.

### Family

Use `Inter Variable` with `PingFang SC` / `HarmonyOS Sans SC` as the cross-platform design reference. Native implementations should prefer the platform system family when that improves rendering fidelity.

### Hierarchy

- `{typography.display-hero}` is reserved for a rare home focus, tournament identity, or rating milestone. One instance maximum per screen.
- `{typography.page-title}` is the standard mobile page title.
- `{typography.section-title}` creates editorial rhythm between tasks, not between every group of 2–3 rows.
- `{typography.metric-xl}` expresses remaining minutes, table count, ranking movement, utilization or membership balance.
- `{typography.score-xl}` is exclusive to match score and tournament match surfaces; it must not appear in booking or membership cards.

### Numeric behavior

Time, price, table number, score, queue position and rating all use tabular numerals. A row of time slots must never visually wobble because numerals have variable width.

### Weight discipline

Use 430 for body and 600–680 for emphasis. Avoid a five-weight hierarchy. Premium is created through spacing and contrast before heavier weight.

### Chinese typesetting

- Mobile body text: 15–17px.
- Secondary metadata: minimum 12–13px with adequate contrast.
- Do not create “premium” by reducing Chinese text to 10–11px gray captions.
- Time and table labels may use slightly tighter letter spacing; legal/cancellation text should not.

## Layout

The base system is called **Table-Line Grid**. It takes the physical logic of a table — strong rectangle, exact center, clear boundaries — and turns it into layout behavior without drawing a literal table around every element.

### Mobile grid

- Baseline design width: approximately 390px.
- Horizontal screen margin: `{spacing.screen}` = 20px.
- Micro grid: 4px.
- Common sibling gap: 8 / 12 / 16px.
- Section gap: 28 / 40px.
- Main content radius: 20–26px.
- Frequent controls: minimum 44px touch target.
- Primary commitment button: 48–50px high.

### The One-Table Rule

Borrowing the focus logic of a single-table arena, each member screen has **one visual table under the spotlight** — one object or decision that owns attention.

Examples:

- Home: next reservation or “Book a table now.”
- Table booking: chosen time block.
- Table map: selected table.
- Training detail: training session + eligibility.
- Waitlist: queue position.
- Check-in: current reservation / table.
- Match room: the opponent pair and start time.
- Tournament: next match.

Secondary recommendations, promotions and memberships must not compete with this focal object.

### Booking timeline layout

Table reservation should use a **date rail + time band + table layer**, not a dense month calendar.

1. Date rail shows 5–7 days.
2. Time bands show morning / afternoon / evening with actual available slots.
3. Once a slot is selected, either auto-assign the best table or reveal the table map.
4. Price, member benefit, duration and cancellation policy appear before commitment.

This matches the user’s mental model: **when → where → which table → how long → how much**.

### Home composition

Home is a **Today + Play** surface, not a grid of 12 feature icons.

Recommended order:

1. identity + current club
2. one focus card: next booking / available play window
3. three compact actions: 订台 / 约教练 / 约球
4. live table availability strip
5. training recommendation
6. rating / membership pulse
7. tournament or community content if relevant

### Information grouping

Do not use cards as universal separators. Use cards when there is one of three reasons:

- the item is actionable as one unit;
- the item floats above a lower layer;
- the item owns a distinct business state.

Otherwise use spacing, line alignment and common region.

### Admin adaptation

Admin is not a stretched mobile app.

- 1280–1600px primary canvas.
- Left navigation 220–248px.
- Dense schedule/calendar and table timeline surfaces may use the full viewport width.
- Rounded corners reduce to 8–12px.
- Photography nearly disappears.
- Tables, timelines, heatmaps, queues and exception lists replace consumer cards.
- Table Teal remains the primary action color; Rally Vermilion is reserved for live/critical sports emphasis, not administrative decoration.

## Elevation & Depth

Depth is **arena lighting translated into interface hierarchy**. The product should feel layered, but never like a pile of floating cards.

### Layer 0 — Club space

The page canvas `{colors.canvas}` is the room. It remains visually stable during most transitions.

### Layer 1 — Play surface

The main working content sits on neutral or white planes. Separation is usually created by tonal contrast, 1px structural lines and spacing, not shadow.

### Layer 2 — Control rail

Floating tab bar, sticky date rail, contextual filters and search use translucent material. Content can visually pass underneath, giving the user a consistent sense of location.

### Layer 3 — Commitment sheet

Booking confirmation, split payment, cancellation consequences, waitlist offer and equipment confirmation use a bottom sheet.

When a sheet opens:

- foreground sheet moves up;
- background content scales only slightly to around 0.992–0.985;
- background shifts downward by 2–4px;
- a moderate scrim appears;
- the original focal object remains recognizable.

This communicates “you are still in the same booking, now making a decision.”

### Layer 4 — Critical focus

Use only for payment failure, identity verification, irreversible refund/cancellation or a system conflict that blocks play.

### Ambient trajectory layer

Short trajectory traces may appear during transitions or live/tournament moments. They belong to the **motion layer**, not the permanent background. A static page should not be covered in curved red lines.

### Shadow rule

- Standard content: no shadow or 1px tonal border.
- Floating navigation: one soft low-alpha shadow.
- Modal/sheet: shadow + scrim, never multiple nested shadows.
- Selected table/map node: 1–2px apparent lift at most.

## Shapes

The shape language is **Cut Court / Soft Rally**: stable rectangular geometry for availability and business state, softer roundness for touch targets and player identity.

### Structural shapes

- Tables, time blocks, match rows and admin schedule cells are primarily rectangular with 8–14px radius.
- Large member cards use 20–26px radius.
- The table map should preserve the recognizable long rectangle of a table; do not turn tables into pills.

### Circular shapes

Circles are reserved for:

- player avatars;
- ball / trajectory micro-motifs;
- progress/rating rings;
- tiny status indicators.

### Pill shapes

Pills are appropriate for:

- primary mobile CTA;
- time slot chips;
- filters;
- status labels;
- compact rating/level badges.

Do not put every label inside a pill. Too many pills destroy the distinction between action, filter and status.

### Asymmetry

Member editorial sections may use slight image offsets, cropped photography and 1.1-card horizontal carousels. Booking, payment and check-in remain strongly aligned and predictable.

## Components

### Primary buttons

`{components.button-primary}` uses Table Teal. It is the only dominant action color on most screens.

Press feedback:

- 0–80ms: scale to 0.985 and darken toward `{colors.court-strong}`;
- release: return with a tight low-overshoot spring;
- haptic: light for selection, medium for booking/check-in confirmation.

Do not animate a frequently tapped primary button for more than 160ms.

### Rally accent

Rally Vermilion is used as a **moving punctuation mark**:

- live match indicator;
- score change underline;
- selected trajectory point;
- tournament hero micro-line;
- rating delta;
- short booking-success trace.

It should almost never fill a full card or large CTA.

### Table availability

A table availability card must answer at glance:

- table number / area;
- start time + duration;
- price or member benefit;
- status: available / held / booked / in use / maintenance;
- special resource: private room / robot / premium table.

Availability is communicated with text + shape + tone, never color alone.

### Table map

The map is not a decorative floor plan. It is a reservation tool.

Each table node expresses:

- table number;
- table type;
- availability;
- any special resource;
- selection state.

The physical anchors — entrance, reception, private room, robot zone — remain visible enough to orient the player.

When selected, a table node may lift 1–2px, brighten the internal “court line,” and show a short 160–200ms focus transition. It must never wobble or bounce repeatedly.

### Time slots

Time chips are horizontally scannable, stable-width and grouped by daypart. Use tabular numerals. If pricing changes by peak/off-peak, show the difference adjacent to the selected slot rather than color-coding every chip.

### Booking confirmation sheet

The sheet is a transaction checkpoint, not a second detail page.

It must show:

1. date / start / end;
2. club + table;
3. duration;
4. players / split payment if used;
5. equipment or robot add-on;
6. membership discount / entitlement;
7. exact payable amount;
8. cancellation consequence;
9. one primary confirmation CTA.

Nothing financially important is hidden behind an info icon.

### Training cards

Training cards prioritize **level + objective + time + coach**, not decorative lifestyle copy.

Recommended hierarchy:

- course name;
- level / age group;
- coach;
- time;
- remaining capacity / waitlist;
- applicable pass.

A course image is optional in schedule mode and encouraged in discovery mode.

### Coach cards

Photography uses natural club light and real playing context. Cards show:

- name;
- technical specialties (e.g. 左手陪练 / 直板 / 青少年启蒙 / 颗粒打法);
- rating / certification only if verified;
- next available times;
- private lesson / sparring role.

Avoid generic “celebrity coach” poster layouts.

### Open match / player matching card

A match card must make trust legible:

- time / club;
- current players and open spots;
- level range;
- friendly vs rated;
- estimated price per person;
- confirmation/cancellation rule.

Reasons for recommendation may appear as short chips such as “水平接近 / 同馆常打 / 时间匹配.” Do not expose personal phone numbers before a match relationship is established.

### Membership pass

The pass uses Carbon Ink with Ball White and a tiny Rally accent. It should feel like club access, not a bank card.

Show:

- membership / pass name;
- remaining hours / sessions / balance;
- validity;
- booking horizon / peak benefits;
- linked home club.

No fake metallic texture, glossy gold gradient or embossed credit-card cliché.

### Rating and growth

Player rating is a capability signal, not a medical or scientific diagnosis.

- Show one primary level/rating.
- Explain recent change.
- Separate adult competitive rating from junior progression levels if the product uses both.
- A small rally-colored delta can communicate movement.
- Deep technical dimensions belong in training progress, not the home header.

### Tournament

Tournament screens may use deeper contrast and slightly more Rally Vermilion than everyday booking screens. The key unit is still **next match**, not the whole bracket.

Score changes use a short number roll or flip around 140–180ms. Do not animate every point with fireworks.

### Check-in

Check-in is designed for walking, carrying equipment and imperfect lighting.

- Large QR / scan target.
- Current booking context above it.
- Table number is prominent after success.
- “无法签到” provides an immediate recovery path.

Success should land in a stable state: `已签到 · 18:22 · 6号台`, not disappear as a toast.

### Motion & micro-interactions — Quiet Rally Physics

Motion follows two schemes:

1. **Standard motion** for recurring controls — compact, nearly mechanical.
2. **Expressive spatial motion** for hero moments — booking confirmation, map focus, check-in, rating milestone, tournament transition.

Recommended timing:

- press / icon response: 80–120ms
- chip / slot / selection: 140–190ms
- score / queue / numeric change: 150–220ms
- list insert / state transition: 180–240ms
- local panel / filter sheet: 240–300ms
- commitment sheet: 280–360ms
- shared-element card → detail: 320–420ms

Recommended curves:

- quick effects: `cubic-bezier(0.2, 0, 0, 1)`
- entrance: `cubic-bezier(0.16, 1, 0.3, 1)`
- exit: `cubic-bezier(0.4, 0, 1, 1)`
- spatial shared motion: tight platform spring, low overshoot

#### Signature micro-motion 1 — Serve Dot

A tiny ball-sized dot appears only at the start of a meaningful commitment transition. On press it compresses along the direction of travel, then resolves into the next state. Keep the total visual distance under 16px for ordinary controls.

#### Signature micro-motion 2 — Slot Sweep

Selecting a time slot fills the selected chip from the centerline outward in 150–180ms. It echoes a table centerline without drawing a literal net.

#### Signature micro-motion 3 — Table Focus

When selecting a table on the map, the node lifts 1–2px, the internal court line brightens, and neighboring nodes slightly reduce contrast. One light haptic confirms selection.

#### Signature micro-motion 4 — Booking Seal

After a successful reservation, a Ball White point travels once across a short Rally Vermilion line and settles into the confirmation check/state. Duration 260–340ms. No confetti.

#### Signature micro-motion 5 — Waitlist Roll

Queue position changes with a vertical numeral roll. Only the number moves; the card stays stable. This communicates progress without adding anxiety.

#### Signature micro-motion 6 — Check-in Line

The scan frame runs one restrained line sweep. On success, the frame contracts into the table number/status block. Do not loop the line indefinitely if nothing is being scanned.

#### Signature micro-motion 7 — Score Flip

A new point performs a short vertical number replacement with 0–1px spatial overshoot. Rally Vermilion may flash on the scoring side for no more than 180ms.

#### Signature micro-motion 8 — Rating Arc

When rating changes after a confirmed rated match, the progress arc advances once over 280–360ms and then stops. The delta remains as text so motion is not the only carrier of information.

#### Reduced motion

When reduced motion is enabled:

- shared-element movement becomes cross-fade;
- z-depth scaling is removed;
- trajectory traces disappear;
- number roll becomes direct value change + opacity transition;
- no blur animation;
- all important state changes remain explicit in text.

### Interaction psychology

#### Recognition over recall

The user never needs to remember which membership applies, whether peak time costs more, or when free cancellation ends. Put that information at the point of decision.

#### Progressive disclosure

First layer: `可订 / 已满 / 候补 / 不可订`.

Second layer: exact reason and immediate remediation.

Third layer: complete policy if the user asks for it.

#### Choice architecture

- Home: maximum three primary quick actions.
- Booking: recommend one best table or auto-assign first; let experts choose manually.
- Coach booking: “最快可约” is a default alongside “指定教练.”
- Filters: expose 4–6 common choices; advanced filters in sheet.

#### Agency and reversibility

- Cancellation is visible, never hidden as a dark pattern.
- If cancellation costs money/credits, show the exact cost before confirmation.
- Recoverable actions get undo where meaningful.
- Irreversible financial changes require explicit confirmation and clear result state.

#### Scarcity without anxiety

Use factual availability: `仅剩2台`, `候补第3位`, `20:00后有4台`.

Do not use fake timers, pulsing red warnings or vague “many people are viewing this” copy.

#### Social trust

Player matching surfaces expose level compatibility, match intent and reliability signals before personal contact information. The product should make strangers feel safe to play, not make the interface feel like a social feed.

### State system

Every major component must have:

- default
- pressed / focused
- selected
- disabled
- loading
- success
- empty
- blocked with reason
- error with recovery

Booking surfaces additionally require:

- available
- held
- booked
- in-use
- waitlist
- maintenance
- expired hold
- price changed
- payment pending

## Do's and Don'ts

### Do

- **Do** make table tennis visually identifiable through precision geometry, table maps, rating, match rhythm and restrained trajectory motion — not literal paddle clip-art.
- **Do** use the One-Table Rule: one object or decision owns each member screen.
- **Do** make date, time, table, duration, price and cancellation consequence visible before payment.
- **Do** distinguish “订球台” from “找球友/公开约球”; they are different mental models.
- **Do** show auto-assigned table as the default when it reduces choice overload, while allowing manual selection when the venue supports it.
- **Do** surface “why recommended” in player/coach matching with short factual explanations.
- **Do** use Rally Vermilion as a kinetic signal, not the general brand flood color.
- **Do** make check-in and booking completion feel physically final through state continuity and haptics.
- **Do** let admin screens become denser while retaining the same geometry, numerals and color discipline.
- **Do** design every empty/error/blocked state with a next action.

### Don't

- **Don't** reuse Pilates/yoga visual language, body-wellness gradients, reformer imagery or spa-like soft green branding.
- **Don't** turn the product into an esports neon-red/black interface.
- **Don't** use paddles, balls and nets as decorative icons on every card.
- **Don't** cover pages in red trajectory curves. Motion motifs should appear during motion.
- **Don't** make all content a rounded card; table schedules and availability need structural grids and rows.
- **Don't** hide cancellation fees, peak pricing, membership restrictions or split-payment consequences.
- **Don't** use animation longer than necessary for repeated booking and check-in tasks.
- **Don't** use color alone to indicate table availability, level, score, error or selected state.
- **Don't** mix tournament spectacle with everyday booking screens. Competition may be more intense; daily club use remains calm.
- **Don't** copy consumer photography, giant radii and oversized cards into the admin system.
- **Don't** use tiny gray text or hairline fonts to simulate luxury.
- **Don't** make the home page a 3×4 feature launcher. The app is a playing companion, not a menu directory.

---
# PART III — Stitch SITE.md
# TT VenueOS / Rally Atelier — Product & Screen Blueprint for Google Stitch

> Visual source of truth: `.stitch/DESIGN.md`  
> Functional source of truth: `乒乓球馆SaaS_完整闭环功能清单_20260828_V2_图片功能融合版.xlsx`  
> Product: high-end table-tennis venue booking, coaching, training, player matching, tournament and operations SaaS  
> Status: pre-build design specification

---

## 1. Product Vision

The product is not a generic class-booking app. It is a **digital club layer for table tennis** connecting five physical realities:

1. **Time inventory** — date, duration, peak/off-peak, booking horizon.
2. **Table inventory** — table type, zone, private table, robot table, maintenance, live occupancy.
3. **People inventory** — coaches, sparring partners, other players, staff.
4. **Entitlements & money** — membership, table hours, class credits, private lesson packs, split payment, refunds.
5. **Competitive identity** — rating, level, training progress, open matches, tournaments.

The member experience should feel like entering a premium club that already knows the next thing the user needs. The staff experience should feel like running a live venue from one operational timeline. The admin experience should feel like a precision control system, not a dashboard collage.

### 1.1 Member mental model

The member should be able to answer in under 5 seconds:

- Can I play today?
- Which tables are available?
- How much will it cost me?
- Can my membership be used?
- Who can I play or train with?
- What happens if I cancel?
- Where do I check in?

### 1.2 Global interaction principles

1. **When before where.** Time is normally the first booking decision.
2. **Recommend before expose.** Show the best table/coach choice before presenting the full inventory.
3. **One commitment surface.** Price, entitlement, cancellation and payment live in one confirmation layer.
4. **Factual scarcity.** Show remaining tables, waitlist position and booking horizon without fake urgency.
5. **Recognition over recall.** Membership applicability and cancellation policy appear at the decision point.
6. **No hidden rule failures.** Every blocked action returns a reason and remediation.
7. **Social trust before social reach.** Level and intent matter more than public profiles in player matching.
8. **Motion explains state.** Micro-motion exists to show selection, continuity, confirmation or score/rank change.

### 1.3 Member app navigation

Use five bottom destinations maximum:

- **首页** — today, next booking, live availability, key recommendations.
- **订台** — table booking and current availability.
- **训练** — classes, private coaching, coaches, training plans.
- **约球** — open matches, player matching, rated/friendly play.
- **我的** — bookings, membership, rating, orders, history, settings.

Tournaments are exposed from Home, Training and My Activity rather than permanently occupying the bottom bar unless the tenant is tournament-first.

---

## 2. Stable Fictional Dataset for Stitch

Use one consistent dataset across screens so the generated images feel like one real product.

### Brand
`ARC TT CLUB / 弧线乒乓`

### Locations
- 静安旗舰馆
- 徐汇训练馆

### Table zones
- A区 · 标准比赛台 01–08
- B区 · 私享台 09–10
- C区 · 发球机台 11–12

### Coaches
- 林骁 — 横板两面弧圈 / 成人进阶 / 赛事陪练
- 周宁 — 少儿启蒙 / 基本功 / 多球训练
- 陈野 — 直板 / 发接发 / 颗粒打法陪练
- Vera Liu — 女子进阶 / 体能与步法

### Member
`沈言`  
Level: `TTR 1468 · 进阶 3`  
Membership: `旗舰会员`  
Table benefit: `非高峰免费 8h/月 · 剩余 3.5h`  
Training pass: `进阶小班 8次 · 剩余 3次`  
Next reservation: `今天 19:30 · A06 · 90 min`

### Example current operational facts
- 19:00–21:00 A区 only 2 tables remain.
- A06 reservation starts in 42 minutes.
- Advanced Loop class tomorrow 19:30 has 1 seat left.
- Open Match tonight 21:00 has 1 open spot, level 1400–1550.
- Robot Table 11 is in maintenance until 20:00.
- Weekend ladder tournament registration closes tomorrow 20:00.

---

## 3. Global Screen Contracts

### 3.1 Screen hierarchy

Every member screen follows:

1. **Orientation** — page, location, date or state.
2. **Focus** — one primary object/decision.
3. **Action** — one dominant next action.
4. **Context** — price, table, coach, membership, policy, player level.
5. **Explore** — alternatives or deeper information.

### 3.2 Standard states

Every major member screen is incomplete unless the design accounts for:

- loading
- empty
- partial data
- disabled
- blocked with explanation
- error with recovery
- success / confirmed
- stale / changed availability where relevant

### 3.3 Transaction states

Booking/payment flows additionally require:

- availability changed
- hold expired
- price changed
- payment pending
- payment failed
- refund pending
- cancellation penalty
- membership ineligible
- waitlist path available

### 3.4 Mobile target

- Baseline frame: 390 × 844.
- Safe area respected.
- Primary commitment action stays above the home indicator.
- System keyboard must never cover the focused input or final confirmation.
- Text scaling to at least 130% must remain usable.

---

# 4. Sitemap

Checklist items should only be marked complete after generation, visual inspection and acceptance.

## 4.1 Member App / Mini Program — `M`

### Entry & Home

- [ ] **M01 `/member/onboarding` — First-time Club Onboarding**  
  Purpose: establish location, play level, interests and preferred use in 3–5 short steps.  
  Decisions: preferred club, self-assessed level, interests `订台 / 训练 / 找球友 / 赛事`.  
  Design: one decision theme per screen; progress visible; optional fields skippable.  
  Exit: show three immediately useful actions, not a tutorial carousel.

- [ ] **M02 `/member/home` — 首页 / Today + Play**  
  First focus: next booking if one exists, otherwise live availability or recommended play window.  
  Quick actions: `订台 / 约教练 / 约球` maximum three.  
  Secondary modules: live table availability, training recommendation, open match, membership/rating pulse.  
  Never use a feature-icon grid as the hero.

- [ ] **M03 `/member/notifications` — 消息中心**  
  Group: booking, waitlist, coach/class change, payment, membership, tournament, marketing.  
  Actionable messages appear first. Each item deep-links to the business object.

- [ ] **M04 `/member/clubs` — 球馆选择**  
  Cards: distance, opening hours, current availability, table types, facilities.  
  Default to current/favorite club; never force map view for known venues.

- [ ] **M05 `/member/club/:id` — 球馆详情**  
  Hero: actual venue, table zones, opening hours, navigation, facilities, current live availability.  
  Primary CTA: `订球台`.

### Table Booking

- [ ] **M06 `/member/book-table` — 订球台入口**  
  Primary input: club + date + start time.  
  Secondary: duration, table preference, players.  
  Show a quick availability strip before full detail.

- [ ] **M07 `/member/book-table/time` — 日期与时段**  
  Sticky 7-day rail.  
  Time groups: morning / afternoon / evening.  
  Slot shows price context or membership benefit only when materially different.  
  State examples: `可订 / 仅剩2台 / 高峰 / 会员免费 / 已满`.

- [ ] **M08 `/member/book-table/select` — 球台地图选台**  
  Default option: `智能分配最合适球台`.  
  Manual map: zones + numbered tables + private/robot status.  
  Each table node: table number, type and state.  
  State: available / selected / held / booked / in-use / maintenance.

- [ ] **M09 `/member/book-table/addons` — 球员与器材**  
  Optional step: add players, split payment, robot, paddle rental, ball pack.  
  Do not force this step when user only wants a simple table booking.

- [ ] **M10 `/member/book-table/review` — 订台确认**  
  One transaction checkpoint.  
  Show: date, exact time, table, duration, players, add-ons, membership benefit, price, cancellation rule.  
  Primary CTA: exact amount, e.g. `支付 ¥72 并确认` or `使用会员时长确认`.

- [ ] **M11 `/member/book-table/success` — 订台成功**  
  Stable success state with table number, start time, navigation and check-in method.  
  Secondary: `邀请球友 / 加入日历 / 查看预约`.  
  Signature motion: Booking Seal.

- [ ] **M12 `/member/booking/:id` — 订台详情**  
  State timeline: confirmed → check-in available → in progress → completed / cancelled.  
  Actions change by time: directions / check in / extend / cancel / contact club.

- [ ] **M13 `/member/booking/:id/reschedule` — 改期 / 换台**  
  If permitted: hold new slot first, then release old slot.  
  Show price/membership difference before confirmation.

- [ ] **M14 `/member/booking/:id/cancel` — 取消预约**  
  Must display exact refund/credit consequence before destructive action.  
  Offer reschedule first when appropriate, without making cancellation hard to find.

- [ ] **M15 `/member/booking/:id/extend` — 延时续台**  
  Check the next time block and linked resource availability.  
  If unavailable, show the closest alternative table/time.

- [ ] **M16 `/member/table-waitlist` — 黄金时段候补**  
  For fully booked peak blocks if the tenant enables table waitlist.  
  Explain match criteria, response time and whether table is auto-assigned.

- [ ] **M17 `/member/split-payment/:bookingId` — AA / 分账**  
  Show total, participants, paid/unpaid status and deadline.  
  Owner can cover unpaid remainder if policy permits.

### Training & Coaching

- [ ] **M18 `/member/training` — 训练首页**  
  Segments: `课程 / 私教·陪练 / 教练`.  
  First module prioritizes next booked training or one suitable next session.  
  Filters remain secondary.

- [ ] **M19 `/member/training/classes` — 训练课程列表**  
  Filters: level, age group, objective, coach, time.  
  Each row shows level, coach, time, remaining seats/waitlist, eligible pass.

- [ ] **M20 `/member/training/class/:id` — 课程详情**  
  Hero: skill objective, level, coach, date/time, capacity.  
  Eligibility and pass consumption above sticky CTA.  
  Cancellation rule visible before booking.

- [ ] **M21 `/member/training/class/:id/book` — 课程预约确认**  
  Compact sheet/page: session, coach, pass to consume, balance after booking, cancellation consequence.  
  If full: switch primary action to `加入候补`.

- [ ] **M22 `/member/training/waitlist/:id` — 训练课候补**  
  Show queue position, autofill/offer mechanics, expiry and notification method.  
  Signature motion: Waitlist Roll.

- [ ] **M23 `/member/coaches` — 教练 / 陪练列表**  
  Filters: specialty, level, role, available soon, club.  
  Cards include technical tags, next availability and service type.

- [ ] **M24 `/member/coach/:id` — 教练详情**  
  Natural portrait, technical style, suited level, verified credentials, next class/private availability.  
  Primary CTA: `查看可约时间`.

- [ ] **M25 `/member/coach/:id/slots` — 教练可约时间**  
  Date rail + available slots.  
  System has already merged coach, table and room/resource availability.  
  Offer `最快可约` and alternate tables/coaches when relevant.

- [ ] **M26 `/member/private/review` — 私教 / 陪练确认**  
  Show coach, table, service duration, pass/price, late cancellation policy.  
  Optional repeat booking is secondary.

- [ ] **M27 `/member/private/success` — 私教预约成功**  
  Stable result + training objective + preparation note + directions.

- [ ] **M28 `/member/training/progress` — 训练成长**  
  Primary level/rating, attendance, coach notes and recent progress.  
  Do not present unsupported biometric/medical interpretations.

### Open Matches / Player Matching

- [ ] **M29 `/member/matches` — 约球首页**  
  Tabs: `可加入 / 我的约球`.  
  Recommended matches prioritized by time, club, level and intent.  
  Primary actions: `加入` or `发起约球`.

- [ ] **M30 `/member/matches/create` — 发起约球**  
  Inputs: date/time, club, friendly/rated, level range, spots, table payment rule.  
  Do not ask for unnecessary social profile information.

- [ ] **M31 `/member/match/:id` — 约球房间**  
  Show players, open spots, compatibility, booking/table state, per-person price, confirmation rule.  
  Personal contact remains protected until policy permits.

- [ ] **M32 `/member/match/:id/join` — 加入约球确认**  
  Confirm level, price, cancellation and whether joining reserves/locks the table.  
  If match is not yet table-backed, say so explicitly.

- [ ] **M33 `/member/match/:id/result` — 比分 / 结果确认**  
  Rated match: result entered → both sides confirm → rating updates.  
  Friendly match: score optional.  
  Signature motion: Score Flip and Rating Arc.

- [ ] **M34 `/member/rating` — 水平等级 / Rating**  
  One primary rating, change explanation, recent rated results and progression.  
  Separate junior progression track from adult competitive rating if both are used.

### Tournament

- [ ] **M35 `/member/tournaments` — 赛事中心**  
  Upcoming tournaments, registration status, level/age groups.  
  More intense visual contrast is allowed, but keep Rally Atelier tokens.

- [ ] **M36 `/member/tournament/:id` — 赛事详情**  
  Event format, date, venue, eligibility, fee, registration deadline, prize/info, cancellation rules.  
  CTA: `报名` or `查看我的赛程`.

- [ ] **M37 `/member/tournament/:id/register` — 报名确认**  
  Group, rating/eligibility, fee, waiver/agreement.  
  No unrelated upsell.

- [ ] **M38 `/member/tournament/:id/bracket` — 签表 / 分组**  
  Mobile-first bracket or group list.  
  Default focus is `我的路径` rather than the entire dense bracket.

- [ ] **M39 `/member/tournament/:id/next` — 下一场**  
  Opponent, table, estimated/start time, check-in status, score entry where permitted.  
  This is the tournament One Big Thing surface.

### Check-in, Wallet & Me

- [ ] **M40 `/member/check-in` — 到馆签到**  
  Show current booking + large QR/scan target + fallback.  
  Success state: `已签到 · 19:18 · A06`.  
  Signature motion: Check-in Line.

- [ ] **M41 `/member/wallet` — 会员 / 卡项**  
  Primary pass, table hours, training credits, balance, expiry and benefits.  
  Expiring or low-balance asset gets one action priority.

- [ ] **M42 `/member/pass/:id` — 卡项详情**  
  Status, remaining hours/credits, validity, peak/off-peak use, applicable clubs/tables/classes, ledger.  
  Freeze/renew/transfer only when policy allows.

- [ ] **M43 `/member/orders` — 订单与支付**  
  Table, training, coach, tournament and retail orders in one consistent money model.

- [ ] **M44 `/member/order/:id` — 订单详情 / 退款**  
  Financial timeline, payment status, linked booking/pass, cancellation/refund state.  
  Failure recovery preserves user context.

- [ ] **M45 `/member/history` — 打球 / 训练历史**  
  Tabs/filters: table play, training, matches, tournaments.  
  Show meaningful recent patterns without turning it into a social feed.

- [ ] **M46 `/member/me` — 我的**  
  Identity + membership + rating first; then bookings/history/orders; settings/service last.  
  No long list of equal-weight feature tiles.

- [ ] **M47 `/member/family` — 家庭 / 监护**  
  For junior training: participant, payer and guardian identities remain explicit.

- [ ] **M48 `/member/settings` — 设置**  
  Notifications, privacy, account, authorized family relationships, help.

### Shared state screens

- [ ] **M49 `state/empty` — Empty State Family**  
  No available tables / no classes / no matches / no orders. Each state has a meaningful next step.

- [ ] **M50 `state/error` — Error & Recovery Family**  
  Network, payment, table just taken, membership invalid, check-in blocked. Preserve context and offer recovery.

- [ ] **M51 `state/success` — Success Family**  
  Booking, payment, check-in, tournament registration. Success must settle into a stable business state, not only toast.

- [ ] **M52 `state/waitlist` — Waitlist / Offer Family**  
  Training and table waitlist, offer timer, accepted/expired states.

- [ ] **M53 `components/sheets` — Bottom Sheets & Dialogs**  
  Booking confirm, cancel consequence, split payment, add equipment, level filter, waitlist offer, refund impact.

- [ ] **M54 `components/library` — Mobile Component Library**  
  Buttons, chips, table nodes, time slots, status pills, score, rating, membership, navigation, loading/skeleton, alerts.

## 4.2 Staff / Coach Mobile — `S`

- [ ] **S01 `/staff/today` — 今日工作台**  
  Upcoming classes/private lessons, table issues, check-ins, waitlist, tasks and exceptions.

- [ ] **S02 `/staff/tables` — 球台实时状态**  
  Table grid/timeline: available / booked / checked-in / in-use / cleaning / maintenance.  
  Fast actions: extend, change table, maintenance.

- [ ] **S03 `/staff/session/:id` — 课程名单**  
  Booked, waitlist, checked-in, no-show, pass/notes context.

- [ ] **S04 `/staff/check-in` — 扫码 / 搜索签到**  
  QR scan + member/booking search fallback.

- [ ] **S05 `/staff/member/:id` — 会员速览**  
  Active pass, table hours, training balance, next booking, rating/coach relationship, risk alerts.

- [ ] **S06 `/staff/quick-book` — 代订台 / 代约课**  
  Same eligibility rules as member self-service; overrides require reason and permission.

- [ ] **S07 `/staff/calendar` — 教练日历 / 可用性**  
  Classes, private lessons, blocked time, leave, cross-location work.

- [ ] **S08 `/staff/tasks` — 任务与预警**  
  Renewal, payment failure, high-value member follow-up, table maintenance, class exception.

- [ ] **S09 `/staff/tournament` — 赛事执行**  
  Check-in, table assignment, next match, score confirmation, delay/forfeit exception.

- [ ] **S10 `/staff/pos` — 快捷收银**  
  Sell/renew pass, table payment, retail, authorized discount, receipt.

## 4.3 Admin Web — `A`

- [ ] **A01 `/admin/overview` — 老板经营驾驶舱**  
  First: needs-attention queue. Then cash, table utilization, class utilization, active members, new leads, trends.

- [ ] **A02 `/admin/today` — 今日运营**  
  Unified time rail for tables, classes, private lessons, tournaments and exceptions.

- [ ] **A03 `/admin/tables` — 球台排期 / 实时台况**  
  Time on vertical axis, tables on horizontal axis. Drag is an enhancement; menu/form alternatives required.

- [ ] **A04 `/admin/table/:id` — 球台详情**  
  Status, type, price, maintenance, current/future bookings, revenue/utilization.

- [ ] **A05 `/admin/schedule` — 训练课程排期**  
  Week calendar, coach/table/room conflicts, copy week, one-click generate draft.

- [ ] **A06 `/admin/session/:id` — 训练课详情**  
  Roster, waitlist, attendance, pass consumption, coach/table resource, change log.

- [ ] **A07 `/admin/members` — 会员列表**  
  Saved views: expiring, inactive, high-frequency, tournament, junior, payment failed.

- [ ] **A08 `/admin/member/:id` — 会员360**  
  Identity, membership, table hours, training credits, rating, next booking, coach relationship, timeline, quick actions.

- [ ] **A09 `/admin/leads` — 线索 / 试课**  
  Lead → trial → attendance → offer → first purchase.

- [ ] **A10 `/admin/products` — 卡项 / 会员产品**  
  Table hours, memberships, training packs, private packs, cross-location, family/team products.

- [ ] **A11 `/admin/orders` — 订单 / 支付 / 退款**  
  Precise financial states and drill-down.

- [ ] **A12 `/admin/finance` — 财务与对账**  
  Cash received vs consumption/service recognition, refunds, outstanding entitlement/service liability.

- [ ] **A13 `/admin/staff` — 员工 / 教练**  
  Role, locations, skills, availability, workload, sales/teaching performance, permissions.

- [ ] **A14 `/admin/payroll` — 薪资 / 提成**  
  Event-traceable commission and payroll statements.

- [ ] **A15 `/admin/tournaments` — 赛事管理**  
  Registration, eligibility, draw, table scheduling, score, results, rating integration.

- [ ] **A16 `/admin/marketing` — 营销 / 自动化**  
  New member trial, inactive return, expiring pass, open match, tournament campaign.

- [ ] **A17 `/admin/reports/tables` — 球台利用率**  
  Day/time heatmap, peak pressure, no-show/cancellation, table type revenue.

- [ ] **A18 `/admin/reports/training` — 训练与教练分析**  
  Fill, attendance, waitlist pressure, coach utilization, retention context.

- [ ] **A19 `/admin/reports/members` — 会员 / 留存 / 续费**  
  Active, renewal, risk, rating/activity cohorts.

- [ ] **A20 `/admin/settings` — 规则 / 权限 / 白标 / 集成**  
  Booking, cancellation, waitlist, table pricing, pass rules, notification, roles, mini-program theme, payments, devices.

---

# 5. Roadmap

Do not generate the entire product in one Stitch prompt. Use these visual gates.

## Phase 0 — Visual calibration

Generate first:

1. M02 Home
2. M07 Date & Time
3. M08 Table Map
4. M10 Booking Review
5. A01 Admin Overview
6. A03 Table Timeline

**Gate:** table-tennis identity must be obvious without paddles/balls being decorative wallpaper. Member UI must feel premium; admin UI must feel like the same system at higher density.

## Phase 1 — Complete table booking

Generate M06–M17 + M40.

**Gate:** a first-time user can book a table, understand price/membership/cancellation, pay, arrive and check in without hidden rules.

## Phase 2 — Training & coaching

Generate M18–M28 + S03/S07.

**Gate:** class booking and private coaching visibly differ as mental models. Coach + table resource conflicts are hidden from the member but handled by the system.

## Phase 3 — Player matching

Generate M29–M34.

**Gate:** private table reservation and open match are visibly distinct. Level, intent, price and confirmation state are always clear.

## Phase 4 — Tournament

Generate M35–M39 + S09 + A15.

**Gate:** tournament uses more energy without visually becoming a separate esports product.

## Phase 5 — Membership & lifecycle

Generate M41–M48 + A07–A12.

**Gate:** pass balance, table hours, training credits, orders and refunds use consistent financial/entitlement language.

## Phase 6 — Staff and admin operations

Generate S01–S10 + A01–A20.

**Gate:** operations prioritize exceptions and today’s workload rather than dashboard decoration.

## Phase 7 — States and system library

Generate M49–M54, then audit every existing screen against them.

**Gate:** blocked/error/empty/success states look like first-class product states, not last-minute illustrations.

---

# 6. Creative Freedom

## 6.1 Allowed

- Use a short table-line or ball-trajectory motif in hero/transitional moments.
- Crop table-tennis photography aggressively if it improves focus and negative space.
- Use slightly asymmetric editorial compositions in Home, Coach and Tournament discovery.
- Use Rally Vermilion more strongly in tournament/live contexts while preserving the palette hierarchy.
- Add concise contextual microcopy that explains why a table/coach/match is recommended.
- Use direct labels in data visualization instead of legends where possible.
- Adapt club photography and accent tone for tenant branding while preserving system contrast and semantic colors.

## 6.2 Not allowed

- Neon esports red/black visual language.
- Red gradient glows, RGB streaks or cyber grid backgrounds.
- Literal ping-pong-ball clip-art repeated as decoration.
- Giant rackets or paddles as page backgrounds.
- All screens turned into rounded-card dashboards.
- Marketing carousel dominating Home.
- Hidden cancellation/peak pricing/membership rules.
- Drag-only table/schedule operations.
- Color-only availability or score states.
- Admin screens styled like consumer lifestyle cards.

## 6.3 Content realism

Use realistic table-tennis-specific examples: table numbers, 60/90/120-minute bookings, coaching objectives, level ranges, adult/junior classes, robot tables, open matches and tournaments. Never use Pilates, yoga, reformer, spin-bike or generic “wellness class” content.

---

## 7. Stitch Acceptance Checklist

Before marking a screen complete:

- [ ] Clearly follows `.stitch/DESIGN.md`.
- [ ] The screen’s One Big Thing is obvious within 3 seconds.
- [ ] Table-tennis identity comes from geometry, content and motion — not decorative clip-art.
- [ ] One dominant CTA only.
- [ ] Date/time/table/price/member benefit/cancellation are visible when relevant.
- [ ] Availability and status do not rely only on color.
- [ ] Blocked actions explain why and what the user can do next.
- [ ] Touch targets >=44px.
- [ ] Mobile safe area is credible.
- [ ] Text remains legible without tiny gray captions.
- [ ] Motion intent is stated for hero or important state changes.
- [ ] Reduced-motion fallback exists for signature motion.
- [ ] Cross-screen data remains consistent with the stable dataset.
- [ ] No Pilates/yoga/reformer visual or textual drift.
- [ ] Admin screens are denser and less photographic than member screens.
