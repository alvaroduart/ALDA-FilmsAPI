from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime
from blog.api.schemas.user_schema import UserOutput


class AddCommentInput(BaseModel):
    movieId: str = Field(
        ..., description="ID do filme ao qual o comentário está relacionado"
    )

    content: str = Field(
        ..., min_length=5, max_length=1000, description="Conteúdo do comentário"
    )


class UpdateCommentInput(BaseModel):
    id: str = Field(..., description="Identificador único do comentário")
    movieId: Optional[str] = Field(
        None, description="ID do filme ao qual o comentário está relacionado"
    )
    content: Optional[str] = Field(
        None, min_length=5, max_length=1000, description="Conteúdo do comentário"
    )


class DeleteCommentInput(BaseModel):
    id: str = Field(
        ...,
        min_length=8,
        max_length=36,
        description="Identificador único do comentário a ser excluído",
    )


class CommentOutput(BaseModel):
    id: str = Field(..., description="Identificador único do comentário")
    movieId: str = Field(
        ..., description="ID do filme ao qual o comentário está relacionado"
    )
    # serId: str = Field(..., description="ID do usuário que fez o comentário")
    user: UserOutput = Field(
        ..., description="Informações do usuário que fez o comentário"
    )
    userName: str = Field(
        ...,
        min_length=2,
        max_length=100,
        description="Nome do usuário que fez o comentário",
    )
    content: str = Field(
        ..., min_length=5, max_length=1000, description="Conteúdo do comentário"
    )
    createdAt: datetime = Field(
        default_factory=datetime.now,
        description="Data e hora em que o comentário foi criado",
    )

    model_config = ConfigDict(from_attributes=True)

    @classmethod
    def from_entity(cls, comment):
        return cls(
            id=comment.id,
            movieId=comment.movieId,
            # userId=comment.userId,
            user=UserOutput.from_entity(comment.user) if comment.user else None,
            userName=comment.userName,
            content=comment.content,
            createdAt=comment.createdAt,
        )
