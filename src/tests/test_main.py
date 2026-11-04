from types import SimpleNamespace
from unittest.mock import Mock

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.database import get_db
from app.main import app


@pytest.fixture
def db():
    return Mock(spec=Session)


@pytest.fixture
def client(db):
    app.dependency_overrides[get_db] = lambda: db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()


def test_health_returns_healthy(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_ready_returns_ready_when_database_is_available(client, db):
    response = client.get("/ready")

    assert response.status_code == 200
    assert response.json() == {"status": "ready"}

    db.execute.assert_called_once()


def test_ready_returns_503_when_database_is_unavailable(client, db):
    db.execute.side_effect = SQLAlchemyError("Database connection failed")

    response = client.get("/ready")

    assert response.status_code == 503
    assert response.json() == {"detail": "database unavailable"}


def test_albums_returns_album_data(client, db):
    albums = [
        SimpleNamespace(
            id=1,
            title="Album One",
            artist="Artist One",
            price=19.99,
            image_url="https://example.com/album1.jpg",
        ),
        SimpleNamespace(
            id=2,
            title="Album Two",
            artist="Artist Two",
            price=24.99,
            image_url="https://example.com/album2.jpg",
        ),
    ]

    db.scalars.return_value.all.return_value = albums

    response = client.get("/albums")

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 2
    assert data[0]["id"] == 1
    assert data[0]["title"] == "Album One"
    assert data[0]["artist"] == "Artist One"
    assert data[0]["price"] == 19.99
    assert data[0]["image_url"] == "https://example.com/album1.jpg"