from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List
from blog.usecases.contact import AddContactUseCase
from blog.usecases.contact.create_contact import CreateContactUseCase
from blog.domain.entities.contact import Contact
from blog.domain.entities.user import User
import uuid
from blog.api.schemas.contact_schema import AddContactInput, ContactOutput
from blog.domain.repositories.contact_repository import ContactRepository
from sqlalchemy.ext.asyncio import AsyncSession
from blog.api.deps import (
    get_db_session,
    get_user_repository,
    get_comment_repository,
    get_current_user,
)
from blog.infra.repositories.sqlalchemy.sqlalchemy_comment_repository import (
    SQLAlchemyCommentRepository,
)
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer()
router = APIRouter()

@router.post("/", response_model=ContactOutput)
async def add_contact(
    contact_input: AddContactInput,
    db: AsyncSession = Depends(get_db_session),
    contact_repository: ContactRepository = Depends(SQLAlchemyCommentRepository),
    current_user: User = Depends(get_current_user),
):
    use_case = CreateContactUseCase(contact_repository)
    contact = await use_case.execute(contact_input, current_user.id)
    return ContactOutput.from_entity(contact)

