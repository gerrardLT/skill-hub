from __future__ import annotations

import hashlib
import json
import uuid
from copy import deepcopy
from dataclasses import dataclass
from typing import Any, Callable

from sqlalchemy import func, select, update
from sqlalchemy.orm import Session

from .models import OutboxEvent, Project, ProjectEvent, ProjectSnapshot, utcnow


class RevisionConflict(RuntimeError):
    pass


class AuditIntegrityError(RuntimeError):
    pass


def canonical_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def digest_json(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def event_digest(payload: dict[str, Any]) -> str:
    return digest_json(payload)


@dataclass(frozen=True)
class ProjectRecord:
    id: str
    name: str
    revision: int
    current_os: str
    current_stage: str
    profile: str
    criticality: str
    state: dict[str, Any]


class ProjectRepository:
    def create_project(
        self,
        session: Session,
        *,
        name: str,
        project_type: str = "greenfield",
        criticality: str = "medium",
        profile: str = "standard",
        actor: str,
        project_id: str | None = None,
        state: dict[str, Any] | None = None,
    ) -> ProjectRecord:
        project_id = project_id or f"project-{uuid.uuid4().hex}"
        if session.get(Project, project_id) is not None:
            raise ValueError(f"Project already exists: {project_id}")
        initial = deepcopy(state or {})
        initial.setdefault("version", "2.0.0")
        initial.setdefault("project", {})
        initial["project"].update({
            "id": project_id,
            "name": name,
            "type": project_type,
            "criticality": criticality,
            "profile": profile,
        })
        initial.setdefault("current_os", "pm")
        initial.setdefault("current_stage", "INTAKE")
        initial["revision"] = 0
        row = Project(
            id=project_id,
            name=name,
            project_type=project_type,
            criticality=criticality,
            profile=profile,
            current_os=str(initial["current_os"]),
            current_stage=str(initial["current_stage"]),
            revision=0,
            state_json=initial,
        )
        session.add(row)
        session.flush()
        self._append_event(session, row, "project-created", actor, {"name": name})
        self._snapshot(session, row)
        session.flush()
        return self._record(row)

    def get_project(self, session: Session, project_id: str, *, for_update: bool = False) -> Project:
        statement = select(Project).where(Project.id == project_id)
        if for_update:
            statement = statement.with_for_update()
        row = session.scalar(statement)
        if row is None:
            raise KeyError(f"Project not found: {project_id}")
        return row

    def list_projects(self, session: Session) -> list[ProjectRecord]:
        rows = session.scalars(select(Project).order_by(Project.updated_at.desc())).all()
        return [self._record(row) for row in rows]

    def update_state(
        self,
        session: Session,
        *,
        project_id: str,
        expected_revision: int,
        actor: str,
        event_type: str,
        mutate: Callable[[dict[str, Any]], dict[str, Any] | None],
        event_payload: dict[str, Any] | None = None,
    ) -> ProjectRecord:
        row = self.get_project(session, project_id, for_update=True)
        if row.revision != expected_revision:
            raise RevisionConflict(
                f"Revision conflict for {project_id}: expected {expected_revision}, actual {row.revision}"
            )
        state = deepcopy(row.state_json)
        result = mutate(state)
        if result is not None:
            state = result
        if not isinstance(state, dict):
            raise ValueError("Project state must remain a JSON object")
        next_revision = expected_revision + 1
        state["revision"] = next_revision
        next_os = str(state.get("current_os", row.current_os))
        next_stage = str(state.get("current_stage", row.current_stage))
        updated_at = utcnow()
        state.setdefault("project", {})["updated_at"] = updated_at.isoformat()

        # Do not rely on SELECT ... FOR UPDATE alone: SQLite ignores it. The
        # revision predicate is the actual compare-and-swap guard on every DB.
        result = session.execute(
            update(Project)
            .where(Project.id == project_id, Project.revision == expected_revision)
            .values(
                revision=next_revision,
                current_os=next_os,
                current_stage=next_stage,
                state_json=state,
                updated_at=updated_at,
            )
            .execution_options(synchronize_session=False)
        )
        if result.rowcount != 1:
            session.expire_all()
            actual = session.scalar(select(Project.revision).where(Project.id == project_id))
            raise RevisionConflict(
                f"Revision conflict for {project_id}: expected {expected_revision}, actual {actual}"
            )

        # Keep the identity-mapped row coherent so event hashes and snapshots
        # are generated from the state that actually won the CAS.
        row.revision = next_revision
        row.current_os = next_os
        row.current_stage = next_stage
        row.state_json = state
        row.updated_at = updated_at
        self._append_event(session, row, event_type, actor, event_payload or {})
        self._snapshot(session, row)
        session.add(OutboxEvent(
            id=f"outbox-{uuid.uuid4().hex}",
            topic="project.state.changed",
            aggregate_id=row.id,
            payload_json={"project_id": row.id, "revision": row.revision, "event_type": event_type},
        ))
        session.flush()
        return self._record(row)

    def restore_revision(
        self,
        session: Session,
        *,
        project_id: str,
        source_revision: int,
        expected_revision: int,
        actor: str,
        reason: str,
    ) -> ProjectRecord:
        snapshot = session.scalar(select(ProjectSnapshot).where(
            ProjectSnapshot.project_id == project_id,
            ProjectSnapshot.revision == source_revision,
        ))
        if snapshot is None:
            raise KeyError(f"Snapshot not found: {project_id}/{source_revision}")
        restored = deepcopy(snapshot.state_json)
        restored.setdefault("recovery", []).append({
            "source_revision": source_revision,
            "reason": reason,
            "restored_by": actor,
            "restored_at": utcnow().isoformat(),
        })
        return self.update_state(
            session,
            project_id=project_id,
            expected_revision=expected_revision,
            actor=actor,
            event_type="project-restored",
            mutate=lambda _state: restored,
            event_payload={"source_revision": source_revision, "reason": reason},
        )

    def verify_audit_chain(self, session: Session, project_id: str) -> dict[str, Any]:
        row = self.get_project(session, project_id)
        events = session.scalars(
            select(ProjectEvent).where(ProjectEvent.project_id == project_id).order_by(ProjectEvent.sequence)
        ).all()
        errors: list[str] = []
        previous_hash = "GENESIS"
        for expected, event in enumerate(events, 1):
            if event.sequence != expected:
                errors.append(f"sequence:{expected}!={event.sequence}")
            if event.previous_hash != previous_hash:
                errors.append(f"previous-hash:{event.sequence}")
            payload = {
                "project_id": event.project_id,
                "sequence": event.sequence,
                "event_type": event.event_type,
                "actor": event.actor,
                "payload": event.payload_json,
                "state_hash": event.state_hash,
                "previous_hash": event.previous_hash,
            }
            calculated = event_digest(payload)
            if calculated != event.event_hash:
                errors.append(f"event-hash:{event.sequence}")
            previous_hash = event.event_hash
        if events and events[-1].state_hash != digest_json(row.state_json):
            errors.append("latest-state-hash")
        return {"valid": not errors, "events": len(events), "errors": errors}

    def _append_event(
        self,
        session: Session,
        row: Project,
        event_type: str,
        actor: str,
        payload: dict[str, Any],
    ) -> ProjectEvent:
        last = session.scalar(
            select(ProjectEvent).where(ProjectEvent.project_id == row.id).order_by(ProjectEvent.sequence.desc()).limit(1)
        )
        sequence = 1 if last is None else last.sequence + 1
        previous_hash = "GENESIS" if last is None else last.event_hash
        created_at = utcnow()
        state_hash = digest_json(row.state_json)
        event_payload = {
            "project_id": row.id,
            "sequence": sequence,
            "event_type": event_type,
            "actor": actor,
            "payload": payload,
            "state_hash": state_hash,
            "previous_hash": previous_hash,
        }
        event = ProjectEvent(
            project_id=row.id,
            sequence=sequence,
            event_type=event_type,
            actor=actor,
            payload_json=payload,
            state_hash=state_hash,
            previous_hash=previous_hash,
            event_hash=event_digest(event_payload),
            created_at=created_at,
        )
        session.add(event)
        return event

    def _snapshot(self, session: Session, row: Project) -> None:
        session.add(ProjectSnapshot(
            project_id=row.id,
            revision=row.revision,
            state_json=deepcopy(row.state_json),
            state_hash=digest_json(row.state_json),
        ))

    @staticmethod
    def _record(row: Project) -> ProjectRecord:
        return ProjectRecord(
            id=row.id,
            name=row.name,
            revision=row.revision,
            current_os=row.current_os,
            current_stage=row.current_stage,
            profile=row.profile,
            criticality=row.criticality,
            state=deepcopy(row.state_json),
        )
