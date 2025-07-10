from pydantic import BaseModel, Field, HttpUrl, ConfigDict
from typing import Optional, Annotated

class CreateMovieInput(BaseModel):
    movieid: Annotated[str, Field(description="Identificador único do filme")]
    title: Annotated[str, Field(description="Título do filme")]
    image: Annotated[HttpUrl, Field(description="URL da imagem do filme")]
    rating: Optional[Annotated[float, Field(ge=0, le=5, description="Avaliação do filme (0 a 5 estrelas), se disponível")]] = None
    description: Annotated[str, Field(min_length=10, max_length=2000, description="Descrição do filme")]
    genre: Annotated[str, Field(min_length=3, max_length=50, description="Gênero do filme")]
    duration: Annotated[str, Field(description="Duração do filme no formato HH:MM:SS")]
    director: Annotated[str, Field(min_length=3, max_length=100, description="Diretor do filme")]

class MovieOutput(BaseModel):
    id: Annotated[str, Field(description="Identificador único do filme")]
    title: Annotated[str, Field(min_length=1, max_length=150, description="Título do filme")]
    image: Annotated[HttpUrl, Field(description="URL da imagem do filme")]
    rating: Optional[Annotated[float, Field(ge=0, le=5, description="Avaliação do filme (0 a 5 estrelas), se disponível")]] = None
    description: Annotated[str, Field(min_length=10, max_length=2000, description="Descrição do filme")]
    genre: Annotated[str, Field(min_length=3, max_length=50, description="Gênero do filme")]
    duration: Annotated[str, Field(description="Duração do filme no formato HH:MM:SS")]
    director: Annotated[str, Field(min_length=3, max_length=100, description="Diretor do filme")]

    model_config = ConfigDict(from_attributes=True)

    @classmethod
    def from_entity(cls, movie):
        return cls(
            id=movie.id,
            title=movie.title,
            image=movie.image,
            rating=movie.rating,
            description=movie.description,
            genre=movie.genre,
            duration=movie.duration,
            director=movie.director
        )
