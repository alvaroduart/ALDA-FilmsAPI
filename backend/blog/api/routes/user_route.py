from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer
from blog.api.schemas.user_schema import UserOutput, LoginInput, UserCreateInput
from blog.domain.entities.user import User
from blog.domain.value_objects.email_vo import Email
from blog.domain.value_objects.password import Password
from blog.domain.repositories.user_repository import UserRepository
from blog.api.deps import get_user_repository
from blog.usecases.user.get_current_user import GetCurrentUserUseCase
from blog.usecases.user.login_user import LoginUserUseCase
from blog.usecases.user.logout_user import LogoutUserUseCase
from blog.usecases.user.register_user import RegisterUserUseCase

import uuid

security = HTTPBearer()
router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/register", response_model=UserOutput)
async def register_user(
    user: UserCreateInput,
    repo: UserRepository = Depends(get_user_repository)
) -> UserOutput:
    user_entity = User(
        id=str(uuid.uuid4()),
        name=user.username,
        email=Email(user.email),
        password=Password(user.password),
        favoriteMovies=[],
        watchedMovies=[]
    )
    usecase = RegisterUserUseCase(repo)
    new_user = await usecase.execute(user_entity)
    return UserOutput.from_entity(new_user)


@router.post("/login")
async def login_user(
    login_data: LoginInput,
    repo: UserRepository = Depends(get_user_repository)
) -> dict:
    usecase = LoginUserUseCase(repo)
    token = await usecase.execute(Email(login_data.email), Password(login_data.password))
    return {"access_token": token, "token_type": "bearer"}


@router.get("/me", response_model=UserOutput)
async def get_current_user(
    credentials=Depends(security),
    repo: UserRepository = Depends(get_user_repository)
) -> UserOutput:
    usecase = GetCurrentUserUseCase(repo)
    user = await usecase.execute(credentials)
    return UserOutput.from_entity(user)


@router.post("/logout")
async def logout_user(
    credentials=Depends(security),
    repo: UserRepository = Depends(get_user_repository)
) -> dict:
    usecase = LogoutUserUseCase(repo)
    await usecase.execute(credentials)
    return {"message": "User logged out successfully"}
