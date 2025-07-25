from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer
from typing import List
from blog.api.schemas.favorite_schema import favoriteInput, favoriteOutput
from blog.domain.entities.favorite import Favorite
from blog.domain.repositories.favorite_repository import FavoriteRepository
from blog.api.deps import get_current_user, get_favorite_repository
from blog.usecases.favorite.add_to_favorites import AddToFavoritesUseCase
from blog.usecases.favorite.get_user_favorites import GetUserFavoritesUseCase
from blog.usecases.favorite.remove_from_favorites import RemoveFromFavoritesUseCase

security = HTTPBearer()
router = APIRouter(prefix="/favorites", tags=["Favorites"])


@router.post("/", response_model=favoriteOutput)
async def add_to_favorites(
    data: favoriteInput,
    credentials=Depends(security),
    user=Depends(get_current_user),
    repo: FavoriteRepository = Depends(get_favorite_repository),
):
    usecase = AddToFavoritesUseCase(repo)
    result = await usecase.execute(user.id, data.movieId)
    return favoriteOutput.from_entity(result)


@router.get("/", response_model=List[favoriteOutput])
async def get_user_favorites(
    # user_id: str,
    credentials=Depends(security),
    user=Depends(get_current_user),
    repo: FavoriteRepository = Depends(get_favorite_repository),
):
    usecase = GetUserFavoritesUseCase(repo)
    favorites = await usecase.execute(user.id)
    return [favoriteOutput.from_entity(f) for f in favorites]


@router.delete("/", status_code=204)
async def remove_from_favorites(
    data: favoriteInput,
    credentials=Depends(security),
    user=Depends(get_current_user),
    repo: FavoriteRepository = Depends(get_favorite_repository),
):
    usecase = RemoveFromFavoritesUseCase(repo)
    await usecase.execute(user.id, data.movieId)
