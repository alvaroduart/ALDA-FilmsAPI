import pytest
from blog.domain.entities.contact import Contact
from blog.domain.repositories.contact_repository import ContactRepository
from blog.usecases.contact.create_contact import CreateContactUseCase
from blog.infra.repositories.in_memory.in_memory_contact_repository import InMemoryContactRepository


def test_create_contact_use_case():
    repo = InMemoryContactRepository()
    use_case = CreateContactUseCase(repo)

    contact = Contact(name="John Doe", email="john.doe@example.com", question="How can I reset my password?")

    use_case.execute(contact)

    assert len(repo.contacts) == 1
    assert repo.contacts[0].name == "John Doe"
    assert repo.contacts[0].email == "john.doe@example.com"