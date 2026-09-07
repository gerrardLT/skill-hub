from __future__ import annotations

import os
from pathlib import Path

from fastapi import FastAPI, Header, Request
from fastapi.responses import JSONResponse

from .errors import DomainError
from .models import ReservationCreate, ReservationResult, SessionCreate, SessionResult
from .service import ReservationService

DEFAULT_DATABASE = Path(os.getenv("VENUE_DATABASE", "./venue-pilot.db"))


def create_app(database: str | Path | None = None) -> FastAPI:
    service = ReservationService(database or DEFAULT_DATABASE)
    app = FastAPI(title="Venue Reservation Pilot", version="0.1.0")

    @app.exception_handler(DomainError)
    async def handle_domain_error(_: Request, exc: DomainError) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error": {
                    "code": exc.code,
                    "message": exc.message,
                    "next_action": exc.next_action,
                }
            },
        )

    @app.get("/health")
    def health() -> dict[str, str]:
        return {"status": "ok"}

    @app.post("/v1/sessions", response_model=SessionResult, status_code=201)
    def create_session(payload: SessionCreate, x_tenant_id: str = Header(...)) -> dict:
        return service.create_session(
            x_tenant_id,
            payload.session_id,
            payload.starts_at.isoformat(),
            payload.capacity,
        )

    @app.get("/v1/sessions/{session_id}", response_model=SessionResult)
    def get_session(session_id: str, x_tenant_id: str = Header(...)) -> dict:
        return service.get_session(x_tenant_id, session_id)

    @app.post("/v1/sessions/{session_id}/reservations", response_model=ReservationResult)
    def reserve(
        session_id: str,
        payload: ReservationCreate,
        x_tenant_id: str = Header(...),
        idempotency_key: str = Header(...),
    ) -> JSONResponse:
        status, body = service.reserve(x_tenant_id, session_id, payload.member_id, idempotency_key)
        return JSONResponse(status_code=status, content=body)

    @app.delete("/v1/reservations/{reservation_id}", response_model=ReservationResult)
    def cancel(
        reservation_id: str,
        x_tenant_id: str = Header(...),
        idempotency_key: str = Header(...),
    ) -> JSONResponse:
        status, body = service.cancel(x_tenant_id, reservation_id, idempotency_key)
        return JSONResponse(status_code=status, content=body)

    @app.get("/v1/sessions/{session_id}/metrics")
    def metrics(session_id: str, x_tenant_id: str = Header(...)) -> dict:
        return service.session_metrics(x_tenant_id, session_id)

    app.state.reservation_service = service
    return app


app = create_app()
