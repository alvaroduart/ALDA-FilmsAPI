import pytest
from httpx import AsyncClient
import datetime


@pytest.mark.asyncio
async def test_create_and_get_posts(client: AsyncClient):
    # Registro + login
    await client.post(
        "/users/register",
        json={
            "name": "Poster",
            "email": "poster@example.com",
            "password": "post@Test123",
            "role": "user",
        },
    )
    login_response = await client.post(
        "/users/login", json={"email": "poster@example.com", "password": "post@Test123"}
    )
    token = login_response.json()["access_token"]

    # Criação do post
    post_data = {
        "title": "Título de teste",
        "description": "Descrição curta",
        "content": "Conteúdo completo do post",
        "date": datetime.datetime.now().isoformat(),
    }

    response = await client.post(
        "/posts/",
        json=post_data,
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    post = response.json()
    assert post["title"] == post_data["title"]

    # GET /posts
    response = await client.get("/posts/")
    assert response.status_code == 200
    posts = response.json()
    assert any(p["title"] == post_data["title"] for p in posts)
