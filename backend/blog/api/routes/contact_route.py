from fastapi import APIRouter, Depends
from blog.api.schemas.contact_schema import ContactInput, ContactOutput
from blog.domain.entities.contact import Contact
from blog.domain.repositories.contact_repository import ContactRepository
from blog.api.deps import get_contact_repository
from blog.usecases.contact.create_contact import CreateContactUseCase

import uuid
from datetime import datetime

router = APIRouter(prefix="/contact", tags=["Contact"])

@router.post("/", response_model=ContactOutput)
async def create_contact(
    data: ContactInput,
    repo: ContactRepository = Depends(get_contact_repository)
):
    contact = Contact(
        id=str(uuid.uuid4()),
        name=data.name,
        email=str(data.email),
        message=data.message,
        createdAt=datetime.now()
    )
    usecase = CreateContactUseCase(repo)
    await usecase.execute(contact)
    return ContactOutput.from_entity(contact)
