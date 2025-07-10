from blog.domain.entities.contact import Contact
from blog.domain.repositories.contact_repository import ContactRepository
import pytest

class InMemoryContactRepository(ContactRepository):
    def __init__(self):
        self.contacts = {}

    @pytest.mark.asyncio
    async def create_contact(self, contact):
        return super().create_contact(contact)