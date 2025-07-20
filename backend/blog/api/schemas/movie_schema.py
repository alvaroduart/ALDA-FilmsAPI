from pydantic import BaseModel, Field
from typing import Optional
from pydantic import ConfigDict


class CreateMovieInput(BaseModel):
    movieid: str = Field(..., description="Identificador único do filme")
    title: str = Field(..., description="Título do filme")
    image: str = Field(..., description="URL da imagem do filme")
    rating: Optional[float] = Field(
        None,
        ge=0,
        le=5,
        description="Avaliação do filme (0 a 5 estrelas), se disponível",
    )
    description: str = Field(
        ..., min_length=10, max_length=2000, description="Descrição do filme"
    )
    genre: str = Field(..., min_length=3, max_length=50, description="Gênero do filme")
    duration: str = Field(..., description="Duração do filme no formato HH:MM:SS")
    director: str = Field(
        ..., min_length=3, max_length=100, description="Diretor do filme"
    )


class MovieOutput(BaseModel):
    id: str = Field(..., description="Identificador único do filme")
    title: str = Field(..., min_length=1, max_length=150, description="Título do filme")
    image: str = Field(..., description="URL da imagem do filme")
    rating: Optional[float] = Field(
        None,
        ge=0,
        le=5,
        description="Avaliação do filme (0 a 5 estrelas), se disponível",
    )
    description: str = Field(
        ..., min_length=10, max_length=2000, description="Descrição do filme"
    )
    genre: str = Field(..., min_length=3, max_length=50, description="Gênero do filme")
    duration: str = Field(..., description="Duração do filme no formato HH:MM:SS")
    director: str = Field(
        ..., min_length=3, max_length=100, description="Diretor do filme"
    )
    userRating: Optional[float] = Field(
        None,
        ge=0,
        le=5,
        description="Avaliação do usuário (0 a 5 estrelas), se disponível",
    )

    model_config = ConfigDict(from_attributes=True)

    @classmethod
    def from_entity(cls, movie, user_rating: Optional[float] = None) -> "MovieOutput":
        return cls(
            id=movie.id,
            title=movie.title,
            image=movie.image,
            rating=movie.rating,
            description=movie.description,
            genre=movie.genre,
            duration=movie.duration,
            director=movie.director,
            userRating=user_rating,
        )
