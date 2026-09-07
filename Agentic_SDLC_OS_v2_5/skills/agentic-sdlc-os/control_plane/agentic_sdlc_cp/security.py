from __future__ import annotations

import base64
import hashlib
import os
import secrets as pysecrets
import uuid
from dataclasses import dataclass
from typing import Iterable

from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from sqlalchemy import select
from sqlalchemy.orm import Session

from .models import Principal, Secret, utcnow


ROLE_PERMISSIONS: dict[str, set[str]] = {
    "viewer": {"project:read", "audit:read", "budget:read", "skill:read"},
    "contributor": {"project:read", "project:write", "job:submit", "evidence:write", "budget:read", "skill:read"},
    "reviewer": {"project:read", "gate:request", "gate:approve", "audit:read", "budget:read", "skill:read"},
    "releaser": {"project:read", "gate:request", "gate:approve", "job:submit", "release:execute", "audit:read", "budget:read"},
    "service": {"project:read", "project:write", "job:submit", "job:execute", "evidence:write", "secret:use", "budget:consume", "skill:read"},
    "admin": {"*"},
}


@dataclass(frozen=True)
class Identity:
    principal_id: str
    display_name: str
    role: str


def token_hash(token: str) -> str:
    return hashlib.sha256(token.encode("utf-8")).hexdigest()


def create_principal(session: Session, display_name: str, role: str) -> tuple[Principal, str]:
    if role not in ROLE_PERMISSIONS:
        raise ValueError(f"Unknown role: {role}")
    token = pysecrets.token_urlsafe(32)
    principal = Principal(
        id=f"principal-{uuid.uuid4().hex}",
        display_name=display_name,
        role=role,
        token_hash=token_hash(token),
    )
    session.add(principal)
    session.flush()
    return principal, token


def authenticate(session: Session, token: str) -> Identity | None:
    if not token:
        return None
    principal = session.scalar(select(Principal).where(Principal.token_hash == token_hash(token), Principal.disabled.is_(False)))
    if principal is None:
        return None
    principal.last_used_at = utcnow()
    session.flush()
    return Identity(principal.id, principal.display_name, principal.role)


def has_permission(identity: Identity, permission: str) -> bool:
    permissions = ROLE_PERMISSIONS.get(identity.role, set())
    return "*" in permissions or permission in permissions


def require_permission(identity: Identity, permission: str) -> None:
    if not has_permission(identity, permission):
        raise PermissionError(f"Role {identity.role} lacks permission {permission}")


def enforce_separation_of_duties(*, requester_id: str, approver: Identity, profile: str) -> None:
    if profile == "high-assurance" and requester_id == approver.principal_id:
        raise PermissionError("High-assurance approvals require an independent approver")


def _decode_master_key(encoded: str, *, label: str = "SDLC_MASTER_KEY_B64") -> bytes:
    if not encoded:
        raise RuntimeError(f"{label} is required for secret operations")
    try:
        key = base64.urlsafe_b64decode(encoded.encode("ascii"))
    except Exception as exc:
        raise RuntimeError(f"{label} is not valid base64") from exc
    if len(key) != 32:
        raise RuntimeError(f"{label} must decode to exactly 32 bytes")
    return key


def _master_key() -> bytes:
    return _decode_master_key(os.environ.get("SDLC_MASTER_KEY_B64", ""))


def generate_master_key() -> str:
    return base64.urlsafe_b64encode(AESGCM.generate_key(bit_length=256)).decode("ascii")


def put_secret(session: Session, *, project_id: str | None, name: str, value: str, actor: Identity, key_version: str = "v1") -> Secret:
    require_permission(actor, "secret:write" if actor.role == "admin" else "secret:use")
    existing = session.scalar(select(Secret).where(Secret.project_id == project_id, Secret.name == name))
    nonce = os.urandom(12)
    aad = f"{project_id or 'global'}:{name}:{key_version}".encode("utf-8")
    ciphertext = AESGCM(_master_key()).encrypt(nonce, value.encode("utf-8"), aad)
    if existing is None:
        existing = Secret(
            id=f"secret-{uuid.uuid4().hex}",
            project_id=project_id,
            name=name,
            ciphertext=ciphertext,
            nonce=nonce,
            key_version=key_version,
            created_by=actor.principal_id,
        )
        session.add(existing)
    else:
        existing.ciphertext = ciphertext
        existing.nonce = nonce
        existing.key_version = key_version
        existing.rotated_at = utcnow()
        existing.disabled = False
    session.flush()
    return existing


def resolve_secret(session: Session, *, project_id: str | None, name: str, actor: Identity) -> str:
    require_permission(actor, "secret:use")
    item = session.scalar(select(Secret).where(Secret.project_id == project_id, Secret.name == name, Secret.disabled.is_(False)))
    if item is None:
        raise KeyError(f"Secret not found: {name}")
    aad = f"{project_id or 'global'}:{name}:{item.key_version}".encode("utf-8")
    plaintext = AESGCM(_master_key()).decrypt(item.nonce, item.ciphertext, aad)
    return plaintext.decode("utf-8")


def rotate_secrets(
    session: Session, *, old_key_b64: str, new_key_b64: str, new_version: str, actor: Identity,
    project_id: str | None = None,
) -> dict[str, int | str]:
    """Atomically re-encrypt active secrets under a new master key.

    The new key is never persisted to the database. Callers are responsible for
    rotating the external secret/KMS value after this transaction succeeds.
    """
    if actor.role != "admin":
        raise PermissionError("Master-key rotation requires admin")
    if not new_version.strip():
        raise ValueError("new_version is required")
    old_key = _decode_master_key(old_key_b64, label="old master key")
    new_key = _decode_master_key(new_key_b64, label="new master key")
    statement = select(Secret).where(Secret.disabled.is_(False))
    if project_id is not None:
        statement = statement.where(Secret.project_id == project_id)
    rows = list(session.scalars(statement).all())
    rotated = 0
    for item in rows:
        old_aad = f"{item.project_id or 'global'}:{item.name}:{item.key_version}".encode("utf-8")
        plaintext = AESGCM(old_key).decrypt(item.nonce, item.ciphertext, old_aad)
        nonce = os.urandom(12)
        new_aad = f"{item.project_id or 'global'}:{item.name}:{new_version}".encode("utf-8")
        item.ciphertext = AESGCM(new_key).encrypt(nonce, plaintext, new_aad)
        item.nonce = nonce
        item.key_version = new_version
        item.rotated_at = utcnow()
        rotated += 1
    session.flush()
    return {"rotated": rotated, "key_version": new_version}


def permission_matrix() -> dict[str, list[str]]:
    return {role: sorted(values) for role, values in ROLE_PERMISSIONS.items()}
