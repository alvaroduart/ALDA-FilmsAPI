import sqlalchemy as sa
from sqlalchemy.orm import relationship, Mapped, mapped_column
from blog.domain.entities.history import History
import uuid
from datetime import datetime
from blog.infra.database import Base

class HistoryModel(Base):
    __tablename__ = "histories"

    id: Mapped[str] = mapped_column(sa.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    userId: Mapped[str] = mapped_column(sa.String(36), nullable=False)
    movieId: Mapped[str] = mapped_column(sa.String(36), nullable=False)
    createdAt: Mapped[datetime] = mapped_column(sa.DateTime, default=datetime.utcnow)

    def to_entity(self) -> History:
        return History(
            id=self.id,
            userId=self.userId,
            movieId=self.movieId,
            createdAt=self.createdAt
        )
    
    user = relationship("UserModel", back_populates="histories")
    movie = relationship("MovieModel", back_populates="histories")
    
    @classmethod
    def from_entity(cls, history: History) -> "HistoryModel":
        return cls(
            id=history.id,
            userId=history.userId,
            movieId=history.movieId,
            createdAt=history.createdAt
        )