from httpx import AsyncClient
import pytest


@pytest.mark.asyncio
async def test_favorites(async_client: AsyncClient):
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

    # Add the movie to favorites
    response = await async_client.post(
        f"/favorites/",
        json={"movieId": created_movie["id"]},
        headers={"Authorization": f"Bearer {login_response['access_token']}"},
    )
    assert response.status_code == 200
    favorite_response = response.json()
    assert favorite_response["movie"]["title"] == "Test Movie"

    # Add again to favorites (should raise an error)
    with pytest.raises(ValueError):
        response = await async_client.post(
            f"/favorites/",
            json={"movieId": created_movie["id"]},
            headers={"Authorization": f"Bearer {login_response['access_token']}"},
        )

    # Get user's favorites
    response = await async_client.get(
        "/favorites/",
        headers={"Authorization": f"Bearer {login_response['access_token']}"},
    )
    assert response.status_code == 200
    favorites = response.json()
    assert len(favorites) == 1
    assert favorites[0]["movie"]["title"] == "Test Movie"

    # Remove the movie from favorites
    response = await async_client.request(
        "DELETE",
        f"/favorites/",
        json={"movieId": created_movie["id"]},
        headers={"Authorization": f"Bearer {login_response['access_token']}"},
    )
    assert response.status_code == 204

    # Verify the movie is no longer in favorites
    response = await async_client.get(
        "/favorites/",
        headers={"Authorization": f"Bearer {login_response['access_token']}"},
    )
    assert response.status_code == 200
    favorites = response.json()
    assert len(favorites) == 0
