import pytest
from blog.domain.entities.contact import Contact
from blog.domain.repositories.contact_repository import ContactRepository
from blog.usecases.contact.create_contact import CreateContactUseCase
from blog.infra.repositories.in_memory.in_memory_contact_repository import (
    InMemoryContactRepository,
)


@pytest.mark.asyncio
async def test_create_contact_use_case():
    repo = InMemoryContactRepository()
    use_case = CreateContactUseCase(repo)

    contact = Contact(
        id="contact1",
        name="John Doe",
        email="john.doe@example.com",
        message="How can I reset my password?",
    )

    await use_case.execute(contact)

    assert len(repo.contacts) == 1
    assert repo.contacts["contact1"].name == "John Doe"
    assert repo.contacts["contact1"].email == "john.doe@example.com"
