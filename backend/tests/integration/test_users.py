from httpx import AsyncClient
import pytest


@pytest.mark.asyncio
async def test_create_and_login_user(async_client: AsyncClient):
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

    # create a user with the same email
    with pytest.raises(ValueError):
        response = await async_client.post(
            "/users/register",
            json={
                "username": "anotheruser",
                "email": "testuser@example.com",
                "password": "testPassword1@",
            },
        )

    # create a user with the same username
    with pytest.raises(ValueError):
        response = await async_client.post(
            "/users/register",
            json={
                "username": "testuser",
                "email": "testuser2@example.com",
                "password": "testPassword1@",
            },
        )

    # Log in the user
    response = await async_client.post(
        "/users/login",
        json={"email": "testuser@example.com", "password": "testPassword1@"},
    )
    assert response.status_code == 200
    login_response = response.json()
    assert "access_token" in login_response

    # GET /users/me
    response = await async_client.get(
        "/users/me",
        headers={"Authorization": f"Bearer {login_response['access_token']}"},
    )
    assert response.status_code == 200
    user_info = response.json()
    assert user_info["username"] == "testuser"
    assert user_info["email"] == "testuser@example.com"
