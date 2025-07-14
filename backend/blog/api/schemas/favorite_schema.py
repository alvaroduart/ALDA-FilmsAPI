from pydantic import BaseModel, Field, ConfigDict
from typing import Optional


class favoriteInput(BaseModel):
    movieId: str = Field(..., description="ID of the movie to be favorited")
    userId: str = Field(..., description="ID of the user favoriting the movie")


class favoriteOutput(BaseModel):
    userId: str = Field(..., description="ID of the user who favorited the movie")
    movieId: str = Field(..., description="ID of the favorited movie")

    model_config = ConfigDict(from_attributes=True)

    @classmethod
    def from_entity(cls, favorite):
        return cls(userId=favorite.userId, movieId=favorite.movieId)
