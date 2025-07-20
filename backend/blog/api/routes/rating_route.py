from blog.api.deps import get_current_user, get_rating_repository
from blog.api.schemas.rating_schema import RatingInput, RatingOutput
from blog.domain.entities.rating import Rating
from fastapi.security import HTTPBearer
from fastapi import APIRouter, Depends, HTTPException
from typing import List, Optional
from blog.usecases.rating.add_rating import AddRatingUseCase
from blog.domain.repositories.rating_repository import RatingRepository
from blog.usecases.rating.get_rating import GetRatingUseCase
from blog.usecases.rating.update_rating import UpdateRatingUseCase
from blog.usecases.rating.is_rated import IsRatedUseCase


security = HTTPBearer()
router = APIRouter(prefix="/ratings", tags=["Ratings"])


@router.post("/", response_model=None)
async def create_rating(
    data: RatingInput,
    credentials=Depends(security),
    user=Depends(get_current_user),
    repo: RatingRepository = Depends(get_rating_repository),
):
    usecase = AddRatingUseCase(repo)
    result = await usecase.execute(user.id, data.movieId, data.rating)
    return RatingOutput.from_entity(result)


@router.put("/", response_model=RatingOutput)
async def update_rating(
    data: RatingInput,
    credentials=Depends(security),
    user=Depends(get_current_user),
    repo: RatingRepository = Depends(get_rating_repository),
):
    getUsecase = IsRatedUseCase(repo)
    existing_rating = await getUsecase.execute(user.id, data.movieId)

    if not existing_rating:
        raise HTTPException(status_code=404, detail="Rating not found")

    usecase = UpdateRatingUseCase(repo)
    result = await usecase.execute(Rating(user.id, data.movieId, data.rating))
    return RatingOutput.from_entity(result)


@router.get("/{movie_id}", response_model=RatingOutput)
async def get_ratings(
    movie_id: str,
    user=Depends(get_current_user),
    repo: RatingRepository = Depends(get_rating_repository),
):
    usecase = GetRatingUseCase(repo)
    result = await usecase.execute(user.id, movie_id)
    if not result:
        raise HTTPException(status_code=404, detail="Rating not found")
    return RatingOutput.from_entity(result)
