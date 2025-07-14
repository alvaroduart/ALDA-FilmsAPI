from pydantic import BaseModel, Field, ConfigDict, EmailStr
from typing import Optional
from datetime import datetime


class ContactInput(BaseModel):
    name: str = Field(
        ...,
        min_length=10,
        max_length=100,
        description="Nome da pessoa que está entrando em contato",
    )
    email: EmailStr = Field(..., description="Endereço de e-mail da pessoa")
    message: str = Field(
        ..., min_length=10, max_length=2000, description="Conteúdo da mensagem enviada"
    )


class ContactOutput(BaseModel):
    id: str = Field(
        ...,
        min_length=8,
        max_length=36,
        description="Identificador único da mensagem de contato",
    )
    name: str = Field(
        ...,
        min_length=10,
        max_length=100,
        description="Nome da pessoa que entrou em contato",
    )
    email: EmailStr = Field(..., description="Endereço de e-mail da pessoa")
    message: str = Field(
        ..., min_length=10, max_length=2000, description="Conteúdo da mensagem enviada"
    )
    createdAt: datetime = Field(
        default_factory=datetime.now,
        description="Data e hora em que a mensagem de contato foi criada",
    )

    @classmethod
    def from_entity(cls, contact):
        return cls(
            id=contact.id,
            name=contact.name,
            email=contact.email,
            message=contact.message,
            createdAt=contact.createdAt,
        )
