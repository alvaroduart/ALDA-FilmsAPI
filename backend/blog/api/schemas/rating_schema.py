from pydantic import BaseModel, ConfigDict, Field


class RatingInput(BaseModel):
    movieId: str = Field(..., description="ID of the movie being rated")
    rating: int = Field(..., ge=1, le=5, description="Rating value between 1 and 5")


class RatingOutput(BaseModel):
    userId: str = Field(..., description="ID of the user who rated the movie")
    movieId: str = Field(..., description="ID of the movie that was rated")
    rating: int = Field(..., ge=1, le=5, description="Rating value between 1 and 5")

    model_config = ConfigDict(from_attributes=True)

    @classmethod
    def from_entity(cls, rating):
        return cls(userId=rating.userId, movieId=rating.movieId, rating=rating.rating)
