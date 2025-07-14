import pytest

pytestmark = pytest.mark.asyncio

from blog.infra.repositories.in_memory.in_memory_favorite_repository import (
    InMemoryFavoriteRepository,
)
from blog.usecases.favorite.get_user_favorites import GetUserFavoritesUseCase
from blog.usecases.favorite.add_to_favorites import AddToFavoritesUseCase
from blog.usecases.favorite.remove_from_favorites import RemoveFromFavoritesUseCase


@pytest.mark.asyncio
async def test_add_to_favorites():
    repo = InMemoryFavoriteRepository()
    use_case = AddToFavoritesUseCase(repo)

    user_id = "user1"
    movie_id = "movie1"
    await use_case.execute(user_id, movie_id)

    favorites = await repo.get_by_user_id(user_id)
    # If favorites is empty, check if AddToFavoritesUseCase and InMemoryFavoriteRepository are implemented correctly.
    assert isinstance(favorites, list)
    assert len(favorites) == 1
    assert (
        getattr(favorites[0], "userId", None) == user_id
        or getattr(favorites[0], "user_id", None) == user_id
    )
    assert (
        getattr(favorites[0], "movieId", None) == movie_id
        or getattr(favorites[0], "movie_id", None) == movie_id
    )


@pytest.mark.asyncio
async def test_get_user_favorites():
    repo = InMemoryFavoriteRepository()
    add_use_case = AddToFavoritesUseCase(repo)
    await add_use_case.execute("user1", "movie1")
    await add_use_case.execute("user1", "movie2")

    get_use_case = GetUserFavoritesUseCase(repo)
    favorites = await get_use_case.execute("user1")

    assert len(favorites) == 2
    assert {
        getattr(fav, "movieId", getattr(fav, "movie_id", None)) for fav in favorites
    } == {"movie1", "movie2"}


@pytest.mark.asyncio
async def test_remove_from_favorites():
    repo = InMemoryFavoriteRepository()
    add_use_case = AddToFavoritesUseCase(repo)
    await add_use_case.execute("user1", "movie1")

    remove_use_case = RemoveFromFavoritesUseCase(repo)
    await remove_use_case.execute("user1", "movie1")

    favorites = await repo.get_by_user_id("user1")
    assert len(favorites) == 0
    assert not await repo.is_favorite("user1", "movie1")


@pytest.mark.asyncio
async def test_is_favorite():
    repo = InMemoryFavoriteRepository()
    add_use_case = AddToFavoritesUseCase(repo)
    await add_use_case.execute("user1", "movie1")

    assert await repo.is_favorite("user1", "movie1") is True
    assert await repo.is_favorite("user1", "movie2") is False
    assert await repo.is_favorite("user2", "movie1") is False
