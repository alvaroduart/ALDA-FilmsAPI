import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_and_get_movie(async_client: AsyncClient):

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

    # Get the created movie by ID
    response = await async_client.get(
        f"/movies/{created_movie['id']}",
        headers={"Authorization": f"Bearer {login_response['access_token']}"},
    )
    assert response.status_code == 200
    movie_info = response.json()
    assert movie_info["title"] == "Test Movie"
    assert movie_info["id"] == created_movie["id"]
    assert movie_info["image"] == "http://example.com/image.jpg"
    assert movie_info["rating"] == 4.0
    assert movie_info["description"] == "A test movie description."
    assert movie_info["genre"] == "Action"
    assert movie_info["duration"] == "120 min"
    assert movie_info["director"] == "Test Director"

    # Search for the movie
    response = await async_client.get(
        "/movies/search/",
        params={"query": "Test"},
        headers={"Authorization": f"Bearer {login_response['access_token']}"},
    )
    assert response.status_code == 200
    search_results = response.json()
    assert len(search_results) > 0
    assert search_results[0]["title"] == "Test Movie"
    assert search_results[0]["id"] == created_movie["id"]
