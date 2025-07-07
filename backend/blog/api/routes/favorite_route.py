from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List
from blog.usecases.favorite import (
    
)
from blog.domain.entities.user import User
import uuid
from blog.api.schemas.favorite_schema 
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