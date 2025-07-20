from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from blog.api.security import create_access_token
from blog.api.schemas.user_schema import (
    LoginInput,
    TokenResponse,
    user_to_output,
    UserCreateInput,
    UserOutput,
)
from blog.domain.entities.user import User
from blog.domain.value_objects.email_vo import Email
from blog.domain.value_objects.password import Password, PasswordValidationError
from blog.domain.repositories.user_repository import UserRepository
from blog.api.deps import get_user_repository, get_current_user
from blog.usecases.user.get_current_user import GetCurrentUserUseCase
from blog.usecases.user.login_user import LoginUserUseCase
from blog.usecases.user.logout_user import LogoutUserUseCase
from blog.usecases.user.register_user import RegisterUserUseCase
import uuid

security = HTTPBearer()
router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/register", response_model=UserOutput)
async def register_user(
    user: UserCreateInput, repo: UserRepository = Depends(get_user_repository)
):
    try:
        user_entity = User(
            id=str(uuid.uuid4()),
            name=user.username,
            email=Email(user.email),
            password=Password(user.password),
        )
    except PasswordValidationError as p:
        raise HTTPException(status_code=400, detail=str(p))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    usecase = RegisterUserUseCase(repo)
    try:
        new_user = await usecase.execute(user_entity)
    except HTTPException as e:
        # Propaga erros do usecase (como e-mail duplicado)
        raise e
    return UserOutput.from_entity(new_user)


@router.post("/login", response_model=TokenResponse)
async def login_user(
    login_data: LoginInput, repo: UserRepository = Depends(get_user_repository)
):
    try:
        usecase = LoginUserUseCase(repo)
        user = await usecase.execute(
            Email(login_data.email), Password(login_data.password)
        )

        if not user:
            raise HTTPException(status_code=404, detail="Usuário not found")

        token = create_access_token(data={"sub": str(user.id)})
        return TokenResponse(
            access_token=token,
            token_type="bearer",
            user=user_to_output(user),
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except HTTPException as e:
        raise e


@router.get("/me", response_model=UserOutput)
async def get_curr_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    user: User = Depends(get_current_user),
):
    try:
        return {"id": user.id, "username": user.name, "email": user.email.value()}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/logout")
async def logout_user(
    credentials=Depends(security), repo: UserRepository = Depends(get_user_repository)
):
    usecase = LogoutUserUseCase(repo)
    return await usecase.execute()
