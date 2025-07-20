from blog.domain.entities.rating import Rating
from blog.infra.models.rating_model import RatingModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from blog.domain.repositories.rating_repository import RatingRepository


class SQLAlchemyRatingRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_rating(self, rating: Rating) -> Rating:
        rating_model = RatingModel.from_entity(rating)

        self.session.add(rating_model)
        await self.session.commit()

        rating_sel = await self.session.execute(
            select(RatingModel).where(
                RatingModel.userId == rating.userId,
                RatingModel.movieId == rating.movieId,
            )
        )
        new_rating_model = rating_sel.scalar_one_or_none()
        if not new_rating_model:
            raise ValueError("Rating not found")
        return new_rating_model.to_entity()

    async def update_rating(self, rating: Rating) -> Rating:
        rating_model = RatingModel.from_entity(rating)
        await self.session.merge(rating_model)
        await self.session.commit()
        rating_sel = await self.session.execute(
            select(RatingModel).where(
                RatingModel.userId == rating.userId,
                RatingModel.movieId == rating.movieId,
            )
        )
        new_rating_model = rating_sel.scalar_one_or_none()
        if not new_rating_model:
            raise ValueError("Rating not found")
        return new_rating_model.to_entity()

    async def is_rated(self, user_id: str, movie_id: str) -> bool:
        result = await self.session.execute(
            select(RatingModel).where(
                RatingModel.userId == user_id, RatingModel.movieId == movie_id
            )
        )
        return result.scalar_one_or_none() is not None

    async def get_rating(self, user_id: str, movie_id: str) -> Rating | None:
        result = await self.session.execute(
            select(RatingModel).where(
                RatingModel.userId == user_id, RatingModel.movieId == movie_id
            )
        )
        rating_model = result.scalar_one_or_none()
        return rating_model.to_entity() if rating_model else None
