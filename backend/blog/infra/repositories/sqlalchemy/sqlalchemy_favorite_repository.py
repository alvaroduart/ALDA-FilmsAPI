from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from blog.domain.entities.favorite import Favorite
from blog.domain.repositories.favorite_repository import FavoriteRepository
from blog.infra.models.favorite_model import FavoriteModel


class SQLAlchemyFavoriteRepository(FavoriteRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_user_id(self, user_id: str) -> list[Favorite]:
        result = await self.session.execute(
            select(FavoriteModel).where(FavoriteModel.userId == user_id)
        )
        favorite_models = result.scalars().all()
        return [model.to_entity() for model in favorite_models]

    async def add_favorite(self, favorite: Favorite) -> None:
        favorite_model = FavoriteModel.from_entity(favorite)
        self.session.add(favorite_model)
        await self.session.commit()

    async def remove_favorite(self, user_id: str, movie_id: str) -> None:
        result = await self.session.execute(
            select(FavoriteModel).where(
                FavoriteModel.userId == user_id, FavoriteModel.movieId == movie_id
            )
        )
        favorite_model = result.scalar_one_or_none()
        if favorite_model:
            await self.session.delete(favorite_model)
            await self.session.commit()
        else:
            raise ValueError("Favorite not found")

    async def is_favorite(self, user_id: str, movie_id: str) -> bool:
        result = await self.session.execute(
            select(FavoriteModel).where(
                FavoriteModel.userId == user_id, FavoriteModel.movieId == movie_id
            )
        )
        return result.scalar_one_or_none() is not None
