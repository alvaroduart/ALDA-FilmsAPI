import pytest
from blog.domain.entities.favorite import Favorite
from blog.domain.repositories.favorite_repository import FavoriteRepository
from blog.usecases.favorite.get_user_favorites import GetUserFavoritesUseCase
from blog.usecases.favorite.add_to_favorites import AddToFavoritesUseCase
from blog.usecases.favorite.remove_from_favorites import RemoveFromFavoritesUseCase
from blog.infra.repositories.in_memory.in_memory_favorite_repository import InMemoryFavoriteRepository


def test_add_to_favorites():
    repo = InMemoryFavoriteRepository()
    use_case = AddToFavoritesUseCase(repo)

    use_case.execute("test_user", "test_movie")

    stored_favorites = repo.get_by_user_id("test_user")
    assert len(stored_favorites) == 1
    assert stored_favorites[0].userId == "test_user"
    assert stored_favorites[0].movieId == "test_movie"


def test_get_user_favorites():
    repo = InMemoryFavoriteRepository()
    add_use_case = AddToFavoritesUseCase(repo)
    add_use_case.execute("test_user", "test_movie")

    get_use_case = GetUserFavoritesUseCase(repo)
    user_favorites = get_use_case.execute("test_user")

    assert len(user_favorites) == 1
    assert user_favorites[0].userId == "test_user"
    assert user_favorites[0].movieId == "test_movie"


def test_remove_from_favorites():
    repo = InMemoryFavoriteRepository()
    add_use_case = AddToFavoritesUseCase(repo)
    add_use_case.execute("test_user", "test_movie")

    remove_use_case = RemoveFromFavoritesUseCase(repo)
    remove_use_case.execute("test_user", "test_movie")

    user_favorites = repo.get_by_user_id("test_user")
    assert len(user_favorites) == 0
    assert not repo.is_favorite("test_user", "test_movie")


def test_is_favorite():
    repo = InMemoryFavoriteRepository()
    add_use_case = AddToFavoritesUseCase(repo)
    add_use_case.execute("test_user", "test_movie")

    assert repo.is_favorite("test_user", "test_movie") is True
    assert repo.is_favorite("test_user", "nonexistent_movie") is False


def test_get_user_favorites_empty():
    repo = InMemoryFavoriteRepository()
    get_use_case = GetUserFavoritesUseCase(repo)

    user_favorites = get_use_case.execute("nonexistent_user")
    assert len(user_favorites) == 0


def test_add_to_favorites_already_exists():
    repo = InMemoryFavoriteRepository()
    add_use_case = AddToFavoritesUseCase(repo)

    add_use_case.execute("test_user", "test_movie")
    add_use_case.execute("test_user", "test_movie")  # Duplicado, mas deve ser ignorado

    stored_favorites = repo.get_by_user_id("test_user")
    assert len(stored_favorites) == 1  # Sem duplicatas


def test_remove_from_favorites_not_exists():
    repo = InMemoryFavoriteRepository()
    remove_use_case = RemoveFromFavoritesUseCase(repo)

    # Não deve causar erro nem alterar nada
    remove_use_case.execute("test_user", "nonexistent_movie")

    assert len(repo.get_by_user_id("test_user")) == 0


def test_is_favorite_not_exists():
    repo = InMemoryFavoriteRepository()
    assert repo.is_favorite("test_user", "nonexistent_movie") is False


def test_get_user_favorites_multiple_favorites():
    repo = InMemoryFavoriteRepository()
    add_use_case = AddToFavoritesUseCase(repo)

    add_use_case.execute("test_user", "movie_1")
    add_use_case.execute("test_user", "movie_2")
    add_use_case.execute("test_user", "movie_3")

    get_use_case = GetUserFavoritesUseCase(repo)
    user_favorites = get_use_case.execute("test_user")

    assert len(user_favorites) == 3
    assert {fav.movieId for fav in user_favorites} == {"movie_1", "movie_2", "movie_3"}


def test_get_user_favorites_no_favorites():
    repo = InMemoryFavoriteRepository()
    get_use_case = GetUserFavoritesUseCase(repo)

    user_favorites = get_use_case.execute("test_user")
    assert len(user_favorites) == 0
