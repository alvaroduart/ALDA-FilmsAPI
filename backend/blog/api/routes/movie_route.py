from fastapi import APIRouter, Depends, Query
from fastapi.security import HTTPBearer
from typing import List
from blog.api.schemas.movie_schema import CreateMovieInput, MovieOutput
from blog.domain.entities.movie import Movie
from blog.domain.repositories.movie_repository import MovieRepository
from blog.api.deps import get_movie_repository
from blog.usecases.movie.create_movie import CreateMovieUseCase
from blog.usecases.movie.get_all_movies import GetAllMoviesUseCase
from blog.usecases.movie.get_movie_by_id import GetMovieByIdUseCase
from blog.usecases.movie.search_movies import SearchMoviesUseCase

import uuid

security = HTTPBearer()
router = APIRouter(prefix="/movies", tags=["Movies"])


@router.post("/", response_model=MovieOutput)
async def create_movie(
    data: CreateMovieInput,
    credentials=Depends(security),
    repo: MovieRepository = Depends(get_movie_repository),
):
    movie = Movie(
        id=data.movieid or str(uuid.uuid4()),
        title=data.title,
        image=str(data.image),
        rating=data.rating or 0.0,
        description=data.description,
        genre=data.genre,
        duration=data.duration,
        director=data.director,
    )
    usecase = CreateMovieUseCase(repo)
    await usecase.execute(movie)
    return MovieOutput.from_entity(movie)


@router.get("/", response_model=List[MovieOutput])
async def get_all_movies(repo: MovieRepository = Depends(get_movie_repository)):
    usecase = GetAllMoviesUseCase(repo)
    movies = await usecase.execute()
    return [MovieOutput.from_entity(m) for m in movies]


@router.get("/{movie_id}", response_model=MovieOutput)
async def get_movie_by_id(
    movie_id: str, repo: MovieRepository = Depends(get_movie_repository)
):
    usecase = GetMovieByIdUseCase(repo)
    movie = await usecase.execute(movie_id)
    return MovieOutput.from_entity(movie)


@router.get("/search/", response_model=List[MovieOutput])
async def search_movies(
    query: str = Query(..., min_length=1),
    repo: MovieRepository = Depends(get_movie_repository),
):
    usecase = SearchMoviesUseCase(repo)
    movies = await usecase.execute(query)
    return [MovieOutput.from_entity(m) for m in movies]
