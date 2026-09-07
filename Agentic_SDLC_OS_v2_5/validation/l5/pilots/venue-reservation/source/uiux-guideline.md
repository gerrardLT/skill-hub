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
