from sqlalchemy.ext.asyncio import AsyncSession
from blog.domain.entities.contact import Contact
from blog.domain.repositories.contact_repository import ContactRepository
from blog.infra.models.contact_model import ContactModel
from sqlalchemy.future import select


class SQLAlchemyContactRepository(ContactRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_contact(self, contact: Contact) -> Contact:
        contact_model = ContactModel.from_entity(contact)
        self.session.add(contact_model)
        await self.session.commit()
        return contact_model.to_entity()

    async def get_contact_by_id(self, contact_id: int) -> Contact | None:
        result = await self.session.execute(
            select(ContactModel).where(ContactModel.id == contact_id)
        )
        contact_model = result.scalar_one_or_none()
        return contact_model.to_entity() if contact_model else None
