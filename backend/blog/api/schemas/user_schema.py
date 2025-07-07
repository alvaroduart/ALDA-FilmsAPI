from pydantic import BaseModel, Field, EmailStr


class UserCreateInput(BaseModel):
    username: str = Field(..., min_length=3, max_length=50, description="Username of the user")
    email: EmailStr = Field(..., description="Email address of the user")
    password: str = Field(..., min_length=8, max_length=100, description="Password for the user account")
   

class LoginInput(BaseModel):
    email: EmailStr = Field(..., description="Email address of the user")
    password: str = Field(..., min_length=8, max_length=100, description="Password for the user account")

class SetCurrentUserInput(BaseModel):
    userId: str = Field(..., description="ID of the user to set as current user")

class UserOutput(BaseModel):
    id: str = Field(..., min_length=8, max_length=36, description="Unique identifier of the user")
    username: str = Field(..., min_length=3, max_length=50, description="Username of the user")
    email: EmailStr = Field(..., description="Email address of the user")
    favorites: list[str] = Field(default_factory=list, description="List of favorite movie IDs")
    history: list[str] = Field(default_factory=list, description="List of watched movie IDs")  

    @classmethod
    def from_entity(cls, user):
        return cls(
            id=user.id,
            username=user.name,
            email=user.email,
            favorites=user.favoriteMovies,
            history=user.watchedMovies
        )