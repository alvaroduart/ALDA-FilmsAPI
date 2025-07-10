from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer
from typing import List
from blog.api.schemas.history_schema import HistoryInput, HistoryOutput
from blog.domain.repositories.history_repository import HistoryRepository
from blog.api.deps import get_history_repository
from blog.usecases.history.add_to_history import AddToHistoryUseCase
from blog.usecases.history.get_user_history import GetUserHistoryUseCase
from blog.usecases.history.remove_from_history import RemoveFromHistoryUseCase

security = HTTPBearer()
router = APIRouter(prefix="/history", tags=["History"])

@router.post("/", response_model=HistoryOutput)
async def add_to_history(
    data: HistoryInput,
    credentials=Depends(security),
    repo: HistoryRepository = Depends(get_history_repository)
):
    usecase = AddToHistoryUseCase(repo)
    await usecase.execute(data.userId, data.movieId)
    return HistoryOutput(userId=data.userId, movieId=data.movieId)

@router.get("/{user_id}", response_model=List[HistoryOutput])
async def get_user_history(
    user_id: str,
    credentials=Depends(security),
    repo: HistoryRepository = Depends(get_history_repository)
):
    usecase = GetUserHistoryUseCase(repo)
    history = await usecase.execute(user_id)
    return [HistoryOutput.from_entity(h) for h in history]

@router.delete("/", status_code=204)
async def remove_from_history(
    data: HistoryInput,
    credentials=Depends(security),
    repo: HistoryRepository = Depends(get_history_repository)
):
    usecase = RemoveFromHistoryUseCase(repo)
    await usecase.execute(data.userId, data.movieId)
