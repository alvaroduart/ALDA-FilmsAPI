from httpx import AsyncClient
import pytest


@pytest.mark.asyncio
async def test_coments_flow(async_client: AsyncClient):
    # Create a user
    response = await async_client.post(
        "/users/register",
        json={
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "testPassword1@",
        },
    )
    assert response.status_code == 200
    created_user = response.json()
    assert created_user["username"] == "testuser"

    # Log in the user
    user = await async_client.post(
        "/users/login",
        json={"email": "testuser@example.com", "password": "testPassword1@"},
    )
    assert user.status_code == 200
    login_response = user.json()
    assert "access_token" in login_response

    # Create a movie
    response = await async_client.post(
        "/movies/",
        json={
            "movieid": "123e4567-e89b-12d3-a456-426614174000",
            "title": "Test Movie",
            "image": "http://example.com/image.jpg",
            "rating": 4,
            "description": "A test movie description.",
            "genre": "Action",
            "duration": "120 min",
            "director": "Test Director",
        },
        headers={"Authorization": f"Bearer {login_response['access_token']}"},
    )
    assert response.status_code == 200
    created_movie = response.json()
    assert created_movie["title"] == "Test Movie"

    # Create a comment
    response = await async_client.post(
        "/comments/",
        json={"movieId": created_movie["id"], "content": "This is a test comment."},
        headers={"Authorization": f"Bearer {login_response['access_token']}"},
    )
    assert response.status_code == 200
    created_comment = response.json()
    assert created_comment["content"] == "This is a test comment."

    # Update the comment
    response = await async_client.put(
        "/comments/",
        json={
            "id": created_comment["id"],
            "movieId": created_movie["id"],
            "content": "This is an updated test comment.",
        },
        headers={"Authorization": f"Bearer {login_response['access_token']}"},
    )
    assert response.status_code == 200
    updated_comment = response.json()
    assert updated_comment["content"] == "This is an updated test comment."

    # Get comments by movie
    response = await async_client.get(
        f"/comments/movie/{created_movie['id']}",
        headers={"Authorization": f"Bearer {login_response['access_token']}"},
    )
    assert response.status_code == 200
    comments = response.json()
    assert len(comments) > 0
    assert comments[0]["content"] == "This is an updated test comment."

    # Delete the comment
    response = await async_client.request(
        "DELETE",
        "/comments/",
        json={"id": created_comment["id"]},
        headers={"Authorization": f"Bearer {login_response['access_token']}"},
    )
    assert response.status_code == 204

    # Verify the comment is deleted
    response = await async_client.get(
        f"/comments/movie/{created_movie['id']}",
        headers={"Authorization": f"Bearer {login_response['access_token']}"},
    )
    assert response.status_code == 200
    comments = response.json()
    assert len(comments) == 0
