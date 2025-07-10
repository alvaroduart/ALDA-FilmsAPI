import sqlalchemy as sa
from sqlalchemy.orm import relationship, Mapped, mapped_column
from blog.domain.entities.favorite import Favorite
import uuid
from datetime import datetime
from blog.infra.database import Base

class FavoriteModel(Base):
    __tablename__ = "favorites"

    id: Mapped[str] = mapped_column(sa.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    userId: Mapped[str] = mapped_column(sa.String(36), sa.ForeignKey("users.id"), nullable=False)
    movieId: Mapped[str] = mapped_column(sa.String(36), sa.ForeignKey("movies.id"), nullable=False)
    createdAt: Mapped[datetime] = mapped_column(sa.DateTime, default=datetime.utcnow)

    # Relacionamentos
    user = relationship("UserModel", back_populates="favorites")
    movie = relationship("MovieModel", back_populates="favorites")

    def to_entity(self) -> Favorite:
        return Favorite(
            userId=self.userId,
            movieId=self.movieId,
        )

    @classmethod
    def from_entity(cls, favorite: Favorite) -> "FavoriteModel":
        return cls(
            userId=favorite.userId,
            movieId=favorite.movieId,
        )
