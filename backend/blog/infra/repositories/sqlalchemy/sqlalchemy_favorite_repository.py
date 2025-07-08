from sqlalchemy.ext.asyncio import AsyncSession
from blog.domain.entities.favorite import Favorite
from blog.domain.repositories.favorite_repository import FavoriteRepository
from blog.infra.models.favorite_model import FavoriteModel
from sqlalchemy.future import select

class SQLAlchemyFavoriteRepository(FavoriteRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_to_favorites(self, favorite: Favorite) -> Favorite:
        favorite_model = FavoriteModel.from_entity(favorite)
        self.session.add(favorite_model)
        await self.session.commit()
        return favorite_model.to_entity()

    async def get_user_favorites(self, user_id: int) -> list[Favorite]:
        result = await self.session.execute(
            select(FavoriteModel).where(FavoriteModel.user_id == user_id)
        )
        favorite_models = result.scalars().all()
        return [model.to_entity() for model in favorite_models]
    
    async def remove_from_favorites(self, favorite_id: int) -> None:
        result = await self.session.execute(
            select(FavoriteModel).where(FavoriteModel.id == favorite_id)
        )
        favorite_model = result.scalar_one_or_none()
        if favorite_model:
            await self.session.delete(favorite_model)
            await self.session.commit()
        else:
            raise ValueError("Favorite not found")