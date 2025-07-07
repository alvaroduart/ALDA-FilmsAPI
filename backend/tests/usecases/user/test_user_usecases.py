import pytest
from blog.domain.entities.user import User
from blog.domain.value_objects.email_vo import Email
from blog.domain.value_objects.password import Password
from blog.usecases.user.register_user import RegisterUserUseCase
from blog.usecases.user.login_user import LoginUserUseCase
from blog.usecases.user.get_user_by_id import GetUserByIdUseCase
from blog.usecases.user.logout_user import LogoutUserUseCase
from blog.usecases.user.forgot_password_user import ForgotPasswordUseCase
from blog.infra.repositories.in_memory.in_memory_user_repository import InMemoryUserRepository


def create_test_user():
    return User(
        id="1",
        name="Test User",
        email=Email("test.user@example.com"),
        password=Password("secure123")  
    )


def test_register_user():
    repo = InMemoryUserRepository()
    use_case = RegisterUserUseCase(repo)
    user = create_test_user()

    use_case.execute(user)

    stored_user = repo.get_by_id(user.id)
    assert stored_user.id == user.id
    assert stored_user.name == user.name
    assert stored_user.email.value() == user.email.value()
    assert stored_user.password.value() == user.password.value()


def test_login_user():
    repo = InMemoryUserRepository()
    register_use_case = RegisterUserUseCase(repo)
    user = create_test_user()
    register_use_case.execute(user)

    login_use_case = LoginUserUseCase(repo)
    email = Email("test.user@example.com")
    password = Password("secure123")

    result = login_use_case.execute(email, password)

    assert result.id == user.id
    assert result.name == user.name
    assert result.email.value() == user.email.value()
    assert result.password.value() == user.password.value()


def test_get_user_by_id():
    repo = InMemoryUserRepository()
    register_use_case = RegisterUserUseCase(repo)
    user = create_test_user()
    register_use_case.execute(user)

    get_user_use_case = GetUserByIdUseCase(repo)
    result = get_user_use_case.execute(user.id)

    assert result.id == user.id
    assert result.name == user.name
    assert result.email.value() == user.email.value()
    assert result.password.value() == user.password.value()


def test_logout_user():
    repo = InMemoryUserRepository()
    register_use_case = RegisterUserUseCase(repo)
    user = create_test_user()
    user = register_use_case.execute(user)

    logout_use_case = LogoutUserUseCase(repo)
    logout_use_case.execute(user.id)

    # Garantia de que o usuário ainda existe após logout
    get_user_use_case = GetUserByIdUseCase(repo)
    result = get_user_use_case.execute(user.id)

    assert result.id == user.id
    assert result.name == user.name
    assert result.email.value() == user.email.value()
    assert result.password.value() == user.password.value()


def test_forgot_password():
    repo = InMemoryUserRepository()
    register_use_case = RegisterUserUseCase(repo)
    user = register_use_case.execute(create_test_user())

    forgot_password_use_case = ForgotPasswordUseCase(repo)
    email = Email("test.user@example.com")
    
    forgot_password_use_case.execute(email)


 
