from __future__ import annotations

import tempfile
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from venue_pilot.api import create_app
from venue_pilot.service import ReservationService


@pytest.fixture
def database_path() -> Path:
    with tempfile.TemporaryDirectory() as tmp:
        yield Path(tmp) / "pilot.db"


@pytest.fixture
def service(database_path: Path) -> ReservationService:
    return ReservationService(database_path)


@pytest.fixture
def client(database_path: Path) -> TestClient:
    with TestClient(create_app(database_path)) as test_client:
        yield test_client
