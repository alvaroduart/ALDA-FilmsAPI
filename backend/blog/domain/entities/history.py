from datetime import datetime
from typing import Optional

from blog.domain.entities.movie import Movie
from blog.domain.entities.user import User


class History:
    def __init__(self, userId: str, movieId: str, movie: Optional[Movie] = None):
        self.userId = userId
        self.movieId = movieId
        self.movie = movie
