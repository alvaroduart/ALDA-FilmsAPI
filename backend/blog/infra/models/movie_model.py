import sqlalchemy as sa
from sqlalchemy.orm import relationship, Mapped, mapped_column
from blog.domain.entities.movie import Movie
import uuid
from datetime import datetime
from blog.infra.database import Base

class MovieModel(Base):
    __tablename__ = "movies"

    id: Mapped[str] = mapped_column(sa.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    title: Mapped[str] = mapped_column(sa.String(150), nullable=False)
    image: Mapped[str] = mapped_column(sa.String(255), nullable=False)
    rating: Mapped[float] = mapped_column(sa.Float, nullable=True)
    director: Mapped[str] = mapped_column(sa.String(100), nullable=False)
    createdAt: Mapped[datetime] = mapped_column(sa.DateTime, default=datetime.utcnow)

    def to_entity(self) -> Movie:
        return Movie(
            id=self.id,
            title=self.title,
            image=self.image,
            rating=self.rating,
            description= self.description,
            genre=self.genre,
            duration=self.duration,
            director=self.director,
        )
    
    @classmethod
    def from_entity(cls, movie: Movie) -> "MovieModel":
        return cls(
            id=movie.id,
            title=movie.title,
            image=movie.image,
            rating=movie.rating,
            director=movie.director,
            description=movie.description,
            genre=movie.genre,
            duration=movie.duration,
        )