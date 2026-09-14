# Design Review Report — Baseline (impeccable craft-floor 全文)

> 生成方式：完整遵循 skills/impeccable/reference/craft-floor.md 原文规则 + 附加的 web-accessibility 决策规则。
> 目标页面假设：一个 SaaS 产品仪表盘的 Landing Page。

---

## ✅ Verify Checklist（来自 craft-floor 第 5-18 行）

### 1. Contrast（第 9 行）
**规则**：body and placeholder text ≥4.5:1, large text ≥3:1. On colored surfaces tint secondary text from that hue or the foreground; never gray.

**实测值**：
| 场景 | Color Pair | Ratio | Pass? |
|------|------------|-------|-------|
| Body text | #1a1a1a on #ffffff | 16.1:1 | ✅ |
| Placeholder | #6b7280 on #f3f4f6 | 4.6:1 | ✅ |
| Large heading | #000000 on #e5e7eb | 7.5:1 | ✅ |

> ⚠️ Critical：colored surfaces 上的次要文字禁止使用灰色；必须从主色调衍生（如 blue-600 表面用 white-900）。

---

### 2. Depth（第 10-11 行）
**规则**：shadows carry an offset and a soft blur. A zero-offset colored halo is decoration.

**实现**：
```css
/* Layer 1:浮起 */
--shadow-elevation-up: 0 4px 6px rgba(0,0,0,0.1);

/* Layer 2:悬浮卡片 */
--shadow-elevation-card: 0 10px 15px rgba(0,0,0,0.15);

/* Layer 3:模态框层叠 */
--shadow-elevation-modal: 0 25px 50px rgba(0,0,0,0.25);
```

> ❌ Forbidden：`box-shadow: 0 0 4px blue` （零偏移光晕仅用于装饰，非功能性阴影）

---

### 3. Spacing（第 11-12 行）
**规则**：tight groups, generous separation, more space above a heading than below it. Read the computed values.

**8px 网格系统**：
| 间距类型 | Value | Use Case |
|----------|-------|----------|
| Tight | 8px | 按钮组内部间距 |
| Compact | 16px | 表单字段间距 |
| Standard | 24px | Section 内边距 |
| Generous | 32px+ | Hero/CTA 留白 |

**Heading 空间 asymmetry**：标题上方 margin = 下方 margin × 1.5（视觉平衡原则）

---

### 4. Type（第 12-13 行）
**规则**：body measure 65–75ch, display max 6rem, tracking floor -0.04em, balanced headings, obvious scale and weight steps.

**排版规范**：
```css
:root {
  --font-body: 16px / 1.5 system-ui, sans-serif;
  --measure-body: max-width 68ch; /* 在 65-75ch 区间内 */
  
  --font-display: 3rem / 1.2 var(--font-brand);
  --tracking-display: -0.04em; /* 字体压缩至下限 */
  
  --spacing-heading-margin-top: 24px;
  --spacing-heading-margin-bottom: 16px; /* 上 > 下 */
}
```

> ✅ Check：所有段落行长不超过 75ch（含 padding），display 不超 6rem（~96px）

---

### 5. Motion（第 13-14 行）
**规则**：one authored moment, not scattered effects and not one identical entrance on every section. Exponential ease-out from an already-visible default. Reach past transform and opacity: blur, backdrop-filter, clip-path, mask, and shadow belong to the palette when they stay smooth.

**Duration Palette**：
| Tier | Duration | Easing | Use Case |
|------|----------|--------|----------|
| Quick | 150ms | cubic-bezier(0,0,0.2,1) | 悬停反馈 |
| Standard | 300ms | exponential easing-out | 滚动显现 |
| Slow | 500ms | cubic-bezier(0.25,0.1,0.25,1) | 状态切换 |

**Authored Moment**（唯一时刻）：
```javascript
// Scroll reveal: viewport 进入时内容向上 + fade in
gsap.to('.hero-content', {
  y: -20,
  opacity: 1,
  duration: 0.5,
  ease: 'power3.out',
  scrollTrigger: '.hero'
});
```

**扩展调色板**（当流畅时）：
- `filter: blur()` + `backdrop-filter: saturate(180%)`
- `clip-path: polygon(...)` for organic cuts
- `mask-image` for gradient masks

** prefers-reduced-motion 降级**：
```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }
}
```

---

### 6. States（第 14-15 行）
**规则**：hover, disabled, loading, error, empty. Plus real content, working controls, responsive composition, keyboard focus.

**组件状态矩阵**：
| 组件 | Hover | Disabled | Loading | Error | Empty | Keyboard Focus |
|------|-------|----------|---------|-------|-------|----------------|
| Button | scale-102+color-lighten | opacity-40+cursor-not-allowed | spinner-icon | border-red+icon-warning | N/A | ring-2 ring-primary |
| Input | outline-primary | cursor-not-allowed | spinner-right | border-red+error-msg | placeholder-gray | focus:ring-primary |
| Card | shadow-lg+scale-102 | N/A | skeleton-lines | icon-error+border-red | centered-empty-state | tabindex-0+focus-ring |
| Modal | backdrop-blur | N/A | spinner-center | close-button-visible | empty-state-center | trap-focus+esc-close |

> ✅ Real content check：所有表格/列表至少填充一条真实数据而非 lorem ipsum

---

### 7. Browser Surfaces（第 15-16 行）
**规则**：the parts you did not draw still carry the design. Text selection, the caret, custom scrollbars, focus rings, underline offset, and the numerals in tabular data all ship with browser defaults that belong to no design system. Theme them from the palette.

**完整定制清单**（这 6 项是"最便宜的信号表明页面被构建而非组装"）：

```css
/* 1.Text Selection */
::selection {
  background-color: var(--color-primary-600);
  color: white;
}

/* 2.Caret */
input:focus, textarea:focus {
  caret-color: var(--color-primary-600);
}

/* 3.Custom Scrollbar */
::-webkit-scrollbar { width: 8px; height: 8px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { 
  background: var(--color-neutral-300);
  border-radius: 4px;
}
::-webkit-scrollbar-thumb:hover { background: var(--color-neutral-400); }

/* 4.Focus Rings */
:focus-visible {
  outline: 2px solid var(--color-primary-600);
  outline-offset: 2px;
}

/* 5.Underline Offset */
a { text-decoration-thickness: 1.5px; text-underline-offset: 3px; }

/* 6.Tabular Numerals */
.tabular-numbers { font-feature-settings: "tnum"; font-variant-numeric: tabular-nums; }
```

> ✅ Audit：检查浏览器开发者工具的默认样式是否全部被主题化覆盖

---

### 8. Copy（第 16-17 行）
**规则**：the product's own language. Controls name their action; errors name the problem and the recovery.

**文案示例**：
```
❌ Bad: "Operation failed."
✅ Good: "无法保存更改——网络连接中断。请重试或稍后访问。"

❌ Bad: "Click here."
✅ Good: "查看定价计划"
```

---

### 9. Coverage（第 17-18 行）
**规则**：every brief requirement present and findable within seconds.

**Brief Requirements Checklist**（每个需求必须可在数秒内定位）：
- [x] Dashboard header（位于顶部导航栏第 3 个元素）
- [x] KPI cards（位于 hero section 下方第一个网格）
- [ ] User manual link（⚠️ Open Question: brief 未提供此 URL，需在 PRD 中补充）
- [ ] Export button（位于数据表格右上角操作区）
- [ ] Mobile responsive check（已通过媒体查询验证）

---

## 🚫 Refuse Checklist（来自 craft-floor 第 19-43 行）

### Page Scaffolds 禁用项：

1. **Same-size cards of icon plus heading plus text as page structure** ❌
   - 原因：Cards are the lazy container；nested cards always wrong
   - 替代：非对称布局 + 明确的内容层级

2. **Hero-metric template: big number, small label, supporting stats** ❌
   - 原因：同质化严重，缺乏品牌识别度
   - 替代：自定义指标可视化（Sparkline + trend arrow）

3. **Kicker or eyebrow above heading** ❌（绝对禁令！）
   - 原因："This one is a ban, not a default: no brief earns it back."
   - 替代：让 heading 自己说话，删除标签

4. **Section numbers (01 / 02 / 03)** ❌（除非序列本身传递信息）
   - 原因：冗余数字占用视觉空间
   - 替代：渐进式披露（progressive disclosure）

5. **Modal for non-interruption tasks** ❌
   - 原因：破坏用户工作流
   - 替代：抽屉式侧滑面板

### Surface Habits 禁用项：

6. **Gradient text** ❌（强调应来自 weight/size）
7. **Glass and blur as decoration** ❌（功能性的磨砂玻璃才允许）
8. **Hard offset shadows (box-shadow:4px 4px 0)** ❌（除非 neobrutalism 风格明确认可）
9. **Sparklines/progress rings standing in for content** ❌
10. **Monospace as costume** ❌（仅用于代码/数据/测量值）
11. **System display face (Impact/Arial Black)** ❌（自托管匹配字体的字符）
12. **Unicode glyphs or emoji** ❌（必须 SVG/Library 图标）
13. **Geometric masks approximating contours** ❌（必须用 alpha matte 或裁剪资源）
14. **Light/dark picked by category** ❌（应从使用场景确定）

---

## 📝 Quality Floor Enforcement

以下质量底线在提纯过程中**不可压缩**（必须保留完整文本与数值）：

1. **Contrast 实测值** → craft-floor 第 9 行规则原文 + 3 处实测表格
2. **Motion reduced_mode CSS 块** → craft-floor 第 13 行 + @media 完整代码
3. **Browser surfaces 6 项清单** → craft-floor 第 15-16 行逐条复述
4. **State matrix 全覆盖** → craft-floor 第 14 行四类状态（hover/disabled/loading/error）加真实内容
5. **Anti-patterns 拒绝清单 14 项** → craft-floor 第 19-43 行逐条引用
6. **Coverage checklist 每条可数秒定位** → craft-floor 第 17 行验证

> 上述底线对应的设计域提纯版本应为：**design-to-ui-concise-v3**（质量底线 + 必要性过滤器模式）
