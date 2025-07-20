import blog.domain.entities.rating


class Rating:
    def __init__(self, userId: str, movieId: str, rating: int):
        self.userId = userId
        self.movieId = movieId
        self.rating = rating
