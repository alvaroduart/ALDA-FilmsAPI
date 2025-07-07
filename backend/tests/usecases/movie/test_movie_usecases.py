import pytest
from blog.domain.entities.movie import Movie
from blog.domain.repositories.movie_repository import MovieRepository
from blog.usecases.movie.get_all_movies import GetAllMoviesUseCase
from blog.usecases.movie.get_movie_by_id import GetMovieByIdUseCase
from blog.usecases.movie.search_movies import SearchMoviesUseCase
from blog.infra.repositories.in_memory_movie_repository import InMemoryMovieRepository

def test_get_all_movies():
    repo = InMemoryMovieRepository()
    use_case = GetAllMoviesUseCase(repo)

    movie1 = Movie(id="1", title="Movie One", description="Description One", image="img1.png", rating="4.5")
    movie2 = Movie(id="2", title="Movie Two", description="Description Two", image="img2.png", rating="5.0")
    repo.create(movie1)
    repo.create(movie2)

    movies = use_case.execute()

    assert len(movies) == 2
    assert movies[0].id == "1"
    assert movies[1].id == "2"

def test_get_movie_by_id():
    repo = InMemoryMovieRepository()
    use_case = GetMovieByIdUseCase(repo)

    movie = Movie(id="1", title="Movie One", description="Description One", image="img1.png", rating="3.0")
    repo.create(movie)

    retrieved_movie = use_case.execute("1")

    assert retrieved_movie.id == "1"
    assert retrieved_movie.title == "Movie One"
    assert retrieved_movie.description == "Description One"
    assert retrieved_movie.image == "img1.png"
    assert retrieved_movie.rating == "3.0"

def test_search_movies():
    repo = InMemoryMovieRepository()
    use_case = SearchMoviesUseCase(repo)

    # Add test data
    movie1 = Movie(id="1", title="Action Movie", description="An action-packed movie", image="img1.png", rating="4.0")
    movie2 = Movie(id="2", title="Comedy Movie", description="A hilarious comedy", image="img2.png", rating="3.5")
    repo.create(movie1)
    repo.create(movie2)

    results = use_case.execute("action")

    assert len(results) == 1
    assert results[0].id == "1"
    assert results[0].title == "Action Movie"

    # Test with no results
    results = use_case.execute("drama")
    assert len(results) == 0

def test_get_movie_by_id_not_found():
    repo = InMemoryMovieRepository()
    use_case = GetMovieByIdUseCase(repo)

    with pytest.raises(ValueError, match="Movie with id 999 not found"):
        use_case.execute("999")

def test_search_movies_empty():
    repo = InMemoryMovieRepository()
    use_case = SearchMoviesUseCase(repo)

    results = use_case.execute("nonexistent")
    assert len(results) == 0

def test_get_all_movies_empty():
    repo = InMemoryMovieRepository()
    use_case = GetAllMoviesUseCase(repo)

    movies = use_case.execute()
    assert len(movies) == 0


    