from __future__ import annotations

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field, field_validator

_ID_CHARS = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_:")


def _validate_identifier(value: str) -> str:
    value = value.strip()
    if not 1 <= len(value) <= 80 or any(ch not in _ID_CHARS for ch in value):
        raise ValueError("identifier must be 1-80 characters using letters, digits, dash, underscore or colon")
    return value


class SessionCreate(BaseModel):
    session_id: str
    starts_at: datetime
    capacity: int = Field(ge=1, le=500)

    @field_validator("session_id")
    @classmethod
    def validate_session_id(cls, value: str) -> str:
        return _validate_identifier(value)


class ReservationCreate(BaseModel):
    member_id: str

    @field_validator("member_id")
    @classmethod
    def validate_member_id(cls, value: str) -> str:
        return _validate_identifier(value)


class SessionResult(BaseModel):
    session_id: str
    tenant_id: str
    status: Literal["OPEN", "CLOSED", "CANCELED"]
    capacity: int
    reserved: int
    available: int
    waitlisted: int
    starts_at: str


class ReservationResult(BaseModel):
    outcome: Literal["RESERVED", "WAITLISTED", "CANCELED"]
    session_id: str
    member_id: str
    reservation_id: str | None = None
    waitlist_id: str | None = None
    queue_position: int | None = None
    promoted_member_id: str | None = None
    promoted_reservation_id: str | None = None
    message: str
