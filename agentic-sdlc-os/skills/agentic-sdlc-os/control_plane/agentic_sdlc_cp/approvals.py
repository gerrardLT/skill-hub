from __future__ import annotations

import uuid
from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.orm import Session

from .models import Approval, Project, utcnow
from .security import Identity, enforce_separation_of_duties, require_permission


def _aware(value: datetime | None) -> datetime | None:
    if value is None:
        return None
    return value if value.tzinfo is not None else value.replace(tzinfo=timezone.utc)


class ApprovalService:
    def request(
        self,
        session: Session,
        *,
        project_id: str,
        gate_name: str,
        reason: str,
        requester: Identity,
        idempotency_key: str,
        expires_at: datetime | None = None,
    ) -> Approval:
        require_permission(requester, "gate:request")
        project = session.get(Project, project_id)
        if project is None:
            raise KeyError(f"Project not found: {project_id}")
        existing = session.scalar(select(Approval).where(
            Approval.project_id == project_id,
            Approval.idempotency_key == idempotency_key,
        ))
        if existing is not None:
            return existing
        row = Approval(
            id=f"approval-{uuid.uuid4().hex}",
            project_id=project_id,
            gate_name=gate_name,
            requested_by=requester.principal_id,
            request_reason=reason,
            artifact_revision=project.revision,
            idempotency_key=idempotency_key,
            expires_at=expires_at,
        )
        session.add(row)
        session.flush()
        return row

    def decide(
        self,
        session: Session,
        *,
        approval_id: str,
        decision: str,
        reason: str,
        approver: Identity,
    ) -> Approval:
        require_permission(approver, "gate:approve")
        if decision not in {"approved", "rejected"}:
            raise ValueError("decision must be approved or rejected")
        row = session.scalar(select(Approval).where(Approval.id == approval_id).with_for_update())
        if row is None:
            raise KeyError(f"Approval not found: {approval_id}")
        if row.status != "pending":
            raise RuntimeError(f"Approval already decided: {row.status}")
        project = session.get(Project, row.project_id)
        if project is None:
            raise KeyError(f"Project not found: {row.project_id}")
        if _aware(row.expires_at) is not None and _aware(row.expires_at) <= utcnow():
            row.status = "expired"
            raise RuntimeError("Approval request has expired")
        if project.revision != row.artifact_revision:
            row.status = "stale"
            raise RuntimeError("Approval is stale because the project revision changed")
        enforce_separation_of_duties(
            requester_id=row.requested_by,
            approver=approver,
            profile=project.profile,
        )
        row.status = decision
        row.decided_by = approver.principal_id
        row.decision_reason = reason
        row.decided_at = utcnow()
        session.flush()
        return row

    def list_pending(self, session: Session, project_id: str | None = None) -> list[Approval]:
        statement = select(Approval).where(Approval.status == "pending").order_by(Approval.requested_at)
        if project_id:
            statement = statement.where(Approval.project_id == project_id)
        return list(session.scalars(statement).all())
