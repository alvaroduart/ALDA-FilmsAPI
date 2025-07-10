from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from blog.domain.entities.user import User
from blog.domain.repositories.user_repository import UserRepository
from blog.infra.models.user_model import UserModel
from blog.domain.value_objects.email_vo import Email
from blog.domain.value_objects.password import Password


class SQLAlchemyUserRepository(UserRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, user_id: str) -> User:
        result = await self.session.execute(
            select(UserModel).where(UserModel.id == user_id)
        )
        user_model = result.scalar_one_or_none()
        if not user_model:
            raise ValueError("User not found")
        return user_model.to_entity()

    async def create(self, user: User) -> None:
        user_model = UserModel.from_entity(user)
        self.session.add(user_model)
        await self.session.commit()

    async def login(self, email: Email, password: Password) -> User:
        result = await self.session.execute(
            select(UserModel).where(
                UserModel.email == str(email),
                UserModel.password == str(password)
            )
        )
        user_model = result.scalar_one_or_none()
        if not user_model:
            raise ValueError("Invalid credentials")
        return user_model.to_entity()

    async def logout(self, user_id: str) -> None:        
        pass

    async def get_by_email(self, email: Email) -> User | None:
        result = await self.session.execute(
            select(UserModel).where(UserModel.email == str(email))
        )
        user_model = result.scalar_one_or_none()
        return user_model.to_entity() if user_model else None

    async def get_current_user(self, user_id: str) -> User:
        return await self.get_by_id(user_id)
