from __future__ import annotations

import uuid
from dataclasses import asdict, dataclass
from typing import Any

from sqlalchemy import select
from sqlalchemy.orm import Session

from .models import Budget, Run


@dataclass(frozen=True)
class BudgetDecision:
    allowed: bool
    level: str
    remaining_usd: float | None
    remaining_tokens: int | None
    actions: list[str]
    reason: str


class BudgetService:
    def upsert(
        self,
        session: Session,
        *,
        project_id: str,
        scope: str = "project",
        soft_limit_usd: float | None = None,
        hard_limit_usd: float | None = None,
        token_limit: int | None = None,
        tool_call_limit: int | None = None,
        human_hour_limit: float | None = None,
        policy: dict[str, Any] | None = None,
    ) -> Budget:
        row = session.scalar(select(Budget).where(Budget.project_id == project_id, Budget.scope == scope).with_for_update())
        if row is None:
            row = Budget(id=f"budget-{uuid.uuid4().hex}", project_id=project_id, scope=scope)
            session.add(row)
        for name, value in {
            "soft_limit_usd": soft_limit_usd,
            "hard_limit_usd": hard_limit_usd,
            "token_limit": token_limit,
            "tool_call_limit": tool_call_limit,
            "human_hour_limit": human_hour_limit,
        }.items():
            if value is not None and float(value) < 0:
                raise ValueError(f"{name} cannot be negative")
            setattr(row, name, value)
        row.policy_json = policy or row.policy_json or {}
        if row.soft_limit_usd is not None and row.hard_limit_usd is not None and row.soft_limit_usd > row.hard_limit_usd:
            raise ValueError("soft_limit_usd cannot exceed hard_limit_usd")
        session.flush()
        return row

    def assess(
        self,
        session: Session,
        *,
        project_id: str,
        estimated_cost_usd: float = 0.0,
        estimated_tokens: int = 0,
        estimated_tool_calls: int = 0,
        estimated_human_hours: float = 0.0,
        scope: str = "project",
    ) -> BudgetDecision:
        row = session.scalar(select(Budget).where(Budget.project_id == project_id, Budget.scope == scope))
        if row is None:
            return BudgetDecision(True, "unbounded", None, None, [], "No budget policy configured")
        projected_cost = row.spent_usd + estimated_cost_usd
        projected_tokens = row.tokens_used + estimated_tokens
        projected_tools = row.tool_calls_used + estimated_tool_calls
        projected_hours = row.human_hours_used + estimated_human_hours
        hard_reasons: list[str] = []
        if row.hard_limit_usd is not None and projected_cost > row.hard_limit_usd:
            hard_reasons.append("hard USD limit exceeded")
        if row.token_limit is not None and projected_tokens > row.token_limit:
            hard_reasons.append("token limit exceeded")
        if row.tool_call_limit is not None and projected_tools > row.tool_call_limit:
            hard_reasons.append("tool-call limit exceeded")
        if row.human_hour_limit is not None and projected_hours > row.human_hour_limit:
            hard_reasons.append("human-hour limit exceeded")
        remaining_usd = None if row.hard_limit_usd is None else round(row.hard_limit_usd - projected_cost, 6)
        remaining_tokens = None if row.token_limit is None else row.token_limit - projected_tokens
        if hard_reasons:
            return BudgetDecision(False, "blocked", remaining_usd, remaining_tokens, [
                "stop optional subagents",
                "require budget owner approval",
                "use cached evidence only",
            ], "; ".join(hard_reasons))
        soft = row.soft_limit_usd is not None and projected_cost >= row.soft_limit_usd
        ratio = 0.0
        if row.hard_limit_usd and row.hard_limit_usd > 0:
            ratio = projected_cost / row.hard_limit_usd
        if soft or ratio >= 0.80:
            return BudgetDecision(True, "degraded", remaining_usd, remaining_tokens, [
                "route routine tasks to economy model tier",
                "disable speculative parallelism",
                "reuse existing evidence before new research",
                "require explicit approval for optional tools",
            ], "Soft budget threshold reached")
        if ratio >= 0.60:
            return BudgetDecision(True, "watch", remaining_usd, remaining_tokens, [
                "prefer bounded tool calls",
                "record forecast before multi-agent fan-out",
            ], "Budget utilization above watch threshold")
        return BudgetDecision(True, "normal", remaining_usd, remaining_tokens, [], "Within budget")

    def record_run(
        self,
        session: Session,
        *,
        project_id: str,
        actor: str,
        os_name: str,
        skill: str,
        model: str,
        outcome: str,
        tokens_input: int = 0,
        tokens_output: int = 0,
        tool_calls: int = 0,
        cost_usd: float = 0.0,
        human_hours: float = 0.0,
        duration_ms: int = 0,
        job_id: str | None = None,
        metadata: dict[str, Any] | None = None,
        scope: str = "project",
    ) -> tuple[Run, BudgetDecision]:
        decision = self.assess(
            session,
            project_id=project_id,
            estimated_cost_usd=cost_usd,
            estimated_tokens=tokens_input + tokens_output,
            estimated_tool_calls=tool_calls,
            estimated_human_hours=human_hours,
            scope=scope,
        )
        if not decision.allowed:
            raise RuntimeError(decision.reason)
        run = Run(
            id=f"run-{uuid.uuid4().hex}",
            project_id=project_id,
            actor=actor,
            os_name=os_name,
            skill=skill,
            model=model,
            outcome=outcome,
            tokens_input=tokens_input,
            tokens_output=tokens_output,
            tool_calls=tool_calls,
            cost_usd=cost_usd,
            human_hours=human_hours,
            duration_ms=duration_ms,
            job_id=job_id,
            metadata_json=metadata or {},
        )
        session.add(run)
        budget = session.scalar(select(Budget).where(Budget.project_id == project_id, Budget.scope == scope).with_for_update())
        if budget is not None:
            budget.spent_usd += cost_usd
            budget.tokens_used += tokens_input + tokens_output
            budget.tool_calls_used += tool_calls
            budget.human_hours_used += human_hours
        session.flush()
        return run, decision

    @staticmethod
    def decision_payload(decision: BudgetDecision) -> dict[str, Any]:
        return asdict(decision)
