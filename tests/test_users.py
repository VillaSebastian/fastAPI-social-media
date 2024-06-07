import jwt
import pytest
from app.schemas import Token
from app.security import SECRET_KEY, ALGORITHM
from fastapi import status
from fastapi.testclient import TestClient
from tests.database import client, test_user


def test_create_user(client: TestClient):
    response = client.post("/users", json={"email": "deadpool@example.com", "password": "chimichangas4life"})

    assert response.status_code == status.HTTP_201_CREATED
    new_user = response.json()
    assert new_user["email"] == "deadpool@example.com"
    assert "id" in new_user
    user_id = new_user["id"]

    response = client.get(f'/users/{user_id}')
    assert response.status_code == status.HTTP_200_OK
    new_user = response.json()
    assert new_user["email"] == "deadpool@example.com"
    assert new_user["id"] == user_id

def test_login_user(client, test_user):
    response = client.post("/login", data={"username": test_user['email'], "password": test_user['password']})
    assert response.status_code == status.HTTP_200_OK
    login_response = Token(**response.json())
    payload = jwt.decode(login_response.access_token, key=SECRET_KEY, algorithms=[ALGORITHM])
    id: str = payload.get("user_id")
    assert id == test_user['id']
    assert login_response.token_type == "bearer"


@pytest.mark.parametrize("email, password, status_code", {
    ('wrongemail@gmail.com', 'password123', 403),
    ('test@gmail.com', 'wrongpassword', 403),
    ('wrongemail@gmail.com', 'wrongpassword', 403),
    (None, 'password123', 422),
    ('wrongemail@gmail.com', None, 422)
})
def test_incorrect_login(client, email, password, status_code):
    response = client.post("/login", data={"username": email, "password": password})

    assert response.status_code == status_code