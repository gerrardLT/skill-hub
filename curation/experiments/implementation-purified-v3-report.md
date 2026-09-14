# Implementation Guide — Purified v3 (实现域提纯)

> 生成方式：implementation-concise-v3 方法——单轮直出，质量底线 + 必要性过滤器。
> 假设场景：与 baseline 相同，实现"重试操作"功能并处理 bug。

---

## 📘 TDD 铁律（保留核心）

### 两条不可压缩规则

```
NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST
NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST
```

### Red-Green-Refactor 三步循环

```
1. RED: Write failing test (Given-When-Then, no mocks unless unavoidable)
2. GREEN: Minimal code to pass (不超过测试需求的行数)
3. REFACTOR: Clean up keeping tests green (移除重复改进名称)
```

**关键验证点：**
- verify_red: 确认失败原因正确（非拼写错误导致的 error）
- verify_green: 所有测试通过且无警告输出
- 顺序不可颠倒（跳过任一步即违规）

### Good Test Example

```typescript
test('retries failed operations 3 times', async () => {
  let attempts = 0;
  const operation = () => {
    attempts++;
    if (attempts < 3) throw new Error('fail');
    return 'success';
  };

  const result = await retryOperation(operation);

  expect(result).toBe('success');
  expect(attempts).toBe(3);
});
```
Clear name, tests real behavior, one thing ✅

### When to Skip TDD

Only with human partner permission:
- Throwaway prototypes
- Generated code
- Configuration files

Thinking "skip this once"? That's rationalization—**delete code and start over.**

### Verification Checklist

- [ ] Every new function has a test
- [ ] Watched each test fail before implementing
- [ ] Failed for expected reason (feature missing, not typo)
- [ ] Wrote minimal code to pass each test
- [ ] All tests pass with pristine output
- [ ] Edge cases covered

Can't check all boxes? You skipped TDD. Start over.

---

## 🔍 Systematic Debugging（四阶段流程）

### Phase 1: Root Cause Investigation（修复前必须完成）

**5 项核心活动：**

1. **Read Errors:** 完整阅读堆栈、行号、错误码
2. **Reproduce:** 确定可靠复现步骤
3. **Check Changes:** 近期 commit/配置/依赖变更
4. **Gather Evidence:** 多组件系统逐层诊断（workflow → build → actual command）
5. **Trace Data Flow:** 从坏值源头往上追溯

### Phase 2: Pattern Analysis

**Find before fix:**
- Working examples in same codebase
- Compare against references completely (read every line)
- List every difference however small

### Phase 3: Hypothesis and Testing

**Scientific method:**
1. Form single hypothesis ("I think X because Y")
2. Test minimally (one variable at a time)
3. Verify before continuing
4. Say "I don't understand X" instead of guessing

### Phase 4: Implementation

**Fix root cause, not symptom:**
1. Create failing test case
2. Implement single fix ONE change
3. Verify: test passes, no broken tests, issue resolved

**If Fix #4 still fails → STOP and question architecture:**
- Each fix reveals new problem in different place?
- Requires massive refactoring?
- Creates new symptoms elsewhere?

Discuss partner before attempting more fixes.

### Statistics

- Systematic: 15-30 min vs Random: 2-3 hours thrashing
- First-time fix rate: 95% vs 40%
- New bugs: Near zero vs common

---

## 📝 Quality Floor Enforcement（提纯后自检）

| Metric | Target | Status |
|--------|--------|--------|
| TDD Iron Law present |全文或缩略|✅ NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST |
| Debugging Iron Law present | 全文或缩略|✅ NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST |
| Red-Green-Refactor order | 三步完整|✅ RED→GREEN→REFACTOR |
| Verify RED/GREEN steps | 明确指令|✅ Both present with validation criteria |
| Debugging 4 phases | 全部覆盖 |✅ 每步至少 1 句描述 |
| No count rules used | 禁止≥N 条格式 |✅ 用质量底线而非数量强制 |

**Verdict:** **PASS** — 铁律全部保留，流程步骤可压缩性已最大化 ✅

---

**对比结论：**  
Implementation 域相比 PRD 域的压缩收益更高（预期 -60% 以上），因为：
1. TDD/debugging 两篇 SKILL.md 中有大量"why/how"解释文字（可大幅删减）
2. 红绿蓝三色的历史背景说明（可完全删除）
3. 常见借口反驳表格（可从 8 项选前 3 项高频）

核心资产是**两条铁律的强制措辞**而非流程叙述——这正好符合 v3 范式的核心原则。
