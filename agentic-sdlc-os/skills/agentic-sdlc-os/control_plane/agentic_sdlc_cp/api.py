from __future__ import annotations

import os
from datetime import datetime
from typing import Any

from fastapi import Depends, FastAPI, Header, HTTPException, Request, status
from fastapi.responses import HTMLResponse
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel, Field
from sqlalchemy import select

from .approvals import ApprovalService
from .costs import BudgetService
from .db import Database, create_database, init_database
from .jobs import JobQueue
from .models import Approval, Budget, Job, Principal, Project, Secret, SkillVersion
from .recovery import RecoveryService
from .repository import ProjectRepository, RevisionConflict
from .security import Identity, authenticate, create_principal, has_permission, put_secret, require_permission


bearer = HTTPBearer(auto_error=False)


class ProjectCreate(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    project_type: str = "greenfield"
    criticality: str = "medium"
    profile: str = "standard"
    project_id: str | None = None
    state: dict[str, Any] | None = None


class StateUpdate(BaseModel):
    expected_revision: int = Field(ge=0)
    state: dict[str, Any]
    event_type: str = "state-replaced"
    reason: str = "API state update"


class ApprovalRequest(BaseModel):
    gate_name: str
    reason: str
    idempotency_key: str
    expires_at: datetime | None = None


class ApprovalDecision(BaseModel):
    decision: str
    reason: str


class JobCreate(BaseModel):
    project_id: str | None = None
    job_type: str
    payload: dict[str, Any] = Field(default_factory=dict)
    idempotency_key: str
    priority: int = 100
    max_attempts: int = 3


class JobLeaseRequest(BaseModel):
    worker_id: str
    lease_seconds: int = 60
    job_types: list[str] | None = None


class JobHeartbeat(BaseModel):
    worker_id: str
    fencing_token: int
    lease_seconds: int = 60


class JobComplete(BaseModel):
    worker_id: str
    fencing_token: int
    result: dict[str, Any] = Field(default_factory=dict)


class JobFail(BaseModel):
    worker_id: str
    fencing_token: int
    error: str


class BudgetUpsert(BaseModel):
    scope: str = "project"
    soft_limit_usd: float | None = None
    hard_limit_usd: float | None = None
    token_limit: int | None = None
    tool_call_limit: int | None = None
    human_hour_limit: float | None = None
    policy: dict[str, Any] = Field(default_factory=dict)


class BudgetAssess(BaseModel):
    scope: str = "project"
    estimated_cost_usd: float = 0.0
    estimated_tokens: int = 0
    estimated_tool_calls: int = 0
    estimated_human_hours: float = 0.0


class PrincipalCreate(BaseModel):
    display_name: str
    role: str


class SecretPut(BaseModel):
    name: str
    value: str
    key_version: str = "v1"


DASHBOARD_HTML = r"""
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Agentic SDLC OS Control Plane</title>
<style>
:root{font-family:Inter,ui-sans-serif,system-ui,sans-serif;color:#18181b;background:#f4f4f5}body{margin:0}.wrap{max-width:1280px;margin:auto;padding:24px}.bar{display:flex;gap:12px;align-items:center;flex-wrap:wrap}.card{background:#fff;border:1px solid #e4e4e7;border-radius:14px;padding:18px;box-shadow:0 1px 2px #0000000d}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:16px;margin-top:16px}input,button{font:inherit;padding:10px 12px;border-radius:9px;border:1px solid #d4d4d8}button{background:#18181b;color:#fff;cursor:pointer}small{color:#71717a}.pill{display:inline-block;padding:3px 8px;border-radius:99px;background:#f4f4f5;font-size:12px}.danger{color:#b91c1c}.ok{color:#166534}pre{white-space:pre-wrap;word-break:break-word;background:#fafafa;padding:10px;border-radius:8px}.metric{font-size:28px;font-weight:700}.muted{color:#71717a}table{width:100%;border-collapse:collapse}th,td{text-align:left;border-bottom:1px solid #eee;padding:8px}</style>
</head>
<body><div class="wrap">
<h1>Agentic SDLC OS</h1><div class="bar"><input id="token" type="password" placeholder="Bearer token" size="42"><button onclick="loadAll()">Load dashboard</button><span id="status" class="muted"></span></div>
<div class="grid"><div class="card"><div class="metric" id="projectCount">-</div><small>Projects</small></div><div class="card"><div class="metric" id="approvalCount">-</div><small>Pending approvals</small></div><div class="card"><div class="metric" id="jobCount">-</div><small>Open jobs</small></div></div>
<div class="grid"><div class="card"><h2>Projects</h2><div id="projects"></div></div><div class="card"><h2>Pending gate approvals</h2><div id="approvals"></div></div><div class="card"><h2>Jobs</h2><div id="jobs"></div></div></div>
</div><script>
const token=document.getElementById('token');token.value=localStorage.getItem('sdlcToken')||'';
async function api(path){localStorage.setItem('sdlcToken',token.value);const r=await fetch(path,{headers:{Authorization:'Bearer '+token.value}});if(!r.ok)throw new Error(await r.text());return r.json()}
function esc(s){return String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#039;'}[c]))}
async function loadAll(){const s=document.getElementById('status');s.textContent='Loading...';try{const [p,a,j]=await Promise.all([api('/api/projects'),api('/api/approvals?status=pending'),api('/api/jobs?open_only=true')]);projectCount.textContent=p.length;approvalCount.textContent=a.length;jobCount.textContent=j.length;projects.innerHTML=p.map(x=>`<p><b>${esc(x.name)}</b><br><span class="pill">${esc(x.profile)}</span> ${esc(x.current_os)}/${esc(x.current_stage)} rev ${x.revision}</p>`).join('')||'<p class="muted">None</p>';approvals.innerHTML=a.map(x=>`<p><b>${esc(x.gate_name)}</b><br>${esc(x.project_id)}<br><small>${esc(x.requested_by)}</small><br><button onclick="decide('${esc(x.id)}','approved')">Approve</button> <button onclick="decide('${esc(x.id)}','rejected')">Reject</button></p>`).join('')||'<p class="muted">None</p>';jobs.innerHTML=j.map(x=>`<p><b>${esc(x.job_type)}</b> <span class="pill">${esc(x.status)}</span><br><small>${esc(x.id)}</small></p>`).join('')||'<p class="muted">None</p>';s.textContent='Updated'}catch(e){s.textContent='Error: '+e.message}}
async function decide(id,decision){const reason=prompt('Decision reason');if(!reason)return;const r=await fetch('/api/approvals/'+id+'/decision',{method:'POST',headers:{Authorization:'Bearer '+token.value,'Content-Type':'application/json'},body:JSON.stringify({decision,reason})});if(!r.ok){alert(await r.text())}else{loadAll()}}
</script></body></html>
"""


def create_app(database: Database | None = None) -> FastAPI:
    db = database or create_database()
    init_database(db)
    repo = ProjectRepository()
    approvals = ApprovalService()
    jobs = JobQueue()
    budgets = BudgetService()
    app = FastAPI(title="Agentic SDLC OS Control Plane", version="2.0.0")
    app.state.database = db

    def current_identity(
        credentials: HTTPAuthorizationCredentials | None = Depends(bearer),
    ) -> Identity:
        token = credentials.credentials if credentials else ""
        bootstrap = os.environ.get("SDLC_BOOTSTRAP_TOKEN", "")
        if bootstrap and token == bootstrap:
            return Identity("bootstrap-admin", "Bootstrap Admin", "admin")
        with db.session() as session:
            identity = authenticate(session, token)
        if identity is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or missing bearer token")
        return identity

    def require(permission: str):
        def dependency(identity: Identity = Depends(current_identity)) -> Identity:
            if not has_permission(identity, permission):
                raise HTTPException(status_code=403, detail=f"Missing permission: {permission}")
            return identity
        return dependency

    @app.get("/health")
    def health() -> dict[str, Any]:
        return {"status": "ok", "version": "2.0.0", "database": db.engine.dialect.name}

    @app.get("/dashboard", response_class=HTMLResponse)
    def dashboard() -> str:
        return DASHBOARD_HTML

    @app.get("/api/projects")
    def list_projects(identity: Identity = Depends(require("project:read"))) -> list[dict[str, Any]]:
        with db.session() as session:
            return [record.__dict__ | {"state": None} for record in repo.list_projects(session)]

    @app.post("/api/projects", status_code=201)
    def create_project(body: ProjectCreate, identity: Identity = Depends(require("project:write"))) -> dict[str, Any]:
        with db.session() as session:
            record = repo.create_project(
                session,
                name=body.name,
                project_type=body.project_type,
                criticality=body.criticality,
                profile=body.profile,
                actor=identity.principal_id,
                project_id=body.project_id,
                state=body.state,
            )
            return record.__dict__

    @app.get("/api/projects/{project_id}")
    def get_project(project_id: str, identity: Identity = Depends(require("project:read"))) -> dict[str, Any]:
        with db.session() as session:
            try:
                row = repo.get_project(session, project_id)
            except KeyError as exc:
                raise HTTPException(status_code=404, detail=str(exc)) from exc
            return {
                "id": row.id, "name": row.name, "revision": row.revision,
                "profile": row.profile, "criticality": row.criticality,
                "current_os": row.current_os, "current_stage": row.current_stage,
                "state": row.state_json,
            }

    @app.put("/api/projects/{project_id}/state")
    def update_state(project_id: str, body: StateUpdate, identity: Identity = Depends(require("project:write"))) -> dict[str, Any]:
        try:
            with db.session() as session:
                record = repo.update_state(
                    session,
                    project_id=project_id,
                    expected_revision=body.expected_revision,
                    actor=identity.principal_id,
                    event_type=body.event_type,
                    mutate=lambda _current: body.state,
                    event_payload={"reason": body.reason},
                )
                return record.__dict__
        except RevisionConflict as exc:
            raise HTTPException(status_code=409, detail=str(exc)) from exc
        except KeyError as exc:
            raise HTTPException(status_code=404, detail=str(exc)) from exc

    @app.get("/api/projects/{project_id}/audit")
    def verify_audit(project_id: str, identity: Identity = Depends(require("audit:read"))) -> dict[str, Any]:
        with db.session() as session:
            try:
                return repo.verify_audit_chain(session, project_id)
            except KeyError as exc:
                raise HTTPException(status_code=404, detail=str(exc)) from exc

    @app.post("/api/projects/{project_id}/approvals", status_code=201)
    def request_approval(project_id: str, body: ApprovalRequest, identity: Identity = Depends(current_identity)) -> dict[str, Any]:
        try:
            with db.session() as session:
                row = approvals.request(
                    session,
                    project_id=project_id,
                    gate_name=body.gate_name,
                    reason=body.reason,
                    requester=identity,
                    idempotency_key=body.idempotency_key,
                    expires_at=body.expires_at,
                )
                return _approval_payload(row)
        except (PermissionError, KeyError, ValueError) as exc:
            raise HTTPException(status_code=403 if isinstance(exc, PermissionError) else 400, detail=str(exc)) from exc

    @app.post("/api/approvals/{approval_id}/decision")
    def decide_approval(approval_id: str, body: ApprovalDecision, identity: Identity = Depends(current_identity)) -> dict[str, Any]:
        try:
            with db.session() as session:
                row = approvals.decide(session, approval_id=approval_id, decision=body.decision, reason=body.reason, approver=identity)
                return _approval_payload(row)
        except KeyError as exc:
            raise HTTPException(status_code=404, detail=str(exc)) from exc
        except PermissionError as exc:
            raise HTTPException(status_code=403, detail=str(exc)) from exc
        except (RuntimeError, ValueError) as exc:
            raise HTTPException(status_code=409, detail=str(exc)) from exc

    @app.get("/api/approvals")
    def list_approvals(status: str | None = None, identity: Identity = Depends(require("project:read"))) -> list[dict[str, Any]]:  # type: ignore[assignment]
        with db.session() as session:
            statement = select(Approval).order_by(Approval.requested_at.desc())
            if status:
                statement = statement.where(Approval.status == status)
            return [_approval_payload(row) for row in session.scalars(statement).all()]

    @app.post("/api/jobs", status_code=201)
    def enqueue_job(body: JobCreate, identity: Identity = Depends(require("job:submit"))) -> dict[str, Any]:
        with db.session() as session:
            row = jobs.enqueue(session, **body.model_dump())
            return _job_payload(row)

    @app.post("/api/jobs/lease")
    def lease_job(body: JobLeaseRequest, identity: Identity = Depends(require("job:execute"))) -> dict[str, Any] | None:
        with db.session() as session:
            lease = jobs.lease_next(session, **body.model_dump())
            return None if lease is None else lease.__dict__

    @app.post("/api/jobs/{job_id}/heartbeat")
    def heartbeat_job(job_id: str, body: JobHeartbeat, identity: Identity = Depends(require("job:execute"))) -> dict[str, Any]:
        with db.session() as session:
            expires = jobs.heartbeat(session, job_id=job_id, **body.model_dump())
            return {"lease_expires_at": expires.isoformat()}

    @app.post("/api/jobs/{job_id}/complete")
    def complete_job(job_id: str, body: JobComplete, identity: Identity = Depends(require("job:execute"))) -> dict[str, Any]:
        with db.session() as session:
            row = jobs.complete(session, job_id=job_id, **body.model_dump())
            return _job_payload(row)

    @app.post("/api/jobs/{job_id}/fail")
    def fail_job(job_id: str, body: JobFail, identity: Identity = Depends(require("job:execute"))) -> dict[str, Any]:
        with db.session() as session:
            row = jobs.fail(session, job_id=job_id, **body.model_dump())
            return _job_payload(row)

    @app.get("/api/jobs")
    def list_jobs(open_only: bool = False, identity: Identity = Depends(require("project:read"))) -> list[dict[str, Any]]:  # type: ignore[assignment]
        with db.session() as session:
            statement = select(Job).order_by(Job.created_at.desc()).limit(200)
            if open_only:
                statement = statement.where(Job.status.in_(["queued", "retry", "leased"]))
            return [_job_payload(row) for row in session.scalars(statement).all()]

    @app.put("/api/projects/{project_id}/budget")
    def upsert_budget(project_id: str, body: BudgetUpsert, identity: Identity = Depends(require("budget:manage"))) -> dict[str, Any]:
        with db.session() as session:
            row = budgets.upsert(session, project_id=project_id, **body.model_dump())
            return _budget_payload(row)

    @app.post("/api/projects/{project_id}/budget/assess")
    def assess_budget(project_id: str, body: BudgetAssess, identity: Identity = Depends(require("budget:read"))) -> dict[str, Any]:
        with db.session() as session:
            return budgets.decision_payload(budgets.assess(session, project_id=project_id, **body.model_dump()))

    @app.post("/api/principals", status_code=201)
    def add_principal(body: PrincipalCreate, identity: Identity = Depends(require("principal:manage"))) -> dict[str, Any]:
        with db.session() as session:
            row, token = create_principal(session, body.display_name, body.role)
            return {"id": row.id, "display_name": row.display_name, "role": row.role, "token": token}

    @app.post("/api/projects/{project_id}/secrets", status_code=201)
    def add_secret(project_id: str, body: SecretPut, identity: Identity = Depends(require("secret:write"))) -> dict[str, Any]:
        with db.session() as session:
            row = put_secret(session, project_id=project_id, name=body.name, value=body.value, actor=identity, key_version=body.key_version)
            return {"id": row.id, "name": row.name, "project_id": row.project_id, "key_version": row.key_version}

    @app.get("/api/skills")
    def list_skills(identity: Identity = Depends(require("skill:read"))) -> list[dict[str, Any]]:
        with db.session() as session:
            return [{
                "id": row.id, "repo": row.repo, "skill_name": row.skill_name,
                "commit_sha": row.commit_sha, "security_status": row.security_status,
                "lifecycle_status": row.lifecycle_status, "effectiveness_score": row.effectiveness_score,
            } for row in session.scalars(select(SkillVersion).order_by(SkillVersion.repo, SkillVersion.skill_name)).all()]

    @app.post("/api/recovery")
    def recover(identity: Identity = Depends(require("recovery:execute"))) -> dict[str, Any]:
        return RecoveryService(db).payload()

    return app


def _approval_payload(row: Approval) -> dict[str, Any]:
    return {
        "id": row.id, "project_id": row.project_id, "gate_name": row.gate_name,
        "status": row.status, "requested_by": row.requested_by,
        "artifact_revision": row.artifact_revision,
        "requested_at": row.requested_at.isoformat(),
        "decided_by": row.decided_by,
    }


def _job_payload(row: Job) -> dict[str, Any]:
    return {
        "id": row.id, "project_id": row.project_id, "job_type": row.job_type,
        "status": row.status, "attempt": row.attempt, "max_attempts": row.max_attempts,
        "lease_owner": row.lease_owner, "error": row.error,
    }


def _budget_payload(row: Budget) -> dict[str, Any]:
    return {
        "id": row.id, "project_id": row.project_id, "scope": row.scope,
        "soft_limit_usd": row.soft_limit_usd, "hard_limit_usd": row.hard_limit_usd,
        "token_limit": row.token_limit, "tool_call_limit": row.tool_call_limit,
        "human_hour_limit": row.human_hour_limit, "spent_usd": row.spent_usd,
        "tokens_used": row.tokens_used, "tool_calls_used": row.tool_calls_used,
        "human_hours_used": row.human_hours_used, "policy": row.policy_json,
    }


app = create_app()
