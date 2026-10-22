---
name: dev-loop
description: >-
  契约化六步研发闭环总控：将自然语言意图路由到 released recipe，按 exact-version released slot 或 sub-recipe 执行需求、设计、实现、独立 QA、交付预检和复盘回流。维护 .workflow/state.json 机器状态及生成的 state.md 视图；歧义、缺输入、未授权或无发布证据时 fail closed。
---

# Dev Loop

六阶段候选尚未发布；本入口当前只可运行 `requirements-to-acceptance-criteria@0.2.0`。完整闭环请求必须返回 `blocked`，不得执行候选 Recipe。

唯一运行链：

```text
自然语言或显式 Recipe
  → released-only catalog
  → exact Recipe ref
  → exact released Slot/sub-Recipe refs
  → Gate 与证据
  → .workflow/state.json
```

## 不变量

1. 只使用 `recipes/catalog.json` 中且验证通过的 released Recipe。
2. 显式 Recipe 优先，其次续接有效状态，最后才做自然语言分类。
3. 歧义返回 `needs-input`；不得猜测、自动平替或调用原始 `skills/`。
4. `.workflow/state.json` 是机器事实源；`.workflow/state.md` 仅由它生成。
5. 任一步非 `passed` 均执行声明的 `failure_routes`；没有唯一匹配路由即停止。
6. 上游变化、失败回跳或 Contract 变化使目标及所有下游旧证据失效；即“上游哈希变化使依赖它的旧证据失效”。
7. 重试受预算与重复失败指纹限制，禁止死循环。
8. QA 不修改产品源码，只报不修。
9. 未显式授权时，禁止代码写入、远端 Git、网络、合并与部署。
10. `ship-release` 默认仅生成 release-ready 包，不执行 merge/deploy。
11. `skills/` 为只读来源快照。

## 入口

- 已发布：`requirements-to-acceptance-criteria@0.2.0`
- 六阶段与完整闭环：候选文件位于 `evals/candidates/full-dev-loop/recipes/`，不可运行。

## 执行

```bash
python tools/curation/recipe_route.py "<用户意图>" \
  --recipes-root recipes --slots-root slots --workspace-root .

python tools/curation/recipe_execute.py \
  --recipe recipes/<recipe>.json \
  --input <input.json> \
  --output-dir <run-dir> \
  --state-dir <target-project>/.workflow \
  --workspace-root .
```

实现 Recipe 需要代码写入时，调用方还须提供：

```text
--authorize workspace-write
```

六阶段实现尚未具备宿主强制的命令级权限隔离；不得将 `--authorize` 视为 `bash` 的网络或远端 Git 隔离。

## 状态

每次外部执行边界前后均原子保存：Recipe ref、步骤 ref、状态、输入哈希、产物、证据、尝试次数、失败指纹及失效历史。状态损坏时保留原文件并返回 `blocked`。

## 回流

`retro-to-requirements.next-requirements` 显式映射到下一轮 `write-prd.validated-product-brief`；不得只生成孤立复盘文档。
