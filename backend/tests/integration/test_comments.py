import pytest
from httpx import AsyncClient
import datetime


@pytest.mark.asyncio
async def test_create_comment(async_client: AsyncClient, user_token: str):
    # Create a comment
    response = await async_client.post(
        "/comments",
        json={
            "movieId": "12345678-1234-5678-1234-567812345678",
            "content": "This is a test comment",
            "createdAt": datetime.datetime.now().isoformat(),
        },
        headers={"Authorization": f"Bearer {user_token}"},
    )

    assert response.status_code == 201
    data = response.json()
    assert data["content"] == "This is a test comment"
    assert data["movieId"] == "12345678-1234-5678-1234-567812345678"


@pytest.mark.asyncio
async def test_get_comments(async_client: AsyncClient, user_token: str):
    # Get comments for a movie
    response = await async_client.get(
        "/comments/12345678-1234-5678-1234-567812345678",
        headers={"Authorization": f"Bearer {user_token}"},
    )

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    if data:
        assert "content" in data[0]
        assert "movieId" in data[0]


@pytest.mark.asyncio
async def test_delete_comment(async_client: AsyncClient, user_token: str):
    # Create a comment to delete
    create_response = await async_client.post(
        "/comments",
        json={
            "movieId": "12345678-1234-5678-1234-567812345678",
            "content": "This comment will be deleted",
            "createdAt": datetime.datetime.now().isoformat(),
        },
        headers={"Authorization": f"Bearer {user_token}"},
    )

    assert create_response.status_code == 201
    comment_id = create_response.json()["id"]

    # Delete the comment
    delete_response = await async_client.delete(
        f"/comments/{comment_id}", headers={"Authorization": f"Bearer {user_token}"}
    )

    assert delete_response.status_code == 204


@pytest.mark.asyncio
async def test_update_comment(async_client: AsyncClient, user_token: str):
    # Create a comment to update
    create_response = await async_client.post(
        "/comments",
        json={
            "movieId": "12345678-1234-5678-1234-567812345678",
            "content": "This comment will be updated",
            "createdAt": datetime.datetime.now().isoformat(),
        },
        headers={"Authorization": f"Bearer {user_token}"},
    )

    assert create_response.status_code == 201
    comment_id = create_response.json()["id"]

    # Update the comment
    update_response = await async_client.put(
        f"/comments/{comment_id}",
        json={
            "content": "This is the updated comment",
            "createdAt": datetime.datetime.now().isoformat(),
        },
        headers={"Authorization": f"Bearer {user_token}"},
    )

    assert update_response.status_code == 200
    data = update_response.json()
    assert data["content"] == "This is the updated comment"
    assert data["id"] == comment_id
