from sqlalchemy.ext.asyncio import AsyncSession
from blog.domain.entities.movie import Movie
from blog.domain.repositories.movie_repository import MovieRepository
from blog.infra.models.movie_model import MovieModel
from sqlalchemy.future import select


class SQLAlchemyMovieRepository(MovieRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, movie: Movie) -> None:
        movie_model = MovieModel.from_entity(movie)
        self.session.add(movie_model)
        await self.session.commit()

    async def get_by_id(self, movie_id: str) -> Movie:
        result = await self.session.execute(
            select(MovieModel).where(MovieModel.id == movie_id)
        )
        movie_model = result.scalar_one_or_none()
        if not movie_model:
            raise ValueError("Movie not found")
        return movie_model.to_entity()

    async def get_all(self) -> list[Movie]:
        result = await self.session.execute(select(MovieModel))
        movie_models = result.scalars().all()
        return [model.to_entity() for model in movie_models]

    async def search(self, query: str) -> list[Movie]:
        result = await self.session.execute(
            select(MovieModel).where(MovieModel.title.ilike(f"%{query}%"))
        )
        movie_models = result.scalars().all()
        return [model.to_entity() for model in movie_models]
