import pytest
from app.main import app
from app.database import get_db
from tests.database import override_get_db, set_up_database, drop_database
from fastapi import status
from fastapi.testclient import TestClient


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture
def client():
    # Run code before tests run
    drop_database()
    set_up_database()
    yield TestClient(app)
    # Run code after tests run


def test_create_user(client: TestClient):
    response = client.post("/users", json={"email": "deadpool@example.com", "password": "chimichangas4life"})

    assert response.status_code == status.HTTP_201_CREATED
    new_user = response.json()
    assert new_user["email"] == "deadpool@example.com"
    assert "id" in new_user
    user_id = new_user["id"]

    response = client.get(f'/users/{user_id}')
    assert response.status_code == 200
    new_user = response.json()
    assert new_user["email"] == "deadpool@example.com"
    assert new_user["id"] == user_id