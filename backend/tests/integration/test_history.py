from httpx import AsyncClient
import pytest


@pytest.mark.asyncio
async def test_history(async_client: AsyncClient):
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

    # Get user history
    response = await async_client.get(
        "/history/",
        headers={"Authorization": f"Bearer {login_response['access_token']}"},
    )
    assert response.status_code == 200
    history = response.json()
    assert isinstance(history, list)
    assert len(history) == 0  # Assuming no history exists for a new user

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

    # Add the movie to user's history
    response = await async_client.post(
        "/history/",
        json={"movieId": created_movie["id"]},
        headers={"Authorization": f"Bearer {login_response['access_token']}"},
    )
    assert response.status_code == 200
    history_response = response.json()
    assert history_response["movie"]["id"] == created_movie["id"]

    # Now check the history again
    response = await async_client.get(
        "/history/",
        headers={"Authorization": f"Bearer {login_response['access_token']}"},
    )
    assert response.status_code == 200
    history = response.json()
    assert isinstance(history, list)
    assert len(history) > 0
    assert history[0]["movie"]["id"] == created_movie["id"]

    # Remove the movie from user's history
    response = await async_client.request(
        "DELETE",
        "/history/",
        json={"movieId": created_movie["id"]},
        headers={"Authorization": f"Bearer {login_response['access_token']}"},
    )
    assert response.status_code == 204

    # Check the history again to ensure the movie was removed
    response = await async_client.get(
        "/history/",
        headers={"Authorization": f"Bearer {login_response['access_token']}"},
    )
    assert response.status_code == 200
    history = response.json()
    assert isinstance(history, list)
    assert len(history) == 0
