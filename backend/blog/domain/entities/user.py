from datetime import datetime
from blog.domain.value_objects.email_vo import Email
from blog.domain.value_objects.password import Password

class User:
    def __init__(self, id: str, name: str, email: Email, password: Password = None, favoriteMovies: list[str] = None, watchedMovies: list[str] = None, createdAt: datetime = None):
        self.id = id
        self.name = name
        self.email = email
        self.password = password
        self.favoriteMovies = favoriteMovies if favoriteMovies is not None else []
        self.watchedMovies = watchedMovies if watchedMovies is not None else []
        self.createdAt = createdAt if createdAt is not None else datetime.now()

