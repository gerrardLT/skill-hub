# Production Readiness — 技术设计文档

## Overview

本设计文档覆盖 MirrorMind 上线前 7 项生产就绪改造的具体实现方案。

## Architecture

### 变更后系统架构

```
┌─────────────────────────────────────────────────────────────────┐
│                    FastAPI Application                            │
├─────────────────────────────────────────────────────────────────┤
│  Middleware Layer (新增):                                         │
│    ├── RateLimitMiddleware (slowapi, IP-based)                   │
│    └── AuthMiddleware (JWT + anonymous fallback)                 │
├─────────────────────────────────────────────────────────────────┤
│  API Routes:                                                     │
│    ├── /v2/auth/* (register, login)                             │
│    ├── /v2/conversation/* (对话，含流式响应)                      │
│    ├── /v2/growth/* (成长可视化，新增)                            │
│    ├── /v2/proactive-messages/* (主动消息)                       │
│    └── /internal/metrics (运营指标，新增)                         │
├─────────────────────────────────────────────────────────────────┤
│  Agent Runtime:                                                   │
│    ├── react_loop.py (ReAct Loop, 最终回复改为流式)              │
│    ├── providers.py (新增 generate_stream 方法)                  │
│    └── knowledge_base.py (加载 55+ 知识条目)                     │
├─────────────────────────────────────────────────────────────────┤
│  Services (新增):                                                │
│    ├── growth.py (认知成长计算)                                   │
│    ├── alerts.py (webhook 告警)                                  │
│    └── identity_migration.py (匿名→注册迁移)                    │
└─────────────────────────────────────────────────────────────────┘
```

### 流式生成数据流

```
变更前:
  Agent respond → generate_json(完整) → 单次 token SSE → 前端显示

变更后:
  Agent respond → generate_stream(流式) → 多次 token SSE(每次10-50字) → 前端逐chunk追加
                                        ↓
                              TTFT < 500ms (首 token 立即推送)
```

---

## Components and Interfaces

### 1. Rate Limiting (Req 1)

**依赖**: `slowapi>=0.1.9`（基于 limits 库，内存存储）

**文件**: `app/core/rate_limit.py` (新增)

```python
from slowapi import Limiter
from slowapi.util import get_remote_address
from app.core.config import get_settings

settings = get_settings()

limiter = Limiter(
    key_func=get_remote_address,
    default_limits=[f"{settings.rate_limit_global_per_minute}/minute"],
    storage_uri="memory://",
)
```

**文件**: `app/main.py` (修改)

```python
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from app.core.rate_limit import limiter

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
```

**文件**: `app/api/v2/conversation.py` (修改)

```python
from app.core.rate_limit import limiter

@router.post("/{session_id}/message")
@limiter.limit(f"{settings.rate_limit_conversation_per_hour}/hour")
async def send_message(...):
    ...
```

**配置** (`config.py` 新增):
```python
rate_limit_conversation_per_hour: int = Field(default=10)
rate_limit_global_per_minute: int = Field(default=30)
```

---

### 2. LLM Streaming (Req 2)

**文件**: `app/ai/providers.py` (新增方法)

```python
class DashScopeNativeAdapter:
    ...
    async def generate_stream(
        self, *, system_prompt: str, user_prompt: str, model: str
    ) -> AsyncGenerator[str, None]:
        """流式生成，逐 chunk yield 文本片段。"""
        url = f"{base_url}/services/aigc/multimodal-generation/generation"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "X-DashScope-SSE": "enable",
        }
        body = {
            "model": model,
            "input": {"messages": [...]},
            "parameters": {"incremental_output": True, "enable_thinking": False},
        }
        async with httpx.AsyncClient() as client:
            async with client.stream("POST", url, headers=headers, json=body, timeout=30) as resp:
                async for line in resp.aiter_lines():
                    if line.startswith("data:"):
                        chunk = json.loads(line[5:])
                        text = self._extract_incremental_text(chunk)
                        if text:
                            yield text
```

**文件**: `app/agent_runtime/react_loop.py` (修改)

当 Agent 决定 respond 时，不再从 JSON response 字段获取完整回复，而是：
1. 从 Thought 中提取 reasoning 作为回复的 prompt 指导
2. 触发一次独立的流式生成调用
3. 通过 on_step 回调逐 chunk 推送 token 事件

```python
if thought.action == LoopAction.RESPOND:
    # 如果 thought.response 已有内容（非流式 fallback），直接使用
    if thought.response:
        yield_final_reply(thought.response)
    else:
        # 流式生成最终回复
        async for chunk in provider.generate_stream(...):
            on_step({"type": "token", "content": chunk})
```

**文件**: `app/api/v2/agent_loop_handler.py` (修改)

`agent_loop_event_stream` 改为支持流式 token 事件列表：
```python
# token 事件：多次增量推送
for token_event in sse_events:
    if token_event["type"] == "token":
        data = json.dumps({"content": token_event["content"]}, ensure_ascii=False)
        yield f"event: token\ndata: {data}\n\n"
```

---

### 3. 知识库扩充 (Req 3)

纯内容工作，新增 Markdown 文件到 `docs/knowledge/`：

| 类别 | 目录 | 新增数量 | 示例 |
|------|------|---------|------|
| 认知偏误 | `cognitive_biases/` | +20 | anchoring, framing, availability, dunning_kruger... |
| 决策框架 | `decision_frameworks/` | +10 | ooda_loop, cynefin, ikigai, design_your_life... |
| 情绪管理 | `emotion_management/` (新) | +5 | cbt_reframe, act_acceptance, emotional_labeling... |
| 沟通模型 | `communication_models/` (新) | +5 | nvc, crucial_conversations, disc_model... |

---

### 4. 认知成长可视化 (Req 4)

**文件**: `app/services/growth.py` (新增)

```python
def compute_radar_scores(db, identity_id) -> dict[str, float]:
    """计算 6 维度认知雷达图分数（0-1）"""
    # 从所有 session 的 coverage 数据聚合
    ...

def compute_insight_trend(db, identity_id, limit=10) -> list[dict]:
    """计算最近 N 个 session 的洞察数量趋势"""
    ...

def detect_breakthroughs(db, identity_id) -> list[dict]:
    """检测模式突破事件"""
    ...
```

**API 端点**: 挂载到 `app/api/v2/growth.py`

---

### 5. 账号体系 (Req 5)

**文件**: `app/api/v2/auth.py` (新增)

```python
@router.post("/register")
async def register(payload: RegisterRequest, db=Depends(get_db_session)):
    # 1. 创建 User
    # 2. 如果有 anonymous_token，执行 identity_migration
    # 3. 返回 JWT

@router.post("/login")
async def login(payload: LoginRequest, db=Depends(get_db_session)):
    # 验证密码，返回 JWT
```

**文件**: `app/services/identity_migration.py` (新增)

```python
async def migrate_anonymous_to_user(db, anonymous_identity_id, user_id):
    """将匿名用户的所有数据迁移到注册用户"""
    # 更新 sessions.user_id
    # 更新 user_memories.identity_id → 关联到 user
    # 保留 anonymous_identity 记录（不删除，防止 token 失效）
```

---

### 6. Metrics (Req 6)

**文件**: `app/api/internal/metrics.py` (新增)

```python
@router.get("/metrics")
async def get_metrics(db=Depends(get_db_session)):
    return {
        "dau": compute_dau(db),
        "active_sessions_24h": count_active_sessions(db, hours=24),
        "avg_turns_per_session": compute_avg_turns(db),
        "self_correction_rate": get_correction_metrics().trigger_rate,
        "llm_error_rate_1h": compute_llm_error_rate(db, hours=1),
        "retention_d1": compute_retention(db, days=1),
        "retention_d7": compute_retention(db, days=7),
    }
```

---

### 7. 前端测试 (Req 7)

**测试文件结构**:
```
apps/web/src/__tests__/
├── use-analysis-stream.test.ts  (SSE 状态机)
├── fetcher.test.ts              (API 客户端)
├── token-store.test.ts          (Token 管理)
└── chat-message.test.tsx        (Chat 组件)
```

**MSW 配置**: `apps/web/src/__tests__/mocks/handlers.ts`

---

## Error Handling

| 场景 | 处理方式 |
|------|----------|
| Rate limit exceeded | HTTP 429 + retry_after header + 友好中文提示 |
| Streaming 连接中断 | 收集已有 chunks 作为部分回复，补充 done 事件 |
| Streaming API 不可用 | 降级为非流式生成（单次 token 事件） |
| Identity migration 失败 | 回滚事务，返回错误，用户可重试 |
| Metrics 计算超时 | 返回缓存的上一次结果 + stale 标记 |

---

## Testing Strategy

- Rate Limiting: pytest + httpx TestClient 验证 429 响应
- Streaming: pytest-asyncio mock DashScope SSE 响应
- Growth APIs: pytest 单元测试 + fixture 数据
- Auth: pytest 集成测试（注册→登录→迁移流程）
- Frontend: vitest + MSW + testing-library
