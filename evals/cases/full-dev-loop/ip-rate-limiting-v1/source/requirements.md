# Production Readiness — 需求文档

## 介绍

MirrorMind 功能开发已完成，但在正式上线前需要解决产品风险和技术短板的交叉问题。本 spec 覆盖 7 个子方案，按优先级分为 P0（防灾）、P1（留存）、P2（商业化）、P3（质量）四个层级，确保系统在真实用户场景下稳定、流畅、可持续运营。

## 术语表

- **Rate Limiting**: API 请求频率限制，防止单个客户端过度消耗资源
- **Token Bucket**: 令牌桶算法，允许突发流量同时维持长期平均速率
- **LLM Streaming**: 大语言模型流式输出，逐 token 返回生成结果而非等待完整响应
- **TTFT (Time To First Token)**: 首 token 延迟，用户发送消息到看到第一个回复字符的时间
- **Incremental Output**: DashScope API 的增量输出模式，每次只返回新生成的内容
- **Knowledge Entry**: 知识库条目，包含认知偏误或决策框架的结构化 Markdown 文件
- **Cognitive Radar**: 认知维度雷达图，展示用户在 6 个维度的成长曲线
- **Identity Migration**: 将匿名用户的数据迁移到注册账号的过程
- **MSW (Mock Service Worker)**: 前端 API mock 工具，用于测试时拦截网络请求

---

## P0：防灾级

### Requirement 1: IP 级 Rate Limiting

**User Story:** 作为系统运维者，我需要限制单个 IP 的 API 调用频率，以便防止恶意脚本批量调用 LLM API 导致成本失控。

#### Acceptance Criteria

1. WHEN a client IP sends more than 10 POST requests to `/v2/conversation/{id}/message` within 1 hour, THEN the system SHALL return HTTP 429 with a JSON body containing `{"detail": "请求过于频繁，请稍后再试", "retry_after": <seconds>}`
2. WHEN a client IP sends more than 30 requests to any API endpoint within 1 minute, THEN the system SHALL return HTTP 429
3. THE rate limit thresholds SHALL be configurable via environment variables `RATE_LIMIT_CONVERSATION_PER_HOUR` and `RATE_LIMIT_GLOBAL_PER_MINUTE`
4. THE rate limiter SHALL use in-memory storage (no Redis dependency) for MVP, with the option to switch to Redis later
5. THE rate limiter SHALL NOT affect the `/healthz` endpoint or internal metrics endpoints
6. THE rate limiter SHALL include `X-RateLimit-Limit`, `X-RateLimit-Remaining`, and `X-RateLimit-Reset` headers in all responses

---

### Requirement 2: 真流式生成（LLM Streaming）

**User Story:** 作为用户，我希望在发送消息后 500ms 内看到 AI 开始回复（打字机效果），以便感受到系统在即时响应而非长时间等待。

#### Acceptance Criteria

1. WHEN the Agent decides to respond (action=respond), THE system SHALL use DashScope streaming API (`X-DashScope-SSE: enable`, `incremental_output: true`) to generate the final reply
2. THE SSE stream SHALL emit multiple `token` events, each containing an incremental text chunk (10-50 characters per chunk)
3. THE Time To First Token (TTFT) SHALL be less than 500ms measured from the moment the Agent decides to respond
4. THE ReAct Loop's Thought phase SHALL continue to use non-streaming JSON generation (complete response required for parsing)
5. IF the streaming API fails or times out, THEN the system SHALL fall back to non-streaming generation and emit a single `token` event with the complete content
6. THE frontend SSE client SHALL progressively render each `token` event chunk, appending to the displayed message in real-time
7. THE total event sequence SHALL remain: thinking → tool_call → tool_result → generating → token(s) → coach_done → ... → done

---

## P1：留存级

### Requirement 3: 知识库扩充

**User Story:** 作为 Agent，我需要更丰富的认知科学知识库，以便在更多场景下为用户提供有价值的思考框架，避免用户感觉"对话几次后没有新东西"。

#### Acceptance Criteria

1. THE knowledge base SHALL contain at least 30 cognitive bias entries (currently 10)
2. THE knowledge base SHALL contain at least 15 decision framework entries (currently 5)
3. THE knowledge base SHALL contain at least 5 emotion management entries (new category)
4. THE knowledge base SHALL contain at least 5 communication model entries (new category)
5. EACH knowledge entry SHALL follow the existing Markdown frontmatter format with fields: name, name_en, category, triggers
6. EACH knowledge entry SHALL contain sections: 简述, 适用场景, 引导问题
7. THE knowledge_search tool SHALL be able to retrieve entries from all categories without code changes

---

### Requirement 4: 认知成长可视化

**User Story:** 作为用户，我希望看到自己跨会话的认知成长数据（维度雷达图、洞察趋势、模式突破），以便直观感受到"这个工具在帮我进步"。

#### Acceptance Criteria

1. THE system SHALL provide `GET /v2/growth/radar` API returning the user's cognitive dimension scores (event, people, constraint, emotion, desire, attempted) based on historical coverage data
2. THE system SHALL provide `GET /v2/growth/insight-trend` API returning insight count per session over time (last 10 sessions)
3. THE system SHALL provide `GET /v2/growth/breakthroughs` API returning instances where the user broke a previously detected pattern
4. THE radar scores SHALL be calculated from the user's session coverage history (average coverage per dimension across all sessions)
5. THE breakthrough detection SHALL compare current session patterns against previously detected patterns from `pattern_detect` tool results
6. THE frontend SHALL display a "我的成长" page accessible from the navigation, containing: radar chart, insight trend line chart, and breakthrough highlights

---

## P2：商业化基础

### Requirement 5: 账号体系升级与数据迁移

**User Story:** 作为用户，我希望在试用几次后注册账号保存我的认知档案，以便换设备后不丢失历史洞察和记忆。

#### Acceptance Criteria

1. THE system SHALL allow anonymous users to have up to 3 conversations without registration
2. WHEN an anonymous user completes their 3rd conversation, THE system SHALL return a `suggest_register` SSE event with a prompt to register
3. THE system SHALL provide `POST /v2/auth/register` accepting email + password, creating a User record and linking the anonymous_identity
4. WHEN a user registers, THE system SHALL migrate all data (sessions, memories, insights, patterns) from the anonymous_identity to the new user account
5. THE system SHALL implement identity-level rate limiting: anonymous users 5 conversations/day, registered users 20 conversations/day
6. THE system SHALL support `POST /v2/auth/login` returning a JWT token for authenticated access
7. WHEN a registered user provides a JWT token, THE system SHALL use the user_id for all operations instead of anonymous_identity_id

---

### Requirement 6: 轻量运营 Metrics

**User Story:** 作为运维者，我需要实时了解系统的关键运营指标，以便在问题发生时快速发现和响应。

#### Acceptance Criteria

1. THE system SHALL provide `GET /internal/metrics` returning JSON with: dau, active_sessions_24h, avg_turns_per_session, self_correction_rate, llm_error_rate_1h, retention_d1, retention_d7
2. THE `/internal/metrics` endpoint SHALL NOT require authentication (internal network only)
3. THE system SHALL support alert webhook configuration via the `ALERT_WEBHOOK_URL` environment variable (Feishu/DingTalk webhook URL format)
4. WHEN llm_error_rate_1h exceeds 5%, THE system SHALL send an alert to the configured webhook
5. WHEN dau drops more than 50% compared to the previous day, THE system SHALL send an alert
6. THE metrics calculation SHALL use existing data from conversation_events and conversation_turns tables (no new tables required)

---

## P3：质量保障

### Requirement 7: 前端关键路径测试

**User Story:** 作为前端开发者，我需要关键路径的自动化测试覆盖，以便在修改代码时快速发现回归问题。

#### Acceptance Criteria

1. THE test suite SHALL include SSE client state machine tests verifying transitions: idle → connecting → open → (receiving events) → closed
2. THE test suite SHALL include Chat message rendering tests verifying: normal message display, thinking process collapse/expand, error state display
3. THE test suite SHALL include anonymous token management tests verifying: token creation, localStorage persistence, token expiry handling
4. THE tests SHALL use MSW (Mock Service Worker) to mock API responses without requiring a running backend
5. THE test suite SHALL achieve at least 80% line coverage on the following files: `use-analysis-stream.ts`, `fetcher.ts`, `token-store.ts`
6. ALL new tests SHALL pass in CI with `npm run test` (vitest)
