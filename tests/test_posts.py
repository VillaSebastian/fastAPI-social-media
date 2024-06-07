from fastapi import status
from fastapi.testclient import TestClient
from tests.database import client, test_user, authorized_client, token


def test_create_post(authorized_client: TestClient):
    # Successful post creation
    post_data = {"title": "Test Post for creating", "content": "This is a test content"}
    response = authorized_client.post("/posts", json=post_data)
    assert response.status_code == status.HTTP_201_CREATED
    new_post = response.json()
    assert new_post["title"] == post_data["title"]
    assert new_post["content"] == post_data["content"]
    assert "id" in new_post

    # Check if the post was added to the database
    post_id = new_post["id"]
    response = authorized_client.get(f'/posts/{post_id}')
    assert response.status_code == status.HTTP_200_OK
    post = response.json()
    assert post["title"] == post_data["title"]
    assert post["content"] == post_data["content"]
    assert post["id"] == post_id

    # Invalid input (missing title)
    invalid_post_data = {"content": "Test Content without Title"}
    response = authorized_client.post("/posts", json=invalid_post_data)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert "detail" in response.json()

def test_get_posts(client: TestClient):
    response = client.get("/posts")
    assert response.status_code == status.HTTP_200_OK

def test_update_post(authorized_client: TestClient):
    # Create a post to update
    initial_data = {"title": "Initial title", "content": "Initial content"}
    response = authorized_client.post("/posts", json=initial_data)
    assert response.status_code == status.HTTP_201_CREATED
    new_post = response.json()
    post_id = new_post["id"]

    # Update the post
    updated_data = {"title": "Updated title", "content": "Updated content"}
    response = authorized_client.patch(f'/posts/{post_id}', json=updated_data)
    assert response.status_code == status.HTTP_200_OK

    # Verify the update
    response = authorized_client.get(f'/posts/{post_id}')
    assert response.status_code == status.HTTP_200_OK
    post = response.json()
    assert post["title"] == updated_data["title"]
    assert post["content"] == updated_data["content"]

    # Invalid input (missing title)
    invalid_post_data = {"content": "Test Content without Title"}
    response = authorized_client.post("/posts", json=invalid_post_data)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert "detail" in response.json()

def test_delete_post(authorized_client: TestClient):
    # Successful post creation
    post_data = {"title": "Test Post", "content": "This is a test content"}
    response = authorized_client.post("/posts", json=post_data)
    new_post = response.json()
    post_id = new_post["id"]

    # Delete post
    response = authorized_client.delete(f'/posts/{post_id}')
    assert response.status_code == status.HTTP_204_NO_CONTENT
    
    # Verify the deletion
    response = authorized_client.get(f'/posts/{post_id}')
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {'detail': f'The post {post_id} was not found'}

    # Attempt to delete again
    response = authorized_client.delete(f'/posts/{post_id}')
    assert response.json() == {'detail': f'The post {post_id} was not found'}