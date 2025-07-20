from pydantic import BaseModel, Field, EmailStr
from blog.domain.entities.user import User


class UserCreateInput(BaseModel):
    username: str = Field(
        ..., min_length=3, max_length=50, description="Username of the user"
    )
    email: EmailStr = Field(..., description="Email address of the user")
    password: str = Field(
        ..., min_length=8, max_length=100, description="Password for the user account"
    )


class LoginInput(BaseModel):
    email: EmailStr = Field(..., description="Email address of the user")
    password: str = Field(
        ..., min_length=8, max_length=100, description="Password for the user account"
    )


class SetCurrentUserInput(BaseModel):
    userId: str = Field(..., description="ID of the user to set as current user")


class UserOutput(BaseModel):
    id: str = Field(
        ..., min_length=8, max_length=36, description="Unique identifier of the user"
    )
    username: str = Field(
        ..., min_length=3, max_length=50, description="Username of the user"
    )
    email: EmailStr = Field(..., description="Email address of the user")

    @classmethod
    def from_entity(cls, user):
        return cls(
            id=str(user.id),
            username=getattr(user, "username", getattr(user, "name", "")),
            email=user.email.value(),
        )


class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    user: UserOutput


def user_to_output(user: User) -> UserOutput:
    return UserOutput(
        id=str(user.id),
        username=getattr(user, "username", getattr(user, "name", "")),
        email=user.email.value(),
    )
