from sqlalchemy.ext.asyncio import AsyncSession
from blog.domain.entities.movie import Movie
from blog.domain.repositories.movie_repository import MovieRepository
from blog.infra.models.movie_model import MovieModel
from sqlalchemy.future import select


class SQLAlchemyMovieRepository(MovieRepository):
    def __init__(self, session: AsyncSession):
        self.session = session


    async def create_movie(self, movie: Movie) -> Movie:
        movie_model = MovieModel.from_entity(movie)
        self.session.add(movie_model)
        await self.session.commit()
        return movie_model.to_entity()


    async def get_movie_by_id(self, movie_id: int) -> Movie | None:
        result = await self.session.execute(
            select(MovieModel).where(MovieModel.id == movie_id)
        )
        movie_model = result.scalar_one_or_none()
        return movie_model.to_entity() if movie_model else None


    async def get_all_movies(self) -> list[Movie]:
        result = await self.session.execute(select(MovieModel))
        movie_models = result.scalars().all()
        return [model.to_entity() for model in movie_models]
   
    async def search_movies(self, query: str) -> list[Movie]:
        result = await self.session.execute(
            select(MovieModel).where(MovieModel.title.ilike(f"%{query}%"))
        )
        movie_models = result.scalars().all()
        return [model.to_entity() for model in movie_models]
