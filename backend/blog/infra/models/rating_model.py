from blog.infra.database import Base
from sqlalchemy.orm import relationship, Mapped, mapped_column
import sqlalchemy as sa
import uuid
from datetime import datetime
from blog.domain.entities.rating import Rating


class RatingModel(Base):
    __tablename__ = "ratings"
    userId: Mapped[str] = mapped_column(
        sa.String(36), sa.ForeignKey("users.id"), primary_key=True, nullable=False
    )
    movieId: Mapped[str] = mapped_column(
        sa.String(36), sa.ForeignKey("movies.id"), primary_key=True, nullable=False
    )
    rating: Mapped[int] = mapped_column(sa.Integer, nullable=False)

    # Relacionamentos
    user = relationship("UserModel", back_populates="ratings")
    movie = relationship("MovieModel", back_populates="ratings")

    def to_entity(self) -> Rating:
        return Rating(userId=self.userId, movieId=self.movieId, rating=self.rating)

    @classmethod
    def from_entity(cls, rating: Rating) -> "RatingModel":
        return cls(userId=rating.userId, movieId=rating.movieId, rating=rating.rating)
