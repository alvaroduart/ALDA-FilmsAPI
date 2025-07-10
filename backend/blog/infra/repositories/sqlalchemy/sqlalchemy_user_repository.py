from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from blog.domain.entities.user import User
from blog.domain.repositories.user_repository import UserRepository
from blog.infra.models.user_model import UserModel
from blog.domain.value_objects.email_vo import Email
from blog.domain.value_objects.password import Password


class SQLAlchemyUserRepository(UserRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, user: User) -> None:
        user_model = UserModel.from_entity(user)
        self.session.add(user_model)
        await self.session.commit()

    async def get_by_email(self, email: Email) -> User | None:
        result = await self.session.execute(
            select(UserModel).where(UserModel.email == email.value())
        )
        user_model = result.scalar_one_or_none()
        return user_model.to_entity() if user_model else None

    async def get_current_user(self, user_id: str) -> User:
        result = await self.session.execute(
            select(UserModel).where(UserModel.id == user_id)
        )
        user_model = result.scalar_one_or_none()
        if user_model is None:
            raise ValueError("Usuário não encontrado")
        return user_model.to_entity()

    async def get_by_id(self, user_id: str) -> User:
        result = await self.session.execute(
            select(UserModel).where(UserModel.id == user_id)
        )
        user_model = result.scalar_one_or_none()
        if user_model is None:
            raise ValueError("Usuário não encontrado")
        return user_model.to_entity()

    async def login(self, email: Email, password: Password) -> User:
        result = await self.session.execute(
            select(UserModel).where(UserModel.email == email.value())
        )
        user_model = result.scalar_one_or_none()
        if user_model is None or user_model.password != password.value():
            raise ValueError("Credenciais inválidas")
        return user_model.to_entity()

    async def logout(self, user_id: str) -> None:
        # Não há lógica de logout persistente no banco (JWT é stateless)
        pass

    async def get_by_username(self, username: str) -> User | None:
        stmt = select(UserModel).where(UserModel.username == username)
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()
        return model.to_entity() if model else None

