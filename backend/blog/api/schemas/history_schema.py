from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from blog.api.schemas.movie_schema import MovieOutput


class HistoryInput(BaseModel):
    movieId: str = Field(..., description="ID of the movie being added to the history")


class HistoryOutput(BaseModel):
    userId: str = Field(
        ..., description="ID of the user who has the movie in their history"
    )
    # movieId: str = Field(..., description="ID of the movie in the user's history")
    movie: MovieOutput = Field(..., description="Movie details in the user's history")
    model_config = ConfigDict(from_attributes=True)

    @classmethod
    def from_entity(cls, history):
        return cls(
            userId=history.userId,
            movie=MovieOutput.from_entity(history.movie) if history.movie else None,
        )
