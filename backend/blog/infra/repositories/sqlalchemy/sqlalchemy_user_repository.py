from sqlalchemy.ext.asyncio import AsyncSession
from blog.domain.entities.user import User
from blog.domain.repositories.user_repository import UserRepository
from blog.infra.models.user_model import UserModel
from sqlalchemy import select

class SQLAlchemyUserRepository(UserRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def register_user(self, user: User) -> User:
        user_model = UserModel.from_entity(user)
        self.session.add(user_model)
        await self.session.commit()
        return user_model.to_entity()
    
    async def get_user_by_id(self, user_id: int) -> User | None:
        result = await self.session.execute(
            select(UserModel).where(UserModel.id == user_id)
        )
        user_model = result.scalar_one_or_none()
        return user_model.to_entity() if user_model else None
    
    async def get_current_user(self, user_id: int) -> User | None:
        result = await self.session.execute(
            select(UserModel).where(UserModel.id == user_id)
        )
        user_model = result.scalar_one_or_none()
        return user_model.to_entity() if user_model else None
    
    async def login_user(self, email: str, password: str) -> User | None:
        result = await self.session.execute(
            select(UserModel).where(UserModel.email == email, UserModel.password == password)
        )
        user_model = result.scalar_one_or_none()
        return user_model.to_entity() if user_model else None
    
    async def logout_user(self, user_id: int) -> None:
        # In a real application, you might handle session invalidation here
        pass

    async def set_current_user(self, user_id: int) -> User | None:
        # This method would typically set the current user in the session context
        return await self.get_user_by_id(user_id)

    
    
    