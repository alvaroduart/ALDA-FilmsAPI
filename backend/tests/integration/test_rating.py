from httpx import AsyncClient
import pytest


@pytest.mark.asyncio
async def test_rating(async_client: AsyncClient):
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

    # Rate the movie
    response = await async_client.post(
        "/ratings/",
        json={"rating": 5, "movieId": created_movie["id"]},
        headers={"Authorization": f"Bearer {login_response['access_token']}"},
    )
    assert response.status_code == 200
    rated_movie = response.json()
    assert rated_movie["rating"] == 5

    # Get the movie by ID to check the rating
    response = await async_client.get(
        f"/movies/{created_movie['id']}",
        headers={"Authorization": f"Bearer {login_response['access_token']}"},
    )
    assert response.status_code == 200
    movie_details = response.json()
    assert movie_details["userRating"] == 5

    # Update the rating
    response = await async_client.put(
        "/ratings/",
        json={"rating": 3, "movieId": created_movie["id"]},
        headers={"Authorization": f"Bearer {login_response['access_token']}"},
    )
    assert response.status_code == 200
    updated_movie = response.json()
    assert updated_movie["rating"] == 3
    assert updated_movie["userId"] == created_user["id"]
    assert updated_movie["movieId"] == created_movie["id"]

    # Get the movie again to check the updated rating
    response = await async_client.get(
        f"/movies/{created_movie['id']}",
        headers={"Authorization": f"Bearer {login_response['access_token']}"},
    )
    assert response.status_code == 200
    movie_details = response.json()
    assert movie_details["userRating"] == 3

    # Get rating
    response = await async_client.get(
        f"/ratings/{created_movie['id']}",
        headers={"Authorization": f"Bearer {login_response['access_token']}"},
    )
    assert response.status_code == 200
    rating_details = response.json()
    assert rating_details["rating"] == 3


@pytest.mark.asyncio
async def test_rating_not_found(async_client: AsyncClient):
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

    # Attempt to get a rating for a non-existent movie
    response = await async_client.get(
        "/ratings/123e4567-e89b-12d3-a456-426614174000",
        headers={"Authorization": f"Bearer {login_response['access_token']}"},
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "Rating not found"}

    # update rating for a non-existent movie
    response = await async_client.put(
        "/ratings/",
        json={"rating": 3, "movieId": "123e4567-e89b-12d3-a456-426614174000"},
        headers={"Authorization": f"Bearer {login_response['access_token']}"},
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "Rating not found"}
