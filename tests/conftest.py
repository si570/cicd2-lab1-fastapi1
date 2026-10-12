import pytest
from sqlalchemy import delete
from fastapi.testclient import TestClient

from app.database import SessionLocal
from app.main import app
from app.models import UserDB

@pytest.fixture(autouse=True)
def clear_users():
    with SessionLocal() as db:
        db.execute(delete(UserDB))
        db.commit()

@pytest.fixture
def client():
    return TestClient(app)