from httpx import AsyncClient
import pytest


@pytest.mark.asyncio
async def test_contact(async_client: AsyncClient):
    # create contact
    response = await async_client.post(
        "/contact/",
        json={
            "name": "Test User",
            "email": "testuser@example.com",
            "message": "This is a test message.",
        },
    )
    assert response.status_code == 200
    created_contact = response.json()
    assert created_contact["name"] == "Test User"
    assert created_contact["email"] == "testuser@example.com"
    assert created_contact["message"] == "This is a test message."
