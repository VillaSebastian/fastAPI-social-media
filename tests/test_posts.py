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


def test_create_post(client: TestClient):
    # Successful post creation
    post_data = {"title": "Test Post for creating", "content": "This is a test content"}
    response = client.post("/posts", json=post_data)
    assert response.status_code == status.HTTP_201_CREATED
    new_post = response.json()
    assert new_post["title"] == post_data["title"]
    assert new_post["content"] == post_data["content"]
    assert "id" in new_post

    # Check if the post was added to the database
    post_id = new_post["id"]
    response = client.get(f'/posts/{post_id}')
    assert response.status_code == status.HTTP_200_OK
    post = response.json()
    assert post["title"] == post_data["title"]
    assert post["content"] == post_data["content"]
    assert post["id"] == post_id

    # Invalid input (missing title)
    invalid_post_data = {"content": "Test Content without Title"}
    response = client.post("/posts", json=invalid_post_data)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert "detail" in response.json()

def test_get_posts(client: TestClient):
    response = client.get("/posts")
    assert response.status_code == status.HTTP_200_OK

def test_update_post(client: TestClient):
    # Create a post to update
    initial_data = {"title": "Initial title", "content": "Initial content"}
    response = client.post("/posts", json=initial_data)
    assert response.status_code == status.HTTP_201_CREATED
    new_post = response.json()
    post_id = new_post["id"]

    # Update the post
    updated_data = {"title": "Updated title", "content": "Updated content"}
    response = client.patch(f'/posts/{post_id}', json=updated_data)
    assert response.status_code == status.HTTP_200_OK

    # Verify the update
    response = client.get(f'/posts/{post_id}')
    assert response.status_code == status.HTTP_200_OK
    post = response.json()
    assert post["title"] == updated_data["title"]
    assert post["content"] == updated_data["content"]

    # Invalid input (missing title)
    invalid_post_data = {"content": "Test Content without Title"}
    response = client.post("/posts", json=invalid_post_data)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert "detail" in response.json()


def test_delete_post(client: TestClient):
    # Successful post creation
    post_data = {"title": "Test Post", "content": "This is a test content"}
    response = client.post("/posts", json=post_data)
    new_post = response.json()
    post_id = new_post["id"]

    # Delete post
    response = client.delete(f'/posts/{post_id}')
    assert response.status_code == status.HTTP_204_NO_CONTENT
    
    # Verify the deletion
    response = client.get(f'/posts/{post_id}')
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {'detail': f'The post {post_id} was not found'}

    # Attempt to delete again
    response = client.delete(f'/posts/{post_id}')
    assert response.json() == {'detail': f'The post {post_id} was not found'}