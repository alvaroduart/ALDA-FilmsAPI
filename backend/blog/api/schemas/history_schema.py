from pydantic import BaseModel, Field, ConfigDict
from typing import Optional

class HistoryInput(BaseModel):
    userId: str = Field(..., description="ID of the user whose history is being recorded")
    movieId: str = Field(..., description="ID of the movie being added to the history")

class HistoryOutput(BaseModel):
    userId: str = Field(..., description="ID of the user who has the movie in their history")
    movieId: str = Field(..., description="ID of the movie in the user's history")    

    model_config = ConfigDict(from_attributes=True)

    @classmethod
    def from_entity(cls, history):
        return cls(
            userId=history.userId,
            movieId=history.movieId,
            
        )