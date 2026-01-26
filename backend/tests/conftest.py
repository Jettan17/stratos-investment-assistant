"""Pytest fixtures for testing."""

import os
import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient, ASGITransport
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Set test database before importing app
os.environ["DATABASE_URL"] = "sqlite:///./test.db"

from api.main import app
from models.database import Base, get_db


# Create test engine
test_engine = create_engine(
    "sqlite:///./test.db", connect_args={"check_same_thread": False}
)
TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


def override_get_db():
    """Override database dependency for testing."""
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(scope="function")
def client():
    """Synchronous test client with fresh database for each test."""
    # Create tables
    Base.metadata.create_all(bind=test_engine)

    # Override database dependency
    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    # Clean up
    Base.metadata.drop_all(bind=test_engine)
    app.dependency_overrides.clear()


@pytest.fixture
async def async_client():
    """Async test client for async endpoint tests."""
    Base.metadata.create_all(bind=test_engine)
    app.dependency_overrides[get_db] = override_get_db

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac

    Base.metadata.drop_all(bind=test_engine)
    app.dependency_overrides.clear()
