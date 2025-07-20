import pytest
from blog.domain.entities.user import User
from blog.domain.value_objects.email_vo import Email
from blog.domain.value_objects.password import Password
from blog.usecases.user.register_user import RegisterUserUseCase
from blog.usecases.user.login_user import LoginUserUseCase
from blog.usecases.user.get_user_by_id import GetUserByIdUseCase
from blog.usecases.user.logout_user import LogoutUserUseCase
from blog.infra.repositories.in_memory.in_memory_user_repository import (
    InMemoryUserRepository,
)


def create_test_user():
    return User(
        id="1",
        name="Test User",
        email=Email("test.user@example.com"),
        password=Password("Secure123@"),
    )


@pytest.mark.asyncio
async def test_register_user():
    repo = InMemoryUserRepository()
    use_case = RegisterUserUseCase(repo)
    user = create_test_user()

    await use_case.execute(user)

    stored_user = await repo.get_by_id(user.id)
    assert stored_user.id == user.id
    assert stored_user.name == user.name
    assert stored_user.email == user.email


@pytest.mark.asyncio
async def test_login_user():
    repo = InMemoryUserRepository()
    register_use_case = RegisterUserUseCase(repo)
    user = create_test_user()
    await register_use_case.execute(user)

    login_use_case = LoginUserUseCase(repo)
    email = Email("test.user@example.com")
    password = Password("Secure123@")

    result = await login_use_case.execute(email, password)

    assert result.id == user.id
    assert result.name == user.name
    assert result.email == user.email


@pytest.mark.asyncio
async def test_get_user_by_id():
    repo = InMemoryUserRepository()
    register_use_case = RegisterUserUseCase(repo)
    user = create_test_user()
    await register_use_case.execute(user)

    get_user_use_case = GetUserByIdUseCase(repo)
    result = await get_user_use_case.execute(user.id)

    assert result.id == user.id
    assert result.name == user.name
    assert result.email.value() == user.email.value()


@pytest.mark.asyncio
async def test_logout_user():
    repo = InMemoryUserRepository()
    register_use_case = RegisterUserUseCase(repo)
    user = create_test_user()
    user = await register_use_case.execute(user)

    logout_use_case = LogoutUserUseCase(repo)
    await logout_use_case.execute()

    # Garantia de que o usuário ainda existe após logout
    get_user_use_case = GetUserByIdUseCase(repo)
    result = await get_user_use_case.execute(user.id)

    assert result.id == user.id
    assert result.name == user.name
    assert result.email == user.email
