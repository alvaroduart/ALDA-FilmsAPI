from datetime import datetime
from typing import Optional

from blog.domain.entities.movie import Movie
from blog.domain.entities.user import User


class Comment:
    def __init__(
        self,
        id: str,
        movieId: str,
        userId: str,
        userName: str,
        content: str,
        createdAt: datetime,
        user: Optional[User] = None,
    ):
        self.id = id
        self.movieId = movieId
        self.userId = userId
        self.userName = userName
        self.content = content
        self.createdAt = createdAt if createdAt is not None else datetime.now()
        self.user = user
