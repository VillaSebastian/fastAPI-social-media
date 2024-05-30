from fastapi import status
from fastapi.testclient import TestClient
from tests.database import client


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