from app.main import app
from fastapi import status
from fastapi.testclient import TestClient


client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == status.HTTP_200_OK
    assert "text/html" in response.headers["content-type"]

def test_get_posts():
    response = client.get("/posts")
    assert response.status_code == status.HTTP_200_OK
    assert "data" in response.json()

def test_create_post():
    post_data = {"title": "Test Title", "content": "Test Content"}
    response = client.post("/posts", json=post_data)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == {'Message': 'Post created successfully'}

def test_get_one_post():
    post_id = 1
    response = client.get(f'/posts/{post_id}')
    if response.status_code == status.HTTP_404_NOT_FOUND:
        assert response.json() == {'detail': f'The post {post_id} was not found'}
    else:
        assert response.status_code == status.HTTP_200_OK
        assert "post_detail" in response.json()

def test_update_post():
    post_id = 1
    update_data = {"title": "Test Title", "content": "Test Content"}
    response = client.patch(f'/posts/{post_id}', json=update_data)
    if response.status_code == status.HTTP_404_NOT_FOUND:
        assert response.json() == {'detail': f'The post {post_id} was not found'}
    else:
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {"Message": "Post updated successfully"}

def test_delete_post():
    post_id = 1
    response = client.delete(f'/posts/{post_id}')
    if response.status_code == status.HTTP_404_NOT_FOUND:
        assert response.json() == {'detail': f'The post {post_id} was not found'}
    else:
        assert response.status_code == status.HTTP_204_NO_CONTENT