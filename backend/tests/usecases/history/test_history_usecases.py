import pytest
from blog.domain.entities.history import History
from blog.usecases.history.get_user_history import GetUserHistoryUseCase
from blog.usecases.history.add_to_history import AddToHistoryUseCase
from blog.usecases.history.remove_from_history import RemoveFromHistoryUseCase
from blog.infra.repositories.in_memory.in_memory_history_repository import (
    InMemoryHistoryRepository,
)


@pytest.mark.asyncio
async def test_add_to_history():
    repo = InMemoryHistoryRepository()
    use_case = AddToHistoryUseCase(repo)

    await use_case.execute("test_user", "test_movie")

    stored_history = await repo.get_by_user_id("test_user")
    assert len(stored_history) == 1
    assert stored_history[0].userId == "test_user"
    assert stored_history[0].movieId == "test_movie"
    assert stored_history[0].timestamp is not None  # gerado automaticamente


@pytest.mark.asyncio
async def test_get_user_history():
    repo = InMemoryHistoryRepository()
    add_use_case = AddToHistoryUseCase(repo)
    await add_use_case.execute("test_user", "test_movie")

    get_use_case = GetUserHistoryUseCase(repo)
    user_history = await get_use_case.execute("test_user")

    assert len(user_history) == 1
    assert user_history[0].userId == "test_user"
    assert user_history[0].movieId == "test_movie"
    assert user_history[0].timestamp is not None


@pytest.mark.asyncio
async def test_remove_from_history():
    repo = InMemoryHistoryRepository()
    add_use_case = AddToHistoryUseCase(repo)
    await add_use_case.execute("test_user", "test_movie")

    remove_use_case = RemoveFromHistoryUseCase(repo)
    await remove_use_case.execute("test_user", "test_movie")

    user_history = await repo.get_by_user_id("test_user")
    assert len(user_history) == 0
    assert not await repo.is_in_history("test_user", "test_movie")


@pytest.mark.asyncio
async def test_is_in_history():
    repo = InMemoryHistoryRepository()
    add_use_case = AddToHistoryUseCase(repo)
    await add_use_case.execute("test_user", "test_movie")

    assert await repo.is_in_history("test_user", "test_movie") is True
    assert await repo.is_in_history("test_user", "nonexistent_movie") is False
